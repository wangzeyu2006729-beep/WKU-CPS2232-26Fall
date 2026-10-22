"""Assemble ordered, labelled CPS2232 questions from content.py + answers.py."""
import re
from content import Q, LECTURES, SOURCES, EXAMS
from answers import A

TYPE_ORDER = {"tf": 0, "mc": 1, "fill": 2, "essay": 3}
CODE = {"tf": "TF", "mc": "MC", "fill": "FB", "essay": "ES"}
TYPE_ZH = {"tf": "判断题", "mc": "选择题", "fill": "填空题", "essay": "解答题"}


def exam_key(no):
    return int(re.split(r"[–,\s]", no)[0])


def load():
    missing = [q["key"] for q in Q if q["type"] == "essay" and q["key"] not in A]
    assert not missing, missing
    extra = set(A) - {q["key"] for q in Q}
    assert not extra, extra
    qs = sorted(Q, key=lambda q: (q["ch"], TYPE_ORDER[q["type"]]))  # stable: keeps authoring order within a group
    counts = {}
    for i, q in enumerate(qs, 1):
        n = counts[(q["ch"], q["type"])] = counts.get((q["ch"], q["type"]), 0) + 1
        q["id"] = i
        q["label"] = f"L{q['ch']}-{CODE[q['type']]}{n:02d}"
        if q["type"] == "essay":
            q["html"] = A[q["key"]]
    papers = {}
    for e in EXAMS:
        items = [(no, q) for q in qs if e in q["exam"] for no in q["exam"][e].split(", ")]
        papers[e] = sorted(items, key=lambda t: exam_key(t[0]))
    return qs, papers


QS, PAPERS = load()
