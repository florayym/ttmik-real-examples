# Topic pages (`topics/`)

A topic page follows one grammar family across levels (引用句法 runs from L5 to L10) and links out to
the note files. It never repeats example sentences — those live only in the note files. A page holds
links, one-line summaries and planning notes, and is rewritten in place as a whole (it doesn't
accumulate `## [Source]` sections).

- `topics/README.md` is the hub: the list of pages, the shared 读表说明 (reading legend), lessons that
  sit on two or more pages, and notes on lesson numbers. The root README's 📚 专题导航 line is built
  from the pages' H1 titles by `notes.py index`; topic pages are not counted in any level index.
- Two kinds:
  - **形态型** — starts from a form and shows how it is composed or contracted; may be laid out as a
    matrix (引用句法).
  - **意义型** — starts from a meaning: a family table in lesson order, 中文对照, then 辨析 / 形态拆解
    taken from the lecture notes.
- Every lesson cited on a page must teach the form written next to it, checked against the lecture
  notes (`tools/ttmik/check_topics.py`). The 原文回指 column lists only back-references the lecture
  notes state explicitly — "In Level X Lesson Y…", "the previous lesson" (`tools/ttmik/backrefs.py`).
- Labels are words, not symbols, so they read without a legend and can be searched:
  - **有例句** — links to the note file holding a real example of that exact form;
  - **待采集** — TTMIK teaches it, the repo has no example yet;
  - **附带出现** — an example of the form sits in another note file: link the file and quote the
    fragment 「…」 from its 原句;
  - **—** — TTMIK has no such lesson or combination; the cell holds no form.
- A form TTMIK never teaches appears only in a page's 「课程外」 table, and only once the repo holds a
  real example of it.

## After filing or moving examples

`notes.py topics <lessons>` lists every labelled cell for those lessons. Make each label true again:

- 待采集 / 附带出现 → 有例句 when the lesson's note file now has an example of that cell's exact form;
- when examples move, repoint 有例句 links and 附带出现 fragments to the file that now holds them.

`notes.py check` fails on an 有例句 link to another lesson's file and on a quoted fragment that is no
longer in any 原句 of the file it links to.
