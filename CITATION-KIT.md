# CITATION-KIT —— 可引用资产与分发说明

> 这份文件不是"外链话术"，是**可引用的东西 + 谁可能想引用 + 引用时的准确说法**。
> 一切发送动作由你（站主）决定；本文只准备素材，不代替你联系任何人。

---

## 1. 我们手上真正可被引用的东西

| 资产 | URL | 为什么别人愿意引用 |
|---|---|---|
| 基准数据页 | `typing-speed-benchmarks.html` | 两条 DOI、样本量（168,960 / 37,370）、设备对比表、单位换算、明确写出「不写什么」 |
| 公开数据仓 | `github.com/hello532/typing-speed-benchmarks` | CSV + Python/JS 百分位实现，代码可跑，数字可核 |
| 百分位换算 | `typing-speed-percentile.html` | 任意分数 → 百分位；给出近似方法与验证方式（复现作者报告的十分位） |
| 证书说明 | `typing-certificate-acceptance.html` | 把「自签证书不算凭证」讲清楚，是同类站点普遍回避的部分 |
| 12 课课程 | `touch-typing-course.html` | 每课一个 drill + 一个过关标准，可被教师直接采用 |

## 2. 准确的说法（照抄，不要加工）

- 桌面键盘平均 **51.56 WPM**（SD 20.2），未修正错误率 1.17%，样本 **168,960** 人、**136,857,600** 次按键。来源：Dhakal, Feit, Kristensson & Oulasvirta, *Observations on Typing from 136 Million Keystrokes*, CHI 2018，doi:10.1145/3173574.3174220。
- 手机平均 **36.17 WPM**（SD 13.22），未修正错误率 2.34%，样本 **37,370** 人。来源：Palin, Feit, Kim, Kristensson & Oulasvirta, *How do People Type on Mobile Devices?*, MobileHCI 2019，doi:10.1145/3338286.3340120。
- 十分位阈值：最快 10% 超过约 **78 WPM**，最慢 10% 低于约 **26 WPM**（同上 CHI 2018）。
- 换算：WPM × 5 = CPM；CPM × 60 = KPH；WPM × 300 = KPH；8,000 次按键/小时 ≈ **26.7 WPM**。

> 引用时请指向**原始论文**，而不是上面两个链接。我们提供的是整理与换算，不是测量。

## 3. 五类可能引用它的地方（按可行性排序）

| 类型 | 具体形态 | 该发什么 | 不该做什么 |
|---|---|---|---|
| 教育/课堂资源页 | 教师资源聚合、homeschool 列表、typing curriculum 推荐页 | 课程页 + 证书说明页（免费、无账号、无学生数据） | 不要声称"被学校采用" |
| 工具目录 | 有编辑审核的工具站（非自动收录） | 一段事实描述：184 个测试、14 语种、无账号、结果存本地 | 不要堆关键词、不要买"加急审核" |
| 数据引用 | 写"平均打字速度"的博客/统计页 | 两条 DOI + 我们的换算表（对方常在找"数字+出处"） | 不要要求对方必须链我们 |
| 开发者社区 | 讨论打字速度数据、键盘、布局的帖子 | 数据仓（可跑的 percentile 代码） | 不要发广告式链接 |
| 开源项目文档 | 打字/键盘类项目的 README "related" 段 | 一行 + 链接，PR 形式 | 不要一次开多个 PR |

## 4. 一条可直接改写的最小外联文本（≤120 词）

> Hi — I maintain a small open dataset of typing-speed benchmarks, and it may save you a citation hunt:
> 51.56 WPM desktop (SD 20.2, n=168,960, CHI 2018) and 36.17 WPM phone (SD 13.22, n=37,370, MobileHCI 2019), plus the percentile curve and a CSV.
> Repo: github.com/hello532/typing-speed-benchmarks (MIT code; figures belong to the papers).
> Page with context: typing.rerivo.com/typing-speed-benchmarks.html
> No ask — use it or ignore it. Happy to add a different cut of the data if it would help.

最后一句是关键：**不索取链接**。索取会把它变成交换，而交换需要披露，披露就变成付费链接风险。

## 5. 判定：什么时候该继续，什么时候该停

| 观察（`weekly.py`） | 判断 |
|---|---|
| 新进榜查询连续两周增加 | 覆盖在扩，继续做内容与内链 |
| 新进榜查询不增、曝光不增 | 权威度不够，全线转外链，停止加页 |
| 排名涨、点击不涨 | 改标题描述（只对 p11-30 的页有意义） |
| 拿到 3-5 个相关引用后仍无变化 | 检查是否 nofollow / 是否被收录 / 是否只是目录页 |

## 6. 期望值（不给幻想）

一个 GitHub 数据仓 + 5 个真实引用，**不会**把 97 点击变成 2000。它可能把若干长尾查询从 p40 推到 p20，
把 28 天点击从 ~29 推到 ~60-100。2000 需要的是同一个动作重复 20-40 次并且被真实引用，
时间尺度是 3-6 个月，不是 3 天。

这份文件的作用是让那 20-40 次动作**不跑偏**，而不是让它们变快。
