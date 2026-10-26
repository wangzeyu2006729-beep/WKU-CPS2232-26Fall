# WKU-CPS2232-26Fall

**Wenzhou-Kean University · CPS2232 · Ehimwenma, K. · Fall 2026 (26Fall)**

[Practice online](https://wangzeyu2006729-beep.github.io/WKU-CPS2232-26Fall/) · Other courses: [MATH3700](https://wangzeyu2006729-beep.github.io/WKU-MATH3700-26Fall/) · [CPS2390](https://wangzeyu2006729-beep.github.io/WKU-CPS2390-26Fall/)

193 de-duplicated questions from two question banks and two past exam papers, grouped by Lecture 1–14: 46 true/false, 44 multiple choice, 63 fill-in-the-blank and 40 essay questions, each with an answer, a Chinese explanation and its source. This is one of the repository owner's Fall 2026 courses at WKU. All three course sites use a compact dark interface and independent browser progress.

## Course information

| Field | Details |
|---|---|
| University | Wenzhou-Kean University (WKU) |
| Course | CPS2232 Data Structures and Algorithms |
| Instructor | Ehimwenma, K. |
| Semester | Fall 2026 (26Fall) |

Use the course selector at the top to switch between MATH3700, CPS2390 and CPS2232. Questions are in English; controls and study notes are in Chinese. This is an independent revision aid, not an official university site or a statement of instructor endorsement.

## Practising past papers or the bank

The **试卷** menu selects one source:

| Source | Questions | Order |
|---|---:|---|
| 全部来源 | 193 | Lecture order |
| 题库（A+B） | 174 | Lecture order |
| 2023/24 Spring Mid-Term | 37 (original Q1–39) | Original paper numbering |
| 2025 Fall Exam | 30 (original Q1–34) | Original paper numbering |

It combines with the question-type tabs, the lecture menu, random practice, incorrect-answer review and bookmarks. When a past paper is selected, each question also shows its original number, for example `24春期中 第 18 题`. Grouped sub-questions (24 春 Q36–38, 25 秋 Q31–33) are one essay; 25 秋 Q13 and Q20 are the same question on the paper and appear once.

## Coverage by lecture

| Lecture | Topic | TF | MC | Fill | Essay | Total |
|---|---|---:|---:|---:|---:|---:|
| 1 | Recursion | 1 | | | | 1 |
| 2 | Objects, classes & references | 3 | | 8 | 1 | 12 |
| 3 | Generics | 3 | 3 | 3 | 1 | 10 |
| 4 | ADTs, interfaces, lambda & lists | 10 | | 3 | 1 | 14 |
| 5 | Stacks & queues | | 2 | 7 | | 9 |
| 6 | Sets, maps & hash tables | 18 | 12 | 11 | | 41 |
| 7 | List implementation | | 1 | 2 | 1 | 4 |
| 8 | Heaps & priority queues | 3 | 6 | 7 | 1 | 17 |
| 9 | Hashing | | 8 | 5 | 7 | 20 |
| 10 | Analysis of algorithms | 4 | | 9 | 4 | 17 |
| 11 | Sorting | | | 1 | 9 | 10 |
| 12 | Dynamic programming | | | | | 0 |
| 13 | BST & AVL trees | 2 | 3 | 6 | 9 | 20 |
| 14 | Red-black trees | 2 | 9 | 1 | 6 | 18 |
| **Total** | | **46** | **44** | **63** | **40** | **193** |

Lecture 12 has no matching question in the supplied banks or papers.

## Practice controls

- The **期中 · L1–6 / 期末 · L7–14** switch at the top limits everything to one exam scope: 87 midterm questions (Lecture 1–6, the default) or 106 final questions (Lecture 7–14). Counts, progress and the incorrect-answer list follow the selected scope; answers in the other scope are kept. Four 24春期中 questions from Lecture 7 and 9 appear under 期末.
- Labels show lecture, type and number: `L13-TF01`, `L13-MC01`, `L13-FB01`, `L13-ES01`. Search a complete label or keyword; Chinese keywords also work.
- True/false and multiple choice are graded automatically, with the reasoning and a note on every option.
- Fill and essay questions accept an optional draft. **查看答案与讲解** reveals the reference answer — essays include tree diagrams, code and step tables — then **答对了** or **需巩固** records a self-assessment. Revealing alone does not count as completion.
- Keyboard: `1`–`6` or `A`–`F` select; `Enter` confirms; arrow keys navigate; `S` bookmarks.

## Sources and answer basis

| Tag | Source |
|---|---|
| 题库A | `Stud_Bank.pdf`, 16 pages, with a senior student's highlighted answers |
| 题库B | `2025.12.8 stud bank DSA Bank.pdf`, 24 pages, no answers; extends 题库A |
| 24春期中 | 2023/24 Spring Mid-Term Exam, 7 photos with the instructor's marking |
| 25秋考试 | 2025 Fall exam, 4 photos, no answers |
| 课堂 | Classroom photos and revision hints |

Questions were transcribed from the page images. Variants that differ only in numbers (for example HashSet capacity 28 / 24 / 10, or `67 >> 4` / `67 >> 3`) are separate questions; exact duplicates appear once with every source listed.

Answers follow the lecture slides and the marked exam; every calculation (hash codes, folding, probing, quick-sort partitions, AVL and red-black trees) was re-computed by program. Five of 题库A's annotated answers disagree with the slides and are corrected with an explanation: heap relational property, unbounded wildcard, the two parts of a hash function, the BST search code and the lambda call. Course conventions used: BST deletion replaces a node with the rightmost node of its left subtree; AVL heights count nodes (leaf = 1) with balance factor = h(right) − h(left); red-black insertion cases follow Lecture 14 (Case 1 red uncle; 2a LR, 2b RL; 3a LL, 3b RR).

## Progress and privacy

Records stay in the current browser's localStorage under `cps2232-practice-v1`. There is no backend, account, tracking, or answer upload. Each other course uses its own key; switching courses or clearing one course does not clear the others. Different devices, browsers and profiles have independent records. Clearing browser data removes progress.

## Build and offline use

`index.html` embeds the full interface, questions and figures. Download it and open it to practise offline.

```bash
python3 build.py                  # index.html, questions.json, translations.json
python3 content/pdf2232.py        # optional: question and answer PDFs in content/out/pdf (needs Google Chrome)
```

`content/content.py` holds every question; `content/answers.py` builds essay answers; `content/trees.py` draws the BST, AVL and red-black tree diagrams. `template.html` is the interface; the shared components (`practice_ui.py`, `practice-ui.css`, `practice-ui.js`, `course-catalog.json`, `verify-ui.js`, `verify-course-flow.js`) are kept identical across the three course repositories. See [adding courses](docs/adding-courses.md).

## License and attribution

Application code is provided under the [MIT License](LICENSE). Original course questions retain their respective authors' rights; the code license does not relicense those materials. See [CONTENT_NOTICE.md](CONTENT_NOTICE.md).
