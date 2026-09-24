#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build "Canadian Citizenship Exam Prep.apkg" from cards.py using genanki.

Usage:  python build_deck.py [output.apkg]     (default: dist/Canadian Citizenship Exam Prep.apkg)
"""

import os
import sys
import genanki

from cards import CHAPTERS, CARDS, LOW_YIELD

DECK_ID = 1789070101      # stable, arbitrary
MODEL_ID = 1789070102

DECK_NAME = "Canadian Citizenship Exam Prep"

CSS = """
.card {
  font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 20px;
  text-align: left;
  color: #1a1a1a;
  background-color: #fdfdfd;
  padding: 16px;
  line-height: 1.5;
}
.question { font-weight: 600; }
.answer   { margin-top: 4px; }
hr#answer { border: none; border-top: 2px solid #d32f2f; margin: 14px 0; }
.flag {
  margin-top: 16px;
  padding: 10px 12px;
  border-left: 4px solid #e6a700;
  background: #fff8e1;
  font-size: 16px;
  line-height: 1.45;
}
.flag b { color: #8a6100; }
.nightMode.card { color: #eee; background-color: #2b2b2b; }
.nightMode .flag { background: #3a3524; border-left-color: #c99a00; }
.nightMode .flag b { color: #e6c256; }
"""

MODEL = genanki.Model(
    MODEL_ID,
    "Citizenship Q/A",
    fields=[{"name": "Question"}, {"name": "Answer"}],
    templates=[
        {
            "name": "Recall",
            "qfmt": '<div class="question">{{Question}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer"><div class="answer">{{Answer}}</div>',
        }
    ],
    css=CSS,
)


def build(out_path):
    deck = genanki.Deck(DECK_ID, DECK_NAME)

    # LOW_YIELD is keyed on exact question text, so a reworded question would
    # silently stop being tagged. Fail loudly instead of shipping a deck whose
    # yield::low tags have quietly drifted out of sync with the cards.
    all_questions = {e[0] for entries in CARDS.values() for e in entries}
    orphans = sorted(LOW_YIELD - all_questions)
    if orphans:
        raise SystemExit(
            "LOW_YIELD contains %d question(s) that match no card - a question "
            "was reworded or removed. Fix cards.py:\n  %s"
            % (len(orphans), "\n  ".join(orphans))
        )

    per_chapter = {}
    flagged = []
    low_yield_count = 0
    total = 0

    for tag, title in CHAPTERS:
        entries = CARDS.get(tag, [])
        per_chapter[tag] = (title, len(entries))

        for entry in entries:
            question, answer = entry[0], entry[1]
            note_text = entry[2] if len(entry) > 2 else None

            tags = ["chapter::" + tag]
            is_low_yield = question in LOW_YIELD
            if is_low_yield:
                tags.append("yield::low")
                low_yield_count += 1
            if note_text:
                answer = (
                    answer
                    + '<div class="flag"><b>&#9888; Check this:</b> '
                    + note_text
                    + "</div>"
                )
                tags.append("flagged::verify")
                flagged.append((tag, question, note_text))

            note = genanki.Note(model=MODEL, fields=[question, answer], tags=tags)

            # Ship the low-yield cards already suspended (genanki writes
            # queue = -1), so a fresh import starts on the 313-card core
            # without anyone having to run a Browse query first. The
            # yield::low tag is kept so they can be brought back with
            # Browse -> tag:yield::low -> Unsuspend.
            if is_low_yield:
                for card in note.cards:
                    card.suspend = True

            deck.add_note(note)
            total += 1

    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    genanki.Package(deck).write_to_file(out_path)
    return total, per_chapter, flagged, low_yield_count


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "dist/Canadian Citizenship Exam Prep.apkg"
    total, per_chapter, flagged, low_yield_count = build(out)

    print("Wrote: %s" % out)
    print("Deck name: %s" % DECK_NAME)
    print("Total cards: %d\n" % total)

    print("Cards per chapter")
    print("-" * 62)
    for tag, title in CHAPTERS:
        title_, n = per_chapter[tag]
        print("  %-4d  %-44s %s" % (n, title_, "chapter::" + tag))
    print("-" * 62)
    print("  %-4d  TOTAL" % total)

    print("\nCards shipped SUSPENDED (tag yield::low): %d" % low_yield_count)
    print("Cards active on import:                   %d" % (total - low_yield_count))
    print("  Bring them back with:  Browse -> tag:yield::low -> Unsuspend")

    print("\nCards tagged flagged::verify: %d" % len(flagged))
    for tag, q, note in flagged:
        print("  [%s] %s" % (tag, q))


if __name__ == "__main__":
    main()
