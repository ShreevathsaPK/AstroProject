from skyfield.api import load
from datetime import datetime, timedelta
import math

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

# Example Usage
dob = "1999-05-10"
tob = "02:34:00"
latitude = 11.00
longitude = 76.58
tz_offset = 5.5  # IST (Indian Standard Time)

result = calculate_tithi_vara_yoga_nakshatra(dob, tob, latitude, longitude, tz_offset)
print(result)


