"""The earlier lessons a lesson's notes refer back to (the 原文回指 column of the topic pages).

  backrefs.py [L5-17 …]      (default: every lesson that has any)

Counts only what the notes say explicitly: "Level X Lesson Y" pointing to an earlier lesson, and a
singular "the previous lesson". Some printed references are wrong (L5-29 says Lesson 16 for L5-17;
L8-6 says Level 6 Lesson 2 for L6-12); the 子形态核对 section of the lesson table lists them — never
copy those onto a page.

Lesson texts come from segment.py: --lessons PATH, or $TTMIK_LESSONS.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import lesson_key, lessons_arg, load_lessons

EXPLICIT = re.compile(r"level\s*(\d+)\s*,?\s*lesson\s*(\d+)", re.I)
PREVIOUS = re.compile(r"\b(in|from|introduced in|covered in|learned in|looked at in) (the|our) previous lesson\b(?!s)", re.I)


def backrefs(key, text):
    lv, n = map(int, key.split("-"))
    found, seen = [], set()
    for m in EXPLICIT.finditer(text):
        target = (int(m.group(1)), int(m.group(2)))
        if target < (lv, n) and target not in seen:
            seen.add(target)
            found.append((f"L{target[0]}-{target[1]}", text[max(0, m.start() - 60):m.end() + 40]))
    m = PREVIOUS.search(text)
    if m:
        found.append((f"L{lv}-{n - 1}（上一课）", text[max(0, m.start() - 20):m.end() + 60]))
    return found


def main(argv):
    L = load_lessons(lessons_arg(argv))
    keys = [lesson_key(a) for a in argv] or list(L)
    for k in keys:
        refs = backrefs(k, L[k])
        if refs or argv:
            print(f"L{k}: " + ("、".join(r for r, _ in refs) or "—"))
            for r, ctx in refs:
                print(f"    {r}: …{ctx}…")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
