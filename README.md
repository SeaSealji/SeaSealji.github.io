# 非洲鸡的小窝

SeaSealji 的个人博客，使用 Hugo 构建，部署到 GitHub Pages。

## 本地预览

先安装 Hugo，然后在项目目录执行：

```bash
hugo server -D
```

打开 <http://localhost:1313/> 即可预览。

## 发布到 GitHub Pages

1. 在 GitHub 创建公开仓库：`SeaSealji.github.io`
2. 将本项目推送到该仓库的 `main` 分支：

   ```bash
   git init
   git add .
   git commit -m "初始化 Hugo 博客"
   git branch -M main
   git remote add origin git@github.com:SeaSealji/SeaSealji.github.io.git
   git push -u origin main
   ```

3. 在仓库中打开 **Settings → Pages**，将发布来源设为 **GitHub Actions**。
4. 等待 Actions 完成，访问 <https://seasealji.github.io/>。

以后每次向 `main` 分支推送内容，GitHub Actions 都会自动重新构建并发布。

## 写新文章

```bash
hugo new posts/my-first-post.md
```

编辑文章后，将 front matter 中的 `draft = true` 改成 `draft = false`，然后提交并推送。

## 批量添加音乐

将音频文件一次性传给批量脚本。脚本会复制、提交、推送，并让已推送的音乐文件不保留在本地工作区：

```bash
./scripts/publish-music.sh --remove-sources \
  "/path/to/song-a.flac" \
  "/path/to/song-b.mp3"
```

推送前请先在 `data/music.yaml` 登记每首歌的 `title`、`artist` 和 `file`。`--remove-sources` 会在推送成功后删除传入的源文件；不使用该参数则只清理仓库工作区中的副本。
