# An assortment of helper functions to use
# throughout the program

# Import necessary libs...
from datetime import datetime, date
import sqlite3


def get_current_date():
    """ Returns [current day, year] """
    return [datetime.now().timetuple().tm_yday, date.today().year]


def testing_entries(db_file):
    """ Used to verify queries are addedd successfully.
        For testing purposes. Prints out all title in table """
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    
    cur.execute("SELECT title,read FROM rmotdEntries")
    rows = [row for row in cur.fetchall()]
    for _ in rows:
        print(_)

    conn.commit()
    conn.close()
