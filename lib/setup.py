"""
Creates database and RSS subscriptions file
"""

import sqlite3
import os

def init_db(db_file):
    """ Creates database """
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    print("[MSG] Creating new database...")

    # Delete existing table (used with --clean arg)
    cur.execute("DROP TABLE IF EXISTS rmotdEntries")

    cur.execute("""
    CREATE TABLE rmotdEntries (
        title TEXT,
        desc TEXT,
        link TEXT,
        read NUMERIC,
        day NUMERIC,
        year NUMERIC
    )
    """)

    print("[MSG] Database created successfully!\n")

    conn.commit()
    conn.close()

# Maybe inform user to only type short-url, not w/ https://
def store_subs():
    """ Prompt user to store RSS subscriptions """
    feeds_file = ".rmotd_feeds"
    subs = []

    if os.path.exists(feeds_file):
        with open(feeds_file, "r", encoding="utf-8") as f:
            existing_subs = f.readlines()
        for existing_sub in existing_subs:
            subs.append(existing_sub)

    while True:
        enter_sub = input("[MSG] Please enter a valid RSS feed URL.\n"
                          "[MSG] When done, press [ENTER|RETURN] to submit or quit: ") + "\n"
        if enter_sub.strip("\n") == "":
            confirm_done = input("[MSG] Press [ENTER|RETURN] again to quit...")
            if confirm_done.strip("\n") == "":
                break
            continue
        # Check if valid RSS feed. Make function for better parsing?
        if "rss" not in enter_sub.lower() and "feed" not in enter_sub.lower():
            print("\n[ERR] Invalid RSS feed URL...\n")
            continue
        else:
            subs.append("https://" + enter_sub)
            print() # Adds in a break in between messages for readability

    # Check if user input anything 
    if len(subs) == 0:
        print("\n[ERR] No input from user!")
    else:
        with open(feeds_file, "w", encoding="utf-8") as f:
            f.writelines(subs)
        print(f"\n[MSG] RSS feeds file `{feeds_file}` uptdated successfully...\n")
