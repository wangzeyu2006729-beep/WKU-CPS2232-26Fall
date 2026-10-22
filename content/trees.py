"""Tiny BST / AVL / RB helpers + SVG renderer for the answer key."""
import html


class N:
    def __init__(self, k, color=None, left=None, right=None, mark=None):
        self.k, self.color, self.left, self.right, self.mark = k, color, left, right, mark


def T(spec):
    """Build tree from nested tuples: (key, left, right) or (key, left, right, color)."""
    if spec is None:
        return None
    if not isinstance(spec, tuple):
        return N(spec)
    k, l, r, *rest = spec
    return N(k, rest[0] if rest else None, T(l), T(r))


def svg(root, scale=1.0, label=None):
    pos, order = {}, []

    def ino(n, d):
        if n is None:
            return
        ino(n.left, d + 1)
        pos[id(n)] = (len(order), d)
        order.append(n)
        ino(n.right, d + 1)

    ino(root, 0)
    dx, dy, r = 42 * scale, 52 * scale, 15 * scale
    maxd = max(d for _, d in pos.values())
    W = len(order) * dx + 20
    H = (maxd + 1) * dy + 10 + (22 if label else 0)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">']

    def xy(n):
        i, d = pos[id(n)]
        return 10 + dx / 2 + i * dx, 20 * scale + d * dy

    def edges(n):
        if n is None:
            return
        x, y = xy(n)
        for c in (n.left, n.right):
            if c is not None:
                cx, cy = xy(c)
                out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" stroke="#555" stroke-width="1.3"/>')
                edges(c)

    edges(root)
    for n in order:
        x, y = xy(n)
        fill, stroke, tc = "#fff", "#333", "#111"
        if n.color == "B":
            fill, stroke, tc = "#2b2b2b", "#000", "#fff"
        elif n.color == "R":
            fill, stroke, tc = "#e53935", "#b71c1c", "#fff"
        elif n.color == "DB":
            fill, stroke, tc = "#2b2b2b", "#000", "#fff"
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        if n.color == "DB":
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 3.5 * scale:.1f}" fill="none" stroke="#000" stroke-width="1.5"/>')
        fs = 12 * scale if len(str(n.k)) < 4 else 10 * scale
        out.append(f'<text x="{x:.1f}" y="{y + fs * 0.36:.1f}" font-size="{fs:.1f}" text-anchor="middle" fill="{tc}" font-family="Helvetica,Arial">{html.escape(str(n.k))}</text>')
        if n.mark:
            out.append(f'<text x="{x + r + 2:.1f}" y="{y - r + 4:.1f}" font-size="{10 * scale:.1f}" fill="#1565c0" font-family="Helvetica,Arial">{html.escape(n.mark)}</text>')
    if label:
        out.append(f'<text x="{W / 2:.1f}" y="{H - 6:.1f}" font-size="12" text-anchor="middle" fill="#333" font-family="PingFang SC,Helvetica">{html.escape(label)}</text>')
    out.append("</svg>")
    return "".join(out)


# ---------------- AVL (balance factor = h(right) - h(left); leaf height 1) ----------------
def h(n):
    return 0 if n is None else 1 + max(h(n.left), h(n.right))


def rot_left(x):
    y = x.right
    x.right, y.left = y.left, x
    return y


def rot_right(y):
    x = y.left
    y.left, x.right = x.right, y
    return x


def avl_insert(root, k, log):
    if root is None:
        return N(k)
    if k == root.k:
        log.append(f"{k} 重复，忽略")
        return root
    if k < root.k:
        root.left = avl_insert(root.left, k, log)
    else:
        root.right = avl_insert(root.right, k, log)
    bf = h(root.right) - h(root.left)
    if bf < -1:
        if k < root.left.k:
            log.append(f"插入 {k}：节点 {root.k} bf={bf}，LL 型 → 右旋 {root.k}")
        else:
            log.append(f"插入 {k}：节点 {root.k} bf={bf}，LR 型 → 先左旋 {root.left.k}，再右旋 {root.k}")
            root.left = rot_left(root.left)
        return rot_right(root)
    if bf > 1:
        if k > root.right.k:
            log.append(f"插入 {k}：节点 {root.k} bf=+{bf}，RR 型 → 左旋 {root.k}")
        else:
            log.append(f"插入 {k}：节点 {root.k} bf=+{bf}，RL 型 → 先右旋 {root.right.k}，再左旋 {root.k}")
            root.right = rot_right(root.right)
        return rot_left(root)
    return root


def clone(n):
    if n is None:
        return None
    return N(n.k, n.color, clone(n.left), clone(n.right))


# ---------------- RB insert (professor's case names) ----------------
class RB:
    def __init__(self):
        self.root = None
        self.par = {}

    def insert(self, k, log):
        x = N(k, "R")
        if self.root is None:
            x.color = "B"
            self.root = x
            self.par[id(x)] = None
            log.append(f"插入 {k}：根节点 → 涂黑")
            return
        p = self.root
        while True:
            nxt = p.left if k < p.k else p.right
            if nxt is None:
                break
            p = nxt
        if k < p.k:
            p.left = x
        else:
            p.right = x
        self.par[id(x)] = p
        steps = []
        while True:
            p = self.par[id(x)]
            if p is None:
                if x.color == "R":
                    x.color = "B"
                    steps.append("根变红 → 重新涂黑")
                break
            if p.color == "B":
                break
            g = self.par[id(p)]
            u = g.right if g.left is p else g.left
            if u is not None and u.color == "R":
                steps.append(f"Case 1（叔叔 {u.k} 为红）：p={p.k}、u={u.k} 涂黑，g={g.k} 涂红")
                p.color = u.color = "B"
                g.color = "R"
                x = g
                continue
            if g.left is p and p.right is x:
                steps.append(f"Case 2(a) LR（叔叔为黑）：左旋 p={p.k} → 变成 LL")
                self._rot(p, "L")
                x, p = p, x
            elif g.right is p and p.left is x:
                steps.append(f"Case 2(b) RL（叔叔为黑）：右旋 p={p.k} → 变成 RR")
                self._rot(p, "R")
                x, p = p, x
            if g.left is p:
                steps.append(f"Case 3(a) LL：右旋 g={g.k}，交换 g={g.k} 与 p={p.k} 的颜色")
                self._rot(g, "R")
            else:
                steps.append(f"Case 3(b) RR：左旋 g={g.k}，交换 g={g.k} 与 p={p.k} 的颜色")
                self._rot(g, "L")
            g.color, p.color = p.color, g.color
            break
        log.append(f"插入 {k}：" + ("；".join(steps) if steps else "父节点为黑，无需调整"))

    def _rot(self, n, d):
        pp = self.par[id(n)]
        if d == "L":
            c = n.right
            n.right = c.left
            if c.left:
                self.par[id(c.left)] = n
            c.left = n
        else:
            c = n.left
            n.left = c.right
            if c.right:
                self.par[id(c.right)] = n
            c.right = n
        self.par[id(n)] = c
        self.par[id(c)] = pp
        if pp is None:
            self.root = c
        elif pp.left is n:
            pp.left = c
        else:
            pp.right = c
