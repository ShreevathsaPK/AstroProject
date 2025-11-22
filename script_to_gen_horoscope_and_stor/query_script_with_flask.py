from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set template folder to project root (one level up from this script)
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

# Configure SQLAlchemy to use an Azure DB if provided via env var `DATABASE_URL`.
# Fallback to the local sqlite file `horoscope.db` for development.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///horoscope.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT secret key for signing tokens (use env var in production)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Initialize SQLAlchemy for user/auth storage
db = SQLAlchemy(app)


# User model for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat()
        }

 
# ------------------- Auth Decorator -------------------
def token_required(f):
    """Decorator to protect endpoints. Checks for valid JWT token in Authorization header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check for token in Authorization header: "Bearer <token>"
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'invalid authorization header format'}), 401

        if not token:
            return jsonify({'error': 'token required'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'invalid token'}), 401

        # Pass user_id to the route function if needed
        return f(current_user_id, *args, **kwargs)
    return decorated


# ------------------- Authentication Routes -------------------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400

    # Check if user already exists
    existing = User.query.filter_by(username=username).first()
    if existing:
        return jsonify({'error': 'user already exists'}), 409

    # Hash password (werkzeug's generate_password_hash uses a salt)
    pw_hash = generate_password_hash(password)
    user = User(username=username, password_hash=pw_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'user created', 'user': user.to_dict()}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'invalid credentials'}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'invalid credentials'}), 401

    # Auth successful. Issue JWT token valid for 24 hours.
    token = jwt.encode(
        {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    return jsonify({
        'message': 'login successful',
        'user': user.to_dict(),
        'token': token
    }), 200

# ------------------- End Authentication Routes -------------------

# Array of zodiac signs and their respective house lords
zodiac_owners = {
    'Aries': ['Mars'], 'Taurus': ['Venus'], 'Gemini': ['Mercury'], 'Cancer': ['Moon'],
    'Leo': ['Sun'], 'Virgo': ['Mercury'], 'Libra': ['Venus'], 'Scorpio': ['Mars', 'Ketu'],
    'Sagittarius': ['Jupiter'], 'Capricorn': ['Saturn'], 'Aquarius': ['Saturn', 'Rahu'],
    'Pisces': ['Jupiter']
}

def create_connection():
    conn = sqlite3.connect('horoscope.db')
    conn.row_factory = sqlite3.Row
    return conn

# ------------------- Your Query Functions (unchanged) -------------------

def query_planet_by_house_or_sign(conn, planet, house=None, sign=None):
    cursor = conn.cursor()

    if house:
        cursor.execute('''
            SELECT DISTINCT personal_info.*, planet_data.* 
            FROM personal_info 
            JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
            WHERE planet_data.planet = ? AND planet_data.house = ?
        ''', (planet, house))
    elif sign:
        cursor.execute('''
            SELECT DISTINCT personal_info.*, planet_data.* 
            FROM personal_info 
            JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
            WHERE planet_data.planet = ? AND planet_data.sign = ?
        ''', (planet, sign))
    else:
        return []

    return cursor.fetchall()

def query_planet_by_retrograde(conn, planet, retro_status):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT personal_info.*, planet_data.* 
        FROM personal_info 
        JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
        WHERE planet_data.planet = ? AND planet_data.retro = ?
    ''', (planet, retro_status))
    return cursor.fetchall()

def query_planets_in_same_sign_or_house(conn, planets, house, sign, querymode):
    cursor = conn.cursor()
    placeholders = ', '.join('?' for _ in planets)

    if querymode == "1":
        query = f'''
            SELECT personal_info.*, planet_data.house, planet_data.sign
            FROM personal_info
            JOIN planet_data ON personal_info.id = planet_data.personal_info_id
            WHERE planet_data.sign = ?
              AND planet_data.planet IN ({placeholders})
            GROUP BY personal_info.id, planet_data.house, planet_data.sign
            HAVING COUNT(DISTINCT planet_data.planet) = ?
        '''
        params = [sign] + planets + [len(planets)]
    else:
        query = f'''
            SELECT personal_info.*, planet_data.house, planet_data.sign
            FROM personal_info
            JOIN planet_data ON personal_info.id = planet_data.personal_info_id
            WHERE planet_data.house = ?
              AND planet_data.planet IN ({placeholders})
            GROUP BY personal_info.id, planet_data.house, planet_data.sign
            HAVING COUNT(DISTINCT planet_data.planet) = ?
        '''
        params = [house] + planets + [len(planets)]

    cursor.execute(query, params)
    return cursor.fetchall()

def query_xth_lord_in_yth_house(conn, xth_house, yth_house):
    cursor = conn.cursor()
    zodiac_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                   'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    results = []
    cursor.execute('''SELECT personal_info.*, planet_data.* 
                      FROM personal_info 
                      JOIN planet_data ON personal_info.id = planet_data.personal_info_id
                      WHERE planet_data.planet = 'Ascendant' ''')
    entries = cursor.fetchall()

    for entry in entries:
        asc = entry['sign']  
        asc_index = zodiac_list.index(asc)

        x_index = (asc_index + (xth_house - 1)) % 12
        lords = zodiac_owners[zodiac_list[x_index]]

        for lord in lords:
            cursor.execute('''
                SELECT personal_info.*, planet_data.* 
                FROM personal_info 
                JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
                WHERE planet_data.planet = ? AND planet_data.house = ?
                  AND personal_info.id = ?
            ''', (lord, yth_house, entry['id']))
            lord_results = cursor.fetchall()
            results.extend(lord_results)

    return results

def query_planets_in_conjunction(conn, planets):
    cursor = conn.cursor()
    placeholders = ', '.join('?' for _ in planets)
    query = f'''
        SELECT personal_info.*, planet_data.house
        FROM personal_info
        JOIN planet_data ON personal_info.id = planet_data.personal_info_id
        WHERE planet_data.planet IN ({placeholders})
        GROUP BY personal_info.id, planet_data.house
        HAVING COUNT(DISTINCT planet_data.planet) = ?
    '''
    params = planets + [len(planets)]
    cursor.execute(query, params)
    return cursor.fetchall()

# ------------------- Static HTML Route -------------------
@app.route('/', methods=['GET'])
def index():
    """Serve the login/signup HTML page."""
    return render_template('index.html')

# ------------------- Protected Astrology Query Routes (JWT Required) -------------------

@app.route("/query1")
@token_required
def api_query1(current_user_id):
    planet = request.args.get("planet")
    house = request.args.get("house")
    sign = request.args.get("sign")

    conn = create_connection()
    rows = query_planet_by_house_or_sign(conn, planet, house, sign)
    conn.close()

    result = [row['name'] for row in rows]
    print(result)
    return str(result)

@app.route("/query2")
@token_required
def api_query2(current_user_id):
    planet = request.args.get("planet")
    conn = create_connection()
    rows = query_planet_by_retrograde(conn, planet, "Retro")
    conn.close()
    
    result = [row[1] for row in rows]  # your final output
    print(result)  # terminal
    return str(result)   # browser shows only this

@app.route("/query3")
@token_required
def api_query3(current_user_id):
    planets = request.args.get("planets").split(",")
    house = request.args.get("house")
    sign = request.args.get("sign")
    mode = request.args.get("mode")  # "1" or "2"

    conn = create_connection()
    rows = query_planets_in_same_sign_or_house(conn, planets, house, sign, mode)
    conn.close()

    result = [row['name'] for row in rows]
    print(result)
    return str(result)

@app.route("/query4")
@token_required
def api_query4(current_user_id):
    x = int(request.args.get("x"))
    y = int(request.args.get("y"))

    conn = create_connection()
    rows = query_xth_lord_in_yth_house(conn, x, y)
    conn.close()

    result = [row['name'] for row in rows]
    print(result)
    return str(result)

@app.route("/query5")
@token_required
def api_query5(current_user_id):
    planets = request.args.get("planets").split(",")
    conn = create_connection()
    rows = query_planets_in_conjunction(conn, planets)
    conn.close()
    result = [row['name'] for row in rows]
    print(result)
    return str(result)

# ------------------- Start Flask -------------------
if __name__ == "__main__":
    # Ensure user table exists (works for Azure DB or local sqlite fallback)
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5009)
