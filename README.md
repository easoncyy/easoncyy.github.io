# 个人笔记

Quarto 构建的黑白极简个人网站：首页、博客归档、分类筛选、全文搜索、文章目录、LaTeX 数学公式、PDF 下载，以及 giscus 评论接入。

## 指令速查表

所有命令在网站目录 `D:\Personal\Homepage` 的 PowerShell 中运行。

| 目的 | 指令 | 说明 |
| --- | --- | --- |
| 进入网站目录 | `cd D:\Personal\Homepage` | 先进入此目录 |
| 只提交并推送源码 | `.\scripts\sync.ps1 -Message "修改自我介绍"` | 自动 commit、同步远端历史并 push 到 main；不构建、不部署网页 |
| 一键发布并指定提交说明 | `.\scripts\deploy.ps1 -Message "更新博客"` | 构建 → commit → push → 部署网页 |
| 一键构建并发布 | `.\scripts\deploy.ps1` | 日常更新用这条；自动合并日志、本地构建、推送源码并触发云端构建部署；复用已有 PDF |
| 一键发布并重建 PDF | `.\scripts\deploy.ps1 -RebuildPdf` | 修改了 `documents/math-notes.qmd` 时使用 |
| 本地预览 | `.\scripts\preview.ps1` | 打开 `http://localhost:4200`；按 Ctrl+C 停止 |
| 完整构建，不发布 | `.\scripts\build.ps1` | 生成 PDF 与网页到 `_site/` |
| 只构建网页 | `.\scripts\build.ps1 -SkipPdf` | 已有 PDF 时跳过 PDF 编译；缺少 PDF 时仍会补建 |
| 新建文字日志 | `python scripts/new-log.py "今天的记录" --text "正文"` | 自动生成时间戳与日志源文件 |
| 新建带照片、链接的日志 | `python scripts/new-log.py "散步" --text "正文" --photo "D:\Photos\sky.jpg" --url "https://quarto.org/"` | 照片与链接均可选，可同时使用 |
| 查看新建日志参数 | `python scripts/new-log.py --help` | 查看所有选项 |
| 只合并日志 | `python scripts/render-log.py` | 生成合并文件；构建和预览已自动执行，通常无需单独运行 |
| 重试云端部署 | `python scripts/publish-github.py` | 从已推送的 main 重新构建部署；不上传本地 `_site`，适合源码上传成功但部署失败时使用 |
| 登录 GitHub | `gh auth login` | 首次使用或登录失效时执行，账号需有网站仓库写入权限 |
| 查看登录状态 | `gh auth status` | 检查 GitHub CLI 登录 |
| 检查真实发布权限 | `python scripts/check-github.py` | 使用当前凭据连接仓库 API，区分网络超时、凭据失效与权限不足 |
| Git 推送故障时使用 API | `python scripts/push-github-api.py` | 上传本地提交并逐一验证哈希；同步脚本在 Git push 失败时自动尝试，远端有分叉时停止 |
| 查看部署状态 | `gh run list --repo easoncyy/easoncyy.github.io --limit 3` | 查看最近的 Pages 部署任务 |
| 配置评论 | `.\scripts\set-comments.ps1 -Repo '用户名/仓库名' -RepoId 'repo-id' -Category '分类名' -CategoryId 'category-id'` | 当前已配置，换评论仓库时才需要 |
| 导入 FIP 笔记 | `python scripts/import-fip.py` | 从指定的 Obsidian FIP 文件夹导入 4 篇已选择笔记；重复执行会用原笔记更新网站副本 |
| 指定 FIP 来源 | `python scripts/import-fip.py --source "D:\你的笔记库\AI\FIP"` | 在其他电脑或路径变化时使用 |
| 归档本次作业 | `python scripts/archive-homework.py` | 处理 `临时/` 中此次选定的 5 份作业 PDF；重复执行更新对应副本 |
| 添加 PDF / EPUB 图书 | `python scripts/add-book.py "书名" "D:\Books\book.pdf" --slug my-book --author "作者" --description "简介"` | 复制图书、添加书目，然后运行 `deploy.ps1` 发布 |
| 查看添加图书参数 | `python scripts/add-book.py --help` | 查看所有参数 |
| 只生成图书馆目录 | `python scripts/render-library.py` | 构建和预览自动执行，通常无需单独运行 |

新建日志参数：标题是必填的位置参数；`--text` 指定正文，`--photo` 后可跟多个照片路径，`--url` 附带一个链接，`--slug` 指定目录后缀。后续更多链接和图片直接在 `.qmd` 正文中编辑。

重复执行同样的日志命令时，会提示已有文件并避免再次创建。如确实需要重复记录，可显式添加 `--allow-duplicate`。新建日志只生成本地文件，仍需运行 `deploy.ps1` 才会更新网页；部署任务完成后线上才会显示。

日常流程：**写/修改 `.qmd` → 可选本地预览 → `.\scripts\deploy.ps1`**。发布命令现在自动提交并推送源码；也可以用 `sync.ps1` 单独提交。命令完成表示已经提交发布，Pages 部署还需要短暂等待，可通过上表指令查看进度。Git 冲突或 push 失败会停止后续部署，已完成的本地提交会保留。

如果输出已经显示源码推送成功，但最后网页发布因 TLS/网络错误失败，在项目根目录运行 `python scripts/publish-github.py`（在 `scripts` 目录则用 `python .\publish-github.py`）即可补发，不必重新构建。部署脚本会记录尚未完成的网页提交，断线后核对远端是否实际更新，重试时复用待发布提交。

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
| `library.qmd` | 图书馆页面 |
| `library/catalog.json` | 图书书名、作者、简介、文件格式、路径和添加日期 |
| `assets/library/` | 可公开分享的 PDF / EPUB 图书 |
| `documents/homework-archive.json` | 作业原文件名、统一命名与文章的对应表 |
| `styles.css` | 黑白视觉样式 |
| `posts/` | 每个目录是一篇文章 |
| `documents/math-notes.qmd` | 示例 PDF 的 Markdown 源文件 |

当前个人介绍为中性的初始文案，文章明确标注为示例；请在上线前换成真实内容。

导航使用英文目录名与较小的中文说明，`~/notes` 是唯一首页导航入口。栏目标题与文章路径延续目录风格。项目和友链用普通 Markdown 编辑：复制 `projects.qmd` 内的项目区块，或按 `links.qmd` 内注释中的格式添加真实友链。当前展示 RSNA 膝关节 MRI 项目、个人网站，以及 Msmile 的友链。

## 写日志

每条日志正文下都有默认折叠的 `comments/ 评论`。第一次展开时才加载 giscus；可以分别展开或收起，每条对应独立的 GitHub Discussion。评论按稳定的日志文件名/目录名绑定，发布后请保持名称不变，以免更换对应讨论；修改标题和正文不影响评论。读者需登录 GitHub 才能留言，首次留言会建立讨论。

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

## 课程归档与 Obsidian 工作流程

作业 PDF 统一使用 `2026-课程英文名-w周次-homework.pdf`；跨周作业使用 `w01-w02`。文章目录使用 `YYYYMMDD-课程英文名-w周次-homework`，作业日期采用 PDF 首页的标注日期。原始文件留在 `临时/`，发布副本位于 `assets/pdf/homework/`，博客支持阅读、下载与内嵌 PDF。

FIP 的博客标题采用 `FIP W02 · 枚举与减治` 格式，目录采用 `YYYYMMDD-fip-w02-主题英文名`。文章日期取源 `.md` 的 Windows 创建时间，不取复制进网站的时间。云同步可能重置文件创建时间，这里使用本次读取到的值。

本次导入 W2、W3、W4 的周笔记及 W3 Python 平方运算专题；W1 的 `AI协作规范.md` 是课程规范，未作为个人学习笔记发布。导入只复制内容，保留原文；代码块不执行，Obsidian `![[图片]]` 转换为网页可用的 Markdown 图片，并复制相关图片。

之后继续在 Obsidian 修改这些笔记，更新网站用：

```powershell
python scripts/import-fip.py
.\scripts\deploy.ps1
```

导入不是后台同步。重复导入会覆盖对应的网站文章副本，因此这些文章的正文请在 Obsidian 原笔记中修改。新增周次时，在 `scripts/import-fip.py` 的 `NOTES` 表里添加来源文件、英文目录名和标题。

## 发布 PDF / EPUB 图书

已上架 6 本：文学《Project Hail Mary》、哲学《纯粹理性批判》、历史《叫魂》、教材/法学《经济法理论与实务》、教材/计算机《深入理解计算机系统》、习题/数学《线性代数习题集》。其中《深入理解计算机系统》原版约 344 MB，使用仓库 Release 的下载入口，其余支持在线阅读和下载。

本次临时文件的全部 11 份原件已整理在本地 `archive/2026-10-06-import/`：`books/` 保存规范命名的图书，`homework/` 保存作业，`manifest.json` 记录原文件名、归档路径、大小和 SHA-256。本地归档不随网站上传；对外发布文件位于 `assets/` 或 Release。发布脚本复用仓库中已有的 PDF，不会在每次发布时重复上传相同文件。

添加一本可公开分享的 PDF：

```powershell
python scripts/add-book.py "书名" "D:\Books\book.pdf" --slug my-book --author "作者" --description "一段简介"
.\scripts\deploy.ps1
```

书目会自动出现在 `library/ 图书馆`：PDF 提供在线阅读和下载；EPUB 提供下载，请用电子书阅读器打开。`--slug` 必填，只用小写英文、数字与连字符；`--author` 和 `--description` 可省略。后续改简介直接编辑 `library/catalog.json`，更新文件则替换 `assets/library/` 中对应文件。

### 图书分类

主分类固定为：**文学、哲学、历史、教材、习题、参考书、其他**。只有教材、习题、参考书使用二级学科；学科名按需填写，例如数学、物理、计算机，不另建复杂分类树。网页先按主分类筛选，再显示该分类已有的学科。

| 图书 | 添加参数 |
| --- | --- |
| 文学作品 | `--category 文学` |
| 哲学或历史 | `--category 哲学` 或 `--category 历史` |
| 数学教材 | `--category 教材 --subject 数学` |
| 数学习题集 | `--category 习题 --subject 数学` |
| 计算机参考书 | `--category 参考书 --subject 计算机` |
| 其他 | `--category 其他`（省略分类时的默认值） |

完整示例：

```powershell
python scripts/add-book.py "微积分教材" "D:\Books\calculus.pdf" --slug calculus --category 教材 --subject 数学 --author "作者"
.\scripts\deploy.ps1
```

教材、习题、参考书添加时必须指定 `--subject`。以后调整分类，在 `library/catalog.json` 修改 `category` 和 `subject`；普通分类的 `subject` 留空。已有未填写分类的书目归入其他；学术分类若手工遗漏学科，网页显示未分学科。相同学科使用一致名称，避免“计算机”和“计算机科学”分成两个筛选项。

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
2. 当前发布方式：从 main 源码触发 GitHub Actions 构建，再通过 Pages artifact 部署。
3. 本地更新文章后运行 `.\scripts\deploy.ps1` 即可完成构建、Git commit、push 和网页发布。修改示例 PDF 源文件后使用 `.\scripts\deploy.ps1 -RebuildPdf`。需要 Git、Python、Quarto 与 GitHub CLI (`gh`) 登录且有仓库写入权限；源码通过 Git（失败时使用 Git API）推送到 main，再触发 GitHub Actions 构建部署。
4. 网站地址为 `https://easoncyy.github.io/`，已在 `_quarto.yml` 配置。
5. 需要 RSS 时，在 `blog.qmd` 的 `listing` 下添加 `feed: true`。

仓库地址为 https://github.com/easoncyy/easoncyy.github.io 。已从原 `homepage` 仓库重命名，以使用用户网站的根网址。

`scripts/templates/publish.yml` 是自动构建工作流模板。当前 GitHub OAuth 凭据没有 `workflow` 权限，因此暂不将其放在 `.github/workflows/`。以后授权 workflow 权限并将模板放回该目录、切换 Pages 为 GitHub Actions 后，可以自动从 main 构建和发布。

官方资料：https://quarto.org/docs/websites/website-blog.html 、 https://quarto.org/docs/publishing/github-pages.html 、 https://giscus.app/zh-CN

## 博客目录与标签

文章开头 YAML 的 `category-path` 是从一级到末级的目录；`categories` 沿用 Quarto 字段名，但现在只表示独立标签。目录不限层级，新增一级名称也会自动出现在筛选器中。没有填写目录时归入 OTHER。

```yaml
category-path: [MATH, CALCULUS, 习题]
categories: [习题, 考前复习]
```

目录选择会包含所有下级文章。回到 `~/notes/blog` 后选择 `#习题`，即可跨学科找所有习题文章；目录、标签和文字搜索也可以组合使用。每页显示 10 篇，按发布时间倒序。现有文章及 FIP/作业导入脚本已经迁移到此格式。

博客目录生成使用 PyYAML（当前电脑已安装）；换电脑后运行 `python -m pip install -r requirements.txt`。

## 正在阅读与书单

公开书单保存在 `library/reading.json`，可以有多份命名书单。未列入书单的图书仍留在普通书架。所有 `reading` 条目会自动显示在图书馆顶端；三种状态是 `reading`（正在阅读）、`planned`（计划阅读）、`completed`（完成阅读）。

| 目的 | 命令 |
| --- | --- |
| 加入正在阅读 | `python scripts/set-reading.py critique-of-pure-reason --status reading --note "阅读第一部分"` |
| 加入计划阅读 | `python scripts/set-reading.py project-hail-mary --status planned` |
| 标记完成 | `python scripts/set-reading.py project-hail-mary --status completed` |
| 创建另一份书单 | `python scripts/set-reading.py computer-systems --list computer-science --title "计算机学习" --status planned` |
| 从书单移除 | `python scripts/set-reading.py computer-systems --list computer-science --remove` |
| 发布更新 | `.\scripts\deploy.ps1 -Message "更新书单"` |

第一个参数是 `library/catalog.json` 中的 `slug`，不是 PDF 文件名。省略 `--list` 时使用 personal 书单；省略 `--note` 会保留之前的备注。

也可以直接编辑 JSON。下面只是格式示例，并不表示你已在阅读这些书：

```json
{
  "lists": [
    {
      "id": "personal",
      "title": "我的书单",
      "items": [
        {"id": "kant", "book": "critique-of-pure-reason", "status": "reading", "note": "阅读第一部分"},
        {"id": "another-book", "title": "没有 PDF 的书也能加入", "url": "https://example.com/", "status": "planned"}
      ]
    }
  ]
}
```

同一书单内每条 `id` 必须唯一。`book` 引用现有图书；未收录的图书可填写 `title`、可选的 `author` 和 `url`，不必上传 PDF。书单与“正在阅读”卡片均以普通书名展示，不带链接、复选框，访客无法修改。图书下载入口位于下方图书分类区。阅读状态只通过上面的后台命令或 JSON 修改后发布。

### 添加 EPUB

与 PDF 使用同一条命令，文件扩展名会自动识别，分类和书单功能均可复用：

```powershell
python scripts/add-book.py "书名" "D:\Books\book.epub" --slug my-epub-book --author "作者" --category 文学
.\scripts\deploy.ps1 -Message "添加 EPUB 图书"
```

上传脚本会检查 EPUB 容器及格式标识，并保留 `.epub` 扩展名。单文件上限仍为 95 MB。EPUB 当前提供下载，不内置网页阅读器。旧 PDF 书目无需修改；新书目自动记录 `format` 字段。

### 手动新增作业时的 PDF 路径

文件放入 `assets/pdf/homework/` 后，文章里的阅读、下载和 iframe 地址都使用以 `/` 开头的网站路径，例如 `/assets/pdf/homework/2026-linear-algebra-w05-homework.pdf`。不要使用 `D:\...`、反斜杠或不带开头 `/` 的 `assets/...`：文章在多级目录下，后一种相对地址会指向文章自己的子目录，导致 404。

## 每日好题 problems/ 与本地 GUI

**双击仓库根目录 `manage-site.cmd` 打开“网站管理”窗口。** 无需每次输入命令。需要本机 Python（含 Tkinter）和 `requirements.txt` 中的 PyYAML；当前电脑已具备。窗口只在本机运行，不开放网站后台登录入口，不保存 GitHub 密钥。

### 日常更新流程

1. **题库编辑**：新建或选择题目，填写标题、分类目录（如 `MATH/LINEAR-ALGEBRA/矩阵`）、逗号分隔标签、题目正文和答案。支持 Markdown 与 `$...$`、`$$...$$` 公式。保存到本地。
2. **每日排期**：输入 `YYYY-MM-DD`，载入该日；从题库多选，加入当天，可上移、下移或移除。选择几道就发布几道，没有固定数量。
3. **保存当天排期**，再到“构建与发布”点击“构建并发布网站”。发布会提交仓库全部修改，操作前窗口会提醒。
4. 未来日期的题目会留在题库和排期中，网页构建只收录北京时间当天及以前的内容。发布一次即可同步未来安排；电脑关闭后仍由 GitHub Actions 每天 **北京时间 00:05** 自动构建和部署。
5. GitHub 定时任务不是精确计时服务，可能延迟；公开仓库长期无活动时计划任务可能被 GitHub 停用。可在 Actions 页面手动运行 `Publish website and scheduled problems`，勾选 rebuild 从源码重新构建。

GUI 还支持新建日志（多图）、修改图书阅读状态、本地 HTTP 预览、查看部署状态和一键发布。博客正文仍用编辑器修改 `.qmd`，窗口提供文件夹入口。构建或发布期间不能保存修改，防止发布内容不一致；文件覆盖前的本地备份保存在忽略上传的 `tmp/manager-backups/`。

### 页面行为

- 上方展示所选日期的题目；初次打开优先今天，今天没有题则显示最近一期。
- 每道题的答案默认折叠，切换日期会重新收起。
- 下方月历支持前后翻月、回到今天，带数量的日期可查看历史题目。
- 分类支持任意层级，标签独立，可跨分类筛选；筛选只影响当前日期题目。
- 可分享日期链接：`/problems.html?date=2026-10-16`。
- 未排期和未来日期的题目不会进入网页资源或站内搜索；**本仓库公开，题库源文件仍可在 GitHub 中查看，排期不是保密措施**。

### 文件格式与扩展

题目保存在 `problems/bank/题目ID.qmd`。ID 使用小写英文、数字和连字符，发布后尽量保持稳定。正文与答案之间用 `<!-- answer -->` 分隔：

```markdown
---
title: "题目标题"
category-path: [MATH, LINEAR-ALGEBRA, 矩阵]
tags: [习题, 基础]
source: "可选的题目出处"
draft: false
---

在这里写题目，例如 $Ax=0$。

<!-- answer -->

在这里写答案与解析。
```

`problems/schedule.json` 将日期映射到题目 ID 列表，顺序即网页顺序：

```json
{
  "2026-10-16": ["linear-algebra-nullspace"],
  "2026-10-17": ["linear-algebra-nullspace"]
}
```

同一道题可跨日安排，同日不能重复。草稿不能排期；错误引用、无效日期和缺少答案会阻止构建。示例题已清理，可通过管理器添加自己的正式题目。

| 目的 | 操作或命令 |
| --- | --- |
| 打开管理窗口 | 双击 `manage-site.cmd` |
| 生成题目页面包含文件 | `python scripts/render-problems.py`（构建自动执行） |
| 预览与发布 | GUI“构建与发布”，或继续使用原 `preview.ps1` / `deploy.ps1` |
| 更改定时任务时间 | 编辑 `.github/workflows/publish-pages.yml` 的 schedule；默认 UTC 16:05 对应次日北京时间 00:05 |

### 部署方式

Pages 使用 GitHub Actions。本地发布推送源码后触发 main 的云端构建，不再通过 Git API 整批上传 `_site`；定时任务从 `main` 重新构建当天页面并通过官方 Pages artifact 部署。不需要另外提供 PAT 或将凭据放到网页里。部署环境允许 `main` 分支运行；原分支规则保留。原有命令保持可用，`deploy.ps1` 完成表示已提交部署任务，最终状态以 Actions 为准。

### 图书馆 GUI（独立栏目）

打开管理窗口的“图书馆”页：左侧显示书架，可搜索书名、作者、分类，并按阅读状态筛选。右侧分为“书目信息与文件”和“书单与阅读状态”。

- **添加图书**：点击“＋ 添加书目”→“选择 / 替换文件”选 PDF/EPUB → 填写书名、作者、分类、可选学科与简介 →“保存书目到本地”。文件会复制到 `assets/library/`，原件保留。
- **编辑书目**：选择左侧图书，修改右侧字段后保存。已存在的 ID 固定，避免破坏书单引用。
- **修改阅读状态**：选中图书，进入“书单与阅读状态”，选择书单、状态，填写备注并保存。选“未加入书单”会从当前书单移除，不删除图书。
- **建立另一份书单**：输入新的英文书单 ID 和名称，再为图书保存状态。
- **替换图书文件**：选中图书，选择新的 PDF/EPUB 后保存；覆盖的文件会备份到 `tmp/manager-backups/`。
- **大文件**：本地导入上限为 95 MB。更大的图书需先上传 GitHub Release，再在新书目中填写外部文件链接与格式。
- 保存只修改本地，最后在“构建与发布”中构建预览或发布网站。

所有演示题和初始示例题均已移入本地回收站，对应排期已清理。

### 题目状态、草稿与删除

题库左侧分开显示两类信息：

| 内容状态 | 含义 |
| --- | --- |
| 草稿 | 尚未准备好。允许题目或答案未写完；不能加入排期，不会进入网页 |
| 可排期 | 已取消草稿并保存，题目和答案完整；可以加入任意日期的排期 |

勾选“草稿”后要点击“保存题目到本地”才生效。写完后取消勾选并保存，再到“每日排期”安排日期。已有排期的题目需先从各日期中移除，才能改回草稿。草稿只影响网页发布，本仓库公开，已推送的草稿源码仍可被访问。

| 排期情况 | 含义 |
| --- | --- |
| 未排期 | 尚未分配日期，不会展示在每日好题中 |
| 待发布 | 只安排在未来日期，云端到期构建时才会展示 |
| 已到期 | 至少一个安排日期已到达；需要构建部署后才会在网上显示，不等于已确认上线 |
| 已到期/待发布 | 同一道题有历史或当天排期，也有未来排期 |

删除：选择左侧题目 →“删除题目”→确认。题目移动到忽略上传的 `archive/problem-trash/`，所有日期的引用同时移除，不会直接永久删除。重新发布后线上内容才会移除。恢复：点击“从回收站恢复”，进入对应日期文件夹选择 `.qmd`；恢复题库内容，但不自动恢复旧排期，避免意外重新发布。同 ID 已存在时不会覆盖。

### 题库与排期页同步

题库编辑和每日排期共用题库、排期文件及同一套状态计算，两页同时显示内容状态、排期情况、已保存日期。草稿只显示在题库编辑列表；保存为可排期后才会进入排期页。保存当天排期后，两页立即刷新。“未保存调整”只留在当天题目编辑区，不会伪装成已保存排期；底部会提示保存后同步。

### 每日自动构建的范围

00:05 的定时工作流会读取 GitHub **main 分支**，重新构建并发布整个网站，不仅是每日好题。所以已推送的博客、日志、图书馆和其他页面改动也会一起上线；只保存在本机、尚未推送的文件不会被云端读取。只运行源码同步（sync）也会让改动进入下一次自动部署。博客可使用 Quarto 的 `draft: true` 暂存；当前日志合并脚本不识别日志草稿标记，不要把未准备公开的日志推送到 main。
