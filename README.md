# Canadian Citizenship Exam Prep — Anki Deck

**`Canadian Citizenship Exam Prep.apkg`** — 440 cards, of which **313 are active
on import** and 127 ship suspended as low-yield. AnkiDroid/Anki compatible.

Built from the official IRCC study guide *Discover Canada: The Rights and
Responsibilities of Citizenship*, fetched live from canada.ca. No facts were
written from memory.

## Getting the deck

**[⬇ Download the latest `.apkg`](https://github.com/dcowsill/cdn-citizenship-anki/releases/latest/download/Canadian.Citizenship.Exam.Prep.apkg)**
— from the [Releases page](https://github.com/dcowsill/cdn-citizenship-anki/releases).
Copy it to your device and open it with AnkiDroid (or File → Import in desktop
Anki). It creates one deck, **Canadian Citizenship Exam Prep**, with a
`Citizenship Q/A` note type (Question / Answer fields).

The `.apkg` isn't committed to this repo — it's a build artifact attached to
each release. To build it yourself instead, see [Rebuilding](#rebuilding)
below.

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
| 24 | Rights and Responsibilities of Citizenship | `chapter::rights-and-responsibilities` |
| 31 | Who We Are | `chapter::who-we-are` |
| 111 | Canada's History | `chapter::history` |
| 44 | Modern Canada | `chapter::modern-canada` |
| 31 | How Canadians Govern Themselves | `chapter::government` |
| 29 | Federal Elections | `chapter::elections` |
| 15 | The Justice System | `chapter::justice-system` |
| 46 | Canadian Symbols | `chapter::symbols` |
| 12 | Canada's Economy | `chapter::economy` |
| 71 | Canada's Regions | `chapter::regions` |
| 17 | The Citizenship Test (format & process) | `chapter::exam-format` |
| **440** | **Total** | |

## What you actually study — 314 active cards

**127 cards ship already suspended** (tagged `yield::low`). On import you get
**313 active cards**; the other 127 are present but out of rotation, so they
never appear in reviews until you ask for them.

To bring them back, all at once or in part:

```
Browse → tag:yield::low → select → Unsuspend        (all 127)
Browse → tag:yield::low tag:chapter::regions        (just one chapter's worth)
```

Nothing is deleted — the built `.apkg` is a complete superset of the guide.

> **If you have already imported an earlier version of this deck:** Anki
> preserves the scheduling state of cards it already knows about, so re-importing
> will *not* suspend them for you. Run the Browse query above and hit **Suspend**
> once. A first-time import needs no such step.

The selection is evidence-based, in descending order of authority:

1. **Citizenship Regulations s.15** — the legally binding definition of what the
   test may probe. It authorises questions on the *"chief characteristics"* of
   Canadian history, geography and government and a *"general understanding"* of
   them, and singles out the **national symbols** as the one thing you must
   positively *"know"*. It never authorises incidental detail.
2. **IRCC's own 31 published study questions** (`study-questions.txt`).
3. The **132-question Richmond Public Library / OCASI practice bank** — the
   closest thing to an IRCC-endorsed question set that exists (OCASI's
   citizenshipcounts.ca is IRCC-funded and serves these questions).

A card is tagged only if it appears in **none** of the three and is sidebar,
caption or enumeration detail. What survives is the whole of elections,
government, rights and justice, plus macro-geography, the symbols core and the
history spine.

**Caveat:** a 2023 Leger poll built from citizenship-test questions did reach
into photo captions. Absence from the practice banks is not proof of absence
from the test. This is a time-budget tool, not a guarantee.

## Flagged cards — `tag:flagged::verify`

20 cards carry an amber "⚠ Check this" box. These are facts where the guide's
text no longer matches the present day, or facts that are **not** in the guide
at all. **Answer the guide's version on the test** — the exam is written from
the guide — but you should know the difference.

| Card | Guide says | Current reality |
|---|---|---|
| Electoral districts | 308 | **343** seats (2023 Representation Order) |
| Levels of government | *names four governments* | The official study question asks for **three**: federal, provincial/territorial, municipal |
| Commonwealth | 53 other nations | **56** member countries (55 other than Canada) |
| Official Opposition | "Her Majesty's Loyal Opposition" | **His** Majesty's, under King Charles III |
| Provincial superior courts | "Court of Queen's Bench" | Now generally **King's** Bench |
| G8 membership | G8 incl. Russia | Global Affairs Canada now describes the **G7**, without Russia |
| Free trade | NAFTA | Replaced by **CUSMA**, in force 1 July 2020 |
| Canada's population | about 34 million | **41,417,056** (StatCan, 1 Apr 2026) |
| Ontario's population | over 12 million | **16,103,890** (StatCan, 1 Apr 2026) |
| Quebec's population | nearly 8 million | **9,016,222** (StatCan, 1 Apr 2026) |
| B.C.'s population | four million | **5,646,420** (StatCan, 1 Apr 2026) |
| Territories' population | 100,000 | about **136,500** (StatCan, 1 Apr 2026) |
| $10 bill | Sir John A. Macdonald | Now the vertical note featuring **Viola Desmond** |
| Indigenous population shares | 65 / 30 / 4 % | **58.0 / 34.5 / 3.9 %** (2021 Census) |
| Religion | "great majority … Christians" | **53.3%** Christian, 34.6% no religion (2021); Catholic still largest |
| "O Canada" second line | "in all thy sons command" | **"in all of us command"** — changed by Parliament in 2018 |
| Ottawa chosen as capital | Refers to Queen Elizabeth II | Sovereign is now **King Charles III** |
| Major parties in the House | Conservative, Liberal, NDP | Changes with each election |
| Current office-holders | *(blank — fill in yourself)* | See below |
| Office-holders to look up | *(blank — fill in yourself)* | Depends on where you live |

### Current office-holders (verified August 2026 — re-check before your test)

- **Sovereign / Head of State:** His Majesty King Charles III — confirmed on
  gg.ca and the Crown in Canada page on canada.ca
- **Governor General:** Her Excellency the Right Honourable Louise Arbour, 31st
  Governor General, sworn in 8 June 2026 — confirmed on gg.ca ("*was sworn in on
  June 8, 2026. She is the 31st governor general of Canada*") and by the
  Canadian Heritage installation news release
- **Prime Minister:** The Right Honourable Mark Carney, sworn in 14 March 2025 —
  confirmed on pm.gc.ca and ourcommons.ca

Also verified at the same time, in case a question reaches for them: the Leader
of the Official Opposition is the Hon. Pierre Poilievre (Conservative), and the
House has 343 seats with the Liberals forming a majority. Seat counts are
*volatile* — the Liberals sit at 172 against a threshold of 171.5, with
by-elections on 31 August 2026 — which is why no card carries a seat breakdown.

These are **not** in *Discover Canada* (the guide leaves blanks for you to fill
in). You also need to look up, for yourself: your MP and federal riding, the
party in power, the Leader of the Opposition, your province's Lieutenant
Governor and Premier, and your mayor or reeve.

## Sources fetched

- All 20 pages of *Discover Canada* (`canada.ca/.../discover-canada/read-online/*`)
  — the 18 chapters plus the two sub-pages hanging off the government chapter.
  One of those, `canadas-system-government`, is the **only** place the guide
  states that the Supreme Court has nine judges appointed by the Governor
  General, and which branch the Prime Minister and Cabinet sit in.
- IRCC citizenship test pages: `how-it-works`, `study`, `online`, `results`,
  `invitation`, `missed`
- `gg.ca`, `pm.gc.ca`, `ourcommons.ca`, canada.ca Crown pages, Bank of Canada,
  Statistics Canada, `laws-lois.justice.gc.ca`

The downloadable PDF at `canada.ca/.../pub/discover.pdf` is the **2012 printed
edition** — its Oath still reads "Her Majesty Queen Elizabeth the Second". The
read-online HTML is the maintained edition and is what this deck follows. Even
that is only partly refreshed: the Royal Anthem section says "God Save the King
(or Queen)" while the Crown section still looks forward to the 2012 Diamond
Jubilee.

Chapter pages carry varying "date modified" stamps (2016 to 2026-05-14); the
underlying booklet text is largely unchanged since 2012, which is why several
figures above have drifted.

## Rebuilding

```bash
python -m venv venv && venv/bin/pip install genanki
venv/bin/python build_deck.py
```

Writes `dist/Canadian Citizenship Exam Prep.apkg` by default (pass a path as
the first argument to write elsewhere). `dist/` is gitignored — the `.apkg` is
a build artifact, regenerated on demand, not committed.

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
