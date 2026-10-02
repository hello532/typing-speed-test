/* engine.js 行为级验证 harness（Node，无需 jsdom）
 * 用法: node src/tools/engine_harness.mjs
 * 验证: P0-1 无限文本流 / P1-1 wpmSamples 单点 / P1-2 增量渲染 / P1-4+5 错误语义 */
import fs from 'fs';
import vm from 'vm';
import path from 'path';

const __dirname = path.dirname(new URL(import.meta.url).pathname);
const root = path.resolve(__dirname, '../..');

// ── 最小 DOM stub ──────────────────────────────────────────
class El {
  constructor(tag = 'div') {
    this.tagName = tag.toUpperCase();
    this.children = [];
    this._text = ''; this._html = '';
    this.className = ''; this.style = {}; this.dataset = {}; this.value = '';
    this._listeners = {};
    this.classList = {
      add: c => { const s = new Set(this.className.split(/\s+/).filter(Boolean)); s.add(c); this.className = [...s].join(' '); },
      remove: c => { const s = new Set(this.className.split(/\s+/).filter(Boolean)); s.delete(c); this.className = [...s].join(' '); },
      toggle: (c, on) => { const s = new Set(this.className.split(/\s+/).filter(Boolean)); if (on === undefined) on = !s.has(c); if (on) s.add(c); else s.delete(c); this.className = [...s].join(' '); },
      contains: c => this.className.split(/\s+/).includes(c),
    };
  }
  get textContent() { return this.children.length ? this.children.map(c => c.textContent).join('') : this._text; }
  set textContent(v) { this._text = String(v); this.children = []; }
  get innerHTML() { return this._html; }
  set innerHTML(v) { this._html = String(v); this.children = []; }
  appendChild(c) { this.children.push(c); return c; }
  addEventListener(ev, fn) { (this._listeners[ev] = this._listeners[ev] || []).push(fn); }
  getBoundingClientRect() { return { top: 100, bottom: 120, left: 0, right: 800, width: 800, height: 20 }; }
  scrollIntoView() {}
  querySelectorAll() { return []; }
  querySelector() { const e = new El('span'); return e; }
  closest() { return null; }
  setAttribute(k, v) { this[k] = v; }
  getAttribute(k) { return this[k] ?? null; }
  focus() {} blur() {} click() {}
  getContext() {
    const noop = () => {};
    return { canvas: { width: 600, height: 130 }, clearRect: noop, beginPath: noop, moveTo: noop, lineTo: noop,
      stroke: noop, fill: noop, fillRect: noop, strokeRect: noop, arc: noop, fillText: noop,
      measureText: () => ({ width: 10 }), save: noop, restore: noop, translate: noop, scale: noop, rotate: noop,
      createLinearGradient: () => ({ addColorStop: noop }) };
  }
}

const elements = {};
const documentStub = {
  createElement: tag => new El(tag),
  createDocumentFragment: () => new El('#fragment'),
  getElementById: id => (elements[id] ||= new El('div')),
  querySelectorAll: () => [], querySelector: () => null,
  addEventListener() {}, removeEventListener() {},
  title: '', documentElement: { clientHeight: 800, clientWidth: 1200 },
  body: new El('body'), head: new El('head'),
};

const store = {};
const localStorageStub = {
  getItem: k => store[k] ?? null,
  setItem: (k, v) => { store[k] = String(v); },
  removeItem: k => { delete store[k]; },
  clear: () => { for (const k of Object.keys(store)) delete store[k]; },
};

// ── 从 ui.js 提取 POOL（5 语言词池，文本供给的数据源）────────
const uiCode = fs.readFileSync(path.join(root, 'ui.js'), 'utf8');
const poolMatch = uiCode.match(/var POOL=(\{[\s\S]*?\});/);
if (!poolMatch) { console.error('无法从 ui.js 提取 POOL'); process.exit(1); }
const POOL = eval('(' + poolMatch[1] + ')');

// ── 沙箱全局（ui.js 依赖全部 stub，只保留 engine.js 真正用到的契约）──
const sandbox = {
  document: documentStub, localStorage: localStorageStub,
  navigator: { userAgent: 'node', clipboard: { writeText: () => Promise.resolve() }, share: null },
  console,
  setInterval: () => ({ unref() {}, ref() {} }), clearInterval: () => {},
  setTimeout: () => ({ unref() {}, ref() {} }), clearTimeout: () => {},
  performance: { now: () => Date.now() },
  Date, Math, JSON, parseInt, parseFloat, isNaN, String, Number, Array, Object, RegExp,
  Set, Map, Promise, Symbol, Error, TypeError, RangeError, encodeURIComponent, decodeURIComponent,
  // window 属性（sandbox.window = sandbox 下面设置）
  innerWidth: 1200, innerHeight: 800, devicePixelRatio: 1,
  location: { hostname: 'typing.rerivo.com', pathname: '/typing-test/', href: 'https://typing.rerivo.com/typing-test/' },
  scrollTo() {}, getComputedStyle: () => ({ display: 'none' }),
  AudioContext: function () {
    return { createGain: () => ({ gain: { value: 1 }, connect() {} }),
      createOscillator: () => ({ connect() {}, start() {}, stop() {}, frequency: { value: 440 }, type: 'sine' }),
      destination: {}, currentTime: 0, state: 'running', resume() {} };
  },
  // ui.js 全局契约
  TR: { lang: 'en', t: k => k, pool: l => POOL[l] || null, fmtDur: s => s < 60 ? s + 's' : (s / 60) + 'm', modeLabel: m => m },
  POOL,
  ls: (k, d) => { const v = localStorageStub.getItem('tr_' + k); return v == null ? d : v; },
  ss: (k, v) => localStorageStub.setItem('tr_' + k, v),
  gs: (k, d) => { const v = localStorageStub.getItem('tr_' + k); return v == null ? d : v; },
  playTick: () => {}, click_: () => {},
  buildKbd: () => {}, updateKbd: () => {}, highlightKey: () => {},
  fmtWpm: w => String(w),
  loadHistory: () => [], renderHistory: () => {}, clearHistory: () => {}, renderChart: () => {},
  applyI18n: () => {},
  I18N: { en: { _name: 'English' } }, UNITS: { en: { s: 's', m: 'm' } },
  LANGS: ['en', 'zh', 'es', 'hi', 'ar'],
};
sandbox.window = sandbox; sandbox.globalThis = sandbox; sandbox.self = sandbox;

// ── 加载 engine.js ─────────────────────────────────────────
const engineCode = (() => {
  let lines = fs.readFileSync(path.join(root, 'src', 'engine.js'), 'utf8').split('\n');
  // 剥掉最外层 IIFE 包裹，使顶层 var/function 成为沙箱全局（测试专用，不改源码）
  if (lines[0] && lines[0].trim() === '(function(){') lines.shift();
  for (let i = lines.length - 1; i >= 0; i--) {
    if (lines[i].trim() === '})();') { lines.splice(i, 1); break; }
  }
  return lines.join('\n');
})();
sandbox.addEventListener = () => {}; sandbox.removeEventListener = () => {};
sandbox.matchMedia = undefined; // 走 typeof guard 分支
const ctx = vm.createContext(sandbox);
try { vm.runInContext(engineCode, ctx, { filename: 'engine.js' }); }
catch (e) { console.error('engine.js 加载失败:', e.message, '\n', e.stack?.split('\n').slice(0, 4).join('\n')); process.exit(1); }

// ── 测试框架 ──────────────────────────────────────────────
let passed = 0, failed = 0;
const assert = (cond, msg) => { if (cond) { passed++; console.log('  ✅', msg); } else { failed++; console.log('  ❌', msg); } };

// engine.js 末尾调用 reset()，chars 已初始化
const elIn = ctx.document.getElementById('input');
const inputHandler = elIn._listeners['input']?.[0];

console.log('\n=== P0-1: 无限文本流（5000 击键永不提前结束）===');
assert(ctx.chars.length >= 240, `seedText 初始铺满 ≥240 字符（实际 ${ctx.chars.length}）`);
assert(ctx.totalTyped === 0 && !ctx.finished, '初始状态 totalTyped=0, finished=false');
assert(!!inputHandler, 'input handler 已注册');

let finishTriggered = false;
const origFinish = ctx.finish;
ctx.finish = function () { finishTriggered = true; origFinish.call(ctx); };

const KEYSTROKES = 5000;
for (let i = 0; i < KEYSTROKES; i++) {
  if (finishTriggered) break;
  const c = ctx.chars[i];
  if (!c) { console.error(`  字符供给不足 at ${i}`); break; }
  elIn.value += c.t;
  ctx.totalTyped = elIn.value.length;
  inputHandler({ type: 'input', target: elIn });
}
assert(!finishTriggered, `5000 击键后 finished 仍为 false（P0 修复：永不提前结束）`);
assert(ctx.totalTyped === KEYSTROKES, `totalTyped=${ctx.totalTyped}（应=${KEYSTROKES}）`);
assert(ctx.chars.length >= KEYSTROKES + 80, `chars 长度 ${ctx.chars.length} ≥ ${KEYSTROKES}+LOOKAHEAD（供给充足）`);

console.log('\n=== P1-2: 增量渲染（render 调用 = O(1) 而非 O(n)）===');
let renderCalls = 0;
const origRender = ctx.render;
ctx.render = function () { renderCalls++; origRender.call(ctx); };
for (let i = 0; i < 100; i++) {
  const c = ctx.chars[ctx.totalTyped]; if (!c) break;
  elIn.value += c.t; ctx.totalTyped = elIn.value.length;
  inputHandler({ type: 'input', target: elIn });
}
assert(renderCalls === 0, `增量路径下 render() 调用 ${renderCalls} 次（应=0，走 updateDOM）`);

console.log('\n=== P1-4/P1-5: 错误语义（errTotal 单调不减）===');
ctx.reset();
const elIn2 = ctx.document.getElementById('input');
const ih2 = elIn2._listeners['input']?.[0];
for (let i = 0; i < 5; i++) { elIn2.value += ctx.chars[i].t; ctx.totalTyped = elIn2.value.length; ih2({ type: 'input', target: elIn2 }); }
assert(ctx.errTotal === 0, '5 个正确字符后 errTotal=0');
elIn2.value += 'X'; ctx.totalTyped = elIn2.value.length; ih2({ type: 'input', target: elIn2 });
assert(ctx.errTotal === 1, `1 个错误后 errTotal=1（实际 ${ctx.errTotal}）`);
elIn2.value = elIn2.value.slice(0, 5) + ctx.chars[5].t; ctx.totalTyped = elIn2.value.length; ih2({ type: 'input', target: elIn2 });
assert(ctx.errTotal === 1, `改对后 errTotal 仍=1（单调不减，实际 ${ctx.errTotal}）`);
elIn2.value += 'Y'; ctx.totalTyped = elIn2.value.length; ih2({ type: 'input', target: elIn2 });
assert(ctx.errTotal === 2, `第 2 个错误后 errTotal=2（实际 ${ctx.errTotal}）`);

console.log('\n=== P1-1: wpmSamples 单点驱动（input handler 不调 showLive）===');
let showLiveCalls = 0;
const origShowLive = ctx.showLive;
ctx.showLive = function () { showLiveCalls++; origShowLive.call(ctx); };
ctx.reset();
const elIn3 = ctx.document.getElementById('input');
const ih3 = elIn3._listeners['input']?.[0];
for (let i = 0; i < 10; i++) { elIn3.value += ctx.chars[i].t; ctx.totalTyped = elIn3.value.length; ih3({ type: 'input', target: elIn3 }); }
assert(showLiveCalls === 0, `input handler 中 showLive 调用 ${showLiveCalls} 次（应=0）`);

console.log('\n=== 附加: 多模式文本供给 ===');
for (const m of ['sentences', 'quotes', 'words', 'numbers']) {
  ctx.mode = m; ctx.reset();
  const ok = ctx.chars.length >= 240;
  assert(ok, `mode=${m}: seedText 铺满 ${ctx.chars.length} 字符 ${ok ? '✅' : '❌'}`);
}

console.log(`\n${'─'.repeat(60)}`);
console.log(`结果: ${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
