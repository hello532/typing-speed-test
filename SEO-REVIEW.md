# 资深复核：前 40 轮哪里做错了，现在改了什么

> 这一页不是成绩单，是**自我批评 + 修正记录**。写完前 40 轮之后回头看，
> 有三处做法经不起资深视角的追问，其中一处是真错误（已修）。

## 一、真错误：语种页把英文当成本地语输出（已修）

**证据**：`src/pools/{ar,es,hi,zh}.json` 里各有 30 条英文模板句（形如
`the steady click teaches patience to willing fingers (ar-0).`）和 10 条带英文署名的引文
（`— coach`）。四个语种页各有 100 条句子、100 条引文，其中 40 条是英文填充。

**后果**：页面标题写「Arabic Typing Test」，描述写「real Arabic sentences」，
实际打出来的是英文。这不只是体验问题——它是「页面承诺与实际内容不符」，
在任何人看来都是模板化填充的典型特征。

**修法**：删掉 160 条填充（四页各 30 句 + 10 引文）。修完实测非 ASCII 占比
阿拉伯 0.67 / 印地 0.81 / 中文 0.51，德语 0.01、西班牙 0.02（这两个本就该接近 ASCII）。

## 二、真错误：hreflang 与 dir 都标错了层级（已修）

| 问题 | 之前 | 现在 | 依据 |
|---|---|---|---|
| hreflang | 14 页互相声明 `hreflang=en/es/zh/...`，而每页 `<html lang="en">`、正文全英文 | `langVariants:false`，不再输出聚类 | 语言变体必须是真的不同语言版本；自相矛盾的标注只会被忽略 |
| dir | `<html lang="en" dir="rtl">`，整个英文界面被翻转 | `<html lang="en">` 不动；`#text` 承担 `lang`（ar/ur 另加 `dir="rtl"`）；`header.top` 承担 UI 语言 | 方向与语言属于那段文字，不属于整页；r75 的 8,796px 横向溢出就是整页 RTL 造成的 |

`ui.js` 的 `setLang` 同步改掉运行时翻转。修后 320 / 390 复测：横向溢出 0，文档方向恒为 LTR。

## 三、方法论错误：把「多写页面」当成了主要杠杆

前 40 轮里我加了 53 页。资深视角看，这是**在错误的阶段做正确的事**：

- 站点只有 29 次可归因的非品牌点击，说明还没建立任何排名立足点；
- 没有立足点时，184 页与 131 页对 Google 的意义几乎一样——都是「这个域名还没被评估过」；
- 而页数越多，每个 URL 分到的抓取与内链权重越少。

**更该做的是**：挑 8 页集中打透（见第五节），其余页面维持现状不再加厚。
第 31–39 轮我做的连续补厚，本质上还是在「多写」，只是选点更准。

## 四、一个被数据否掉的假设：关键词自相残杀

我原本打算做合并（301）来消除 cannibalization。先拉数据验证：GSC 28 天 `query × page`。

```
query×page 行数 1,913 ｜ 被 2 个以上自家页面命中的查询：272 个
```

看起来很多，但看位置就清楚了：

| 查询 | 自家页面（曝光, 位置） |
|---|---|
| typing practice | typing-practice（70, **p94.8**）· keyboard-practice（14, **p93.3**） |
| online typing practice | typing-practice（51, **p98.4**）· keyboard-practice（33, **p88.1**） |
| wpm test free | 1-minute（24, p71.1）· free-typing-test（6, p83.5） |

**全部在 p70 以后。** 自相残杀的前提是两个页面争同一个前 20 的名次；当所有页面都在第 7–10 页时，
它们不是在竞争，而是一起缺席。**合并只会销毁内容，不会换来名次。**

结论：不做合并。这是一个「本来打算动手、被数据拦下」的决定，比动手更值钱。

## 五、SERP 形态错配：有些页面注定赢不了

查了 `ssc chsl typing test 35 wpm passage` 的实际竞品（RealMocks 85 篇分级范文、
cgltyping.in 段落库、currentaffairspulse 逐条引用官方通知与判分规则、
sarkariexamtyping 支持 Hindi Mangal 字体与类别分档、typingnation 的 TCS iON 模拟器）。

**这个 SERP 要的是「带题库的模拟器」，不是「一篇文章」。** 我们那页是文章，
再补 2,000 字也赢不了——缺的是产品能力（段落库、判分规则、字体、计时模拟），不是文案。

这条推论对所有考试类页面成立：它们的产品形态决定了上限。写内容之前先看 SERP 是
**文章型**（前 10 是博客/指南）还是**工具型**（前 10 是交互页面/数据库），
形态不对就不要投入。

## 六、接下来该做的（按优先级）

1. **集中打透 8 页**——这是唯一还有位置空间的页面（p11–30，实测）：
   `cpm-typing-test`（p19.0）· `government-typing-test`（p27.2）· `top-1000-english-words`（p28.3）
   · `how-to-pass-a-typing-test`（p28.3）· `2-minute-typing-test`（p27.8）· `bigram-typing-practice`（p12.3）
   · `touch-typing-for-adults`（p21.0）· `korean-typing-test`（p23.8）
2. **不要再加页面。** 184 页已覆盖查询面，新增只会稀释。
3. **工具型 SERP 要么做产品要么放弃**：考试类页面若不做段落库与判分模拟，就不该再投内容。
4. **外链**仍是唯一能改变量级的变量，需要你的账号与授权。

## 附：这一轮改动的验证

```
build --check  OK: all 184 pages match src/
verify         20/20（骨架金标重签 a19637e964d698f1）
health         12/12
deploysync     抽样 12 页逐字节一致（已部署）
browsercheck   9/9
mobilesweep    320 / 390 / 横屏 横向溢出 0
```
