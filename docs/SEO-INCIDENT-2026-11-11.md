# 事故复盘：2026-10-28 全站曝光归零

## 观测（GSC API，2026-11-11 抓取）

- 曝光曲线：10-19 307 → 10-20 353 → 10-21 381 → 10-22 454 → 10-23 470 → 10-26 374 → **10-27 149 → 10-28 3 → 之后 0–2/天**
- 点击：10-27 之后基本为 0
- 首页 URL Inspection：`verdict = NEUTRAL`，`coverageState = "Crawled - currently not indexed"`，`lastCrawlTime = 2026-10-29T10:02:30Z`
- `robotsTxtState = ALLOWED`，`indexingState = INDEXING_ALLOWED`，`pageFetchState = SUCCESSFUL`
- sitemap：`submitted 184 / indexed 0`
- 站点在 10-20 → 11-01 之间**没有任何提交**，因此不是自身技术改动导致

## 判断

技术层无阻断（robots 允许、抓取成功、canonical 自指正确）→ 站点级**质量判定**。
184 页里 52 页是同一模板套出来的角色/考试/词表变体（`typing-test-for-*`、
`bank-typing-test`、`top-en-words` 等），命中 Google「scaled content abuse」
的形态特征。抓取时间 10-29 与曝光归零 10-28 完全吻合。

**待人工确认（API 读不到）**：GSC → 安全和手动操作 → 手动操作。
若有一条针对本资源的手动处置，说明是人工判定，恢复要等复查通过；若为空，
说明是算法性降权，靠内容整改 + 时间恢复。两种情况的本轮整改内容相同。

## 已做（r108 / r109，2026-11-11 部署）

1. 删除 52 个同模板变体页，184 → 132；四处同步（pages.json / clusters.json / llms.txt / 产物），21 处内链改指幸存页
2. 新增 contact / terms / editorial-policy 三个信任页（E-E-A-T + AdSense 要求）
3. 重写隐私政策：原文写「没有广告像素、没有第三方追踪」，与已部署的 AdSense 直接矛盾
4. sitemap 重新提交 + IndexNow 推送 135 个 URL（HTTP 200）

## 恢复预期

- 重新抓取通常 3–14 天；站点级质量判定的恢复通常需要 **2–8 周**，且不保证
- 观察指标：GSC 首页 verdict 从 `NEUTRAL` 变 `PASS`，sitemap 的 `indexed` 从 0 开始上升
- 不要在此期间继续加页。**下一步是继续减页 + 加深核心页，不是扩张**

## 下一步（按优先级）

1. 人工看 GSC 手动操作页（2 分钟），有处置就准备复查申请
2. 再砍一轮：把 135 页里正文 < 900 词、且 90 天曝光 ≤ 5 的页面合并掉，目标 60–70 页
3. 核心 8 页（首页 / 1-minute / average-typing-speed / words-per-minute / typing-practice / benchmarks / keystrokes-per-hour / typing-tests）各补一节只此页才有的内容
4. 外链：现有 88 条台账里 dofollow 比例与来源质量要复核，低质目录链比没有更糟
