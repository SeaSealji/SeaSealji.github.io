#!/usr/bin/env bash
set -euo pipefail

remote_host="gain-meal-server"
remote_dir="/opt/1panel/apps/openresty/openresty/root/music"
public_base_url="https://119.29.54.234/music"

usage() {
  echo "用法：$0 [--remove-sources] 音频文件..."
  echo "通过 SSH 将音频上传到独立服务器。脚本不会修改、提交或推送 Git 仓库。"
  echo "默认保留源文件；如需在上传成功后删除，请显式传入 --remove-sources。"
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

declare -a uploaded_sources=()
for source in "$@"; do
  if [[ ! -f "$source" ]]; then
    echo "找不到音频文件：$source" >&2
    exit 1
  fi

  filename=$(basename "$source")
  if [[ ! "$filename" =~ ^[A-Za-z0-9._-]+$ ]]; then
    echo "文件名只能包含英文字母、数字、点、下划线和连字符：$filename" >&2
    exit 1
  fi

  temporary_path="/tmp/${filename}.upload"
  scp -- "$source" "$remote_host:$temporary_path"
  ssh "$remote_host" "sudo install -d -m 0755 '$remote_dir' && sudo install -m 0644 '$temporary_path' '$remote_dir/$filename' && rm -f '$temporary_path'"
  uploaded_sources+=("$source")
  echo "已上传：$public_base_url/$filename"
done

if [[ "$remove_sources" == true ]]; then
  for source in "${uploaded_sources[@]}"; do
    rm -f -- "$source"
  done
  echo "已删除上传成功的本地源文件。"
fi

echo "请将上述 HTTPS 地址登记到 data/music.yaml 的 url 字段，然后进行本地预览。"
