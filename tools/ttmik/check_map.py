"""Check the lesson table against TTMIK's lecture notes.

  check_map.py [--lessons PATH]

1. Lesson rows: every form a 语法 / 总结 row names (句型 and 教什么 columns) is looked up in that
   lesson's notes. Forms not found literally are listed for review: most are conjugation variants
   (the notes write -어요 where the table writes -다). Look each one up with `lesson.py grep` before
   changing the table.
2. 子形态核对: every row's lessons exist; every 课内讲到的形态 row has evidence below that is found in
   the notes; every L1–L10 没有课的形态 row's pattern occurs in no lesson outside the allowed ones; and
   a few claims that a lesson does NOT teach something hold. A row without evidence is reported —
   add an entry here once you've read the lesson.

Lesson texts come from segment.py: --lessons PATH, or $TTMIK_LESSONS. Exits 1 if anything fails.
"""
import itertools
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import expand, keys_in, lesson_rows, lessons_arg, load_lessons, occurs, sub_tables

# 课内讲到的形态: form (exactly as in the table) -> {lesson: [regexes that must occur in its notes]}
TAUGHT = {
    "N + 밖에 + 否定": {"3-18": [r"밖에"], "2-15": [r"adding -만"]},
    "-기（动词名词化）": {"2-14": [r"Adding -기"], "2-19": [r"-는 것"]},
    "못 + V「不能」": {"2-17": [r"adding 못 before a verb"]},
    "-아/어/여서（原因、先后）": {"3-7": [r"-아/어/여\+서"]},
    "그러면 · 그럼": {"3-15": [r"그러면 is a combination of 그렇다", r"그럼"]},
    "이러면 · 그러면 · 저러면（ㅎ 脱落）": {"4-23": [r"the consonant ㅎ is dropped"]},
    "-(으)면 -(으)ㄹ수록": {"4-1": [r"바쁘면 바쁠수록"]},
    "안 + V-아/어/여도 되다「不…也可以」": {"4-8": [r"안 먹어도 돼요"], "1-21": [r"the negative verb ending, 지 않다"]},
    "-아/어/여도 돼요? · 괜찮아요? · 될까요?": {"6-4": [r"-아/어/여도 돼요\?", r"-아/어/여도 괜찮아요\?", r"-아/어/여도 될까요\?"]},
    "-(이)라는 + N": {"5-12": [r"-\(이\)라는"]},
    "-(ㄴ/는)다는 + N": {"5-17": [r"-\(ㄴ/는\)다는"]},
    "-았/었/였다고 · -(으)ㄹ 거라고": {"5-29": [r"-았/었/였 \+ -다고", r"-\(으\)ㄹ 거 \+ -라고"]},
    "-(이)라는 것(은) · -(이)란": {"6-15": [r"-\(이\)란"]},
    "-(ㄴ/는)다는 것": {"7-28": [r"-\(ㄴ/는\)다는 것"]},
    "-(이)라니까 · -(으)라니까": {"7-16": [r"-\(이\)라니까", r"-\(으\)라니까"]},
    "-(ㄴ/는)다던데(요) · -(이)라던데(요)": {"7-18": [r"-\(ㄴ/는\)다던데"], "10-12": [r"Noun \+ -\(이\)라던데요"]},
    "-(ㄴ/는)다는데(요) · -(이)라는데(요)": {"7-18": [r"-\(ㄴ/는\)다는데", r"-\(이\)라는데"]},
    "-(ㄴ/는)다잖아요 · -라잖아요": {"7-21": [r"-\(ㄴ/는\)다잖아요"]},
    "-(ㄴ/는)다면서(요) · -(이)라면서(요) · -(으)라면서(요)": {"9-24": [r"-\(ㄴ/는\)다면서", r"가라면서요"]},
    "-(ㄴ/는)다니（= -다고 하니）· -(으)라니": {"10-14": [r"short for -\(ㄴ/는\)다고 하니", r"-\(으\)라고 하니"]},
    "-(ㄴ/는)다거나": {"10-7": [r"-\(ㄴ/는\)다거나"]},
    "-기만 하면 · -(느)ㄴ 한 · -지만 않으면": {"7-27": [r"-기만 하면", r"-\(느\)ㄴ 한", r"-지만 않으면"]},
    "-았/었/였으면 좋겠어요": {"8-8": [r"The past tense version"]},
    "-(으)면 -(으)ㄹ 텐데 · -았/었/였으면 -았/었/였을 텐데": {"10-11": [r"-\(으\)면 -\(으\)ㄹ 텐데", r"-았/었/였으면 -았/었/였을 텐데"]},
    "얼마나 -(으)면": {"10-27": [r"얼마나 -\(으\)면"]},
    "V-기는 하다 · V-기는 V": {"6-24": [r"가기는 했어요", r"가기는 갔어요"]},
    "V + -는데도 (불구하고) · N + -에도 불구하고": {"8-28": [r"-는데도 불구하고", r"Noun \+ -에도 불구하고"]},
    "-(으)ㄹ 때「…的时候」": {"6-29": [r"the -\(으\)ㄹ 때 ending"]},
    "때문에 · 덕분에": {"10-13": [r"most commonly used expression is 때문에", r"덕분에"]},
    "动词 + -(으)ㄴ + N（过去时定语）": {"4-26": [r"past tense\W{0,3}noun groups", r"-\(으\)ㄴ \[-\(eu\)n\] \+ noun"]},
    "动词 + -(으)ㄹ + N（将来时定语）": {"4-25": [r"future tense noun groups", r"-\(으\)ㄹ \[-\(eu\)l\] \+ noun"]},
    "-던 · -았/었/였던（回想定语）": {"8-4": [r"-던 and -았/었/였던"]},
    "-(으)ㅁ（名词形）": {"9-9": [r"-\(으\)ㅁ"]},
    "-(으)면서": {"9-23": [r"-\(으\)면서"]},
    "-아/어/여야겠다 · -지 말아야겠다": {"10-24": [r"-아/어/여야겠다", r"-지 말아야겠다"]},
    "-겠-": {"6-16": [r"-겠-"]},
    "-았/었/였었- · -고는 했다 · -(으)ㄴ 적 있다": {"8-9": [r"-았/었/였었어요", r"-고는 했어요", r"-\(으\)ㄴ 적 있어요"]},
    "-(으)ㄹ 계획이다 · -(으)ㄹ 예정이다 · -(으)ㄹ지도 모르다 · -(으)ㄹ까 생각 중이다 · -(으)ㄹ까 하다": {
        "8-15": [r"-\(으\)ㄹ 계획이에요", r"-\(으\)ㄹ 예정이에요", r"-\(으\)ㄹ지도 몰라요", r"-\(으\)ㄹ까 생각 중이에요", r"-\(으\)ㄹ까 해요"]},
    "-(이)나 vs -(이)라도（退而求其次）": {"10-4": [r"how it is different from -\(이\)라도"]},
}

# L1–L10 没有课的形态: form -> (regex that must occur in no lesson's notes, lessons where it may occur
# only inside an example sentence). None = checked by a NOT_TAUGHT claim instead.
ABSENT = {
    "-(으)면 어때요?": (r"면어때", set()),
    "-자고 하다 · -재요（转述提议）": (r"자고(하|했|해요|그러)|재요", set()),
    "-냐는 + N · -냬요": (r"냐는|냬", set()),
    "-(으)래요（转述命令的缩略）": (r"으래요|(?<![이])[하가오주보]래요", set()),
    "-아/어 달라고": (r"달라고|달래", {"9-2"}),
    "-다(고 하)길래": (r"다길래|다고하길래|라길래", set()),
    "V-지만": (None, set()),
    "-다면": (r"다면(?!서)", {"8-28"}),
    "-더라도（单用）": (r"더라도", {"8-19", "8-20", "9-30"}),
    "-는 동안": (r"는동안|은동안", set()),
    "-고 나서": (r"고나서", {"9-6"}),
    "-든지 · -든가": (r"든지|든가", {"6-18"}),
    "-다시피 · -듯이": (r"다시피|듯이", set()),
    "-나요? · -(으)ㄴ가요?": (r"나요\?|은가요\?|인가요\?", {"1-19", "2-7", "2-8", "9-8", "10-14"}),
    "-아/어야지": (r"야지", {"10-21"}),
    "-았/었다가（做完再…）": (r"[았었였]다가", set()),
    "-다 보니(까)「…着…就（发现、变得）」": (r"다보니", set()),
    "-고 보니(까)「…了才发现」": (r"고보니", set()),
    "-(으)면 되다「只要…就行」": (r"면되|면돼|면됩|면될", {"8-14"}),
    "-아/어 드리다（-아/어 주다 的谦让形）": (r"드리|드려|드릴|드렸|드립", {"8-23", "10-14"}),
    "-았/었을 거예요（对过去的推测）": (r"[았었였]을거", {"8-17"}),
}

# claims that a lesson does NOT teach something (the table's notes rely on them)
NOT_TAUGHT = [
    ("3-14", r"-\(으\)ㄴ|-\(으\)ㄹ|[Pp]ast tense|[Ff]uture tense", "L3-14 teaches a past / future verb modifier"),
    ("3-22", r"지 모르|지 몰라", "L3-22 teaches -(으)ㄹ지도 모르다"),
    ("6-1", r"면 어때", "L6-1 teaches -(으)면 어때요?"),
    ("2-6", r"(?<!그렇)지만", "L2-6 teaches a -지만 ending"),
    ("8-15", r"-겠-", "L8-15 teaches -겠-"),
    ("5-14", r"[Ff]ound|[Dd]iscover|[Rr]ealiz|[Tt]urn(?:ed|s)? out", "L5-14 teaches a discovery -(으)니까"),
]


def has(text, rx):
    return bool(re.search(rx, text) or re.search(rx.replace(" ", ""), re.sub(r"\s+", "", text)))


# ---------------------------------------------------------------- 1. lesson rows

def forms_named(pattern, teaches):
    """Hyphen-led forms written in a row; cross-references to other lessons are left out."""
    teaches = re.sub(r"[（(][^）)]*(?:见|与|和|不是|对比|vs)[^）)]*[）)]", " ", teaches)
    teaches = re.sub(r"(?:见|与|和|不是)\s*L\d+-\d+\S*", " ", teaches)
    teaches = re.sub(r"官方课名[^，；]*", " ", teaches)   # a description of the course title, not a claim
    out = []
    for piece in re.split(r",|，|、|；| vs | / ", pattern + "，" + teaches):
        piece = re.sub(r"(?:形容词|动词|疑问词|N|V)\s*\+\s*|\s*\+\s*N\b", "", piece)
        out += re.findall(r"-[가-힣ㄱ-ㅎ()/~?]+(?: [가-힣ㄱ-ㅎ()/?]+)*", piece)
    return [f.strip() for f in out]


def check_rows(L, rows):
    misses = []
    for key, (typ, pattern, teaches) in rows.items():
        if typ not in ("语法", "总结") or key not in L:
            continue
        text_ns = re.sub(r"[\s+]", "", L[key])
        for form in forms_named(pattern, teaches):
            for combo in expand(form.lstrip("-")):
                if not any(occurs(text_ns, alt) for alt in combo):
                    misses.append((key, form, combo[0].strip()))
    return misses


# ---------------------------------------------------------------- 2. 子形态核对

def check_sub(L, rows):
    fails, unverified = [], []
    tables = sub_tables()
    taught = tables.get("课内讲到的形态", [])
    absent = tables.get("L1–L10 没有课的形态", [])
    for cells in taught + absent:
        for k in keys_in(" ".join(cells[1:])):
            if k not in rows:
                fails.append(f"子形态核对 「{cells[0]}」 cites L{k}, which is not a lesson")
    for cells in taught:
        form = cells[0]
        if form not in TAUGHT:
            unverified.append(form)
            continue
        if keys_in(cells[1])[:1] != list(TAUGHT[form])[:1]:
            fails.append(f"「{form}」: the table's first lesson {cells[1]} differs from the evidence's L{list(TAUGHT[form])[0]}")
        for k, rxs in TAUGHT[form].items():
            for rx in rxs:
                if k not in L or not has(L[k], rx):
                    fails.append(f"「{form}」: L{k}'s notes lack /{rx}/")
    for cells in absent:
        form = cells[0]
        if form not in ABSENT:
            unverified.append(form)
            continue
        rx, allowed = ABSENT[form]
        if rx:
            hits = {k for k, t in L.items() if re.search(rx, re.sub(r"\s+", "", t))} - allowed
            if hits:
                fails.append(f"「{form}」 occurs in the notes of {', '.join('L' + k for k in sorted(hits))}")
    in_table = {c[0] for c in taught + absent}
    for form in list(TAUGHT) + list(ABSENT):
        if form not in in_table:
            fails.append(f"evidence for 「{form}」, which is no longer in the table")
    for k, rx, claim in NOT_TAUGHT:
        if re.search(rx, re.sub(r"\s+", "", L[k])):
            fails.append(f"claim broken: {claim}")
    return fails, unverified


def main(argv):
    L = load_lessons(lessons_arg(argv))
    rows = lesson_rows()
    misses = check_rows(L, rows)
    fails, unverified = check_sub(L, rows)
    print(f"1. lesson rows: {len(misses)} form(s) not found literally — review each with lesson.py grep")
    for key, form, alt in misses:
        print(f"   L{key:6s} {form}  (looked for {alt})")
    print(f"2. 子形态核对: {len(fails)} failure(s), {len(unverified)} row(s) without evidence")
    for f in fails:
        print("   FAIL", f)
    for u in unverified:
        print("   NO EVIDENCE", u)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
