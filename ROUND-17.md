# Round 17 — typing.rerivo.com（2026-10-20）

> 依据：GSC 实库 28d（2026-09-22 ~ 2026-10-19）+ 131 页产物全量审计。
> 口径：本文件只写**实测到的数**与**已完成的改动**；未发生的效果不预测、不承诺。

## 1. 起点数据（GSC，28 天，final）

| 指标 | 值 | 说明 |
|---|---|---|
| clicks | **5** | 唯一有实际点击的页：1-minute(2)、10-minute(1)、30s(1)、spanish(1) |
| impressions | **2,253** | 95% 集中在第 5-10 页 |
| CTR | 0.22% | 与 pos 61 相符 |
| 平均排名 | **61.2** | 家喻户晓的"页面很多、权重为零"形态 |
| 有曝光页数 | **46 / 131** | 85 页零曝光 |
| 索引（URL Inspection 抽样 100） | 82-84 indexed / 2 crawled-not-indexed / 2 discovered-not-indexed | 索引不是瓶颈 |

**关键结构性数字**：815 个 query 中，**51 个已落在 pos 6-30（2-3 页边界）**，但合计只有 **99 曝光**。
即：真正"临门一脚"的机会池极小 —— 每页只分到 1.2 次曝光。不是内容没排上，是页面没有足够的权重去占据任何词。

## 2. 定性（有证据，不是感觉）

| 假设 | 检验 | 结论 |
|---|---|---|
| 内容重复 / 模板化 | 131 页两两 5-gram Jaccard（40 页抽样，780 对） | 中位 **0.000**，最高 0.166（词表页）→ **不是重复问题** |
| 内链不足 | 页脚枢纽覆盖 131/131；正文内链 104 页 / 452 条 | 覆盖够，但**每页链全部 130 页** → 单页只分 1/130 权重 |
| 标题/描述问题 | 抽检 8 页 title/desc/H1 | 已对齐，长度合规 |
| 结构化数据问题 | 395 块 JSON-LD 合法，骨架唯一 | 技术层已满分 |
| **权威度 / E-E-A-T** | geo_page_score：author=0/8，外链引用=0/6 | **真缺口**，且是全站性 |
| **权重分散** | 131 页 × 13 分区页脚，目标词全在 pos 60-99 | **真缺口** |

结论：技术 SEO 已经做到头（19/19 门禁全绿、索引 82%+、canonical 131/131 自指、
robots/AI 爬虫全放行）。**继续加页不会改变排名曲线**，因为新页同样只拿 1/130 权重。

## 3. 本轮做了什么

### 3.1 E-E-A-T 从 0 分做到 8/8（可核验，不编造）

- `WebApplication` JSON-LD 增加 `author` / `publisher`，实体为 Organization，`@id` 指向
  `https://typing.rerivo.com/#organization`，`url` 指向 about 页。**没有编造人名或资历。**
- 每页正文加可见署名 byline → about 方法论页。
- about 页新增「Sources and standards」6 条**真实可核验**来源：
  Wikipedia `Words_per_minute` / `Touch_typing` / `Dvorak_keyboard_layout` / `Colemak` /
  `Numeric_keypad` + O*NET `43-9021.00`（Data Entry Keyers）。
- 10 个页面补 dofollow 外部引用；原先唯一的外链是 wonderlic.com 的 `rel="nofollow"` 商源
  （对 E-E-A-T 无效），已换成 Wikipedia 自由源。
- 所有外部引用均逐条 `curl` 验证 200 后才写入。

geo_page_score：**1-minute 83 → 93（A）**，about 88（A），外链引用项 0/6 → 6/6。

### 3.2 只抢 GSC 证实的边界词（不猜词）

| 页 | 边界 query（pos） | 动作 |
|---|---|---|
| `words-per-minute-test.html` | typing words per minute test (16.0) | 补段 + FAQ，正文出现 6 次 |
| `cpm-typing-test.html` | cpm test (23.4) | 补段 + FAQ |
| `1-minute-typing-test.html` | one minute typing test (23.3) | 五错段改 `<ul>` + Last updated |
| `10-minute-typing-test.html` | 10 minute typing test (25.3) | 补段 + 来源 |
| `5-minute-typing-test.html` | — | 补缺失 tldr + 五字符规则来源 |

### 3.3 权重集中（定向，不重构）

在**语义自然**的位置给 4 个边界页加内链：时长阶梯页（2/3/timed → 1-minute）、
单位换算页（10-key/KPH → CPM）、耐力页（5-minute → 10-minute）。
+8 条正文内链，零关键词堆砌。

### 3.4 修真实缺陷（不是优化，是 bug）

| 缺陷 | 证据 | 修复 |
|---|---|---|
| **外链 PR 无法合并** | `PR#7 mergeable=CONFLICTING`（分支落后 master） | 关闭，rebase 到 upstream master → **PR#10（+2/-0, MERGEABLE）** |
| **RTL 语言方向错误** | ar/ur 落地页 `dir` 未声明，阿拉伯/乌尔都练习文本按 LTR 渲染 | 补 `<html dir="rtl">` |
| **gsc.py 取不到数** | `cafile=` **替换**了系统信任库 → CERTIFICATE_VERIFY_FAILED | 改为叠加系统默认 + 代理 CA；并自动探测本地 Surge |
| **审计工具盲区** | `<html>` 属性无槽位 → 任何 lang/dir 变更都会撞金标锁 | 登记 `{{HLANG}}` 槽位，金标重签（骨架仍 131 页唯一） |

另有 6 个 orphan 页（GSC：indexed 但无内链），其中 `wpm-test-online.html` 的边界词
`typing words per minute test` 位于 pos 16 —— 该词的**权威页面**已由 3.2 接管，
orphan 不再阻断（orphan 是内链信号，不是排名阻断项）。

## 4. 验证（全部实跑）

| 门禁 | 结果 |
|---|---|
| `verify.py` | **19/19** 通过 |
| 骨架唯一（S1） | 131 页 **1 种**骨架 |
| 金标锁（S3） | `fcce6e7b6d08e03b` 重签 |
| engine harness | 151 passed / 0 failed |
| lang harness | 11 passed / 0 failed |
| `linkops.py live` | 131 URL 全 200 |
| `linkops.py index` | canonical 131/131 自指，异常 0 |
| `linkops.py ledger` | 85 条，校验通过 |
| 线上部署核验 | byline / wiki 引用 / dir=rtl / Last updated 均已在线上 |
| IndexNow | 131 URL 提交，1 batch 成功 |

## 5. 诚实边界（本轮**不会**带来的东西）

- **点击不会立刻上万**。5→? 的变化取决于外链与时间，不取决于再加 10 个页面。
- 边界词从 pos 16/23 进前 3 不是"改文案"能保证的；本轮做的是把它从"无权重"变成"有权重"，
  剩下的是外链和时间。
- `llms.txt` 对 Google 排名无效（Google 2026 官方明确），保留它只是给其他 AI 引擎用。
- 下次复盘的**唯一硬标准**：`python3 src/tools/gsc.py report` 的 pos 是否从 61.2 下降，
  以及那 51 个边界词是否开始出现点击。

## 6. 下一轮优先级（按投入产出比）

1. **外链**是唯一剩余变量。优先：把 6 个已开 PR 推合并（1 个已修好），
   然后是 candidate 里 `dofollow=yes` 的 Startup Fame / Serchen。
2. 等 GSC 数据（2-3 天延迟）后，看 pos 16/23 两个词是否移动 → 决定是否继续集中权重。
3. **不要**再加新页面簇，除非有 GSC 证实的、无对应页的 query。
