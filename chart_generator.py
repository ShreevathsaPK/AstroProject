import swisseph as swe
import datetime
import os
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pandas as pd  # Import pandas to work with Excel files

os.environ['SWISSEPH_DIR'] = '/workspace/AstroProject/'

# Set the path for the Swiss Ephemeris files
swe.set_ephe_path('/workspace/AstroProject/')

# Set sidereal mode with Lahiri Ayanamsha for Vedic astrology
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Calculate combust status
def check_combust(planet, planet_degree, sun_degree):

    combust_ranges = {
            swe.MERCURY: 8,
            swe.VENUS: 8,
            swe.MARS: 7,
            swe.JUPITER: 11,
            swe.SATURN: 15,
            swe.MOON: 12,
        }
    
    if planet in combust_ranges:
        if abs(planet_degree - sun_degree) <= combust_ranges[planet]:
            return "Combust"
    return "No"

def calculate_house(ascendant_sign, planet_sign):
    # Zodiac signs mapped to numbers
    signs = {
        "Aries": 1, "Taurus": 2, "Gemini": 3, "Cancer": 4, "Leo": 5, "Virgo": 6,
        "Libra": 7, "Scorpio": 8, "Sagittarius": 9, "Capricorn": 10, "Aquarius": 11, "Pisces": 12
    }

    # Convert signs to numbers
    asc_num = signs[ascendant_sign]
    planet_num = signs[planet_sign]

    # Calculate the house
    house = (planet_num - asc_num + 1) % 12 
    if house == 0:
        house = 12  # Adjust for the case where it wraps around

    return house

def calculate_planet_positions(jd, ascendant_degree,asc_sign):
    """Calculate positions for planets, their signs, degrees, retrograde status, and more."""
    planets_data = []

    # Planets to include (using Swiss Ephemeris constants)
    planets = [ swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
               swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO, swe.MEAN_NODE, swe.TRUE_NODE]
    for planet in planets:
        # Get planet data with sidereal flag applied
        planet_info = swe.calc_ut(jd, planet, swe.FLG_SIDEREAL | swe.FLG_SPEED)
        degree = planet_info[0][0]  # Longitude in sidereal degrees

        # Adjust degree for Rahu (mean node) and Ketu (true node)
        if swe.get_planet_name(planet) == "true Node":
            degree = (degree + 180) % 360

        # Check retrograde status if the tuple has sufficient length
        retrograde = "Direct"
        if  planet_info[0][3] < 0:
            retrograde = "Retro"

        # Calculate sign
        sign, sign_lord = get_sign_and_lord(degree)

        # Nakshatra and its lord
        nakshatra, naksh_lord = get_nakshatra(degree)

        # Combust and Avastha (example placeholder values)
        # Define combust ranges in degrees for each planet
        
        combust = "No"

        sun_info = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL | swe.FLG_SPEED)
        sun_degree = sun_info[0][0]  # Longitude in sidereal degrees
        combust = check_combust(planet, degree, sun_degree)

        avastha = "Yuva"  # Default example; you may add specific calculations for avastha

        # Determine the house relative to the Ascendant
        #house = ((int((degree - ascendant_degree) / 30) - 1) % 12) + 1 old logic buggy.
        house = calculate_house(asc_sign, sign)


        # Status placeholder
        status = "--"  # Adjust as needed based on specific conditions

        planets_data.append({
            "Planet": "Rahu" if swe.get_planet_name(planet) == "mean Node" else (
                "Ketu" if swe.get_planet_name(planet) == "true Node" else swe.get_planet_name(planet)),
            "Sign": sign,
            "Sign Lord": sign_lord,
            "Nakshatra": nakshatra,
            "Naksh Lord": naksh_lord,
            "Degree": degree,
            "Retro(R)": retrograde,
            "Combust": combust,
            "Avastha": avastha,
            "House": house,
            "Status": status
        })

    return planets_data

def calculate_ascendant(jd, latitude, longitude):
    """Calculate the sidereal Ascendant (Lagna) using Swiss Ephemeris and Lahiri Ayanamsha."""
    # Set sidereal mode to use Lahiri Ayanamsha
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # Calculate houses and cusps in tropical, then adjust for sidereal
    houses_info, ascendant_cusps = swe.houses(jd, latitude, longitude, b'S')  # 'A' for Placidus
    
    # First cusp (Ascendant) in tropical coordinates
    ascendant_tropical = ascendant_cusps[0]

    # Convert tropical to sidereal by adjusting with ayanamsha
    ayanamsha = swe.get_ayanamsa(jd)
    
    sidereal_ascendant = (ascendant_tropical - ayanamsha  ) % 360

    return sidereal_ascendant



def get_sign_and_lord(degree):
    """Determine sign and its lord based on degree."""
    signs = [
        ("Aries", "Mars"), ("Taurus", "Venus"), ("Gemini", "Mercury"), ("Cancer", "Moon"),
        ("Leo", "Sun"), ("Virgo", "Mercury"), ("Libra", "Venus"), ("Scorpio", "Mars"),
        ("Sagittarius", "Jupiter"), ("Capricorn", "Saturn"), ("Aquarius", "Saturn"), ("Pisces", "Jupiter")
    ]
    sign_index = int(degree / 30)
    return signs[sign_index]

def get_nakshatra(degree):
    """Determine the nakshatra and its lord based on degree."""
    nakshatras = [
        ("Ashwini", "Ketu"), ("Bharani", "Venus"), ("Krittika", "Sun"),
        ("Rohini", "Moon"), ("Mrigashira", "Mars"), ("Ardra", "Rahu"),
        ("Punarvasu", "Jupiter"), ("Pushya", "Saturn"), ("Ashlesha", "Mercury"),
        ("Magha", "Ketu"), ("Purva Phalguni", "Venus"), ("Uttara Phalguni", "Sun"),
        ("Hasta", "Moon"), ("Chitra", "Mars"), ("Swati", "Rahu"),
        ("Vishakha", "Jupiter"), ("Anuradha", "Saturn"), ("Jyeshtha", "Mercury"),
        ("Moola", "Ketu"), ("Purva Ashadha", "Venus"), ("Uttara Ashadha", "Sun"),
        ("Shravana", "Moon"), ("Dhanishta", "Mars"), ("Shatabhisha", "Rahu"),
        ("Purva Bhadrapada", "Jupiter"), ("Uttara Bhadrapada", "Saturn"), ("Revati", "Mercury")
    ]
    index = int((degree % 360) // (360 / 27)) % 27  # Ensure index stays within bounds
    return nakshatras[index]

def calculate_julian_day(year, month, day, hour, minute, second):
    """Calculate Julian Day from date and time."""
    return swe.julday(year, month, day, hour + (minute / 60) + (second / 3600))



def get_lat_long_from_location(location_name):
    # Initialize the geolocator
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(location_name)
    
    # Check if location is found
    if location:
        return location.latitude, location.longitude
    else:
        print("Location not found. Please enter a valid location.")
        return None, None

def get_timezone(latitude, longitude):
    # Initialize the timezone finder
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    
    if timezone_str:
        return pytz.timezone(timezone_str)
    else:
        print("Timezone could not be determined.")
        return None

def main():
    # Input for date and time of birth
    name = input("Enter name of the Person")
    date_of_birth = input("Enter Date of Birth (YYYY-MM-DD): ")
    time_of_birth = input("Enter Time of Birth (HH:MM:SS): ")
    location_name = input("Enter Place of Birth (City, Country): ")
    
    # Get latitude and longitude from location
    latitude, longitude = get_lat_long_from_location(location_name)
    if latitude is None or longitude is None:
        return  # Exit if location was not found

    # Get timezone based on latitude and longitude
    local_tz = get_timezone(latitude, longitude)
    if local_tz is None:
        return  # Exit if timezone could not be determined

    # Parse date and time
    dob = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
    tob = datetime.datetime.strptime(time_of_birth, "%H:%M:%S")
    local_dt = local_tz.localize(datetime.datetime.combine(dob, tob.time()))

    # Convert to UTC
    utc_dt = local_dt.astimezone(pytz.utc)

    # Calculate Julian Day in UTC
    jd = calculate_julian_day(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute, utc_dt.second)

    # Calculate Ascendant
    ascendant_degree = calculate_ascendant(jd, latitude, longitude)
    asc_sign, asc_lord = get_sign_and_lord(ascendant_degree)

    # Information to be added to "Sheet 1"
    sheet1_data = {
        "Name": name,
        "Date": dob.strftime("%d/%m/%Y"),
        "Time": tob.strftime("%H:%M:%S"),
        "Place": location_name,
        "Latitude": latitude,
        "Longitude": longitude,
        "Timezone": "tobefilled GMT+5.5",
        "Sunrise": "tobefilled",
        "Sunset": "tobefilled",
        "Ayanamsha": "tobefilled"
    }

    # Convert to DataFrame to write into Excel
    sheet1_df = pd.DataFrame(list(sheet1_data.items()))


    # Prepare ascendant data for DataFrame
    ascendant_data = [{
        "Planet": "Ascendant",
        "Sign": asc_sign,
        "Sign Lord": asc_lord,
        "Nakshatra": "--",
        "Naksh Lord": "--",
        "Degree": ascendant_degree % 30,
        "Retro(R)": "--",
        "Combust": "--",
        "Avastha": "--",
        "House": 1,
        "Status": "--"
    }]

    # Display Ascendant information
    print(f"{'Planet':<10}{'Sign':<10}{'Sign Lord':<10}{'Nakshatra':<15}{'Naksh Lord':<10}{'Degree':<10}{'Retro(R)':<10}{'Combust':<10}{'Avastha':<10}{'House':<10}{'Status':<10}")
    print(f"{'Ascendant':<10}{asc_sign:<10}{asc_lord:<10}{'--':<15}{'--':<10}{ascendant_degree%30:<10.2f}{'--':<10}{'--':<10}{'--':<10}{'1':<10}{'--':<10}")

    # Calculate planetary data
    planetary_data = calculate_planet_positions(jd, ascendant_degree,asc_sign)

    # Combine ascendant and planetary data
    all_data = ascendant_data + planetary_data
    # Convert data to DataFrame
    df = pd.DataFrame(all_data)
    planetary_data_df =  df.iloc[1:]  # Get all rows after the first as Planet data
    ascendant_data_df = df.iloc[0:1]  # Get the first row as Ascendant data
    
    # Assuming sheet1_df, ascendant_data_df, and planetary_data_df are already defined

    with pd.ExcelWriter("nameoftheperson_chartgen.xlsx", engine="openpyxl") as writer:
        
        # Write "Sheet 1" data starting from the second row with a title in the first row
        sheet1_df.to_excel(writer, sheet_name="Sheet 1", index=False, header=False, startrow=1)
        worksheet1 = writer.sheets['Sheet 1']
        
        # Merge cells across 7 columns in the first row for "Table 1" title
        worksheet1.merge_cells(start_row=1, start_column=1, end_row=1, end_column=7)
        worksheet1.cell(row=1, column=1, value="Table 1") 

        # Write "Sheet 2" data, leaving space for title and ascendant data
        worksheet2 = writer.book.create_sheet(title="Sheet 2")
        
        # Add a title "Table 1" in the first row, merged across 11 columns
        worksheet2.merge_cells(start_row=1, start_column=1, end_row=1, end_column=11)
        worksheet2.cell(row=1, column=1, value="Table 1")
        ####
        planetary_headers = list(planetary_data_df.columns)
        # Write Ascendant headers in row 2
        for col_idx, header in enumerate(planetary_headers, start=1):
            worksheet2.cell(row=2, column=col_idx, value=header)
        ####
        # Write Ascendant data starting from row 3
        for col_idx, value in enumerate(ascendant_data_df.iloc[0], start=1):  # Assuming first row contains the ascendant data
            worksheet2.cell(row=3, column=col_idx, value=value)

        # Write planetary data starting from row 3
        for row_idx, row in planetary_data_df.iterrows():
            for col_idx, value in enumerate(row, start=1):
                worksheet2.cell(row=row_idx + 3, column=col_idx, value=value)

    # Now the file will save automatically upon exiting the context manager


    # Display planetary information
    for data in planetary_data:
        print(f"{data['Planet']:<10}{data['Sign']:<10}{data['Sign Lord']:<10}{data['Nakshatra']:<15}{data['Naksh Lord']:<10}{data['Degree']%30:<10.2f}{data['Retro(R)']:<10}{data['Combust']:<10}{data['Avastha']:<10}{data['House']:<10}{data['Status']:<10}")

if __name__ == "__main__":
    main()

