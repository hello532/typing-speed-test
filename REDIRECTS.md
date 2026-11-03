# 合并页的跳转桩（不是 build.py 产物，别删）

build.py 只写 src/pages.json 里的页；下面 4 个 URL 已合并进更强的同意图页，
线上保留一个静态 meta-refresh + canonical 桩，让已收录的地址转权重、用户不撞 404：

| 旧 URL | 目标 |
|---|---|
| easy-typing-test.html | beginner-typing-test.html |
| ssc-chsl-typing-test.html | ssc-typing-test.html |
| 10000-keystrokes-per-hour-test.html | keystrokes-per-hour-test.html |
| wpm-to-kph-converter.html | keystrokes-per-hour-test.html |

依据（GSC 2026-10-06~11-02）：这 4 页 28 天曝光为 0，同意图的存活页有曝光
（beginner 37 次 / p29.7，KPH 56 次 / p29.6），SSс 两页均 0 且 CHSL 是 SSC 的子集。
新增合并时：从 src/pages.json 和 src/clusters.json 删条目 → build.py → 删 .md →
写同样的桩 → make sure llms.txt 里那条也删掉（llms.txt 是手工维护的）。
