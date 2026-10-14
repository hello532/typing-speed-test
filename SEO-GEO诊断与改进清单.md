# SEO/GEO 诊断与改进清单

> 基线：GSC 2026-09-16 ~ 2026-10-13（28 天）· 采集于 2026-10-14
> 目标：CTR 与收录量提升 200%（= 3×）

## 一、真实基线（不是猜测，来自 GSC API）

| 指标 | 值 |
|---|---|
| 点击 | **4** |
| 曝光 | **1197** |
| CTR | **0.33%** |
| 平均排名 | **56.6** |
| sitemap | 49 URL，0 错误 0 警告 |
| 编制索引 | 23 已编入 / 13 未编入（11 crawled_not_indexed + 2 discovered） |
| 有曝光的页 | 23 / 49（20 页从未出现） |

## 二、关键发现：**49 页其实都已被索引**

用 `site:` 抽查 + GSC 180 天数据交叉验证：`chinese-typing-test`、`typing-certificate`、`typing-tutor` 等「未曝光」页**都能被 Google 搜到**。

→ 所以「提升收录」的真实含义**不是**让现有页被收录（已收录），而是：
1. 让已收录但排名差的页**往上走**（现在 81% 曝光在 pos>50）
2. 扩大**可被索引的覆盖面**（新增有真实需求、但当前无页面的查询簇）

## 三、曝光的位置分布（决定 CTR 的物理上限）

| 位置 | 曝光 | 点击 | 实测 CTR |
|---|---|---|---|
| 1–3 | 10 | 1 | 10.00% |
| 4–10 | 77 | 1 | **1.30%** |
| 11–20 | 22 | 0 | 0% |
| 21–30 | 37 | 0 | 0% |
| 31–50 | 66 | 0 | 0% |
| **50+** | **925** | 1 | 0.11% |

**结论**：81% 的曝光落在 pos>50，那里的天然 CTR 只有 ~0.1%。**排名是 CTR 的主导变量**，而排名由权重（外链）决定 → 这是长线。

可立即改善的是 pos 4–10 那 77 次曝光：实测 CTR 1.30%，而该位置正常应有 2–5% → **snippet 有问题，属于可直接修复的缺口**。

## 四、已定位的四个可修复缺口

### 缺口 1：标题与真实查询不匹配（CTR 直接原因）

| 页面 | 现标题 | 真实查询 | 缺口 |
|---|---|---|---|
| words-per-minute-test | Words Per Minute Test - Free Typing WPM Test Online | `typing words per minute test`（27 imp, pos 8.7） | 标题缺 `typing` 前置；pos 8.7 却 0 点击 |
| 1-minute-typing-test | 1 Minute Typing Test - Free 60 Second WPM… | `one minute typing test`（9 imp, pos 3.3） | 标题无 `one minute` 变体 |
| 2-minute-typing-test | 2 Minute Typing Test - Free 2 Min WPM Test | `typing test 2 minutes`（pos 15.8） | 语序不匹配 |
| typing-tips | Typing Tips - Practical Tips to Type Faster… | `how to type faster and more accurately`（pos 25.7） | 标题无 `how to` |
| free-typing-test | Free Typing Test - No Sign Up, Instant WPM | `free typing test wpm`（pos 48.4） | 缺 wpm 语义 |

### 缺口 2：内链锚文本浪费

页脚 48 条全站内链的锚文本是 **`30s` / `1 min` / `2 min` / `WPM` / `Numbers`** 这类缩写：

```html
<a href="1-minute-typing-test.html">1 min</a>
<a href="words-per-minute-test.html">WPM</a>
```

锚文本是重要的相关性信号，`1 min` 远不如 `1 minute typing test` 有效。**全站 48×49 = 2352 个锚点全部被浪费。**

### 缺口 3：正文偏薄

正文词数中位 **654**，最小 519。且是模板生成，19 个「未覆盖查询簇」没有对应页面。

未被覆盖但有真实曝光的查询簇：

| 查询簇 | 曝光 | 是否有页面 |
|---|---|---|
| `assessment` / `assessments`（typing assessment free 等） | 34 | **无** |
| `quiz`（typing quiz free） | 6 | **无** |
| `courses` / `techniques` / `skills` | 8 | **无** |
| `ten key punch`（数字小键盘） | 2 | **无**（与 number-typing-test 意图不同） |

### 缺口 4：外链 0 条已生效

台账 46 条：submitted 10 / candidate 14 / blocked_cf 7 / needs_login 15，**已生效 0 条**。
→ 这是排名（进而 CTR）的真因，但需要外部审核，**不是本地改代码能解决的**。

## 五、改进方案（按杠杆排序）

| # | 动作 | 影响 | 可本地完成 |
|---|---|---|---|
| 1 | 重写 title/metaDesc 匹配真实查询 | CTR ↑（pos 4–10 的 1.30% → 目标 2.5%+） | ✅ |
| 2 | 页脚锚文本改为描述性关键词 | 内链权重与相关性 ↑ | ✅ |
| 3 | 薄页内容加深（独特数据/对比/步骤） | 排名 ↑ | ✅ |
| 4 | 新增 2–3 个有真实需求的页面（assessment / quiz） | 收录面 ↑ | ✅ |
| 5 | IndexNow 重提 + GEO 清单刷新 | 重抓速率 ↑ | ✅ |
| 6 | 外链推进（14 candidate + 15 needs_login） | **排名真因** | ❌ 需外部 |

## 六、必须说清的三件事

1. **不会批量生成 100+ 页**。本站是模板生成站，而 Google 垃圾内容政策明确打击「规模化内容滥用（用 AI 批量生成大量低质量页面）」。为凑「收录量 200%」而扩到 150 页，风险是全站被降权。→ 只新增「有真实需求 + 内容确实不同」的少数页面。

2. **CTR 的 200% 需要 2–4 周 GSC 数据才能验证**。GSC 有 ~3 天延迟，当前基数只有 4 点击，单点噪声极大（多 4 个点击就是 +100%）。今天能做的是把**可控代理指标**改到位（标题覆盖率、锚文本质量、内容深度），真实 CTR 待观察。

3. **主导 CTR 的是排名，排名的主导是外链**。本地能做的只是把「已经排上来的曝光」转化成点击；要让 925 次 pos>50 的曝光上移，必须解决外链——那 15 条 needs_login 需要人工登录提交。
