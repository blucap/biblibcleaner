# biblibcleaner

## Context

Some academic journals accept LaTeX files, including your BibTex
library. The problem is that you do not want to upload your entire
library. Instead, you want only to upload the BibTex entries that your
paper mentions.

On top of that, my BibTeX library uses abbreviations instead of
journal names: American Economic Review is AER in my bibtex entries:

`@string{AER = "{American Economic Review}"}`

------------------------------------------------------------------------

This utility prepares a bibtex file for publication in an academic
journal.

1.  It replaces the abbreviations with the full journal names.

2.  It extracts the BibTex entries that are in your paper.

------------------------------------------------------------------------

## Usage

`biblibcleaner.py [-h] [-i BIBIN] [-a ARTICLE] [-o BIBOUT]`

`optional arguments:` `-h, --help` show this help message and exit

`-i BIBIN, --bibin BIBIN` your mybib.bib file (default:
`my_library.bib`)

`-a ARTICLE, --article ARTICLE` your article (default:
`my_nobel_prize_winning_article.tex`)

`-o BIBOUT, --bibout BIBOUT` Output (default:
`bibs_in_nobel_article.bib`)

`python biblibcleaner.py -i my_library.bib  -a my_nobel_prize_winning_article.tex -o bibs_in_nobel_article.bib`
