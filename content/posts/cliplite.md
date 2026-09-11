+++
title = "ClipLite：一个轻量的 macOS 剪贴板历史工具"
date = 2026-06-13T23:05:03+08:00
description = "介绍我制作的 ClipLite：一个基于 Swift 和 AppKit 的本地剪贴板历史工具，以及它的功能、适用场景和使用方式。"
draft = false
categories = ["项目"]
tags = ["ClipLite", "Swift", "AppKit", "macOS", "剪贴板", "效率工具"]
+++

## 项目简介

[ClipLite](https://github.com/SeaSealji/ClipLite) 是我制作的一个轻量 macOS 剪贴板历史工具。它使用 Swift 和 AppKit 编写，不依赖 Electron，也不需要额外的后台运行时，主要目标是让最近复制过的内容能够被快速找回。

这个项目的仓库创建于 2026 年 6 月 13 日，因此本文也以 GitHub 仓库创建时间作为发布时间。

ClipLite 常驻在 macOS 菜单栏，不显示 Dock 图标。复制文字或小图片之后，只需要按下 `Command-Shift-V`，就可以在鼠标附近打开历史窗口，点击某一项将它重新复制到剪贴板，并在获得辅助功能权限时自动粘贴回之前使用的应用。

项目地址：[GitHub - SeaSealji/ClipLite](https://github.com/SeaSealji/ClipLite)，也可以直接阅读项目的 [README](https://github.com/SeaSealji/ClipLite#readme)。

## 它解决了什么问题

日常工作里，我们经常会在多个应用之间复制内容：一段命令、一串路径、一张截图、一个临时链接，或者一段刚刚改过又想找回的文字。系统自带剪贴板通常只保留最近的一项内容，一旦复制了新的内容，之前那一项就很难找回。

ClipLite 的思路很直接：在本地保留一小段时间内的剪贴板历史，把“重新复制”这件事变成一次快捷键操作。它不追求复杂的搜索、同步和团队协作功能，而是专注于一个小而明确的使用环节。

## 核心功能

### 全局快捷键快速呼出

按下 `Command-Shift-V`，ClipLite 会打开剪贴板历史窗口。窗口会尽量出现在鼠标附近，并根据当前屏幕边缘自动调整位置，避免被屏幕裁切。

### 支持文字和小图片

历史记录支持剪贴板中的文本和小图片。图片项目会显示缩略图，方便在多张截图之间快速辨认，而不必逐条打开查看。

### 单击选择并自动粘贴

点击历史记录中的某一项后，ClipLite 会将它重新写回系统剪贴板。如果已经授予辅助功能权限，它还会尝试向之前正在使用的应用发送 `Command-V`，完成自动粘贴。

如果没有授予辅助功能权限，ClipLite 仍然可以正常捕获剪贴板，也可以把选中的内容复制回系统剪贴板；这时只需要手动按下 `Command-V` 即可。

### 本地保存，不上传剪贴板内容

ClipLite 的历史记录只保存在本机，不做云端同步，也不会上传或通过网络发送剪贴板内容。当前数据和日志位置如下：

```text
~/Library/Application Support/ClipLite2/history.json
~/Library/Application Support/ClipLite2/run.log
```

隐私说明可以查看项目中的 [PRIVACY.md](https://github.com/SeaSealji/ClipLite/blob/main/docs/PRIVACY.md)。

### 有限的历史保留策略

为了避免剪贴板历史无限增长，ClipLite 设置了明确的边界：

- 最多保留 50 条记录；
- 最长保留最近 6 小时的内容；
- 大于 5 MB 的图片不会被保存；
- 每秒检查一次剪贴板变化；
- 快速连续复制时，会延迟磁盘写入，减少频繁写文件。

这些限制让它更适合作为“最近内容的临时记忆”，而不是长期资料库。

## 技术实现

ClipLite 使用原生 Swift + AppKit 构建，核心逻辑集中在 [Sources/main.swift](https://github.com/SeaSealji/ClipLite/blob/main/Sources/main.swift)。项目没有引入 Electron 或其他后台运行时，安装后就是一个原生 macOS 菜单栏工具。

剪贴板变化通过 `NSPasteboard.changeCount` 判断。只有当变化计数发生改变时，程序才会读取剪贴板内容，这样可以避免无意义地重复读取。窗口打开时，会根据历史条目数量和内容类型调整大小，并将窗口限制在可见屏幕区域内。

项目还提供了 [build.sh](https://github.com/SeaSealji/ClipLite/blob/main/scripts/build.sh)、[install.sh](https://github.com/SeaSealji/ClipLite/blob/main/scripts/install.sh) 和 [uninstall.sh](https://github.com/SeaSealji/ClipLite/blob/main/scripts/uninstall.sh)，用于构建、安装和卸载应用。

## 适用场景

### 开发和调试

开发时经常需要在终端、编辑器、浏览器和文档之间切换。ClipLite 可以保留最近复制过的命令、文件路径、错误日志和代码片段，减少反复切换窗口寻找内容的时间。

### 写作和资料整理

整理资料时，常常会连续复制标题、链接、摘要和引用。剪贴板历史可以暂时保存这些中间内容，让它们不会因为下一次复制而立即消失。

### 设计、截图和视觉工作

对于需要频繁复制颜色值、尺寸、图片或界面文案的工作，缩略图预览比单纯显示文件名更容易识别。5 MB 的图片限制也能避免把大型素材误当成剪贴板记录保存。

### 日常办公

如果一天中经常需要在邮件、表格、聊天窗口和浏览器之间复制信息，ClipLite 可以作为一个小型的临时缓冲区使用。它不需要学习复杂的操作，记住一个快捷键就够了。

## 如何构建和安装

ClipLite 目前是源代码项目，没有预先打包的发布版本。使用前需要 macOS 13 或更高版本，以及 Swift 工具链或 Xcode Command Line Tools。

如果尚未安装命令行工具，可以执行：

```zsh
xcode-select --install
```

然后进入项目目录，执行：

```zsh
./scripts/build.sh
```

构建完成后，应用包会生成在：

```text
build/ClipLite.app
```

也可以直接使用安装脚本：

```zsh
./scripts/install.sh
```

安装脚本会构建应用，将它安装到 `/Applications/ClipLite2.app` 并立即启动。

## 辅助功能权限说明

ClipLite 捕获剪贴板本身不需要辅助功能权限。只有当你希望它在选择历史内容之后，自动回到之前的应用并发送 `Command-V` 时，才需要授予权限。

授权路径是：

```text
系统设置 > 隐私与安全性 > 辅助功能
```

然后添加或启用：

```text
/Applications/ClipLite2.app
```

如果快捷键无法打开窗口，或者只能复制但不能自动粘贴，可以参考项目的 [故障排查文档](https://github.com/SeaSealji/ClipLite/blob/main/docs/TROUBLESHOOTING.md)。

## 这个项目的边界

ClipLite 刻意保持小而简单，因此它也有明确的边界：

- 不提供云同步；
- 不跨设备共享历史；
- 不保存超过 5 MB 的图片；
- 不把剪贴板历史当作长期知识库；
- 暂时没有图形化设置页；
- 暂时没有正式的安装包和版本发布页。

这些限制并不是遗漏，而是项目当前的取舍。剪贴板里可能包含密码、验证码、个人信息和工作资料，默认只在本机短时间保存，反而更容易控制风险。

另外，仓库目前尚未选择开源许可证。项目中的 [LICENSE](https://github.com/SeaSealji/ClipLite/blob/main/LICENSE) 明确说明，在作者补充许可之前，不应复制、修改、分发或使用这份代码。

## 写在最后

ClipLite 是一个功能边界很清楚的小工具：它不试图替代完整的生产力软件，只希望把“刚才复制过的东西去哪了”这个小问题处理得更顺手一些。

对我来说，这个项目也记录了一个很实际的开发过程：从监听剪贴板、注册全局快捷键，到处理窗口位置、图片预览、自动粘贴和权限说明，每个功能都围绕一个具体的使用动作展开。

如果你也需要一个本地、轻量、没有云同步的 macOS 剪贴板历史工具，可以从 [ClipLite 仓库](https://github.com/SeaSealji/ClipLite) 开始了解和构建。
