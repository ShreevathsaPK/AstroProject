from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

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

# ------------------- API ROUTES -------------------

@app.route("/query1")
def api_query1():
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
def api_query2():
    planet = request.args.get("planet")
    conn = create_connection()
    rows = query_planet_by_retrograde(conn, planet, "Retro")
    conn.close()
    
    result = [row[1] for row in rows]  # your final output
    print(result)  # terminal
    return str(result)   # browser shows only this

@app.route("/query3")
def api_query3():
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
def api_query4():
    x = int(request.args.get("x"))
    y = int(request.args.get("y"))

    conn = create_connection()
    rows = query_xth_lord_in_yth_house(conn, x, y)
    conn.close()

    result = [row['name'] for row in rows]
    print(result)
    return str(result)

@app.route("/query5")
def api_query5():
    planets = request.args.get("planets").split(",")
    conn = create_connection()
    rows = query_planets_in_conjunction(conn, planets)
    conn.close()
    result = [row['name'] for row in rows]
    print(result)
    return str(result)

# ------------------- Start Flask -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009)
