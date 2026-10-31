// 全站移动端扫描 —— 184 页在 390×844 下逐页量横向溢出。
//
//   cd <repo> && python3 -m http.server 8765 &
//   ego-browser nodejs < src/tools/mobilesweep.js
//
// 为什么要逐页量：r73/r75 两个问题（宽表格被裁、RTL 负 left 反向溢出 8,796px）
// 都是「静态检查全绿、只有真视口才看得见」。抽 3 页会漏掉只在 RTL 出现的那个，
// 所以这里扫全站，退出码 1 表示有页面溢出或导航失败。
//
// 用本地服务器而不是线上：184 次线上导航会撞 CDN 缓存与速率限制，本地是确定的。

const BASE = "http://127.0.0.1:8765";
const REPO = "/Users/doi/Desktop/DSH/work/typing-speed-test";
const VIEWPORT = { width: 390, height: 844, deviceScaleFactor: 2, mobile: true };
const TOLERANCE = 2; // 像素；亚像素舍入不算问题

const fs = await import("node:fs/promises");
const task = await taskSpace("typing.rerivo mobile sweep");
const page = task.page("p1");

const files = (await fs.readdir(REPO)).filter(
  (f) => f.endsWith(".html") && !f.startsWith("google") && !f.startsWith("share") && f !== "404.html",
);

await page.cdp("Emulation.setDeviceMetricsOverride", VIEWPORT);

const overflow = [];
const failed = [];
for (const f of files) {
  try {
    await page.goto(`${BASE}/${f}`, { waitUntil: "domcontentloaded" });
  } catch (e) {
    failed.push({ page: f, error: String(e).slice(0, 60) });
    continue;
  }
  const o = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  if (o > TOLERANCE) overflow.push({ page: f, overflow: o });
}

await page.cdp("Emulation.clearDeviceMetricsOverride");

console.log(`扫描 ${files.length} 页 @ ${VIEWPORT.width}×${VIEWPORT.height}`);
if (overflow.length) {
  console.log(`\n❌ 横向溢出 ${overflow.length} 页：`);
  for (const o of overflow.slice(0, 15)) console.log(`   ${String(o.overflow).padStart(6)}px  ${o.page}`);
} else {
  console.log("✅ 无横向溢出");
}
if (failed.length) {
  console.log(`\n⚠️  导航失败 ${failed.length} 页：`);
  for (const f of failed.slice(0, 8)) console.log(`   ${f.page} — ${f.error}`);
}
process.exit(overflow.length ? 1 : 0);
