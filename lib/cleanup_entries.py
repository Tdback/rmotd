# Used to clean up old entries in rmotd_feed.db

# Import database api
import sqlite3

# Import helper function to calculate date
from lib.helper import get_current_date


def get_age_of_entry(day, year):
    """ Returns age of entry (in days) """
    curr_day, curr_year = get_current_date()
    return abs(day - (365 * (curr_year - year))) + curr_day if (year < curr_year) else abs(day - curr_day)

def rem_entries_from_db(db_file, entry_age=3):
    """ Checks age of read entries and removes `old` entries from db """
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("SELECT title, day, year FROM rmotdEntries WHERE read = 1")
    read_entries = [row for row in cur.fetchall()]

    for entry in read_entries:
        if get_age_of_entry(entry[1], entry[2]) >= entry_age:
            cur.execute("""
            DELETE FROM rmotdEntries
            WHERE title = (?)
            """,
            (entry[0],))

    conn.commit()
    cur.close()
