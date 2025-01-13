import sqlite3

# Array of zodiac signs and their respective house lords
zodiac_owners = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}

# Co-lords for specific signs (treated as the same lord)
co_lords = {
    'Aquarius': 'Saturn',  # Co-lord Rahu treated as Saturn for simplicity
    'Scorpio': 'Mars'      # Co-lord Ketu treated as Mars for simplicity
}

# List of Nakshatras in order
nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", 
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", 
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", 
    "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", 
    "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def obtain_nakshatra_from_code(number):
    """ Convert the numeric index of Nakshatra to the Nakshatra name """
    if 1 <= number <= 27:
        return nakshatras[number - 1]
    else:
        return None

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file. """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def query_planets_in_nakshatra(conn, nakshatra):
    """ Query planets in the specified Nakshatra """
    cursor = conn.cursor()
    cursor.execute(''' 
        SELECT DISTINCT 
            planet_data.planet, planet_data.house_lord 
        FROM 
            planet_data 
        WHERE 
            planet_data.nakshatra = ?''', (nakshatra,))
    return cursor.fetchall()

def query_lord_in_nakshatra(conn, lord, nakshatra):
    """ Query specific lords in the specified Nakshatra """
    cursor = conn.cursor()
    cursor.execute(''' 
        SELECT DISTINCT 
            planet_data.planet, planet_data.house_lord 
        FROM 
            planet_data 
        WHERE 
            planet_data.planet = ? AND planet_data.nakshatra = ?''', (lord, nakshatra))
    return cursor.fetchall()

def main():
    # Connect to the database
    db_file = 'horoscope.db'
    conn = create_connection(db_file)
    if not conn:
        print("Failed to connect to the database. Exiting.")
        return

    # Display Nakshatras for reference
    print("\nAvailable Nakshatras:")
    for idx, name in enumerate(nakshatras, start=1):
        print(f"{idx}: {name}")
    
    # Query 1: Find planets in a Nakshatra
    try:
        nakshatra_code = int(input('\nEnter Nakshatra index (1-27): '))
        nakshatra = obtain_nakshatra_from_code(nakshatra_code)
        if not nakshatra:
            print("Invalid Nakshatra index! Please enter a number between 1 and 27.")
            return

        print(f"\nPlanets in Nakshatra {nakshatra}:")
        results = query_planets_in_nakshatra(conn, nakshatra)
        if results:
            for planet, house_lord in results:
                print(f"Planet: {planet}, House Lordship: {house_lord}")
        else:
            print(f"No planets found in Nakshatra {nakshatra}.")
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        return

    # Query 2: Find specific lords in a Nakshatra
    try:
        lord = input('\nEnter the Lord (e.g., Mars, Venus, etc.): ').strip()
        if not lord:
            print("Lord input cannot be empty!")
            return

        nakshatra_for_lord_code = int(input('Enter Nakshatra index for the Lord (1-27): '))
        nakshatra_for_lord = obtain_nakshatra_from_code(nakshatra_for_lord_code)
        if not nakshatra_for_lord:
            print("Invalid Nakshatra index! Please enter a number between 1 and 27.")
            return

        # If the Nakshatra has a co-lord, map it to the primary lord
        if nakshatra_for_lord in co_lords:
            lord = co_lords[nakshatra_for_lord]

        print(f"\nPlanets ruled by {lord} in Nakshatra {nakshatra_for_lord}:")
        lord_results = query_lord_in_nakshatra(conn, lord, nakshatra_for_lord)
        if lord_results:
            for planet, house_lord in lord_results:
                print(f"Planet: {planet}, House Lordship: {house_lord}")
        else:
            print(f"No planets ruled by {lord} found in Nakshatra {nakshatra_for_lord}.")
    except ValueError:
        print("Invalid input! Please enter a valid number.")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
