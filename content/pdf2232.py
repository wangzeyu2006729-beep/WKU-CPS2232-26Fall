"""Print CPS2232 exam papers and the chapter bank as 2390-style Question / Answer PDFs."""
import html
import re
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from content import LECTURES, SOURCES, EXAMS
from dataset import QS, PAPERS, TYPE_ZH

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out" / "pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
x = html.escape
SEC_EN = {"tf": "True or False", "mc": "Multiple Choice", "fill": "Fill in the gap / Short answer", "essay": "Essay"}

CSS = """
@page { size: A4; margin: 18mm 20mm 18mm 20mm;
  @bottom-right { content: counter(page); font: 8.5pt Arial, sans-serif; color: #777; } }
body { font-family: Calibri, Carlito, "Helvetica Neue", Arial, "PingFang SC", sans-serif; font-size: 10.5pt; line-height: 1.45; color: #111; margin: 0; }
.cover { height: 252mm; position: relative; break-after: page; }
.cover .bar { border-left: 4px solid #1f3a5f; padding-left: 14px; margin-top: 6mm; }
.eyebrow { font-size: 9pt; letter-spacing: .04em; color: #333; text-transform: uppercase; }
.cover h1 { font-family: Arial, "PingFang SC", sans-serif; font-weight: 400; font-size: 25pt; margin: 4px 0 6px; color: #1f3a5f; }
.cover .sub { color: #444; font-size: 9.5pt; }
.meta { margin-top: 11mm; font-size: 9.5pt; color: #1f3a5f; }
.meta div { margin: 2px 0; } .meta span { color: #666; }
.cover h2 { font-size: 10.5pt; font-weight: 400; letter-spacing: .04em; color: #1f3a5f; margin: 11mm 0 4mm; text-transform: uppercase; }
.toc a { display: flex; justify-content: space-between; color: #333; text-decoration: none; font-size: 9.5pt; padding: 3px 0; }
.toc a .n { color: #555; }
.notes { margin-top: 10mm; font-size: 8.6pt; color: #444; }
.notes p { margin: 3px 0; }
.foot { position: absolute; bottom: 0; font-size: 8pt; color: #666; }
.part { break-before: page; }
.part > h1 { text-align: center; font-size: 13pt; margin: 0 0 2px; }
.part > .ptsub { text-align: center; font-style: italic; font-size: 9.5pt; color: #333; margin-bottom: 6mm; }
h3.sec { font-size: 11pt; margin: 7mm 0 2mm; break-after: avoid; }
.q { margin: 0 0 5mm; break-inside: avoid; }
.q.long { break-inside: auto; }
.qn { font-weight: 700; }
.lab { font-size: 7.5pt; color: #777; margin-left: 6px; font-weight: 400; }
.stem { white-space: pre-wrap; }
.tfline { margin: 2px 0 0 26px; }
ol.opts { list-style: none; margin: 3px 0 0 26px; padding: 0; }
ol.opts li { margin: 1px 0; }
.blank { display: inline-block; min-width: 26mm; border-bottom: 1px solid #333; height: 1em; vertical-align: baseline; }
.ans, .fillans { color: #1d3fbf; font-weight: 700; }
.fillans { text-decoration: underline; }
ol.opts li.right { color: #1d3fbf; font-weight: 700; }
.why { color: #444; font-size: 9pt; margin: 2px 0 0 26px; }
.why b { color: #1d3fbf; }
.fig { display: block; margin: 3px 0 3px 26px; max-width: 150mm; max-height: 62mm; }
.fig.wide { max-height: 80mm; }
.lines { margin: 4px 0 0 26px; }
.lines div { border-bottom: 1px solid #bbb; height: 7.5mm; }
.essay { margin: 4px 0 0 26px; color: #1d3fbf; }
.essay p { margin: 3px 0; }
.essay .muted, .muted { color: #555; font-size: 9pt; }
pre, .code { font-family: Menlo, Consolas, "Courier New", monospace; font-size: 8.4pt; line-height: 1.35; white-space: pre-wrap; margin: 4px 0; }
.stem pre { color: #111; }
.essay pre { color: #1d3fbf; border-left: 2px solid #c7d2f5; padding-left: 8px; }
.ans-table { border-collapse: collapse; margin: 4px 0; font-size: 8.8pt; }
.ans-table th, .ans-table td { border: 1px solid #9aa6c7; padding: 2px 6px; text-align: left; vertical-align: top; }
.ans-table th { background: #eef1fa; color: #1f3a5f; }
.tree-row { display: flex; flex-wrap: wrap; gap: 6px 14px; align-items: flex-end; margin: 4px 0; break-inside: avoid; }
.tree-box { margin: 0; }
.essay ol { margin: 3px 0; padding-left: 20px; }
.src { font-size: 7.5pt; color: #777; }
.empty { color: #777; font-style: italic; }
"""


def blanks(text, answers=None):
    def rep(m):
        i = int(m.group(1)) - 1
        if answers is None:
            return '<span class="blank"></span>'
        return f'<span class="fillans">{x(answers[i])}</span>'
    return re.sub(r"____\[(\d+)\]", rep, x(text).replace("____[", "____["))


def stem_html(q, answers=None, exam=False):
    t = q.get("etext") if exam and q.get("etext") else q["text"]
    if q["type"] == "fill":
        body = blanks(t, q["answers"] if answers else None)
    else:
        body = x(t)
    figs = "".join(f'<img class="fig{" wide" if f in ("rb_q21.png", "heap_abcd.png") else ""}" src="../../img/{f}">' for f in q["fig"])
    return f'<span class="stem">{body}</span>{figs}'


def src_line(q):
    s = " · ".join(SOURCES[k].split(" · ")[0] for k in q["src"])
    ex = "；".join(f'{EXAMS[e]["short"]} 第 {n} 题' for e, n in q["exam"].items())
    return f'<div class="src">出处：{s}{"；" + ex if ex else ""}</div>'


def q_block(num, q, answers, label=True, src=False, exam=False):
    lab = f'<span class="lab">{q["label"]}</span>' if label else ""
    long = " long" if q["type"] == "essay" and answers else ""
    out = [f'<div class="q{long}"><span class="qn">{x(num)}.</span>{lab} {stem_html(q, answers, exam)}']
    if q["type"] == "tf":
        if answers:
            out.append(f'<div class="tfline">True or False.　<span class="ans">Answer: {"True" if q["answer"] == "A" else "False"}</span></div>')
        else:
            out.append('<div class="tfline">True or False.</div>')
    elif q["type"] == "mc":
        items = []
        for i, o in enumerate(q["options"]):
            right = answers and "ABCDEF"[i] in q["answer"]
            items.append(f'<li class="{"right" if right else ""}">{"abcdef"[i]}) {x(o)}</li>')
        out.append(f'<ol class="opts">{"".join(items)}</ol>')
        if answers:
            out.append(f'<div class="why"><b>Answer: {q["answer"].lower()}</b></div>')
    elif q["type"] == "essay":
        if answers:
            out.append(f'<div class="essay">{q["html"]}</div>')
        else:
            out.append('<div class="lines">' + "<div></div>" * 4 + "</div>")
    if answers and q["ex"]:
        out.append(f'<div class="why">解析：{x(q["ex"])}</div>')
    if answers and q["note"]:
        out.append(f'<div class="why">注：{x(q["note"])}</div>')
    if src:
        out.append(src_line(q))
    out.append("</div>")
    return "".join(out)


def cover(eyebrow, title, sub, toc, notes):
    toc_html = "".join(f'<a href="#{a}"><span>{x(t)}</span><span class="n">⟦{a}⟧</span></a>' for a, t in toc)
    return f"""<section class="cover"><div class="bar"><div class="eyebrow">{x(eyebrow)}</div><h1>{x(title)}</h1><div class="sub">{x(sub)}</div></div>
<div class="meta"><div>Wenzhou-Kean University · CPS 2232 Data Structures and Algorithms</div><div><span>Instructor:</span> Ehimwenma, K. · <span>Term:</span> Fall 2026</div></div>
<h2>Contents</h2><nav class="toc">{toc_html}</nav><div class="notes">{notes}</div>
<div class="foot">题号保留原卷 / 题库编号。PDF 目录可点击，左侧书签可跳转。</div></section>"""


def paper_doc(answers):
    toc, parts = [], []
    for e, items in PAPERS.items():
        meta = EXAMS[e]
        toc.append((e, f"{meta['title']}（{meta['short']}）— {len(items)} 题" + (" · 含答案与解析" if answers else "")))
        secs, starts = [], dict(meta["parts"])
        for no, q in items:
            first = int(re.split(r"[–,\s]", no)[0])
            if first in starts:
                secs.append(f'<h3 class="sec">{x(starts.pop(first))}</h3>')
            secs.append(q_block(no, q, answers, label=False, exam=True))
        parts.append(f'<section class="part" id="{e}"><h1>CPS 2232 – {x(meta["title"])}</h1><div class="ptsub">{x(meta["note"])}</div>{"".join(secs)}</section>')
    notes = ("<p>两套真题按原卷顺序与题号整理（照片识别）。2025 秋第 13、20 题原卷重复，均保留。24 春期中第 36–38 题、25 秋第 31–33 题为同一组小题。</p>"
             + ("<p>蓝色粗体为答案；“解析”为独立整理的讲解，依据老师讲义（Lecture 1–14）与试卷批改。计算题均经程序复核。</p>" if answers else "<p>答案见配套的《真题 · 答案》PDF。</p>"))
    title = "真题 · 答案 Past Exams – Answers" if answers else "真题 · 题目 Past Exams – Questions"
    return cover("CPS2232 / PAST EXAMS", title, "2023/24 Spring Mid-Term · 2025 Fall Exam", toc, notes) + "".join(parts)


def bank_doc(answers):
    toc, parts = [], []
    for ci, (zh, en) in enumerate(LECTURES, 1):
        qs = [q for q in QS if q["ch"] == ci]
        anchor = f"L{ci}"
        toc.append((anchor, f"Lecture {ci} · {en} · {zh.split(' ', 1)[1]} — {len(qs)} 题"))
        body, cur = [], None
        if not qs:
            body.append('<p class="empty">本讲在现有题库与真题中没有对应题目。</p>')
        for q in qs:
            if q["type"] != cur:
                cur = q["type"]
                body.append(f'<h3 class="sec">{SEC_EN[cur]}（{TYPE_ZH[cur]}）</h3>')
            body.append(q_block(q["label"].split("-")[1], q, answers, label=False, src=True))
        parts.append(f'<section class="part" id="{anchor}"><h1>Lecture {ci} – {x(en)}</h1><div class="ptsub">{x(zh)} · 题号前缀 L{ci}-</div>{"".join(body)}</section>')
    notes = ("<p>题库A（Stud_Bank.pdf，16 页）与题库B（2025.12.8 DSA Bank，24 页）合并去重，并按老师讲义 Lecture 1–14 分章；同一题的不同数字版本（如 67&gt;&gt;4 与 67&gt;&gt;3）分别保留。每题下方注明出处，出现在真题中的题标出原卷题号。</p>"
             + ("<p>蓝色粗体为答案。题库A 学长批注有 5 处与讲义不符（堆的 relational property、无界通配符、哈希函数两部分、BST 查找代码、Lambda 调用），已按讲义更正并在解析中说明。</p>" if answers else "<p>答案见配套的《题库 · 答案》PDF。</p>"))
    title = "题库 · 答案 Question Bank – Answers" if answers else "题库 · 题目 Question Bank – Questions"
    return cover("CPS2232 / QUESTION BANK BY LECTURE", title, f"{len(QS)} questions · grouped by Lecture 1–14", toc, notes) + "".join(parts)


def render(name, body):
    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / f"{name}.html"
    pdf = OUT / f"{name}.pdf"

    def write(b):
        src.write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{x(name)}</title><style>{CSS}</style></head><body>{b}</body></html>', encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--generate-pdf-document-outline",
                        f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True)

    # pass 1: hidden page markers in each part heading
    marked = re.sub(r'<section class="part" id="([^"]+)"><h1>', lambda m: f'<section class="part" id="{m.group(1)}"><h1><span style="font-size:1px;color:#fff">@@{m.group(1)}@@</span>', body)
    write(marked)
    pages = {}
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
    for p in range(1, n + 1):
        t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), str(pdf), "-"], capture_output=True, text=True).stdout
        for a in re.findall(r"@@([A-Za-z0-9]+)@@", t):
            pages.setdefault(a, p)
    final = re.sub(r"⟦([^⟧]+)⟧", lambda m: str(pages.get(m.group(1), "")), body)
    write(final)
    src.unlink()
    return pdf, n


if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    jobs = {
        "CPS2232_真题_题目": lambda: paper_doc(False),
        "CPS2232_真题_答案": lambda: paper_doc(True),
        "CPS2232_题库_题目": lambda: bank_doc(False),
        "CPS2232_题库_答案": lambda: bank_doc(True),
    }
    for name, fn in jobs.items():
        if "all" in which or name in which:
            pdf, n = render(name, fn())
            print(pdf.name, n, "pages")
