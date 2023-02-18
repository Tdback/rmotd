#!/usr/bin/python3

# Import necessary libs...
import os
from sys import exit
import argparse

# Import necessary files...
from lib import setup
from lib import populate
from lib import cleanup_entries
from lib import display
from lib.helper import testing_entries


def main():
    """ Main function... (duh) """
    # Definitely need to fix this desc and formatting
    parser = argparse.ArgumentParser(description="The terminal RSS Feed Viewer!")
    parser.add_argument("--show",default=1,metavar="<I>",dest="show",
                        help="Display <I> number of RSS entries where <I> is an integer. The default is 1.")
    parser.add_argument("--add",dest="add",action="store_true",
                        help="Add an RSS URL (or URLs) to the subscriptions file, located in .rmotd_feeds")
    parser.add_argument("--setup",dest="setup",action="store_true",
                        help="Similar functionality to --clean. Deletes and re-creates the database but also creates the subscriptions file. Shoud only be run if the subscriptions file does not already exist.")
    args = parser.parse_args()

    db_file = "rmotd_feeds.db"
    if not os.path.exists(db_file) or args.setup:
        print("[MSG] Running setup script...")
        setup.init_db(db_file)
        setup.store_subs()

    # Add new subscription if user passes `--add`
    if args.add:
        setup.store_subs()

    populate.push_to_db(db_file)
    # testing_entries(db_file)

    # Could maybe make this faster w/out using a for loop
    for x in range(int(args.show)):
        display.display_entry(db_file)

    # Add a check for if no input from user, maybe don't create a db file

    # When calling this with `--age`, add argparse to pass in how age
    # for removing entries. The current default is 3
    # Add warning that `0` is NOT recommended
    cleanup_entries.rem_entries_from_db(db_file)
    exit()

    
if __name__ == '__main__':
    main()
