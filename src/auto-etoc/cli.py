# define skullduggery here
import datetime
import argparse
import typer
from typing_extensions import Annotated

from . import scraper

logo = """
   _____     _           _____ _____ _____ _____
  |  _  |_ _| |_ ___ ___|   __|_   _|     |     |
  |     | | |  _| . |___|   __| | | |  |  |  ---|
  |__|__|___|_| |___|   |_____| |_| |_____|_____|   
  ----your friendly neighbourhood ETOC maker----
"""

app = typer.Typer()


@app.command()
def article(
    urls: Annotated[
        list[str], typer.Argument(help=f"The URL(s) of the article to scrape")
    ],
):
    """Extract the metadata from a single article."""
    for url in urls:
        print("Scraping the article at {0}...".format(url))
        scraper.check_url(url)
        soup = scraper.get_website_soup(url)
        article_info = scraper.extract_article_info(soup)
        article_info["link"] = url
        print("\n", scraper.get_etoc_entry(article_info), "\n")


@app.command()
def issue(url: Annotated[str, typer.Argument(help=f"The URL of the issue to scrape")]):
    """Extract the metadata from a whole issue's articles."""
    print(scraper.generate_etoc(url))


@app.command()
def recent(
    url: Annotated[
        str, typer.Argument(help=f"The URL of the 'online first' page to scrape")
    ],
):
    """Extract the metadata from all the most recently published articles."""
    print("Scraping the most recent articles at {0}...".format(url))


@app.command()
def since(
    url: Annotated[
        str, typer.Argument(help=f"The URL of the 'online first' page to scrape")
    ],
    date: Annotated[str, typer.Argument(help="The cutoff date (DD.MM.YYYY)")],
):
    """Extract the metadata from the most recent articles published since a date."""
    print("Scraping articles since {1} at {0}...".format(url, date))


if __name__ == "__main__":
    app()
