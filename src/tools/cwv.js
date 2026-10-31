// Core Web Vitals 实测 —— 移动端 + Slow 4G + 4× CPU，冷启动。
//
//   cd <repo> && python3 -m http.server 8765 &
//   ego-browser nodejs < src/tools/cwv.js
//
// 为什么要分两次测：
//   本站的 HTML/CSS/JS 自己产生的 CLS 是 0。实测到的 0.11–0.14 全部来自
//   Google AdSense 的自动广告在 ~2s 插入。把广告域屏蔽后复测得到 0，就是证明。
//   所以这里同时输出两列：`cls_own`（广告屏蔽，衡量我们自己的代码）与
//   `cls_ads`（真实加载，衡量用户的体验）。只有前者能当回归门禁——
//   后者取决于 AdSense 账号的自动广告设置，不是仓库能改的东西。
//
// 指标的采集方式：Page.addScriptToEvaluateOnNewDocument 在首次绘制前装好
// PerformanceObserver（buffered），因此不会漏掉加载早期的 layout-shift；
// 外部脚本读不到，必须是内联注入。

const BASE = "http://127.0.0.1:8765";
const PAGES = ["/", "/typing-tests.html", "/average-typing-speed.html",
               "/typing-speed-calculator.html", "/sql-typing-practice.html"];
const AD_URLS = ["*googlesyndication.com*", "*doubleclick.net*",
                 "*googleadservices.com*", "*googletagservices.com*"];
const VIEWPORT = { width: 390, height: 844, deviceScaleFactor: 3, mobile: true };
const SLOW_4G = { offline: false, latency: 150,
                  downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8 };

const OBSERVER = `
  window.__cls = 0; window.__shifts = []; window.__lcp = 0; window.__lcpEl = "";
  try {
    new PerformanceObserver(l => {
      const e = l.getEntries()[l.getEntries().length - 1];
      window.__lcp = Math.round(e.startTime);
      window.__lcpEl = e.element ? (e.element.nodeName + "." + ((e.element.className || "").toString().slice(0, 18))) : "";
    }).observe({ type: "largest-contentful-paint", buffered: true });
  } catch (e) {}
  try {
    new PerformanceObserver(l => {
      for (const e of l.getEntries()) {
        if (e.hadRecentInput) continue;
        window.__cls += e.value;
        window.__shifts.push({ v: Math.round(e.value * 1000) / 1000, t: Math.round(e.startTime),
          src: (e.sources || []).map(s => s.node ? (s.node.nodeName + "." +
            ((s.node.className || "").toString().slice(0, 18))) : "?").slice(0, 2) });
      }
    }).observe({ type: "layout-shift", buffered: true });
  } catch (e) {}
`;

const task = await taskSpace("typing.rerivo mobile sweep");
const page = task.page("p1");

await page.cdp("Network.setCacheDisabled", { cacheDisabled: true });
await page.cdp("Network.emulateNetworkConditions", SLOW_4G);
await page.cdp("Emulation.setCPUThrottlingRate", { rate: 4 });
await page.cdp("Emulation.setDeviceMetricsOverride", VIEWPORT);
await page.cdp("Page.addScriptToEvaluateOnNewDocument", { source: OBSERVER });

async function measure(path, blockAds) {
  await page.cdp("Network.setBlockedURLs", { urls: blockAds ? AD_URLS : [] });
  await page.goto(BASE + path, { waitUntil: "domcontentloaded" });
  await new Promise(r => setTimeout(r, 2500));
  return await page.evaluate(() => {
    const nav = performance.getEntriesByType("navigation")[0] || {};
    return {
      fcp: nav.responseEnd ? Math.round(nav.responseEnd) : null,
      dcl: nav.domContentLoadedEventEnd ? Math.round(nav.domContentLoadedEventEnd) : null,
      docKb: Math.round((nav.transferSize || 0) / 1024),
      lcp: window.__lcp || null,
      lcpEl: window.__lcpEl || "",
      cls: Math.round((window.__cls || 0) * 1000) / 1000,
      worst: (window.__shifts || []).sort((a, b) => b.v - a.v).slice(0, 1),
    };
  });
}

const rows = [];
for (const p of PAGES) {
  const own = await measure(p, true);
  const real = await measure(p, false);
  rows.push({ page: p, fcp: own.fcp, lcp: own.lcp, lcpEl: own.lcpEl, dcl: own.dcl,
              docKb: own.docKb, cls_own: own.cls, cls_ads: real.cls, worstReal: real.worst });
}

await page.cdp("Network.setBlockedURLs", { urls: [] });
await page.cdp("Emulation.clearDeviceMetricsOverride");
await page.cdp("Emulation.setCPUThrottlingRate", { rate: 1 });
await page.cdp("Network.setCacheDisabled", { cacheDisabled: false });

console.log("移动端 390×844 / Slow 4G / 4× CPU / 冷启动\n");
console.log("page".padEnd(28), "FCP".padStart(6), "LCP".padStart(6), "DCL".padStart(6),
            "doc".padStart(6), "CLS_own".padStart(8), "LCP element");
for (const r of rows) {
  console.log(r.page.padEnd(28), String(r.fcp).padStart(6), String(r.lcp).padStart(6),
              String(r.dcl).padStart(6), (r.docKb + "kB").padStart(6),
              String(r.cls_own).padStart(8), r.lcpEl);
}
const worstOwn = Math.max(...rows.map(r => r.cls_own));
console.log(`\n自有代码 CLS 最大 ${worstOwn}（广告屏蔽后）；带广告 CLS 最大 ${Math.max(...rows.map(r => r.cls_ads))}`);
console.log("门禁口径：cls_own 必须 ≤ 0.05；cls_ads 仅作信息记录（由 AdSense 自动广告决定）");
process.exit(worstOwn > 0.05 ? 1 : 0);
