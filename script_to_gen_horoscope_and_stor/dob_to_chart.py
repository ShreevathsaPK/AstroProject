import csv
import sqlite3

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file. """
    conn = sqlite3.connect(db_file)
    conn.text_factory = str  # Set text factory to handle byte strings
    return conn

def create_tables(conn):
    """ Create tables for personal info and planet data. """
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT,
            place TEXT,
            latitude REAL,
            longitude REAL,
            timezone TEXT,
            sunrise TEXT,
            sunset TEXT,
            ayanamsha REAL,
            comments TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS planet_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            planet TEXT,
            sign TEXT,
            sign_lord TEXT,
            nakshatra TEXT,
            naksh_lord TEXT,
            degree TEXT,
            retro TEXT,
            combust TEXT,
            avastha TEXT,
            house INTEGER,
            status TEXT,
            personal_info_id INTEGER,
            FOREIGN KEY (personal_info_id) REFERENCES personal_info (id)
        )
    ''')
    conn.commit()

def add_data_from_csv(personal_info_file, planet_info_file):
    """ Add data from CSV files to the SQLite database. """
    # Create a database connection
    conn = create_connection('horoscope.db')
    create_tables(conn)
    cursor = conn.cursor()

    # Read and insert personal info from CSV
    with open(personal_info_file, mode='r') as personal_file:
        reader = csv.DictReader(personal_file)
        
        for row in reader:
            cursor.execute('''INSERT INTO personal_info (name, date, time, place, latitude, longitude, timezone, sunrise, sunset, ayanamsha, comments)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (row['Name'], row['Date'], row['Time'], row['Place'],
                            row['Latitude'], row['Longitude'], row['Timezone'],
                            row['Sunrise'], row['Sunset'], row['Ayanamsha'], row['Comments']))
            personal_id = cursor.lastrowid  # Get the ID of the inserted personal info

            # Read and insert planet info for this personal info
            with open(planet_info_file, mode='r') as planet_file:
                planet_reader = csv.DictReader(planet_file)
                for planet in planet_reader:
                    cursor.execute('''INSERT INTO planet_data (planet, sign, sign_lord, nakshatra, naksh_lord, degree, retro, combust, avastha, house, status, personal_info_id)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                   (planet['Planet'], planet['Sign'], planet['Sign Lord'],
                                    planet['Nakshatra'], planet['Naksh Lord'], planet['Degree'],
                                    planet['Retro(R)'], planet['Combust'], planet['Avastha'],
                                    planet['House'], planet['Status'], personal_id))

    conn.commit()
    conn.close()

def main():
    # Specify CSV filenames
    personal_info_file = 'personal_info.csv'
    planet_info_file = 'planet_data.csv'

    # Adding data to database
    add_data_from_csv(personal_info_file, planet_info_file)
    print("Data from '{}' and '{}' has been added to the database 'horoscope.db'.".format(personal_info_file, planet_info_file))

if __name__ == "__main__":
    main()
