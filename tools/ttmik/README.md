# tools/ttmik

Checks the lesson table (`skills/korean-grammar-extractor/references/ttmik-grammar-map.md`) and the
topic pages against TTMIK's lecture notes. Only the scripts live here, never the lecture-note text.

## Input: the lecture notes as text

Take the text of TTMIK's three lesson-note volumes (Levels 1–3, 4–7, 8–10) — the PDFs' text layer,
with each page's `LEVEL 4 LESSON 26` header on its own line — and split it into lessons:

    python3 tools/ttmik/segment.py levels1-3.txt levels4-7.txt levels8-10.txt -o /tmp/ttmik-lessons.json
    export TTMIK_LESSONS=/tmp/ttmik-lessons.json

It repairs the one misprinted page header (L6-2 printed as LEVEL 6 LESSON 12) and reports any lesson it
can't find; there should be 25 for Level 1 and 30 for every other level (the PDFs have no Essential
Review lessons).

## Scripts

| Command | What it does |
|---|---|
| `lesson.py show L3-14` | print a lesson's notes |
| `lesson.py grep '만큼' L7-5` | find a pattern in some lessons, or in all of them |
| `check_map.py` | every form a lesson row names is in that lesson's notes; every 子形态核对 row has evidence from the notes |
| `check_topics.py` | every form on a topic page is in the notes of the lessons cited beside it |
| `backrefs.py L5-17` | the earlier lessons a lesson's notes point back to (the topic pages' 原文回指) |

`check_map.py` lists forms it can't find literally; these are usually conjugation variants (the notes
write -어요 where the table writes -다). Read each one with `lesson.py` before changing anything. A new
子形态核对 row needs an evidence entry in `check_map.py` — a pattern copied from that lesson's notes.
