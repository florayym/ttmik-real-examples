"""Check the topic pages' lesson citations against TTMIK's lecture notes.

  check_topics.py [--lessons PATH]

1. Every L<x>-<y> on a page is a lesson in the lesson table.
2. In every table cell (or row, for one-form-per-row tables) each Korean form written next to lesson
   numbers occurs in the notes of at least one lesson cited there — spaces and optional parts such as
   (으) or (ㄴ/는) ignored, a final -다 also matched conjugated. 「课程外」 tables and quoted repo fragments are skipped.
Links are checked by the formatter's `notes.py check`.

Lesson texts come from segment.py: --lessons PATH, or $TTMIK_LESSONS. Exits 1 on a problem.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CONJUGATED, REPO, keys_in, lesson_rows, lessons_arg, load_lessons


def core(x):
    """Hangul only: optional parts like (으) (ㄴ/는) and alternations like 았/었/였 dropped, (요) kept."""
    x = re.sub(r"\((?!요\))[^)]*\)", "", x)
    x = re.sub(r"(?:[가-힣]/)+[가-힣]", "", x)
    return re.sub(r"[^가-힣]", "", x)


def variants(c):
    """A form's core, plus its conjugated spellings when it ends in a dictionary-form -다."""
    out = {c}
    if c.endswith("다") and len(c) > 2:
        stem = c[:-1]
        out |= {stem} | {stem[:-1] + v for v in CONJUGATED.get(stem[-1], "")}
    return out


def forms_in(cell):
    cell = re.sub(r"\[[^\]]*\]\([^)]*\)", "", cell)     # links
    cell = re.sub(r"「[^」]*」", "", cell)                 # quoted repo fragments
    cell = cell.replace(" / ", " ， ")
    out = []
    for f in re.findall(r"(?:-|N \+ |V \+ |V-)?[가-힣ㄱ-ㅎ()/]+(?: [가-힣()/]+)*", cell):
        c = core(f)
        if re.fullmatch(r"[가-힣]{2,}", c):
            out.append((f.strip(), c))
    return out


def main(argv):
    L = {k: core(t) for k, t in load_lessons(lessons_arg(argv)).items()}
    rows = lesson_rows()
    problems, checked = [], 0
    for page in sorted((REPO / "topics").glob("*.md")):
        text = page.read_text(encoding="utf-8")
        for k in keys_in(text):
            if k not in rows:
                problems.append(f"{page.name}: L{k} is not a lesson")
        if page.name == "README.md":
            continue
        section = ""
        for line in text.splitlines():
            if line.startswith("## "):
                section = line
            if not line.startswith("| ") or line.startswith("|---") or "课程外" in section:
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            row_keys = keys_in(line)
            for c in cells:
                ckeys = keys_in(c) or row_keys
                if not ckeys or "原文写作" in c:
                    continue
                for form, cf in forms_in(c):
                    checked += 1
                    if not any(v in L[k] for k in ckeys if k in L for v in variants(cf)):
                        problems.append(f"{page.name}: 「{form}」 not in the notes of {', '.join('L' + k for k in ckeys)} :: {c[:60]}")
    print(f"{checked} form citation(s) checked")
    print("PROBLEMS:" if problems else "PROBLEMS: none")
    for p in problems:
        print("  ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
