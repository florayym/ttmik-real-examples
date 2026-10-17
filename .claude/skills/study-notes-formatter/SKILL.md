---
name: study-notes-formatter
description: >
  Formats Korean grammar analysis into per-file content blocks ready to be merged into a study-notes
  repository. Use this skill after korean-grammar-extractor has produced an analysis, when the user
  wants to prepare the notes for saving — triggers include "整理成文件", "格式化", "准备存", "整理笔记",
  "format for repo", "准备提交", "合并推送". This skill ONLY shapes content and assigns each block a
  target filename based on naming conventions. It does NOT write files, does NOT decide
  create-vs-append, does NOT generate README indexes, and does NOT touch git. Those steps need the
  repository's real state and belong to the session that has the repo checked out (local Claude
  Code, or a chat session with the repo attached), guided by the repo's CLAUDE.md.
---

# Study Notes Formatter

## Purpose

Take a Korean grammar analysis (from korean-grammar-extractor) and reshape it into discrete
**content blocks**, each tagged with the **target filename** it belongs to. The output is an
intermediate artifact that the repo session (whichever session has the real checkout) merges into
the repository by CLAUDE.md §5. Now that chat sessions can attach the repo and push, that is often
the same session, right after the analysis.

## Critical Boundary — What This Skill Does NOT Do

This skill has **no knowledge of the repository's actual state**. Therefore it must never:
- ❌ Say whether a file should be created or appended to (only the real checkout can tell, after `git pull`)
- ❌ Generate or update README index tables (those require scanning the real repo)
- ❌ Write commit messages or run git
- ❌ Emit any imperative instruction to the repo session

The contract between this skill and the repo session is **the filename, nothing more**. This skill
says "here is content, and it belongs to file X". The repo session decides everything about how X is
reconciled with reality.

The reason: a formatter that only sees new content has no authority to dictate merge actions.
Assigning a filename is legitimate because the grammar-point → filename mapping is a pure,
state-independent convention (-거든요 always maps to `-거든요.md`). Whether that file currently
exists is a question only the real repo can answer. Keep the two steps apart even when one session
does both: shape the blocks first, then reconcile them with the checkout. Mixing them is how merge
decisions end up made from memory instead of from the repo.

## Naming Conventions (state-independent, safe to apply)

These map content to filenames. They never depend on repo state.

### Folder
- Grammar point of TTMIK Level N → belongs under `level-N/`
- The level comes from the **first** lesson in the analysis header — the extractor lists the lesson
  that teaches the exact form first (`— TTMIK Level 7 Lesson 18 · Level 10 Lesson 12` → `level-7/`).
- One file per lesson's form. Never combine forms from different lessons into one file; if the
  analysis compares forms, split the examples by the lesson each one actually shows.
- A form marked 「TTMIK 未单独成课（最接近：Level X Lesson Y）」 goes into the closest lesson's file,
  with its 讲解 saying the form isn't taught as its own lesson. If no closest lesson is named, the
  form goes into the `_expressions.md` block instead of a level file.
- A grammar point marked 「课号待核实」 gets no filename yet: list it at the end under
  `### ⚠️ 课号待核实` so the lesson is checked before anything is saved.

### Grammar point filenames
- Use the grammar pattern as the filename
- Replace `/` with nothing, `~` with the actual characters
- Keep Korean characters as-is (GitHub renders them fine)
- Examples:
  - `-거든요` → `-거든요.md`
  - `-(으)니까` → `-(으)니까.md`
  - `-아/어 주다` → `-아어-주다.md`
  - `-ㄴ/는 것 같다` → `-것-같다.md`
  - `전혀` → `전혀.md`

### Special files (underscore prefix, top-level)
- Vocabulary → `_vocabulary.md`
- Expressions → `_expressions.md`
- These live at the **repo root**, not inside `level-X/` — vocab/expressions are scoped to their
  source, not to a level, and are shared across all levels.

### Topic pages
- Not produced here. The pages in `topics/` are maintained by the repo session (CLAUDE.md §4), which
  checks every lesson citation against the lecture notes and updates each page's status labels after
  a merge. A formatter block for a topic page would carry unchecked citations.

## Content Block Format

For each grammar point, output a block in this shape:

````
### 📄 目标文件：level-X/[grammar].md

# [Grammar Point] — [Chinese summary]

> TTMIK Level X Lesson Y
> 📖 语法核心：[core explanation]

## [Source Title]

> 来源：[source description]

### 例句 1
**原句：** ...
**场景：** ...
**拆解：**
- ...
**讲解：**
...
````

Notes on the block:
- The `### 📄 目标文件：...` line is the **only** routing signal — it names the destination file.
- The TTMIK line copies the analysis header's lessons in the same order:
  `> TTMIK Level 7 Lesson 18 · Level 10 Lesson 12`. Index generation reads the first one.
- The block contains the FULL content for this grammar point from THIS source: the H1 title +
  TTMIK reference + 语法核心 line, then a `## [Source]` section with examples.
- **No dates.** Source attribution only.
- The repo session will later decide: if the file is new, write the whole block; if it exists, keep
  the existing H1 header and append only the `## [Source]` section. THIS SKILL DOES NOT MAKE THAT
  DECISION — it just provides the complete content and lets the repo session reconcile.

### Vocabulary / Expressions blocks

One block each (not per level — vocab/expressions are shared across all levels):

````
### 📄 目标文件：_vocabulary.md

## [Source Title]

| 단어 | 词性 | 意思 | 备注 |
|------|------|------|------|
| ... | ... | ... | ... |
````

````
### 📄 目标文件：_expressions.md

## [Source Title]

| 表达 | 意思 | 用法说明 |
|------|------|----------|
| ... | ... | ... |
````

Same principle: just the source section, no dates, no merge instruction.

## Output Structure

Produce all blocks for the analysis in this order:
1. Each grammar point block, grouped by level (one per `level-X/[grammar].md`)
2. The `_vocabulary.md` block (one total, covering all grammar points in this analysis)
3. The `_expressions.md` block (one total)
4. `### ⚠️ 课号待核实`, only if the analysis left any lesson unconfirmed

Then end. Do NOT add:
- A README block (the repo session regenerates indexes from real state)
- A summary of "what to do next"
- Any git or file-operation guidance

A brief closing line in Chinese is fine, e.g. "以上是按文件分好的内容块，可以按 CLAUDE.md 合并入仓库。"

## Why No README Here

README index tables count grammar points and examples across the WHOLE level — that requires
seeing every file currently in the repo, which this skill cannot. The repo session regenerates the
README after merging, when it has the complete real picture. Generating a README here would
produce stale or wrong counts.

## Maintenance

Version 2. This skill lives only in the study repo (`.claude/skills/study-notes-formatter/`). It
loads automatically whenever the repo is attached to a session, which is the only time it's needed,
so there is no account copy to keep in sync.
