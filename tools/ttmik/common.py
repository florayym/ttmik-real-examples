"""Shared helpers for the TTMIK data tools."""
import itertools
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAP = REPO / "skills/korean-grammar-extractor/references/ttmik-grammar-map.md"


def lessons_arg(argv):
    """Pop `--lessons PATH` from argv; fall back to $TTMIK_LESSONS."""
    if "--lessons" in argv:
        i = argv.index("--lessons")
        path = argv[i + 1]
        del argv[i:i + 2]
        return path
    path = os.environ.get("TTMIK_LESSONS")
    if not path:
        sys.exit("lecture-note texts: pass --lessons PATH or set TTMIK_LESSONS (segment.py makes the file)")
    return path


def load_lessons(path):
    """{"3-14": text} with whitespace collapsed."""
    raw = json.load(open(path, encoding="utf-8"))
    return {k: re.sub(r"\s+", " ", " ".join(v)) for k, v in raw.items()}


def lesson_rows():
    """{"3-14": (type, pattern, teaches)} from the lesson table."""
    rows, lv = {}, None
    for line in MAP.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## Level (\d+)", line)
        if m:
            lv = int(m.group(1))
            continue
        if line.startswith("## "):
            lv = None
            continue
        m = re.match(r"^\|\s*L(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]*)\|", line)
        if m and lv:
            rows[f"{lv}-{int(m.group(1))}"] = (m.group(2).strip(), m.group(3).strip(), m.group(4).strip())
    return rows


def sub_tables():
    """{subsection title: [[cells], …]} for the tables under ## 子形态核对."""
    out, section, sub = {}, None, None
    for line in MAP.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        elif line.startswith("### "):
            sub = line[4:].strip()
        elif section == "子形态核对" and line.startswith("| ") and not re.match(r"^\|\s*形态\s*\|", line):
            out.setdefault(sub, []).append([c.strip() for c in line.strip().strip("|").split("|")])
    return out


def lesson_key(s):
    m = re.search(r"(\d+)\D+(\d+)", s)
    if not m:
        sys.exit(f"not a lesson: {s!r} (try L3-14)")
    return f"{int(m.group(1))}-{int(m.group(2))}"


def keys_in(text):
    return [f"{a}-{b}" for a, b in re.findall(r"(?<![\w-])L(\d+)-(\d+)(?!\d)", text)]


# ---------------------------------------------------------------- matching forms in the notes

CONJUGATED = {"하": ["해", "했", "합"], "되": ["돼", "됐", "됩"]}   # stem endings the notes write conjugated
UNIT = re.compile(r"(?:\([^)]*\))?[가-힣ㄱ-ㅎ]")   # one syllable or jamo, maybe with an optional (으) in front


def _top_split(s, sep="/"):
    parts, depth, cur = [], 0, ""
    for ch in s:
        depth += (ch == "(") - (ch == ")")
        if ch == sep and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    return parts + [cur]


def expand(form):
    """The forms a notation stands for, as combos: each combo is a list of strings, any one of which
    may occur. Slashes between one-syllable alternatives (아/어/여, 은/는) mark allomorphs — one combo.
    Other slashes (-는/(으)ㄴ/(으)ㄹ, 되다/하다) separate forms — one combo each, all must be taught.
    A suffix written once after the last alternative belongs to all of them (-아/어/여야, -(으)ㄴ/는지)."""
    depth = 0
    for i, ch in enumerate(form):
        depth += (ch == "(") - (ch == ")")
        if ch == "/" and depth == 0:
            j = i
            while j > 0 and form[j - 1] not in " -":
                j -= 1
            k, d = i, 0
            while k < len(form) and not (form[k] == " " and d == 0):
                d += (form[k] == "(") - (form[k] == ")")
                k += 1
            prefix, alts, rest = form[:j], _top_split(form[j:k]), form[k:]
            suffix = ""
            if len(alts) > 1 and all(UNIT.fullmatch(a) for a in alts[:-1]) and not UNIT.fullmatch(alts[-1]):
                m = UNIT.match(alts[-1])
                if m:
                    suffix, alts = alts[-1][m.end():], alts[:-1] + [alts[-1][:m.end()]]
            allomorphs = all(re.fullmatch(r"[가-힣]", a) for a in alts)
            out = []
            for rc in expand(rest):
                if allomorphs:
                    out.append([prefix + a + suffix + r for a in alts for r in rc])
                else:
                    out += [[prefix + a + suffix + r for r in rc] for a in alts]
            return out
    return [[form]]


def spellings(s):
    """Ways a form can be written in the notes: optional parts dropped or kept, a final -다 conjugated."""
    s = re.sub(r"\(\?\)|\?", "", s).lstrip("-")
    groups = re.split(r"(\([^)]*\))", s)
    options = [["", g[1:-1]] + g[1:-1].split("/") if g.startswith("(") else [g] for g in groups]
    out = {re.sub(r"[\s+]", "", s)}                      # as written, e.g. (으)ㄴ in "-(으)ㄴ + noun"
    for combo in itertools.product(*options):
        c = re.sub(r"[\s+]", "", "".join(combo))
        out.add(c)
        if c.endswith("다") and len(c) > 2:
            stem = c[:-1]
            out |= {stem} | {stem[:-1] + v for v in CONJUGATED.get(stem[-1], "")}
        m = re.match(r"^[ㄱ-ㅎ]+", c)
        if m and len(c) - m.end() >= 2:                 # -(으)ㄹ 만큼 → 놀랄 만큼: the jamo sits on the stem
            out.add(c[m.end():])
    return {c for c in out if re.search(r"[가-힣]", c)}


def occurs(text_ns, s):
    """Whether form s occurs in a lesson text with spaces and "+" removed."""
    return any(c in text_ns for c in spellings(s))
