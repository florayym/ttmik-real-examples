"""Read TTMIK's lecture notes by lesson.

  lesson.py show L3-14 [--chars N]     the lesson's text, page boilerplate and romanisation dropped
  lesson.py grep REGEX [L3-14 …]       every match with context, in the given lessons (default: all)

Lesson texts come from segment.py: --lessons PATH, or $TTMIK_LESSONS.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import lesson_key, lessons_arg, load_lessons

BOILER = re.compile(r"TalkToMeInKorean\.com - Free Korean Lesson Notes|This PDF is to be used along with the MP3 "
                    r"audio lesson available at TalkToMeInKorean\.com\.|Please feel free to share TalkToMeInKorean.s "
                    r"free Korean lessons and PDF files with anybody who is studying Korean\.|If you have any "
                    r"questions or feedback, visit TalkToMeInKorean\.com\.")


def main(argv):
    path = lessons_arg(argv)
    if len(argv) < 2 or argv[0] not in ("show", "grep"):
        print(__doc__)
        return 2
    L = load_lessons(path)
    if argv[0] == "show":
        chars = int(argv[argv.index("--chars") + 1]) if "--chars" in argv else 4000
        for a in [a for a in argv[1:] if not a.isdigit() and a != "--chars"]:
            k = lesson_key(a)
            text = re.sub(r"\s*\[[^\]]{0,80}\]", "", BOILER.sub("", L[k]))
            print(f"===== L{k}\n{re.sub(r'  +', ' ', text).strip()[:chars]}\n")
        return 0
    pattern = re.compile(argv[1])
    keys = [lesson_key(a) for a in argv[2:]] or list(L)
    total = 0
    for k in keys:
        hits = list(pattern.finditer(L[k]))
        if hits:
            total += len(hits)
            print(f"L{k}: {len(hits)} match(es)")
            for m in hits[:8]:
                print("   …" + L[k][max(0, m.start() - 60):m.end() + 60] + "…")
    print(f"{total} match(es) in {len(keys)} lesson(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
