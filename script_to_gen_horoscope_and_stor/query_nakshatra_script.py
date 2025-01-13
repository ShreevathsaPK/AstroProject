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

def obtain_nakshatra_from_code(number):
    # List of Nakshatras in order
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", 
        "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", 
        "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", 
        "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", 
        "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
        "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    
    # Validate input
    if 1 <= number <= 27:
        return nakshatras[number - 1]
    else:
        return "Invalid input! Please enter a number between 1 and 27."


def main():
    # Connect to the database.
    conn = create_connection('horoscope.db')

    
    
    # Query 1: Planet with House or Sign
    planet = input('Enter the Planet: ')
    nakshatras_info = [
        "1:Ashwini", "2:Bharani", "3:Krittika", "4:Rohini", "5:Mrigashira", 
        "6:Ardra", "7:Punarvasu", "8:Pushya", "9:Ashlesha", "10:Magha", 
        "11:Purva Phalguni", "12:Uttara Phalguni", "13:Hasta", "14:Chitra", 
        "15:Swati", "16:Vishakha", "17:Anuradha", "18:Jyeshtha", "19:Mula", 
        "20:Purva Ashadha", "21:Uttara Ashadha", "22:Shravana", "23:Dhanishta", 
        "24:Shatabhisha", "25:Purva Bhadrapada", "26:Uttara Bhadrapada", "27:Revati"
    ]
    print(nakshatras_info)
    nakshatra_code = input('Enter the Nakshatra: ')
    nakshatra = obtain_nakshatra_from_code(int(nakshatra_code))
    print("Query 1: Results for {} in house {}".format(planet, nakshatra))
    results = query_planet_by_house_or_sign(conn, planet, nakshatra=nakshatra)
    for result in results:
        print(result[1])

    # Close the connection.
    conn.close()

if __name__ == "__main__":
    main()