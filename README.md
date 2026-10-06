# 个人笔记

Quarto 构建的黑白极简个人网站：首页、博客归档、分类筛选、全文搜索、文章目录、LaTeX 数学公式、PDF 下载，以及 giscus 评论接入。

## 本地使用（Windows / PowerShell）

在此目录打开 PowerShell：

```powershell
.\scripts\build.ps1
.\scripts\preview.ps1
```

打开 http://localhost:4200 。停止预览按 Ctrl+C。

脚本优先使用 `.tools/quarto/bin/quarto.cmd` 中的便携版，否则使用系统 Quarto。其他电脑需从 https://quarto.org/docs/download/ 安装 Quarto。仅写文字和公式无需安装 R、Python 或 TeX。

## 修改网站

| 文件 | 用途 |
| --- | --- |
| `_quarto.yml` | 站名、导航、搜索和页脚 |
| `index.qmd` | 个人首页及最近文章 |
| `about.qmd` | 自我介绍与真实联系方式 |
| `blog.qmd` | 博客归档、分类与过滤 |
| `styles.css` | 黑白视觉样式 |
| `posts/` | 每个目录是一篇文章 |
| `documents/math-notes.qmd` | 示例 PDF 的 Markdown 源文件 |

当前个人介绍为中性的初始文案，文章明确标注为示例；请在上线前换成真实内容。

## 写新文章

新建 `posts/my-first-post/index.qmd`：

```markdown
---
title: "我的第一篇文章"
description: "一两句话介绍文章内容。"
date: "2026-10-06"
categories: [笔记]
---

## 一个问题

正文使用 Markdown。行内公式：$E=mc^2$。

$$
\int_0^1 x^2\,\mathrm{d}x=\frac{1}{3}
$$
```

文章目录名会成为网址，发布后尽量保持稳定，以保留外部链接和评论对应关系。插图放在文章目录，用 `![说明](image.png)` 引用。

## Markdown、LaTeX 与 Typst

- `.qmd` 是带元数据与扩展功能的 Markdown；网页公式使用 LaTeX 数学语法，由 MathJax 渲染，需要访问 MathJax CDN。
- `build.ps1` 先将 `documents/math-notes.qmd` 通过 Quarto 内置 Typst 编译成 PDF，再复制到 `assets/pdf/`。网页下载的是实际文件。
- 任意已有 `.typ` / `.tex` 文档可先自行编译 PDF，放入 `assets/pdf/`，再在文章里链接它。这里没有实现任意 Typst 或 LaTeX 文档到网页的自动转换。
- Typst 模板和 LaTeX 宏包是不同体系；网页公式支持范围也不同于完整 TeX。

## 启用评论

当前评论未启用，文章末尾显示“评论暂未开放”。没有模拟评论或本地留言替代。

1. 在 GitHub 选择一个公开仓库，在 Settings → General → Features 开启 Discussions。
2. 在 https://giscus.app/zh-CN 安装 giscus App，授权该仓库。
3. 在配置页选择仓库与 Announcements 类型的讨论分类，映射选 `pathname`，勾选严格匹配，主题选 light，语言选简体中文。
4. 从生成的脚本复制 `data-repo`、`data-repo-id`、`data-category`、`data-category-id`，运行：

```powershell
.\scripts\set-comments.ps1 -Repo '用户名/仓库名' -RepoId '真实repo-id' -Category '分类名称' -CategoryId '真实category-id'
.\scripts\build.ps1
```

这些 ID 是公开配置，不是密码。读者需 GitHub 账号并授权 giscus 才能评论；评论保存在 Discussions，可在 GitHub 管理。配置完成后，必须在线验证评论的提交与重新加载。

## 发布到 GitHub Pages

1. 创建公开仓库 `easoncyy.github.io`，把本目录源码上传到 `main` 分支（不上传 `.tools/` 与 `_site/`）。
2. 当前发布方式：将生成的网站上传到 `gh-pages` 分支，Pages 使用该分支的根目录。
3. 本地更新文章后运行 `scripts/build.ps1`，再运行 `python scripts/publish-github.py`。需要 GitHub CLI (`gh`) 登录且有仓库写入权限；发布脚本通过 GitHub API 保留 main 历史并更新 gh-pages。
4. 网站地址为 `https://easoncyy.github.io/`，已在 `_quarto.yml` 配置。
5. 需要 RSS 时，在 `blog.qmd` 的 `listing` 下添加 `feed: true`。

仓库地址为 https://github.com/easoncyy/easoncyy.github.io 。已从原 `homepage` 仓库重命名，以使用用户网站的根网址。

`scripts/templates/publish.yml` 是自动构建工作流模板。当前 GitHub OAuth 凭据没有 `workflow` 权限，因此暂不将其放在 `.github/workflows/`。以后授权 workflow 权限并将模板放回该目录、切换 Pages 为 GitHub Actions 后，可以自动从 main 构建和发布。

官方资料：https://quarto.org/docs/websites/website-blog.html 、 https://quarto.org/docs/publishing/github-pages.html 、 https://giscus.app/zh-CN
