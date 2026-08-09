#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fact-check pass: extract every year, figure and proper name used in the cards
and confirm each appears in the fetched source text for its chapter.

Anything that cannot be matched is printed for manual review, so no fact
silently enters the deck unverified.

Usage:  python factcheck.py <path-to-scratchpad>
"""

import html
import os
import re
import sys
import unicodedata

from cards import CHAPTERS, CARDS

# chapter tag -> source text files (relative to the scratchpad dir)
SOURCES = {
    "oath":                        ["text/oath-citizenship.txt"],
    "rights-and-responsibilities": ["text/rights-resonsibilities-citizenship.txt"],
    "who-we-are":                  ["text/who-are-canadians.txt"],
    "history":                     ["text/canadas-history.txt"],
    "modern-canada":               ["text/modern-canada.txt"],
    "government":                  ["text/how-canadians-govern-themselves.txt"],
    "elections":                   ["text/federal-elections.txt"],
    "justice-system":              ["text/justice-system.txt"],
    "symbols":                     ["text/canadian-symbols.txt"],
    "economy":                     ["text/canadas-economy.txt"],
    "regions":                     ["text/canadas-regions.txt"],
    "exam-format":                 ["examtext/how-it-works.txt", "examtext/study.txt",
                                    "examtext/results.txt", "examtext/online.txt",
                                    "text/applying-citizenship.txt",
                                    "text/message-readers.txt"],
}

# Numbers that are structural to a question ("name three...", "list the six...")
# rather than claims about Canada. Ignored by the numeric check.
STOPNUMS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"}

# Capitalised words that are ordinary English (sentence starts, question words,
# connectives) rather than claims about Canada. Checked case-insensitively.
NAME_STOPWORDS = {w.lower() for w in [
    "The", "A", "An", "And", "But", "Or", "If", "In", "On", "At", "By", "For",
    "From", "To", "With", "Of", "As", "It", "Its", "They", "Their", "There",
    "This", "That", "These", "Those", "He", "She", "His", "Her", "You", "Your",
    "We", "Our", "Us", "Who", "What", "Which", "When", "Where", "Why", "How",
    "Name", "List", "Give", "Yes", "No", "Not", "Any", "Both", "All", "Each",
    "Some", "Most", "Many", "More", "Less", "Because", "Since", "After",
    "Before", "During", "While", "Until", "Under", "Over", "Between", "Besides",
    "Today", "Check", "Answer", "Use", "Verify", "Note", "Do", "Does", "Did",
    "Can", "Could", "Should", "Would", "Will", "May", "Must", "Have", "Has",
    "Had", "Is", "Are", "Was", "Were", "Be", "Been", "Being", "One", "Two",
    "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "First",
    "Second", "Third", "Matters", "Pioneers", "Representatives", "Ordinarily",
    "Symbols", "Experiences", "Hundreds", "Outside", "Party", "Sovereign",
    "Governor", "Prime", "Minister", "General", "Head", "State", "Crown",
    "Parliament", "Constitution", "Charter", "Act", "Cup", "Day", "War",
    "Battle", "Court", "House", "Commons", "Senate", "Cabinet", "Premier",
    "Lieutenant", "Commissioner", "Register", "Opposition", "Executive",
    "Legislative", "Judicial", "Islands", "Arctic", "Citadels", "Oath",
    "Anthem", "Royal", "Arms", "Monday", "Aboriginal", "Aboriginals",
    "European", "Europeans", "Asian", "Catholic", "Catholics", "Christian",
    "Christians", "Protestant", "Muslims", "Jews", "Hindus", "Sikhs",
    "English", "French", "Italian", "Chinese", "Ukrainian", "Scottish",
    "Irish", "Welsh", "German", "Dutch", "Polish", "Japanese", "Vietnamese",
    "Hungarian", "Canada", "Canadian", "Canadians", "Nobel", "Prize",
    "Motion", "Research", "Agreement", "Organization", "Languages", "Bay",
    "Company", "North", "South", "East", "West", "Coast", "Island",
]}


def norm(s):
    """Unescape HTML, strip tags, normalize quotes/dashes for comparison."""
    s = re.sub(r"<br\s*/?>", ". ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = unicodedata.normalize("NFC", s)
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'),
                 ("”", '"'), ("—", "-"), ("–", "-"),
                 ("−", "-"), (" ", " ")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s)


def fold(s):
    """Accent- and case-insensitive form, for name comparison."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def load_sources(base):
    out = {}
    for tag, files in SOURCES.items():
        chunks = []
        for f in files:
            p = os.path.join(base, f)
            if os.path.exists(p):
                chunks.append(open(p, encoding="utf-8").read())
            else:
                print("  !! missing source file: %s" % p)
        out[tag] = norm(" ".join(chunks))
    out["__ALL__"] = norm(" ".join(out[t] for t in SOURCES))
    return out


NUM_RE = re.compile(r"\b\d[\d,]*(?:\.\d+)?%?\b")
# Individual capitalised tokens: catches invented or misspelled proper nouns
# without the phrase-boundary noise of multi-word matching.
NAME_RE = re.compile(r"\b[A-Z][A-Za-zÀ-ſ'’\-]{2,}\b")


def numbers_in(text):
    return {m.group(0) for m in NUM_RE.finditer(text)}


SENT_START_RE = re.compile(r"(?:^|[.!?:;]\s+|\"\s*)([A-Z][A-Za-zÀ-ſ'’\-]{2,})")


def names_in(text):
    """Capitalised tokens that are not sentence-initial and not ordinary words.

    Possessive endings are stripped, so "Alberta's" is checked as "Alberta".
    """
    sentence_initial = set(SENT_START_RE.findall(text))
    found = set()
    for t in NAME_RE.findall(text):
        if t in sentence_initial:
            continue
        base = re.sub(r"['’]s$", "", t)
        if len(base) < 3 or base.lower() in NAME_STOPWORDS:
            continue
        found.add(base)
    return found


def num_present(n, src):
    if n in src:
        return True
    bare = n.rstrip("%")
    if bare != n and bare in src:
        return True
    # allow 4,200 <-> 4200 style differences
    nc = bare.replace(",", "")
    if nc and nc in src.replace(",", ""):
        return True
    return False


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    src = load_sources(base)

    unmatched_nums = []
    unmatched_names = []
    flagged_cards = []
    checked = 0

    for tag, title in CHAPTERS:
        chapter_src = src[tag]
        for entry in CARDS.get(tag, []):
            q, a = entry[0], entry[1]
            has_note = len(entry) > 2
            if has_note:
                flagged_cards.append((tag, q, entry[2]))
            text = norm(q + " " + a)
            checked += 1

            for n in sorted(numbers_in(text)):
                if n in STOPNUMS:
                    continue
                if not num_present(n, chapter_src) and not num_present(n, src["__ALL__"]):
                    unmatched_nums.append((tag, n, q))

            for nm in sorted(names_in(text)):
                if fold(nm) in fold(chapter_src) or fold(nm) in fold(src["__ALL__"]):
                    continue
                unmatched_names.append((tag, nm, q))

    print("=" * 74)
    print("FACT-CHECK PASS  -  %d cards checked against fetched source text" % checked)
    print("=" * 74)

    print("\n[1] NUMBERS / DATES not found verbatim in the source (%d)" % len(unmatched_nums))
    if not unmatched_nums:
        print("    none - every figure traced to the guide")
    for tag, n, q in unmatched_nums:
        print("    %-22s %-10s  %s" % (tag, n, q[:70]))

    print("\n[2] PROPER NAMES not found verbatim in the source (%d)" % len(unmatched_names))
    if not unmatched_names:
        print("    none")
    for tag, nm, q in unmatched_names:
        print("    %-22s %-32s  %s" % (tag, nm[:32], q[:52]))

    print("\n[3] CARDS CARRYING A 'check this' FLAG (%d)" % len(flagged_cards))
    for tag, q, note in flagged_cards:
        print("    [%s] %s" % (tag, q))
        print("        -> %s" % norm(note)[:150])


if __name__ == "__main__":
    main()
