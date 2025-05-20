import requests
from bs4 import BeautifulSoup
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
import re

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
    trailing_chars = "0123456789,&" + " "
    if "\xa0" in author:
        return(author.split("\xa0")[0].strip(trailing_chars))
    else:
        return(author.strip(trailing_chars))

def get_author_line(authors):
    clean_names = [clean_author_text(author.text) for author in authors]
    # Capture up fronts or other non-article exceptions
    if len(clean_names) == 0: 
        return ""
    elif len(clean_names) == 1:
        return clean_names[0]
    # Capture "on behalf of..." or "for..." exceptions
    elif re.search(r"(on\s)|(for\s)", clean_names[-1]):
        return ", ".join(clean_names[:-2]) + f" & {clean_names[-2]} {clean_names[-1]}"
    # Connect to last author with and (standard response)
    else:
        return ", ".join(clean_names[:-1]) + f" & {clean_names[-1]}"

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
    # Find article metadata and list of authors
    article_title = soup.find_all("h1", class_="c-article-title")[0].text
    article_info = soup.find_all("li", class_="c-article-identifiers__item") 
    authors = soup.find_all("li", class_="c-article-author-list__item")
    # Create dictionary containing data
    data = {
        "title": article_title,
        "type": article_info[0].text,
        "open-access": article_info[1].text == '\nOpen access\n',
        "authors": get_author_line(authors),
        "link": "" 
    }
    return data


def get_etoc_entry(article_info): #variant of print_etoc_entry
    article_type = f"\n({article_info["type"]})" if article_info["type"]!="Article" else ""
    entry = f"""
{article_info["link"]}
{article_info["title"]}
{article_info["authors"]}{article_type}
{"(Open Access)" if article_info["open-access"] else ""}\n"""
    return entry

def get_article_links_from_journal_issue(soup):
    links = []
    articles_list = soup.find_all("h3", class_="app-card-open__heading")
    for article in articles_list:
        links.append(article.find_all("a")[0]["href"])
    return links

def generate_etoc(journal_issue_url):
    try:
        check_url(journal_issue_url, target="issue")
        soup = get_website_soup(journal_issue_url)
        links = get_article_links_from_journal_issue(soup)
        etoc = ""
        for url in links:
            check_url(url)
            soup = get_website_soup(url)
            article_info = extract_article_info(soup)
            article_info["link"] = url
            etoc += get_etoc_entry(article_info)
    except ValueError:
        etoc = "Error generating ETOC: URL does not link to SpringerLink site."
    except requests.exceptions.MissingSchema:
        etoc = "Error generating ETOC: URL is invalid."
    except AttributeError:
        etoc = "Error generating ETOC: webpage contains no content"
    return etoc

class etocGUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="journal")
        self.title("eTOC Generator")
        self.geometry("475x360")

        # Entry Field
        self.entry = ttk.Entry(self, width=65)
        self.entry.pack(pady=10)

        # Generate Button
        self.generate_button = ttk.Button(self, text="Generate Issue eTOC", command=self.generate_etoc_gui, bootstyle=PRIMARY)
        self.generate_button.pack(pady=5)

        # Scrolled Text Output
        self.output_text = ScrolledText(self, height=15, width=65, wrap='word')
        self.output_text.pack(pady=10, padx=10)

    def generate_etoc_gui(self):
        input_text = self.entry.get()
        output = f"Generated eTOC:\n{generate_etoc(input_text)}"
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", output)

if __name__ == "__main__":
    app = etocGUI()
    app.mainloop()