# auto-etoc
> Generate an electronic table of contents (etoc) for an issue of a journal

Journals regularly distribute a summary of what they have published recently to their audiences in what is called an "electronic table of contents", or "etoc". Collecting the information needed to create an etoc is tedious and takes time; enter `auto-etoc`.

`auto-etoc` is a webscraper that creates a plaintext summary of a journal\* issue and lists the essential information of every article in the issue to share in an etoc:  a link to the article, its title and authors, what type of article it is, and whether or not it is open access.

\* `auto-etoc` currently only works with SpringerLink journals. 

# Installation

> [!IMPORTANT]
> You need [python 3.13](https://www.python.org/downloads/) to use `auto-etoc`.

Download the code as a .zip file or  clone this repository onto your system.  Create a safe environment to run `auto-etoc` using python on Windows with the following commands:

```powershell
# Go to the folder containing auto-etoc
cd $PATH_TO_AUTO_ETOC$

# Create and enter a virtual python environment
$PATH_TO_AUTO_ETOC$ py -m venv .venv
$PATH_TO_AUTO_ETOC$ .venv/Scripts/activate

# Download dependencies
$PATH_TO_AUTO_ETOC$ (.venv) py -m pip install -r requirements.txt
```

# CLI Usage (reccommended)
1. Run `auto-etoc\src\auto-etoc.py` on the command line.
```powershell
$PATH_TO_AUTO_ETOC$ (.venv) py src/auto-etoc.py
```
2. To scrape a single article, provide its URL when prompted and press enter. The etoc entry will be printed to STDOUT, then you will be prompted to give another URL. 
3. At any time, press enter without an input to scrape a whole journal issue. Give the issue URL when prompted, and each article in the issue will be scraped.

# GUI usage
1. Run `auto-etoc\src\auto-etoc-with-gui.py` on the command line.
```powershell
$PATH_TO_AUTO_ETOC$ (.venv) py src/auto-etoc-with-gui.py
```
2. Paste the journal issue URL into the top text entry field.
3. Press "generate etoc" and wait.

# The future
0. (**DONE**) Fix parsing of author names to account for organisational affiliations.
1. (**DONE**) Allow user to input journal issue and produce whole etoc, not just one entry.
2. (**DONE**) Add simple tk GUI with textbox and button.
3. Widen scope to other publishers than SpringerNature
4. Rewrite for distribution

# Credit
*Ben Butterworth, 2025*

The GUI interface `etoc-GUI` to auto-etoc, was written with the help of AI (ChatGPT).