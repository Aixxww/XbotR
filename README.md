# 🤖 XBot - X (Twitter) Automated Interaction & Traffic Funnel
# XBot - X平台自动回复截流与互动系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Playwright](https://img.shields.io/badge/Core-Playwright-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**[ 🇺🇸 English ](#-english-introduction) | [ 🇯🇵 日本語 ](#-日本語の紹介) | [ 🇨🇳 中文说明 ](#-中文项目介绍)**

</div>

---

## <a id="-中文项目介绍"></a>📖 中文项目介绍

**XBot** 是一个基于 Python 和 Playwright 开发的自动化互动工具。它旨在通过模拟真人的浏览和回复行为，帮助用户在 X (Twitter) 平台上筛选高价值推文，进行智能互动（点赞、回复），从而通过“截流”的方式自然增长账号曝光度与关注者。

### 核心原理：漏斗筛选与拟人化

系统采用严格的 **"筛选漏斗" (Funnel Strategy)** 来确保互动的有效性和安全性：

1.  **时间过滤**：仅抓取最近 `N` 小时内的推文（保证热度）。
2.  **热度验证**：点赞数必须高于 `MIN_LIKES`（排除劣质内容）。
3.  **蓝海策略**：评论数必须低于 `MAX_REPLIES`（确保回复能出现在前排，被更多人看到）。
4.  **内容风控**：通过 `BLACKLIST`（黑名单）自动过滤政治、暴力、诈骗等敏感词，保护账号安全。
5.  **拟人操作**：内置随机滚动、随机停留、随机输入延迟，完全模拟真人操作轨迹。

---

### 🚀 快速开始 (Installation)

本项目提供全平台一键安装脚本，无需懂代码即可部署。

#### 1. 克隆项目
```bash
git clone https://github.com/aixxww/XBot-Auto-Reply.git
cd XBot-Auto-Reply
```

#### 2. 运行一键管理脚本 (Mac/Linux)
```bash
chmod +x manager.sh
./manager.sh
```
> **Note:** Windows 用户请直接在 Git Bash 中运行上述命令，或手动运行 `python main.py`

#### 3. 脚本菜单说明
运行 `manager.sh` 后，您将看到如下菜单：
* **[1] 安装与环境配置**：自动安装 Python 依赖 (Playwright, Rich 等) 和浏览器内核。
* **[2] 生成 Cookie**：核心步骤。脚本会引导您粘贴 X.com 的 `auth_token`，生成免登录凭证。
* **[3] 启动任务**：在后台 (Screen) 启动机器人，即使关闭终端也会继续运行。
* **[4] 查看日志**：实时监控机器人的运行状态。

---

### ⚙️ 配置文件说明 (Config.py)

`config.py` 是控制机器人行为的核心。修改参数前请务必阅读以下说明：

| 参数 | 默认值 | 作用与影响 |
| :--- | :--- | :--- |
| `MAX_TIME_HOURS` | `6` | **时效性**：只回复过去 6 小时内的推文。设置太长可能回复到冷门贴。 |
| `MIN_LIKES` | `100` | **最低门槛**：只有点赞超过 100 才会关注。提高此值可只蹭大V热度。 |
| `MAX_REPLIES` | `20` | **抢占前排**：评论超过 20 条就不回了。这是为了确保你的回复在前三行。 |
| `DAILY_LIMIT` | `2400` | **安全熔断**：单日最大回复量。新号建议改为 50-100，避免被封。 |
| `MIN/MAX_SLEEP` | `20-59` | **冷却时间**：每发一条回复后的休息秒数。**切勿设置过低**，否则会被判定为 Bot。 |
| `BLACKLIST` | `[...]` | **黑名单**：包含这些词的推文直接跳过。建议定期更新以规避新型诈骗词。 |

---

### 🧠 语料库与回复逻辑 (Replies)

项目采用 **场景化回复 (Context-Aware Reply)** 机制，定义在 `replies_data.py` 中。
系统会分析推文关键词，自动分类为：
* `manga` (漫画/动漫)
* `art` (插画/艺术)
* `crypto` (加密货币)
* `funny` (搞笑/梗)
* `general` (通用兜底)

**如何添加自定义回复？**
编辑 `replies_data.py`，在 `REPLIES` 字典中添加您想要的句子即可。支持日语、中文、英语混编。

---

### ⚠️ 安全注意事项 (Safety)

1.  **Cookies 隐私**：生成的 `cookies.json` 包含您的登录凭证，**绝对不要**分享给他人或上传到 GitHub。本项目默认的 `.gitignore` 已屏蔽该文件。
2.  **频率控制**：X 平台对自动化行为非常敏感。建议新账号将 `MAX_REPLIES_PER_HOUR` 设置在 10 以下，养号一周后再逐渐增加。
3.  **免责声明**：本项目仅供学习与技术研究使用。开发者不对因使用本工具导致的账号封禁、限制或其他后果负责。请遵守 X 平台的服务条款。

---

## <a id="-english-introduction"></a>🇺🇸 English Introduction

**XBot** is a Python & Playwright-based automation tool designed to interact with tweets organically. It uses a "Traffic Funnel" strategy to like and reply to high-potential tweets, effectively gaining exposure and followers.

### Key Features
* **Smart Filtering**: Only targets tweets within `N` hours with >100 likes and <20 replies (Blue Ocean Strategy).
* **Safety First**: Built-in `BLACKLIST` to avoid political or scam content.
* **Human Simulation**: Random delays, scrolling, and typing emulation to bypass bot detection.

### Quick Start
1.  Run `./manager.sh` in your terminal.
2.  Select **Option 1** to install dependencies.
3.  Select **Option 2** to inject your `auth_token` (Cookie).
4.  Select **Option 3** to start the bot in the background.

---

## <a id="-日本語の紹介"></a>🇯🇵 日本語の紹介

**XBot** は、PythonとPlaywrightを使用したX (旧Twitter) 自動運用ツールです。「自動リプライ」と「いいね」を通じて、インプレッション（表示回数）とフォロワーを効率的に増やします。

### 主な機能
* **厳選フィルタリング**: 直近の投稿かつ、いいね数が多く、リプライが少ない（競合が少ない）ツイートのみを狙い撃ちします。
* **安全性**: 政治的・センシティブな単語を自動で除外するブラックリスト機能を搭載。
* **人間らしい挙動**: ランダムな待機時間やスクロール動作により、Bot判定を回避します。

### 使い方
1.  ターミナルで `./manager.sh` を実行します。
2.  メニュー **[1]** で環境構築を行います。
3.  メニュー **[2]** で `auth_token` を入力し、ログイン状態を保存します。
4.  メニュー **[3]** でBotをバックグラウンド起動します。

---

**Created by @aixxww **