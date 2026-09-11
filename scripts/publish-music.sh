#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "用法：$0 [--remove-sources] 音频文件..."
  echo "将一个或多个音频复制到 static/music/，提交并推送，然后让仓库音乐文件不出现在本地工作区。"
  echo "默认不会删除源文件；如需同时清理源文件，请显式传入 --remove-sources。"
}

remove_sources=false
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi
if [[ "${1:-}" == "--remove-sources" ]]; then
  remove_sources=true
  shift
fi
if [[ "$#" -eq 0 ]]; then
  usage >&2
  exit 2
fi

repo_root=$(git rev-parse --show-toplevel)
music_dir="$repo_root/static/music"
mkdir -p "$music_dir"

declare -a copied_files=()
declare -a source_files=()
for source in "$@"; do
  if [[ ! -f "$source" ]]; then
    echo "找不到音频文件：$source" >&2
    exit 1
  fi
  filename=$(basename "$source")
  target="$music_dir/$filename"
  cp -p "$source" "$target"
  copied_files+=("$target")
  source_files+=("$source")
done

echo "已复制 ${#copied_files[@]} 个音频文件。"
echo "请确认 data/music.yaml 中已经登记标题、歌手和 file 路径。"
git add -- static/music data/music.yaml
git commit -m "添加本地音乐"
git push origin main

for target in "${copied_files[@]}"; do
  relative=${target#"$repo_root/"}
  git update-index --skip-worktree -- "$relative"
  rm -f -- "$target"
done

if [[ "$remove_sources" == true ]]; then
  for source in "${source_files[@]}"; do
    rm -f -- "$source"
  done
fi

echo "推送完成，本地工作区已移除音乐文件。"
if [[ "$remove_sources" == false ]]; then
  echo "源文件未删除；如需清理源文件，请自行删除，或下次使用 --remove-sources。"
fi
