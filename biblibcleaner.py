#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:44:25 2022

@author: Martien Lubberink
"""
import re
#import sys
#import os
import os.path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import warnings
warnings.simplefilter("ignore")


def closedafile(output, fi):
    with open(fi, "w", encoding="utf8") as text_file:
        print(output, file=text_file)


def opendafile(fn):
    with open(fn, encoding="utf8") as fp:
        contents = fp.read()
    return(contents)


def replace_abbrev(abbrev, journal, contents):
    #print(abbrev)
    contents = re.sub(r"journal\s?=\s?" + abbrev + ",", "journal = {" + journal + "},", contents)
    return contents


def ridlines(contents):
    contents = re.sub(r"@string{.*\n", "", contents)
    contents = re.sub(r'\n\s*\n', '\n\n', contents)
    return contents


def full_journals(fi):
    # Open bibtex file, and replace abbreviations with full journal name
    #
    contents = opendafile(fi)
    journals = re.findall(r'@string{(.*)\s=.*"{(.*)}"}', contents)
    for x in journals:
        #print(x[0], x[1])
        contents = replace_abbrev(x[0], x[1], contents)
    contents = ridlines(contents)
    return contents


def get_library_entries(contents):
    # With the bibtex file in memory, extract the publication types (book, article, misc)
    #
    pubtypes = ''.join([str(elem + "|") for elem in list(set(re.findall(r'^@([A-Zaz]*){.*,', contents, re.IGNORECASE|re.MULTILINE)))])
    library = re.findall(r'@(' + pubtypes + '){(.*),', contents, re.IGNORECASE)
    library = [x[1] for x in library]
    return pubtypes, library, contents


def get_refs_in_article(libry, arti):
    # Finds all the refereces in your article and stores them in a lyst
    #
    arti = opendafile(arti)
    lyst = []
    for ref in libry:
        found = re.findall(ref, arti)
        if len(found) > 0:
            #print(ref)
            lyst.append(found[0])
    return arti, lyst


def make_bib_from_lyst(lyst, bibfile, tup_lib, fo):
    # Retrieves all the bibtex entries you need (lyst) from your library (bibfile) then saves output to fo.
    #
    art_bib = []
    for ref in lyst:
        seekstring = r"(@(" + tup_lib + "){" + ref + "[\s\S]*?\n})"
        found = re.findall(seekstring, bibfile, re.IGNORECASE|re.MULTILINE)
        if len(found) > 0:
            if len(found[0][0]) > 0:
                print(ref)
                #print(len(found[0][0]))
                #print(found[0][0]+"\n")
                art_bib.append(found[0][0] + "\n\n")
    art_bib = ''.join([str(elem) for elem in art_bib])
    closedafile(art_bib, fo)
    return art_bib


parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--bibin",   default="my_library.bib", help="Your mybib.bib file")
parser.add_argument("-a", "--article", default="my_nobel_prize_winning_article.tex", help="Your article")
parser.add_argument("-o", "--bibout",  default="bibs_in_nobel_article.bib", help="Output")
args = vars(parser.parse_args())


fi = args["bibin"]    # "my_library.bib"
fa = args["article"]  # "my_nobel_prize_winning_article.tex"
fo = args["bibout"]   # "bibs_in_nobel_article.bib"


if (fi.endswith('.bib')) & (fo.endswith('.bib')) & (fa.endswith('.tex')) & (len(fo) > 4):
    cont = True
else:
    cont = False

if cont & os.path.exists(fi):
    print(f"\nFound your bib file: {fi}.\n")
    bib_library = full_journals(fi)
    tup_lib, library, bibfile = get_library_entries(bib_library)
else:
    cont = False
    print(f"\nCould not find {fi} in this folder.")

if cont & (os.path.exists(fa)):
    print(f"\nFound your article file: {fa}.\n")
    article, lyst = get_refs_in_article(library, fa)
    make_bib_from_lyst(lyst, bibfile, tup_lib, fo)
    print(f"\nConverted {len(lyst)} entries. Saved to {fo}.\n")
else:
    cont = False
    print(f"\nCould not find {fa} in this folder.")

if cont:
    print("\nDone.")
else:
    print("\nCheck your inputs.")
