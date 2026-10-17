# CLAUDE.md — ttmik-real-examples

This repository stores Korean grammar study notes mined from real Korean media, organized by
TTMIK (Talk To Me In Korean) level. This file is the **authoritative source** for how the repo
is structured and how new notes are merged in. When working in this repo, follow these rules.

---

## 1. What this repo is

- A personal Korean-learning notebook for a Chinese-speaking learner (中文母语) using TTMIK.
- Notes are grammar-point-centric: each grammar point is its own file that accumulates real
  example sentences from different sources over time.
- The learner studies in Chinese; explanations are in Chinese, Korean text stays in Korean.

## 2. Repository structure

```
ttmik-real-examples/
├── CLAUDE.md                  ← this file (authoritative conventions)
├── README.md                  ← root index (auto-generated, see §6)
├── _vocabulary.md             ← vocabulary (top-level, organized by source — see §4)
├── _expressions.md            ← useful expressions (top-level, organized by source)
├── .claude/skills/            ← source copies of the two skills that produce note content (§3)
│   ├── korean-grammar-extractor/   (analyzes Korean text → grammar analysis)
│   └── study-notes-formatter/      (shapes analysis → per-file content blocks)
├── level-1/ ... level-10/     ← one folder per TTMIK level
│   ├── README.md              ← per-level index (auto-generated, see §6)
│   └── [grammar].md           ← one file per grammar point
├── topics/                    ← cross-level thematic navigation pages (see §4)
│   ├── README.md              ← hub: topic list, shared legend, lessons shared between topics
│   └── [theme].md
```

## 3. The division of labor (important)

Three roles, each only does what it can do correctly:

| Role | Sees | Produces |
|------|------|----------|
| **korean-grammar-extractor** (skill) | Korean text (+ TTMIK lesson notes, when available) | grammar analysis with checked lesson numbers (no dates, no file structure) |
| **study-notes-formatter** (skill) | the analysis + naming rules | content blocks tagged with a target filename |
| **Repo session (you)** | the **real repo state** (via git) + this file | merge decisions, file writes, indexes, topic labels, commits |

The repo session is whichever session has a real checkout: Claude Code on the learner's machine,
or a Claude chat session with this repo attached. Chat sessions can attach the repo and push, so
one session can run all three roles in a row. The skills deliberately do NOT decide
create-vs-append, do NOT generate indexes, and do NOT touch git — they don't look at the repo.
**You do.** The formatter hands you content blocks each labeled with a target filename (e.g.
`level-5/-거든요.md`). That filename is the only routing signal. You decide everything else by
inspecting the actual repo.

### Skill copies
- `.claude/skills/` holds the source copies of both skills. Change them here, in git.
- korean-grammar-extractor is also installed in the learner's Claude account, so chats without this
  repo can still analyse text. That copy is made from this one: after changing the extractor here,
  update the account copy too (SKILL.md through a skill proposal card; reference files by
  re-uploading the folder).
- study-notes-formatter has no account copy. It loads whenever this repo is attached, which is the
  only time it's needed.
- Each SKILL.md states its version under "Maintenance". If a session sees an account copy of the
  extractor that differs from this one, follow this one and tell the learner the account copy needs
  updating.
- The TTMIK lesson-note PDFs and `TTMIK_Index.md` live in the learner's Claude Project, not in this
  repo. When `references/ttmik-grammar-map.md` changes, regenerate `TTMIK_Index.md` from it: the
  备注 column and the 子形态核对 appendix. The Project copy can only be overwritten whole, so check
  its page column against the lesson-note PDFs before writing it back.
- The account copy is updated through a skill proposal card, which carries SKILL.md only. Until the
  folder is re-uploaded, the account's map may be older than this one; SKILL.md tells the extractor
  to fall back on `TTMIK_Index.md` in that case, which is why the Index must stay current.

## 4. Naming conventions

### Folders
- A grammar point taught at TTMIK Level N lives under `level-N/`.
- When the analysis lists several lessons, the first one (the lesson that teaches the exact form)
  decides the folder.
- One file per lesson's form: don't combine forms from different lessons into one file.
- A form marked 「TTMIK 未单独成课」 goes into the file of the closest lesson the analysis names; with
  no closest lesson, it goes into `_expressions.md`.
- Nothing marked 「课号待核实」 is saved until its lesson has been checked.

### Grammar-point filenames
- Filename = the grammar pattern itself, Korean kept as-is.
- Replace `/` with nothing; spell out `~`.
- Examples: `-거든요.md`, `-(으)니까.md`, `-아/어 주다 → -아어-주다.md`,
  `-ㄴ/는 것 같다 → -것-같다.md`, `전혀.md`.

### TTMIK lesson numbers (`> TTMIK Level X Lesson Y`)
- The number must match a row in `.claude/skills/korean-grammar-extractor/references/ttmik-grammar-map.md`
  **and** that lesson's lecture notes must actually teach the form. The map's 子形态核对 section lists
  the sub-forms that are easy to misplace, the common forms no lesson teaches, and the few
  cross-references inside the PDFs that are wrong (never copy those).
- The file lives in the folder of that lesson's level (`level-X/`).
- A form that no lesson teaches gets no lesson number: write 「TTMIK 未单独成课」 and point to the
  closest lesson instead of inventing one.

### Special files
- `_vocabulary.md`, `_expressions.md` (underscore prefix) live at the **repo top level**, not
  inside `level-N/`. Vocabulary and expressions are scoped to their **source** (each is a
  `## [Source]` section), not to a TTMIK level — a word from one video has no inherent level — so
  they are shared across all levels rather than split per folder.

### Topic pages (`topics/[theme].md`)
- For a grammar *family* that spans many levels (e.g. 引用句法 running from L5 to L10), a topic
  page is a hand-curated navigation index linking out to the real per-level files
  (`../level-X/[grammar].md`). `topics/README.md` is the hub: list of topic pages, the shared
  reading legend, lessons that sit on two or more pages, and notes on lesson numbers.
- Two kinds: **形态型** (start from a form and show how it is composed/contracted; may be laid out
  as a matrix, e.g. 引用句法) and **意义型** (start from a meaning; family table in lesson order +
  中文对照 + 辨析/形态拆解 taken from the lecture notes).
- Every lesson cited on a topic page must be checked against that lesson's lecture-note text (the
  form really is taught there). The family table's 原文回指 column lists only back-references the
  lecture notes state explicitly ("In Level X Lesson Y…" / "the previous lesson").
- Status labels are words, not symbols: **有例句** (link to the file holding a real example of that
  exact form), **待采集** (TTMIK teaches it, repo has no example yet), **附带出现** (an example of the
  form already sits in another file — name the file and quote the fragment), **—** (TTMIK has no
  such lesson/combination; write no form in that cell). A form TTMIK never teaches appears only in a
  page's 「课程外」 table, and only when the repo already holds a real example of it.
- After merging new notes (§5), search `topics/` for the lesson just touched and update its label
  (待采集 / 附带出现 → 有例句) so the pages stay true.
- **No duplicated examples.** A topic page never repeats 例句 content — only links, one-line
  summaries, and planning notes. The per-level file is still the only source of truth for examples.
- Unlike grammar-point files, a topic page is a single whole-file write (not source-accumulating) —
  when new material surfaces for a theme, update the existing table/prose in place rather than
  appending a `## [Source]` section.
- Not counted in any `level-N/README.md` (they live outside every level). Link topic pages from
  the root README instead (see §6).

## 5. How to merge incoming content blocks

You will receive content blocks from the formatter, each headed by
`### 📄 目标文件：level-X/[name].md`. For each block:

1. **`git pull` first** — always reconcile against the true current state of the repo. Never
   assume; the repo is the single source of truth.

2. **Resolve the target file** from the block's filename label.

3. **Decide create vs. append by checking whether the file exists:**
   - **File does NOT exist** → create it with the full block content (H1 title + TTMIK reference
     + 语法核心 line + the `## [Source]` section).
   - **File EXISTS** → keep the existing H1 header (title / TTMIK ref / 语法核心) unchanged, and
     append ONLY the new `## [Source]` section (with its examples) to the end of the file,
     preceded by a `---` separator if not already present.

4. **Never overwrite existing example sections.** Appending only. Each source is additive.

5. **Idempotency check** — if a `## [Source]` section with the same source title already exists
   in the target file, do not duplicate it. Ask the user whether to replace or skip.

6. **For `_vocabulary.md` / `_expressions.md`** — these are the **top-level** files (`/_vocabulary.md`,
   `/_expressions.md`), not per-level. Same rule: append the new `## [Source]` table section;
   don't touch existing ones. If a `## [Source]` section already exists (e.g. the source already
   contributed vocab from a different level's grammar), append the new rows into that existing
   table rather than creating a duplicate source section.

## 6. Regenerating indexes (your job, not the skills')

Indexes require seeing the whole level, so only you can build them — after merging.

### Per-level README (`level-N/README.md`)
Rebuild by scanning every `*.md` in the folder (excluding README):
- Title = the file's H1 (text before ` —`).
- TTMIK lesson = parsed from the `> TTMIK Level X Lesson Y` line → format `LX.0Y`.
- Example count = number of `### 例句` headers in the file.
- **No date column** (chronology lives in git history).
- The footer links point **up** to the shared top-level files (`../_vocabulary.md`, `../_expressions.md`).

Table format:
```markdown
# Level N 语法笔记索引

| 语法点 | TTMIK 课号 | 例句数 |
|--------|-----------|--------|
| [-거든요](-%EA%B1%B0%EB%93%A0%EC%9A%94.md) | L5.05 | 2 |
...

📝 [词汇积累](../_vocabulary.md) · 💡 [好用的表达](../_expressions.md)
```

### Root README
- Overview table: one row per level → 语法点数 (file count) and 总例句数 (sum of 例句 across files).
- Source log table: 来源 → 涵盖级别. **No dates.**
- A link to the top-level `_vocabulary.md` / `_expressions.md` near the top.
- A `📚 专题导航：` line near the top, alongside the vocabulary/expressions links: first the hub
  (`topics/README.md`, labelled 专题总览), then each topic page labelled by its H1 title.

## 7. Markdown link encoding (critical)

Grammar-point filenames contain `(`, `)`, `+`, spaces — these BREAK markdown links if used raw,
because the first `)` closes the link early. **URL-encode every internal link** in generated
READMEs:
- `(` → `%28`  `)` → `%29`  `+` → `%2B`  space → `%20`
- Korean characters can stay literal (GitHub handles them), but encoding them is also fine.
- **Normalize the filename to NFC before encoding.** macOS can hand back decomposed (NFD) Hangul
  from the filesystem, while the names stored in git are NFC; an NFD-encoded link does not resolve
  on GitHub (raw.githubusercontent.com returns 404 for it). In Python:
  `urllib.parse.quote(unicodedata.normalize("NFC", name))`.
- After generating any README, verify each link resolves to a real file.

Example: `-(으)니까.md` → link target `-%28%EC%9C%BC%29%EB%8B%88%EE%9D%8C.md`
(in practice, URL-encode the whole filename to be safe).

## 8. Dates — don't write them

The repo deliberately contains **no calendar dates** inside files. Learning chronology is read
from `git log`. Keep source attribution (which video/article), never a date. If you find a
stray date in incoming content, strip it before committing.

## 9. Commit conventions

- One save action = one commit (atomic).
- Message format: `Add Level X notes from [source title]`
  - Multi-level: `Add L3/L4/L5 notes from [source title]`
  - Index-only refresh: `Rebuild indexes`
- Commit the merged note files AND the regenerated indexes together.
- Then `git push`.

## 10. Two kinds of requests you may get

1. **"Merge these notes / 把这些笔记合并推送"** — follow §5, §6, §9.
2. **"Structurally change the repo itself"** (e.g. change the index format, add a GitHub Action,
   restructure folders) — you are the engineer for this repo; do it directly against real state,
   then update THIS file (CLAUDE.md) if you changed a convention. Keep CLAUDE.md the single
   source of truth — if a rule changes, change it here.

## 11. What NOT to do

- ❌ Don't let the skills (or yourself, on their behalf) decide create-vs-append before `git pull`.
- ❌ Don't generate indexes from partial information — always scan real state post-merge.
- ❌ Don't add dates.
- ❌ Don't overwrite existing example sections.
- ❌ Don't leave broken (unencoded) markdown links in READMEs.
