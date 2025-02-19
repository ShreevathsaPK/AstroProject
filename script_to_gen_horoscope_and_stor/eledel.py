import sqlite3
from skyfield.api import load
from datetime import datetime, timedelta
import math
import pytz
from datetime import timezone

def convert_timezone(tz_offset):
    try:
        return float(tz_offset)
    except ValueError:
        pass  
    try:
        tz = pytz.timezone(tz_offset)
        now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
        local_time = now_utc.astimezone(tz)
        return 5.5
    except Exception as e:
        print(f"Error: Invalid timezone '{tz_offset}' - {e}")
        return None

def convert_datetime(date_str, time_str):
    date_format = "%d/%m/%Y"
    time_formats = ["%I:%M %p", "%H:%M:%S"]
    try:
        parsed_date = datetime.strptime(date_str, date_format).date()
    except ValueError:
        print(f"Error: Unable to parse date {date_str}")
        return None
    for time_fmt in time_formats:
        try:
            parsed_time = datetime.strptime(time_str, time_fmt).time()
            break
        except ValueError:
            continue
    else:
        print(f"Error: Unable to parse time {time_str}")
        return None
    return datetime.combine(parsed_date, parsed_time).strftime("%Y-%m-%d %H:%M:%S")

eph = load('de421.bsp')
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



def get_lahiri_ayanamsha(year):
    return 23.85

def calculate_tithi_vara_yoga_nakshatra_karan(dob, tob, latitude, longitude, tz_offset):
    dt_str = f"{dob} {tob}"
    dt_utc = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S") - timedelta(hours=tz_offset)
    ts = load.timescale()
    jd = ts.utc(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour, dt_utc.minute, dt_utc.second)
    earth = eph['earth']
    sun = eph['sun']
    moon = eph['moon']
    observer = earth.at(jd)
    sun_apparent = observer.observe(sun).apparent()
    moon_apparent = observer.observe(moon).apparent()
    sun_lon_tropical = sun_apparent.ecliptic_latlon()[1].degrees % 360
    moon_lon_tropical = moon_apparent.ecliptic_latlon()[1].degrees % 360
    ayanamsha = get_lahiri_ayanamsha(dt_utc.year)
    sun_lon = (sun_lon_tropical - ayanamsha) % 360
    moon_lon = (moon_lon_tropical - ayanamsha) % 360
    tithi_index = int(((moon_lon - sun_lon) % 360) / 12) % 15
    tithi = TITHIS[tithi_index]
    jd_local = jd.tt + (tz_offset / 24.0)
    vara_index = int(jd_local + 0.5) % 7
    vara = VARS[vara_index]
    nakshatra_index = math.floor(moon_lon / 13.3333) % 27
    nakshatra = NAKSHATRAS[nakshatra_index]
    yoga_index = math.floor(((sun_lon + moon_lon) % 360) / (360 / 27))
    yoga = YOGAS[yoga_index]
    
  
    
    return {
        "Tithi": tithi,
        "Vara": vara,
        "Nakshatra": nakshatra,
        "Yoga": yoga,
        "Karan": karan  # MODIFIED: Added Karan
    }

def get_all_personal_info(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, date, time, latitude, longitude, timezone FROM personal_info")
    results = cursor.fetchall()
    conn.close()
    return results

db_path = "horoscope.db"
all_people = get_all_personal_info(db_path)
results_dict = []
if all_people:
    for person in all_people:
        name, dob, tob, latitude, longitude, tz_offset = person
        converted_datetime = convert_datetime(dob, tob)
        dob = converted_datetime[:10]
        tob = converted_datetime[11:]
        tz_offset = convert_timezone(tz_offset)
        result = calculate_tithi_vara_yoga_nakshatra_karan(dob, tob, latitude, longitude, 5.5)
        results_dict.append([name, result])

print("""
    1. Tithi Search
    2. Vaar Search
    3. Yoga Search
    4. Karan Search  # MODIFIED: Implemented Karan Search
    5. Nakshatra Search
""")
s_key = int(input("Search mode: "))
if s_key == 4:
    print(KARANS)
    karan_selection = input("Enter Karan to search: ")
    for k in results_dict:
        if k[1]['Karan'] == karan_selection:
            print(k[0])
