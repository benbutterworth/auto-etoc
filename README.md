# `auto-etoc`
> Generate an electronic table of contents (etoc) for an issue of an academic journal

Journals let their audience know what they've been publishing recently by sending them regular _etocs_, **e**lectronic **t**ables **o**f **c**ontents. These etocs contain short summaries of recent articles. Gathering these summaries, however, is pretty tedious and time consuming; this is where `auto-etoc` comes in.

`auto-etoc` is a webscraper that creates a plaintext summary of every article in an issue of a journal\* containing essential information like its title and authors, what type of article it is, and whether or not it is open access. A summary of an example article is below.

```
https://www.example.com/example-journal-article
Developing Automation Software in Publishing: A Retrospective
J. Smith, E. Mustermann
(Review)
(Open Access)
15 March 2044
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
5. Exit the virtual environment using `deactivate`.

# Usage 
`auto-etoc article ARTICLE_URL...   `  - Extract the metadata from one or more articles.

`auto-etoc issue ISSUE_URL      `  - Extract the metadata from a specific issue's articles

`auto-etoc recent ONLINE_FIRST_URL      `  - Extract the metadata from all the most recently published articles.

`auto-etoc since ONLINE_FIRST_URL DATE `  - Extract the metadata from the most recent articles published since `DATE`.

# Project Roadmap

## Recent Updates
0. (**DONE**) Fix parsing of author names to account for organisational affiliations.
1. (**DONE**) Allow user to input journal issue and produce whole etoc, not just one entry.
2. (**DONE**) Add simple tk GUI with textbox and button.
3. (**DONE**) Add date published to output data
4. ~~Add option to export to text instead of to STDOUT~~ *redundant with shell scripting*
5. (**DONE**) Work into CLI tool instead of text interface


## Stretch Goals
- Refactor to build GUI application on top of core library instead of as separate file.
- Rewrite for distribution as single executable.
- Widen scope to other scrape issues from other publishers than SpringerNature

# Credit
*Ben Butterworth, 2026*