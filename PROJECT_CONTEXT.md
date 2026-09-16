# 项目上下文

这是一份给后续维护者和新任务窗口使用的项目速记。强制工作流与博客写作规范见根目录 `AGENTS.md`。修改前先看这两个文件，再检查 `git status`，不要因为看到未跟踪文件就默认把它们加入提交。

## 项目概况

- 项目：非洲鸡的小窝（SeaSealji 的个人博客）
- 技术栈：Hugo Extended 静态网站，中文站点，原生 HTML 模板 + CSS，无前端框架
- 部署：GitHub Pages，通过 `.github/workflows/hugo.yaml` 在 `main` 分支推送后自动构建部署
- 远程仓库：`git@github.com:SeaSealji/SeaSealji.github.io.git`
- 站点地址：<https://seasealji.github.io/>
- CI 使用的 Hugo 版本：`0.166.0`
- 站点配置：`hugo.toml`

整体视觉是浅米色背景、深墨绿色文字、橙色强调色；支持通过右上角按钮切换深色模式。修改页面时尽量沿用现有 CSS 变量和组件风格。

## 重要目录

| 路径 | 用途 |
| --- | --- |
| `content/` | 页面和文章内容，包括分类页 `_index.md` 与 `content/posts/` 文章 |
| `layouts/` | Hugo 模板；`layouts/_default/list.html` 负责分类/列表页 |
| `layouts/partials/` | 页头、页脚、文章卡片、音乐播放器等可复用模板 |
| `static/css/main.css` | 全站样式 |
| `static/js/main.js` | 主题切换及页面交互 |
| `static/images/recommendations/` | 推荐页本地低清海报 |
| `data/film_recommendations.yaml` | 美剧电影推荐数据 |
| `data/music.yaml` | 音乐播放器曲目数据 |
| `static/music/` | 音乐资源说明和可选封面，不保存音频 |
| `scripts/publish-music.sh` | 通过 SSH 向独立服务器批量上传音乐的脚本 |
| `public/` | Hugo 生成的构建输出，不是主要编辑入口 |

## 美剧电影推荐页

入口分类页：`/categories/美剧电影推荐/`。

推荐内容由 `data/film_recommendations.yaml` 驱动。顶层是剧集集合，每个集合包含：

```yaml
- slug: "series-slug"
  title: "剧集名称"
  kicker: "WATCHLIST · 01—05"
  description: "剧集集合简介"
  items:
    - season: "第一季"
      code: "S01"
      year: "2024"
      title: "剧集 第一季"
      english: "Original Title · Season 1"
      meta: "2024 · 类型"
      description: "本季简介"
      poster: "/images/recommendations/poster.jpg"
      link: "https://example.com/detail"
```

`layouts/_default/list.html` 会在“美剧电影推荐”分类页中遍历这些剧集集合；每个季条目渲染为一张横向卡片，包含海报、简介和外部详情链接。对应样式在 `static/css/main.css` 的 `.recommendation-*` 规则中。

当前已经收录：

- 《怪奇物语》第一至第五季，详情链接为 `https://pomo.mom/1938` 至 `https://pomo.mom/1942`
- 《绝命毒师》第一至第五季，详情链接为 `https://pomo.mom/1809`、`/1810`、`/1811`、`/1813`、`/1814`
- `https://pomo.mom/1812` 当前返回 404，因此没有作为有效季数使用

海报已下载到本地并缩小到约 320px 高的 JPEG，单张约几十 KB，以节省仓库存储和页面加载成本。新增剧集时，先下载并压缩海报，再在 YAML 中填写本地 `poster` 路径；跳转地址填写详情页的完整 HTTPS URL。

## 本地预览与构建

在项目根目录运行：

```bash
hugo server --bind 127.0.0.1 --port 1313 --disableFastRender
```

预览地址：<http://localhost:1313/>。

如需包含草稿：

```bash
hugo server -D --bind 127.0.0.1 --port 1313 --disableFastRender
```

构建检查：

```bash
hugo --gc --minify --baseURL https://seasealji.github.io/
```

Hugo 会监听 `content/`、`data/`、`layouts/`、`static/` 和 `hugo.toml` 的变化并自动刷新预览。不要直接编辑 `public/` 里的生成 HTML 来修复页面。

## 博客创作流程

新博客文章默认使用 `draft = false`，或省略 `draft` 字段，并通过普通 `hugo server` 在本地预览。用户检查并明确表示审查通过、发布或推送后，才完成构建检查、精确暂存、提交和推送。文章在本地处于可发布状态不会影响线上网站；只有推送到 GitHub 后，GitHub Actions 才会部署并显示文章。

用户只给出一段话或零散素材时，文章应尽量简短明确，减少废话，默认按以下主线组织：

1. 原因：为什么要做、遇到了什么问题。
2. 架构或方案：整体组成、流程、关键实现和取舍。
3. 总结：结果、价值和注意事项。

完整的约束以 `AGENTS.md` 为准。

## 发布约定

1. 先运行 `git status --short`，确认改动和未跟踪文件。
2. 只暂存本次任务涉及的明确文件；不要使用 `git add .` 把用户草稿或临时文件一并提交。
3. 运行 `git diff --check`，并进行一次 Hugo 构建检查。
4. 用户明确要求推送时，提交到 `main` 并执行 `git push origin main`。
5. 推送后由 GitHub Actions 自动部署；不要把 `public/` 构建产物当成主要源文件维护。

## 当前工作区注意事项

以下文章在最近检查时是用户已有的未跟踪文件，除非用户明确要求，否则不要修改、删除或加入其他功能提交：

- `content/posts/free-multidevice-document-sync.md`
- `content/posts/paper-reading-prompt.md`

推荐页相关提交已推送到 `main`；后续新增内容应在此基础上单独提交，提交前仍需重新检查工作区状态。
