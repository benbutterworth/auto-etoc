import requests
from bs4 import BeautifulSoup

print("""
   _____     _           _____ _____ _____ _____
  |  _  |_ _| |_ ___ ___|   __|_   _|     |     |
  |     | | |  _| . |___|   __| | | |  |  |  ---|
  |__|__|___|_| |___|   |_____| |_| |_____|_____|   
  ----your friendly neighbourhood ETOC maker----

""")

def check_url(url):
    # add error check that URL is springerlink and an articlehere
    # if url doesn't have https://link.springer.com/article then throw error
    pass

def clean_author_text(author):
    if "\xa0" in author:
        return(author.split("\xa0")[0].strip("0123456789, "))
    else:
        return(author.strip("0123456789, "))

# Scrape HTML webpage from springerlink here
def get_website_soup(url):
    check_url(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
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
    return data
    

# Print out article information in ETOC format
def print_etoc_entry(article_info):
    print("\n")
    print(article_info["title"])
    print(article_info["authors"])
    if article_info["type"]!="Article":
        article_type = "(" + article_info["type"] + ")"
        print(article_type)
    if article_info["open-access"]:
        print("(Open Access)")
    print("\n")
    return 0

if __name__=="__main__":
    while True:
        url = str(input("Input page URL here: "))
        if url == "":
            break
        soup = get_website_soup(url)
        main = soup.find(id="main")
        article_info = extract_article_info(main)
        print_etoc_entry(article_info)