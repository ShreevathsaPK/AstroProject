import sqlite3

# Array of zodiac signs and their respective house lords
zodiac_owners = {
    'Aries': ['Mars'], 'Taurus': ['Venus'], 'Gemini': ['Mercury'], 'Cancer': ['Moon'],
    'Leo': ['Sun'], 'Virgo': ['Mercury'], 'Libra': ['Venus'], 'Scorpio': ['Mars', 'Ketu'],
    'Sagittarius': ['Jupiter'], 'Capricorn': ['Saturn'], 'Aquarius': ['Saturn', 'Rahu'],
    'Pisces': ['Jupiter']
}

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file. """
    conn = sqlite3.connect(db_file)
    return conn

# Query 1: Search by Planet and House or Sign with Personal Info
def query_planet_by_house_or_sign(conn, planet, house=None, sign=None):
    cursor = conn.cursor()

    if house:
        cursor.execute('''
            SELECT DISTINCT personal_info.*, planet_data.* 
            FROM personal_info 
            JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
            WHERE planet_data.planet = ? AND planet_data.house = ?''', (planet, house))
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

# Query 2: Search by Planet and Retrograde Status with Personal Info
def query_planet_by_retrograde(conn, planet, retro_status):
    cursor = conn.cursor()

    cursor.execute('''
        SELECT personal_info.*, planet_data.* 
        FROM personal_info 
        JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
        WHERE planet_data.planet = ? AND planet_data.retro = ?''', (planet, retro_status))
    results = cursor.fetchall()
    return results

# Query 3: Search for Planets in the Same Zodiac Sign or House with Personal Info
def query_planets_in_same_sign_or_house(conn, planets, house=None, sign=None):
    cursor = conn.cursor()

    if sign:
        placeholders = ', '.join('?' for _ in planets)
        query = '''
            SELECT DISTINCT personal_info.*, planet_data.* 
            FROM personal_info 
            JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
            WHERE planet_data.planet IN ({}) AND planet_data.sign = ?'''.format(placeholders)
        cursor.execute(query, planets + [sign])  # Use list for concatenation
    elif house:
        placeholders = ', '.join('?' for _ in planets)
        query = '''
            SELECT DISTINCT personal_info.*, planet_data.* 
            FROM personal_info 
            JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
            WHERE planet_data.planet IN ({}) AND planet_data.house = ?'''.format(placeholders)
        cursor.execute(query, planets + [house])  # Use list for concatenation
    else:
        print("Please provide either house or sign for search.")
        return []

    results = cursor.fetchall()
    return results

# Query 4: Identify lord of xth house and check if it sits in the yth house
# Modify the function to handle multiple lords for xth house sign
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
        ascendant = entry[14]
        ascendant_index = zodiac_list.index(ascendant)

        xth_house_index = (ascendant_index + (xth_house - 1)) % 12
        xth_house_lords = zodiac_owners[zodiac_list[xth_house_index]]

        for xth_house_lord in xth_house_lords:
            cursor.execute('''SELECT personal_info.*, planet_data.* 
                              FROM personal_info 
                              JOIN planet_data ON personal_info.id = planet_data.personal_info_id 
                              WHERE planet_data.planet = ? AND planet_data.house = ? 
                              AND personal_info.id = ?''', (xth_house_lord, yth_house, entry[0]))

            lord_results = cursor.fetchall()
            if lord_results:
                results.extend(lord_results)

    return results

def main():
    # Connect to the database
    conn = create_connection('horoscope.db')

    # Query 1: Planet with House or Sign
    planet = input('Enter the Planet: ')
    house = input('Enter the House: ')
    zodiac = input('Enter the Zodiac: ')
    print("Query 1: Results for {} in house {}".format(planet, house))
    results = query_planet_by_house_or_sign(conn, planet, house=house)
    for result in results:
        print(result[1])

    print("Query 1: Results for {} in zodiac {}".format(planet, zodiac))
    results = query_planet_by_house_or_sign(conn, planet, sign=zodiac)
    for result in results:
        print(result[1])

    # Query 2: Planet with Retrograde Status
    planet = input('Enter the Planet for Retro: ')
    retro_status = 'Retro'
    print("\nQuery 2: Results for {} with retrograde status {}".format(planet, retro_status))
    results = query_planet_by_retrograde(conn, planet, retro_status)
    for result in results:
        print(result[1])

    # Query 4: Identify xth lord in yth house
    xth_house = int(input('Enter the xth House: '))
    yth_house = int(input('Enter the yth House: '))
    print("\nQuery 4: Checking if lord of {}th house is in {}th house...".format(xth_house, yth_house))
    results = query_xth_lord_in_yth_house(conn, xth_house, yth_house)

    print("\nTotal Matches Found:", len(results))
    for result in results:
        print(result[1])

    # Close the connection.
    conn.close()

if __name__ == "__main__":
    main()