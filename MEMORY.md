
## 关于 PERTI（柚柚子/老婆）
- 飞书 ID：ou_b555dae0f3710c44d97657ed9ab1d09d
- 身高158cm，体重52kg
- **记忆错误纠正（2026-04-04）**：曾误记为"衣柜品牌方"，实为 LeonWan 的妻子，衣柜需求提出者，小万家群成员。

## 关于肥肥羊（LeonWan/万里扬）
- 身高165cm，体重67kg

## 小红书账号 (2026-03-25)

**账号：** 鱼丸丸啦 | ID: 668406872 | user_id: 5e0f770a0000000001003d8c

**Cookie (需定期刷新)：**
- web_session=0400698f7b3442566ddada15f63b4bb850c1fb
- a1=19d228fe049mbk2ozoda3shslvs2lq
- webId=0361d616916e84b92d2e0a710376ea

**刷新方式：** 每月检查一次有效性，过期需重新扫码登录
**保存位置：** ~/.openclaw/workspace/xhs_cookies.json

**Chrome配置：** ~/.config/google-chrome/Default (已登录态)
**启动命令：** google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome/Default"

---

## Home Assistant (2026-03-26 更新)

**HA Token（永久有效，定期检查）：**
`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4NjAzZGQ3NTQ0Mzc0OWRhYjBhYTZiMTE5ZTQ0ZTM1MiIsImlhdCI6MTc3NDIyMzE4OCwiZXhwIjoyMDg5NTgzMTg4fQ.3nanh3eeg39FVu6Dv0AtKH2JnDcgUtJtMUq6k8C10sg`
⚠️ 如果遇到 401 报错，需要重新在 HA 网页版创建 Long-Lived Access Token

**主卧小米音箱：**
- 型号：xiaomi.wifispeaker.lx06（小爱音箱Pro）
- Entity: `media_player.xiaomi_cn_266211823_lx06`
- Token: `7373475a74304c48344c4d796b6a7467`
- DID: `266211823`
- ⚠️ TTS/播报功能有问题（notify服务底层调用play_media，音箱不支持）
- 临时修复：音箱唤醒 + 云端TTS，或等集成版本更新

**HA 配置路径：** `/home/leonwan/ha/config/`
**HA Token 更新地址：** HA → 用户头像 → Long-Lived Access Tokens

---

## 🛡️ 铁律：内容必须有出处 (2026-03-25)

LeonWan 明确要求，所有内容必须：
1. **有据可查** — 数据、数字、人名、时间必须注明来源
2. **不杜撰** — 不确定就说不知道，绝不凭感觉编造
3. **真实优先** — 宁可不回答，也不要瞎答

这条铁律写入了 SOUL.md，每次启动都会加载。

---

## 投资组合 (2026-04-09 更新)

**总资产约 4035 元：**
- 黄金 ETF：约 1035 元
- 基金（美股为主）：约 3000 元
- PERTI 黄金仓位：约 45%

**每日定投：** 每天 100 元，分散在黄金ETF、鸿利、S&P500、纳斯达克、AI基金
- 2026-04-09 因美伊停火加仓 S&P500 +20元、Nasdaq +20元

**投资理念：**
- 纪律 > 择时（坚持每日定投，不做波段）
- 看好 AI Agent 赛道（未来2-3年核心投资主题）
- 以美股为主，少量黄金

**小红书定投打卡：** Day 115+（2026-04-09）

---

## 系统配置 (2026-04-09 更新)

**Node & npm：**
- nvm node: v24.14.1
- npm global: ~/.npm-global/lib/node_modules/
- npm bin: ~/.npm-global/bin/
- OpenClaw: 2026.4.5（2026-04-09 升级）
- .openclaw 目录大小：约 1.1GB

**资源占用：**
- openclaw-gateway：约 576 MB RAM
- 系统总内存：3.8 GB

**Docker：**
- 配置了阿里云、USTC、腾讯云镜像源
- 跑着 homeassistant 容器（host网络、privileged模式）
- 容器配置：/home/leonwan/ha/config → /config，时区 Asia/Shanghai

**天气服务：**
- wttr.in 已不可用（持续故障）
- 改用 Open-Meteo 作为主数据源

---

## 定时任务 Cron (2026-04-09 更新)

**系统 crontab：**
- 每天 03:00：备份脚本 → ~/.openclaw/logs/backup-cron.log
- 每天 05:00：learnings-promotion.sh（记忆整理）

**OpenClaw cron jobs：**
- 小红书定投早间推送：周一~周五 12:00（已暂停）
- 日报：每天 18:00
- 主动心跳检查：每 3 小时

**已禁用的 cron：**
- 小红书赛道周报（MCP 服务不可用）
- 金价监控 - 每日9点检查（400 报错）

**备份策略：**
- 备份目录：~/openclaw-backups/
- 保留最新 7 份
- 上次成功：2026-04-08 08:18（54MB）

---

## 偏好习惯 (2026-04-09 更新)

**消息偏好：**
- 不喜欢收例行天气推送，除非有变化
- 不喜欢收"运行正常"类状态消息
- 飞书 bot 是主要通知渠道（小万家群 oc_559a42fd644941ab5ffa52c0ff8e3b6b）

**日报偏好：**
- 喜欢深度分析 > 篇幅长度
- 重视：经验教训、值得关注的信号
- 不追求每日全面覆盖

**OpenClaw 使用：**
- 心跳检查：状态检查和消息发送在同一 cycle，可能有竞态条件
- MCP 进程有残留问题，需定期清理

---

## 极空间 NAS（2026-03-28 接入）

**型号**: ZSpace Z4Pro-EQP7
**IP**: 192.168.3.134
**管理后台**: http://192.168.3.134:5050
**SSH 端口**: 10000
**WebDAV 端口**: 5005
**账号**: 18664974664 / Wly19940728

**连接方式**:
```bash
ssh 18664974664@192.168.3.134 -p 10000  # 直连密码方式（备选）
```

⚠️ **SSH公钥认证失败（2026-04-01）**：NAS系统疑似重置，公钥丢失，密码方式也被拒绝。WebDAV正常可用。需在管理后台重新配置SSH公钥或密码登录。

**公钥**: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOId3OiVgbhXXKQ2p0eXEZGgntHW6g+0FnI3xKRhKK3C leonwan@openclaw-server`

**存储**:
- SATA1 (bcache0) 3.7TB — 29%已用，主存储
- SATA2 (bcache1) 3.7TB — 2%已用
- NVMe (n001) 908GB — 5%已用
