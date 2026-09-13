+++
title = "解决 Codex 每次先 Reconnecting 5 次的问题"
slug = "codex-http-streaming-proxy"
date = 2026-09-13T15:55:16+08:00
description = "记录我排查 Codex WebSocket 连接失败、切换到 HTTP 流式响应，并为 Clash 配置本地代理的过程。"
draft = false
categories = ["技术"]
tags = ["Codex", "WebSocket", "HTTP 流式响应", "Clash", "代理配置"]
+++

最近使用 Codex 时，经常要先等待一轮 `Reconnecting… 1/5` 到 `5/5`，之后才开始正常回答。等待本身不算长，但每次打开或开始新任务都重复一次，使用体验很不稳定。

## 先确认问题发生在哪里

我先检查了 Codex 的本地日志。日志里记录的不是普通请求失败，而是连接

```text
wss://chatgpt.com/backend-api/codex/responses
```

出现 `Connection reset by peer` 或 `Connection refused`。失败之后，Codex 会重试 5 次，最后再回退到普通 HTTP 流式请求。也就是说，模型和账号本身都能用，问题集中在 WebSocket 握手这一段。

我本机使用的是 Clash Verge，混合代理端口为 `7897`。检查 Codex app-server 的运行环境时，发现其中没有 `HTTP_PROXY`、`HTTPS_PROXY` 等变量，因此不能假设桌面进程会自动使用 Clash 的系统代理。

## 让 Codex 直接使用 HTTP 流式响应

这次我采用的是一个自定义 provider，保留 Codex 的 ChatGPT 登录认证，但明确关闭 WebSocket：

```toml
model_provider = "openai_http"

[model_providers.openai_http]
name = "OpenAI HTTP streaming"
wire_api = "responses"
requires_openai_auth = true
supports_websockets = false
```

`supports_websockets = false` 的作用是让这个 provider 不再尝试 Responses API 的 WebSocket 传输，直接使用 HTTPS 的流式响应。这样就绕开了每次都失败的 WSS 握手，也不会再先等待五轮重连。

## 给代理环境补上 `.env`

为了让 HTTP 请求，以及以后可能重新启用的 WebSocket，都能明确走 Clash，我又在 `~/.codex/.env` 中加入：

```dotenv
HTTP_PROXY="http://127.0.0.1:7897"
HTTPS_PROXY="http://127.0.0.1:7897"
NO_PROXY="localhost,127.0.0.1,::1"
```

这里的端口采用的是我自己电脑上 Clash 的配置。不同电脑的代理端口可能不同，照着配置时要根据自己电脑上 Clash 显示的实际端口修改。

## 验证结果

配置完成后，我分别做了两次最小请求测试。使用持久化的 HTTP provider 时，请求一次返回 `HTTP_OK`；临时恢复默认 provider 并保留 `.env` 时，代理路径也一次返回 `WS_PROXY_OK`，没有再出现连续重连。

这次排查也让我确认了一件事：界面上看到的“五次重连”不一定代表服务端或模型异常，最好先看日志里的具体传输协议和错误地址。对于本地代理环境，禁用不稳定的 WebSocket，再保留标准 HTTP 代理配置，是一个比较容易回滚的处理方式。

## 总结

现在 Codex 默认走 HTTP 流式响应，Clash 的 `127.0.0.1:7897` 也已经写入 `.env`。原来的 `config.toml` 另有备份，之后如果网络环境改善，可以把 provider 切回默认配置，再继续测试 WebSocket。
