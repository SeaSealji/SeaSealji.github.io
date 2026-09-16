# 非洲鸡的小窝

SeaSealji 的个人博客，使用 Hugo 构建，部署到 GitHub Pages。

> Agent 和后续维护者请先阅读 [AGENTS.md](AGENTS.md) 与 [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)。前者记录本地审查后再推送的强制流程和博客写作规范，后者记录项目结构与当前上下文。

## 本地预览

先安装 Hugo Extended，然后在项目目录执行：

```bash
hugo server --bind 127.0.0.1 --port 1313 --disableFastRender
```

打开 <http://localhost:1313/> 即可预览。

需要同时预览草稿时，加上 `-D` 参数。

## 发布到 GitHub Pages

仓库和 GitHub Actions 已经配置完成，不需要再次执行 `git init` 或添加远程仓库。博客内容必须先在本地预览并由用户审查；只有用户明确要求发布或推送后，才执行：

```bash
git status --short
git add -- <本次任务涉及的明确文件>
git commit -m "说明本次改动"
git push origin main
```

不要使用 `git add .`，以免把未审查的文章或其他文件一并提交。推送后等待 GitHub Actions 完成，再访问 <https://seasealji.github.io/>。

以后每次向 `main` 分支推送内容，GitHub Actions 都会自动重新构建并发布。

## 写新文章

```bash
hugo new posts/my-first-post.md
```

新文章默认使用 `draft = false`，先在本地预览。审查通过并收到明确的发布指令后，再提交并推送；未推送前不会影响线上博客。

## 批量添加音乐

将音频文件一次性传给批量脚本。脚本会通过 SSH 上传到独立服务器，不会修改、提交或推送 Git 仓库：

```bash
./scripts/publish-music.sh --remove-sources \
  "/path/to/song-a.flac" \
  "/path/to/song-b.mp3"
```

上传后在 `data/music.yaml` 登记每首歌的 `title`、`artist` 和 `url`。`--remove-sources` 会在上传成功后删除传入的源文件；不使用该参数则保留源文件。

网页播放建议使用 AAC/M4A 等压缩格式，并在文件名中加入版本号（例如 `song-web-v1.m4a`）。服务器会为音频设置长期浏览器缓存，替换内容时应修改版本号。
