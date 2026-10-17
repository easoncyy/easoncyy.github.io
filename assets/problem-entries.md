::: {.problem-day data-date="2026-10-17"}

## 2026-10-17 {.problem-date-heading}

::: {.problem-entry data-problem="{&quot;path&quot;: [&quot;MATH&quot;, &quot;CALCULUS&quot;, &quot;数列与极限&quot;], &quot;tags&quot;: [&quot;次可加性&quot;, &quot;下确界&quot;, &quot;极限&quot;], &quot;title&quot;: &quot;次可加数列与 Fekete 引理&quot;}"}

```{=html}

<div class="problem-meta">MATH / CALCULUS / 数列与极限</div>

<h3>01. 次可加数列与 Fekete 引理</h3>

<div class="entry-tags">#次可加性 · #下确界 · #极限</div>

```

设实数数列 $\{x_n\}_{n\ge1}$ 满足：对任意正整数 $m,n$，

$$
0\le x_{m+n}\le x_m+x_n.
$$

证明 $\displaystyle\lim_{n\to\infty}\frac{x_n}{n}$ 存在，且

$$
\lim_{n\to\infty}\frac{x_n}{n}
=\inf_{k\ge1}\frac{x_k}{k}.
$$

```{=html}

<details class="problem-answer"><summary>answer/ 展开答案</summary><div class="problem-solution">

```

**思路：** 固定一个分块长度 $k$，将 $n$ 写成 $qk+r$。次可加性控制完整的块，有限种余数产生的误差除以 $n$ 后趋于零。

**1. 确定下确界。** 题设直接保证 $x_n\ge0$（$n\ge2$）。同时，由 $0\le x_2\le2x_1$ 可知 $x_1\ge0$。因此

$$
\alpha=\inf_{k\ge1}\frac{x_k}{k}
$$

是有限的非负实数，且对所有 $n\ge1$，$x_n/n\ge\alpha$。

**2. 固定分块长度。** 固定正整数 $k$，对 $n\ge k$，作带余除法

$$
n=qk+r,\qquad q\ge1,\quad0\le r<k.
$$

反复使用次可加性：当 $r>0$ 时，$x_n\le qx_k+x_r$；当 $r=0$ 时，$x_n\le qx_k$。

仅为统一记号，令 $x_0=0$，再记

$$
M_k=\max\{x_0,x_1,\ldots,x_{k-1}\}.
$$

于是两种情形均给出

$$
\alpha\le\frac{x_n}{n}
\le\frac{qx_k}{n}+\frac{M_k}{n}
\le\frac{x_k}{k}+\frac{M_k}{n},
$$

其中最后一步用到了 $qk\le n$ 和 $x_k\ge0$。

**3. 用下确界收束。** 任给 $\varepsilon>0$，由下确界的定义，可选定 $k$ 使

$$
\alpha\le\frac{x_k}{k}<\alpha+\frac\varepsilon2.
$$

固定这个 $k$，再取充分大的 $n$，使 $M_k/n<\varepsilon/2$，便有

$$
0\le\frac{x_n}{n}-\alpha
\le\frac{x_k}{k}-\alpha+\frac{M_k}{n}<\varepsilon.
$$

故 $x_n/n\to\alpha$，即得结论。

这里先选 $k$，再令 $n$ 充分大；不能让分块长度随 $n$ 任意变化。

```{=html}

</div></details>

<p class="problem-source">来源：吉米多维奇数学分析习题集-137题</p>

```

:::

::: {.problem-entry data-problem="{&quot;path&quot;: [&quot;MATH&quot;, &quot;LINEAR-ALGEBRA&quot;, &quot;行列式&quot;], &quot;tags&quot;: [&quot;换元法&quot;, &quot;多项式&quot;, &quot;三角行列式&quot;], &quot;title&quot;: &quot;换元法计算上 a 下 b 的行列式&quot;}"}

```{=html}

<div class="problem-meta">MATH / LINEAR-ALGEBRA / 行列式</div>

<h3>02. 换元法计算上 a 下 b 的行列式</h3>

<div class="entry-tags">#换元法 · #多项式 · #三角行列式</div>

```

设 $a\ne b$，证明

$$
D=\begin{vmatrix}
x_1&a&\cdots&a\\
b&x_2&\cdots&a\\
\vdots&\vdots&\ddots&\vdots\\
b&b&\cdots&x_n
\end{vmatrix}
=\frac{a f(b)-b f(a)}{a-b},
$$

其中

$$
f(t)=\prod_{i=1}^{n}(x_i-t).
$$

```{=html}

<details class="problem-answer"><summary>answer/ 展开答案</summary><div class="problem-solution">

```

**思路：** 给行列式的每个元素加上同一个参数 $t$，得到一个至多一次的多项式；令 $t=-a,-b$，它分别变成下三角、上三角行列式。

令

$$
P(t)=\begin{vmatrix}
x_1+t&a+t&\cdots&a+t\\
b+t&x_2+t&\cdots&a+t\\
\vdots&\vdots&\ddots&\vdots\\
b+t&b+t&\cdots&x_n+t
\end{vmatrix}.
$$

从最后一行向第二行依次作 $R_i\leftarrow R_i-R_{i-1}$。由于按从下往上的顺序操作，减去的都是尚未改变的原行。这些操作不改变行列式，并且使第二行至第 $n$ 行中的参数 $t$ 全部消去。

所以只有第一行含 $t$，按第一行展开可知 $P(t)$ 是关于 $t$ 的至多一次多项式。又 $P(0)=D$，故可写为

$$
P(t)=ct+D.
$$

当 $t=-a$ 时，上三角区域全为零，故

$$
P(-a)=\prod_{i=1}^{n}(x_i-a)=f(a).
$$

当 $t=-b$ 时，下三角区域全为零，故

$$
P(-b)=\prod_{i=1}^{n}(x_i-b)=f(b).
$$

因此

$$
-ac+D=f(a),\qquad -bc+D=f(b).
$$

第二式乘 $a$，第一式乘 $b$，相减消去 $c$，得到

$$
(a-b)D=a f(b)-b f(a).
$$

因为 $a\ne b$，除以 $a-b$ 即得所证公式。

这里应说“至多一次”，因为某些参数下 $c$ 可以为零。

```{=html}

</div></details>

<p class="problem-source">来源：线性代数习题精选精解</p>

```

:::

::: {.problem-entry data-problem="{&quot;path&quot;: [&quot;MATH&quot;, &quot;COMBINATORICS&quot;, &quot;抽屉原理&quot;], &quot;tags&quot;: [&quot;前缀和&quot;, &quot;抽屉原理&quot;], &quot;title&quot;: &quot;A chess master and exactly 21 games&quot;}"}

```{=html}

<div class="problem-meta">MATH / COMBINATORICS / 抽屉原理</div>

<h3>03. A chess master and exactly 21 games</h3>

<div class="entry-tags">#前缀和 · #抽屉原理</div>

```

A chess master who has 11 weeks to prepare for a tournament decides to play at least one game every day, but in order not to tire himself he decides not to play more than 12 games during any one week. Show that there exists a succession of days during which the chess master will have played exactly 21 games.

```{=html}

<details class="problem-answer"><summary>answer/ 展开答案</summary><div class="problem-solution">

```

Let $a_i$ be the total number of games played during the first $i$ days, for $1\le i\le77$.

Since at least one game is played each day,

$$
1\le a_1<a_2<\cdots<a_{77}.
$$

There are $11$ weeks, with at most $12$ games in each week, so

$$
a_{77}\le11\cdot12=132.
$$

Now consider the two lists

$$
a_1,a_2,\ldots,a_{77}
$$

and

$$
a_1+21,a_2+21,\ldots,a_{77}+21.
$$

Together they contain $154$ integer entries, all lying between $1$ and $153$. By the pigeonhole principle, two entries must be equal.

Each list is strictly increasing, so equality cannot occur between two entries from the same list. Hence there exist indices $i,j$ such that

$$
a_i=a_j+21.
$$

Since $a_i>a_j$, we have $i>j$. Consequently, the total number of games played on the consecutive days $j+1,j+2,\ldots,i$ is

$$
a_i-a_j=21,
$$

as required.

```{=html}

</div></details>

<p class="problem-source">来源：Introductory Combinatics</p>

```

:::

```{=html}

<details id="discussion-2026-10-17" class="log-comments problem-discussion" data-comment-term="/problems/2026-10-17/" data-comment-date="2026-10-17" data-comment-title="每日好题 · 2026-10-17">

<summary>discussion/ <span>2026-10-17 · 当日讨论</span></summary>

<div class="log-comments-body"><p class="log-comments-status" aria-live="polite">展开后加载讨论，使用 GitHub 账号分享思路、提问或勘误。</p><div class="log-comments-widget"></div></div>

</details>

```

:::

::: {.problem-day data-date="2026-10-16"}

## 2026-10-16 {.problem-date-heading}

::: {.problem-entry data-problem="{&quot;path&quot;: [&quot;MATH&quot;, &quot;CALCULUS&quot;, &quot;数列与极限&quot;], &quot;tags&quot;: [&quot;反证法&quot;, &quot;阶乘级数&quot;], &quot;title&quot;: &quot;证明 e 是无理数&quot;}"}

```{=html}

<div class="problem-meta">MATH / CALCULUS / 数列与极限</div>

<h3>01. 证明 e 是无理数</h3>

<div class="entry-tags">#反证法 · #阶乘级数</div>

```

证明自然常数 $e$ 是无理数。

```{=html}

<details class="problem-answer"><summary>answer/ 展开答案</summary><div class="problem-solution">

```

**思路：** 沿用博客《吉米多维奇刷题-数列-1》中的证明：利用阶乘级数的余项，构造一个严格介于 $0$ 与 $1$ 之间的整数。

由 $e$ 的阶乘级数展开，对任意正整数 $n$，记

$$
R_n=e-\sum_{k=0}^{n}\frac1{k!}=\sum_{k=n+1}^{\infty}\frac1{k!}.
$$

余项首项为 $1/(n+1)!$，后续相邻项的比值不超过 $1/(n+2)$，且从某项起严格小于它。因此

$$
0<R_n<\frac1{(n+1)!}\sum_{j=0}^{\infty}\frac1{(n+2)^j}
=\frac{n+2}{(n+1)^2n!}<\frac1{n\,n!}.
$$

反设 $e=p/q$，其中 $p,q$ 为正整数。取 $n=q$，两边同乘 $q!q$，得到

$$
0<q!q\,e-\sum_{k=0}^{q}\frac{q!q}{k!}<1.
$$

然而 $q!q\,e=pq!$ 为整数，且当 $0\le k\le q$ 时，$q!q/k!$ 也为整数。因此中间的数是整数，与它严格介于 $0$ 和 $1$ 之间矛盾。

故 $e$ 是无理数。

参考：[本站博客第 72、73 题](/posts/20261009-analysis-array-1/)。

```{=html}

</div></details>

<p class="problem-source">来源：本站博客《吉米多维奇刷题-数列-1》第 72、73 题</p>

```

:::

::: {.problem-entry data-problem="{&quot;path&quot;: [&quot;MATH&quot;, &quot;LINEAR-ALGEBRA&quot;, &quot;行列式&quot;], &quot;tags&quot;: [&quot;拆分法&quot;, &quot;行列式性质&quot;], &quot;title&quot;: &quot;乘积为 1 的四元行列式&quot;}"}

```{=html}

<div class="problem-meta">MATH / LINEAR-ALGEBRA / 行列式</div>

<h3>02. 乘积为 1 的四元行列式</h3>

<div class="entry-tags">#拆分法 · #行列式性质</div>

```

设 $abcd=1$，计算

$$
D=\begin{vmatrix}
a^2+\dfrac1{a^2}&a&\dfrac1a&1\\
b^2+\dfrac1{b^2}&b&\dfrac1b&1\\
c^2+\dfrac1{c^2}&c&\dfrac1c&1\\
d^2+\dfrac1{d^2}&d&\dfrac1d&1
\end{vmatrix}.
$$

```{=html}

<details class="problem-answer"><summary>answer/ 展开答案</summary><div class="problem-solution">

```

**解：** 按第一列的加法拆分，得

$$
D=
\begin{vmatrix}
a^2&a&1/a&1\\
b^2&b&1/b&1\\
c^2&c&1/c&1\\
d^2&d&1/d&1
\end{vmatrix}
+
\begin{vmatrix}
1/a^2&a&1/a&1\\
1/b^2&b&1/b&1\\
1/c^2&c&1/c&1\\
1/d^2&d&1/d&1
\end{vmatrix}.
$$

从第一个行列式的四行分别提出 $a,b,c,d$，得到

$$
D=abcd
\begin{vmatrix}
a&1&1/a^2&1/a\\
b&1&1/b^2&1/b\\
c&1&1/c^2&1/c\\
d&1&1/d^2&1/d
\end{vmatrix}
+
\begin{vmatrix}
1/a^2&a&1/a&1\\
1/b^2&b&1/b&1\\
1/c^2&c&1/c&1\\
1/d^2&d&1/d&1
\end{vmatrix}.
$$

将第二个行列式的列顺序调整为原来的第 $2,4,1,3$ 列：先交换第 $1,2$ 列，再将第 $4$ 列向左交换两次，共交换三次，因此变号。于是

$$
D=(abcd-1)
\begin{vmatrix}
a&1&1/a^2&1/a\\
b&1&1/b^2&1/b\\
c&1&1/c^2&1/c\\
d&1&1/d^2&1/d
\end{vmatrix}
=0.
$$

```{=html}

</div></details>

<p class="problem-source">来源：线性代数习题精选精解</p>

```

:::

::: {.problem-entry data-problem="{&quot;path&quot;: [&quot;MATH&quot;, &quot;COMBINATORICS&quot;, &quot;抽屉原理&quot;], &quot;tags&quot;: [&quot;同余&quot;, &quot;抽屉原理&quot;], &quot;title&quot;: &quot;52 个整数中的和或差&quot;}"}

```{=html}

<div class="problem-meta">MATH / COMBINATORICS / 抽屉原理</div>

<h3>03. 52 个整数中的和或差</h3>

<div class="entry-tags">#同余 · #抽屉原理</div>

```

证明：任给 $52$ 个整数，其中必有两个整数，它们的和或差能被 $100$ 整除。

```{=html}

<details class="problem-answer"><summary>answer/ 展开答案</summary><div class="problem-solution">

```

**思路：** 将模 $100$ 意义下互为相反数的余数放进同一个抽屉。

将模 $100$ 的 $100$ 种余数分成以下 $51$ 组：

$$
\{0\},\quad\{50\},\quad\{1,99\},\quad\{2,98\},\quad\ldots,\quad\{49,51\}.
$$

每个整数按照它除以 $100$ 的非负余数归入对应组。由于有 $52$ 个整数、只有 $51$ 个组，由抽屉原理，至少有两个整数 $u,v$ 被归入同一组。

- 如果两者的余数相同，则 $u-v\equiv0\pmod{100}$，即它们的差能被 $100$ 整除。
- 如果两者的余数不同，则该组必为 $\{r,100-r\}$，从而 $u+v\equiv0\pmod{100}$，即它们的和能被 $100$ 整除。

因此结论成立。整数允许为负数，也允许重复；这里选取的是所给 $52$ 个整数中的两个不同位置。

**补充：为什么是 52？** 取 $0,1,2,\ldots,50$ 这 $51$ 个整数，任意两个不同数的差的绝对值介于 $1$ 与 $50$ 之间，和介于 $1$ 与 $99$ 之间，都不能被 $100$ 整除。因此 $52$ 是保证结论成立的最小数量。

```{=html}

</div></details>

<p class="problem-source">来源：Introductory Combinatics</p>

```

:::

```{=html}

<details id="discussion-2026-10-16" class="log-comments problem-discussion" data-comment-term="/problems/2026-10-16/" data-comment-date="2026-10-16" data-comment-title="每日好题 · 2026-10-16">

<summary>discussion/ <span>2026-10-16 · 当日讨论</span></summary>

<div class="log-comments-body"><p class="log-comments-status" aria-live="polite">展开后加载讨论，使用 GitHub 账号分享思路、提问或勘误。</p><div class="log-comments-widget"></div></div>

</details>

```

:::

```{=html}

<script id="problem-index" type="application/json">{"builtDate": "2026-10-17", "dates": {"2026-10-17": 3, "2026-10-16": 3}}</script>

```
