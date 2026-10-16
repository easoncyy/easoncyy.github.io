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

<script id="problem-index" type="application/json">{"builtDate": "2026-10-16", "dates": {"2026-10-16": 3}}</script>

```
