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

#naskhatra lord list
nakshatra_lords = {
    "Ashwini": "Ketu", "Bharani": "Venus", "Krittika": "Sun", "Rohini": "Moon",
    "Mrigashira": "Mars", "Ardra": "Rahu", "Punarvasu": "Jupiter", "Pushya": "Saturn",
    "Ashlesha": "Mercury", "Magha": "Ketu", "Purva Phalguni": "Venus", 
    "Uttara Phalguni": "Sun", "Hasta": "Moon", "Chitra": "Mars", 
    "Swati": "Rahu", "Vishakha": "Jupiter", "Anuradha": "Saturn", 
    "Jyeshtha": "Mercury", "Mula": "Ketu", "Purva Ashadha": "Venus", 
    "Uttara Ashadha": "Sun", "Shravana": "Moon", "Dhanishta": "Mars", 
    "Shatabhisha": "Rahu", "Purva Bhadrapada": "Jupiter", 
    "Uttara Bhadrapada": "Saturn", "Revati": "Mercury"
}

# Define the house lordship for planets
planet_house_mapping = {
    "Sun": ["Leo"],                     # Sun rules Leo
    "Moon": ["Cancer"],                 # Moon rules Cancer
    "Mars": ["Aries", "Scorpio"],       # Mars rules Aries and Scorpio
    "Mercury": ["Gemini", "Virgo"],     # Mercury rules Gemini and Virgo
    "Jupiter": ["Sagittarius", "Pisces"], # Jupiter rules Sagittarius and Pisces
    "Venus": ["Taurus", "Libra"],       # Venus rules Taurus and Libra
    "Saturn": ["Capricorn", "Aquarius"], # Saturn rules Capricorn and Aquarius
    "Rahu": ["Aquarius"],               # Rahu co-rules Aquarius
    "Ketu": ["Scorpio"]                 # Ketu co-rules Scorpio
}

# Define the zodiac signs in order
zodiac_signs = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def cal_house_lrd(naksh_lord, ascendant_identified):
    """
    Calculate the houses ruled by the Nakshatra lord based on the ascendant.

    Parameters:
        naksh_lord (str): The Nakshatra lord.
        ascendant_identified (str): The ascendant sign.

    Returns:
        list: A list of house numbers (1-12) ruled by the Nakshatra lord.
    """
    # Normalize input
    naksh_lord = naksh_lord.strip().title()
    ascendant_identified = ascendant_identified.strip().title()

    # Dictionary mapping Nakshatra lords to their ruled signs
    planet_house_mapping = {
        "Sun": ["Leo"],
        "Moon": ["Cancer"],
        "Mars": ["Aries", "Scorpio"],
        "Mercury": ["Gemini", "Virgo"],
        "Jupiter": ["Sagittarius", "Pisces"],
        "Venus": ["Taurus", "Libra"],
        "Saturn": ["Capricorn", "Aquarius"],
        "Rahu": ["Aquarius"],
        "Ketu": ["Scorpio"]
    }

    # List of zodiac signs in order
    zodiac_signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    # Get the signs ruled by the Nakshatra lord
    ruled_signs = planet_house_mapping.get(naksh_lord)
    if not ruled_signs:
        return [-1,-1]

    # Find the position of the ascendant in the zodiac
    try:
        ascendant_index = zodiac_signs.index(ascendant_identified)
    except ValueError:
        return f"Invalid ascendant: '{ascendant_identified}'. Please check the input."

    # Map each zodiac sign to a house number based on the ascendant
    ######NOT E: BELOW LOGIC IS TRASH BUT ITS WORKING FINE. DONT TRY TO COMPREHEND #####
    houses = {}
    for i in range(12):
        house_number = (i - ascendant_index + 12 ) % 12 + 1  #3 is some correction factor
        #print(f"house_number {house_number}")
        houses[zodiac_signs[i]] = house_number
    #print(houses)
    # Determine the houses ruled by the Nakshatra lord
    #print(f"ruled_signs {ruled_signs[0]} number {houses[ruled_signs[0]]} ")
    ruled_houses = sorted([houses[sign] for sign in ruled_signs])

    return ruled_houses



def obtain_nakshatra_from_code(number):
    """ Convert the numeric index of Nakshatra to the Nakshatra name """
    return nakshatras[number - 1] if 1 <= number <= 27 else None

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def query_planets_in_nakshatra(conn, nakshatra):
    """ Query planets in the specified Nakshatra """
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT DISTINCT personal_info.name,planet_data.personal_info_id, planet_data.nakshatra, planet_data.planet  
FROM personal_info 
JOIN planet_data ON personal_info.id = planet_data.personal_info_id
WHERE planet_data.nakshatra = ?''', (nakshatra,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return []

def query_lord_in_nakshatra(conn, lord, nakshatra):
    """ Query specific lords in the specified Nakshatra """
    cursor = conn.cursor()
    try:
        cursor.execute(''' 
            SELECT DISTINCT 
                planet_data.planet, planet_data.house_lord 
            FROM 
                planet_data 
            WHERE 
                planet_data.planet = ? AND planet_data.nakshatra = ?''', (lord, nakshatra))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return []

def calculate_which_lord_is_in_tht_naks(conn,planet,personal_id):
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT DISTINCT planet_data.sign from planet_data
        WHERE planet_data.planet='Ascendant' AND planet_data.personal_info_id=?;
        ''',(personal_id,))
    except sqlite3.Error as e:
        print(f"PLEASE CHECK SOMETHING IS OFF: {e}")

    ascendant_identified = cursor.fetchall()
    #print(ascendant_identified[0][0])
    #naksh_lord = cal_naksh_lrd(nakshatra_que)  DEL
    house_lrd = cal_house_lrd(planet,ascendant_identified[0][0])
    #print(f"house lrd {house_lrd}")
    return house_lrd

def main():
    db_file = 'horoscope.db'
    conditional_check_flg = int(input("Do u want conditional check? give 1"))
    conditional_house_number = input("If yes give conditional house")

    conn = create_connection(db_file)
    if not conn:
        print("Failed to connect to the database. Exiting.")
        return

    print("\nAvailable Nakshatras:")
    for idx, name in enumerate(nakshatras, start=1):
        print(f"{idx}: {name}")
    
    # Query 1: Find planets in a Nakshatra

    nakshatra_code = int(input('\nEnter Nakshatra index (1-27): '))
    nakshatra = obtain_nakshatra_from_code(nakshatra_code)
    if not nakshatra:
        print("Invalid Nakshatra index! Please enter a number between 1 and 27.")
        return

    print(f"\nPlanets in Nakshatra {nakshatra}:")
    results = query_planets_in_nakshatra(conn, nakshatra)
    if results:
        for result in results:
            lord_of_house=calculate_which_lord_is_in_tht_naks(conn,result[3],result[1])
            #print(f"Lord of the following houses :{lord_of_house}")
            #print(f"lord of house {lord_of_house} conditional_house_number {conditional_house_number}")
            
            another_flg = False
            for _ in lord_of_house:
                #print(lord_of_house)
                if(int(conditional_house_number)==int(_)):
                    another_flg =True

            if conditional_check_flg==0 or another_flg :
                print(f"Name: {result[0]} Planet : {result[3]} Lord : {lord_of_house} ")  # Adjust formatting based on actual data

    else:
        print(f"No planets found in Nakshatra {nakshatra}.")
    

    conn.close()

if __name__ == "__main__":
    main()
