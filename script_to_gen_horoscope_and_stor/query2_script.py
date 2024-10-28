import sqlite3


# Array of zodiac signs and their respective house lords
zodiac_owners = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file. """
    conn = sqlite3.connect(db_file)
    return conn

# Query 1: Search by Planet and House or Sign with Personal Info.
def query_planet_by_house_or_sign(conn, planet, nakshatra, sign=None):
    cursor = conn.cursor()

    if nakshatra:
        cursor.execute('''
            SELECT DISTINCT personal_info.*, planet_data.* 
            FROM personal_info 
            JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
            WHERE planet_data.planet = ? AND planet_data.nakshatra = ?''', (planet, nakshatra))
    elif sign:
        cursor.execute('''
            SELECT DISTINCT personal_info.*, planet_data.* 
            FROM personal_info 
            JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
            WHERE planet_data.planet = ? AND planet_data.sign = ?''', (planet, sign))
    else:
        print("Please provide either house or sign for search.")
        return []

    results = cursor.fetchall()
    return results

def main():
    # Connect to the database
    conn = create_connection('horoscope.db')

    
    # Query 1: Planet with House or Sign
    planet = input('Enter the Planet: ')
    nakshatra = input('Enter the Nakshatra: ')
    print("Query 1: Results for {} in house {}".format(planet, nakshatra))
    results = query_planet_by_house_or_sign(conn, planet, nakshatra=nakshatra)
    for result in results:
        print(result[1])

    # Close the connection.
    conn.close()

if __name__ == "__main__":
    main()