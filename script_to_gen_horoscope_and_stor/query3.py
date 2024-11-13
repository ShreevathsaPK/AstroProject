import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = sqlite3.connect(db_file)
    return conn

def query_planet_with_least_degree(conn, input_planet):
    """Query to check if the input planet has the least degree (excluding Ascendant,Uranus, Neptune, and Pluto)."""
    cursor = conn.cursor()

    # SQL query to get all the planet data for each person
    query = '''
    SELECT personal_info.*, planet_data.planet, planet_data.degree
    FROM personal_info
    JOIN planet_data ON personal_info.id = planet_data.personal_info_id
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    # Group the planets by person and process each person's planet data
    people_planets = {}

    for result in results:
        person_name = result[1]  # Assuming name is in the 1st index (index starts from 0)
        planet_name = result[12]  # Assuming planet name is in the 12th index
        degree_str = result[13]  # Assuming degree is in the 13th index

        # Exclude Uranus, Neptune, Pluto
        if planet_name not in ('Ascendant','Uranus', 'Neptune', 'Pluto'):
            if person_name not in people_planets:
                people_planets[person_name] = []
            people_planets[person_name].append((planet_name, degree_str))

    # Remove duplicates by planet name
    for person_name in people_planets:
        people_planets[person_name] = remove_duplicates(people_planets[person_name])

    # Now for each person, we find the planet with the least degree
    for person_name, planet_data in people_planets.items():
        decimal_degrees = []
        #print("{}<__PERSONS ".format(person_name))
        # Convert degrees to decimal for each planet of the person
        for planet_name, degree_str in planet_data:
            decimal_degree = convert_to_decimal(degree_str, planet_name)
            if decimal_degree is not None:
                decimal_degrees.append((planet_name, decimal_degree))
        #print("{}<__PLANET ".format(decimal_degrees))
        if decimal_degrees:
            # Find the planet with the least degree
            min_planet, min_degree = min(decimal_degrees, key=lambda x: x[1])

            # Check if the planet with the least degree matches the input planet (Darakaraka)
            if min_planet == input_planet:
                print(f"The following person has {input_planet} as the Darakaraka with the least degree:")
                print(f"Name: {person_name}, Planet: {min_planet}, Degree: {min_degree:.4f}")

def remove_duplicates(planet_data):
    """Remove duplicate planet entries by name."""
    seen = set()
    unique_data = []
    for planet_name, degree_str in planet_data:
        if planet_name not in seen:
            seen.add(planet_name)
            unique_data.append((planet_name, degree_str))
    return unique_data

def convert_to_decimal(degree_str, planet):
    """Convert degree in '°′″' format or decimal degree format to a decimal number."""
    # Check if the planet is one of the excluded ones (already handled earlier in the query)
    if planet in ('Ascendant','Uranus', 'Neptune', 'Pluto'):
        print(f"Excluding {planet} from processing.")  # Log excluded planets
        return None

    # Check if the degree is in the decimal format (e.g., '294.5136114389239')
    if isinstance(degree_str, str) and '.' in degree_str:
        try:
            decimal_degree = float(degree_str)  # Convert to float if it's already in decimal
            return decimal_degree
        except ValueError:
            #print(f"Warning: Invalid decimal degree format for {planet}: {degree_str}")
            return None  # Return None for invalid decimal degree format

    # If the degree is in DMS format (e.g., '18∘17′15″')
    elif isinstance(degree_str, str) and '∘' in degree_str and '′' in degree_str and '″' in degree_str:
        try:
            # Clean the degree string and log it for debugging
            degree_str = degree_str.strip()

            # Split the string by degree symbol
            degree_parts = degree_str.split('∘')
            degrees = int(degree_parts[0])

            # Remove the '′' symbol and split the remaining part into minutes and seconds
            minute_second_parts = degree_parts[1].split('′')
            minutes = int(minute_second_parts[0])

            # Strip any remaining spaces and seconds (also clean '″' symbol)
            seconds_str = minute_second_parts[1].replace('″', '').strip()
            seconds = float(seconds_str) if seconds_str else 0.0

            # Convert to decimal degree
            decimal_degree = degrees + (minutes / 60) + (seconds / 3600)
            return decimal_degree
        except ValueError as e:
            print(f"Warning: Invalid degree format for {planet}: {degree_str}. Error: {e}")
            return None  # Return None for invalid degree format
    else:
        #print(f"Warning: Unrecognized degree format for {planet}: {degree_str}. Skipping this entry.")
        return None  # Return None if the degree format is incorrect or non-degree values


def main():
    # Connect to the database.
    conn = create_connection('horoscope.db')

    # Take input from user for planet
    input_planet = input("Enter the planet you want to check: ").capitalize()

    # Query to check if the input planet has the least degree
    print(f"Checking if {input_planet} has the least degree (excluding Ascendant,Uranus, Neptune, Pluto)...")
    query_planet_with_least_degree(conn, input_planet)

    # Close the connection.
    conn.close()

if __name__ == "__main__":
    main()
