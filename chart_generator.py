import swisseph as swe

# Set the path to Swiss Ephemeris files
swe.set_ephe_path('/workspaces/AstroProject/swisseph/')  # Adjust the path based on your setup

def calculate_planets(dob, tob, lat, lon):
    # Convert date and time to Julian Day
    year, month, day = map(int, dob.split('-'))
    hour, minute, second = map(int, tob.split(':'))
    
    # Calculate Julian Day
    jd = swe.julday(year, month, day, hour + minute / 60 + second / 3600)

    # Get the planetary positions
    planets = range(0, 10)  # 0 to 9 for Sun to Pluto
    positions = []
    for planet in planets:
        ret, pos = swe.calc(jd, planet)
        positions.append(pos)

    # Placeholder data for the example output (these should be computed)
    output_data = [
        ['Ascendant', 'Pisces', 'Jupiter', 'Purva Bhadrapada', 'Jupiter', '1°52′3″', 'Direct', 'No', '--', 1, '--'],
        ['Sun', 'Aries', 'Mars', 'Bharani', 'Venus', '24°58′10″', 'Direct', 'No', 'Mrita', 2, 'Exalted'],
        ['Moon', 'Aquarius', 'Saturn', 'Shatabhisha', 'Rahu', '9°5′36″', 'Direct', 'No', 'Kumara', 12, 'Enemy'],
        ['Mercury', 'Aries', 'Mars', 'Ashwini', 'Ketu', '7°57′49″', 'Direct', 'No', 'Kumara', 2, 'Enemy'],
        ['Venus', 'Gemini', 'Mercury', 'Aadra', 'Rahu', '7°30′27″', 'Direct', 'No', 'Kumara', 4, 'Friendly'],
        ['Mars', 'Libra', 'Venus', 'Chitra', 'Mars', '4°49′34″', 'Retro', 'No', 'Bala', 8, 'Friendly'],
        ['Jupiter', 'Pisces', 'Jupiter', 'Revati', 'Mercury', '26°22′39″', 'Direct', 'No', 'Bala', 1, 'Owned'],
        ['Saturn', 'Aries', 'Mars', 'Bharani', 'Venus', '14°29′35″', 'Direct', 'Yes', 'Yuva', 2, 'Enemy'],
        ['Rahu', 'Cancer', 'Moon', 'Ashlesha', 'Mercury', '23°43′31″', 'Retro', 'No', 'Kumara', 5, '--'],
        ['Ketu', 'Capricorn', 'Saturn', 'Dhanishta', 'Mars', '23°43′31″', 'Retro', 'No', 'Kumara', 11, '--'],
        ['Neptune', 'Capricorn', 'Saturn', 'Shravana', 'Moon', '10°31′18″', 'Direct', 'No', 'Vriddha', 11, '--'],
        ['Uranus', 'Capricorn', 'Saturn', 'Shravana', 'Moon', '22°53′20″', 'Direct', 'No', 'Kumara', 11, '--'],
        ['Pluto', 'Scorpio', 'Mars', 'Anuradha', 'Saturn', '15°50′41″', 'Direct', 'No', 'Yuva', 9, '--']
    ]

    # Print the results in a formatted table
    print(f"{'Planet':<10}{'Sign':<10}{'Sign Lord':<12}{'Nakshatra':<15}{'Naksh Lord':<12}{'Degree':<10}{'Retro':<8}{'Combust':<8}{'Avastha':<10}{'House':<8}{'Status':<8}")
    for data in output_data:
        print(f"{data[0]:<10}{data[1]:<10}{data[2]:<12}{data[3]:<15}{data[4]:<12}{data[5]:<10}{data[6]:<8}{data[7]:<8}{data[8]:<10}{data[9]:<8}{data[10]:<8}")

if __name__ == "__main__":
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    tob = input("Enter Time of Birth (HH:MM:SS): ")
    lat = float(input("Enter Place of Birth Latitude: "))
    lon = float(input("Enter Place of Birth Longitude: "))

    calculate_planets(dob, tob, lat, lon)
