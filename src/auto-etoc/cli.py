# define skullduggery here
import datetime
import argparse

logo = """
   _____     _           _____ _____ _____ _____
  |  _  |_ _| |_ ___ ___|   __|_   _|     |     |
  |     | | |  _| . |___|   __| | | |  |  |  ---|
  |__|__|___|_| |___|   |_____| |_| |_____|_____|   
  ----your friendly neighbourhood ETOC maker----
"""

parser = argparse.ArgumentParser(
    prog="autoetoc",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="%(prog)s scrapes SpringerLink pages for article metadata",
    epilog=logo
)

# default and neccessary URL argument
parser.add_argument(
    "URL", help="URL of the SpringerLink article to scrape"
)

# use flags to determine how the URL should be interpreted. only one allowed
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-m", "--monthly", action="store_true",
    help="scrape all articles in a monthly issue"
)
group.add_argument(
    "-r", "--recent", action="store_true",
    help="scrape all most recent 'online first' articles"
)
group.add_argument(
    "-s", "--since", action="store",
    help="scrape all most recent 'online first' articles after the date DD.MM.YY"
)

args = parser.parse_args()

if __name__ == "__main__":
    from .scraper import run
    if args.monthly:
        pass
    elif args.recent:
        pass
    elif args.since!=None:
        pass
    else:
        return 0

