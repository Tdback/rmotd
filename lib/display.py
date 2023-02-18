# Displays a message when user runs `rmotd` or on terminal startup

# Import necessary libs...
import sqlite3
from random import randint


def display_entry(db_file):
    """ Displays a random entry to terminal.
        Marks the entry as read for future deletion """
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Fetch all unread entries
    cur.execute("""
    SELECT * FROM rmotdEntries
    WHERE read = 0
    """)
    all_unread_entries = [row for row in cur.fetchall()]

    # Get a random entry
    entry = all_unread_entries[randint(0,len(all_unread_entries))-1]

    # TODO: Improve UI in terminal output
    print("Title: {}\n\n{}\n{}".format(entry[0],entry[1][:200] + "...",entry[2]))

    # Mark entry as read
    cur.execute("""
    UPDATE rmotdEntries
    SET read = 1
    WHERE title = (?)
    """,
                (entry[0],)
                )

    conn.commit()
    conn.close()
