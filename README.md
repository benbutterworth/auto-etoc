# auto-etoc
> Generate an electronic table of contents (etoc) for an issue of an academic journal

Journals regularly distribute a summary of what they have published recently to their audiences in what is called an "electronic table of contents", or "etoc". Collecting the information needed to create an etoc is tedious and takes time; enter `auto-etoc`.

`auto-etoc` is a webscraper that creates a plaintext summary of every article in an issue of a journal\* containing essential information like its title and authors, what type of article it is, and whether or not it is open access. A summary of an example article is below.

```
https://www.example.com/example-journal-article
Developing Automation Software in Publishing: A Retrospective
J. Smith, E. Mustermann
(Review)
(Open Access)
```

\* `auto-etoc` currently only works with SpringerLink journals. 

# Installation

> [!IMPORTANT]
> `auto-etoc` is a Python script, so you must install the Python programming language to use it. Download the latest verison of Python [here](https://www.python.org/downloads/).

1. Download the code in this repository as a .zip file or git clone it onto your system.  
2. Navigate to the folder with this code and open a terminal window by typing `powershell` in the top navigation bar.
3. Create and enter a virtual python environment to run `auto-etoc` in with the following commands:
```
py -m venv .venv
.venv/Scripts/activate
```
4. Download the required python package dependencies with the command  `py -m pip install -r requirements.txt`.
5. Exit the virtual environment using `deactivate

# CLI Usage (reccommended)
1. Navigate to the folder `auto-etoc`and open powershell, then re-enter the python virtual environment with `.venv/Scripts/activate`.
2. Run the CLI script using `python src/auto-etoc.py`
3. Scrape a single article by pasting its URL into the terminal when asked to and press enter. The etoc entry will be printed to the terminal, where you can copy the text for your etoc. This input process loops until you press enter without giving a URL.
4. After you press enter without giving a URL, you have the option to scrape a whole journal issue. Give the issue's URL when prompted and an etoc will be generated.

# GUI usage
1. Navigate to the folder `auto-etoc`and open powershell, then re-enter the python virtual environment with `.venv/Scripts/activate`.
2. Run the GUI script using `python src/auto-etoc-with-gui.py`
3. Paste the journal issue URL into the top text entry field, then press "Generate issue etoc".
4. After a couple of seconds, the text box will contain an etoc entry for every article in the issue.

# The future
0. (**DONE**) Fix parsing of author names to account for organisational affiliations.
1. (**DONE**) Allow user to input journal issue and produce whole etoc, not just one entry.
2. (**DONE**) Add simple tk GUI with textbox and button.
3. Refactor to build GUI application on top of core library instead of as separate file.
4. Rewrite for distribution as single executable.
5. Widen scope to other scrape issues from other publishers than SpringerNature


# Credit
*Ben Butterworth, 2025*

The GUI interface `etoc-GUI` to auto-etoc, was written with the help of AI (ChatGPT).