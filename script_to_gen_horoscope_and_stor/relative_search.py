#!/usr/bin/env python3
"""
Command-line utility for searching the horoscope database by relative
planet positions.

Usage example:
    $ python relative_search.py
    Reference planet: Moon
    Target planet: Saturn
    Offset houses from reference (1 means next house): 2
    Found charts for:
      - Alice
      - Bob
"""

import os
import sqlite3
import sys

# guard against Python2 execution
if sys.version_info[0] < 3:
    sys.exit("This script requires Python 3. Run as `python3 relative_search.py`.")

# database resides at the top level of Astro_Projects; build an absolute path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'horoscope.db')


def create_connection(db_file=DB_PATH):
    """Return a sqlite3 connection with row factory set."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn


def query_relative_position(conn, ref_planet, target_planet, offset):
    """Return rows where ``target_planet`` is ``offset`` houses from
    ``ref_planet``.  Offset is counted forward; 1 means the next house.
    """
    cursor = conn.cursor()
    query = '''
        SELECT p.name, ref.house AS reference_house, targ.house AS target_house
        FROM planet_data ref
        JOIN planet_data targ ON ref.personal_info_id = targ.personal_info_id
        JOIN personal_info p ON p.id = ref.personal_info_id
        WHERE ref.planet = ?
          AND targ.planet = ?
          AND (((ref.house - 1 + ?) % 12) + 1) = targ.house
    '''
    cursor.execute(query, (ref_planet, target_planet, offset))
    return cursor.fetchall()


def main():
    conn = create_connection()

    print("Relative-position search in horoscope.db")
    ref = input("Reference planet: ").strip().capitalize()
    targ = input("Target planet: ").strip().capitalize()
    try:
        offs = int(input("Offset houses from reference (1 means next house): "))
    except ValueError:
        print("Invalid offset; must be an integer.")
        return

    rows = query_relative_position(conn, ref, targ, offs)
    if not rows:
        print("No matching charts found.")
    else:
        print("Found charts for:")
        for row in rows:
            print(f"  - {row['name']} (ref: {row['reference_house']}, targ: {row['target_house']})")
    conn.close()


if __name__ == '__main__':
    main()
