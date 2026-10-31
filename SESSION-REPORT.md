# SESSION REPORT — 2026-10-31 / 11-01

> 一晚的连续工作记录，压缩成一页。细节在 `ROUND-22.md`，计划在 `PLAN-90-DAY.md`，
> 竞品对标原文在 `work/competitors-top50.md`。

## 结果先说

| 项 | 开工 | 现在 |
|---|---|---|
| 页面数 | 131 | **184** |
| 正文中位数 | 2,583 字符 | **2,541 字符**（最小 1,513，privacy 除外） |
| 页均 FAQ | 3.9 条 | **5.0 条** |
| 门禁 | 20/20 | **20/20** |
| 站点体检 | —（无此工具） | **12/12** |
| 真浏览器交互验收 | — | **9/9** |
| 移动端横向溢出 | 未知 | **184 页 0 处**（390 / 320 / 横屏各扫一遍） |
| 移动端 CLS | 0.14 | **0.006**（390）/ 0.024（320） |
| 部署一致性 | 未知 | **184/184 逐字节一致** |
| 外链台账 | 87 条 | **88 条**（新增 1 个公开数据仓） |

**2000 点击/28 天没有达成，也不会因为站内再改而达成。** 见文末。

## 站内做了什么（按杠杆分组）

1. **可竞争查询面**：+53 页，全部落在「小站也能进首页」的族——KPH/净 WPM/百分位、
   联邦/SSC/CritiCall/护理/调度/法务、30–100 WPM 目标速度、SQL/TS/Rust/Go/Excel 代码池、
   德/法语种、12 课课程、一致性指标、平台期诊断、工位人体工学。
2. **可引用性（GEO）**：两条 DOI（CHI 2018 / MobileHCI 2019）、百分位曲线、CSV、
   `Dataset` 结构化数据、`HowTo`、每页 TL;DR 163/184、长页目录、`llms.txt` 42KB 含
   8 条 Quick answers、`llms-full.txt`、每页 `.md` 镜像。
3. **内链**：目录页由 clusters 生成（162 条正文内链）；首页到任意页 ≤2 跳；
   给 6 个「有曝光但入链极少」的页面补了 11 条语义相邻链接。
4. **技术**：`dateModified` 由 git 历史派生（不再全站写死）；表格横向滚动容器；
   RTL 屏外定位溢出修复；header/打字区预留高度消除 CLS；标题层级跳级清零。

## 站外做了什么

一个公开数据仓 **github.com/hello532/typing-speed-benchmarks**：两条 DOI、CSV 曲线、
`percentile.py` / `percentile.js`（两实现结果逐位一致）、README 明确「引用论文而不是这个仓库」。
这是唯一一种不联系任何人、不买链接就能拿到的主题相关引用。

## 这一晚真正的收获是工具，不是页面

四个问题全部是**静态检查全绿、只有真浏览器/真视口才看得见**：

| 问题 | 只有哪种检查能发现 |
|---|---|
| 目录筛选器计数变了但列表不动 | 真浏览器（脚本在目标解析前执行） |
| 宽表格最后一列被裁 | 真视口 + 量元素尺寸 |
| RTL 页能横拖 8,796px | RTL 视口 + 量文档 scrollWidth |
| 全站 h1→h3 跳级 | 解析标题序列（不是看渲染） |

所以它们现在都是脚本：`browsercheck.js` / `mobilesweep.js` / `cwv.js` / `health.py` /
`deploysync.py` / `linkout.py` / `weekly.py` / `gauges.py` / `roadmap.py` / `linkgraph.py`。
下次改动跑一遍，就不必靠记性。

## 2000 点击缺什么（算术）

```
现在   97 点击 / 5,612 曝光 / CTR 1.73% / 平均排名 56.4
其中   68 次点击来自首页的匿名查询（CTR 65%，品牌/导航型行为）
可归因的非品牌点击 ≈ 29 次

2000 点击需要：
  CTR 3% → 66,667 曝光（×11.9）
  CTR 5% → 40,000 曝光（×7.1）
```

CTR 35% 只有品牌词能达到，所以唯一现实组合是 **曝光 ×6 以上 + CTR 3–6%**。
而曝光放大 6 倍只能来自「更多查询把我们排进前 20」——那是引用域名的函数，不是内容的函数。

**站内能做的已经做到这个域名的上限。** 剩下的是：外链、时间、以及等 Google 重新评估。

## 每周该跑的

```bash
python3 src/tools/weekly.py          # 只看「新进榜查询」这一个信号
python3 src/tools/gauges.py          # 今天先改哪页（uplift 排序）
python3 build.py && python3 verify.py && python3 src/tools/health.py
python3 src/tools/deploysync.py      # 线上是否真的是这一版
```

浏览器/视口类检查（需要本机 ego-browser 与本地服务器）：

```bash
python3 -m http.server 8765 &
ego-browser nodejs < src/tools/browsercheck.js
ego-browser nodejs < src/tools/mobilesweep.js
ego-browser nodejs < src/tools/cwv.js
```
