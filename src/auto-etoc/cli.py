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
        etoc_entry = scraper.scrape(url)
        print(etoc_entry)


@app.command()
def issue(url: Annotated[str, typer.Argument(help=f"The URL of the issue to scrape")]):
    """Extract the metadata from a whole issue's articles."""
    etoc_entries = scraper.generate_etoc(url)
    print(etoc_entries)


@app.command()
def recent(
    url: Annotated[
        str, typer.Argument(help=f"The URL of the 'online first' page to scrape")
    ],
):
    """Extract the metadata from all the most recently published articles."""
    print("Scraping the most recent articles at {0}...".format(url))
    scraper.check_url(url, target="recent")
    soup = scraper.get_website_soup(url)
    urls = scraper.get_article_links_from_page(soup)
    for url in urls:
        etoc_entry = scraper.scrape(url)
        print(etoc_entry)


@app.command()
def since(
    url: Annotated[
        str, typer.Argument(help=f"The URL of the 'online first' page to scrape")
    ],
    date: Annotated[str, typer.Argument(help="The cutoff date (DD.MM.YYYY)")],
):
    """Extract the metadata from the most recent articles published since a date."""
    scraper.check_url(url, target="recent")
    try:
        datetime.datetime.strptime(date, "%d.%m.%Y")
    except e:
        raise Exception("DATE was not valid: use format DD.MM.YYYY")
    date = datetime.datetime.strptime(date, "%d.%m.%Y")
    # IN LOOP check date information
    soup = scraper.get_website_soup(url)
    etoc_entries = []
    urls = scraper.get_article_links_from_page(soup)
    for url in urls:
        soup = scraper.get_website_soup(url)
        info = scraper.extract_article_info(soup)
        if info["published"] > date:
            info["link"] = url
            entry = scraper.get_etoc_entry(info)
            etoc_entries.append(entry)
        else:
            continue
    etoc = "\n".join(etoc_entries)
    print(etoc)


if __name__ == "__main__":
    app()
