# 个人笔记

Quarto 构建的黑白极简个人网站：首页、博客归档、分类筛选、全文搜索、文章目录、LaTeX 数学公式、PDF 下载，以及 giscus 评论接入。

## 指令速查表

所有命令在网站目录 `D:\Personal\Homepage` 的 PowerShell 中运行。

| 目的 | 指令 | 说明 |
| --- | --- | --- |
| 进入网站目录 | `cd D:\Personal\Homepage` | 先进入此目录 |
| 一键构建并发布 | `.\scripts\deploy.ps1` | 日常更新用这条；自动合并日志、构建网页、上传源码和网页并触发 Pages 部署；复用已有 PDF |
| 一键发布并重建 PDF | `.\scripts\deploy.ps1 -RebuildPdf` | 修改了 `documents/math-notes.qmd` 时使用 |
| 本地预览 | `.\scripts\preview.ps1` | 打开 `http://localhost:4200`；按 Ctrl+C 停止 |
| 完整构建，不发布 | `.\scripts\build.ps1` | 生成 PDF 与网页到 `_site/` |
| 只构建网页 | `.\scripts\build.ps1 -SkipPdf` | 已有 PDF 时跳过 PDF 编译；缺少 PDF 时仍会补建 |
| 新建文字日志 | `python scripts/new-log.py "今天的记录" --text "正文"` | 自动生成时间戳与日志源文件 |
| 新建带照片、链接的日志 | `python scripts/new-log.py "散步" --text "正文" --photo "D:\Photos\sky.jpg" --url "https://quarto.org/"` | 照片与链接均可选，可同时使用 |
| 查看新建日志参数 | `python scripts/new-log.py --help` | 查看所有选项 |
| 只合并日志 | `python scripts/render-log.py` | 生成合并文件；构建和预览已自动执行，通常无需单独运行 |
| 只上传已构建的网站 | `python scripts/publish-github.py` | 不构建；通常直接用 `deploy.ps1` |
| 登录 GitHub | `gh auth login` | 首次使用或登录失效时执行，账号需有网站仓库写入权限 |
| 查看登录状态 | `gh auth status` | 检查 GitHub CLI 登录 |
| 查看部署状态 | `gh run list --repo easoncyy/easoncyy.github.io --limit 3` | 查看最近的 Pages 部署任务 |
| 配置评论 | `.\scripts\set-comments.ps1 -Repo '用户名/仓库名' -RepoId 'repo-id' -Category '分类名' -CategoryId 'category-id'` | 当前已配置，换评论仓库时才需要 |

新建日志参数：标题是必填的位置参数；`--text` 指定正文，`--photo` 后可跟多个照片路径，`--url` 附带一个链接，`--slug` 指定目录后缀。后续更多链接和图片直接在 `.qmd` 正文中编辑。

日常流程：**写/修改 `.qmd` → 可选本地预览 → `.\scripts\deploy.ps1`**。命令完成表示已经提交发布，Pages 部署还需要短暂等待，可通过上表指令查看进度。

## 本地预览与构建

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
| `projects.qmd` | 项目展示，包含简介、技术标签与 GitHub 链接 |
| `links.qmd` | 友链列表及本站交换友链信息 |
| `log.qmd` | 单页日志流的页面结构 |
| `logs/` | 日志正文；支持目录中的 `index.qmd` 或直接放置 `.qmd` 文件 |
| `styles.css` | 黑白视觉样式 |
| `posts/` | 每个目录是一篇文章 |
| `documents/math-notes.qmd` | 示例 PDF 的 Markdown 源文件 |

当前个人介绍为中性的初始文案，文章明确标注为示例；请在上线前换成真实内容。

导航使用英文目录名与较小的中文说明，`~/notes` 是唯一首页导航入口。栏目标题与文章路径延续目录风格。项目和友链用普通 Markdown 编辑：复制 `projects.qmd` 内的项目区块，或按 `links.qmd` 内注释中的格式添加真实友链。当前展示 RSNA 膝关节 MRI 项目、个人网站，以及 Msmile 的友链。

## 写日志

`log/ 日志` 是单页时间流：每条完整显示文字，可以在同一条里附上多张照片、插入链接。没有类型分类，也没有日志二级页面。支持关键词搜索、照片点击放大，时间戳自动生成，使用 UTC+08:00。

在网站目录打开 PowerShell：

```powershell
python scripts/new-log.py "今天的想法" --text "记下今天的一点收获。"
python scripts/new-log.py "今天出门走了走" --text "傍晚的天空很好看，也读到一个有趣的网站。" --photo "D:\Photos\sky.jpg" --url "https://quarto.org/"
```

照片与链接都可选，能同时附在一条文字里。命令创建 `logs/时间-entry/index.qmd`，照片复制到 `assets/log/`，并自动填写创建时间。打开输出的文件，用 Markdown 继续写完整正文、修改照片说明或添加行内链接。`--slug walk` 可指定目录后缀。

无需手动填写日期：使用命令时自动生成；手工新建文件只写 `title` 和正文也可以，第一次构建会自动写入时间，后续编辑和发布保持原时间。

### 手工新建日志

可以直接创建 `logs/today.qmd`，也可以创建 `logs/today/index.qmd`。文件名用英文、数字和连字符比较方便；每条日志使用不同名称。最简内容如下：

```markdown
---
title: "今天出门走了走"
---

傍晚的天空很好看。

![傍晚的天空](/assets/photos/sky.jpg)

也读到一个[有趣的网站](https://quarto.org/)。
```

手工写日志时，把照片自行放到 `assets/photos/sky.jpg`（需要时创建目录）。正文直接显示在日志页，日期会在首次构建时自动写回源文件；无需手动填 `date` 或 `timestamp`。不要让直接放置的文件和子目录使用同一个名称，以免页面锚点重复。

手工插图请放在 `assets/`，使用 `![说明](/assets/照片文件名.jpg)` 引用。日志源文件只用于合成单页，不生成独立网页。构建前脚本自动把完整正文按时间倒序合并到 `assets/log-entries.md`；请编辑 `logs/` 源文件，不要编辑自动合并文件。

保存后发布：

```powershell
.\scripts\deploy.ps1
```

## 写博客文章

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

已开启网站仓库的 Discussions，并配置 giscus、Announcements 分类、简体中文与浅色主题。若 giscus App 尚未授权仓库，需要访问 https://github.com/apps/giscus 完成安装，仅选择 `easoncyy.github.io` 仓库。

1. 在 GitHub 选择一个公开仓库，在 Settings → General → Features 开启 Discussions。
2. 在 https://giscus.app/zh-CN 安装 giscus App，授权该仓库。
3. 配置使用 Announcements 分类、严格匹配、light 主题和简体中文。代码按规范化后的文章路径映射，目录网址与 `index.html` 共用评论区。
4. 从生成的脚本复制 `data-repo`、`data-repo-id`、`data-category`、`data-category-id`，运行：

```powershell
.\scripts\set-comments.ps1 -Repo '用户名/仓库名' -RepoId '真实repo-id' -Category '分类名称' -CategoryId '真实category-id'
.\scripts\build.ps1
```

这些 ID 是公开配置，不是密码。读者需 GitHub 账号并授权 giscus 才能评论；评论保存在 Discussions，可在 GitHub 管理。首次留言会自动建立文章的讨论。App 安装完成后，需要在文章末尾实际提交留言并刷新，以验证完整流程。

## 发布到 GitHub Pages

1. 创建公开仓库 `easoncyy.github.io`，把本目录源码上传到 `main` 分支（不上传 `.tools/` 与 `_site/`）。
2. 当前发布方式：将生成的网站上传到 `gh-pages` 分支，Pages 使用该分支的根目录。
3. 本地更新文章后运行 `.\scripts\deploy.ps1` 即可完成构建和发布。修改示例 PDF 源文件后使用 `.\scripts\deploy.ps1 -RebuildPdf`。需要 Python、Quarto 与 GitHub CLI (`gh`) 登录且有仓库写入权限；发布脚本通过 GitHub API 保留 main 历史并更新 gh-pages。
4. 网站地址为 `https://easoncyy.github.io/`，已在 `_quarto.yml` 配置。
5. 需要 RSS 时，在 `blog.qmd` 的 `listing` 下添加 `feed: true`。

仓库地址为 https://github.com/easoncyy/easoncyy.github.io 。已从原 `homepage` 仓库重命名，以使用用户网站的根网址。

`scripts/templates/publish.yml` 是自动构建工作流模板。当前 GitHub OAuth 凭据没有 `workflow` 权限，因此暂不将其放在 `.github/workflows/`。以后授权 workflow 权限并将模板放回该目录、切换 Pages 为 GitHub Actions 后，可以自动从 main 构建和发布。

官方资料：https://quarto.org/docs/websites/website-blog.html 、 https://quarto.org/docs/publishing/github-pages.html 、 https://giscus.app/zh-CN
