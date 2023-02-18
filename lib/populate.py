"""
Fetches entries from RSS subscriptions and populates database
"""

# Import necessary libs...
from sys import exit
import sqlite3
import feedparser as fp

# Import necessary files...
from lib.helper import get_current_date


def push_to_db(db_file):
    """ Checks for RSS subscriptions file. Throw error and exit if none are found """
    try:
        with open(".rmotd_feeds", "r", encoding="utf-8") as f:
            feeds = f.readlines()

    except FileNotFoundError:
        print("[ERR] No subscriptions file found!\n"
              "[MSG] Try running `rmotd --setup` or `rmotd --add` to create a subscriptions file...\n")
        exit()

    entry_grabber(feeds, db_file)


# Test to see if there are duplicate entries
def entry_grabber(feeds, db_file):
    """ Pulls entries down from RSS feeds
        and inserts them into rmotd db """
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    curr_day, curr_year = get_current_date()

    # Get a list of existing entries
    cur.execute("""
    SELECT title from rmotdEntries
    WHERE day = (?) and year = (?)
    """,
                (curr_day, curr_year))
    existing_entries = [row[0] for row in cur.fetchall()]

    # Could probably make this faster
    for url in feeds:
        d = fp.parse(url.strip("\n"))
        for entry in d.entries:
            if entry.title not in existing_entries:
                cur.execute("""
                INSERT INTO rmotdEntries (title, desc, link, read, day, year)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                            (entry.title, sanitize(entry.description), entry.link,
                             0, curr_day, curr_year))

    conn.commit()
    conn.close()


def sanitize(entry_desc):
    """ Cleans up entry descriptions.
        Looks for extra <p> and </p> """
    return entry_desc[:entry_desc.find("<p>")]
