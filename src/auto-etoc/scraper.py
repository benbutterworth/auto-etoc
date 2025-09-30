import requests
from bs4 import BeautifulSoup
from bs4 import element
import re  # proREGEXgang
import datetime

greeting = """
   _____     _           _____ _____ _____ _____
  |  _  |_ _| |_ ___ ___|   __|_   _|     |     |
  |     | | |  _| . |___|   __| | | |  |  |  ---|
  |__|__|___|_| |___|   |_____| |_| |_____|_____|   
  ----your friendly neighbourhood ETOC maker----

"""


def check_url(url: str, target="article") -> None:
    """Throw an error if the target URL will not go to a scrapable link"""
    regex = r"link\.springer\.com"
    if target == "article":
        regex += r"\/article\/10\.1007"
    elif target == "issue":
        regex += r"\/journal\/125\/volumes-and-issues"
    elif target == "recent":
        regex += r"\/journal\/125\/online-first"
    else:
        raise TypeError("Invalid target - please specify what the source should be")
    # Check that url matches these formats
    if not re.search(regex, url):
        raise ValueError("URL does not point to valid source of etoc information.")
    pass


def clean_author_text(author: str) -> str:
    """Remove all author affiliations and trailing characters etc. from an author line"""
    trailing_chars = "0123456789,&" + " "
    if "\xa0" in author:
        return author.split("\xa0")[0].strip(trailing_chars)
    else:
        return author.strip(trailing_chars)


def get_author_line(authors: element.Tag) -> str:
    """Format a pythonic list of author names into a prose list of authors"""
    clean_names = [clean_author_text(author.text) for author in authors]
    # Capture up fronts or other exceptions w/o author lists
    if len(clean_names) == 0:
        return ""
    elif len(clean_names) == 1:  # RARE - only one author
        return clean_names[0]
    # Capture affiliation exceptions like "on behalf of..." or "for..." a group
    elif re.search(r"(on\s)|(for\s)", clean_names[-1]):
        return ", ".join(clean_names[:-2]) + f" & {clean_names[-2]} {clean_names[-1]}"
    # Connect to last author with and (standard response)
    else:
        return ", ".join(clean_names[:-1]) + f" & {clean_names[-1]}"


def get_website_soup(url: str, give_main=True) -> element.Tag:
    """Scrape the contents of a HTML webpage at `url`"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    if give_main:
        main = soup.find(id="main")
        return main
    return soup


def extract_article_info(soup: element.Tag) -> dict:
    """Extract article information from its scraped soup"""
    # Find article metadata and list of authors
    article_title = soup.find_all("h1", class_="c-article-title")[0].text
    article_info = soup.find_all("li", class_="c-article-identifiers__item")
    authors = soup.find_all("li", class_="c-article-author-list__item")
    # Extract published date from open access
    isOpenAccess = article_info[1].text == "\nOpen access\n"
    if isOpenAccess:
        datePublishedString = article_info[2].text.strip()
    else:
        datePublishedString = article_info[1].text.strip()
    datePublished = datetime.datetime.strptime(
        datePublishedString.split(": ")[1], "%d %B %Y"
    )
    # Create dictionary containing article information to put into etoc
    data = {
        "title": article_title,
        "type": article_info[0].text,
        "open-access": isOpenAccess,
        "published": datePublished,
        "authors": get_author_line(authors),
        "link": "",
    }
    return data


def get_etoc_entry(article_info: dict) -> str:  # variant of print_etoc_entry
    """Create an etoc entry string from a articles parsed metadata"""
    isUncommon = article_info["type"] != "Article"
    isOpenAccess = article_info["open-access"]
    datePublished = article_info["published"].strftime("%d %B %Y")
    entry = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(
        article_info["link"],
        article_info["title"],
        article_info["authors"],
        f"({article_info["type"]})" if isUncommon else "",
        "(Open Access)" if isOpenAccess else "",
        datePublished,
    )
    # Strip empty lines from common and non OA articles
    entry = re.sub("\n+", "\n", entry).strip()
    return entry


def get_article_links_from_journal_issue(soup: element.Tag) -> list:
    """Extract all article links in an issue landing page from an issue url"""
    links = []
    articles_list = soup.find_all("h3", class_="app-card-open__heading")
    for article in articles_list:
        slug = article.find_all("a")[0]["href"]
        links.append("https://link.springer.com" + slug)
    return links


def generate_etoc(journal_issue_url: str) -> str:
    """Construct a monthly etoc for an issue with entries for every article in it"""
    check_url(journal_issue_url, target="issue")
    soup = get_website_soup(journal_issue_url)
    links = get_article_links_from_journal_issue(soup)
    etoc = ""
    for url in links:
        check_url(url)
        soup = get_website_soup(url)
        article_info = extract_article_info(soup)
        article_info["link"] = url
        etoc += get_etoc_entry(article_info) + "\n"
    return etoc

def scrape(article_url: str) -> str:
    check_url(url)
    soup = get_website_soup(url)
    article_info = extract_article_info(soup)
    article_info["link"] = url
    output = "\n" + get_etoc_entry(article_info)+ "\n"
    return output

# Interactive script for scraping
if __name__ == "__main__":
    print(greeting)

    # Loop continuously and enter articles one by one (for weekly ETOCs)
    while True:
        url = str(input("Input page URL here: "))
        if url == "":
            break
        print(scrape(url))

    # Create an ETOC for a whole issue (for monthly ETOCs)
    journal_issue_url = str(input("Input journal issue URL here: "))
    if journal_issue_url != "":
        print(generate_etoc(journal_issue_url))

    print("\nBye for now!")
