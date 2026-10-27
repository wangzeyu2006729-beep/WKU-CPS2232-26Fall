"""Build the CPS2232 practice site (index.html, questions.json, translations.json) from content/."""
from collections import Counter
from pathlib import Path
import base64
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / "content")]
from content import LECTURES, SOURCES, EXAMS, MID_LAST_LECTURE, MID_EXTRA_KEYS  # noqa: E402
from dataset import QS, PAPERS, TYPE_ZH  # noqa: E402
from practice_ui import prepare_ui, source_hash  # noqa: E402

REVISION = "2026-10-22.1"
STORAGE_KEY = "cps2232-practice-v1"


def data_uri(name):
    raw = (ROOT / "content" / "img" / name).read_bytes()
    return "data:image/png;base64," + base64.b64encode(raw).decode()


def option_notes(q):
    if q["type"] == "tf":
        return [("应选。" if "AB"[i] == q["answer"] else "不选。") + q["ex"] for i in range(2)]
    return [("应选。" if "ABCDEF"[i] == q["answer"] and not n.startswith("应选") else "") + n for i, n in enumerate(q["oe"])]


def build():
    questions, translations = [], {}
    assert MID_EXTRA_KEYS <= {q["key"] for q in QS}, MID_EXTRA_KEYS - {q["key"] for q in QS}
    for q in QS:
        item = dict(id=q["id"], label=q["label"], key=q["key"], chapter=q["ch"] - 1, bank=q["type"], type=q["type"],
                    text=q["text"], options=q["options"], answer=q.get("answer"), answers=q.get("answers", []),
                    explanation=q["ex"], note=q["note"], references=f"Lecture {q['ch']} · {LECTURES[q['ch'] - 1][1]}",
                    review_revision=REVISION, sources=[SOURCES[s] for s in q["src"]],
                    exam={e: n for e, n in q["exam"].items()}, src=q["src"], figs=[data_uri(f) for f in q["fig"]],
                    part="mid" if q["ch"] <= MID_LAST_LECTURE or q["key"] in MID_EXTRA_KEYS else "final")
        if q["type"] in ("tf", "mc"):
            item["option_explanations"] = option_notes(q)
        if q["type"] == "essay":
            item["html"] = q["html"]
        questions.append(item)
        translations[q["label"]] = dict(text=q["zh"], options=q["zo"], source_sha256=source_hash(item))
    (ROOT / "translations.json").write_text(json.dumps(dict(questions=translations), ensure_ascii=False, indent=1) + "\n")
    papers = {e: dict(title=m["title"], short=m["short"], note=m["note"],
                      order=list(dict.fromkeys(q["id"] for _, q in PAPERS[e])), numbers={str(q["id"]): q["exam"][e] for _, q in PAPERS[e]})
              for e, m in EXAMS.items()}
    data = dict(course=dict(code="CPS2232", school="Wenzhou-Kean University", instructor="Ehimwenma, K.", term="26Fall",
                            storage_key=STORAGE_KEY, review_revision=REVISION, answer_basis="lecture"),
                chapters=[dict(name=zh, english=en) for zh, en in LECTURES], papers=papers, questions=questions)
    ui = prepare_ui(ROOT, data)
    (ROOT / "questions.json").write_text(json.dumps({**data, "questions": [{k: v for k, v in q.items() if k != "figs"} for q in questions]},
                                                    ensure_ascii=False, indent=1) + "\n")
    template = (ROOT / "template.html").read_text()
    for marker, value in ui.items():
        template = template.replace(marker, value)
    (ROOT / "index.html").write_text(template.replace("__QUIZ_DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
    print(json.dumps(dict(questions=len(questions), types=dict(Counter(q["type"] for q in questions)),
                          papers={e: len(p["order"]) for e, p in papers.items()}), ensure_ascii=False))


if __name__ == "__main__":
    build()
