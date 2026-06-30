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
├── .claude/skills/            ← the two skills that produce note content
│   ├── korean-grammar-extractor/   (analyzes Korean text → grammar analysis)
│   └── study-notes-formatter/      (shapes analysis → per-file content blocks)
├── level-1/ ... level-10/     ← one folder per TTMIK level
│   ├── README.md              ← per-level index (auto-generated, see §6)
│   ├── [grammar].md           ← one file per grammar point
│   ├── _vocabulary.md         ← vocabulary for this level
│   └── _expressions.md        ← useful expressions for this level
```

## 3. The division of labor (important)

Three roles, each only does what it can do correctly:

| Role | Sees | Produces |
|------|------|----------|
| **korean-grammar-extractor** (skill) | Korean text only | grammar analysis (no dates, no file structure) |
| **study-notes-formatter** (skill) | the analysis + naming rules | content blocks tagged with a target filename |
| **Claude Code (you)** | the **real repo state** (via git) + this file | merge decisions, file writes, indexes, commits |

The skills deliberately do NOT decide create-vs-append, do NOT generate indexes, and do NOT
touch git. They cannot — they don't see the real repo. **You do.** The formatter hands you
content blocks each labeled with a target filename (e.g. `level-5/-거든요.md`). That filename is
the only routing signal. You decide everything else by inspecting the actual repo.

## 4. Naming conventions

### Folders
- A grammar point taught at TTMIK Level N lives under `level-N/`.

### Grammar-point filenames
- Filename = the grammar pattern itself, Korean kept as-is.
- Replace `/` with nothing; spell out `~`.
- Examples: `-거든요.md`, `-(으)니까.md`, `-아/어 주다 → -아어-주다.md`,
  `-ㄴ/는 것 같다 → -것-같다.md`, `전혀.md`.

### Special files
- `_vocabulary.md`, `_expressions.md` (underscore prefix).

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

6. **For `_vocabulary.md` / `_expressions.md`** — same rule: append the new `## [Source]` table
   section; don't touch existing ones.

## 6. Regenerating indexes (your job, not the skills')

Indexes require seeing the whole level, so only you can build them — after merging.

### Per-level README (`level-N/README.md`)
Rebuild by scanning every `*.md` in the folder (excluding README, `_vocabulary`, `_expressions`):
- Title = the file's H1 (text before ` —`).
- TTMIK lesson = parsed from the `> TTMIK Level X Lesson Y` line → format `LX.0Y`.
- Example count = number of `### 例句` headers in the file.
- **No date column** (chronology lives in git history).

Table format:
```markdown
# Level N 语法笔记索引

| 语法点 | TTMIK 课号 | 例句数 |
|--------|-----------|--------|
| [-거든요](-%EA%B1%B0%EB%93%A0%EC%9A%94.md) | L5.05 | 2 |
...

📝 [词汇积累](_vocabulary.md) · 💡 [好用的表达](_expressions.md)
```

### Root README
- Overview table: one row per level → 语法点数 (file count) and 总例句数 (sum of 例句 across files).
- Source log table: 来源 → 涵盖级别. **No dates.**

## 7. Markdown link encoding (critical)

Grammar-point filenames contain `(`, `)`, `+`, spaces — these BREAK markdown links if used raw,
because the first `)` closes the link early. **URL-encode every internal link** in generated
READMEs:
- `(` → `%28`  `)` → `%29`  `+` → `%2B`  space → `%20`
- Korean characters can stay literal (GitHub handles them), but encoding them is also fine.
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
