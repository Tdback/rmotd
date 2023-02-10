# Import necessary libs...
import os
from sys import exit
import argparse

# Import necessary files...
import setup
import populate
import cleanup_entries
import display
from helper import testing_entries


def main():
    """ Main function... (duh) """
    # Definitely need to fix this desc and formatting
    parser = argparse.ArgumentParser(description="Testing some code")
    parser.add_argument("--show",default=1,metavar="N",dest="show",help="Display N number of messages")
    parser.add_argument("--add",dest="add",action="store_true",help="Add RSS subscriptions to .rmotd_feeds")
    args = parser.parse_args()

    db_file = "rmotd_feeds.db"
    if not os.path.exists(db_file):
        print("Running setup script...")
        setup.init_db(db_file)
        setup.store_subs()
        print("Database now exists!")

    # Add new subscription if user passes `--add`
    if args.add:
        setup.store_subs()

    populate.push_to_db(db_file)
    # testing_entries(db_file)

    # Could maybe make this faster w/out using a for loop
    for x in range(int(args.show)):
        display.display_entry(db_file)

    # Add function to append entries to rss feeds file

    # Add a check for if no input from user, maybe don't create a db file

    # Actually, move the feed adding to another separate function for
    # when user runs --add to add another RSS subscription

    # Nevermind, that already happens lol. Just call store_subs() when
    # user runs --add to accomplish above

    # When calling this with `--age`, add argparse to pass in how age
    # for removing entries. The current default is 2
    # Add warning that `0` is NOT recommended
    cleanup_entries.rem_entries_from_db(db_file)
    exit()

    
if __name__ == '__main__':
    main()
