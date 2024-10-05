import sqlite3

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

def main():
    # Connect to the database
    conn = create_connection('horoscope.db')
    
    # Query 1: Planet with House or Sign
    planet = raw_input('Enter the Planet')
    house = input('Enter the house')
    print("Query 1: Results for {} in house {}".format(planet, house))
    results = query_planet_by_house_or_sign(conn, planet, house=house)
    for result in results:
        print(result[1])
    
    # Query 2: Planet with Retrograde Status
    planet = raw_input('Enter the Planet for Retro')
    retro_status = 'Retro'
    print("\nQuery 2: Results for {} with retrograde status {}".format(planet, retro_status))
    results = query_planet_by_retrograde(conn, planet, retro_status)
    for result in results:
        print(result[1])

    # Query 3: Planets in Same House or Zodiac
    '''
    planets = ['Sun', 'Venus']
    house = 2
    print("\nQuery 3: Results for planets {} in house {}".format(planets, house))
    results = query_planets_in_same_sign_or_house(conn, planets, house=house)
    for result in results:
        print(result[1])
    '''
    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
