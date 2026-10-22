"""Reference-answer HTML for every essay question (shared by the website and the PDFs)."""
import html
from trees import T, svg, avl_insert, clone, RB

x = html.escape


def code(s):
    return f'<pre class="code">{x(s.strip(chr(10)))}</pre>'


def row(*items):
    return '<div class="tree-row">' + "".join(f'<figure class="tree-box">{s}</figure>' for s in items) + "</div>"


def table(head, rows, cls=""):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="ans-table {cls}"><tr>{h}</tr>{b}</table>'


A = {}

A["lambda-mult"] = code("""
public class Test {
    public static void main(String[] args) {
        NumberMultiply nm = (a, b) -> a * b;   // lambda 实现唯一的抽象方法 mult
        System.out.println(nm.mult(2, 3));     // 输出 6.0
    }
}""") + "<p>Lambda 的参数 (a, b) 对应 mult 的两个 double 参数，箭头右边是方法体。注意调用的方法名就是 mult（题库A 学长批注写成 nm.Doublemult(2,3) 是错的）。</p>"

A["ll-add80"] = code("""
// 方法一：java.util.LinkedList
LinkedList<Integer> list = new LinkedList<>(Arrays.asList(4, 1, 3, 7));
list.addFirst(80);                 // 80 -> 4 -> 1 -> 3 -> 7

// 方法二：自己实现的单链表
public void addFirst(E e) {
    Node<E> newNode = new Node<>(e);
    newNode.next = head;           // 新节点指向原来的头节点
    head = newNode;                // head 指向新节点
    size++;
    if (tail == null) tail = head; // 原来是空表时，tail 也指向它
}""") + "<p>只改指针，时间复杂度 O(1)。</p>"

A["q-vs-pq"] = "<p><b>Queue</b>：FIFO，先进先出，元素按到达顺序出队。<br><b>Priority queue</b>：每个元素带优先级（key），出队的是优先级最高（或 key 最小/最大）的元素，与插入顺序无关，通常用堆实现，插入和删除都是 O(log n)。</p>"

bucket20 = table(["index", "bucket（chaining）"], [["0", ""], ["1", "(1, 4)"], ["2", "(42, 7) → (2, 21)"], ["3", ""], ["4", "(4, 14)"], ["5 … 18", ""], ["19", "(39, 3)"]], "bucket")
A["hash-n20"] = "<p><b>(a)</b></p>" + code("""
public static int hashCode(int key) {
    return key % 20;          // N = 20
}""") + "<p><b>(b)</b> 1 % 20 = 1；42 % 20 = 2；39 % 20 = 19；4 % 20 = 4；2 % 20 = 2（与 42 冲突）</p><p><b>(c)</b> 冲突的条目在同一个 bucket 中用链表串起来：</p>" + bucket20 + \
    "<p>课堂例题（会考照片）：N = 20，(1,20)(2,70)(42,80)(4,25)(12,44)(14,32)(17,11)(13,78)(37,98) → 下标 1, 2, 2, 4, 12, 14, 17, 13, 17。</p>"

bucket21 = table(["index", "bucket"], [["0", "(42, 7)"], ["1", "(1, 89)"], ["2", "(2, 21)"], ["3", ""], ["4", "(4, 10) → (4, 14)"], ["5 … 9", ""], ["10", "(31, 45)"], ["11 … 17", ""], ["18", "(39, 3)"], ["19, 20", ""]], "bucket")
A["hash-n21"] = "<p><b>(31)</b></p>" + code("""
public static int hashCode(int key, int N) {
    return key % N;           // N = 21
}""") + "<p><b>(32)</b> 4 % 21 = 4；42 % 21 = 0；1 % 21 = 1；39 % 21 = 18；4 % 21 = 4；2 % 21 = 2；31 % 21 = 10</p><p><b>(33)</b></p>" + bucket21 + \
    "<p>key 4 出现两次：按 bucket array 画法两条都挂在 4 号桶；若当作 Map 存储，(4, 14) 会覆盖 (4, 10)，可在答卷中注明。</p>"


def hc(s, extra=""):
    n = len(s)
    chars = "，".join(f"{'空格' if c == ' ' else c}={ord(c)}" for c in s)
    terms = " + ".join(f"{ord(c)}×31<sup>{n - 1 - i}</sup>" for i, c in enumerate(s))
    vals = [ord(c) * 31 ** (n - 1 - i) for i, c in enumerate(s)]
    tot = sum(vals)
    j = tot & 0xFFFFFFFF
    j = j - 2**32 if j >= 2**31 else j
    r = f"<p><b>s = “{x(s)}”</b>，n = {n}，最高次幂 n−1 = {n - 1}；{chars}<br>= {terms}<br>= {' + '.join(f'{v:,}' for v in vals)}<br>= <b>{tot:,}</b>"
    if j != tot:
        r += f"<br><span class='muted'>（Java 中 int 会溢出，\"{x(s)}\".hashCode() 实际返回 {j}；考试写数学结果即可。）</span>"
    return r + extra + "</p>"


A["hc-hello"] = hc("hello", "<br>2024 春期中按此作答得满分。")
A["hc-tops"] = hc("tops")
A["hc-three"] = hc("hello world") + hc("stop", "<br>与课堂幻灯片 “stop” 例题一致。") + hc("algorithm") + "<p class='muted'>题库B 题干把 algorithm 印成了 algorith。</p>"

A["lin-probe"] = "<p>h(k) = k % 11，冲突时依次看 (k + j) % 11，j = 1, 2, …</p><p>34→1，29→7，53→9，44→0，120→10，39→6，45→1 冲突 → 2，40→7 冲突 → 8</p>" + \
    table(["index"] + [str(i) for i in range(11)], [["key", "44", "34", "45", "", "", "", "39", "29", "40", "53", "120"]])

A["probe-algos"] = "<p>三种都是开放地址法（open addressing），从 k = h(key) = key % N 开始，位置被占就按规则找下一个（j = 0, 1, 2, …）：</p><p><b>(a) Linear probing</b>：index = (k + j) % N，逐格往后找；缺点是一次聚集（primary clustering）。<br><b>(b) Quadratic probing</b>：index = (k + j²) % N，依次看 k, k+1, k+4, k+9, …；避免一次聚集，但有二次聚集（secondary clustering）。<br><b>(c) Double hashing</b>：index = (h(key) + j·h'(key)) % N，h'(key) = PRIME − key % PRIME（PRIME 是小于 N 的素数，如 7）。</p>" + code("""
int insert(int key) {
    int k = key % N;
    for (int j = 0; j < N; j++) {
        int index = (k + j) % N;          // (b) 改为 (k + j*j) % N；(c) 改为 (k + j*h2(key)) % N
        if (table[index] == null) {
            table[index] = key;
            return index;
        }
    }
    return -1;                            // 表满：rehash（容量翻倍后重新插入）
}""") + "<p>开放地址法一般保持负载因子 λ &lt; 0.5，超过就 rehashing。</p>"

A["sum-java"] = "<p>公式：1 + 2 + … + n = n(n+1)/2 = (first + last)(last − first + 1)/2；前 5000 个数之和 = 5000 × 5001 / 2 = 12,502,500。</p>" + code("""
public static int addNumbers() {
    int first = 1;
    int last = 5000;
    int sum = (first + last) * (last - first + 1) / 2;   // 12,502,500
    return sum;
}""") + "<p class='muted'>题库A 学长批注漏了 int sum 声明和乘号 *，上面已补全。也可以用 for 循环累加，但公式法是 O(1)。</p>"

A["tc-linear"] = "<p>i = 0 执行 1 次：O(1)<br>i &lt; n 判断 n + 1 次：O(n)<br>i++ 执行 n 次：O(n)<br>k = k + 7 执行 n 次：O(n)<br>T(n) = O(1) + O(n) + O(n) + O(n) = O(1) + 3·O(n) = <b>O(n)</b>，所以是线性的。</p>"
A["tc-nn"] = "<p>外层循环执行 n 次；外层每执行一次，内层循环执行 n 次；循环体 k = k + 1 共执行 n × n = n² 次。<br>T(n) = c·n² + （循环控制的低阶项）= <b>O(n²)</b>。</p>"
A["tc-n5"] = "<p>外层 n 次，内层固定 5 次，循环体执行 5n 次。<br>T(n) = 5n = <b>O(n)</b>（常数 5 忽略）。</p>"

QS_HEAD = ["子表 / pivot", "low 找第一个 &gt; pivot、high 找第一个 ≤ pivot，交换", "pivot 归位后"]
QS_INTRO = "<p>方法（Liang Listing 23.8，课上用的 partition）：pivot = 子表第一个元素；low 从第二个元素向右找第一个 <b>&gt; pivot</b> 的元素，high 从最后向左找第一个 <b>≤ pivot</b> 的元素；low &lt; high 时交换；两者交错后，把 pivot 与 high 位置的元素交换，pivot 就到了最终位置，再对左右两段递归。</p>"
A["qs-a"] = QS_INTRO + table(QS_HEAD, [["[0 3 −1 5 2]，p=0", "3 ↔ −1", "[−1] <b>0</b> [3 5 2]"], ["[3 5 2]，p=3", "5 ↔ 2", "[2] <b>3</b> [5]"]]) + "<p>结果：<b>−1 0 2 3 5</b></p>"
A["qs-b"] = QS_INTRO + table(QS_HEAD, [["[0 −1 3 5 2]，p=0", "无交换", "[−1] <b>0</b> [3 5 2]"], ["[3 5 2]，p=3", "5 ↔ 2", "[2] <b>3</b> [5]"]]) + "<p>结果：<b>−1 0 2 3 5</b></p>"
A["qs-c"] = QS_INTRO + table(QS_HEAD, [
    ["全表，p=38", "81 ↔ 14，48 ↔ 13", "[13 14 22] <b>38</b> [48 69 93 81 45 58 79 72]"],
    ["[13 14 22]，p=13", "无", "<b>13</b> [14 22]，再 p=14 → <b>14</b> [22]"],
    ["[48 69 93 81 45 58 79 72]，p=48", "69 ↔ 45", "[45] <b>48</b> [93 81 69 58 79 72]"],
    ["[93 81 69 58 79 72]，p=93", "无", "[72 81 69 58 79] <b>93</b>"],
    ["[72 81 69 58 79]，p=72", "81 ↔ 58", "[69 58] <b>72</b> [81 79]"],
    ["[69 58]，p=69；[81 79]，p=81", "无", "58 <b>69</b>；79 <b>81</b>"]]) + "<p>结果：<b>13 14 22 38 45 48 58 69 72 79 81 93</b></p>"
A["qs-d"] = QS_INTRO + table(QS_HEAD, [
    ["全表，p=4", "5 ↔ 3", "[3 3 2 4 1] <b>4</b> [5 9 5 8 9 7]"],
    ["[3 3 2 4 1]，p=3", "4 ↔ 1", "[1 3 2] <b>3</b> [4]"],
    ["[1 3 2]，p=1；[3 2]，p=3", "无", "<b>1</b> [3 2] → [2] <b>3</b>"],
    ["[5 9 5 8 9 7]，p=5", "9 ↔ 5", "[5] <b>5</b> [9 8 9 7]"],
    ["[9 8 9 7]，p=9", "无", "[7 8 9] <b>9</b>"],
    ["[7 8 9]，p=7；[8 9]，p=8", "无", "<b>7</b> [8 9] → <b>8</b> [9]"]]) + "<p>结果：<b>1 2 3 3 4 4 5 5 7 8 9 9</b></p>"
A["qs-e"] = QS_INTRO + table(QS_HEAD, [
    ["全表，p=5", "9 ↔ 1，8 ↔ 0 → 5 2 1 3 0 4 8 9 6 7", "[4 2 1 3 0] <b>5</b> [8 9 6 7]"],
    ["[4 2 1 3 0]，p=4", "无", "[0 2 1 3] <b>4</b>"],
    ["[0 2 1 3]，p=0；[2 1 3]，p=2", "无", "<b>0</b> [2 1 3] → [1] <b>2</b> [3]"],
    ["[8 9 6 7]，p=8", "9 ↔ 7", "[6 7] <b>8</b> [9]"],
    ["[6 7]，p=6", "无", "<b>6</b> [7]"]]) + "<p>结果：<b>0 1 2 3 4 5 6 7 8 9</b>（第一轮的两次交换与课堂板书一致）</p>"

A["alg-merge"] = code("""
MERGE-SORT(A, low, high)                     // 分治，O(n log n)
1  if low < high
2      mid = (low + high) / 2
3      mergeSort(A, low, mid)                // 递归排序左半
4      mergeSort(A, mid + 1, high)           // 递归排序右半
5      merge(A, low, mid, high)              // 合并两个有序段

merge：用两个下标分别扫描左右两段，每次把较小的元素放进临时数组，
       一段用完后把另一段剩余元素整体复制过去，最后拷回 A。""")
A["alg-quick"] = code("""
QUICK-SORT(list, first, last)                // 分治，平均 O(n log n)，最坏 O(n^2)
1  if last > first
2      pivotIndex = partition(list, first, last)
3      quickSort(list, first, pivotIndex - 1)
4      quickSort(list, pivotIndex + 1, last)

partition(list, first, last):
    pivot = list[first]; low = first + 1; high = last
    while high > low:
        while low <= high and list[low] <= pivot: low++
        while low <= high and list[high] > pivot: high--
        if high > low: swap(list[low], list[high])
    while high > first and list[high] >= pivot: high--
    if pivot > list[high]:
        list[first] = list[high]; list[high] = pivot; return high
    else: return first""")
A["alg-select"] = code("""
SELECTION-SORT(list)                         // O(n^2)
    for i = 0 to n - 2:
        minIndex = i
        for j = i + 1 to n - 1:              // 在 list[i..n-1] 中找最小值
            if list[j] < list[minIndex]: minIndex = j
        swap(list[i], list[minIndex])        // 放到第 i 个位置""")
A["alg-insert"] = code("""
INSERTION-SORT(list)                         // O(n^2)
    for i = 1 to n - 1:
        currentElement = list[i]
        k = i - 1
        while k >= 0 and list[k] > currentElement:
            list[k + 1] = list[k]            // 比它大的元素后移
            k--
        list[k + 1] = currentElement         // 插入到正确位置""")

TRAV = {
    "trav-60": ("60 55 45 57 59 100 67 107 101", "45 59 57 55 67 101 107 100 60", "45 55 57 59 60 67 100 101 107", "BST 的中序遍历是升序，可用来自检。"),
    "trav-ak": ("a b d h e i j c f k g", "h d i j e b k f g c a", "h d b i e j a f k c g", "k 是 f 的右孩子。"),
    "trav-green": ("g c b a c e d f k i h j m l n", "a c b d f e c h j i l n m k g", "a b c c d e f g h i j k l m n", "第一个 c 是根的左孩子，第二个 c 是 b 的右孩子。"),
    "trav-7-15": ("7 2 1 3 12 11 16 15", "1 3 2 11 15 16 12 7", "1 2 3 7 11 12 15 16", "15 是 16 的左孩子。"),
    "trav-7": ("7 2 1 3 12 11 16", "1 3 2 11 16 12 7", "1 2 3 7 11 12 16", ""),
}
for k, (pre, post, ino, note) in TRAV.items():
    A[k] = f"<p>i) Pre-order（根 左 右）：<b>{pre}</b><br>ii) Post-order（左 右 根）：<b>{post}</b><br>iii) In-order（左 根 右）：<b>{ino}</b></p>" + (f"<p class='muted'>{note}</p>" if note else "")

A["bst-search"] = code("""
public static Node search(Node root, int key) {
    if (root == null || root.value == key)    // 空树或找到
        return root;
    if (key < root.value)                     // 比当前小 → 去左子树
        return search(root.left, key);
    return search(root.right, key);           // 否则 → 去右子树
}""") + "<p>时间复杂度 O(h)，h 为树高（平衡时 O(log n)，退化成链时 O(n)）。<span class='muted'>题库A 批注的版本返回类型写成 void 却 return root，判空写成 root.value == null，已修正。</span></p>"

A["bst-del20"] = "<p>20 有左孩子 → 找左子树中最右（最大）的节点 <b>19</b>，用 19 替换 20，再删去原来的 19（它没有孩子）。</p>" + \
    row(svg(T((15, (10, 8, 12), (19, (18, 16, None), 30))), 0.9, "删除 20 之后"))

avl_before = T((78, (50, 48, (62, 54, None)), 88))
for n_, m in [(avl_before, "bf=−2"), (avl_before.left, "bf=+1"), (avl_before.left.right, "bf=−1")]:
    n_.mark = m
A["avl78"] = """<p>高度（叶子 = 1）：48、54、88 = 1；62 = 2；50 = 3；78 = 4。<br>
bf = h(right) − h(left)：bf(48) = bf(54) = bf(88) = 0；bf(62) = 0 − 1 = <b>−1</b>；bf(50) = 2 − 1 = <b>+1</b>；bf(78) = 1 − 3 = <b>−2</b> → 78 失衡。<br>
78 的左孩子 50 偏右（新节点在 50 的右子树 62 下）→ <b>LR 型，双旋</b>：① 左旋 50（z = 78，y = 50，x = 62），变成 LL；② 右旋 78。</p>""" + \
    row(svg(avl_before, 0.85, "原树"), svg(T((78, (62, (50, 48, 54), None), 88)), 0.85, "① 左旋 50"), svg(T((62, (50, 48, 54), (78, None, 88))), 0.85, "② 右旋 78，平衡")) + \
    "<p>结果：62 为根，左 50（48, 54），右 78（右孩子 88）；bf(78) = +1，其余为 0。</p>"

log, r, snaps = [], None, []
for k in "a b c d e d f g i j k l".split():
    r = avl_insert(r, k, log)
    snaps.append(clone(r))
A["avl-build"] = "<p>按字母顺序比较。第二个 d 是重复元素，插入时忽略。每次插入后自底向上算 bf = h(right) − h(left)，|bf| = 2 就旋转。元素按递增顺序插入，所以每次失衡都是 <b>RR 型 → 左旋</b>：</p><ol>" + \
    "".join(f"<li>{x(s)}</li>" for s in log) + "</ol>" + \
    row(svg(snaps[4], 0.72, "插入 e 后"), svg(snaps[6], 0.72, "插入 f 后"), svg(snaps[8], 0.72, "插入 i 后"), svg(snaps[10], 0.72, "插入 k 后")) + \
    row(svg(snaps[11], 0.9, "最终 AVL 树")) + "<p>最终：根 d；左 b(a, c)；右 i，i 的左 f(e, g)、右 k(j, l)。</p>"

rb = RB()
log, snaps = [], []
for k in range(1, 8):
    rb.insert(k, log)
    snaps.append(clone(rb.root))
A["rb-build"] = "<p>新节点一律插成红色；根据叔叔 u 的颜色决定 case（按 Lecture 14 编号）：</p><ol>" + "".join(f"<li>{x(s)}</li>" for s in log) + "</ol>" + \
    row(svg(snaps[2], 0.75, "插入 3 后"), svg(snaps[3], 0.75, "插入 4 后"), svg(snaps[4], 0.75, "插入 5 后"), svg(snaps[5], 0.75, "插入 6 后"), svg(snaps[6], 0.8, "最终（插入 7 后）")) + \
    "<p>检查：根到每个 NIL 的路径都经过 2 个黑节点（如 2→1、2→4→3、2→4→6→5），没有相邻红节点。</p>"

A["rb-del-a"] = """<p>① 删除 50：v = 50 是<b>红</b>叶子 → Case 1 简单情形，直接删除，黑高不变。<br>
② 删除 40：v = 40 是黑叶子，顶替它的 u = NIL（黑）→ Black + Black = <b>DB（双黑）</b>（Case 2）。<br>
③ DB 的兄弟 s = 20 是黑色，且两个孩子都是黑（NIL）→ <b>Case 3b</b>：s 变红（B − B = R），双黑上推给父亲 30：30 原为黑 → B + B = DB；30 是根 → <b>Case 3d</b>：根的双黑直接变单黑。</p>""" + \
    row(svg(T((30, (20, None, None, "B"), (40, None, (50, None, None, "R"), "B"), "B")), 0.8, "原树 (a)"), svg(T((30, (20, None, None, "B"), (40, None, None, "B"), "B")), 0.8, "删 50"),
        svg(T((30, (20, None, None, "B"), ("NIL", None, None, "DB"), "B")), 0.8, "删 40 → DB"), svg(T((30, (20, None, None, "R"), None, "B")), 0.8, "结果")) + \
    "<p>检查：根到每个 NIL 的路径都只经过 1 个黑节点（30），没有相邻红节点。</p>"
A["rb-del-b"] = """<p>① 删除 29：红叶子，直接删除。<br>
② 删除 28：黑叶子，NIL 顶替 → <b>DB</b>（在 25 的右孩子位置）。<br>
③ 兄弟 s = 15 是黑色，两个孩子都是黑 → <b>Case 3b</b>：s = 15 变红；父亲 25 是<b>红</b> → red + double black = single black，25 变黑，结束（不再上推）。</p>""" + \
    row(svg(T((30, (25, (15, None, None, "B"), (28, None, (29, None, None, "R"), "B"), "R"), (100, None, None, "B"), "B")), 0.8, "原树 (b)"),
        svg(T((30, (25, (15, None, None, "B"), ("NIL", None, None, "DB"), "R"), (100, None, None, "B"), "B")), 0.8, "删 29、删 28 → DB"),
        svg(T((30, (25, (15, None, None, "R"), None, "B"), (100, None, None, "B"), "B")), 0.8, "结果")) + \
    "<p>检查：根到每个 NIL 的路径都经过 2 个黑节点（30→25、30→100），没有相邻红节点。</p>"

A["left-rotate"] = """<p>LEFT-ROTATE 把 x 的右孩子 y 提上来，x 下沉成为 y 的左孩子；中序顺序 α x β y γ 不变。</p>
<p>第 1 行：y 指向 x 的右孩子。<br>第 2 行：把 y 的左子树 β 挂成 x 的右子树。<br>第 3–4 行：若 β 非空，把 β 的父指针改为 x。<br>
第 5 行：y 的父指针改为 x 原来的父亲（y 接替 x 的位置）。<br>第 6–7 行：若 x 原来是根，则 y 成为新根；<br>第 8–9 行：否则若 x 是父亲的左孩子，父亲的左孩子改为 y；<br>
第 10 行：否则父亲的右孩子改为 y。<br>第 11 行：x 成为 y 的左孩子。<br>第 12 行：x 的父指针指向 y。</p>
<p class="muted">原题把第 5 行缩进到 if 里，实际第 5 行不在 if 里；题库B 还把第 1 行误印成 y.left = x.right。旋转只改指针，O(1)，不破坏 BST 性质。</p>"""
A["right-rotate"] = code("""
RIGHT-ROTATE(T, y)
1  x = y.left               // x 是 y 的左孩子
2  y.left = x.right         // x 的右子树 β 挂到 y 的左边
3  if x.right ≠ T.nil
4      x.right.p = y        // β 的父指针改为 y
5  x.p = y.p                // x 接替 y 的位置
6  if y.p == T.nil
7      T.root = x           // y 原来是根 → x 成为根
8  elseif y == y.p.right
9      y.p.right = x        // y 是右孩子 → 父亲的右孩子改为 x
10 else y.p.left = x        // y 是左孩子 → 父亲的左孩子改为 x
11 x.right = y              // y 成为 x 的右孩子
12 y.p = x                  // y 的父指针指向 x""") + "<p>与 LEFT-ROTATE 完全对称：把 x 和 y、left 和 right 互换。</p>"

q21 = [
    T((34, (15, (3, None, None, "B"), (20, (16, None, None, "R"), (25, None, (27, None, None, "R"), "R"), "B"), "R"), (50, None, None, "B"), "B")),
    T((34, (15, (3, None, None, "B"), (20, (16, None, None, "B"), (25, None, (27, None, None, "R"), "B"), "R"), "R"), (50, None, None, "B"), "B")),
    T((34, (20, (15, (3, None, None, "B"), (16, None, None, "B"), "R"), (25, None, (27, None, None, "R"), "B"), "R"), (50, None, None, "B"), "B")),
    T((20, (15, (3, None, None, "B"), (16, None, None, "B"), "R"), (34, (25, None, (27, None, None, "R"), "B"), (50, None, None, "B"), "R"), "B")),
]
A["rb-q21"] = """<p>刚插入 27（红），父亲 25（红）→ 两个红节点相邻。<br>
<b>第 1 个空框</b>：叔叔 u = 16 是<b>红</b> → <b>Case 1</b>：p = 25、u = 16 涂黑，g = 20 涂红（得到图中第 2 棵树）。<br>
此时 20（红）与父亲 15（红）冲突：x = 20，p = 15，g = 34，叔叔 u = 50 是<b>黑</b>；p 是左孩子、x 是右孩子 → <b>Case 2(a) LR</b>。<br>
<b>第 2 个空框</b>：左旋 p = 15，得到 34 的左孩子 20（红），20 的左孩子 15（红，挂 3、16），20 的右孩子 25 → 变成 <b>LL</b>。<br>
最后 <b>Case 3(a) LL</b>：右旋 g = 34，交换 34 与 20 的颜色 → 20 成为黑色的根（题图最后一棵）。</p>""" + \
    row(svg(q21[0], 0.72, "插入 27"), svg(q21[1], 0.72, "空框 1：Case 1 重新着色"), svg(q21[2], 0.72, "空框 2：左旋 15（LR→LL）"), svg(q21[3], 0.72, "右旋 34 + 换色"))

A["isa-partof"] = """<p><b>(a)</b> <b>is-a</b>：泛化 / 继承（generalization / inheritance），子类是父类的一种，例如 Dog is-a Animal。<br>
<b>isPartOf</b>：整体-部分关系（aggregation / composition），例如 Engine isPartOf Car；composition 中部分不能脱离整体独立存在。</p>
<p><b>(b)</b> is-a：<b>实线 + 空心三角箭头</b>，箭头指向父类（实现接口用虚线 + 空心三角）。<br>
isPartOf：<b>菱形</b>画在整体一端；空心菱形 = aggregation（部分可独立存在），<b>实心菱形 = composition</b>（部分不能脱离整体存在）。</p>"""

A["genstack-diff"] = """<p><b>GenericStack&lt;T&gt;</b>：参数化（泛型）类型，使用时指定具体类型，如 GenericStack&lt;String&gt;；编译器做类型检查，取元素不用强制转换，类型错误在编译期发现，类型安全。<br>
<b>GenericStack</b>：原始类型（raw type），相当于 GenericStack&lt;Object&gt;，什么对象都能放进去，编译器不检查；取出时要强转，类型不对会在运行时抛 ClassCastException。</p>"""
