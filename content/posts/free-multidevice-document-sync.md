+++
title = "免费的多设备文档同步方案"
date = 2026-09-12T12:00:00+08:00
description = "使用 Obsidian 和 GitHub 私人仓库，实现一套免费的多设备 Markdown 文档同步方案。"
draft = true
categories = ["技术"]
tags = ["Obsidian", "Git", "GitHub", "文档同步"]
+++

我平时使用 Obsidian 管理笔记和文档。它的文件本质上是 Markdown，目录结构清晰，也比较容易和各种 AI 工具、插件配合使用。只是官方 Sync 需要付费，于是我尝试用 GitHub 私人仓库实现一套免费的多设备同步方案。

## 整体思路

把 Obsidian 的 Vault 放进 GitHub 私人仓库，每台设备都保留一份本地副本，通过 Git 拉取和推送最新内容：

```text
设备 A 编辑文档
      ↓
git commit + git push
      ↓
GitHub 私人仓库
      ↓
git pull
      ↓
设备 B 获取最新文档
```

由于 Markdown、配置文件和大多数笔记附件都可以作为普通文件管理，这种方式不需要额外的同步服务器，也不依赖付费服务。

## 实现流程

1. 在 GitHub 创建一个私人仓库。
2. 将现有 Obsidian Vault 初始化为 Git 仓库，并推送到 GitHub。
3. 在其他电脑或设备上克隆这个仓库。
4. 使用 Obsidian 打开克隆后的目录。
5. 安装 Obsidian Git 插件，用它完成 Pull、Commit 和 Push。

日常使用时，可以保持这样的习惯：切换设备前先 Push，开始编辑前先 Pull。这样每台设备都能拿到最新版本，Git 也会保留完整的修改历史，误删内容时还可以回滚恢复。

## 需要注意什么

Git 同步不是实时同步。多台设备同时修改同一个文件时，可能产生冲突，需要手动合并。因此，最好避免在不同设备上同时编辑同一篇文章。

另外，建议不要提交 Obsidian 的临时工作区和缓存文件，例如：

```text
.obsidian/workspace.json
.obsidian/cache
.trash
```

如果知识库中包含很多图片、音频或视频，还需要注意仓库大小。纯文本笔记非常适合使用 Git，但大型二进制文件可以考虑单独存储。

## 总结

GitHub 私人仓库 + Obsidian Git 插件并不能完全替代官方 Sync 的实时体验，但它提供了一种免费、透明、可回溯的同步方式：

- 文档保存在自己的私人仓库中；
- 每次修改都有版本记录；
- 不需要额外购买同步服务；
- Markdown 文件方便备份、迁移和被 AI 工具读取。

对于主要由 Markdown 文件组成的个人知识库来说，这套方案已经足够实用。
