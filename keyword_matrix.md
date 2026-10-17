# 关键词矩阵 — typing.rerivo.com（41 页基线）

> 2026-10-10 建立。关键词取自每页 `src/pages.json` 的 `seo[0].h2`（页面主旨），即页面实际竞争的目标词。
> src/ 是唯一源；新增页面必须先在此登记目标词，再建池建页。

## 选词口径

- 只打「工具型搜索意图」：搜的人想立刻测/练，不是想读文章。
- 每页一个主词，主词之间不互相竞争（时长线、模式线、教育线、游戏线、语言线、差异化线互斥）。
- 优先有竞品背书的词（竞品已在打 = 有搜索量），见「竞品背书」列。

## P0 品牌与核心大盘词（流量入口）

| 页面 | 目标词 | 竞品背书 | 备注 |
|---|---|---|---|
| index.html | typing speed test | monkeytype, 10fastfingers, typingtest.com | 全站主词，首页 |
| wpm-test-online.html | WPM test online | monkeytype | 与下条互为变体，title 侧重 check your wpm |
| words-per-minute-test.html | words per minute test | typingtest.com | 大盘词 |
| online-typing-test.html | online typing test | typingtest.com, ratatype | |
| free-typing-test.html | free typing test, no sign up | typingtest.com | 「no sign up」是差异化锚点 |

## P1 时长线（高商业意图，最容易切）

| 页面 | 目标词 | 备注 |
|---|---|---|
| 1-minute-typing-test.html | 1 minute typing test | 60s，首页默认档 |
| 2-minute-typing-test.html | 2 minute typing test | |
| 3-minute-typing-test.html | 3 minute typing test | |
| 5-minute-typing-test.html | 5 minute typing test | |
| 10-minute-typing-test.html | 10 minute typing test | |
| 30-second-typing-test.html | 30 second typing test | |

## P1 模式线（按练习内容切分）

| 页面 | 目标词 | 备注 |
|---|---|---|
| punctuation-typing-test.html | punctuation typing test | 标点密度闸门 ≥15% 支撑 |
| capital-letter-typing-test.html | capital letter typing test | shift 键专项 |
| number-typing-test.html | number typing test | 数字小键盘 |
| typing-accuracy-test.html | typing accuracy test | |
| easy-typing-test.html | easy typing test for beginners | |
| keyboard-typing-test.html | keyboard typing test | |
| custom-typing-test.html | custom typing test | 自定义时长+模式 |

## P1 教育线（搜索意图：学/练，停留长，Adsense 单价好）

| 页面 | 目标词 | 竞品背书 | 备注 |
|---|---|---|---|
| typing-tutorial.html | typing tutorial | typing.com | 步骤式课程 |
| typing-tutor.html | typing tutor | ratatype | 反馈纠错式陪练，池= tutor |
| learn-to-type.html | learn to type | typing.com | 零基础起步，池= learner |
| learn-to-type-faster.html | learn to type faster | typing.com | 进阶 |
| typing-trainer.html | typing trainer | typingtest.com | 训练计划/肌肉记忆，池= trainer |
| typing-lessons.html | typing lessons | typing.com | |
| typing-practice.html | typing practice | typing.com, keybr | |
| typing-tips.html | typing tips | typing.com | |
| touch-typing-test.html | touch typing test | ratatype, keybr | 触觉盲打 |

## P1 游戏线（搜索意图：玩，传播性强）

| 页面 | 目标词 | 备注 |
|---|---|---|
| typing-games.html | typing games | 汇总页 |
| typing-test-game.html | typing test game | 单游戏页 |
| typing-race.html | typing race | 竞速 |

## P1 多语言线（GEO 五语聚类 + hreflang）

| 页面 | 目标词 | 备注 |
|---|---|---|
| english-typing-test.html | english typing test | 默认 en |
| spanish-typing-test.html | spanish typing test | |
| chinese-typing-test.html | chinese typing test | |
| hindi-typing-test.html | hindi typing test | |
| arabic-typing-test.html | arabic typing test | RTL |
| typing-tests-in-other-languages.html | typing tests in other languages | 语言线 hub |

## P1 差异化线（竞品少，转化留客）

| 页面 | 目标词 | 备注 |
|---|---|---|
| typing-certificate.html | typing certificate | 可打印证书，独有 |
| dvorak-typing.html | dvorak typing | Dvorak 布局 |
| one-hand-typing.html | one hand typing | 单手练习 |

## P2 扩展页（2026-10-11 新增：GEO 数据页 + 长尾）

| 页面 | 目标词 | 竞品背书 | 备注 |
|---|---|---|---|
| average-typing-speed.html | average typing speed / good typing speed / average wpm | wonderlic, typingtest.now | 基准数据 hub（技能/年龄/职业三表），GEO 可引用，内链枢纽 |
| cpm-typing-test.html | cpm typing test / characters per minute | 10fastfingers, typingtest.com | CPM 指标线（CPM=WPM×5），与 number 线不互斥 |
| typing-test-for-kids.html | typing test for kids / kids typing test | typing.com, typingclub | 儿童受众，words 模式 + 年龄表 |
| typing-test-for-jobs.html | typing test for jobs / pre employment typing test / data entry typing test | typingtest.com, typing.com | 就业/数据录入意图，职业要求表 + 准确率列 |

## 非排名字段（合规/品牌，不参与选词）

| 页面 | 用途 |
|---|---|
| privacy-policy.html | AdSense 合规 |
| about.html | AdSense 合规 + 品牌信任 |

## 仍空白的有背书词（下一批候选）

来源 `competitor_keywords.md`，已有竞品在打但本站未建页：

| 词 | 竞品 | 优先级 | 备注 |
|---|---|---|---|
| typing practice test | keybr, typing.com | P2 | 与 typing-practice 高度重叠，先观察 |
| typing speed test online | typingtest.com | P2 | 与 online-typing-test 重叠 |
| improve typing speed | typing.com | P2 | 意图偏文章，与工具站定位不符，暂缓 |

结论：41 页已覆盖全部 P0/P1 有背书词，P2 与现有页重叠度过高，暂不扩页；下一轮重心转收录与外链，而非继续建页。

## P3 布局线（2026-10-12 新增：Round-2 竞品吸收 + GEO 数据页）

| 页面 | 目标词 | 竞品背书 | 备注 |
|---|---|---|---|
| keyboard-layouts.html | keyboard layouts / dvorak vs qwerty / colemak vs qwerty / best keyboard layout | keybr /layouts, thetypingcat | GEO 磁铁：四布局对比表（home-row% / same-finger% / finger-travel），可被 AI 引用；布局线内链枢纽 |
| colemak-typing.html | colemak typing test / colemak practice | ratatype, keybr, typingmaster | 布局线实测页；engine 支持 QWERTY/Dvorak/Colemak 三路，含 Colemak 指法引导 |

本轮同时做功能增强（非建页，吸收自 top10 竞品）：键位热力图（keybr/TypingMaster）、成绩分级+百分位（TypingMaster/Ratatype 档位）、分级证书 Platinum/Gold/Silver（Ratatype）、Colemak 布局（keybr/typingmaster）。

## P4 技能/职业/考试线（2026-10-16 Round-3：Google autosuggest 实测选词）

> 数据源：`seo_round3/suggest_raw.json`（1350 条 autosuggest 查询 → 9867 条唯一建议，curl 直连 suggestqueries.google.com）。
> 口径：prominence 分数 = Σ(10−位置)，越大越靠前越热门；选「工具型高意图」词（搜的人想立刻测/练）。

| 页面 | 目标词 | autosuggest 证据（prominence） | 备注 |
|---|---|---|---|
| ten-key-typing-test.html | 10 key typing test / ten key typing / numpad typing test | "10 key typing test/practice/speed" 全组，含 numbers only | 数字键盘专项，numbers 模式 |
| data-entry-typing-test.html | data entry typing test | "data entry typing test/jobs/practice/speed" 高需求簇 | 与 for-jobs 互补（jobs=要求表，entry=实测） |
| keystrokes-per-hour-test.html | keystrokes per hour / kph typing test | "keystrokes per hour test/calculator/to wpm" 全组 | KPH↔WPM↔CPM 换算表 |
| typing-speed-calculator.html | typing speed calculator / words per minute calculator | "typing speed calculator/formula/wpm" + "words per minute calculator" | 工具型计算页 + 换算公式 |
| quick-brown-fox-typing-test.html | quick brown fox typing test | "quick brown fox typing test/practice/sentence" 全组 | pangram 热身 + 键盘检测 |
| home-row-typing-test.html | home row typing test | "typing practice home row" / "typing practice j and f" | 指法表 + 内链 touch typing |
| typing-test-for-adults.html | typing test for adults | "typing test for adults/practice/games" 全组 | 成人受众，平均 40 WPM |
| typing-test-for-students.html | typing test for students | "typing test for students/college/elementary" | 学生受众，各学段 WPM 目标表 |
| typing-skill-test.html | typing skill test | "typing skill test online/practice/paragraph" | 技能等级表（WPM×准确率） |
| government-typing-test.html | government typing test / typing test for government jobs | "government typing test/practice/5 minutes" + "typing test for government jobs" | 3 分钟默认，公职/文书考试 |

内链枢纽：首页新增「Typing tests by skill and job」段，全 10 新页互链 + 链回首页/核心页。

## P5 格式/级别/考试线（2026-10-16 Round-3 批次二）

| 页面 | 目标词 | autosuggest 证据 |
|---|---|---|
| paragraph-typing-test.html | paragraph typing test | "paragraph typing test online/5 minutes/1 minute/english" 全组 |
| beginner-typing-test.html | beginner typing test / typing test for beginners | 两组均 10+ 条建议 |
| timed-typing-test.html | timed typing test / typing test with timer | "timed typing test free/1 minute/5 minutes" + "with timer" |
| fast-typing-test.html | fast typing test | "fast typing test free/online/game/practice" |
| hard-typing-test.html | hard typing test / difficult typing test | 两组 "hard typing test paragraph/10 minutes" |
| advanced-typing-test.html | advanced typing test | "advanced typing test english/online/5 minutes" |
| how-fast-can-i-type.html | how fast can i type / how fast do i type | "how fast can i type test/per minute" + "how fast do i type" |
| typing-test-for-interview.html | typing test for interview | "typing test for interview/job interview/bpo" |
| bank-typing-test.html | bank typing test | "bank typing test / typing test for banking exam" |
| ssc-typing-test.html | ssc typing test | "ssc typing test online/practice/10 minutes" |
| typing-test-for-teachers.html | typing test for teachers | "typing test for teachers" (6 条) |
| keyboard-practice.html | keyboard practice / keyboard online practice | "keyboard online practice" 10 条 |

