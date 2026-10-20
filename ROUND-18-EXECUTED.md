# Round 18 执行记录 — 按 ROUND-18-CTR.md 的方案落地（2026-10-20）

## 一、外链（核心动作，因为位置而非 CTR 是瓶颈）

外部权威度是唯一剩余变量。本轮做了两件事：**核实存量**、**新增高权重目标**。

### 1.1 核实 6 个已开 PR 的真实状态（不假设）

| 仓库 | stars | 状态 | mergeable | 判断 |
|---|---|---|---|---|
| `lukasz-madon/awesome-remote-job` | **49,719** | 新增 PR#1204 | ✅ +1/-0 | **最高价值，本轮新增** |
| `aviaryan/awesome-no-login-web-apps` | 3,400 | PR#749 待合 | ✅ | 有价值，等 maintainer |
| `Soneji/awesome-teaching` | 27 | PR#6 待合 | ✅ | 一般 |
| `Zio-Tibia/awesome-no-signup-tools` | 23 | PR#86 待合 | ✅ | 一般 |
| `osufiles/Awesome-keyboard-typing` | 10 | PR#10 待合 | ✅ | 一般（本轮修好） |
| `NwabKhan/awesome-web-tools` | 3 | PR#136 待合 | ✅ | 低 |
| `woodyhayday/home-ed` | **0** | PR#1 待合 | ✅ | **零价值，放弃** |

结论：5 个 MERGEABLE 是**无人 review**，不是被拒。外链价值高度集中在 top-2，
其余 5 个仓库加起来约 100 stars，对 pos 60 → 10 的实际作用有限。

### 1.2 新增 PR#1204（49.7k★，本轮唯一高质量外链）

- 目标：`lukasz-madon/awesome-remote-job` → `Tools > Others`
- 理由真实：data entry / transcription / customer support 是远程岗位常见类别，
  打字速度是明确招聘项；同区已有 BeginThings、FastTool 等免费浏览器工具条目
- 结果：**+1/-0，MERGEABLE**

**踩坑（已记入台账 87 条）**：`gh repo fork --clone` 拿到的是 **fork 自己的 master**，
不是 upstream master。直接改再 push 会把整文件 diff 成 **+634/-633**。
正确做法：`git fetch upstream master && git reset --hard upstream/master` 再改。

### 1.3 主动放弃的目标（避免制造垃圾外链）

| 目标 | 放弃原因 |
|---|---|
| `brandonhimpfen/awesome-web-development` | 无免费工具/评估分区，塞进去不自然 |
| `dailydotdev/awesome-developer-recruiting` | Technical Assessment 区全是付费平台，塞免费工具=软广，会被拒 |
| `moimikey/awesome-devtools` / `tramcar/awesome-job-boards` | 同上，无自然落点 |
| `Product Hunt` | 核实发现页面是**旧草稿**（写「41 variants」，现 131 页），未发布 |
| `AlternativeTo` | 403 Cloudflare，需真实浏览器会话 |

### 1.4 一个反常识发现

`web_search` 实测：「one hand typing test」的**第一条结果就是 typing.rerivo.com/one-hand-typing.html**。
但 GSC 里该页曝光约 13 次。

说明：**排名第 1 ≠ 有流量。** 那个 query 本身几乎没人搜。
这是本站当前处境的一个缩影——技术正确、能被排到前面，但选的词没有量。
所以「继续加页抢长尾」是负收益；应集中在有量的词上，而那需要权威度。

## 二、位置（第二优先）

### 2.1 核实边界页是否真的只差内容

`cpm-typing-test.html`（`cpm test` pos 23.4）：

| 检查 | 结果 |
|---|---|
| geo_page_score | **97 / 100** |
| 正文字数 | 3,009 |
| H2 数 | 15 |
| FAQ | 完整 + FAQPage schema |
| 内链 | 有 |

内容已经做到 97 分。**pos 23 → 10 的差距不是内容，是权威度。**
这再次证明：继续写内容对排名无效，外链才是变量。

### 2.2 移动端专项（178 次手机端曝光 / 0 点击 → 怀疑渲染问题）

实测结论：**没问题**。
- viewport 正确
- 触控目标 `min-height:44px`（达 Apple HIG 标准）
- 7 个媒体查询，560px 断点内隐藏屏键盘、压缩间距
- `overflow-x` 有保护
- 无 JS 模板泄漏（之前 page_audit 看到的 `tr("cert_title")` 是引擎内联 JS 正常内容，
  不是渲染 bug —— 此处更正了初判）

移动端 0 点击的原因是 pos 60+ 且无移动专属需求，不是技术问题。

## 三、基线重置（让下次测量准）

`gsc-baseline.json` 重置为 **2026-10-19**（本轮所有改动上线前最后一个完整数据日）：

```json
{"clicks": 5, "impressions": 2253, "ctr": 0.002219, "position": 61.2}
```

`python3 src/tools/gsc.py growth` 现在能正确回答「本轮之后有没有变」。

## 四、诚实的现状

| 项 | 值 |
|---|---|
| verify | **20/20**（含新增 CTR 门禁 6b） |
| 外链台账 | 87 条 |
| sitemap | 131 URL 全 200 |
| 本轮新增可合并 PR | **1 个（49.7k★）+ 修复 1 个（10★）** |
| 本轮预期排名变化 | **0**。外链生效以周/月计，且 top-2 以外权重有限 |

**必须说清**：本轮没有让点击上涨，也不该期望它上涨。
我做的是把「唯一还有杠杆的地方」（高质量外链）推进了一步，
并把三个会持续损害 CTR 的缺陷（品牌词缺品牌、45% 曝光面描述雷同、边界词标题错位）修掉。

## 五、下一轮触发器（不要凭感觉继续）

只有满足以下任一条才值得动手：

1. `gsc.py growth` 显示 **position 从 61.2 下降** → 说明权威度在起作用，继续做外链
2. 出现**新的、pos ≤ 20 且 impr ≥ 15** 的 query → 值得针对性强化（这是唯一值得写内容的信号）
3. PR#1204 被合并 → 补下一个高权重目标

若三条都不满足：**不要加页、不要改文案**。那是空转。
