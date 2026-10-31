# Round 21 — 5 个高曝光低点击页的标题/描述重写（2026-10-31）

数据源：GSC 90 天（coolun337@gmail.com）。本轮只动这 5 页的 `<title>`/`<meta description>`、
与 title 主题不一致的 `<h1>`、以及首页正文内链；**不动**首页 title/描述（首页 CTR 26.8%）。

## 1. 为什么是这 5 页

| 页面 | 点击 / 曝光 | CTR | 相关零点击查询 |
|---|---|---|---|
| `/1-minute-typing-test.html` | 2 / 802 | 0.25% | `one minute typing test` 19 曝光 1 点击 |
| `/words-per-minute-test.html` | 1 / 465 | 0.22% | `wpm` 87 曝光 1 点击 |
| `/typing-practice.html` | 5 / 424 | 1.18% | `online typing practice` 83 曝光 **0 点击** |
| `/best-typing-test-online.html` | 1 / 125 | 0.80% | — |
| `/learn-to-type.html` | 1 / 106 | 0.94% | `typing tutorial` 18 曝光 1 点击 |

全站 121 页有曝光、总 CTR 约 1%，所以这 5 页不是「顺便」，是曝光面里最集中的一块。

## 2. 改法：把页面上**已经有**的东西提到最前面

原则：描述里出现的每个卖点，都能在页面上点到实物（计时器、模式按钮、结果面板、无注册）。
不新增能力，不借用别的页的能力。

| 页面 | 新 title | 新 description | 依据（页面实物） |
|---|---|---|---|
| 1-minute | `1 Minute Typing Test: 60-Second Timer, Instant WPM Score` | `Free 1 minute typing test: a live 60-second countdown, instant WPM and accuracy, no sign up, no ads in the typing area. Sentences, quotes or numbers.` | `sTime` 倒计时、结果面板、chips 四模式、无注册 |
| wpm | `WPM Test — Words Per Minute Typing Test, Instant Result` | `Take a free WPM test and get your words per minute instantly, scored as 5 characters per word. Pick 15 seconds to 10 minutes. No sign up, CPM shown too.` | 每轮即时 WPM、结果面板同时给 CPM、15s–10min |
| typing-practice | `Online Typing Practice — Free Drills, 15s to 10 Minutes` | `Free online typing practice with timed drills from 15 seconds to 10 minutes: sentences, quotes, numbers and words, instant WPM. No sign up, progress saved.` | 四模式、时长 chips、localStorage 历史 |
| best-typing-test-online | `Best Typing Test Online (2026): 6 Free Sites Compared` | `6 best free typing tests online compared: monkeytype, 10fastfingers, typing.com, keybr, TypingTest.com — languages, sign-up, practice. Pick in ten seconds.` | 表格里正好 6 家（含本站）、"How to choose in ten seconds" 小节 |
| learn-to-type | `Learn to Type: Free Typing Tutorial From the Home Row` | `Learn to type for free with a typing tutorial that starts at the home row: one row at a time, 60 seconds a day, instant feedback. No sign up, no install.` | 首页行起步、逐行加、60 秒/天、即时反馈 |

`6 Free Sites` 与 `typing tutorial` 是**已有事实换个说法**，不是新承诺：对比表本来就是 6 家，
learn-to-type 本来就是逐课教程（FAQ 里已有 "What is the first thing I should learn?"）。

## 3. `<h1>` 对齐（只改不一致的 4 个）

| 页面 | 旧 h1 | 新 h1 | 理由 |
|---|---|---|---|
| 1-minute | 1 Minute Typing Test | 不变 | 已与 title 同主题 |
| wpm | Words Per Minute Test | Words Per Minute Test (WPM) | title 主打 `WPM Test`，h1 补上缩写（`wpm` 是 87 曝光主查询） |
| typing-practice | Typing Practice | Free Online Typing Practice | 目标词是 `online typing practice` |
| best-typing-test-online | Best Free Typing Tests Online | Best Free Typing Tests Online (2026) | 与 title 的年份口径一致 |
| learn-to-type | Learn to Type | Learn to Type: Free Typing Tutorial for Beginners | 与 title 的 `Typing Tutorial` 口径一致 |

## 4. 首页正文内链（不是导航）

新增一节 `Where to start: the tests people use most`（落在 `{{SEO}}` 槽位内，骨架不变），
用**目标查询词做锚文本**，5 条全部指向本轮 5 页：

- `one minute typing test` → 1-minute-typing-test.html
- `words per minute test` → words-per-minute-test.html
- `online typing practice` → typing-practice.html
- `best free typing tests online` → best-typing-test-online.html
- `typing tutorial` → learn-to-type.html

之前这 5 页只有三处入口：顶栏 3 个短语（"1 Minute Test" / "WPM Test" / "Typing Practice"）、
相关导航 1 条、页脚 131 条扁平链接。页脚是样板，顶栏文字短到看不出主题，
所以正文段落是第一次用**查询词锚文本**指过去。落点已进 `index.md` 与 `llms-full.txt`。

## 5. 结构化数据

5 页原本就有 `WebApplication` + `FAQPage` + `BreadcrumbList` 三块（verify 6 号门禁逐页锁类型与顺序），
本轮复验：全部 `json.loads` 通过、Breadcrumb 与页面主题一致、canonical 自指。
**未新增**任何 schema 字段——加字段会同时撞 6 号（类型顺序）与 9 号（骨架金标）两处约束。

## 6. `llms.txt` / `llms-full.txt`

`llms.txt` 本来就逐条列了这 5 页（verify 13 号门禁要求 URL 集合与页面集合完全相等），
本轮复查无缺项。`llms-full.txt` 由 `build.py` 生成，已随本轮正文改动更新。

## 7. 门禁结果

```
python3 build.py && python3 verify.py   → 通过 20/20 项
6b. title≤62 / desc≤155(≤158) / 131 页描述两两相似度 ≤0.70
9.  骨架 == 金标 d0f62ba4f8c51dbb（新增正文节未破结构）
7.  sitemap 131/131 URL 不变（仅 6 个 lastmod 更新到 2026-10-31）
13. llms.txt 131/131 URL 一致
```

## 8. 诚实的预期

同 ROUND-18：这轮的曝光主要在 pos 51-100 区间，标题改写改变的是「被点到」的概率，
不是曝光量。1-minute 页 802 曝光若 CTR 从 0.25% 抬到 2%，三个月多约 10 次点击——
是修缺陷，不是翻盘。位置仍靠外链。
