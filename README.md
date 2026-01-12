# `auto-etoc`
> Command line tool for creating a textual **e**lectronic **t**ables **o**f **c**ontents (etoc) for an issue of an research journal

Journals let people know what they're publishing by sending them regular *etoc*s of recently published articles. Gathering the short summaries of these articles can be pretty tedious and time consuming; `auto-etoc` reduces the amount of repetetive admin involved.

`auto-etoc` is a command line tool to create a plaintext summary of a research article based on its metadata in a journal\* issue: its title, authors, category and whether or not it is Open Access. It can summarise entire issues, what has been published recently, or individual articles

An example article summary is below.

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
It's reccommended you install auto-etoc with `pipx` by running the following command:

`pipx install git+https://github.com/benbutterworth/auto-etoc.git`

# Usage 
`auto-etoc article $URL$...`  - Extract the metadata from an article, available from the SpringerLink url `$URL$`. Inputting more than one url will output a summary for each of the articles given.

`auto-etoc issue $URL$`  - Extract the metadata from each article in a specific journal issue, where `$URL$` is the issue to summarise.

`auto-etoc recent $URL$`  - Extract the metadata from the most recently published articles, where `$URL$` is the link to the "online-first" section of a journal. 

`auto-etoc since $URL$ $DATE$ `  - Extract the metadata from the most recently published articles since `$DATE$`, where `$URL$` is the link to the "online-first" section of a journal.

>[!TIP]
> `auto-etoc` works best in scripting automations where the outputs can be piped to textfiles.

# Credit
*Ben Butterworth, 2026*