---
name: korean-grammar-extractor
description: >
  Extracts Korean grammar examples from real-world Korean text and provides structured breakdowns
  for a Chinese-speaking learner studying with TTMIK (Talk To Me In Korean). Use this skill whenever
  the user provides Korean text (transcripts, subtitles, articles, lyrics, social media posts, chat
  logs, or any Korean-language content) and wants to study specific grammar points or TTMIK levels.
  Also trigger when the user asks to "分析", "拆解", "提取语法", "找例句", "学习笔记", or mentions
  TTMIK levels in combination with Korean text. Even if the user just pastes Korean text and says
  something like "帮我分析 Level 4 语法" or "这里面有什么好的表达", use this skill.
---

# Korean Grammar Extractor

## Purpose

Transform raw Korean text from any media source into structured grammar study notes for a
Chinese-speaking Korean learner who uses TTMIK (Talk To Me In Korean) as their curriculum
framework.

This skill produces **analysis content only**. It does not decide file names, file structure,
or how/where notes are stored. Those concerns belong to the formatter skill
(study-notes-formatter) and to the study repo's CLAUDE.md. Keeping this skill
environment-agnostic means it works identically in a Project chat, in a session with the study
repo attached, or anywhere else.

## Inputs

1. **Korean text** — from any source: transcripts (often with auto-caption errors), lyrics,
   articles, webtoon dialogue, social posts, chat messages, etc.
2. **Target grammar** — specified as:
   - A specific TTMIK lesson: "Level 4 Lesson 12"
   - A level range: "Level 4 语法" or "Level 3-5"
   - A specific pattern: "-아/어 보다" or "-거든요"
   - A general request: "适合我水平的语法" (check conversation/memory for the learner's level)

## Processing Steps

### Step 1: Clean the Text
Auto-generated transcripts contain errors. Identify likely transcription errors (e.g.,
트린트먼트 → 트리트먼트), note them with "[자막 오류 추정]", but work with the intended meaning.
Strip timestamps for analysis.

### Step 2: Identify Target Grammar
Consult `references/ttmik-grammar-map.md`. It lists **every** lesson of TTMIK Core Grammar
Levels 1–10 (Level 1 has 26 lessons, Levels 2–10 have 31), each with a type tag and a one-line
「教什么」summary, and ends with a **子形态核对** section: forms taught inside a lesson whose title
doesn't show them, and common forms that no lesson teaches. Lesson numbers and titles come from
TTMIK's official course tables of contents; the forms were checked against TTMIK's lecture notes.

- When the user names a lesson ("Level 4 Lesson 12"), look it up and target exactly what that row
  says it teaches. Don't guess from memory: lesson numbers in the old audio era and in other
  learners' notes are often off by one or two.
- When the user names a level or range, the grammar targets are the rows tagged **语法** (plus
  **总结** if they ask about tenses). The other tags still matter, but they route elsewhere:
  构词 (Word Builder) → 汉字词 in 词汇积累; 惯用语 / 情境 / 表达 → 好用的表达; 活用 and 书写
  (irregulars, contractions, spacing) → mention inside 拆解 when the text shows them;
  操练 / 复习 contain no new grammar, so never use them as a lesson citation.
- The two tense-summary lessons (L8-9 past, L8-15 future) also introduce a few forms that no other
  lesson teaches; their map rows name them. Treat those as Level 8 grammar targets and cite the
  summary lesson when the text shows one.
- When one pattern is taught across several lessons, the map's 跨课对照 section lists them; cite all.
- If a pattern in the text isn't taught as its own TTMIK lesson, say 「TTMIK 未单独成课」 and point
  to the closest lesson rather than inventing a lesson number. 子形态核对 lists the common ones;
  for anything not listed, check the lecture notes before deciding.
- Before writing any lesson number, run it through **课号核对** below.

### Step 3: Extract and Organize
For each grammar point found:
1. List all occurrences from the source
2. Pick the best 2-3 examples — complete, natural, clearly demonstrating the point, from
   varied speakers/contexts, not too garbled.
3. Keep one grammar point to one lesson. Attach each example to the lesson that teaches the exact
   form it shows: an -았던 example belongs under L8-4 (-던), not under L4-26 (-(으)ㄴ + N).
   Comparisons with neighbouring lessons go into 讲解. Don't merge forms from different lessons
   into one grammar point: the notes are filed per lesson, so a merged point ends up under the
   wrong one.

### Step 4: Break Down Each Example
- **原句** — the Korean sentence as it appears
- **场景** — one line restoring the real situation it was said in
- **拆解** — morpheme breakdown of the key structure: `morpheme（meaning/function）+ ...`
- **讲解** — Chinese explanation, Korean grammar terms kept in Korean; note nuance, register
  (반말/존댓말/formal), and contrast with similar grammar where useful

### Step 5: Vocabulary (词汇积累)
Group by category, prioritizing: Sino-Korean words (汉字词, show Chinese character mapping),
pure Korean (고유어, esp. onomatopoeia/의태어), Konglish/loanwords (note English origin),
and domain-specific terms.

### Step 6: Useful Expressions (好用的表达)
Natural expressions worth learning that aren't necessarily the target grammar: idioms (관용 표현),
colloquial contractions, slang, culturally specific phrases. The map's 惯用语 rows (Levels 8–10,
organized by 눈 / 귀 / 손 / 마음 / 말…) and 情境 rows (refusing, agreeing, regret, asking directions…)
make a good checklist here: when the text contains one, cite that lesson.

## 课号核对 — checking lesson numbers

The lesson number decides where an example is filed and which cross-level topic pages it fills, so
a wrong number misfiles the example without anyone noticing. Lesson titles alone don't settle it:
checking the study notes against TTMIK's lecture notes turned up examples filed under a
neighbouring lesson.

1. **A number is right only if that lesson's notes teach that exact form.** Look the form up in the
   map's 子形态核对 first. The baseline is TTMIK's lesson-note PDFs for Levels 1–10 (in the
   learner's project knowledge; `TTMIK_Index.md` gives each lesson's volume and page). For a form
   the map doesn't settle, read the lesson before citing it when those notes are available.
   TTMIK's current online course may have revised some lessons; a sub-form the notes don't contain
   gets no lesson number.
2. **Don't copy the PDFs' own cross-references blindly.** A few are wrong; 子形态核对 lists them.
3. **Still unsure?** Write 「课号待核实」 instead of a guess. A missing number costs one check later;
   a wrong one misfiles the example silently.
4. **Several lessons:** list the lesson that teaches the exact form first and related lessons after
   it, because downstream filing routes by the first one.

Older copies of the map have no 子形态核对 section and list three forms the lecture notes never teach
there: -지 않아도 되다 under L4-8, -(으)면 어때요? under L6-1, -겠- under L8-15. If your copy is one of
those, use the 子形态核对 appendix of `TTMIK_Index.md` in the learner's project knowledge instead.

## Output Format

```
## [Grammar Point Name] — TTMIK Level X Lesson Y

> 📖 语法核心：[one-line Chinese summary, consistent with the map's 教什么 for that lesson]

### 例句 1
**原句：** [Korean]
**场景：** [situation]
**拆解：**
- [morpheme breakdown]
**讲解：**
[Chinese explanation]

### 例句 2
...

---

## [Next Grammar Point] — ...

---

## 📝 词汇积累
| 단어 | 词性 | 意思 | 备注 |
|------|------|------|------|
| ... | ... | ... | ... |

## 💡 好用的表达
| 表达 | 意思 | 用法说明 |
|------|------|----------|
| ... | ... | ... |
```

Header variants:
- Several lessons: `## -다던데요 — TTMIK Level 7 Lesson 18 · Level 10 Lesson 12` (exact-form lesson first)
- No lesson: `## -는 동안 — TTMIK 未单独成课`, or with a closest lesson:
  `## -다면 — TTMIK 未单独成课（最接近：Level 2 Lesson 23）`
- Not yet confirmed: `## [Grammar Point] — TTMIK 课号待核实`

## Output Language Rules
- Explanations in Chinese (中文)
- Korean examples preserved in Korean (한국어)
- Korean grammar terminology in Korean with Chinese gloss on first mention, e.g. 받침（收音/韵尾）
- Section headers in Chinese

## Important Guidelines
1. **No dates anywhere.** Do not stamp examples or sections with dates. Chronology is tracked
   externally (git history when published). Source attribution (which video/article) is fine and
   encouraged; calendar dates are not.
2. **No file-structure assumptions.** Don't reference file names, folders, or "where this gets
   saved." Just produce the analysis. Storage is handled downstream.
3. **Accuracy over quantity.** Skip examples too garbled to analyze reliably.
4. **Real context matters.** Always include 场景.
5. **Level-appropriate depth.** Lower levels (1-3): explain basics. Higher levels (7+): focus on
   nuance and comparison.
6. **Connect to Chinese.** Surface 汉字词 mappings as memory shortcuts.
7. **Distinguish registers.** Mark 반말 / 존댓말 / formal.
8. **Lesson numbers are checked facts, not recall.** See 课号核对.

## TTMIK Grammar Reference
Read `references/ttmik-grammar-map.md` for every lesson number, its type, what it teaches, and the
子形态核对 tables. Every Level X Lesson Y you write must match a row there **and** pass 课号核对. If
the map file is missing, `TTMIK_Index.md` in the learner's project knowledge carries the same lesson
notes and 子形态核对 tables.

## Maintenance
- Version 3. The source copy lives in the study repo (`.claude/skills/korean-grammar-extractor/`,
  tracked in git); the copy installed in the Claude account is made from it (SKILL.md through a
  skill proposal card, the map by re-uploading the folder). If the two differ, the repo copy wins.
- When the map changes, regenerate `TTMIK_Index.md` from it (备注 column and 子形态核对 appendix),
  so the project knowledge says the same thing as the skill.
