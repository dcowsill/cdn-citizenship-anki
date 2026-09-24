# CLAUDE.md

Anki deck for the Canadian citizenship exam, built from IRCC's official study
guide. Someone is studying for a real exam from this deck — **correctness beats
speed, and beats card count**.

## The one rule

**Never write a fact from memory.** Every fact in this deck must be traceable to
text fetched from canada.ca. If a fetch fails, stop and report it — do not quietly
fall back on training data. `fetch_sources.py` prints that warning for a reason.

## Workflow

```bash
python -m venv venv && venv/bin/pip install -r requirements.txt

python fetch_sources.py sources          # ground truth -> sources/{text,examtext}
venv/bin/python build_deck.py            # -> dist/Canadian Citizenship Exam Prep.apkg
venv/bin/python factcheck.py sources     # must report 0 unmatched numbers
```

`sources/` and `dist/` are gitignored — both are regenerated, never committed.

| File | Role |
|---|---|
| `cards.py` | All card content, one list per chapter. **Edit facts here only.** |
| `build_deck.py` | genanki packaging: note type, CSS, deck, tags |
| `factcheck.py` | Verification pass (see below) |
| `fetch_sources.py` | Downloads + text-extracts the guide and IRCC test pages |

## Fetching canada.ca — read this before trying

canada.ca sits behind a CDN that is picky about clients. Three findings, all
learned the hard way:

- **`WebFetch` returns HTTP 403.** It cannot read these pages. Use Bash + curl.
- **Plain `urllib` hangs** until timeout with no error.
- **A spoofed browser User-Agent gets the HTTP/2 stream reset**
  (`curl: (92) ... INTERNAL_ERROR`). curl's *default* UA works fine. Do not add
  `-A` to the curl call in `fetch_sources.py`.

Which hosts block you *changes over time* — re-probe rather than trusting this
list. Verified 2026-08-09:

- **`gg.ca` works** (HTTP 200 via curl) and is the best Governor General source:
  it alone gives the post-installation style and the ordinal in one sentence.
  An earlier note here said it 403s; that is no longer true.
- **`lop.parl.ca` (ParlInfo) now 403s** to both curl and WebFetch. Use
  `ourcommons.ca` and `pm.gc.ca`, which carry the same facts.
- **`statcan.gc.ca` subject pages render their figures in JavaScript**, so curl
  sees an empty shell. Get numbers from the matching *Daily* release under
  `www150.statcan.gc.ca/n1/daily-quotidien/...` instead.

## Card format

`cards.py` entries are `(question, answer)` or `(question, answer, note)`.

A third element renders an amber "⚠ Check this" box on the card and adds the
`flagged::verify` tag. Use it — and only it — for the two cases below.

`LOW_YIELD`, at the foot of `cards.py`, is a set of exact question strings.
`build_deck.py` tags those cards `yield::low` **and ships them suspended**
(genanki `Card.suspend` → `queue = -1`), so a fresh import starts on the 314-card
core. Nothing is ever deleted; `tag:yield::low` → Unsuspend restores them. See
the README for the basis of the selection.

Note that Anki preserves the scheduling state of cards already in a collection,
so re-importing over an existing copy will not retroactively suspend anything.

## Handling drift between the guide and reality

The *Discover Canada* booklet text has been largely frozen since 2012, while the
pages carry varying "date modified" stamps. Several facts are now stale: 308
electoral districts (now 343), a 34-million population, the G8, NAFTA (now
CUSMA), "Her Majesty's Loyal Opposition", "Court of Queen's Bench", Macdonald on
the $10 bill (now Viola Desmond), and "in all thy sons command" in the anthem
(changed by Parliament in 2018).

Note the online edition is only *partly* refreshed — within the symbols chapter
the Royal Anthem section says "God Save the King (or Queen)" while the Crown
section still looks forward to the 2012 Diamond Jubilee. Do not assume a page is
current just because one nearby passage is.

**Do not silently correct these.** The exam is written from the guide, so the
guide's answer is the answer that scores. The convention is:

1. The card's answer states the guide's version, marked as such.
2. The `note` explains what has since changed, with the current figure if it was
   independently verified from an official source.

Same treatment for facts that are *not in the guide at all* (current Sovereign,
Governor General, Prime Minister — the guide leaves blanks for these). Verify
them live, flag them, and say they must be re-checked before the exam.

## Verification

`factcheck.py` extracts every number and proper noun from all 441 cards and
confirms each appears in the fetched source text for its chapter.

- **Section [1] numbers must stay at zero unmatched.** A hit there is a real
  defect — a wrong date or figure.
- Section [2] names has known-benign residue: `IRCC` (an abbreviation, not a
  claim) and `Carney` / `Honourable` / `Excellency` / `March` from the flagged
  current-officials card. Its substring matching can also mask a name (`Arbour`
  matches inside `harbour`), so it catches invented names but does not prove a
  name correct.
- Section [3] just lists the flagged cards.

`build_deck.py` additionally hard-fails if any `LOW_YIELD` entry no longer
matches a card. That set is keyed on exact question text, so rewording a
question would otherwise silently drop its `yield::low` tag.

**The single highest-value check is `sources/text/study-questions.txt`** — IRCC's
own 31 published study questions. Anything there must have a card, worded to
match. Two were missing when this deck was first built. `authorities.txt` is the
next most useful: it carries Citizenship Regulations s.15, the legally binding
statement of what the test may ask.

Spot-check exam-critical facts with grep against `sources/`. Beware: the source
text uses **curly quotes** (`“ ” ’`), so straight-quote grep patterns silently
miss. That produced one false "NOT FOUND" during the build.

## Style

- Paraphrase; do not lift sentences verbatim from the guide (copyright, and
  recall testing works better on reworded prompts).
- One fact per card, specific over vague — "What is the minimum voting age?" not
  "What do you know about voting?"
- Attribute the guide's evaluative claims rather than asserting them (it calls
  Arthur Currie "Canada's greatest soldier" — the card says the guide calls him
  that).
- Answers are HTML: `&mdash;`, `&eacute;`, `<br>` for lists. `factcheck.py`
  unescapes before comparing, so entities are safe to use.

## Deck facts

440 cards, 12 chapters, one `chapter::<name>` tag each. 127 also carry
`yield::low` and ship suspended, leaving 313 active on import; 20 carry
`flagged::verify` and all of them stay active. The `.apkg` is a build artifact
(`dist/`, gitignored) — run `build_deck.py` to produce it, do not commit it.
Deck and model IDs in `build_deck.py` are fixed constants — **do not change
them**, or re-importing will duplicate rather than update an existing user's
deck.
