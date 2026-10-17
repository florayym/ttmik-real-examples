# CLAUDE.md — ttmik-real-examples

Korean grammar notes mined from real Korean media (variety shows, press conferences, vlogs, dramas),
organised by TTMIK (Talk To Me In Korean) Core Grammar lesson, for a Chinese-speaking learner.
Explanations are in Chinese; Korean stays Korean.

## Layout

```
level-1/ … level-10/                     one note file per TTMIK lesson's form, examples grouped by source
_vocabulary.md, _expressions.md          vocabulary and expressions, grouped by source
README.md, level-N/README.md             generated indexes
topics/                                  cross-level topic pages
.claude/skills/study-notes-formatter/    the skill that writes into this repo
skills/korean-grammar-extractor/         the analysis skill, kept here under version control; it doesn't run here
tools/ttmik/                             checks the lesson table and topic pages against TTMIK's lecture notes
```

## Working here

- Notes arrive as an analysis made elsewhere. Filing one, and any edit to note files,
  `_vocabulary.md`, `_expressions.md`, the indexes or `topics/`, goes through
  **study-notes-formatter**. Its SKILL.md is this repo's format: when a convention changes, change it
  there, not here.
- Every TTMIK lesson number in the repo must match the lesson table,
  `skills/korean-grammar-extractor/references/ttmik-grammar-map.md`, and that lesson's lecture notes
  must teach the form. Change the table only after checking the lecture notes with `tools/ttmik/`.
- Edit korean-grammar-extractor in `skills/korean-grammar-extractor/`.
