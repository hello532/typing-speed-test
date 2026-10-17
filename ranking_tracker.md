# 排名与收录追踪 — typing.rerivo.com

> 2026-10-10 建立。41 页基线。`src/pages.json` 为页面唯一源，本表手动同步。
> 免费工具：Bing `site:` 实查（Bing Webmaster Tools 已连通 IndexNow）；Google 需 GSC（未接入）。

## 收录基线

| 日期 | 引擎 | 查询 | 收录数 | 备注 |
|---|---|---|---|---|
| 2026-10-09 | Bing | `site:typing.rerivo.com` | 21–30 条 | SERP 3 页分页（first=11/21）；cn.bing.com 劫持 RSS 返回无关中文结果，不可用 |

收录率：30/41 ≈ 73%。剩余 11 页为近期新增（certificate / dvorak / one-hand / tutor / learner / trainer / privacy / about 等），已全部经 IndexNow 提交，待抓取。

## 已提交 IndexNow 记录

| 圈次 | 日期 | URL | 返回 |
|---|---|---|---|
| 1–8 | 2026-10-05 ~ 10-08 | 前 28 页分批 | 200 |
| 9 | 2026-10-09 | typing-certificate.html 等 | 200，key 39f4…txt 线上实测匹配 |
| 10 | 2026-10-10 | dvorak-typing.html / one-hand-typing.html | 200 |
| 11 | 2026-10-10 | 全量 41 页（本轮） | 见 IndexNow 提交日志 |

## 排名追踪表

口径：Bing 无登录态实查，取前三页。`—` = 未进入前三页（未收录或排名差）。Google 无 GSC，暂不查。

| 页面 | 目标词 | Bing 排名 | 备注 |
|---|---|---|---|
| index.html | typing speed test | — | 大盘词，竞品极强 |
| wpm-test-online.html | wpm test online | — | |
| words-per-minute-test.html | words per minute test | — | |
| online-typing-test.html | online typing test | — | |
| free-typing-test.html | free typing test | — | |
| 1-minute-typing-test.html | 1 minute typing test | — | |
| 2-minute-typing-test.html | 2 minute typing test | — | |
| 3-minute-typing-test.html | 3 minute typing test | — | |
| 5-minute-typing-test.html | 5 minute typing test | — | |
| 10-minute-typing-test.html | 10 minute typing test | — | |
| 30-second-typing-test.html | 30 second typing test | — | |
| punctuation-typing-test.html | punctuation typing test | — | |
| capital-letter-typing-test.html | capital letter typing test | — | |
| number-typing-test.html | number typing test | — | |
| typing-accuracy-test.html | typing accuracy test | — | |
| easy-typing-test.html | easy typing test | — | |
| keyboard-typing-test.html | keyboard typing test | — | |
| custom-typing-test.html | custom typing test | — | |
| typing-tutorial.html | typing tutorial | — | |
| typing-tutor.html | typing tutor | — | 新页，待收录 |
| learn-to-type.html | learn to type | — | 新页，待收录 |
| learn-to-type-faster.html | learn to type faster | — | |
| typing-trainer.html | typing trainer | — | 新页，待收录 |
| typing-lessons.html | typing lessons | — | |
| typing-practice.html | typing practice | — | |
| typing-tips.html | typing tips | — | |
| touch-typing-test.html | touch typing test | — | |
| typing-games.html | typing games | — | |
| typing-test-game.html | typing test game | — | |
| typing-race.html | typing race | — | |
| english-typing-test.html | english typing test | — | |
| spanish-typing-test.html | spanish typing test | — | |
| chinese-typing-test.html | chinese typing test | — | |
| hindi-typing-test.html | hindi typing test | — | |
| arabic-typing-test.html | arabic typing test | — | |
| typing-tests-in-other-languages.html | typing tests in other languages | — | |
| typing-certificate.html | typing certificate | — | 新页，待收录 |
| dvorak-typing.html | dvorak typing | — | 新页，待收录 |
| one-hand-typing.html | one hand typing | — | 新页，待收录 |
| colemak-typing.html | colemak typing test | — | 新页(Round-2)，待收录 |
| keyboard-layouts.html | keyboard layouts / dvorak vs qwerty | — | 新页(Round-2)，GEO 数据页，待收录 |

> 首次填写时全部为 `—`：站点上线约一周，大盘词竞争激烈，预期 1–3 个月后才进前三页。
> 复查节奏：每 7 天跑一次 Bing `site:` 计数 + 高意图长尾词（如 `1 minute typing test`、`typing certificate`）逐词实查。

## 外链与品牌资产（dofollow 记录）

| 资产 | 状态 | 备注 |
|---|---|---|
| github.com/hello532/typing-speed-test | ✅ dofollow | repo homepage 已设为站点 URL；description 含 34 timed variants（应更新为 41）；13 topics |
| AlternativeTo | ⏳ 待提交 | Cloudflare 挑战 + React 表单，挂用户浏览器提交 |
| X / Twitter @ucool391128 | ✅ 已发 2/5 | 见外链执行包 §2 |

## 下次复查清单

1. Bing `site:typing.rerivo.com` 计数是否从 30 涨到 41。
2. 高意图词逐词查：`typing certificate`、`dvorak typing test`、`one hand typing`、`typing tutor`、`learn to type`。
3. GitHub repo description 更新为 41 variants（目前写 34，落后）。
4. AlternativeTo 提交状态回写。

## Round-3 增量（2026-10-16）

- 页数：49 → **71**（+22 高意图工具页，新增 keyword_matrix §P4/§P5）。
- 新增 URL 已同步 sitemap.xml / llms.txt / llms-full.txt / 页脚枢纽 / 首页内链段。
- 选词依据：Google autosuggest 实测（1350 查询 → 9867 唯一建议）。
- 待复查：2–4 周后查 GSC/Bing 各新页展现与点击，重点看 10 Key、Data Entry、KPH、Paragraph、Interview、Bank/SSC、How fast can I type。
- Provider id: IndexNow key file 39f4fcd69975670c8a24a9ab78838ba9.txt 已在仓库根，提交后需 POST 新 URL。
