import requests
from bs4 import BeautifulSoup
import re

greeting = """
   _____     _           _____ _____ _____ _____
  |  _  |_ _| |_ ___ ___|   __|_   _|     |     |
  |     | | |  _| . |___|   __| | | |  |  |  ---|
  |__|__|___|_| |___|   |_____| |_| |_____|_____|   
  ----your friendly neighbourhood ETOC maker----

"""

def check_url(url, target="article"):
    # Define the appropriate url format for each type of site to scrape
    if target == "article":
        regex = r"link\.springer\.com\/article\/10\.1007"
    elif target == "issue":
        regex = r"link\.springer.com\/journal\/125\/volumes-and-issues"
    else:
        raise TypeError("Invalid target - please specify what the source should be")
    # Check that url matches these formats
    if not re.search(regex, url):
        raise ValueError("URL does not point to valid source of etoc information.")
    pass

def clean_author_text(author):
    if "\xa0" in author:
        return(author.split("\xa0")[0].strip("0123456789, "))
    else:
        return(author.strip("0123456789, "))

# Scrape HTML webpage from springerlink here
def get_website_soup(url, give_main=True):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    if give_main:
        main = soup.find(id="main")
        return main
    return soup

  
# Extract article information from HTML
def extract_article_info(soup):
    data = {}
    # Find the title
    data["title"] = soup.find_all("h1", class_="c-article-title")[0].text
    # Find article type and open access
    article_info = soup.find_all("li", class_="c-article-identifiers__item")
    data["type"] = article_info[0].text
    data["open-access"] = article_info[1].text == '\nOpen access\n'
    # Cycle through all authors
    authors = soup.find_all("li", class_="c-article-author-list__item")
    authors_names = [clean_author_text(author.text) for author in authors]

    # need to do some extra checking here for last item
    # Note if "on behalf of" or other exceptions
    # add "&" symbol between last two
    data["authors"] = ", ".join(authors_names)
    data["link"] = ""
    return data
    

# Print out article information in ETOC format
def print_etoc_entry(article_info):
    print("\n")
    if article_info["link"]:
        print(article_info["link"])
    print(article_info["title"])
    print(article_info["authors"])
    if article_info["type"]!="Article":
        article_type = "(" + article_info["type"] + ")"
        print(article_type)
    if article_info["open-access"]:
        print("(Open Access)")
    print("\n")
    return 0

def get_etoc_entry(article_info): #variant of print_etoc_entry
    article_type = f"\n({article_info["type"]})" if article_info["type"]!="Article" else ""
    entry = f"""
{article_info["link"]}
{article_info["title"]}
{article_info["authors"]}{article_type}
{"(Open Access)" if article_info["open-access"] else ""}"""
    # entry = ""
    # if article_info["link"]:
    #     entry += article_info["link"] + "\n"
    # entry += article_info["title"] + "\n"
    # entry += article_info["authors"] + "\n"
    # if article_info["type"]!="Article":
    #     entry += f"({article_info["type"]})\n"
    # if article_info["open-access"]:
    #     entry += "(Open Access)\n"
    return entry

def get_article_links_from_journal_issue(soup):
    links = []
    articles_list = soup.find_all("h3", class_="app-card-open__heading")
    for article in articles_list:
        links.append(article.find_all("a")[0]["href"])
    return links

def generate_etoc(journal_issue_url):
    check_url(journal_issue_url, target="issue")
    soup = get_website_soup(journal_issue_url)
    links = get_article_links_from_journal_issue(soup)
    for url in links:
        check_url(url)
        soup = get_website_soup(url)
        article_info = extract_article_info(soup)
        article_info["link"] = url
        print(get_etoc_entry(article_info))
    return 0

if __name__=="__main__":
    print(greeting)
    while True:
        url = str(input("Input page URL here: "))
        if url == "":
            break
        check_url(url)
        soup = get_website_soup(url)
        article_info = extract_article_info(soup)
        print(get_etoc_entry(article_info))
    journal_issue_url = str(input("Input journal issue URL here: "))
    if journal_issue_url != "":
        generate_etoc(journal_issue_url)
    print("\nBye for now!")
