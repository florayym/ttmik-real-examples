"""Split the text of TTMIK's three lesson-note volumes into lessons.

  segment.py LEVELS1-3.txt LEVELS4-7.txt LEVELS8-10.txt -o lessons.json

Input: the PDFs' text layer, each page's header on its own line.
- Volumes 1–2 and Levels 8–9: only UPPERCASE `LEVEL X LESSON Y[ - title]` lines start a lesson. Mixed-case
  `Level X Lesson Y` lines in volume 1 head workbook questions; workbook pages belong to no lesson.
- Level 10 uses short mixed-case `Level 10 Lesson N` / `TTMIK Level 10 Lesson N` lines.
- In-text review lists (`Level 5 Lesson 16: VERB + …`) never start a lesson.
- A header that breaks the local order (previous + 1 expected, next == previous + 2) is relabelled
  previous + 1. This repairs L6-2, whose page header is misprinted `LEVEL 6 LESSON 12`.
Output: {"6-2": [lines…], …}.
"""
import collections
import json
import re
import sys

UP = re.compile(r"^LEVEL\s+(\d+)\s+LESSON\s+(\d+)(\s+-\s+.*)?\s*$")
L10 = re.compile(r"^(?:TTMIK\s+)?Level\s+(10)\s+Lesson\s+(\d+)\s*$")
WORKBOOK = re.compile(r"(WORKBOOK|reinforce what you have learned|Please answer the following questions)", re.I)
TEST = re.compile(r"^\s*(TEST YOUR KOREAN|Test Your Korean)", re.I)


def main(argv):
    if "-o" not in argv or len(argv) != 5:
        print(__doc__)
        return 2
    i = argv.index("-o")
    out_path = argv[i + 1]
    parts = [a for j, a in enumerate(argv) if j not in (i, i + 1)]

    runs = []  # [volume, level, lesson, lines]
    for vol, path in enumerate(parts, 1):
        cur = None
        for raw in open(path, encoding="utf-8"):
            line = raw.rstrip("\n")
            st = line.strip()
            m = UP.match(st) or (L10.match(st) if vol == 3 else None)
            if m:
                key = (int(m.group(1)), int(m.group(2)))
                if runs and runs[-1][0] == vol and (runs[-1][1], runs[-1][2]) == key:
                    cur = runs[-1]
                else:
                    cur = [vol, key[0], key[1], []]
                    runs.append(cur)
                continue
            if (vol == 1 and WORKBOOK.search(st)) or TEST.match(st):
                cur = None
            if cur is not None:
                cur[3].append(line)

    merged = []
    for r in runs:
        if merged and (merged[-1][1], merged[-1][2]) == (r[1], r[2]):
            merged[-1][3].extend(r[3])
        else:
            merged.append(r)
    repairs = []
    for j in range(1, len(merged) - 1):
        a, b, c = merged[j - 1], merged[j], merged[j + 1]
        if a[1] == b[1] == c[1] and b[2] != a[2] + 1 and c[2] == a[2] + 2:
            repairs.append(f"L{b[1]}-{b[2]} -> L{b[1]}-{a[2] + 1}")
            b[2] = a[2] + 1

    lessons = collections.OrderedDict()
    for _, lv, n, lines in merged:
        lessons.setdefault(f"{lv}-{n}", []).extend(lines)
    json.dump(lessons, open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
    print("header repairs:", repairs or "none")
    for lv in range(1, 11):
        have = sorted(int(k.split("-")[1]) for k in lessons if int(k.split("-")[0]) == lv)
        expected = range(1, 26 if lv == 1 else 31)   # the PDFs carry no Essential Review lessons
        missing = [n for n in expected if n not in have]
        extra = [n for n in have if n not in expected]
        print(f"L{lv}: {len(have)} lessons" + (f"; missing {missing}" if missing else "") + (f"; extra {extra}" if extra else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
