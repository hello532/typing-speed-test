# ROUND-22：SEO/GEO 增强批（2026-10-31，r23–r36 合并记录）

> 目标：把排名与点击推到 **2000 点击/28 天**。
> 本文记录这一批做了什么、依据是什么、以及「2000 点击」到底还差什么。
> 所有数字分三层标注：**实测（GSC）／算术（反推）／假设（行业观察值）**。

---

## 一、开工前的实测基线（不是估计）

GSC，2026-10-03 ~ 2026-10-30，28 天：

```
点击 97 ｜ 曝光 5,612 ｜ CTR 1.73% ｜ 平均排名 56.4
```

90 天 page+query 交叉拉取（`gsc.py` 之外的组合维度查询）暴露了本批工作的选点依据：

| 页面 | 曝光 | 点击 | 位置 | 查询面 |
|---|---|---|---|---|
| 1-minute-typing-test | 802 | 2 | 65.2 | 202 个查询，主词 `1 minute typing test` 49 曝光 / p53 |
| average-typing-speed | 596 | 0 | 58.8 | 251 个查询，全部 p55–70 |
| words-per-minute-test | 465 | 1 | 58.3 | — |
| typing-practice | 424 | 5 | 68.3 | 主词 `typing practice` 70 曝光 / **p94** |
| keyboard-practice | 341 | 0 | 77.2 | `keyboard practice` 48 曝光 / p84 |
| free-typing-test | 239 | 0 | 72.5 | 81 个查询，p71–92 |
| typing-speed-requirements | 52 | 0 | 47.2 | 只有 17 个查询 → 页面与需求错配 |

关键结论：**曝光面只有 5,612，而 121 个「有曝光」页面若全部进前 10，可回收点击上限也只有 50。**
也就是说，这一阶段的问题不是文案 CTR，而是**可竞争的查询面太窄 + 平均排名 56**。

---

## 二、竞品对标（第三方独立研究，Bing en-US 实抓，见 `work/competitors-top50.md`）

50 个可用站点 + 108 首页 + 45 子页 + 74 sitemap 实抓。三条对本站有直接影响的发现：

1. **格式竞争三分且互不重叠**：裸工具页赢所有测量类查询；数据/报告页（样本量 + 百分位 + 年份）赢 `average typing speed`；职位/考试页赢 `typing test for {job}`。课程页只赢 `touch typing`。
2. **可打面是「小站也能进首页」的族**：`wpm→kph 转换`、`gross vs net WPM`、`percentile`、`is-X-wpm-good`、职位页、年级页——这些 SERP 上站着的是几十个 URL 的小站，不是大品牌。
3. **GEO 已经是标配**：工具下方实时统计块、带样本量的研究引用、结论先行 H1、自限段、署名+日期、`FAQPage`/`BreadcrumbList`。本站在 schema 与 llms 上已达标，缺的是**可被引用的具体数字**。

> 诚实边界：Google 侧无 API、直连被拦，排名证据全部来自 Bing en-US，不能 1:1 迁移到 Google。竞品文件里没有任何流量/外链/搜索量数字，一律 `not observed`。

---

## 三、这一批做了什么（页数 131 → 171）

| 轮次 | 内容 | 为什么是它 |
|---|---|---|
| r23 | 6 页：10000 KPH、WPM→KPH、gross vs net、percentile、receptionist、call center | 竞品只有静态表格；KPH/净 WPM/百分位是高频且可算的查询 |
| r24 | 6 页：护士、法庭记录员、911 调度、SSC CHSL、五年级、法律秘书 | 职位族 SERP 由小站占据，可打 |
| r25 | 重写 `typing-speed-requirements`（17 查询 → 三单位互转 + 公开标准）与 `average-typing-speed`（主口径换成 CHI 2018 的 51.56 WPM） | 这两页曝光最大但排名最差，属于结构性问题 |
| r26 | 6 页：联邦、公务员、CritiCall、字母数字、虚拟助理、医疗计费 | 考试/证书族，招聘方驱动，商业意图强 |
| r27 | 6 页：30/40/50/60/70/100 WPM | 与 `is-X-wpm-good` 同一意图，但做成「目标速度」而不是 15 个近重复页 |
| r28 | `wpm-chart`（结论表）+ **实时双向 WPM↔KPH 转换器**（内联 JS，公式有单测） | 竞品全是静态表；真工具是差异化 |
| r29 | 4 页：手机 vs 键盘、年级分档、简历 WPM、证书验收 | 全是可引用页：两条 DOI、分档表、诚实自限 |
| r30 | `typing-tests.html` 目录页（构建时从 clusters 生成 162 条正文内链） | 手写目录必然过期，生成式永远等于实际页数 |
| r31 | `linkgraph.py` + 首页/关于页接入目录 | 修前首页正文可达 113/178、深度≥3 有 97 页 → 修后 161/178、深度≥3 只剩 7 页（全是 noindex share 卡） |
| r33 | `roadmap.py`：2000 点击台阶表 + 三杠杆归因 | 把「还差多少」变成可复算的数 |
| r34 | SQL/TypeScript/Rust/Excel 各 36 行真实语法 + 会计/律助两页 | 代码族 query 无大站覆盖，且变体池只注入对应页（零冗余） |
| r35 | USPS 考试真相页、60+ 打字、客服渠道、30 天计划 | USPS 页给的是「474–477 不含打字测试」这个可核验答案，而不是卖无关练习 |
| r36 | llms.txt 事实修正 + 14 页 TL;DR | AI 引用错一个数字，比不被引用更糟 |

工程侧同时落地：

- `build.py`：`datePublished`/`dateModified` 改由 **git 历史**派生（首次/末次提交），正文署名行输出同源日期——不再全站写死一个日期
- `expand.py`：一次写四个真源（pages.json / footer.html / llms.txt / clusters.json），并硬校验 `title≤62`、`desc≤158`、描述两两相似度 `≤0.70`、正文 `≥1200` 字符、`FAQ≥5`
- `gauges.py`（今天先改哪页）、`roadmap.py`（2000 缺什么）、`linkgraph.py`（正文内链图）

---

## 四、门禁与线上验证

```
python3 build.py && python3 verify.py     → 20/20 通过（171 页）
python3 src/tools/linkops.py live         → sitemap 167/167 URL 全部 200，0 异常
python3 src/tools/indexnow.py             → 167 URL 提交成功（1 batch, 0 failed）
```

`verify.py` 里真正起作用的几条：3（产物=build 输出）、6b（标题/描述长度与互不雷同）、
7/13（sitemap 与 llms.txt 覆盖严格相等）、9（骨架金标锁）、12（页脚覆盖全站）。

---

## 五、2000 点击到底缺什么（算术，不是预测）

```
现在   97 点击 / 5,612 曝光 / CTR 1.73% / 平均排名 56.4
2000 点击需要：
  CTR 2% → 100,000 曝光（×17.8）
  CTR 3% →  66,667 曝光（×11.9）
  CTR 5% →  40,000 曝光（×7.1）
```

三个杠杆分开看：

| 杠杆 | 现在 | 需要 | 手段 |
|---|---|---|---|
| 曝光量 | 5,612 | 100,000（保持 CTR） | 更多可竞争查询 + 现有页进前 20 |
| CTR | 1.73% | 35.6%（保持曝光） | 位置 >30 时 CTR 由位置决定，文案空间有限 |
| 平均排名 | 56.4 | ≤15 | 相关性（已做够）+ **引用域名（当前瓶颈）** |

台阶表（`roadmap.py` 可复算）：

| 点击/28d | CTR 2% | CTR 3% | CTR 5% |
|---|---|---|---|
| 250 | 12,500 曝光 | 8,333 | 5,000 |
| 500 | 25,000 曝光 | 16,667 | 10,000 |
| 1,000 | 50,000 曝光 | 33,333 | 20,000 |
| 2,000 | 100,000 曝光 | 66,667 | 40,000 |

**结论：2000 点击不是内容问题，是权威度问题。** 这一批把「可竞争查询面」从 131 页扩到 171 页、
把正文内链深度收紧到 ≤2 跳、把可引用事实（DOI、样本量、分档表）补齐——这些是外链到来后
能立刻变现的地基。没有外链，任何一页都停在 p50 上下，写多少字都不会动。

---

## 六、下一步（按性价比排序）

1. **外链**：台账里 87 条已提交，PR 9 个在审。可自控的还有：awesome-list 新增条目、行业目录、把
   `typing-speed-percentile` 与 `typing-speed-phone-vs-keyboard` 作为「可引用数据页」去争取引用。
2. **等数据**：GSC 有 2–3 天延迟，本轮 40 页新页需要 2–4 周才能看出是否进 p20 以内。
   复查指令：`python3 src/tools/gauges.py` → 看「已进前 30」清单是否变长。
3. **CTR 只对 p11–30 的页做**：现在满足条件的只有 about / online-typing-practice / top-hi-words 等少数几页，
   其余页面位置太深，改标题没有意义。
4. **别再堆页**：171 页已经足够覆盖现有可竞争面，继续加页的边际收益低于加外链。

---

## 七、复跑指令

```bash
python3 src/tools/gauges.py          # 今天先改哪页（uplift 排序）
python3 src/tools/roadmap.py         # 2000 点击的台阶表与缺口归因
python3 src/tools/linkgraph.py       # 正文内链图与点击深度
python3 src/tools/gsc.py pages       # 28 天按页取数
python3 src/batch*/…                 # 内容批次（expand.py 写入四个真源）
python3 build.py && python3 verify.py
python3 src/tools/indexnow.py        # 新增 URL 提交
```

---

## 八、续批（r38–r48，同一晚继续）

| 轮次 | 内容 | 验证 |
|---|---|---|
| r38 | 4 页文书/物流职位（法院书记员、医疗前台、理赔、仓库行政） | 175 页，20/20 |
| r39 | 长页自动目录（≥6 节生成 On this page）+ 稳定 h2 锚点 | 60 页有目录，锚点全解析 |
| r40 | 数据页 `typing-speed-benchmarks` + 25 行 CSV（只放可溯源数字） | 176 页，20/20 |
| r41 | 手指图加 486×265 内在尺寸与 lazy/async（CLS） | 尺寸与 PNG IHDR 实测一致 |
| r42 | `health.py`：9 项不依赖搜索数据的硬检查 | 178 页全绿 |
| r43 | 德语 / 法语真实语料（QWERTZ / AZERTY），语言数 → 14 | hreflang 14 + x-default |
| r44 | 30 天计划页 HowTo；骨架归一支持任意块数 JSON-LD | 金标按流程重签 065d8701 |
| r45 | `weekly.py` 周报 + PLAN-90-DAY | 关键发现：97 点击里 68 次是品牌型 |
| r46 | 补厚 6 个薄页（教师/高级/多快/困难/快速/段落） | 正文 1,000 → 1,800-2,500 字符 |
| r47 | 补厚 4 个语种页（阿拉伯/英语/印地/中文） | 每页 5 FAQ，机制差异写清 |

### 这一批结束时的事实

```
页数 131 → 178
verifier 20/20 ｜ health 9/9 ｜ structure gate S1/S2/S3 全绿
线上 sitemap 178/178 URL 全部 200（IndexNow 已提交 178 条，0 失败）
ui.js 语种池 14 个（de/fr 各 40 句已上线）
正文内链深度：178 页中 171 页 ≤2 跳，其余 7 页为 noindex 分享卡与验证文件
正文重复度检查：8-gram Jaccard >0.25 的只有 11 对，最高 0.43（同族词表页的交叉链接段），
                无整页重复
```

### 仍未解决的一件事（不掩饰）

**2000 点击/28 天需要的不是更多的页，而是数量级更多的引用域名。**
截至本轮，站内能做的（覆盖、深度、内链、可引用性、技术卫生）已经做到这个域名当前的上限；
剩下的 6 倍曝光缺口只能靠外链 + 时间，`PLAN-90-DAY.md` 里按周拆了动作。

---

## 九、第二批续跑（r49–r56）

| 轮次 | 内容 | 结果 |
|---|---|---|
| r49 | `health.py` 挂进 CI 硬门禁；README 工具表补全 | CI 第 5 步：死链/重复 title/canonical/h1/sitemap 一致性 |
| r50 | `touch-typing-course`：12 课，每课一个 drill + 一个过关标准 | 竞品研究显示「touch typing」赢课程页；引 Feit 2016 支持「一致性 > 固定指法」 |
| r51–r54 | 把全站最后 16 个薄页补到 ≥1,500 字符 | 正文 min 1,265→1,500（privacy 除外），中位数 2,386 |
| r55 | 按 GSC 真实查询给 6 个高曝光页补 13 条 FAQ | 用查询原话（"one minute typing test"、"free wpm test"…），不是同义改写 |
| r56 | 对比页升级：7 维表 + 方法说明 + 「明确不测什么」 | 竞品研究里赢的对比页都带方法论与自限段 |
| r57 | `typing-speed-calculator` 变成真计算器（字符/错误/秒 → gross/net WPM、CPM、KPH、百分位） | JS 的 erf 近似与 Python `math.erf` 在 40/60/80/100 WPM 上偏差 ≤0.1 个百分位 |

### 这一批的质量基线

```
页数 179 ｜ 正文中位数 2,386 字符（min 1,500，privacy 例外）
FAQ 页均 5.4 条（新增页强制 ≥5）
verify 20/20 ｜ structure gate S1/S2/S3 ｜ health 9/9 ｜ CI 4 步全绿
```

---

## 十、外链资产（r60，第一次真正的站外动作）

站内已经铺满（184 页），所以这一轮做了一件站外但完全自控的事：把数据做成
**公开可引用仓库**，而不是继续加页。

**仓库**：<https://github.com/hello532/typing-speed-benchmarks>

| 内容 | 说明 |
|---|---|
| README | 两条 DOI（CHI 2018 / MobileHCI 2019）、设备对比表、单位换算表、明确的「不写什么」 |
| benchmarks.csv | 5 WPM 步长 25 行（wpm/percentile/cpm/kph），与站内同源 |
| percentile.py | 标准库实现，`python3 percentile.py 40 60 80 100` → 28.4 / 66.2 / 92.0 / 99.2 |
| percentile.js | 无依赖 ESM，Abramowitz-Stegun erf 近似；与 Python 结果逐位一致（已验证） |
| LICENSE | 代码 MIT，数字归属原论文（README 里写明） |

为什么这样做：这是唯一一种**不联系任何人、不买链接、不碰 ToS** 就能拿到的、主题相关的
dofollow 引用（GitHub DR 96，README 内链 benchmarks 页）。同时它给下个月的 awesome-list
提交提供了「可引用数据」的实体，而不是一句「请收录我的打字网站」。

台账已登记（第 88 条，status=live）。诚实提醒：GitHub 的站内链接权重传递有限，
它是**引用的起点**，不是排名解药；真正起作用的是有人引用这个数据集。

---

## 十一、r61 与「零曝光页」排查

这一轮先做了证据排查再动手：GSC 180 天 page 维度显示 **184 页里 121 页有曝光、63 页从未出现**。
其中 53 页是昨天新建（零曝光是正常），10 页是旧页：

```
colemak · paragraph · fast · hard · ssc-typing-test · top-ko · top-id · top-tr ·
how-to-type-faster-and-more-accurately · mechanical-keyboard-for-typing
```

用 `linkgraph.py` 复核：这 10 页都有 2-6 条正文内链、点击深度 1-2，**不缺内链**。
所以零曝光的解释不是孤儿页，而是「排不进前 100，任何查询都不出图」。结论与前面一致：
**权威度问题，不是内链或内容问题。**

本轮实际改动：

| 项 | 内容 |
|---|---|
| 证书页 | 1,752 → 3,290 字符：印了什么（6 字段及理由）、A4/Letter 与黑白打印、该用哪个 WPM、雇主怎么看待自签、数据去哪了；加 TL;DR 明确「自签≠监考」 |
| CITATION-KIT.md | 可引用资产清单、可照抄的准确说法、五类场景与禁区、一条不索取链接的外联文本、判定规则与期望值 |

**page+query 的一个硬限制**（写下来避免下次再试）：对 67 曝光以下的页面，GSC 的
page+query 组合维度会因匿名化返回空集，只有 page 维度总量可见。也就是说
「这一页到底靠哪些词拿到曝光」在低量阶段是**不可知**的，针对它的 CTR 改写只能是盲改。
这也是为什么本轮没有去改 `online-typing-practice`（p4.2 / 67 曝光 / 1 点击）的标题——
不知道查询是什么，改了就是赌。

---

## 十二、r62–r66（目标轮 5–6）

| 轮次 | 内容 | 依据 / 验证 |
|---|---|---|
| r62 | CPM 页加三向实时换算器；KPH 页 4,000→6,560 字符（平均 KPH、8000 KPD→26.7 WPM、key depression vs keystroke） | 30 天 query 维度："cpm test" 49 曝光 p20.8、"average keystrokes per hour" p18.3、"8000 key depression in wpm" p70.7 |
| r63 | about 页补「发布与纠错原则」；health.py 第 10 项锚点检查 | 184 页 0 个未解析锚点 |
| r64 | typing-practice 改成练习枢纽：Start here 三步 + 四周计划表 + 12 节按「开始→计划→诊断→纠错」重排 | "typing practice" 族 608 曝光 p84-94，竞品研究说这一族赢课程/枢纽格式 |
| r65 | health.py 第 11 项：行内脚本 node --check（去重 55 段，378 段原始） | 0 语法错误；覆盖我这一晚加的 3 处交互 |
| r66 | quotes 1,706→2,400、typing-skill-test 重排补三节 | 两页分别在 p27.2 / p19.8 |
| r67 | average-typing-speed 补「为什么各家口径不一致」四口径对照表 | 该族 229 曝光 p57-65 0 点击；新增 40 / 51.56 / 36.17 / 60-70 四个口径的适用人群 |
| r68 | 首页正文接入考试/数据/课程三簇，正文内链 35→42 | federal、SSC CHSL、CritiCall、SQL、benchmarks、consistency、课程页此前只在页脚与 related |

### 一个必须记住的取证限制

对曝光量小的页面，**GSC 的 page+query 组合维度因匿名化返回空集**。例如
`online-typing-practice`（67 曝光 / p4.2）在组合维度里查到 0 条查询。
结论：低量页「靠哪些词拿曝光」不可知，针对它改标题就是赌——这一条写在
`why` 里，避免下次再花时间试。

### 当前形态

```
184 页 ｜ 正文 min/median/max = 1,500 / 2,386 / 32,209
verify 20/20 ｜ health 11/11 ｜ structure gate S1/S2/S3
线上 184/184 URL 200 ｜ sitemap 184 ｜ llms.txt 覆盖一致
外链台账 88 条（1 条 live 为新建的 GitHub 数据仓）
```

---

## 十三、r69：真浏览器验收抓到一个静态检查抓不到的 bug

用 `ego-browser` 在**线上**跑交互，而不是只看构建产物：

| 交互 | 结果 |
|---|---|
| WPM↔KPH 换算器 | ✅ 50 WPM → 15,000 KPH；12,000 KPH → 40 WPM |
| 速度计算器 | ✅ 400 字符 / 4 错 / 120 秒 → 40 gross、39.6 net、200 CPM、12,000 KPH、28th |
| 目录筛选器 | ❌ **计数变了但列表不动** |
| 德语页语种接线 | ✅ `TR.lang='de'`，首句为德语，界面切到德语 |

筛选器的根因不是语法，是**执行顺序**：内联脚本位于页面上方的第一个 seo 区块，
执行时后面的 catalog 列表还没被解析，`sec.querySelectorAll('ul.catalog')` 取到长度 0 的
静态 NodeList 并被闭包固化；之后 `run()` 遍历空数组，只有 `o.textContent` 那行照常执行——
于是出现"显示 0 matches，但 184 条一条没隐藏"。

修法：把查询移进 `run()`，每次输入重新取。修复后线上复测：
`nurse` → 1 条、`kph` → 1 条、清空 → 184 条。

**教训（写进流程）**：`node --check` 只能证明语法合法。这一晚加的 3 处交互里，
只有真浏览器跑一遍才能发现这类"合法但无效"的脚本。后续每加一处交互，都要用
`ego-browser` 在线上点一次。
