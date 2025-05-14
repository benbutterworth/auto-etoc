import requests
from bs4 import BeautifulSoup
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText

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
def get_website_soup(url, give_main=True):
    check_url(url)
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


def get_etoc_entry(article_info): #variant of print_etoc_entry
    entry = "\n"
    if article_info["link"]:
        entry += article_info["link"] + "\n"
    entry += article_info["title"] + "\n"
    entry += article_info["authors"] + "\n"
    if article_info["type"]!="Article":
        entry += "(" + article_info["type"] + ")\n"
    if article_info["open-access"]:
        entry += "(Open Access)\n"
    return entry

def get_article_links_from_journal_issue(soup):
    links = []
    articles_list = soup.find_all("h3", class_="app-card-open__heading")
    for article in articles_list:
        links.append(article.find_all("a")[0]["href"])
    return links

def generate_etoc(journal_issue_url):
    soup = get_website_soup(journal_issue_url)
    links = get_article_links_from_journal_issue(soup)
    etoc = ""
    for url in links:
        soup = get_website_soup(url)
        article_info = extract_article_info(soup)
        article_info["link"] = url
        etoc += get_etoc_entry(article_info)
    return etoc

class etocGUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="journal")  # You can change the theme here
        self.title("eTOC Generator")
        self.geometry("475x360")

        # Entry Field (65 characters wide)
        self.entry = ttk.Entry(self, width=65)
        self.entry.pack(pady=10)

        # Generate Button
        self.generate_button = ttk.Button(self, text="Generate eTOC", command=self.generate_etoc_gui, bootstyle=PRIMARY)
        self.generate_button.pack(pady=5)

        # Scrolled Text Output (30 lines, 65 characters)
        self.output_text = ScrolledText(self, height=15, width=65, wrap='word')
        self.output_text.pack(pady=10, padx=10)

    def generate_etoc_gui(self):
        # Example logic: reverse the string and uppercase it
        input_text = self.entry.get()
        output = f"Generated eTOC:\n{generate_etoc(input_text)}"
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", output)

if __name__ == "__main__":
    app = etocGUI()
    app.mainloop()