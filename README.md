# Canadian Citizenship Exam Prep — Anki Deck

**`Canadian Citizenship Exam Prep.apkg`** — 430 cards, AnkiDroid/Anki compatible.

Built from the official IRCC study guide *Discover Canada: The Rights and
Responsibilities of Citizenship*, fetched live from canada.ca. No facts were
written from memory.

## Import

Copy the `.apkg` to your device and open it with AnkiDroid (or File → Import in
desktop Anki). It creates one deck, **Canadian Citizenship Exam Prep**, with a
`Citizenship Q/A` note type (Question / Answer fields).

## Exam format (verified from IRCC, page updated 2026‑03‑31)

| | |
|---|---|
| Questions | 20 (multiple choice or true/false) |
| Time limit | 45 minutes |
| Passing score | 15 / 20 |
| Languages | English or French |
| Attempts | 3 |
| Who must take it | Applicants aged 18–54 on the day they sign the application |
| Default format | Online, webcam-monitored, 30 days to complete |

All test questions are drawn from the *Discover Canada* guide.

## Studying by chapter

Every card carries a `chapter::` tag, so you can study one section at a time.
In Anki, use a filtered deck or the browser search `tag:chapter::history`.

| Cards | Chapter | Tag |
|------:|---------|-----|
| 9 | The Oath of Citizenship | `chapter::oath` |
| 22 | Rights and Responsibilities of Citizenship | `chapter::rights-and-responsibilities` |
| 30 | Who We Are | `chapter::who-we-are` |
| 111 | Canada's History | `chapter::history` |
| 44 | Modern Canada | `chapter::modern-canada` |
| 29 | How Canadians Govern Themselves | `chapter::government` |
| 29 | Federal Elections | `chapter::elections` |
| 13 | The Justice System | `chapter::justice-system` |
| 45 | Canadian Symbols | `chapter::symbols` |
| 12 | Canada's Economy | `chapter::economy` |
| 70 | Canada's Regions | `chapter::regions` |
| 16 | The Citizenship Test (format & process) | `chapter::exam-format` |
| **430** | **Total** | |

## Flagged cards — `tag:flagged::verify`

10 cards carry an amber "⚠ Check this" box. These are facts where the guide's
text no longer matches the present day, or facts that are **not** in the guide
at all. **Answer the guide's version on the test** — the exam is written from
the guide — but you should know the difference.

| Card | Guide says | Current reality |
|---|---|---|
| Electoral districts | 308 | **343** seats (2023 Representation Order, Elections Canada) |
| Commonwealth | 53 other nations | Membership has changed since publication |
| Official Opposition | "Her Majesty's Loyal Opposition" | **His** Majesty's, under King Charles III |
| Provincial superior courts | "Court of Queen's Bench" | Now generally **King's** Bench |
| G8 membership | G8 incl. Russia | Has met as the **G7** without Russia since 2014 |
| Canada's population | about 34 million | Substantially higher now |
| Ottawa chosen as capital | Refers to Queen Elizabeth II | Sovereign is now **King Charles III** |
| Major parties in the House | Conservative, Liberal, NDP | Changes with each election |
| Current office-holders | *(blank — fill in yourself)* | See below |
| Office-holders to look up | *(blank — fill in yourself)* | Depends on where you live |

### Current office-holders (verified August 2026 — re-check before your test)

- **Sovereign / Head of State:** King Charles III — confirmed by the Oath of
  Citizenship page and the Crown in Canada page on canada.ca
- **Governor General:** The Rt. Hon. Louise Arbour, 31st Governor General,
  installed 8 June 2026 — confirmed by a Canadian Heritage news release
- **Prime Minister:** Mark Carney — confirmed on pm.gc.ca

These are **not** in *Discover Canada* (the guide leaves blanks for you to fill
in). You also need to look up, for yourself: your MP and federal riding, the
party in power, the Leader of the Opposition, your province's Lieutenant
Governor and Premier, and your mayor or reeve.

## Sources fetched

- All 18 chapters of *Discover Canada* (`canada.ca/.../discover-canada/read-online/*`)
- IRCC citizenship test pages: `how-it-works`, `study`, `online`, `results`
- `pm.gc.ca`, canada.ca Crown/Governor General pages, elections.ca (seat count)

Chapter pages carry varying "date modified" stamps (2016 to 2026-05-14); the
underlying booklet text is largely unchanged since 2012, which is why several
figures above have drifted.

## Rebuilding

```bash
python -m venv venv && venv/bin/pip install genanki
venv/bin/python build_deck.py "Canadian Citizenship Exam Prep.apkg"
```

- `cards.py` — all card content, grouped by chapter
- `build_deck.py` — genanki packaging, note type, styling, tags
- `factcheck.py` — verification pass: extracts every figure and proper name from
  the cards and confirms each appears in the fetched source text. Run it with the
  path to a directory holding the extracted guide text.

## Notes on card writing

- Questions and answers are paraphrased, not lifted verbatim from the guide.
- Cards target one fact each where possible, with enough context to be
  memorable rather than purely rote.
- Card content is factual recall; the guide contains little that is a matter of
  degree. Where the guide makes an evaluative claim (e.g. describing someone as
  "Canada's greatest soldier"), the card attributes it rather than asserting it.
