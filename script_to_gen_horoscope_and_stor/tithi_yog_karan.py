import sqlite3

def fetch_yoga_grouped_personal_info(db_path="horoscope.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    WITH SunMoon AS (
    SELECT 
        p1.personal_info_id,
        p1.degree AS sun_degree,
        p2.degree AS moon_degree
    FROM planet_data p1
    JOIN planet_data p2 ON p1.personal_info_id = p2.personal_info_id
    WHERE p1.planet = 'Sun' AND p2.planet = 'Moon'
)
SELECT 
    pi.id, pi.name, pi.date, pi.time, pi.place, 
    sm.sun_degree, sm.moon_degree, 
    CAST(((CAST(sm.sun_degree AS REAL) + CAST(sm.moon_degree AS REAL)) / (360.0/27)) AS INTEGER) AS yoga_index,
    CASE CAST(((CAST(sm.sun_degree AS REAL) + CAST(sm.moon_degree AS REAL)) / (360.0/27)) AS INTEGER)
        WHEN 0 THEN 'Vishkambha'
        WHEN 1 THEN 'Priti'
        WHEN 2 THEN 'Ayushman'
        WHEN 3 THEN 'Saubhagya'
        WHEN 4 THEN 'Shobhana'
        WHEN 5 THEN 'Atiganda'
        WHEN 6 THEN 'Sukarma'
        WHEN 7 THEN 'Dhriti'
        WHEN 8 THEN 'Shula'
        WHEN 9 THEN 'Ganda'
        WHEN 10 THEN 'Vriddhi'
        WHEN 11 THEN 'Dhruva'
        WHEN 12 THEN 'Vyaghata'
        WHEN 13 THEN 'Harshana'
        WHEN 14 THEN 'Vajra'
        WHEN 15 THEN 'Siddhi'
        WHEN 16 THEN 'Vyatipata'
        WHEN 17 THEN 'Variyan'
        WHEN 18 THEN 'Parigha'
        WHEN 19 THEN 'Shiva'
        WHEN 20 THEN 'Siddha'
        WHEN 21 THEN 'Sadhya'
        WHEN 22 THEN 'Shubha'
        WHEN 23 THEN 'Shukla'
        WHEN 24 THEN 'Brahma'
        WHEN 25 THEN 'Indra'
        ELSE 'Vaidhriti'
    END AS Yoga
FROM SunMoon sm
JOIN personal_info pi ON sm.personal_info_id = pi.id
ORDER BY Yoga;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    print(f"{'Name':<15} {'Date':<12} {'Time':<8} {'Place':<20} {'Yoga':<15}")
    print("=" * 80)
    for row in rows:
        print(f"{row[0]:<15} {row[1]:<12} {row[2]:<8} {row[3]:<20} {row[7]:<15}")

    conn.close()

# Run the script
fetch_yoga_grouped_personal_info()
