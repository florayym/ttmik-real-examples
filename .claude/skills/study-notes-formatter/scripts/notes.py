#!/usr/bin/env python3
"""Repo tool for study-notes-formatter.

  notes.py lookup LESSON     which note file holds a TTMIK lesson (L8-4, 8-4, "Level 8 Lesson 4"),
                             plus the lesson-table row and its 子形态核对 entries
  notes.py lessons           every note file with the lessons on its TTMIK line
  notes.py index [--diff]    rebuild README.md and level-N/README.md
                             (--diff: print what would change, write nothing)
  notes.py topics LESSON...  every topic-page cell that cites these lessons, with its current label
  notes.py check             validate the repo; exits 1 if anything is wrong

Paths are resolved from this file's location, so it runs from any directory.
"""
import os
import re
import subprocess
import sys
import unicodedata
import urllib.parse
import difflib
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
MAP = REPO / "skills/korean-grammar-extractor/references/ttmik-grammar-map.md"
LESSON = re.compile(r"Level (\d+) Lesson (\d+)")
DATE = re.compile(r"(?<!\d)(?:19|20)\d{2}\s*(?:[-./]\s*\d{1,2}\s*[-./]\s*\d{1,2}(?!\d)"
                  r"|年\s*\d{1,2}\s*月(?:\s*\d{1,2}\s*日)?|년\s*\d{1,2}\s*월(?:\s*\d{1,2}\s*일)?)")
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
LABEL = re.compile(r"有例句|待采集|附带出现")


def rel(p):
    return Path(p).resolve().relative_to(REPO).as_posix()


def tag(key):
    return f"L{key[0]}-{key[1]}"


def enc(name):
    return urllib.parse.quote(unicodedata.normalize("NFC", name))


# ---------------------------------------------------------------- data

def lesson_table():
    """{(level, lesson): (type, pattern, teaches)} and the 子形态核对 rows [(subsection, cells)]."""
    rows, sub, lv, section, subsection = {}, [], None, None, None
    for line in MAP.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## Level (\d+)", line)
        if m:
            lv = int(m.group(1))
            continue
        if line.startswith("## "):
            lv, section = None, line[3:].strip()
            continue
        if line.startswith("### "):
            subsection = line[4:].strip()
            continue
        m = re.match(r"^\|\s*L(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]*)\|", line)
        if m and lv:
            rows[(lv, int(m.group(1)))] = (m.group(2).strip(), m.group(3).strip(), m.group(4).strip())
        elif section == "子形态核对" and line.startswith("| ") and not line.startswith("| 形态"):
            sub.append((subsection, [c.strip() for c in line.strip().strip("|").split("|")]))
    return rows, sub


def notes():
    """[(path, h1, [lessons on the TTMIK line], text)] for every level-N/*.md except README.md."""
    out = []
    for p in sorted(REPO.glob("level-*/*.md")):
        if p.name == "README.md":
            continue
        t = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", t, re.M)
        line = re.search(r"^> TTMIK (.+)$", t, re.M)
        lessons = [(int(a), int(b)) for a, b in LESSON.findall(line.group(1))] if line else []
        out.append((p, h1.group(1).strip() if h1 else None, lessons, t))
    return out


def file_for(key):
    return [p for p, _, ls, _ in notes() if ls and ls[0] == key]


def parse_key(s):
    m = re.search(r"(\d+)\D+(\d+)", s)
    if not m:
        sys.exit(f"can't read a lesson from {s!r} (try L8-4)")
    return int(m.group(1)), int(m.group(2))


def suggest_name(pattern):
    """A starting point for a new file's name, from the lesson table's pattern."""
    first = re.split(r"[,，]", pattern)[0]
    first = re.sub(r"^(?:N|V|形容词|动词|疑问词)\s*\+\s*", "", first.strip())
    first = re.sub(r"[（(][^)）]*[一-鿿][^)）]*[)）]", "", first)   # drop Chinese notes like （1）
    first = re.sub(r"\s*\+\s*N$", "", first)
    if not re.search(r"[가-힣ㄱ-ㅎ]", first) or re.search(r"[一-鿿]", first):
        return None
    return re.sub(r"\s+", "-", first.replace("/", "").replace("?", "").strip()) + ".md"


# ---------------------------------------------------------------- indexes

def build_indexes():
    """{path: new content} for every generated index."""
    out, level_stats, source_levels = {}, {}, {}

    def parse(t):
        title = re.search(r"^# (.+)$", t, re.M).group(1).split(" —")[0].strip()
        lesson = tuple(int(x) for x in LESSON.search(re.search(r"^> TTMIK (.+)$", t, re.M).group(1)).groups())
        return title, lesson, len(re.findall(r"^### 例句", t, re.M)), re.findall(r"^## (.+)$", t, re.M)

    for lv in range(1, 11):
        rows, n_files, n_ex = [], 0, 0
        for p in sorted(REPO.glob(f"level-{lv}/*.md")):
            if p.name == "README.md":
                continue
            title, (l, n), ex, sources = parse(p.read_text(encoding="utf-8"))
            rows.append(((n, title), f"| [{title}]({enc(p.name)}) | L{l}.{n:02d} | {ex} |"))
            n_files, n_ex = n_files + 1, n_ex + ex
            for s in sources:
                source_levels.setdefault(s.strip(), set()).add(lv)
        rows.sort(key=lambda r: r[0])
        level_stats[lv] = (n_files, n_ex)
        out[f"level-{lv}/README.md"] = (
            f"# Level {lv} 语法笔记索引\n\n| 语法点 | TTMIK 课号 | 例句数 |\n|--------|-----------|--------|\n"
            + "\n".join(r[1] for r in rows)
            + "\n\n📝 [词汇积累](../_vocabulary.md) · 💡 [好用的表达](../_expressions.md)\n")

    # root README: keep the prose, rebuild the two tables and the 专题导航 line
    root = (REPO / "README.md").read_text(encoding="utf-8")
    overview = "| Level | 语法点数 | 总例句数 |\n|-------|---------|---------|\n" + "\n".join(
        f"| [Level {lv}](level-{lv}/) | {level_stats[lv][0]} | {level_stats[lv][1]} |" for lv in range(1, 11))
    root = re.sub(r"\| Level \| 语法点数 \| 总例句数 \|\n\|[-|]+\|\n(?:\|.*\|\n?)+", overview + "\n", root)
    listed = [s for s, _ in re.findall(r"^\| (.+?) \| (L\d.*?) \|$", root, re.M)]
    order = [s for s in listed if s in source_levels] + sorted(s for s in source_levels if s not in listed)
    sources = "| 来源 | 涵盖级别 |\n|------|---------|\n" + "\n".join(
        f"| {s} | {', '.join(f'L{x}' for x in sorted(source_levels[s]))} |" for s in order)
    root = re.sub(r"\| 来源 \| 涵盖级别 \|\n\|[-|]+\|\n(?:\|.*\|\n?)+", sources + "\n", root)
    pages = sorted(REPO.glob("topics/*.md"))

    def label(p):
        return re.search(r"^# (.+)$", p.read_text(encoding="utf-8"), re.M).group(1).split(" —")[0].strip()

    links = [f"[专题总览](topics/{enc('README.md')})" for p in pages if p.name == "README.md"] + [
        f"[{label(p)}](topics/{enc(p.name)})" for p in pages if p.name != "README.md"]
    root = re.sub(r"^📚 专题导航：.*$", "📚 专题导航：" + " · ".join(links), root, flags=re.M)
    out["README.md"] = root
    return out


def stale_indexes():
    """[(path, old, new)] for indexes whose content differs from a fresh build."""
    stale = []
    for path, new in build_indexes().items():
        f = REPO / path
        old = f.read_text(encoding="utf-8") if f.exists() else ""
        if old != new:
            stale.append((path, old, new))
    return stale


# ---------------------------------------------------------------- commands

def cmd_lookup(arg):
    rows, sub = lesson_table()
    key = parse_key(arg)
    if key not in rows:
        print(f"{tag(key)} is not a lesson in the lesson table")
        return 1
    typ, pattern, teaches = rows[key]
    print(f"{tag(key)}  {typ} · {pattern} — {teaches}")
    if typ in ("操练", "复习"):
        print("  (teaches nothing new — never file under it)")
    hits = file_for(key)
    for p in hits:
        print(f"file: {rel(p)}")
    if not hits:
        name = suggest_name(pattern)
        print("file: none" + (f" — a new file would be level-{key[0]}/{name}" if name else ""))
    for p, _, ls, _ in notes():
        if key in ls[1:]:
            print(f"also on the TTMIK line of: {rel(p)}")
    for table, cells in sub:
        if any(re.search(rf"(?<![\d-]){re.escape(tag(key))}(?!\d)", c) for c in cells):
            print(f"子形态核对 · {table}: " + " | ".join(cells))
    return 0


def cmd_lessons():
    for p, h1, ls, _ in sorted(notes(), key=lambda x: x[2][:1] or [(99, 99)]):
        print(f"{' · '.join(tag(k) for k in ls) or '—':16s} {rel(p):40s} {h1 or ''}")
    return 0


def cmd_index(diff=False):
    stale = stale_indexes()
    for path, old, new in stale:
        if diff:
            sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), new.splitlines(True), path, path + " (rebuilt)"))
        else:
            (REPO / path).write_text(new, encoding="utf-8")
    print(f"{len(stale)} index file(s) {'would change' if diff else 'rewritten'}")
    return 0


def cmd_topics(args):
    keys = [parse_key(a) for a in args]
    found = 0
    for page, cells in topic_rows():
        for i, cell in enumerate(cells):
            hit = [k for k in keys if k in cell_lessons(cells, i)]
            if hit and LABEL.search(cell):
                found += 1
                print(f"topics/{page.name} · {', '.join(tag(k) for k in hit)} · row 「{' | '.join(cells[:2])[:50]}」\n    {cell}")
    print(f"{found} labelled cell(s)")
    return 0


def git_names():
    """Paths exactly as git stores them (tracked, plus untracked files that aren't ignored)."""
    r = subprocess.run(["git", "-C", str(REPO), "-c", "core.quotepath=off", "ls-files", "-z",
                        "--cached", "--others", "--exclude-standard"], capture_output=True)
    return set(r.stdout.decode("utf-8").split("\0")) - {""}


def strip_code(text):
    """Remove fenced code blocks and inline code, so example links inside them aren't checked."""
    text = re.sub(r"^```.*?^```[^\n]*$", "", text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", "", text)


def lessons_in(text):
    return [(int(a), int(b)) for a, b in re.findall(r"(?<![\w-])L(\d+)-(\d+)(?!\d)", text)]


def topic_rows():
    """(page, cells) for every table row of the topic pages (the hub excluded)."""
    for page in sorted(REPO.glob("topics/*.md")):
        if page.name != "README.md":
            for cells in table_rows(page.read_text(encoding="utf-8")):
                yield page, cells


def cell_lessons(cells, i):
    """The lessons a cell is about: the ones written in it, else the row's first lesson."""
    return lessons_in(cells[i]) or next((lessons_in(c)[:1] for c in cells if lessons_in(c)), [])


def table_rows(text):
    for line in text.splitlines():
        if line.startswith("|") and not re.match(r"^\|[-\s|:]+\|$", line):
            yield [c.strip() for c in line.strip().strip("|").split("|")]


def cmd_check():
    rows, _ = lesson_table()
    errors = []
    all_notes = notes()

    # note files: lessons exist, folder matches, one file per lesson, has examples
    first = {}
    for p, h1, ls, t in all_notes:
        r = rel(p)
        if not h1:
            errors.append(f"{r}: no H1 title")
        if not ls:
            errors.append(f"{r}: no '> TTMIK Level X Lesson Y' line")
            continue
        for k in ls:
            if k not in rows:
                errors.append(f"{r}: {tag(k)} is not in the lesson table")
            elif rows[k][0] in ("操练", "复习"):
                errors.append(f"{r}: cites {tag(k)}, a {rows[k][0]} lesson")
        if ls[0][0] != int(p.parent.name.split("-")[1]):
            errors.append(f"{r}: first lesson {tag(ls[0])} doesn't belong in {p.parent.name}/")
        first.setdefault(ls[0], []).append(r)
        if not re.search(r"^### 例句", t, re.M):
            errors.append(f"{r}: no 例句 left — delete the file")
        for a, b in re.findall(r"(?<![\w-])L(\d+)(?: L|-)(\d+)(?!\d)", t):   # 「L7 L12」/「L7-12」 in the text
            k = (int(a), int(b))
            if k not in rows or rows[k][0] in ("操练", "复习"):
                errors.append(f"{r}: mentions {tag(k)}, which is not a lesson that teaches anything")
    for k, files in first.items():
        if len(files) > 1:
            errors.append(f"{tag(k)} is in {len(files)} files: {', '.join(files)} — one lesson, one file")

    # calendar dates (example sentences may mention dates as content, so 原句 lines are skipped)
    scope = [p for p, *_ in all_notes] + [REPO / "_vocabulary.md", REPO / "_expressions.md", REPO / "README.md"] \
        + sorted(REPO.glob("topics/*.md"))
    for p in scope:
        if not p.exists():
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            m = DATE.search(line)
            if m and not line.startswith("**原句："):
                errors.append(f"{rel(p)}:{i}: calendar date 「{m.group(0)}」 — chronology lives in git log")

    # links resolve to the exact path git stores (an NFD-spelled link 404s on GitHub)
    names = git_names()
    md_files = [p for p in REPO.rglob("*.md") if not set(p.relative_to(REPO).parts[:1]) & {".claude", "tools", ".git"}]
    for md in md_files:
        for _, href in LINK.findall(strip_code(md.read_text(encoding="utf-8"))):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = href.split("#")[0]
            target = os.path.normpath(os.path.join(os.path.dirname(rel(md)), urllib.parse.unquote(path)))
            if target in names or (REPO / target).is_dir():
                continue
            if unicodedata.normalize("NFC", target) in names:
                errors.append(f"{rel(md)}: link {href} spells the file differently from git (Unicode normalisation)")
            else:
                errors.append(f"{rel(md)}: broken link {href}")

    # indexes current
    stale = stale_indexes()
    if stale:
        errors.append("indexes out of date: " + ", ".join(p for p, _, _ in stale) + " — run notes.py index")

    # topic pages: an 有例句 link must lead to a file of that cell's lesson, and a quoted 附带出现
    # fragment must still be in the file it links to
    by_path = {rel(p): (ls, t) for p, _, ls, t in all_notes}
    for page, cells in topic_rows():
        for i, cell in enumerate(cells):
            keys = cell_lessons(cells, i)
            for label, href in LINK.findall(cell):
                target = os.path.normpath(os.path.join("topics", urllib.parse.unquote(href)))
                first_lesson = by_path.get(target, ([], ""))[0][:1]
                if label == "有例句" and keys and first_lesson and first_lesson[0] not in keys:
                    errors.append(f"topics/{page.name}: 有例句 for {', '.join(tag(k) for k in keys)} links to "
                                  f"{target}, a {tag(first_lesson[0])} file")
            for href, frag in re.findall(r"\]\(([^)\s]+)\)\s*「([^」]+)」", cell):
                target = os.path.normpath(os.path.join("topics", urllib.parse.unquote(href)))
                if target in by_path:
                    said = " ".join(l for l in by_path[target][1].splitlines() if l.startswith("**原句："))
                    if frag not in said.replace("**", ""):
                        errors.append(f"topics/{page.name}: 「{frag}」 is not in any 原句 of {target}")

    for e in errors:
        print("ERROR ", e)
    print(f"{len(all_notes)} notes checked · {len(errors)} error(s)")
    return 1 if errors else 0


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "lookup" and rest:
        return cmd_lookup(" ".join(rest))
    if cmd == "lessons":
        return cmd_lessons()
    if cmd == "index":
        return cmd_index(diff="--diff" in rest)
    if cmd == "topics" and rest:
        return cmd_topics(rest)
    if cmd == "check":
        return cmd_check()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
