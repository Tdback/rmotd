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
    # Need to change this to only fetch title, desc, and link
    cur.execute("""
    SELECT title, desc, link
    FROM rmotdEntries
    WHERE read = 0
    """)
    all_unread_entries = [row for row in cur.fetchall()]

    # Get a random entry
    title, desc, link = all_unread_entries[randint(0,len(all_unread_entries))-1]

    # If no desc, just print out title and link
    if desc == "":
        print(f"Title: {title}\n\n"
              f"Read more here:\n{link}\n")
    else:
        # Have to use hacky `chr(10)` to truncate description since f-strings can't
        # include a backslash... for some f'ing reason
        print(f"Title: {title}\n\n"
              f"{desc[:desc.find(chr(10))]}\n\n"
              f"Read more here:\n{link}\n")

    # Mark entry as read
    cur.execute("""
    UPDATE rmotdEntries
    SET read = 1
    WHERE title = (?)
    """,
                (title,))

    conn.commit()
    conn.close()
