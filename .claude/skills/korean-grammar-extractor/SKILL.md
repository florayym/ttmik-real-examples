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
or how/where notes are stored. Those concerns belong to the publisher/formatter skill and to
the repo's CLAUDE.md. Keeping this skill environment-agnostic means it works identically whether
run in a Project, in Claude Code, or anywhere else.

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
Consult `references/ttmik-grammar-map.md` to determine which grammar patterns belong to the
requested level(s), then scan the text for occurrences. The map is verified against the TTMIK
lesson-note PDFs and lists only core grammar — Word Builder, Sentence Building Drills, vocabulary,
tense-review, and Advanced Idiomatic/Situational Expression lessons are intentionally omitted. So a
lesson number missing from a level's table is a non-grammar lesson, not a gap to invent grammar for.

### Step 3: Extract and Organize
For each grammar point found:
1. List all occurrences from the source
2. Pick the best 2-3 examples — complete, natural, clearly demonstrating the point, from
   varied speakers/contexts, not too garbled.

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
colloquial contractions, slang, culturally specific phrases. TTMIK's Advanced Idiomatic Expression
lessons (Levels 8-10, organized by body parts / themes like 눈·손·마음·말) sit outside the grammar
map but make a good checklist for this section — surface matches when the text contains them.

## Output Format

```
## [Grammar Point Name] — TTMIK Level X Lesson Y

> 📖 语法核心：[one-line Chinese summary]

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

## TTMIK Grammar Reference
Read `references/ttmik-grammar-map.md` to verify levels, find lesson numbers, or check what
grammar exists at a given level.
