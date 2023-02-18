"""
Displays a message when user runs `rmotd` or on terminal startup
"""

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

    # If no desc, just print out title and link
    if entry[1] == "":
        print(f"Title: {entry[0]}\n\n"
              f"Read more here:\n{entry[2]}\n")
    else:
        # Have to use hacky `chr(10)` to truncate description since f-strings can't
        # include a backslash... for some f'ing reason
        print(f"Title: {entry[0]}\n\n"
              f"{entry[1][:entry[1].find(chr(10))]}\n\n"
              f"Read more here:\n{entry[2]}\n")

    # Mark entry as read
    cur.execute("""
    UPDATE rmotdEntries
    SET read = 1
    WHERE title = (?)
    """,
                (entry[0],))

    conn.commit()
    conn.close()
