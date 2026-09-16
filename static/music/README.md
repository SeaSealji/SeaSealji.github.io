# 音乐资源说明

音频文件存放在独立服务器的 `/music/` 目录，GitHub 仓库只在 `data/music.yaml` 中登记歌曲信息和 HTTPS 地址。本目录仅保留说明或体积较小的封面，不再保存音频。

示例：

```yaml
tracks:
  - title: "歌曲名称"
    artist: "音乐人"
    url: "https://119.29.54.234/music/song-name.mp3"
    cover: "music/song-name.jpg"
```

上传工具为 `scripts/publish-music.sh`。网页播放优先使用 AAC/M4A 等压缩格式并通过带版本号的文件名更新缓存；服务器为音频设置一年浏览器缓存。请只上传你有权使用的音频，并确保远程服务器的 HTTPS 与自动续期保持正常。
