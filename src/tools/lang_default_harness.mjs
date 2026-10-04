/* 多语落地页“页面默认语言”链路验证（Node，无需 jsdom）
 * 用法: node src/tools/lang_default_harness.mjs
 * 验证: head 片段注入的 window.__trPageLang -> ui.js init 决策 -> 引擎 tr-relang 重播
 *       使落地页默认落目标语言，同时显式用户偏好优先、页面默认不落盘。
 * 与 engine_harness.mjs 互补：本 harness 加载真实 root/ui.js（五语池）+ src/engine.js，
 * 覆盖 ui.js init 与引擎的跨脚本协作；engine_harness 专注引擎内部行为（TR 由 stub 提供）。 */
import fs from 'fs';
import vm from 'vm';
import path from 'path';

const __dirname = path.dirname(new URL(import.meta.url).pathname);
const root = path.resolve(__dirname, '../..');

// ── 最小 DOM stub（仅满足 ui.js/engine.js 装载所需契约）─────────
class El {
  constructor(tag = 'div') {
    this.tagName = (tag || 'div').toUpperCase();
    this.children = []; this._text = ''; this._html = '';
    this.className = ''; this.style = {}; this.dataset = {}; this.value = '';
    this._listeners = {};
    this.classList = { add(){}, remove(){}, toggle(){}, contains: () => false };
  }
  get textContent() { return this.children.length ? this.children.map(c => c.textContent).join('') : this._text; }
  set textContent(v) { this._text = String(v); this.children = []; }
  get innerHTML() { return this._html; }
  set innerHTML(v) { this._html = String(v); this.children = []; }
  appendChild(c) { this.children.push(c); return c; }
  addEventListener(ev, fn) { (this._listeners[ev] = this._listeners[ev] || []).push(fn); }
  getBoundingClientRect() { return { top: 100, bottom: 120, left: 0, right: 800, width: 800, height: 20 }; }
  scrollIntoView() {} querySelectorAll() { return []; } querySelector() { return new El('span'); }
  closest() { return null; } setAttribute(k, v) { this[k] = v; } getAttribute(k) { return this[k] ?? null; }
  removeAttribute(k) { delete this[k]; }
  focus() {} blur() {} click() {}
  getContext() {
    const n = () => {};
    return { canvas:{width:600,height:130}, clearRect:n,beginPath:n,moveTo:n,lineTo:n,stroke:n,fill:n,
      fillRect:n,strokeRect:n,arc:n,fillText:n,measureText:()=>({width:10}),save:n,restore:n,
      translate:n,scale:n,rotate:n,createLinearGradient:()=>({addColorStop:n}) };
  }
}
const elements = {};
const htmlEl = { clientHeight: 800, clientWidth: 1200, lang: 'en', dir: '',
  setAttribute(k, v) { this[k] = v; }, getAttribute(k) { return this[k] ?? null; }, removeAttribute(k) { delete this[k]; } };
const documentStub = {
  createElement: tag => new El(tag),
  createDocumentFragment: () => new El('#fragment'),
  getElementById: id => (elements[id] ||= new El('div')),
  querySelectorAll: () => [], querySelector: () => null,
  addEventListener() {}, removeEventListener() {},
  readyState: 'complete', // 直接走 init()，不等 DOMContentLoaded
  title: '', documentElement: htmlEl,
  body: new El('body'), head: new El('head'),
};

// ── 从 root/ui.js 提取真实 POOL（构建时已注入五语池）──
const uiCode = fs.readFileSync(path.join(root, 'ui.js'), 'utf8');
const poolMatch = uiCode.match(/var POOL=(\{[\s\S]*?\});/);
if (!poolMatch) { console.error('无法从 ui.js 提取 POOL'); process.exit(1); }
const POOL = eval('(' + poolMatch[1] + ')');
const ES0 = POOL.es.sentences[0];
const ZH0 = POOL.zh.sentences[0];

// ── 剥掉最外层 IIFE 包裹，使顶层 var/function 成为沙箱全局（测试专用，不改源码）──
function stripIIFE(code) {
  const lines = code.split('\n');
  const openIdx = lines.findIndex(l => l.trim() === '(function(){');
  if (openIdx >= 0) lines.splice(openIdx, 1);
  for (let i = lines.length - 1; i >= 0; i--) {
    if (lines[i].trim() === '})();') { lines.splice(i, 1); break; }
  }
  return lines.join('\n');
}
const engineCode = stripIIFE(fs.readFileSync(path.join(root, 'src', 'engine.js'), 'utf8'));
const uiCodeBare = stripIIFE(uiCode);

// ── 场景装载器：先引擎（body 内联、非 defer，先跑）后 ui.js（defer，后跑），
//    复现真实页面脚本顺序；返回沙箱与 localStorage 存储。──
function loadPage(store0, pageLang) {
  const store = { ...store0 };
  const localStorageStub = {
    getItem: k => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: k => { delete store[k]; },
  };
  // 真实事件派发：ui.js setLang 派发 tr-relang -> 触发引擎监听重播
  const listeners = {};
  const sandbox = {
    document: documentStub, localStorage: localStorageStub,
    navigator: { userAgent: 'node', clipboard: { writeText: () => Promise.resolve() }, share: null },
    console,
    setInterval: () => ({ unref(){}, ref(){} }), clearInterval: () => {},
    setTimeout: () => ({ unref(){}, ref(){} }), clearTimeout: () => {},
    performance: { now: () => Date.now() },
    Date, Math, JSON, parseInt, parseFloat, isNaN, String, Number, Array, Object, RegExp,
    Set, Map, Promise, Symbol, Error, TypeError, RangeError, encodeURIComponent, decodeURIComponent,
    Event: class { constructor(type) { this.type = type; } },
    addEventListener: (t, fn) => { (listeners[t] = listeners[t] || []).push(fn); },
    removeEventListener: () => {},
    dispatchEvent: e => { (listeners[e.type] || []).forEach(fn => fn(e)); return true; },
    innerWidth: 1200, innerHeight: 800, devicePixelRatio: 1,
    location: { hostname: 'typing.rerivo.com', pathname: '/', href: 'https://typing.rerivo.com/' },
    scrollTo() {}, getComputedStyle: () => ({ display: 'none' }),
    AudioContext: function () {
      return { createGain: () => ({ gain:{value:1}, connect(){} }),
        createOscillator: () => ({ connect(){},start(){},stop(){},frequency:{value:440},type:'sine' }),
        destination: {}, currentTime: 0, state: 'running', resume(){} };
    },
    __trPageLang: pageLang, // head 片段按页注入的页面默认语言（无则 undefined）
  };
  sandbox.window = sandbox; sandbox.globalThis = sandbox; sandbox.self = sandbox;
  const ctx = vm.createContext(sandbox);
  vm.runInContext(engineCode, ctx, { filename: 'engine.js' });
  ctx.rnd = () => 0; // 装载后确定性取句（恒取 sentences[0]），便于断言文本归属
  vm.runInContext(uiCodeBare, ctx, { filename: 'ui.js' });
  return { ctx, store };
}

// ── 测试框架 ─────────────────────────────────────────────
let passed = 0, failed = 0;
const assert = (cond, msg) => { if (cond) { passed++; console.log('  ✅', msg); } else { failed++; console.log('  ❌', msg); } };
const seededText = ctx => ctx.chars.map(c => c.t).join('');

// ═══ A. 页面默认语言生效（无存储偏好）══════════════════════
console.log('\n=== A: 多语落地页默认语言（无存储偏好，__trPageLang=es）===');
{
  const { ctx, store } = loadPage({}, 'es');
  assert(ctx.TR.lang === 'es', `页面默认生效 TR.lang==="es"（实际 ${ctx.TR.lang}）`);
  const t = seededText(ctx);
  assert(t.includes(ES0), '练习文本取自西语池（含 es.sentences[0]）');
  assert(!t.includes(ctx.SENTENCES[0]), '练习文本不再是默认英文池句子');
  assert(!('trLang' in store), '页面默认不落盘 trLang（防偏好泄漏到其他页）');
}

// ═══ B. 显式英文偏好覆盖页面默认 ══════════════════════════
console.log('\n=== B: 用户已存英文偏好，覆盖页面默认 ===');
{
  const { ctx, store } = loadPage({ trLang: 'en' }, 'es');
  assert(ctx.TR.lang === 'en', `显式偏好胜出 TR.lang==="en"（实际 ${ctx.TR.lang}）`);
  assert(store.trLang === 'en', '显式偏好保持不变');
}

// ═══ C. 基线英文页（无页面默认、无存储）行为不变 ════════════
console.log('\n=== C: 基线英文页（无 __trPageLang、无存储）===');
{
  const { ctx, store } = loadPage({}, undefined);
  assert(ctx.TR.lang === 'en', `基线页 TR.lang==="en"（实际 ${ctx.TR.lang}）`);
  assert(!('trLang' in store), '默认 en 同样不落盘（与基线行为一致）');
}

// ═══ D. 显式非英文偏好胜出并触发引擎重播 ════════════════════
console.log('\n=== D: 用户已存中文偏好（非 en），验证引擎按偏好重播 ===');
{
  const { ctx, store } = loadPage({ trLang: 'zh' }, 'es');
  assert(ctx.TR.lang === 'zh', `存储偏好胜过页面默认 TR.lang==="zh"（实际 ${ctx.TR.lang}）`);
  const t = seededText(ctx);
  assert(t.includes(ZH0), '引擎按存储偏好重播为中文（含 zh.sentences[0]）');
  assert(store.trLang === 'zh', '显式偏好保持不变');
}

console.log(`\n结果: ${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
