"""CPS2232 question data: every distinct question once, tagged with lecture, sources and exam numbers."""

LECTURES = [
    ("L1 递归", "Recursion (Ch18)"),
    ("L2 类、对象与引用", "Objects, Classes & References"),
    ("L3 泛型", "Generics (Ch19)"),
    ("L4 ADT、接口与 Lambda", "ADTs, Interfaces & Lists (Ch20)"),
    ("L5 栈与队列", "Stacks & Queues (Ch20)"),
    ("L6 Set、Map 与哈希表", "Sets, Maps & Hash Tables (Ch21)"),
    ("L7 链表实现", "List Implementation (Ch24)"),
    ("L8 堆与优先队列", "Heaps & Priority Queues (Ch20/24)"),
    ("L9 哈希", "Hashing (Ch27)"),
    ("L10 算法分析", "Analysis of Algorithms (Ch22)"),
    ("L11 排序", "Sorting (Ch23)"),
    ("L12 动态规划", "Dynamic Programming"),
    ("L13 BST 与 AVL", "BST & AVL Trees (Ch26)"),
    ("L14 红黑树", "Red-Black Trees (Ch43)"),
]
SOURCES = {
    "A": "题库A · Stud_Bank.pdf",
    "B": "题库B · 2025.12.8 DSA Bank.pdf",
    "M24": "2023/24 春季期中真题",
    "F25": "2025 秋季考试真题",
    "K": "课堂/会考提示",
    "AS1": "作业1 · AS CPS2232 DSA_Unit1-4.pdf",
}
EXAMS = {
    "M24": dict(title="2023/24 Spring Mid-Term Exam", short="24春期中",
                note="7 张试卷照片（第 6 页缺失），含老师批改。Part A 判断 17 题、B 选择 6 题、C 填空 11 题、D 解答 5 题。",
                parts=[(1, "Part A: True or False (85 points: 17 quizzes, 5pts each)"), (18, "Part B: Multiple Choice (30 points: 6 quizzes, 5pts each)"),
                       (24, "Part C: Short answers/Fill-in the gap (55 points: 11 quizzes, 5pts each)"), (35, "Part D: Essay (20 points: 4 quizzes, 5pts each)")]),
    "F25": dict(title="2025 Fall Exam", short="25秋考试",
                note="4 张试卷照片（第 2–4 页及第 1 页下半），卷面无答案。Part A 判断、B 选择、C 填空各 10 题，D 解答 4 题。",
                parts=[(1, "Part A: True or False (10 questions: 100 points, 10pt each)"), (11, "Part B: Multiple Choice (10 questions: 100 points, 10pt each)"),
                       (21, "Part C: Short answers/Fill-in the gap (10 questions: 100 points: 10pts each)"), (31, "Part D: Essay (4 questions: 100 points: 25pts each)")]),
}
# 期中前 = Lecture 1–7 (both past midterms test lists from Lecture 7), plus the Lecture 9 hashing items both
# midterms test: bucket-array modulo indexing (already in the Lecture 6 slides) and polynomial string hash codes.
# Everything else (Lecture 8, the rest of Lecture 9, Lecture 10–14) is 期中后.
MID_LAST_LECTURE = 7
MID_EXTRA_KEYS = {"hash-n20", "hash-n21", "hc-hello", "hc-tops", "hc-three"}

Q = []
TF_ZH =["正确（True）", "错误（False）"]


def _add(**d):
    d.setdefault("exam", {})
    d.setdefault("fig", [])
    d.setdefault("note", "")
    d["src"] = d["src"].split()
    for e in d["exam"]:
        assert e in d["src"], (d["key"], e)
    assert d["key"] not in {q["key"] for q in Q}, d["key"]
    Q.append(d)


def tf(ch, key, q, a, ex, src, zh, exam=None, note=""):
    _add(ch=ch, key=key, type="tf", text=q, options=["True", "False"], answer="A" if a == "T" else "B",
         ex=ex, src=src, zh=zh, zo=TF_ZH, exam=exam or {}, note=note)


def mc(ch, key, q, opts, a, ex, oe, src, zh, zo, exam=None, fig=None, note=""):
    assert len(opts) == len(oe) == len(zo), key
    _add(ch=ch, key=key, type="mc", text=q, options=opts, answer=a, ex=ex, oe=oe, src=src, zh=zh, zo=zo,
         exam=exam or {}, fig=fig or [], note=note)


def fb(ch, key, q, answers, ex, src, zh, exam=None, fig=None, note="", etext=None):
    import re
    assert len(re.findall(r"____\[\d+\]", q)) == len(answers) == len(re.findall(r"____\[\d+\]", zh)), key
    _add(ch=ch, key=key, type="fill", text=q, options=[], answers=answers, ex=ex, src=src, zh=zh, zo=[],
         exam=exam or {}, fig=fig or [], note=note, etext=etext)


def es(ch, key, q, html, src, zh, exam=None, fig=None, ex="", note=""):
    _add(ch=ch, key=key, type="essay", text=q, options=[], html=html, ex=ex, src=src, zh=zh, zo=[],
         exam=exam or {}, fig=fig or [], note=note)


# =====================================================================  L1 递归
tf(1, "rec-eff", "Recursive methods are computationally more efficient than iterative techniques.", "F",
   "递归每次调用都要压栈（保存参数、局部变量和返回地址），有额外的时间和空间开销，一般不比等价的迭代写法高效；递归的优点是写法简洁、适合递归结构的问题。",
   "B", "递归方法在计算上比迭代方法更高效。")

# =====================================================================  L2 类、对象与引用
tf(2, "class-ref-obj", "A class always references its object.", "F",
   "是对象（通过引用变量）指向某个类的实例，而不是类去引用它的对象。2024 春期中有同学选 True 被判错。",
   "A B M24", "类总是引用它的对象。", exam={"M24": "1"})
tf(2, "obj-ref-class", "An object always references its class.", "T",
   "每个对象都是某个类的实例，可以通过它找到所属的类（如 getClass()）。题库批注为 True。",
   "A B", "对象总是引用它所属的类。")
tf(2, "default-ctor", "Default constructors must be the first statement in its method body.", "F",
   "False。默认构造方法是一个构造方法，不是一条“语句”，说它是“第一条语句”不成立。Java 真正的规则（Lecture 2「The Superclass Constructor is always Invoked」）是：构造方法体的第一条语句必须是 this(...) 或 super(...)；没有显式写时，编译器自动插入 super()（调用父类的无参构造方法）作为第一条语句。",
   "A B M24", "默认构造方法必须是其方法体中的第一条语句。", exam={"M24": "4"},
   note="题库A 批注为 True，24春期中第 4 题学生也选了 True（该页 Part A 得 75/85，照片上没有逐题对错标记）。本站按 Java 的实际规则判 False；如果考试照题库给分，那是把题意理解成“编译器插入的 super() 是第一条语句”。")
fb(2, "new-kw", "Given the following statement\n    Progression arithmeticProgress = new Progression();\nThe function (job) of the new keyword is ____[1].",
   ["to create (instantiate) a new Progression object: allocate memory for it on the heap, call the constructor, and return its reference"],
   "new 创建对象：在堆上分配内存、调用构造方法，并把对象的引用（地址）返回给引用变量 arithmeticProgress。",
   "A B M24", "给定语句 Progression arithmeticProgress = new Progression(); new 关键字的作用是 ____[1]。", exam={"M24": "26"})
fb(2, "ref-var", "Given the following statement\n    Progression arithmeticProgress = new Progression();\nReference variable in the statement is ____[1].",
   ["arithmeticProgress"], "引用变量是等号左边保存对象地址的变量名 arithmeticProgress；Progression 是类型。",
   "A B M24", "上述语句中的引用变量是 ____[1]。", exam={"M24": "27"})
fb(2, "ref-var-desc", "A reference variable can be described as ____[1].",
   ["a variable that holds the address (reference / memory location) of an object rather than the object itself"],
   "引用变量存放的是对象在堆中的地址，通过它访问对象。",
   "A B", "引用变量可以描述为 ____[1]。")
fb(2, "heap-dynamic", "During program execution, a heap could be described as ____[1] memory allocation.",
   ["dynamic"], "运行时用 new 创建的对象都放在堆（heap）上，属于动态内存分配；局部变量和方法调用在栈（stack）上。",
   "A B", "在程序执行期间，堆可以被描述为 ____[1] 内存分配。")
fb(2, "uml-comp", "The given symbol  ──────◆  (solid line with a filled diamond) in a UML diagram is known as ____[1].",
   ["composition"], "实心菱形 = composition（组合）；空心菱形 = aggregation（聚合）。",
   "A B F25", "UML 图中给出的符号（实线 + 实心菱形）称为 ____[1]。", exam={"F25": "23"}, fig=["uml_comp.png"])
fb(2, "uml-comp-mean", "In the above (composition symbol), the meaning of the symbol is stated as ____[1].",
   ["a strong whole-part (isPartOf) relationship: the part cannot exist without the whole and shares its lifetime"],
   "组合是强的整体-部分关系，部分不能脱离整体独立存在，例如 bird 与 wings、car 与 engine。",
   "A B F25", "上题中该（组合）符号的含义是 ____[1]。", exam={"F25": "24"})
fb(2, "uml-real", "The given symbol  - - - - -▷  (dashed line with a hollow triangle) in a UML diagram is known as ____[1].",
   ["realization (interface implementation)"], "虚线 + 空心三角箭头 = realization（实现），箭头指向被实现的接口；实线 + 空心三角是继承（generalization）。",
   "A B", "UML 图中给出的符号（虚线 + 空心三角）称为 ____[1]。", fig=["uml_real.png"])
fb(2, "uml-real-mean", "In the above (realization symbol), the meaning of the symbol is stated as ____[1].",
   ["a class implements an interface (the arrow points to the interface)"], "表示类实现（implements）某个接口。",
   "A B", "上题中该（实现）符号的含义是 ____[1]。")

# =====================================================================  L3 泛型
tf(3, "gen-cast", "Generics framework is a way to avoid casting explicitly.", "T",
   "使用泛型后编译器知道元素类型，取出元素时不需要显式强制类型转换，类型错误在编译期就能发现。",
   "A B M24", "泛型框架是一种避免显式类型转换的方式。", exam={"M24": "5"})
tf(3, "gen-prim", "In a parameterized generic class, actual or concrete parameter types can be primitive types.", "F",
   "泛型的实际类型参数必须是引用类型，例如 ArrayList<Integer>，不能写 ArrayList<int>；基本类型要用包装类。",
   "A B M24", "在参数化的泛型类中，实际（具体）类型参数可以是基本类型。", exam={"M24": "6"})
tf(3, "gen-raw-flex", "The type GenericStack can be more flexible than the GenericStack<T> type.", "F",
   "GenericStack 是原始类型（raw type），编译器不做类型检查，取出元素要强转，容易在运行时出错，不能说比泛型类型“更灵活”。",
   "A B M24", "GenericStack 类型可以比 GenericStack<T> 类型更灵活。", exam={"M24": "8"})
mc(3, "print-obj", "Given the code snippet, which is odd among the options?\n\npublic static void print(Object[] list) {\n    for (int i = 0; i < list.length; i++)\n        System.out.print(list[i] + \" \");\n    System.out.println();\n}",
   ["No target object is specified.", "Prone to error when lists are not consistent.", "Accept all types including primitives", "Accept only object types"], "C",
   "参数类型是 Object[]，只能接收引用类型的数组；int[]、double[] 等基本类型数组传不进去，所以 C 的说法不成立，是“odd”的一项。2024 春期中选 C 判对。",
   ["描述成立：Object[] 没有指定具体的目标元素类型，任何引用类型的数组都能传入（对比泛型方法 print(E[]) 指定了类型 E）。", "Object[] 可以混装不同类型的元素，类型不一致时容易出错，描述成立。", "错误说法：基本类型数组（如 int[]）不是 Object[]，不能传入。", "描述成立：只接受对象（引用类型）数组。"],
   "A B M24", "给定代码片段，下列哪一项与众不同（说法不对）？", ["没有指定目标对象。", "当列表元素类型不一致时容易出错。", "接受包括基本类型在内的所有类型", "只接受对象类型"],
   exam={"M24": "19"})
mc(3, "gen-ctor", "Which of the following program statement about generic constructors is incorrect?",
   ["new GenericStack<T>( )", "new GenericStack( )", "new GenericStack<String>( )", "new GenericStack<Number>()"], "A",
   "在普通代码（如 main）里 T 不是已声明的类型，new GenericStack<T>() 无法编译，所以 A 不正确；只有在声明了类型参数 T 的泛型类或泛型方法内部，这种写法才合法。B 是原始类型（raw type），可以编译（有 unchecked 警告）；C、D 是正确的参数化写法。2024 春期中有同学选 B 被判错；2025 秋考试第 13 题和第 20 题重复出现此题。",
   ["不正确：T 在这里不是已声明的类型，无法编译。", "原始类型构造，可以编译（有警告）。", "正确写法，具体类型 String。", "正确写法，具体类型 Number。"],
   "A B M24 F25", "下列关于泛型构造方法的程序语句中，哪一个是错误的？",
   ["new GenericStack<T>( )", "new GenericStack( )", "new GenericStack<String>( )", "new GenericStack<Number>()"],
   exam={"M24": "20", "F25": "13, 20"})
mc(3, "unbounded", "Which of the following is termed as an unbounded generic wildcard.",
   ["< ? super E >", "< ? extends E >", "< E extends Object >", "< Object extends E >"], "C",
   "严格说四个选项都不对：真正的无界通配符是 <?>（等价于 <? extends Object>），选项里没有。C 的 <E extends Object> 是“无界类型参数”（Liang：<E> 等同于 <E extends Object>），不是通配符，但它是唯一不设限的写法，所以只能选 C。A 是下界通配符，B 是上界通配符。题库A 学长批注高亮的是 B，与讲义定义不符；题库A 的 D 选项印作 < E extends ? >。",
   ["下界（lower bounded）通配符：E 或 E 的父类。", "上界（upper bounded）通配符：E 或 E 的子类，不是无界。", "无界类型参数，等价于 <E>；不是通配符，但在这些选项里最接近“无界”。", "写法本身不合法。"],
   "A B F25", "下列哪一个被称为无界泛型通配符？", ["< ? super E >", "< ? extends E >", "< E extends Object >", "< Object extends E >"],
   exam={"F25": "14"})
fb(3, "wrapper", "Wrapper classes are ____[1] types.", ["reference (object)"],
   "包装类（Integer、Double、Character…）把基本类型包装成对象，属于引用类型，可以放进泛型集合。",
   "A B M24", "包装类是 ____[1] 类型。", exam={"M24": "28"})
fb(3, "gen-cap", "Generics is the capability to ____[1].", ["parameterize types (define classes, interfaces and methods with type parameters)"],
   "泛型就是把类型参数化：定义时用类型参数 <T>，使用时代入具体类型，由编译器检查类型。",
   "A B", "泛型是 ____[1] 的能力。")
fb(3, "wildcards", "Identify the following wildcard notations and give examples of each:\n<? extends T> is ____[1], e.g. ____[2];\n<? super T> is ____[3], e.g. ____[4].",
   ["upper bounded wildcard (T or a subtype of T)", "ArrayList<? extends Number> list = new ArrayList<Integer>();",
    "lower bounded wildcard (T or a supertype of T)", "ArrayList<? super Integer> list = new ArrayList<Number>();"],
   "extends 设上界，接受 T 及其子类；super 设下界，接受 T 及其父类。",
   "A B", "说出下列通配符的名称并各举一例：<? extends T> 是 ____[1]，例如 ____[2]；<? super T> 是 ____[3]，例如 ____[4]。")

# =====================================================================  L4 ADT、接口、Lambda、List
tf(4, "lambda-can", "Lambda expression can be used to implement a functional interface.", "T",
   "函数式接口只有一个抽象方法，Lambda 表达式就是这个方法的实现。", "A B", "Lambda 表达式可以用来实现函数式接口。")
tf(4, "lambda-cannot", "Lambda expression cannot be used to implement a functional interface.", "F",
   "与上一题相反，Lambda 正是用来实现函数式接口的。", "B", "Lambda 表达式不能用来实现函数式接口。")
tf(4, "lambda-obj", "With the Lambda expression, objects of functional interfaces can implement the methods of an interface.", "T",
   "Lambda 表达式生成函数式接口的对象，并实现接口中唯一的抽象方法。", "F25", "借助 Lambda 表达式，函数式接口的对象可以实现接口中的方法。", exam={"F25": "8"})
tf(4, "iface-impl", "Methods declared in interfaces provide implementation detail.", "F",
   "一般而言为 False：接口中的抽象方法只有方法头，没有方法体，具体实现由实现该接口的类提供。例外是 Java 8 起的 default、static 方法（以及 Java 9 的 private 方法）可以带方法体（见 L4-TF08），所以说接口方法“提供实现细节”不是普遍成立的。", "A B M24", "接口中声明的方法提供实现细节。", exam={"M24": "2"})
tf(4, "iface-single", "Interfaces can have single inheritance but abstract classes can have multiple inheritance.", "F",
   "正好相反：一个接口可以继承多个接口、一个类可以实现多个接口；类（包括抽象类）只能单继承。题库A 原文为 “…abstract classes can also have multiple inheritance”。",
   "A B M24", "接口只能单继承，而抽象类可以多继承。", exam={"M24": "3"})
tf(4, "iface-multi", "Interfaces can have multiple inheritance but (abstract) classes can only have single class inheritance.", "T",
   "接口可多继承，类只能 extends 一个父类。", "B", "接口可以多继承，而（抽象）类只能单继承。")
tf(4, "iface-both", "Interfaces can have multiple inheritance, and abstract classes can also have multiple inheritance.", "F",
   "抽象类也是类，只能单继承。", "F25", "接口可以多继承，抽象类也可以多继承。", exam={"F25": "10"})
tf(4, "default-kw", "The keyword default is used in the methods of an interface.", "T",
   "Java 8 起，接口中可以用 default 关键字定义带方法体的默认方法。", "A B M24", "关键字 default 用于接口的方法中。", exam={"M24": "7"})
tf(4, "default-impl", "The default keyword allows interfaces to override and define its implementation method.", "T",
   "default 方法让接口自己提供方法实现，实现类可以直接继承或重写。", "F25", "default 关键字允许接口重写并定义其实现方法。", exam={"F25": "5"})
tf(4, "list-del-tail", "Deletion from a list shifts elements towards the tail of the list.", "F",
   "从数组表中删除一个元素后，它后面的元素都向表头（head）方向前移一位来填补空位，不是向表尾移动。",
   "A B M24", "从列表中删除元素会使元素向表尾方向移动。", exam={"M24": "9"})
fb(4, "iface-headers", "Methods declared in interfaces are just method headers because ____[1].",
   ["the implementation (method body) is provided by the class that implements the interface"],
   "接口只声明“能做什么”，由实现类决定“怎么做”。", "A B M24", "接口中声明的方法只是方法头，因为 ____[1]。", exam={"M24": "24"})
fb(4, "alist-1", "Given the following code snippet:\n    ArrayList<Integer> list = new ArrayList<>();\n    list.add(23);\n    list.add(12);\n    list.add(37);\n    list.add(2,10);\nThe output is ____[1].",
   ["[23, 12, 10, 37]"], "add(e) 追加到末尾：[23, 12, 37]；add(2, 10) 插到下标 2，原来的 37 后移：[23, 12, 10, 37]。（原题把 new 印成了 newe）",
   "A B M24", "给定代码（依次 add 23、12、37，再 add(2,10)），输出是 ____[1]。", exam={"M24": "29"})
fb(4, "alist-2", "Given the following code snippet:\n    ArrayList<Integer> list = new ArrayList<>();\n    list.add(23);\n    list.add(12);\n    list.add(37);\n    list.add(1,56);\n    list.add(17);\n    list.add(4,83);\nThe output is ____[1].",
   ["[23, 56, 12, 37, 83, 17]"], "[23] → [23,12] → [23,12,37] → add(1,56)：[23,56,12,37] → add(17)：[23,56,12,37,17] → add(4,83)：[23,56,12,37,83,17]。",
   "F25", "给定代码（add 23、12、37，add(1,56)，add 17，add(4,83)），输出是 ____[1]。", exam={"F25": "21–22"})
es(4, "lambda-mult", "Here is a functional interface code:\n\npublic interface NumberMultiply {\n    double mult(double a, double b);\n}\n\nImplement this interface (write a short program) using lambda expression given the values 2 and 3.",
   "", "A B M24", "给出函数式接口 NumberMultiply（方法 double mult(double a, double b)），用 Lambda 表达式实现它，并用 2 和 3 调用。", exam={"M24": "35"})

# =====================================================================  L5 栈与队列
fb(5, "stack-lifo", "The principle of stack operation is ____[1].", ["LIFO (last in, first out)"],
   "栈只在栈顶 push / pop，后进先出。", "A B", "栈操作的原则是 ____[1]。")
fb(5, "queue-fifo", "Queues operate the principle of a ____[1].", ["FIFO (first in, first out)"],
   "队列在 rear 入队、在 front 出队，先进先出。", "A B", "队列遵循 ____[1] 原则。")
fb(5, "queue-front", "Deletion is only possible at ____[1] end of a queue.", ["the front"],
   "出队（dequeue）只能在 front 端；入队（enqueue）在 rear（back）端。", "A B F25", "队列只能在 ____[1] 端删除。", exam={"F25": "25"})
fb(5, "queue-formula", "The formula for determining the number of elements in a queue is ____[1].", ["(rear − front) + 1"],
   "课上公式：No. of elements = (Back − Front) + 1（rear 也叫 back）。2024 春期中有人写 getSize() 被判错；会考提示中也强调了这个公式。",
   "A B M24 F25 K", "确定队列中元素个数的公式是 ____[1]。", exam={"M24": "32", "F25": "28"})
fb(5, "queue-count3", "Given the following queue, applying the formula for the number of elements, the queue has ____[1] number of elements.\n\n| [0]   | [1]   | [2]   | [3] 4 | [4] 11 | [5] -1 |",
   ["3"], "front 是第一个有元素的下标 3，rear 是最后一个下标 5：(5 − 3) + 1 = 3。2024 春期中写 6 被判错，写 3 判对。",
   "A B M24 F25", "给定队列（下标 3、4、5 依次存 4、11、-1，前三格为空），用元素个数公式，队列有 ____[1] 个元素。", exam={"M24": "34", "F25": "30"})
fb(5, "queue-count4", "Given the following queue, applying the formula for the number of elements, the queue has ____[1] number of elements.\n\n| [0]   | [1]   | [2] 19 | [3] 24 | [4] 100 | [5] -13 |",
   ["4"], "front = 2，rear = 5：(5 − 2) + 1 = 4。", "B", "给定队列（下标 2–5 依次存 19、24、100、-13），队列有 ____[1] 个元素。")
mc(5, "queue-adt", "By convention, which of the following is a method of the Queue ADT.", ["pop( )", "push( )", "enque( )", "add( )"], "C",
   "按 ADT 约定，队列的操作是 enqueue / dequeue，栈的操作是 push / pop。（Java 的 Queue 接口也有 add/offer，但题目问 ADT 约定）",
   ["栈的出栈操作。", "栈的入栈操作。", "队列入队操作，应选。", "Java 集合的通用方法，不是队列 ADT 的约定名称。"],
   "B F25", "按约定，下列哪一个是队列 ADT 的方法？", ["pop( )", "push( )", "enque( )", "add( )"], exam={"F25": "11"})
mc(5, "stack-adt", "By convention, which of the following is the method of the stack ADT.", ["pop( )", "deque( )", "enque( )", "add( )"], "A",
   "栈 ADT：push、pop、peek。原卷选项字母印作 e–h（另一版 i–l）。",
   ["栈的出栈操作，应选。", "队列出队操作。", "队列入队操作。", "集合通用方法，不是栈 ADT 约定。"],
   "B", "按约定，下列哪一个是栈 ADT 的方法？", ["pop( )", "deque( )", "enque( )", "add( )"])
fb(5, "stack-out", "In the following stack program\n    IntStack s = new IntStack();\n    s.push(1);\n    s.push(2);\n    s.push(3);\n    System.out.println(s.pop());\nThe output from the print out statement is ____[1].",
   ["3"], "后进先出：最后压入的 3 最先弹出。", "A B", "依次 push 1、2、3 后执行 pop 并打印，输出是 ____[1]。")

# =====================================================================  L6 Set / Map
tf(6, "hashmap-ord", "HashMap is an ordered data structure.", "F", "HashMap 按哈希值存放，输出顺序不确定。", "A B M24", "HashMap 是有序的数据结构。", exam={"M24": "11"})
tf(6, "lhm-ins", "LinkedHashMap is a data structure whose output follows the order of insertion.", "T",
   "LinkedHashMap 用双向链表记录插入顺序（默认），遍历时按插入顺序输出。", "A B M24", "LinkedHashMap 的输出遵循插入顺序。", exam={"M24": "12"})
tf(6, "lhm-random", "LinkedHashMap is a data structure whose output follows some random order against the inserting order.", "F",
   "LinkedHashMap 默认按插入顺序输出，不是随机顺序。", "F25", "LinkedHashMap 的输出是与插入顺序不同的某种随机顺序。", exam={"F25": "1"})
tf(6, "lhs-not", "The output from the LinkedHashSet does not follow the order of insertion.", "F", "LinkedHashSet 按插入顺序输出。", "A B", "LinkedHashSet 的输出不遵循插入顺序。")
tf(6, "lhs-ins", "The output from the LinkedHashSet follows the order of insertion.", "T", "LinkedHashSet = HashSet + 链表记录插入顺序。", "A B M24", "LinkedHashSet 的输出遵循插入顺序。", exam={"M24": "15"})
tf(6, "treemap-asc", "TreeMap is an ordered data structure that outputs elements in ascending order.", "T",
   "TreeMap 按键排序（默认升序，基于红黑树）。", "A B M24", "TreeMap 是有序的数据结构，按升序输出元素。", exam={"M24": "13"})
tf(6, "lhs-dup", "LinkedHashSet allows duplicate elements.", "F", "所有 Set 都不允许重复元素。2024 春期中选 False 判对。", "A B M24", "LinkedHashSet 允许重复元素。", exam={"M24": "14"})
tf(6, "hs-dup", "The HashSet allows duplicate element.", "F", "Set 不允许重复元素，add 重复元素会返回 false。", "F25", "HashSet 允许重复元素。", exam={"F25": "7"})
tf(6, "hs-order", "The output of the HashSet follows its insertion order.", "F", "HashSet 无序；要保持插入顺序用 LinkedHashSet。", "F25", "HashSet 的输出遵循插入顺序。", exam={"F25": "6"})
tf(6, "set-dup", "A set is an unordered collection of element that can take duplicate elements.", "F",
   "Set 是不含重复元素的集合（Liang：store unordered, non-duplicate elements）。", "F25", "Set 是可以包含重复元素的无序集合。", exam={"F25": "9"})
tf(6, "map-dupkey", "The Map data structure allows duplicate keys.", "F", "Map 的键唯一；put 已存在的键会覆盖旧值。", "A B M24", "Map 数据结构允许重复的键。", exam={"M24": "16"})
tf(6, "map-dupval", "The Map<K, V> data structure allows duplicate values.", "T", "不同的键可以对应相同的值。", "A B M24 F25", "Map<K, V> 数据结构允许重复的值。", exam={"M24": "17", "F25": "2"})
tf(6, "lhm-access", "The LinkedHashMap(16, 0.75f) constructor statement is for creating a Map with output in last access order.", "F",
   "两参数构造器（初始容量 16、负载因子 0.75）按插入顺序；要按访问顺序需要 LinkedHashMap(16, 0.75f, true)。",
   "A B F25", "构造语句 LinkedHashMap(16, 0.75f) 用于创建按最近访问顺序输出的 Map。", exam={"F25": "3"})
tf(6, "lhm-access-true", "The LinkedHashMap(16, 0.75f, true) constructor statement is for creating a Map with output in last access order.", "T",
   "第三个参数 accessOrder = true 时，按访问顺序（最近访问的在最后）输出。", "B", "构造语句 LinkedHashMap(16, 0.75f, true) 用于创建按最近访问顺序输出的 Map。")
tf(6, "lhm-default", "The LinkedHashMap( ) constructor statement is for creating a Map with output in order of insertion.", "T",
   "无参构造器默认 accessOrder = false，即插入顺序。", "A B", "构造语句 LinkedHashMap( ) 用于创建按插入顺序输出的 Map。")
tf(6, "lf-eff", "In the LinkedHashMap(16, 0.75f), increase in load factor increases efficiency in search time complexity.", "F",
   "负载因子越大，扩容前表越满，冲突越多，查找反而变慢；提高负载因子只节省空间。", "F25", "在 LinkedHashMap(16, 0.75f) 中，增大负载因子可以提高查找的时间效率。", exam={"F25": "4"})
tf(6, "map-size", "The map.size() insert an object in the map and returns the number of entries.", "F",
   "size() 只返回键值对个数，不插入任何东西；插入用 put。", "A B M24", "map.size() 在 map 中插入一个对象并返回条目数。", exam={"M24": "10"})
tf(6, "keyset-val", "The map.keySet() returns the set of values in a map.", "F", "keySet() 返回所有键组成的 Set；values() 才返回值的集合。", "B", "map.keySet() 返回 map 中值的集合。")
mc(6, "ordered-ds", "One of the following is used to create an ordered data structure", ["HashMap", "HashSet", "LinkedHashMap", "TreeMap"], "CD",
   "C、D 都对。ordered（有序）指遍历顺序是确定的：LinkedHashMap 按插入（或访问）顺序遍历，Lecture 6 也把 LinkedHashSet 称为 ordered collection；TreeMap 按键排序，sorted 也一定是 ordered。HashMap、HashSet 无序。如果题目问的是“排序（sorted）”，才只有 D。2024 春期中选 D 判对。",
   ["无序。", "应选。按插入（或访问）顺序遍历，是有序（ordered）结构。", "应选。按键升序排列（sorted），也是有序结构。", "无序。"], "A B M24",
   "下列哪一个用于创建有序的数据结构？", ["HashMap", "HashSet", "LinkedHashMap", "TreeMap"], exam={"M24": "21"})
mc(6, "lhm-params", "In the following constructor statement LinkedHashMap(16, 0.75f), 16 and 0.75f are known as ____ and ____",
   ["Key and value pair", "InitialCapacity and loadfactor", "Data and operation", "Object and address"], "B",
   "第一个参数是初始容量，第二个是负载因子。", ["不是键值对。", "应选：初始容量和负载因子。", "无关。", "无关。"], "A B M24",
   "构造语句 LinkedHashMap(16, 0.75f) 中，16 和 0.75f 分别称为 ____ 和 ____。", ["键值对", "初始容量和负载因子", "数据和操作", "对象和地址"], exam={"M24": "22"})
mc(6, "manager-map", "Your company manager has asked you to generate a Map data structure in an increasing order of entries (k, v). Which of the following is most suitable?",
   ["TreeMap", "LinkedHashMap", "HashMap", "TreeSet"], "A",
   "要求“Map”且“按递增顺序”→ TreeMap。TreeSet 不是 Map。", ["按键升序的 Map，应选。", "插入顺序，不是递增顺序。", "无序。", "是 Set 不是 Map。"],
   "A B M24 F25", "经理要求你生成一个按条目 (k, v) 递增顺序排列的 Map，下列哪个最合适？", ["TreeMap", "LinkedHashMap", "HashMap", "TreeSet"],
   exam={"M24": "23", "F25": "16"})
mc(6, "not-sorted-ds", "One of the following is not a sorted data structure", ["SortedSet", "LinkedList", "TreeSet", "TreeMap"], "B",
   "SortedSet、TreeSet、TreeMap 都按顺序排列元素；LinkedList 只按插入位置存放。", ["有序。", "不排序，应选。", "有序。", "有序。"],
   "B F25", "下列哪一个不是排序的数据结构？", ["SortedSet", "LinkedList", "TreeSet", "TreeMap"], exam={"F25": "12"})
mc(6, "sorted-ds", "One of the following is a sorted data structure", ["HashSet", "LinkedList", "TreeSet", "HashMap"], "C",
   "TreeSet 按元素大小排序。原卷选项字母印作 e–h。", ["无序。", "不排序。", "排序，应选。", "无序。"],
   "B", "下列哪一个是排序的数据结构？", ["HashSet", "LinkedList", "TreeSet", "HashMap"])
mc(6, "not-sorted-set1", "One of the following is not a sorted set", ["SortedSet", "LinkedList", "TreeSet", "None"], "B",
   "LinkedList 不是排序集合（甚至不是 Set）。", ["排序集合接口。", "应选。", "排序集合。", "B 就是答案，所以不是 None。"],
   "A B", "下列哪一个不是排序集合（sorted set）？", ["SortedSet", "LinkedList", "TreeSet", "以上都不是"])
mc(6, "not-sorted-set2", "One of the following is not a sorted set", ["SortedSet", "TreeSet", "TreeMap", "HashMap"], "CD",
   "C、D 都对。SortedSet、TreeSet 是排序集合。TreeMap 虽然按键排序，但它是 Map（实现 SortedMap），不是 Set；HashMap 既不是 Set 也不排序。命题本意多半是 D，但按字面 TreeMap 同样“不是 sorted set”。",
   ["排序集合。", "排序集合。", "应选。按键排序，但它是 Map，不是 Set。", "应选。既不是 Set，也不排序。"],
   "B", "下列哪一个不是排序集合？", ["SortedSet", "TreeSet", "TreeMap", "HashMap"])
mc(6, "not-sorted-set3", "One of the following is not a sorted set", ["HashSet", "LinkedList", "TreeSet", "HashMap"], "ABD",
   "A、B、D 都对，只有 TreeSet 是排序集合。HashSet 是无序的 Set；LinkedList 是 List，不是 Set；HashMap 既不是 Set 也不排序。2024 春期中这题选 B（LinkedList）判对，那只是阅卷结果，不代表 A、D 错。",
   ["应选。是 Set，但无序。", "应选。是 List，不是 Set。", "排序集合。", "应选。是 Map，既不是 Set 也不排序。"],
   "M24", "下列哪一个不是排序集合？", ["HashSet", "LinkedList", "TreeSet", "HashMap"], exam={"M24": "18"})
mc(6, "dup-elem", "One of the following data structures accept duplicate elements", ["HashSet", "HashMap", "LinkedHashSet", "Set"], "B",
   "各种 Set 都不允许重复元素。HashMap 的键不能重复，但值可以重复，所以把“元素”理解为值时选 B；题干的 elements 措辞不严谨。", ["Set，不允许重复。", "值可以重复（键不能重复），应选。", "Set，不允许重复。", "不允许重复。"],
   "A B", "下列哪一种数据结构接受重复元素？", ["HashSet", "HashMap", "LinkedHashSet", "Set"])
mc(6, "set-iter", "To get an iterator from a set, you may use the ______ method.", ["getIterator", "findIterator", "iterator", "iterators"], "C",
   "Collection 接口的方法是 iterator()。", ["没有这个方法。", "没有这个方法。", "应选：set.iterator()。", "没有这个方法。"],
   "F25", "要从一个 set 获得迭代器，可以使用 ______ 方法。", ["getIterator", "findIterator", "iterator", "iterators"], exam={"F25": "17"})
mc(6, "equals-hash", "If two objects o1 and o2 are equal, what are the values for o1.equals(o2) and o1.hashCode() == o2.hashCode()?",
   ["true true", "true false", "false true", "false false"], "A",
   "equals 相等则 hashCode 必须相等（hashCode 约定）；反过来 hashCode 相等不一定 equals。",
   ["应选。", "违反 hashCode 约定。", "对象相等时 equals 必为 true。", "不对。"],
   "F25", "如果两个对象 o1、o2 相等，o1.equals(o2) 和 o1.hashCode() == o2.hashCode() 的值分别是？", ["true true", "true false", "false true", "false false"], exam={"F25": "18"})
mc(6, "addall", "Suppose set s1 is [1, 2, 5] and set s2 is [2, 3, 6]. After s1.addAll(s2), s1 is ______.",
   ["[1, 2, 2, 3, 5, 6]", "[1, 2, 3, 5, 6]", "[1, 5]", "[2, 3, 6]"], "B",
   "addAll 求并集，重复的 2 只保留一个。", ["Set 不允许重复的 2。", "并集，应选。", "这是差集 removeAll。", "这是 s2。"],
   "F25", "设 s1 = [1, 2, 5]，s2 = [2, 3, 6]。执行 s1.addAll(s2) 后 s1 是 ______。", ["[1, 2, 2, 3, 5, 6]", "[1, 2, 3, 5, 6]", "[1, 5]", "[2, 3, 6]"], exam={"F25": "19"})
fb(6, "lf-cap", "____[1] and ____[2] is used to determine at what point the size of an array can be doubled dynamically.",
   ["load factor", "capacity"], "阈值 = capacity × load factor，元素数超过阈值时容量翻倍（rehashing）。2024 春期中判对。",
   "A B M24", "____[1] 和 ____[2] 用来决定数组何时动态翻倍。", exam={"M24": "25"})
fb(6, "lf-calc", "Give a simple calculation to explain at what point the size of an array (default capacity 16, load factor 0.75) is doubled.\nThreshold = ____[1]",
   ["16 × 0.75 = 12 (when the number of elements exceeds 12, the capacity doubles to 32)"], "阈值 = 容量 × 负载因子。",
   "A B", "用简单计算说明数组何时翻倍（默认容量 16，负载因子 0.75）。阈值 = ____[1]")
fb(6, "hs-28", "In a HashSet, if the initial capacity = 28, and load factor = 0.75. The data structure will double its capacity at ____[1].",
   ["21"], "按题目给的容量：28 × 0.75 = 21，元素个数超过 21 时容量翻倍。注意真实的 java.util.HashSet 会把容量取到不小于它的 2 的幂：new HashSet<>(28, 0.75f) 实际容量 32，阈值 32 × 0.75 = 24，插入第 25 个元素时扩到 64。", "A B", "HashSet 初始容量 28、负载因子 0.75，容量在 ____[1] 时翻倍。")
fb(6, "hs-24", "In a HashSet, if the initial capacity = 24, and load factor = 0.75. The data structure will double its capacity at ____[1].",
   ["18"], "按题目给的容量：24 × 0.75 = 18，元素个数超过 18 时容量翻倍（2024 春期中判对）。注意真实的 java.util.HashSet 会把容量取到 2 的幂：new HashSet<>(24, 0.75f) 实际容量 32，阈值 24，插入第 25 个元素时扩到 64。", "M24", "HashSet 初始容量 24、负载因子 0.75，容量在 ____[1] 时翻倍。", exam={"M24": "33"})
fb(6, "hs-10", "In a HashSet, if the initial capacity = 10, and load factor = 0.75. The data structure will double its capacity at ____[1].",
   ["7.5 (i.e. when the 8th element is added)"], "按题目给的容量：10 × 0.75 = 7.5，元素个数超过 7.5，即加入第 8 个元素时扩容。注意真实的 java.util.HashSet 会把容量取到 2 的幂：new HashSet<>(10, 0.75f) 实际容量 16，阈值 (int)(16 × 0.75) = 12，插入第 13 个元素时从 16 扩到 32。", "F25",
   "HashSet 初始容量 10、负载因子 0.75，容量在 ____[1] 时翻倍。", exam={"F25": "29"})
fb(6, "set-noequal", "Complete the statement: no two elements e1 and e2 can be in a ____[1] such that e1.equals(e2) is true.", ["Set (HashSet)"],
   "这正是 Set 不含重复元素的定义。", "A B", "补全：在 ____[1] 中不能同时存在 e1.equals(e2) 为 true 的两个元素 e1 和 e2。")
fb(6, "hs-16", "In the HashSet constructor, the value 16 is known as ____[1].", ["initial capacity"], "HashSet() 默认初始容量 16、负载因子 0.75。",
   "A B", "HashSet 构造器中的值 16 称为 ____[1]。")
fb(6, "map-get", "To get an object from a map, use ____[1].", ["map.get(key)"], "按键取值；put(key, value) 插入。", "A B", "要从 map 中取得一个对象，使用 ____[1]。")
fb(6, "keyset", "Given the following program snippet\n    Map<Integer, String> map = new HashMap<>();\n    map.add(1, \"Jane\");\n    map.add(2, \"John\");\n    map.add(3, \"Eve\");\n    map.add(4, \"Jane\");\nThe keySet method call on the map is ____[1].",
   ["map.keySet() — returns the set of keys [1, 2, 3, 4]"], "注意 Map 没有 add 方法，应为 put。keySet() 返回所有键组成的 Set。", "A B",
   "给定程序（向 map 放入 1 Jane、2 John、3 Eve、4 Jane），对 map 调用 keySet 方法是 ____[1]。")
fb(6, "map-iter", "For the same map, the iterator method call on the map is ____[1].",
   ["map.keySet().iterator() (or map.entrySet().iterator())"], "Map 本身没有 iterator()，要先取 keySet() 或 entrySet() 视图。", "A B",
   "对同一个 map，调用 iterator 方法的写法是 ____[1]。")
fb(6, "hasnext", "The hasNext() and next() on the iterator object is ____[1].",
   ["hasNext() checks whether there are more elements; next() returns the next element and advances the iterator"],
   "典型写法：while (it.hasNext()) System.out.println(it.next());", "A B", "迭代器对象上的 hasNext() 和 next() 的作用是 ____[1]。")

# =====================================================================  L7 链表实现
mc(7, "ll-node", "The node of a single linked list contains ______", ["Head and tail pointer", "Head pointer and data", "Node and data", "Data and next pointer"], "D",
   "单链表的每个节点保存数据 element 和指向下一个节点的 next 引用；head、tail 是链表对象的字段。",
   ["属于链表对象，不在节点里。", "head 不在节点里。", "说法不准确。", "应选。"],
   "B F25", "单链表的节点包含 ______。", ["头指针和尾指针", "头指针和数据", "节点和数据", "数据和 next 指针"], exam={"F25": "15"})
fb(7, "ll-front", "The time complexity for inserting at the beginning a LinkedList is ____[1].", ["O(1)"],
   "只需新建节点并修改 head 指针，与表长无关。", "F25", "在 LinkedList 开头插入的时间复杂度是 ____[1]。", exam={"F25": "26"})
fb(7, "list-del-mid", "A deletion of an element from the middle of a list will shift ____[1].",
   ["the elements after it one position towards the head of the list, filling the gap (size decreases by 1, order is kept)"],
   "对数组实现的表（ArrayList / 课上的 MyArrayList），删除中间元素后，后面的元素依次向表头方向移动一位，size 减 1，时间 O(n)。如果是链表（LinkedList），只需修改前驱节点的 next 指针，不需要移动元素。", "A B M24 F25",
   "从列表中间删除一个元素会使 ____[1]。", exam={"M24": "31", "F25": "27"},
   etext="A delete operation on an element from the middle of a list does what?\n____[1]")
es(7, "ll-add80", "Given the LinkedList 4 → 1 → 3 → 7. Write a method (code snippet) to insert element 80 in front.", "", "M24",
   "给定链表 4 → 1 → 3 → 7，写一个方法（代码片段）在表头插入 80。", exam={"M24": "30"})

# =====================================================================  L8 堆与优先队列
tf(8, "down-ins", "In the heap data structures, down heap bubbling occurs when insert an element.", "F",
   "插入时新元素放在最后位置，再向上比较交换，是 up-heap bubbling（上浮）。", "B", "在堆中，插入元素时发生 down-heap bubbling（下沉）。")
tf(8, "down-del", "In the heap data structures, down heap bubbling occurs when delete an element.", "T",
   "删除（removeMin/Max）时把最后一个节点放到根，再向下比较交换，即 down-heap bubbling。", "B", "在堆中，删除元素时发生 down-heap bubbling（下沉）。")
tf(8, "heap-lastnode", "In heaps, any deleted node is replaced by the last node.", "T",
   "堆删除后用最后一个节点（last node）填补空位，保持完全二叉树结构。删根时再向下调整（down-heap）；删任意节点时要看换上来的值，可能需要向上（up-heap）或向下调整。", "B", "在堆中，任何被删除的节点都由最后一个节点替换。")
mc(8, "heap-rel", "Which of the following statement about the relational property of binary heap is correct.",
   ["∀ v ≠ root → key(v) ≅ key(parent(v))", "∀ v ≠ root → key(v) ≥ key(parent(v))", "∀ v ≠ root → key(v) < key(parent(v))", "∀ v ≠ root → key(v) > key(parent(v))"], "B",
   "Lecture 8 的 Heap-Order Property：除根以外每个位置 p，存放的键 ≥ 其父节点的键，符号 ∀v≠root → key(child(v)) ≥ key(parent(v))，即 B（最小堆写法）。讲义也说可以有 ≥ / ≤ 两种全序。注意：题库A 学长批注高亮的是 C，但 C 是严格小于，与讲义原文不符。",
   ["“约等于”不是堆序。", "应选：讲义原文的 heap-order property。", "严格小于，不允许相等键，且与讲义写法不同（学长批注选此项）。", "严格大于，同样不允许相等键。"],
   "A B", "下列关于二叉堆关系性质（relational property）的说法哪个正确？",
   ["∀ v ≠ root → key(v) ≅ key(parent(v))", "∀ v ≠ root → key(v) ≥ key(parent(v))", "∀ v ≠ root → key(v) < key(parent(v))", "∀ v ≠ root → key(v) > key(parent(v))"])
mc(8, "heap-is", "Which of the following is a binary heap. (see figures a–d)", ["Figure a", "Figure b", "Figure c", "Figure d"], "ABC",
   "A、B、C 都对。a、b、c 都是完全二叉树且满足最大堆序（Lecture 8 允许 ≥ 或 ≤ 两种全序）；d 中 13 只有右孩子没有左孩子，不是完全二叉树。题库A 批注只标了 a。",
   ["应选。完全二叉树，满足最大堆序。", "应选。完全二叉树，满足最大堆序。", "应选。完全二叉树，满足最大堆序。", "13 只有右孩子，不完全，不是堆。"],
   "A", "下列哪一个是二叉堆？（见图 a–d）", ["图 a", "图 b", "图 c", "图 d"], fig=["heap_abcd.png"])
mc(8, "heap-not", "Which of the following is not a binary heap. (see figures a–d)", ["Figure a", "Figure b", "Figure c", "Figure d"], "D",
   "堆必须是完全二叉树（最后一层从左往右填）。d 中 13 没有左孩子却有右孩子 9，不完全，所以不是堆。",
   ["合法的堆。", "合法的堆。", "合法的堆。", "不完全，应选。"],
   "B", "下列哪一个不是二叉堆？（见图 a–d）", ["图 a", "图 b", "图 c", "图 d"], fig=["heap_abcd.png"])
mc(8, "parent-0", "If the leftChild and rightChild of a node is calculated by 2i + 1 and 2i + 2, the formula for finding the parent of node i is ______",
   ["(i+2)/2", "i/2", "(i+1)/2", "(i-1)/2"], "D", "根下标为 0 时：左 2i+1、右 2i+2、父 (i−1)/2（整除）。",
   ["不对。", "这是根下标为 1 时的公式。", "不对。", "应选。"], "B", "若节点的左、右孩子按 2i+1、2i+2 计算，节点 i 的父节点公式是 ______。",
   ["(i+2)/2", "i/2", "(i+1)/2", "(i-1)/2"])
mc(8, "parent-1", "If the leftChild and rightChild of a node is calculated by 2i and 2i + 1, the formula for finding the parent of node i is ______",
   ["(i+2)/2", "i/2", "(i+1)/2", "(i-1)/2"], "B", "根下标为 1 时：左 2i、右 2i+1、父 i/2（整除）。",
   ["不对。", "应选。", "不对。", "这是根下标为 0 时的公式。"], "B", "若节点的左、右孩子按 2i、2i+1 计算，节点 i 的父节点公式是 ______。",
   ["(i+2)/2", "i/2", "(i+1)/2", "(i-1)/2"])
mc(8, "heap-del-mc", "In a heap, if a node is deleted, the ______ replaces the deleted node", ["root node", "leftChild", "last node", "rightChild"], "C",
   "用最后一个节点替换，再 down-heap bubbling。", ["不对。", "不对。", "应选。", "不对。"], "B",
   "在堆中删除一个节点后，由 ______ 替换被删节点。", ["根节点", "左孩子", "最后一个节点", "右孩子"])
fb(8, "heap-del", "A node that is deleted from a heap is replaced by ____[1].", ["the last node (then down-heap bubbling)"],
   "保持完全二叉树形状，再下沉恢复堆序。", "A B", "从堆中删除的节点由 ____[1] 替换。")
fb(8, "heap-props", "A heap satisfies two important properties namely, ____[1] and ____[2].", ["relational property (heap-order)", "structural property (complete binary tree)"],
   "关系性质规定父子键的大小关系；结构性质要求是完全二叉树。", "A B", "堆满足两个重要性质：____[1] 和 ____[2]。")
fb(8, "heap-shape", "____[1] property defines the shape of a heap.", ["Structural"], "结构性质（完全二叉树）决定堆的形状。", "A B", "____[1] 性质定义了堆的形状。")
fb(8, "heap-desc", "A heap is best described as ____[1].", ["a binary tree T that stores entries at its positions and satisfies the relational and structural properties"],
   "Goodrich 定义：堆是在各位置存放条目的二叉树，并满足两条性质。", "A B", "堆最好的描述是 ____[1]。")
fb(8, "idx-14-1", "Given that 0 ≤ i ≤ n where the root index i = 1, if a node is at index i = 14,\nthe left child index is ____[1]\nthe right child index is ____[2]\nthe parent index is ____[3]",
   ["28", "29", "7"], "根下标 1：左 2i = 28，右 2i+1 = 29，父 i/2 = 7。", "A B", "根下标为 1，节点在下标 14：左孩子 ____[1]，右孩子 ____[2]，父节点 ____[3]。")
fb(8, "idx-14-0", "Given that 0 ≤ i ≤ n where the root index i = 0, if a node is at index i = 14,\nthe left child index is ____[1]\nthe right child index is ____[2]\nthe parent index is ____[3]",
   ["29", "30", "6"], "根下标 0：左 2i+1 = 29，右 2i+2 = 30，父 (i−1)/2 = 6（整除）。", "A B", "根下标为 0，节点在下标 14：左孩子 ____[1]，右孩子 ____[2]，父节点 ____[3]。")
fb(8, "idx-17-1", "Given that 0 ≤ i ≤ n where the root index i = 1, if a node is at index i = 17,\nthe left child index is ____[1]\nthe right child index is ____[2]\nthe parent index is ____[3]",
   ["34", "35", "8"], "左 34，右 35，父 17/2 = 8（整除）。", "B", "根下标为 1，节点在下标 17：左孩子 ____[1]，右孩子 ____[2]，父节点 ____[3]。")
es(8, "q-vs-pq", "The difference between a queue and a priority queue is ______.", "", "A B", "队列与优先队列的区别是 ______。")

# =====================================================================  L9 哈希
mc(9, "not-hash", "One of the following is not a hashing technique", ["Mid square", "Mean square", "Extraction", "Division"], "B",
   "讲义的四种哈希技术：Division、Extraction、Mid-Square、Folding。没有 Mean square。",
   ["平方取中，是。", "不存在，应选。", "抽取法，是。", "除留余数法，是。"], "A B", "下列哪一个不是哈希技术？", ["平方取中法", "均值平方法", "抽取法", "除法（取模）"])
mc(9, "shift-fold", "For an array size N = 11, the index of the key 1642811509 using Shift Folding is ______", ["10", "11", "3", "9"], "A",
   "按 3 位分段：164 + 281 + 150 + 9 = 604；604 % 11 = 10。",
   ["应选。", "下标范围是 0–10，不可能是 11。", "计算错误。", "计算错误（学长批注曾误标）。"], "A B",
   "数组大小 N = 11，用 Shift Folding 计算键 1642811509 的下标是 ______。", ["10", "11", "3", "9"])
mc(9, "bnd-fold", "For an array size N = 11, the index of the key 123456789 using Boundary Folding is ______", ["7", "3", "6", "4"], "D",
   "Boundary folding：隔一段反转。123 | 456 | 789 → 123 + 654 + 789 = 1566；1566 % 11 = 4。",
   ["计算错误。", "计算错误。", "计算错误。", "应选。"], "A B", "数组大小 N = 11，用 Boundary Folding 计算键 123456789 的下标是 ______。", ["7", "3", "6", "4"])
mc(9, "shift-67-4", "The shift expression 67 >> 4 produces ______", ["1", "2", "4", "8"], "C", "右移 4 位 = 整除 2⁴：67 / 16 = 4。",
   ["不对。", "不对。", "应选。", "这是 67 >> 3。"], "A B", "移位表达式 67 >> 4 的结果是 ______。", ["1", "2", "4", "8"])
mc(9, "shift-67-3", "The shift expression 67 >> 3 produces ______", ["1", "2", "4", "8"], "D", "67 / 8 = 8。",
   ["不对。", "不对。", "这是 67 >> 4。", "应选。"], "B", "移位表达式 67 >> 3 的结果是 ______。", ["1", "2", "4", "8"])
mc(9, "shift-87-4", "The shift expression 87 >> 4 produces ______", ["5", "3", "4", "8"], "A", "87 / 16 = 5。",
   ["应选。", "不对。", "不对。", "不对。"], "A B", "移位表达式 87 >> 4 的结果是 ______。", ["5", "3", "4", "8"])
mc(9, "shift-87-3", "The shift expression 87 >> 3 produces ______", ["5", "10", "4", "8"], "B", "87 / 8 = 10。",
   ["这是 87 >> 4。", "应选。", "不对。", "不对。"], "B", "移位表达式 87 >> 3 的结果是 ______。", ["5", "10", "4", "8"])
mc(9, "dh-expr", "One of the following is the math expression for double hashing", ["(K + j) % N", "(K + j²) % N", "(K + j * (7 – K % 7)) % N", "(K + 1 * 7 – K % 7) % N"], "C",
   "双重哈希：(h(K) + j·h'(K)) % N，其中 h'(K) = 7 − K % 7（PRIME = 7），即 C。",
   ["线性探测。", "二次探测。", "应选。", "只是 j = 1 的特例。"], "B", "下列哪一个是双重哈希的数学表达式？",
   ["(K + j) % N", "(K + j²) % N", "(K + j * (7 – K % 7)) % N", "(K + 1 * 7 – K % 7) % N"],
   note="题库B 原选项 C 印作 (K + j * 7 – K % 7) % N，少了括号：按运算优先级是 K + 7j − K%7，不是双重哈希（例如 N = 11、K = 15、j = 2 时得 6，正确应为 5）。本站补上括号。")
fb(9, "hash-4types", "The four types of hashing techniques are ____[1], ____[2], ____[3] and ____[4].", ["Division", "Extraction", "Mid-Square", "Folding"],
   "Folding 又分 shift folding 和 boundary folding。", "A B", "四种哈希技术是 ____[1]、____[2]、____[3] 和 ____[4]。")
fb(9, "hash-parts", "The two parts of a hash function are ____[1] and ____[2].", ["hash code", "compression function"],
   "讲义 “Parts of a Hash Function”：hash code 把 key 映射成整数，compression function 把整数压到 [0, N−1]。题库A 学长批注写的 perfect / good hash function 是哈希函数的种类，不是两部分。",
   "A B", "哈希函数的两个部分是 ____[1] 和 ____[2]。")
fb(9, "fold-164", "Given that the size of an array N = 11. With the use of\na) Shift Folding technique,\nb) Boundary Folding technique,\ngenerate the index for the key 164281509.\na) ____[1]   b) ____[2]",
   ["8", "8"], "分段 164 | 281 | 509。Shift：164 + 281 + 509 = 954，954 % 11 = 8。Boundary（第二段反转为 182）：164 + 182 + 509 = 855，855 % 11 = 8。",
   "A B", "数组大小 N = 11，分别用 a) Shift Folding、b) Boundary Folding 求键 164281509 的下标：a) ____[1]  b) ____[2]")
fb(9, "dh-89", "Given an array size N = 11 and a PRIME of 7. If the key of an object is 89, and that the primary hash function index is full. Calculate the secondary hash function for the next two indexes in which i = 1, 2.\ni = 1: ____[1]   i = 2: ____[2]",
   ["3", "5"], "h(89) = 89 % 11 = 1；h'(89) = 7 − 89 % 7 = 7 − 5 = 2。i=1：(1 + 1×2) % 11 = 3；i=2：(1 + 2×2) % 11 = 5。",
   "A B", "N = 11，PRIME = 7，键 89 的主哈希位置已满，求 i = 1、2 时的下一个下标：i=1 ____[1]，i=2 ____[2]")
fb(9, "dh-15", "Given an array size N = 11 and a PRIME of 7. If the key of an object is 15, and that the primary hash function index is full. Calculate the secondary hash function for the next two indexes in which i = 1, 2.\ni = 1: ____[1]   i = 2: ____[2]",
   ["10", "5"], "h(15) = 15 % 11 = 4；h'(15) = 7 − 15 % 7 = 7 − 1 = 6。i=1：(4 + 6) % 11 = 10；i=2：(4 + 12) % 11 = 5。",
   "B", "N = 11，PRIME = 7，键 15 的主哈希位置已满，求 i = 1、2 时的下一个下标：i=1 ____[1]，i=2 ____[2]")
es(9, "hash-n20", "Given that the key of array A is length N = 20 and the <k, v> pair of entries to be stored in a bucket array are (1, 4), (42, 7), (39, 3), (4, 14), (2, 21).\n(a) As a code snippet (using the modulo operator), define a function to compute the hash code.\n(b) Using the modulo operator, calculate the index of each entry.\n(c) Using a diagram, demonstrate how you can store the entries in a bucket array.",
   "", "A B M24 K", "数组 A 长度 N = 20，要放入 bucket array 的键值对为 (1,4)、(42,7)、(39,3)、(4,14)、(2,21)。(a) 用取模写一个计算哈希码的函数；(b) 计算每个条目的下标；(c) 画图说明如何放入 bucket array。",
   exam={"M24": "36–38"})
es(9, "hash-n21", "Given that the key of array A of length N = 21 and the pair <k, v> of entries to be stored in a bucket array are (4, 10), (42, 7), (1, 89), (39, 3), (4, 14), (2, 21), (31, 45).\n(31) With a code snippet using modulo operator, write a function to compute the hash codes.\n(32) Using the modulo operator, calculate the index of each entry.\n(33) Using a diagram, demonstrate how you can store the entries which are calculated in a bucket array.",
   "", "F25", "数组 A 长度 N = 21，键值对为 (4,10)、(42,7)、(1,89)、(39,3)、(4,14)、(2,21)、(31,45)。(31) 用取模写哈希函数；(32) 计算各条目下标；(33) 画出 bucket array。",
   exam={"F25": "31–33"})
es(9, "hc-hello", "Given the string s = hello; calculate the hashcode summation using the polynomial rule\n    s0·a^(n−1) + s1·a^(n−2) + … + s(n−2)·a + s(n−1)\nwhere a = 31, and si = charAt(i), and ASCII code as follows: e = 101, h = 104, l = 108, o = 111.\nHint: Detailed steps are important.",
   "", "A M24", "给定字符串 s = hello，用多项式规则 s0·a^(n−1) + … + s(n−1)（a = 31，si = charAt(i)）计算哈希码，写出详细步骤。", exam={"M24": "39"})
es(9, "hc-tops", "Given the string s = tops; calculate the hashcode summation using the polynomial rule\n    s0·a^(n−1) + s1·a^(n−2) + … + s(n−2)·a + s(n−1)\nwhere a = 31, and si = charAt(i), and ASCII code as follows: t: 116, p: 112, s: 115, o: 111.\nHint: Detailed steps are important.",
   "", "F25", "给定字符串 s = tops，用多项式规则（a = 31）计算哈希码，写出详细步骤。", exam={"F25": "34"})
es(9, "hc-three", "Given the strings s = hello world; stop; algorithm — calculate the hashcode summation using the polynomial rule\n    s0·a^(n−1) + s1·a^(n−2) + … + s(n−2)·a + s(n−1)\nwhere a = 31, and si = charAt(i).\nHint: Detailed steps will attract more points.",
   "", "B K", "给定字符串 hello world、stop、algorithm，分别用多项式规则（a = 31）计算哈希码。")
es(9, "lin-probe", "Show the hash table of size 11 after inserting entries with keys 34, 29, 53, 44, 120, 39, 45, and 40 using linear probing.",
   "", "A B", "用线性探测，依次插入键 34、29、53、44、120、39、45、40，画出大小为 11 的哈希表。")
es(9, "probe-algos", "State the algorithm for (a) linear probing, (b) quadratic probing, (c) double hashing.", "", "B",
   "分别写出线性探测、二次探测和双重哈希的算法。")

# =====================================================================  L10 算法分析
tf(10, "bs-between", "If a list is sorted, the best strategy to find a search key that is in-between the first and last element is through a linear search algorithm.", "F",
   "有序表应使用二分查找 O(log n)，线性查找是 O(n)。", "A B", "如果列表已排序，查找位于首尾之间的键的最佳策略是线性查找。")
tf(10, "bs-linear", "If a list is sorted, the best strategy to find a search key is through a linear search.", "F",
   "同上，有序时二分查找更好。", "A B", "如果列表已排序，查找键的最佳策略是线性查找。")
tf(10, "n1-linear", "A search key that is located in index N-1 in a list is faster to retrieve using a linear search algorithm than binary search.", "F",
   "前提是列表有序（二分查找要求有序）：位于最后的元素，线性查找要比较 N 次，二分查找约 log₂N 次，所以说法错误。", "A B", "位于下标 N-1 的键用线性查找比二分查找更快。")
tf(10, "n1-binary", "A search key that is located in index N-1 in a list is faster to retrieve using the binary search than the linear search algorithm.", "T",
   "前提是列表有序（二分查找要求有序）：二分查找约 log₂N 次比较，远少于线性查找的 N 次。", "A B", "位于下标 N-1 的键用二分查找比线性查找更快。")
fb(10, "loglinear", "The O(n log n) time complexity is known as ____[1].", ["log-linear (linearithmic) time complexity"],
   "归并排序、快速排序（平均）都是 O(n log n)。", "A B", "O(n log n) 时间复杂度称为 ____[1]。")
fb(10, "exp-hanoi", "The time complexity O(2ⁿ) is applicable to ____[1] problem.", ["Towers of Hanoi / recursive Fibonacci (exponential time)"],
   "O(2ⁿ) 是指数时间，例如汉诺塔（移动 2ⁿ − 1 次，Lecture 1），以及 Lecture 10 举的递归求 Fibonacci。", "B", "时间复杂度 O(2ⁿ) 适用于 ____[1] 问题。")
fb(10, "exp-sort", "The time complexity O(2ⁿ) is applicable to ____[1] sort.", ["no common sorting algorithm (O(2ⁿ) is exponential, e.g. Towers of Hanoi)"],
   "题库A 版本问的是 “… sort”，学长批注 “not any common”：常见排序都是 O(n²) 或 O(n log n)。", "A", "时间复杂度 O(2ⁿ) 适用于 ____[1] 排序。")
fb(10, "hamilton", "A Hamiltonian cycle is a cycle that visits each ____[1] in the graph exactly once and returns to the ____[2].",
   ["vertex", "starting vertex"], "哈密顿回路经过每个顶点恰好一次并回到起点。", "A B", "哈密顿回路是经过图中每个 ____[1] 恰好一次并回到 ____[2] 的回路。")
fb(10, "log2", "Given that i) n = 16, ii) n = 32, iii) n = 256; the time complexity T(N) = log₂n is ____[1], ____[2], ____[3].",
   ["4", "5", "8"], "2⁴ = 16，2⁵ = 32，2⁸ = 256。", "A B", "当 n = 16、32、256 时，T(N) = log₂n 分别为 ____[1]、____[2]、____[3]。")
fb(10, "8n100", "The time complexity of the expression f(n) = 8n + 100 is ____[1].", ["O(n)"], "忽略常数系数和低阶项。", "A B", "f(n) = 8n + 100 的时间复杂度是 ____[1]。")
fb(10, "nested", "The time complexity of following nested loops is ____[1].\n    for(int i = 1; i < list.length; i++){\n        for(int i = 1; i < list.length; i++){\n        }\n    }",
   ["O(n²)"], "两层各约 n 次。（原题内外层都写 i，实际会编译错误，按两层 n 次理解）", "A B", "下面嵌套循环的时间复杂度是 ____[1]。")
fb(10, "sum-20000", "The sum of the first twenty thousand numbers is ____[1].", ["20000 × 20001 / 2 = 200,010,000"],
   "公式 1 + 2 + … + n = n(n+1)/2。", "A B", "前两万个正整数之和是 ____[1]。")
fb(10, "sum-9000", "The sum of the first nine thousand numbers is ____[1].", ["9000 × 9001 / 2 = 40,504,500"], "公式 n(n+1)/2。", "B", "前九千个正整数之和是 ____[1]。")
es(10, "sum-java", "State the formula, then write a Java algorithm to compute (the sum of) the first five thousand numbers.", "", "A B",
   "写出公式，再用 Java 写一个计算前五千个数之和的算法。")
es(10, "tc-linear", "Given the following code snippet,\n    for (int i = 0; i < n; i++) {\n        k = k + 7;\n    }\nShow in a step-by-step proof that the time complexity is linear.", "", "A B",
   "给定循环（i 从 0 到 n−1，每次 k = k + 7），逐步证明其时间复杂度是线性的。")
es(10, "tc-nn", "Calculate (show the step-by-step proof of) the time complexity of the following operation.\n    for(int i = 0; i < n; i++)\n        for(int j = 0; j < n; j++)\n            int k = k + 1;", "", "A B",
   "计算下面两层 n 次循环的时间复杂度，写出步骤。")
es(10, "tc-n5", "Calculate the time complexity of the following operation.\n    for(int i = 0; i < n; i++)\n        for(int j = 0; j < 5; j++)\n            int k = k + 1;", "", "A B",
   "计算外层 n 次、内层 5 次的循环的时间复杂度。")

# =====================================================================  L11 排序
fb(11, "qs-worst", "The worst case time complexity for the quicksort algorithm is ____[1].", ["O(n²)"],
   "每次 pivot 都选到最大或最小值（例如已排好序的表取第一个元素为 pivot），划分极不平衡。", "B", "快速排序的最坏时间复杂度是 ____[1]。")
for _k, _lst, _src in [("qs-a", "0 3 -1 5 2", "A B"), ("qs-b", "0 -1 3 5 2", "A B"), ("qs-c", "38 81 22 48 13 69 93 14 45 58 79 72", "A B"),
                       ("qs-d", "4 5 2 4 1 3 5 9 3 8 9 7", "A B"), ("qs-e", "5 2 9 3 8 4 0 1 6 7", "B K")]:
    es(11, _k, f"With the partition technique of the quick sort, sort the following list of numbers using every first element as pivot:\n    {_lst}",
       "", _src, f"用快速排序的划分（partition）方法，每次取第一个元素为 pivot，对列表 {_lst} 排序。",
       note="题库原文写成 “partition technique of the selection sort”，按课上的快速排序理解。" if _k != "qs-e" else "课堂板书例题；会考提示：Lecture 11 的 quick sort 会考。")
es(11, "alg-merge", "State the algorithm for MergeSort.", "", "A B", "写出归并排序算法。")
es(11, "alg-quick", "State the algorithm for QuickSort.", "", "A B", "写出快速排序算法。")
es(11, "alg-select", "State the algorithm for SelectionSort.", "", "B", "写出选择排序算法。")
es(11, "alg-insert", "State the algorithm for InsertionSort.", "", "B", "写出插入排序算法。")

# =====================================================================  L13 BST 与 AVL
tf(13, "bst-dup-lt", "The following logical formula\n    ∀ parentNode(n) → leftChild(l) < parentNode(n) ≤ rightChild(r)\nstates the order of relation of nodes in a binary search tree with duplicate elements.", "T",
   "课上定义：左 < 父 ≤ 右，重复元素放到右子树。", "A B", "逻辑式 ∀ parentNode(n) → leftChild(l) < parentNode(n) ≤ rightChild(r) 描述了含重复元素的 BST 中节点的大小关系。")
tf(13, "bst-dup-le", "The following logical formula\n    ∀ parentNode(n) → leftChild(l) ≤ parentNode(n) ≤ rightChild(r)\nstates the order of relation of nodes in a binary search tree with duplicate elements.", "F",
   "按课上（Lecture 14）的定义：左 < 父 ≤ 右，重复元素一律放右子树，左边写 ≤ 与此不符，所以为 False。注意这是定义约定：CLRS 等教材允许两边都用 ≤。另外严格地说，BST 性质要对整棵左右子树成立，而不只是直接孩子。", "B", "逻辑式 ∀ parentNode(n) → leftChild(l) ≤ parentNode(n) ≤ rightChild(r) 描述了含重复元素的 BST 中节点的大小关系。")
mc(13, "bst-prop", "Which of the following satisfies the BST property (in logic formula, the property of the BST is ______)",
   ["∀parent → lChild > Parent ≤ rChild", "∀parent → lChild ≥ Parent ≥ rChild", "∀parent → lChild < Parent ≤ rChild", "∀parent → lChild ≥ Parent ≤ rChild"], "C",
   "BST：左孩子 < 父 ≤ 右孩子。题库B 另一版用 leftChild(u) < parent(x) ≤ rightChild(y) 写法，答案相同。",
   ["左边方向反了。", "左右都反了。", "应选。", "左边方向反了。"], "A B", "下列哪一个满足 BST 性质？",
   ["∀parent → lChild > Parent ≤ rChild", "∀parent → lChild ≥ Parent ≥ rChild", "∀parent → lChild < Parent ≤ rChild", "∀parent → lChild ≥ Parent ≤ rChild"])
mc(13, "use-height", "One of the following uses height(s) for balancing trees.", ["Red-black trees", "Binary search trees", "AVL trees", "Priority heap"], "C",
   "AVL 树用左右子树高度差（平衡因子）判断是否旋转。", ["用颜色。", "普通 BST 不自平衡。", "应选。", "堆不是平衡 BST。"], "A B",
   "下列哪一个用高度来平衡树？", ["红黑树", "二叉搜索树", "AVL 树", "优先堆"])
mc(13, "avl-bf", "In AVL trees, ______ is used to balance a tree.", ["node color", "node balance factor", "node height", "node depth"], "BC",
   "B、C 都对。AVL 每个节点保存高度，由左右子树高度算出平衡因子，平衡因子超出 {−1, 0, 1} 就旋转。平衡因子是直接判据，高度是它的依据；L13-MC02 也把“用高度平衡”的树答作 AVL。",
   ["红黑树用颜色。", "应选。直接决定是否旋转、做哪种旋转。", "应选。节点保存高度，平衡因子由高度算出。", "深度无关。"], "B",
   "在 AVL 树中，______ 用于平衡树。", ["节点颜色", "节点平衡因子", "节点高度", "节点深度"])
fb(13, "bst-rule", "The property (rule) of a binary search tree is stated as ____[1].", ["for any node: leftChild < parent ≤ rightChild"],
   "左子树所有元素小于它，右子树所有元素大于等于它。", "A B", "二叉搜索树的性质（规则）是 ____[1]。")
fb(13, "bst-replace", "A node that is deleted from a binary search tree is replaced by ____[1].",
   ["the rightmost (largest) node of its left subtree; if it has no left child, its parent is linked to its right child"],
   "Lecture 13 的做法：Case 1 无左孩子 → 父节点直接连右孩子；Case 2 有左孩子 → 用左子树最右节点替换。", "A B", "从 BST 中删除的节点由 ____[1] 替换。")
fb(13, "bf-formula", "In an AVL tree, the balance factor formula is given as ____[1].", ["height(rightSubtree) − height(leftSubtree)"],
   "课上主写法 bf = h(right) − h(left)；讲义也提到可以用 left − right。", "A B", "AVL 树中平衡因子的公式是 ____[1]。")
fb(13, "bf-range", "The range of values of the balance factor in an AVL is ____[1].", ["{−1, 0, 1}"], "超出这个范围就要旋转。", "A B", "AVL 中平衡因子的取值范围是 ____[1]。")
fb(13, "avl60", "Given the following AVL tree\ni) The height of the node 100 is ____[1]\nii) Balance factor of node 60 is ____[2]\niii) Because of the balance factor node 60 is ____[3] heavy.",
   ["3", "1", "right"], "AVL 一章按节点数算高度（叶子 = 1）：100 → 67 → 87，高度 3；55 子树高 2。bf(60) = 3 − 2 = 1，bf ≥ +1 为 right-heavy。（BST 一章定义单节点高度 0，若按那个算 height(100) = 2，bf 不变。）",
   "A B", "给定 AVL 树：i) 节点 100 的高度 ____[1]；ii) 节点 60 的平衡因子 ____[2]；iii) 根据平衡因子，节点 60 是 ____[3] heavy。", fig=["avl60.png"])
fb(13, "bst115", "As a BST, if node 115 is deleted what node replaces it?  ____[1]", ["32"],
   "115 有左子树（13 → 20 → 32），左子树最右节点是 32。若用右子树最小节点则是 200，但课上规则是左子树最右。", "A B",
   "作为 BST，若删除节点 115，由哪个节点替换？____[1]", fig=["bst115.png"])
for _k, _fig, _desc, _src in [("trav-60", "bst60.png", "树 1（根 60 的 BST）", "A B"), ("trav-ak", "tree_ak.png", "树 2a（a–k）", "A B"),
                              ("trav-green", "tree_green.png", "树 2b（绿色，根 g）", "A B"), ("trav-7-15", "tree7_15.png", "树 3（根 7，含 15）", "A B"),
                              ("trav-7", "tree7.png", "树 4（根 7，不含 15）", "A B")]:
    es(13, _k, "For the figure, state the\ni) pre-order traversal\nii) post-order traversal\niii) in-order traversal", "", _src,
       f"写出图中{_desc}的前序、后序、中序遍历。", fig=[_fig])
es(13, "bst-search", "State the algorithm for searching for an element in a BST.", "", "A B", "写出在 BST 中查找元素的算法。")
es(13, "bst-del20", "Given the following BST, deleting node 20 rebalances the tree into a new structure. Draw the new structure in the space provided.",
   "", "A B", "给定 BST，删除节点 20 后树会变成新结构，画出新结构。", fig=["bst20.png"])
es(13, "avl78", "Given the following AVL tree, calculate the balance factor of the nodes and perform the appropriate rotation to rebalance the tree.\nNB: Detailed steps will attract marks.",
   "", "A B", "给定 AVL 树，计算各节点平衡因子，并做适当的旋转使树重新平衡，写出详细步骤。", fig=["avl78.png"])
es(13, "avl-build", "Using the following list of elements, construct an AVL tree: a, b, c, d, e, d, f, g, i, j, k, l\nNB: details will attract marks.",
   "", "A B", "用元素 a, b, c, d, e, d, f, g, i, j, k, l 构建 AVL 树，写出过程。")

# =====================================================================  L14 红黑树
tf(14, "rb-black", "In a red black tree, every simple path from a node to a descendant leaf node contains the same number of black nodes.", "T",
   "红黑树性质：从任一节点到其后代叶子（NIL）的每条简单路径上黑节点数相同（black height）。", "A B",
   "在红黑树中，从一个节点到其后代叶子的每条简单路径包含相同数量的黑色节点。")
tf(14, "rb-adjred", "In a red black tree, two adjacent nodes can be red.", "F",
   "红节点的孩子必须是黑色，不能有两个相邻（父子）红节点；出现即违规，需要重新着色或旋转。", "A B", "在红黑树中，两个相邻节点可以都是红色。")
mc(14, "rb-prop", "Which of the following is not correct about the properties of a red black tree.",
   ["Every node is either red or black.", "Every leaf node is red.", "If a node is red, then both of its children are black.", "None  (another version: Every inserted node is always red.)"], "B",
   "叶子（NIL）节点是黑色的。", ["正确性质。", "错误说法，应选。", "正确性质。", "B 是错误说法，所以不是 None；另一版的“插入节点总是红色”也是正确说法。"],
   "A B", "下列关于红黑树性质的说法哪个不正确？", ["每个节点不是红色就是黑色。", "每个叶子节点都是红色。", "若节点是红色，它的两个孩子都是黑色。", "以上都不是（另一版：插入的节点总是红色）"])
mc(14, "rb-notcorrect", "Which of the following is not correct about red black trees.",
   ["Every inserted node is a red node.", "The root node is always a black node.", "If any two consecutive nodes are RED, then there is a violation and the tree is balanced.", "None"], "C",
   "两个连续红节点是违规，树是不平衡（imbalanced）的，要重新着色/旋转。C 说“balanced”是错的。",
   ["正确。", "正确。", "错误说法，应选。", "C 错，所以不是 None。"], "A B",
   "下列关于红黑树的说法哪个不正确？", ["每个插入的节点都是红节点。", "根节点总是黑色。", "若两个连续节点都是红色，则违规且树是平衡的。", "以上都不是"])
mc(14, "rb-samecount", "In a red black tree, every simple path from a node to a descendant leaf node contains the same number of ______ nodes.",
   ["red", "parent", "child", "black"], "D", "black height 相同。", ["不对。", "不对。", "不对。", "应选。"], "B",
   "在红黑树中，从节点到后代叶子的每条简单路径包含相同数量的 ______ 节点。", ["红色", "父", "子", "黑色"])
mc(14, "rb-case2a", "In a RB tree, case 2a is the ______", ["RR", "LL", "RL", "LR"], "D",
   "Lecture 14 编号：Case 1 叔叔红；Case 2(a) LR、Case 2(b) RL（双旋）；Case 3(a) LL、Case 3(b) RR（单旋）。",
   ["Case 3(b)。", "Case 3(a)。", "Case 2(b)。", "Case 2(a)，应选。"], "B", "在红黑树中，case 2a 是 ______。", ["RR", "LL", "RL", "LR"])
mc(14, "rb-rl", "In a RB tree, if we insert node x, and we have a RL case; we then rotate ______", ["g(x)", "p(x)", "u(x)", "x"], "B",
   "RL：先右旋父节点 p，变成 RR，再按 RR 处理（左旋 g）。", ["第二步才旋转 g。", "应选。", "叔叔不旋转。", "不旋转 x。"], "B",
   "在红黑树中插入 x，出现 RL 型时，先旋转 ______。", ["g(x)", "p(x)", "u(x)", "x"])
mc(14, "rb-ll", "In the RB tree LL case, we rotate node ______", ["g", "p", "u", "x"], "A",
   "LL：右旋祖父 g，并交换 g 与 p 的颜色。", ["应选。", "不对。", "不对。", "不对。"], "B", "红黑树 LL 型中，旋转节点 ______。", ["g", "p", "u", "x"])
mc(14, "rb-uncle-red", "In a RB tree, if the uncle u of an inserted node x is red, then do ______",
   ["rotate the tree and swap colors", "swap the colors of g and both of p and u", "swap the colors of g and p", "swap the colors of u and x"], "B",
   "Case 1：p、u 涂黑，g 涂红（若 g 是根再涂黑，否则继续向上检查）。不需要旋转。",
   ["叔叔红时不旋转。", "应选。", "这是旋转后的换色。", "不对。"], "B", "在红黑树中，若插入节点 x 的叔叔 u 是红色，则 ______。",
   ["旋转并换色", "交换 g 与 p、u 两者的颜色", "交换 g 和 p 的颜色", "交换 u 和 x 的颜色"])
mc(14, "rb-rr-black", "In a RB tree, if the uncle u of an inserted node x is black in a RR case, then do ______",
   ["right rotate g and swap colors of g and p", "right rotate g and swap colors of g and u", "left rotate g and swap colors of g and p", "left rotate g and swap colors of g and x"], "C",
   "Case 3(b) RR：左旋 g，交换 g 与 p 的颜色。", ["这是 LL。", "不对。", "应选。", "不对。"], "B",
   "在红黑树中，若插入节点 x 的叔叔 u 是黑色且为 RR 型，则 ______。",
   ["右旋 g，交换 g 与 p 的颜色", "右旋 g，交换 g 与 u 的颜色", "左旋 g，交换 g 与 p 的颜色", "左旋 g，交换 g 与 x 的颜色"])
mc(14, "use-color", "One of the following uses colors for balancing trees.", ["Binary search tree", "AVL", "Heaps", "Red-black trees"], "D",
   "红黑树用节点颜色维持平衡。", ["不自平衡。", "用高度。", "不是平衡 BST。", "应选。"], "A B", "下列哪一个用颜色来平衡树？", ["二叉搜索树", "AVL", "堆", "红黑树"])
fb(14, "rb-insred", "In a red black tree, every inserted node is always ____[1] color.", ["RED"], "新节点先涂红，不改变黑高，再修复可能出现的连续红。", "A B", "在红黑树中，新插入的节点总是 ____[1] 色。")
es(14, "rb-build", "Given the following list 1 2 3 4 5 6 7. Build a Red Black tree that is balanced in black height along any simple path.\nNB: Detailed steps will attract marks.",
   "", "A B", "用 1 2 3 4 5 6 7 依次构建红黑树，使任意简单路径黑高相同，写出详细步骤。")
es(14, "rb-del-a", "Given the following Red Black tree (a). Delete the node 50 and then node 40 (to create a double black). Now, rebalance the tree.\nNB: Detailed steps will attract marks.",
   "", "A B", "给定红黑树 (a)，先删除 50，再删除 40（产生双黑），然后重新平衡。", fig=["rb_a.png"])
es(14, "rb-del-b", "Given the following Red Black tree (b). Delete the node 29 and then node 28 (to create a double black). Now rebalance the tree.\nNB: Detailed steps will attract marks.",
   "", "A B", "给定红黑树 (b)，先删除 29，再删除 28（产生双黑），然后重新平衡。", fig=["rb_b.png"])
es(14, "left-rotate", "Use the Tree Figure to study the algorithm and explain each step in the LEFT-ROTATE algorithm.\n\nLEFT-ROTATE(T, x)\n1  y = x.right\n2  x.right = y.left\n3  if y.left ≠ T.nil\n4      y.left.p = x\n5  y.p = x.p\n6  if x.p == T.nil\n7      T.root = y\n8  elseif x == x.p.left\n9      x.p.left = y\n10 else x.p.right = y\n11 y.left = x\n12 x.p = y",
   "", "A B", "结合图示，逐行解释 LEFT-ROTATE 算法。", fig=["rotate.png"])
es(14, "right-rotate", "Use the Figure (in the LEFT-ROTATE question) and write the RIGHT-ROTATE algorithm and explain each step.", "", "A B",
   "结合同一图示，写出 RIGHT-ROTATE 算法并逐行解释。", fig=["rotate.png"])
es(14, "rb-q21", "Balance the RB tree by showing/explaining the missing details (Ch 43 p.10).\nNB: black ring is BLACK, and green is RED.", "", "B",
   "补全图中空白框，说明这棵红黑树如何一步步恢复平衡（黑圈为黑色，绿色为红色）。", fig=["rb_q21.png"])

# =====================================================================  L2 补充：UML 关系、GenericStack 区别
es(2, "isa-partof", "(a) What is the difference between the is-a relationship and isPartOf relationships in a UML diagram?\n(b) Draw / identify the isPartOf and is-a symbols of relationships as used in a UML.",
   "", "A B", "(a) UML 中 is-a 关系与 isPartOf 关系有什么区别？(b) 画出/指出 UML 中 isPartOf 与 is-a 的符号。")
es(3, "genstack-diff", "State the difference between the reference type GenericStack<T> and the type GenericStack.", "", "A B",
   "说明引用类型 GenericStack<T> 与类型 GenericStack 的区别。")

# =====================================================================  作业 1（AS1 U1–4）与会考补充
es(1, "as1-rec-iter", "Explain which is more efficient between recursive method calls and iterative loops, and why.", "", "AS1",
   "说明递归方法调用和迭代循环哪个更高效，并解释原因。")
es(1, "as1-sum-loop", "Given the expression\n    s = Σ(i=1..4) Σ(j=1..5) 2i²\nwrite the equivalent for loop code.", "", "AS1",
   "给定表达式 s = Σ(i=1..4) Σ(j=1..5) 2i²，写出等价的 for 循环代码。")
es(1, "as1-fib", "Write a program that uses an iterative loop (e.g. for) to compute the Fibonacci series. Test with n = 11, and 100, respectively.",
   "", "AS1", "用迭代循环（例如 for）写程序计算斐波那契数列，分别用 n = 11 和 n = 100 测试。")
es(1, "as1-perm", "(String permutation) Write a recursive method to print all the permutations of a string. For example, for the string abc, the permutations are\n    abc  acb  bac  bca  cab  cba\nHint: define the following two methods; the second is a helper method.\n    public static void displayPermutation(String s)\n    public static void displayPermutation(String s1, String s2)\nThe first method simply invokes displayPermutation(\"\", s). The second method uses a loop to move a character from s2 to s1 and recursively invokes itself with the new s1 and s2. The base case is that s2 is empty: print s1 to the console.\nWrite a test program that prompts the user to enter a string and displays all its permutations.",
   "", "AS1", "（字符串全排列）写一个递归方法，打印字符串的所有排列，例如 abc 的排列为 abc、acb、bac、bca、cab、cba。提示：定义 displayPermutation(String s) 和辅助方法 displayPermutation(String s1, String s2)；前者直接调用 displayPermutation(\"\", s)；后者用循环把 s2 中的一个字符移到 s1，再用新的 s1、s2 递归调用；s2 为空时打印 s1。写测试程序：让用户输入字符串并输出它的所有排列。")
es(3, "as1-gen-product", "With the use of a generic type class, find the product of x = 5.5, and y = 7.7.", "", "AS1",
   "用泛型类求 x = 5.5 与 y = 7.7 的乘积。")
es(4, "as1-array-list", "State\n(a) the differences between an array and the ArrayList class.\n(b) Support your answers with program code and output from your code.", "", "AS1",
   "(a) 说明数组与 ArrayList 类的区别；(b) 用程序代码及其输出来支持你的答案。")
es(6, "hash-class20", "Hashing (using the modulo operator): a hash table of size N = 20 stores the following items in the (k, v) format:\n    (1, 20), (2, 70), (42, 80), (4, 25), (12, 44), (14, 32), (17, 11), (13, 78), (37, 98)\n(a) Compute the hash (array index) of each key with the modulo operator.\n(b) Which entries collide? Show how all entries are stored in the bucket array.",
   "", "K", "哈希（取模）：大小 N = 20 的哈希表要以 (k, v) 形式存入 (1,20)、(2,70)、(42,80)、(4,25)、(12,44)、(14,32)、(17,11)、(13,78)、(37,98)。(a) 用取模算出每个键的下标；(b) 哪些条目冲突？画出所有条目在 bucket array 中的存放方式。",
   note="课堂例题：2024-04-02 会考照片，Lecture 6 课件「Hashing and Hash Table」一页。")
es(11, "qs-last", "With the partition technique of the quick sort, sort the following list of numbers using the last element of every sub-list as pivot:\n    10, 80, 30, 90, 40, 50, 70",
   "", "K", "用快速排序的划分（partition）方法，每次取子表最后一个元素为 pivot，对列表 10, 80, 30, 90, 40, 50, 70 排序。",
   note="课堂例题：2024-05-09 会考照片（Partition around 70 / 80）；会考提示：Lecture 11 的 quick sort 会考。")
