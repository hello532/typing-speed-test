// 线上交互验收 —— 在真浏览器里点一次，而不是只看构建产物。
//
//   ego-browser nodejs < src/tools/browsercheck.js
//
// 为什么需要它：`node --check` 只能证明语法合法。r69 抓到的筛选器 bug
// （脚本在目录解析前取空 NodeList，计数变了但列表不动）语法完全合法，
// 只有真浏览器跑一遍才看得见。所以每加一处交互，都要跑这个脚本。
//
// 退出码：0 全部通过；1 有检查失败（可直接挂 CI，但需要真浏览器环境）。
// 说明：这里刻意不引入任何依赖，只用 ego-browser 暴露的 taskSpace / page API。

const SITE = "https://typing.rerivo.com";
// 每次运行加一个变化的查询串，绕开静态站 CDN 的 10 分钟缓存
const BUST = `?bc=${Date.now()}`;

const checks = [];
function record(name, ok, detail) {
  checks.push({ name, ok, detail });
}

const task = await taskSpace("typing.rerivo browser check");
const page = task.page("p1");

async function open(path) {
  await page.goto(SITE + path + BUST);
}

// 1) WPM ↔ KPH 双向换算
try {
  await open("/wpm-to-kph-converter.html");
  const r = await page.evaluate(() => {
    const w = document.getElementById("convWpm");
    const k = document.getElementById("convKph");
    const o = document.getElementById("convOut");
    if (!w || !k || !o) return { ok: false, reason: "inputs missing" };
    w.value = 50;
    w.dispatchEvent(new Event("input", { bubbles: true }));
    const fromW = { kph: k.value, text: o.textContent };
    k.value = 12000;
    k.dispatchEvent(new Event("input", { bubbles: true }));
    return { ok: true, fromW, fromK: { wpm: w.value, text: o.textContent } };
  });
  record("converter: 50 WPM → 15,000 KPH",
    r.ok && r.fromW.kph === "15000", r.fromW);
  record("converter: 12,000 KPH → 40 WPM",
    r.ok && r.fromK.wpm === "40", r.fromK);
} catch (e) {
  record("converter", false, String(e).slice(0, 120));
}

// 2) 速度计算器：gross / net / CPM / KPH / 百分位
try {
  await open("/typing-speed-calculator.html");
  const r = await page.evaluate(() => {
    const c = document.getElementById("calcChars");
    if (!c) return { ok: false };
    c.value = 400;
    document.getElementById("calcErr").value = 4;
    document.getElementById("calcSec").value = 120;
    c.dispatchEvent(new Event("input", { bubbles: true }));
    return { ok: true, text: document.getElementById("calcOut").textContent };
  });
  // 400 字符 / 4 错 / 120 秒 → 40 gross、39.6 net、200 CPM、12,000 KPH
  record("calculator: 400 chars / 4 errors / 120 s",
    r.ok && /40(\.0)? WPM gross/.test(r.text) && /39\.6 WPM net/.test(r.text) && /12,000 KPH/.test(r.text),
    r.text);
} catch (e) {
  record("calculator", false, String(e).slice(0, 120));
}

// 3) 目录筛选器：三态（有匹配 / 另一匹配 / 清空）
try {
  await open("/typing-tests.html");
  const r = await page.evaluate(() => {
    const i = document.getElementById("testFinder");
    if (!i) return { ok: false };
    const count = () => document.querySelectorAll("ul.catalog li:not([hidden])").length;
    const before = count();
    i.value = "nurse"; i.dispatchEvent(new Event("input", { bubbles: true }));
    const nurse = { n: count(), out: document.getElementById("finderOut").textContent };
    i.value = ""; i.dispatchEvent(new Event("input", { bubbles: true }));
    const cleared = { n: count(), out: document.getElementById("finderOut").textContent };
    return { ok: true, before, nurse, cleared };
  });
  record("directory filter: 'nurse' narrows the list",
    r.ok && r.nurse.n > 0 && r.nurse.n < r.before, r.nurse);
  record("directory filter: clearing restores every entry",
    r.ok && r.cleared.n === r.before, r.cleared);
} catch (e) {
  record("directory filter", false, String(e).slice(0, 120));
}

// 4) 语种接线：德语页必须默认德语池
try {
  await open("/german-typing-test.html");
  const r = await page.evaluate(() => {
    const pool = window.TR && window.TR.pool ? window.TR.pool("de") : null;
    return { ok: !!pool, lang: window.TR && window.TR.lang,
             first: pool ? pool.sentences[0].slice(0, 24) : null };
  });
  record("german page: language pool wired",
    r.ok && r.lang === "de", r);
} catch (e) {
  record("german page", false, String(e).slice(0, 120));
}

// 5) 每页必备的结构信号（抽样，防止模板回归）
try {
  await open("/typing-speed-benchmarks.html");
  const r = await page.evaluate(() => ({
    title: document.title.length,
    canonical: (document.querySelector('link[rel="canonical"]') || {}).href || null,
    h1: document.querySelectorAll("h1").length,
    jsonld: document.querySelectorAll('script[type="application/ld+json"]').length,
    toc: !!document.querySelector('nav.toc'),
  }));
  record("benchmarks page: canonical + h1 + JSON-LD + TOC",
    r.h1 === 1 && r.jsonld >= 3 && r.toc && (r.canonical || "").endsWith("typing-speed-benchmarks.html"),
    r);
} catch (e) {
  record("benchmarks page", false, String(e).slice(0, 120));
}

const failed = checks.filter(c => !c.ok);
for (const c of checks) {
  console.log(`${c.ok ? "✅" : "❌"} ${c.name}`);
  // 只在失败时打印细节：ego-browser 的 Node 进程不继承 shell 环境变量，
  // 所以这里不放 verbose 开关，避免给出一个永远不生效的选项。
  if (!c.ok) {
    console.log("    ", JSON.stringify(c.detail));
  }
}
console.log(`\n${checks.length - failed.length}/${checks.length} 通过`);
if (failed.length) process.exit(1);
