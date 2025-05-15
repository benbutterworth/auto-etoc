# auto-etoc
> Generate an electronic table of contents (etoc) for an issue of a journal

Creating a newsletter to promote a journal issue can be tedious - enter the auto-etoc! It scrapes an\* article's webpage and extracts only the most important information from it - the title, authors, and whether or not it is open access!

\*provided it's a SpringerLink article

# Installation
Clone this repository into your preferred folder.

# CLI Usage 
1. Run `auto-etoc\src\auto-etoc.py` on the command line.
2. To scrape a single article, provide its URL when prompted and press enter. The etoc entry will be printed to STDOUT, then you will be prompted to give another URL. 
3. At any time, press enter without an input to scrape a whole journal issue. Give the issue URL when prompted, and each article in the issue will be scraped.

# GUI usage
1. Run `auto-etoc\src\auto-etoc-with-gui.py` on the command line.
2. Paste the journal issue URL into the top text entry field.
3. Press "generate etoc" and wait.

# The future
0. Fix parsing of author names to account for organisational affiliations.
1. (**DONE**) Allow user to input journal issue and produce whole etoc, not just one entry.
2. (**DONE**) Add simple tk GUI with textbox and button.
3. Widen scope to other publishers than SpringerNature

# Credit
*Ben Butterworth, 2025*