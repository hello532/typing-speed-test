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

// ══════════════ P2: 7 主题页 variant 行为验证 ══════════════
const VARIANTS = JSON.parse(fs.readFileSync(path.join(root, 'src', 'variants.json'), 'utf8'));
const PUNCT = new Set([',', '.', ';', ':', '!', '?', '"', "'", '(', ')', '-', '—']);
const NON_WS_DENS = t => { let p = 0, n = 0; for (const c of t) { if (!/\s/.test(c)) n++; if (PUNCT.has(c)) p++; } return n ? p / n * 100 : 0; };

// 与 build.py inject_variant 完全一致：pool = 去掉 _ 前缀键后的整个 variant 对象（含 css）
function setVariant(name) {
  ctx.VARIANT = name;
  const v = VARIANTS[name], pool = {};
  for (const k of Object.keys(v)) if (!k.startsWith('_')) pool[k] = v[k];
  ctx.VPOOL = pool;
  return pool;
}
function clearVariant() { ctx.VARIANT = null; ctx.VPOOL = null; }
function typeChars(n, ih, el) {
  for (let i = 0; i < n; i++) {
    const c = ctx.chars[ctx.totalTyped]; if (!c) return i;
    el.value += c.t; ctx.totalTyped = el.value.length;
    ih({ type: 'input', target: el });
  }
  return n;
}

console.log('\n=== P2-a: 变体文本池（池本身 + nextChunk 生成）===');
{
  const p = setVariant('punctuation');
  const poolText = p.sentences.concat(p.quotes).join(' ');
  const poolDens = NON_WS_DENS(poolText);
  assert(poolDens >= 15, `punctuation 池标点密度 ${poolDens.toFixed(1)}% ≥ 15%（标点/非空白字符）`);
  const kinds = [...PUNCT].filter(c => poolText.includes(c));
  assert(kinds.length >= 8, `punctuation 覆盖 ${kinds.length} 种标点（${kinds.join(' ')}）`);
  assert(p.sentences.length >= 30 && p.quotes.length >= 4, `池规模 sentences=${p.sentences.length} quotes=${p.quotes.length}`);
  let sampled = 0, sampledP = 0;
  for (let r = 0; r < 40; r++) {
    const t = ctx.nextChunk('sentences');
    for (const c of t) { if (!/\s/.test(c)) sampled++; if (PUNCT.has(c)) sampledP++; }
  }
  assert(sampledP / sampled * 100 >= 10, `nextChunk 生成文本标点密度 ${(sampledP / sampled * 100).toFixed(1)}% ≥ 10%`);
  assert(ctx.nextChunk('quotes').includes('"'), 'quotes 模式返回带引号的引语');
}
{
  const p = setVariant('capital');
  const poolText = p.sentences.concat(p.words).join(' ');
  assert(/[A-Z]{2,}/.test(poolText), 'capital 池含全大写缩写（NASA/IBM 类）');
  assert(/[a-z][A-Z][a-z]/.test(poolText), 'capital 池含驼峰式词（getUserName 类）');
  assert(/\b[A-Z][a-z]+ [a-z]+\b/.test(poolText), 'capital 池含句首/专有名词大写');
  const w = ctx.nextChunk('words');
  assert(w.split(' ').length === 40, `capital words 模式返回 40 词（实际 ${w.split(' ').length}）`);
  const caps = [...poolText].filter(c => /[A-Z]/.test(c)).length;
  const letters = [...poolText].filter(c => /[A-Za-z]/.test(c)).length;
  assert(caps / letters >= 0.05, `capital 池大写字母占比 ${(caps / letters * 100).toFixed(1)}% ≥ 5%`);
}
{
  const p = setVariant('easy');
  const bad = p.words.filter(w => w.length > 5 || w.length < 2 || /[^a-z]/.test(w));
  assert(bad.length === 0 && p.words.length >= 100,
    `easy 池 ${p.words.length} 词全部 2-5 字母纯小写（违规 ${bad.length}: ${bad.slice(0, 3)}）`);
  const gen = ctx.nextChunk('words');
  assert(NON_WS_DENS(gen) === 0 && gen === gen.toLowerCase(), 'easy 生成文本无标点、无大写');
}
{
  const p = setVariant('numbers_ext');
  const types = [...new Set(p.formats.map(f => f.type))];
  for (const t of ['int', 'decimal', 'date', 'time', 'phone', 'currency', 'percent'])
    assert(types.includes(t), `numbers_ext 格式表含 ${t}`);
  const all = Array.from({ length: 300 }, () => ctx.nextChunk('sentences')).join(' ');
  const found = {
    小数: /\d+\.\d+/.test(all), 日期: /\d{4}-\d{2}-\d{2}|\d{2}\/\d{2}\/\d{4}/.test(all),
    时间: /\d{2}:\d{2}/.test(all), 电话: /\(\d{3}\) \d{3}-\d{4}/.test(all),
    货币: /[$€£¥]\d/.test(all), 百分比: /\d+%/.test(all),
  };
  const missing = Object.keys(found).filter(k => !found[k]);
  assert(missing.length === 0, `生成文本实测覆盖 6 类格式${missing.length ? '（缺 ' + missing + '）' : ''}`);
  assert(!/[A-Za-z]/.test(all), 'numbers_ext 生成文本不含任何字母（纯数字/符号）');
}
clearVariant();

console.log('\n=== P2-b: game — 连击倍率 / 分数 / 等级 / 错误清零 ===');
{
  setVariant('game');
  ctx.reset();
  const el = ctx.document.getElementById('input');
  const ih = el._listeners['input'][0];
  assert(ctx.score === 0 && ctx.combo === 0 && ctx.level === 1 && ctx.bestCombo === 0,
    'game reset 后 score/combo/level/bestCombo 归零');
  typeChars(9, ih, el);
  assert(ctx.combo === 9 && ctx.score === 90, `9 连击 → combo=${ctx.combo} score=${ctx.score}（每字 ×1=10 分）`);
  el.value += ctx.chars[ctx.totalTyped].t; ctx.totalTyped = el.value.length; ih({ type: 'input', target: el });
  assert(ctx.combo === 10 && ctx.score === 110 && ctx.gameMult() === 2,
    `第 10 连击 → score=110，倍率升为 ×${ctx.gameMult()}`);
  typeChars(10, ih, el);
  assert(ctx.combo === 20 && ctx.score === 320,
    `20 连击 → combo=${ctx.combo} score=${ctx.score}（11-19 各 ×2，第 20 触发 ×3）`);
  const expectLevel = 1 + Math.floor(ctx.score / 200);
  assert(ctx.level === expectLevel, `level=${ctx.level} == 1+floor(score/levelEvery)=${expectLevel}`);
  assert(ctx.bestCombo === 20, `bestCombo=${ctx.bestCombo} 记录本局最高连击`);
  const wrong = ctx.chars[ctx.totalTyped].t === 'a' ? 'b' : 'a';
  el.value += wrong; ctx.totalTyped = el.value.length; ih({ type: 'input', target: el });
  assert(ctx.combo === 0 && ctx.score === 320 && ctx.errTotal === 1,
    `错误 → combo 清零、score 不倒扣（${ctx.score}）、errTotal=1`);
  assert(ctx.bestCombo === 20, '错误后 bestCombo 仍保留历史最高');
  // 原地改对不重触发计分（totalTyped 不增），再续打一个新字 → combo 从 1 重新累计
  el.value = el.value.slice(0, -1) + ctx.chars[ctx.totalTyped - 1].t; ctx.totalTyped = el.value.length;
  ih({ type: 'input', target: el });
  el.value += ctx.chars[ctx.totalTyped].t; ctx.totalTyped = el.value.length; ih({ type: 'input', target: el });
  assert(ctx.combo === 1 && ctx.score === 330, `修正并续打 → combo 重新累计=${ctx.combo} score=${ctx.score}`);
  ctx.reset();
  assert(ctx.score === 0 && ctx.combo === 0 && ctx.level === 1 && ctx.bestCombo === 0, '再次 reset 清空全局计分');
}

console.log('\n=== P2-c: accuracy — 错键阻塞前进 + 错键分布 + 分母修正 ===');
{
  setVariant('accuracy');
  ctx.reset();
  const el = ctx.document.getElementById('input');
  const ih = el._listeners['input'][0];
  typeChars(3, ih, el);
  assert(ctx.totalTyped === 3 && ctx.errTotal === 0, '3 个正确字符通过，errTotal=0');
  const target = ctx.chars[3].t;
  const wrong = target === 'a' ? 'b' : 'a';
  el.value += wrong; ctx.totalTyped = el.value.length; ih({ type: 'input', target: el });
  assert(el.value.length === 3 && ctx.totalTyped === 3,
    `错键被阻塞：input 截断回 ${el.value.length}（原 4），光标未前进`);
  assert(ctx.errTotal === 1, `被拦下的击键计入 errTotal=${ctx.errTotal}`);
  assert(ctx.keyErrors[target] === 1, `错键分布记录目标键 "${target}": 1`);
  el.value += wrong; ctx.totalTyped = el.value.length; ih({ type: 'input', target: el });
  assert(ctx.errTotal === 2 && ctx.keyErrors[target] === 2, '重复错同一键 → errTotal=2，分布=2');
  const s1 = ctx.stats();
  assert(s1.acc === 60, `accuracy 变体 acc=${s1.acc}%（分母含被阻塞击键：3 正确/(3+2)=60%），否则恒 100%`);
  el.value += target; ctx.totalTyped = el.value.length; ih({ type: 'input', target: el });
  assert(ctx.totalTyped === 4 && ctx.errTotal === 2, '修正后前进：totalTyped=4，errTotal 保持 2');
  assert(Object.keys(ctx.keyErrors).length === 1, '只有打错过的键进入分布表');
  ctx.reset();
  assert(Object.keys(ctx.keyErrors).length === 0, 'reset 清空错键分布');
}
{
  // 普通页（VARIANT=null）不受阻塞语义影响
  clearVariant();
  ctx.reset();
  const el = ctx.document.getElementById('input');
  const ih = el._listeners['input'][0];
  typeChars(2, ih, el);
  el.value += 'Q'; ctx.totalTyped = el.value.length; ih({ type: 'input', target: el });
  assert(ctx.totalTyped === 3 && el.value.length === 3, '普通页错键不阻塞（totalTyped=3），保持原语义');
}

console.log('\n=== P2-d: finger_drill — 只出所选手指负责的键 ===');
{
  setVariant('finger_drill');
  const drill = (fg) => {
    ctx.drillFinger = fg;
    let out = '';
    for (let r = 0; r < 40; r++) out += ctx.nextChunk('sentences');
    return out;
  };
  for (const [fg, keys] of [['LP', 'qaz'], ['LR', 'wsx'], ['RM', 'ik'], ['RP', 'p']]) {
    const t = drill(fg);
    const bad = [...new Set([...t.replace(/ /g, '')])].filter(c => !keys.includes(c));
    assert(bad.length === 0, `finger_drill ${fg} 只出 ${keys}（越界键: ${bad.join('') || '无'}）`);
    assert(t.includes(' '), `${fg} 文本含空格分隔`);
  }
  const all = drill('all');
  assert(new Set(all.replace(/ /g, '')).size >= 20, `all 模式覆盖 ${new Set(all.replace(/ /g, '')).size} 个不同键`);
  const opts = ctx.fingerOptions();
  assert(opts.length === 9 && opts[0][0] === 'all' && !opts.some(o => o[0] === 'TH'),
    `选择器 ${opts.length} 项：含 all、排除拇指（空格练习无意义）`);
  assert(opts.every(o => o[1].length > 1), '每个手指选项都有可读标签');
  ctx.drillFinger = 'all';
}
clearVariant();
ctx.reset();

console.log('\n=== 附加: 多模式文本供给 ===');
for (const m of ['sentences', 'quotes', 'words', 'numbers']) {
  ctx.mode = m; ctx.reset();
  const ok = ctx.chars.length >= 240;
  assert(ok, `mode=${m}: seedText 铺满 ${ctx.chars.length} 字符 ${ok ? '✅' : '❌'}`);
}

console.log(`\n${'─'.repeat(60)}`);
console.log(`结果: ${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
