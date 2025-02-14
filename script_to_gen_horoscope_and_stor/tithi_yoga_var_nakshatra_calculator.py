import sqlite3
from skyfield.api import load
from datetime import datetime, timedelta
import math
from datetime import datetime
import pytz
from datetime import datetime, timezone

def convert_timezone(tz_offset):
    """
    Converts timezone string (e.g., 'Asia/Kolkata') to float UTC offset.
    If tz_offset is already a float, returns it directly.
    """
    try:
        # If already a float (numeric offset), return it
        return float(tz_offset)
    except ValueError:
        pass  # Means tz_offset is a string

    try:
         # Get timezone object
        tz = pytz.timezone(tz_offset)
        
        # Get current UTC time and convert to the given timezone
        now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
        local_time = now_utc.astimezone(tz)

        # Get UTC offset in hours
        utc_offset = local_time.utcoffset().total_seconds() / 3600
        return 5.5
    except Exception as e:
        print(f"Error: Invalid timezone '{tz_offset}' - {e}")
        return None  # Handle errors gracefully

def convert_datetime(date_str, time_str):
    """
    Convert date ('DD/MM/YYYY') and time ('hh:mm AM/PM' or 'HH:MM:SS')
    into standard 'YYYY-MM-DD HH:MM:SS' format.
    """
    date_format = "%d/%m/%Y"  # Fixed date format: DD/MM/YYYY
    time_formats = ["%I:%M %p", "%H:%M:%S"]  # 12-hour AM/PM & 24-hour formats
    
    # Parse the date
    try:
        parsed_date = datetime.strptime(date_str, date_format).date()
    except ValueError:
        print(f"Error: Unable to parse date {date_str}")
        return None

    # Try parsing the time in both formats
    for time_fmt in time_formats:
        try:
            parsed_time = datetime.strptime(time_str, time_fmt).time()
            break
        except ValueError:
            continue
    else:
        print(f"Error: Unable to parse time {time_str}")
        return None

    # Combine parsed date and time into a single datetime object
    final_datetime = datetime.combine(parsed_date, parsed_time)
    return final_datetime.strftime("%Y-%m-%d %H:%M:%S")  # Standard format
    
# Load ephemeris data
eph = load('de421.bsp')

# Define constants for Tithi, Vara, Nakshatra, and Yoga
TITHIS = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami",
    "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
]
VARS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
    "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]
YOGAS = [
    "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti",
    "Shula", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi",
    "Vyatipata", "Variyan", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti"
]

# Lahiri Ayanamsha (approximate, dynamically varies with time)
def get_lahiri_ayanamsha(year):
    return 23.85  # This should ideally be calculated dynamically

def calculate_tithi_vara_yoga_nakshatra(dob, tob, latitude, longitude, tz_offset):
    # Convert input date and time to UTC datetime object
    dt_str = f"{dob} {tob}"
    dt_utc = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S") - timedelta(hours=tz_offset)

    # Convert to Julian Date using Skyfield
    ts = load.timescale()
    jd = ts.utc(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour, dt_utc.minute, dt_utc.second)

    # Load planetary positions
    earth = eph['earth']
    sun = eph['sun']
    moon = eph['moon']

    # Get observer position from Earth
    observer = earth.at(jd)

    # Compute Sun and Moon apparent positions
    sun_apparent = observer.observe(sun).apparent()
    moon_apparent = observer.observe(moon).apparent()

    # Extract tropical ecliptic longitudes
    sun_lon_tropical = sun_apparent.ecliptic_latlon()[1].degrees % 360
    moon_lon_tropical = moon_apparent.ecliptic_latlon()[1].degrees % 360

    # Apply Lahiri Ayanamsha to get sidereal longitude
    ayanamsha = get_lahiri_ayanamsha(dt_utc.year)
    sun_lon = (sun_lon_tropical - ayanamsha) % 360
    moon_lon = (moon_lon_tropical - ayanamsha) % 360

    # Calculate Tithi
    tithi_index = int(((moon_lon - sun_lon) % 360) / 12) % 15
    tithi = TITHIS[tithi_index]

    # Calculate Vara (Weekday)
    jd_local = jd.tt + (tz_offset / 24.0)  # Adjust for local timezone
    vara_index = int(jd_local + 0.5) % 7  # Corrected formula
    vara = VARS[vara_index]

    # Calculate Nakshatra
    nakshatra_index = math.floor(moon_lon / 13.3333) % 27
    nakshatra = NAKSHATRAS[nakshatra_index]

    # Calculate Yoga
    yoga_index = math.floor(((sun_lon + moon_lon) % 360) / (360 / 27))
    yoga = YOGAS[yoga_index]

    # Return result
    return {
        "Tithi": tithi,
        "Vara": vara,
        "Nakshatra": nakshatra,
        "Yoga": yoga
    }

# Function to fetch all personal info from the database
def get_all_personal_info(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT name, date, time, latitude, longitude, timezone FROM personal_info"
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.close()
    
    return results

# Example Usage
db_path = "horoscope.db"  # Update with actual DB path
all_people = get_all_personal_info(db_path)
results_dict =[]
if all_people:
    for person in all_people:
        name, dob, tob, latitude, longitude, tz_offset = person
        #print(dob)
        #print(tob)
        converted_datetime = convert_datetime(dob, tob)
        dob = converted_datetime[:10]
        tob = converted_datetime[11:]

        tz_offset = convert_timezone(tz_offset)
        
       #print(f"tddd {tz_offset}")
        # kNOTE DID N"T USE THE TIMEZONE OFFSET VALUE COZ IT WAS GIVING WRONG VALUES SO THIS IS APPLICABLE TO ONLY INDIA LOCATION
        result = calculate_tithi_vara_yoga_nakshatra(dob, tob, latitude, longitude, 5.5)
        #print(f"Results for {name}: {result}")
        results_dict.append([name,result])
else:
    print("No records found in the database.")

print('''
    1. Tithi Search
    2. Vaar Search
    3. Yoga Search
    4. Karan Search #Yet to be implemented
    5. Nakshatra Search
''')
s_key = int(input("search mode"))
if(s_key == 1):
    print(TITHIS)
    tithi_selection = input("Enter tithi to search")
    for k in results_dict:
        if(k[1]['Tithi']==tithi_selection):
            print(k)
if(s_key == 2):
    print(VARS)
    var_selection = input("Enter Var to search")
    for k in results_dict:
        if(k[1]['Vara']==var_selection):
            print(k)
if(s_key == 3):
    print(YOGAS)
    yoga_selection = input("Enter Yoga to search")
    for k in results_dict:
        if(k[1]['Yoga']==yoga_selection):
            print(k)
if(s_key == 5):
    print(NAKSHATRAS)
    naks_selection = input("Enter Nakshatra to search")
    for k in results_dict:
        if(k[1]['Nakshatra']==naks_selection):
            print(k)
print(calculate_tithi_vara_yoga_nakshatra('2000-02-21', '10:34:38', latitude, longitude, 5.5))