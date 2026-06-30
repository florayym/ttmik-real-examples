---
name: study-notes-formatter
description: >
  Formats Korean grammar analysis into per-file content blocks ready to be merged into a study-notes
  repository. Use this skill after korean-grammar-extractor has produced an analysis, when the user
  wants to prepare the notes for saving — triggers include "整理成文件", "格式化", "准备存", "整理笔记",
  "format for repo", "准备提交". This skill ONLY shapes content and assigns each block a target
  filename based on naming conventions. It does NOT write files, does NOT decide create-vs-append,
  does NOT generate README indexes, and does NOT touch git. Those steps require the repository's real
  state and belong to Claude Code (guided by the repo's CLAUDE.md).
---

# Study Notes Formatter

## Purpose

Take a Korean grammar analysis (from korean-grammar-extractor) and reshape it into discrete
**content blocks**, each tagged with the **target filename** it belongs to. The output is an
intermediate artifact that Claude Code later merges into the real repository.

## Critical Boundary — What This Skill Does NOT Do

This skill has **no knowledge of the repository's actual state**. Therefore it must never:
- ❌ Say whether a file should be created or appended to (only Claude Code can know this after `git pull`)
- ❌ Generate or update README index tables (those require scanning the real repo)
- ❌ Write commit messages or run git
- ❌ Emit any imperative instruction to Claude Code

The contract between this skill and Claude Code is **the filename, nothing more**. This skill
says "here is content, and it belongs to file X". Claude Code decides everything about how X is
reconciled with reality.

The reason: a formatter that only sees new content has no authority to dictate merge actions.
Assigning a filename is legitimate because the grammar-point → filename mapping is a pure,
state-independent convention (-거든요 always maps to `-거든요.md`). Whether that file currently
exists is a question only the real repo can answer.

## Naming Conventions (state-independent, safe to apply)

These map content to filenames. They never depend on repo state.

### Folder
- Grammar point of TTMIK Level N → belongs under `level-N/`

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

### Special files (underscore prefix)
- Vocabulary → `_vocabulary.md`
- Expressions → `_expressions.md`

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
- The block contains the FULL content for this grammar point from THIS source: the H1 title +
  TTMIK reference + 语法核心 line, then a `## [Source]` section with examples.
- **No dates.** Source attribution only.
- Claude Code will later decide: if the file is new, write the whole block; if it exists, keep
  the existing H1 header and append only the `## [Source]` section. THIS SKILL DOES NOT MAKE THAT
  DECISION — it just provides the complete content and lets Claude Code reconcile.

### Vocabulary / Expressions blocks

````
### 📄 目标文件：level-X/_vocabulary.md

# Level X — 词汇积累

## [Source Title]

| 단어 | 词性 | 意思 | 备注 |
|------|------|------|------|
| ... | ... | ... | ... |
````

Same principle: full content, source section, no dates, no merge instruction.

## Output Structure

Produce all blocks for the analysis, grouped by level, in this order per level:
1. Each grammar point block (one per `level-X/[grammar].md`)
2. The `_vocabulary.md` block
3. The `_expressions.md` block

Then end. Do NOT add:
- A README block (Claude Code regenerates indexes from real state)
- A summary of "what to do next"
- Any git or file-operation guidance

A brief closing line in Chinese is fine, e.g. "以上是按文件分好的内容块，可交给 Claude Code 合并入仓库。"

## Why No README Here

README index tables count grammar points and examples across the WHOLE level — that requires
seeing every file currently in the repo, which this skill cannot. Claude Code regenerates the
README after merging, when it has the complete real picture. Generating a README here would
produce stale or wrong counts.
