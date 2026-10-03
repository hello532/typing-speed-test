(function(){
"use strict";
var SENTENCES=[
"Learning to type quickly is a skill that helps students and professionals save time every day.",
"Practice a little each day and your fingers will learn the keyboard without looking down.",
"Good posture and relaxed hands make typing faster and more accurate over time.",
"The quick brown fox jumps over the lazy dog near the quiet river bank every morning.",
"Reading books aloud can improve both your vocabulary and your typing rhythm.",
"Accurate typing is often more valuable than fast typing in professional work.",
"A clean desk, a comfortable chair, and good lighting help you focus on your work.",
"Software developers spend hours every day typing code, notes, and documentation.",
];
var QUOTES=[
"The secret of getting ahead is getting started. - Mark Twain",
"Quality is not an act, it is a habit. - Aristotle",
"Do not wait for opportunity. Create it. - George Bernard Shaw",
"Success is the sum of small efforts repeated day in and day out. - Robert Collier",
"Whether you think you can or you think you cannot, you are right. - Henry Ford",
"The best time to plant a tree was twenty years ago. The second best time is now.",
"Typing is the language we use to speak to computers. Learn it well.",
"Practice does not make perfect. Perfect practice makes perfect. - Vince Lombardi",
];
var WORDS=["the","be","and","of","to","in","that","have","it","for","not","on","with","he","as","you","do","at","this","but","his","by","from","they","we","say","her","she","or","an","will","my","one","all","would","there","their","what","so","up","out","if","about","who","get","which","go","me","when","make","can","like","time","no","just","him","know","take","people","into","year","your","good","some","could","them","see","other","than","then","now","look","only","come","its","over","think","also","back","after","use","two","how","our","work","first","well","way","even","new","want","because","any","these","give","day","most","us","water","world","life","hand","part","child","eye","woman","place","week","case","point","government","company","number","group","problem","fact"];
function rnd(n){return Math.floor(Math.random()*n);}
function pickN(arr,n){var a=[],i;for(i=0;i<n;i++)a.push(arr[rnd(arr.length)]);return a.join(" ");}
function pick3(arr){var a=[],i;for(i=0;i<3;i++)a.push(arr[rnd(arr.length)]);return a.join(" ");}
function pad2(n){return (n<10?"0":"")+n;}
function fmtDate(f){
  var y=f.minYear+rnd(f.maxYear-f.minYear+1), m=1+rnd(12), d=1+rnd(28);
  var pat=f.pattern||"YYYY-MM-DD";
  return pat.replace("YYYY",y).replace("MM",pad2(m)).replace("DD",pad2(d));
}
function fmtTime(f){
  var h=f.h24?rnd(24):(1+rnd(12)), m=rnd(60), sec=rnd(60);
  var pat=f.pattern||"HH:MM";
  return pat.replace("HH",pad2(h)).replace("MM",pad2(m)).replace("SS",pad2(sec));
}
function fmtPhone(f){
  var pat=f.pattern||"(XXX) XXX-XXXX", out="", i;
  for(i=0;i<pat.length;i++){out+=(pat[i]==="X"?String(rnd(10)):pat[i]);}
  return out;
}
function genOne(f){
  var t=f.type, v, s;
  if(t==="int")return String(f.min+rnd(f.max-f.min+1));
  if(t==="decimal"||t==="currency"||t==="percent"){
    v=f.min+Math.random()*(f.max-f.min); s=v.toFixed(f.dp!=null?f.dp:2);
    if(t==="currency")return (f.prefix||"")+s;
    if(t==="percent")return s+"%";
    return s;
  }
  if(t==="date")return fmtDate(f);
  if(t==="time")return fmtTime(f);
  if(t==="phone")return fmtPhone(f);
  return String(rnd(100));
}
function genNumbers(formats,n){
  var totalW=0,i; for(i=0;i<formats.length;i++)totalW+=(formats[i].weight||1);
  var out=[],k,r,f;
  for(k=0;k<n;k++){
    r=rnd(totalW); f=formats[0];
    for(i=0;i<formats.length;i++){r-=(formats[i].weight||1); if(r<0){f=formats[i];break;}}
    out.push(genOne(f));
  }
  return out.join(" ");
}
function fingerKeys(fg){
  var ks=[],c;
  if(fg==="all"){return (KB_ROWS.join("").split("")).concat([" "]);}
  for(c in FINGER){if(FINGER[c]===fg)ks.push(c);}
  return ks.length?ks:["a"];
}
function genFingerKeys(){
  var ks=fingerKeys(drillFinger),out=[],n=30,i;
  for(i=0;i<n;i++){out.push(ks[rnd(ks.length)]); if(i%5===4)out.push(" ");}
  return out.join("");
}
/* ─────────── variant 行为层（VARIANT=null 时整层闲置）───────────
   7 个主题页各自"真做"：punctuation/capital/easy/numbers_ext 只换文本池（见 nextChunk），
   accuracy 阻塞错键并统计错键分布，game 有连击倍率/分数/等级/HUD/粒子，
   finger_drill 提供手指选择器，只出该手指负责的键。
   变体专属 CSS 由 VPOOL.css 在运行时注入 <style>，刻意不进 src/style.css——
   这样 13 个普通页的 CSS 与 HTML 对基线保持逐字节等价（verify.py check 4/9 守卫）。 */
function injectVariantCSS(){
  if(!VPOOL||!VPOOL.css)return;
  var st=document.createElement("style");
  st.setAttribute("data-variant",VARIANT);
  st.textContent=VPOOL.css;
  document.head.appendChild(st);
}
function beforeTyping(node){
  var tp=document.querySelector(".typing");
  if(!tp||!tp.parentNode)return null;
  tp.parentNode.insertBefore(node,tp); return node;
}
/* --- accuracy --- */
function buildAccBanner(){
  if(!VPOOL||!VPOOL.banner)return;
  var d=document.createElement("div");
  d.className="acc-banner"; d.textContent=VPOOL.banner;
  beforeTyping(d);
}
function keyDistHTML(){
  var ks=[],k,i,out="";
  for(k in keyErrors)ks.push([k,keyErrors[k]]);
  ks.sort(function(a,b){return b[1]-a[1];});
  if(!ks.length)return '<span class="kd">No blocked keys \u2014 clean run</span>';
  for(i=0;i<Math.min(ks.length,10);i++){
    out+='<span class="kd"><b>'+ks[i][1]+'\u00d7</b>'+esc(ks[i][0]===" "?"space":ks[i][0])+"</span>";
  }
  return out;
}
/* --- game --- */
function gameMult(){return Math.min((VPOOL&&VPOOL.maxMultiplier)||8,1+Math.floor(combo/10));}
function buildGameHUD(){
  var h=document.createElement("div"); h.className="game-hud"; h.id="gameHud";
  h.innerHTML='<div class="hud-cell"><span class="hud-lab">Score</span><b id="gScore">0</b></div>'
    +'<div class="hud-cell"><span class="hud-lab">Combo</span><b id="gCombo">0</b></div>'
    +'<div class="hud-cell"><span class="hud-lab">Mult</span><b id="gMult">\u00d71</b></div>'
    +'<div class="hud-cell"><span class="hud-lab">Level</span><b id="gLevel">1</b></div>';
  beforeTyping(h);
}
function setHUD(id,txt){var e=document.getElementById(id); if(e)e.textContent=txt;}
function updateHUD(){
  if(VARIANT!=="game")return;
  setHUD("gScore",score); setHUD("gCombo",combo);
  setHUD("gMult","\u00d7"+gameMult()); setHUD("gLevel",level);
}
function hudShake(){
  var h=document.getElementById("gameHud"); if(!h)return;
  h.classList.remove("shake"); void h.offsetWidth; h.classList.add("shake");
}
function levelUpFx(){
  var tp=document.querySelector(".typing"); if(!tp)return;
  var d=document.createElement("div"); d.className="lvl-fx";
  d.textContent="LEVEL "+level; tp.appendChild(d);
  setTimeout(function(){if(d.parentNode)d.parentNode.removeChild(d);},1200);
}
function sparkBurst(el){
  if(!el||!VPOOL||!VPOOL.particles)return;
  var tp=document.querySelector(".typing"); if(!tp)return;
  var r=el.getBoundingClientRect(), pr=tp.getBoundingClientRect(), i;
  for(i=0;i<6;i++){
    var s=document.createElement("div"); s.className="spark";
    var a=Math.random()*Math.PI*2, dist=16+Math.random()*24;
    s.style.left=(r.left-pr.left+r.width/2)+"px";
    s.style.top=(r.top-pr.top+r.height/2)+"px";
    s.style.setProperty("--dx",(Math.cos(a)*dist).toFixed(1)+"px");
    s.style.setProperty("--dy",(Math.sin(a)*dist).toFixed(1)+"px");
    tp.appendChild(s);
    (function(n){setTimeout(function(){if(n.parentNode)n.parentNode.removeChild(n);},520);})(s);
  }
}
function gameOnChar(ok,el){
  var g=VPOOL||{};
  if(ok){
    combo++; if(combo>bestCombo)bestCombo=combo;
    score+=(g.basePoints||10)*gameMult();
    if(combo%10===0)sparkBurst(el);
  }else{combo=0; hudShake();}
  var nl=1+Math.floor(score/(g.levelEvery||200));
  if(nl>level){level=nl; levelUpFx();}
  updateHUD();
}
/* --- finger_drill --- */
function fingerOptions(){
  var opts=[],i,f,lab=(VPOOL&&VPOOL.labels)||{},fs=(VPOOL&&VPOOL.fingers)||[];
  if(VPOOL&&VPOOL.allFingersOption)opts.push(["all","All fingers"]);
  for(i=0;i<fs.length;i++){
    f=fs[i];
    if(f==="TH")continue;                 /* 拇指只管空格，单独练没有意义 */
    opts.push([f,lab[f]||f]);
  }
  return opts;
}
function buildFingerBar(){
  var bar=document.createElement("div"); bar.className="finger-bar"; bar.id="fingerBar";
  var opts=fingerOptions(),html="",i;
  for(i=0;i<opts.length;i++){
    html+='<button type="button" class="finger-btn" data-f="'+opts[i][0]+'">'+esc(opts[i][1])+"</button>";
  }
  bar.innerHTML=html; beforeTyping(bar); paintFingerBar();
  bar.addEventListener("click",function(e){
    var t=e.target,b=null;
    while(t&&t!==bar){if(t.classList&&t.classList.contains("finger-btn")){b=t;break;}t=t.parentNode;}
    if(!b)return;
    drillFinger=b.getAttribute("data-f")||"all";
    paintFingerBar(); reset(); elIn.focus();
  });
}
function paintFingerBar(){
  var bar=document.getElementById("fingerBar"); if(!bar)return;
  var bs=bar.querySelectorAll(".finger-btn"),i;
  for(i=0;i<bs.length;i++){var bf=bs[i]; bf.classList.toggle("on",bf.getAttribute("data-f")===drillFinger); bf.setAttribute("aria-pressed",bf.getAttribute("data-f")===drillFinger?"true":"false");}
}
/* --- 变体结果块：finish() 时挂到结果面板尾部 --- */
function variantResult(){
  var host=document.getElementById("resultPanel"); if(!host||!VARIANT)return;
  var old=document.getElementById("variantRes");
  if(old&&old.parentNode)old.parentNode.removeChild(old);
  var d=document.createElement("div"); d.className="variant-res"; d.id="variantRes";
  if(VARIANT==="game"){
    var gk="gameBest_"+dur, gb=0, nb;
    try{gb=parseInt(localStorage.getItem(gk)||"0",10)||0;}catch(e){}
    nb=score>gb;
    if(nb){try{localStorage.setItem(gk,String(score));}catch(e){}}
    d.innerHTML='<div class="vr-title">Game summary</div><div class="vr-grid">'
      +'<div><b>'+score+'</b><span>Score</span></div>'
      +'<div><b>'+level+'</b><span>Level reached</span></div>'
      +'<div><b>'+bestCombo+'</b><span>Best combo</span></div></div>'
      +'<div class="vr-note">'+(nb?"New best score! \u2605":"Best score: "+Math.max(gb,score))+'</div>';
  }else if(VARIANT==="accuracy"&&VPOOL&&VPOOL.showKeyDist){
    d.innerHTML='<div class="vr-title">Most-missed keys</div><div class="kd-list">'+keyDistHTML()+'</div>';
  }else{return;}
  host.appendChild(d);
}
function buildVariantUI(){
  if(!VARIANT)return;
  injectVariantCSS();
  if(VARIANT==="game")buildGameHUD();
  else if(VARIANT==="finger_drill")buildFingerBar();
  else if(VARIANT==="accuracy")buildAccBanner();
}
function nextChunk(mode){
  /* ── variant 专用文本池（VARIANT=null 时全部跳过，走下方标准逻辑）── */
  if(VARIANT==="punctuation"&&VPOOL){
    if(mode==="quotes"&&VPOOL.quotes)return VPOOL.quotes[rnd(VPOOL.quotes.length)];
    return pick3(VPOOL.sentences);
  }
  if(VARIANT==="capital"&&VPOOL){
    if(mode==="words"&&VPOOL.words)return pickN(VPOOL.words,40);
    return pick3(VPOOL.sentences);
  }
  if(VARIANT==="easy"&&VPOOL){return pickN(VPOOL.words,40);}   /* 强制短词，忽略 mode */
  if(VARIANT==="numbers_ext"&&VPOOL){return genNumbers(VPOOL.formats,30);}
  if(VARIANT==="finger_drill"){return genFingerKeys();}
  if(mode==="numbers"){var a=[];for(var i=0;i<24;i++){a.push(String(100+rnd(899)));}return a.join(" ");}
  var L=(window.TR&&TR.pool&&TR.lang&&TR.lang!=="en")?TR.pool(TR.lang):null;
  if(L){
    if(mode==="quotes"&&L.quotes&&L.quotes.length){return L.quotes[rnd(L.quotes.length)];}
    if(mode==="words"&&L.words&&L.words.length){var w=[];for(var i=0;i<40;i++){w.push(L.words[rnd(L.words.length)]);}return w.join(" ");}
    if(L.sentences&&L.sentences.length){var s=[];for(var i=0;i<3;i++){s.push(L.sentences[rnd(L.sentences.length)]);}return s.join(" ");}
  }
  if(mode==="quotes"){return QUOTES[rnd(QUOTES.length)];}
  if(mode==="words"){var a=[];for(var i=0;i<40;i++){a.push(WORDS[rnd(WORDS.length)]);}return a.join(" ");}
  var s=[];for(var i=0;i<3;i++){s.push(SENTENCES[rnd(SENTENCES.length)]);}
  return s.join(" ");
}
var elText=document.getElementById("text"), elIn=document.getElementById("input"),
    elT=document.getElementById("sTime"), elW=document.getElementById("sWpm"), elA=document.getElementById("sAcc"),
    elHint=document.getElementById("hint"), elRes=document.getElementById("resultPanel"),
    chipsD=document.querySelectorAll(".dur"), chipsM=document.querySelectorAll(".mode");
var dur=60, mode="sentences", VARIANT=null, VPOOL=null;/*VAR_INIT*/
var chars=[], timer=null, startAt=0, finished=false, totalTyped=0;
var errTotal=0;            /* 累计打错次数（单调不减）——结果面板 Errors 用它 */
var wpmSamples=[]; var _prevLen=0;
var curEl=null;            /* 当前持 .cur 的 span，增量渲染时只动这一个节点 */
/* variant 运行时状态（普通页 VARIANT=null，以下全部闲置） */
var drillFinger="all";           /* finger_drill：当前练习的手指 */
var combo=0, score=0, level=1, bestCombo=0;   /* game：连击 / 分数 / 等级 / 本局最高连击 */
var keyErrors={};                /* accuracy：错键分布 target->count */
/* 无限文本流：初始铺满首屏，之后只要光标前方余量不足 LOOKAHEAD 就尾部追加一个 chunk。
   追加只发生在末尾，已输入部分的 chars[i] ↔ v[i] 索引对应关系不受影响。 */
var INIT_CHARS=240, LOOKAHEAD=80;
function mmss(s){return Math.floor(s/60)+":"+String(s%60).padStart(2,"0");}
function render(){
  /* 全量重建路径：reset() 与 finish() 使用。打字中走 updateDOM() 增量路径。 */
  var frag=document.createDocumentFragment(), i, sp;
  for(i=0;i<chars.length;i++){
    sp=document.createElement("span");
    sp.textContent=chars[i].t;
    if(i<totalTyped)sp.className=chars[i].ok?"ok":"bad";
    else if(i===totalTyped&&!finished)sp.className="cur";
    chars[i].el=sp;
    frag.appendChild(sp);
  }
  elText.innerHTML=""; elText.appendChild(frag);
  curEl=(chars[totalTyped]&&!finished)?chars[totalTyped].el:null;
  highlightKey();
}
function pushChunk(){
  var c=nextChunk(mode);
  if(!c)return 0;
  if(chars.length)c=" "+c;                     /* chunk 之间用空格分隔 */
  var frag=document.createDocumentFragment(), i, sp;
  for(i=0;i<c.length;i++){
    sp=document.createElement("span");
    sp.textContent=c[i];
    chars.push({t:c[i],ok:false,el:sp});
    frag.appendChild(sp);
  }
  elText.appendChild(frag);
  return c.length;
}
function seedText(){
  var guard=0;
  while(chars.length<INIT_CHARS&&guard++<20)pushChunk();
  if(!chars.length)pushChunk();
}
function ensureSupply(){
  /* 光标前方余量低于 LOOKAHEAD 就续写；guard 防 nextChunk 返回空串时死循环 */
  var guard=0;
  while(chars.length-totalTyped<LOOKAHEAD&&guard++<40){if(!pushChunk())break;}
}
function updateDOM(prev){
  /* 增量路径：只改 [min,max) 区间的 class 与光标节点，O(1) 级而非全量重建 */
  var lo=Math.min(prev,totalTyped), hi=Math.max(prev,totalTyped), i, el;
  for(i=lo;i<hi;i++){
    el=chars[i]&&chars[i].el; if(!el)continue;
    el.className=(i<totalTyped)?(chars[i].ok?"ok":"bad"):"";
  }
  if(curEl){curEl.classList.remove("cur"); curEl=null;}
  var c=chars[totalTyped];
  if(c&&c.el&&!finished){c.el.classList.add("cur"); curEl=c.el;}
  highlightKey();
}
function followCursor(){
  /* 打字中保持光标行可见；block:"nearest" 只在真的滚出视口时才动，避免每击键都滚 */
  var c=chars[totalTyped]; if(!c||!c.el||finished)return;
  var r=c.el.getBoundingClientRect(), vh=window.innerHeight||document.documentElement.clientHeight;
  if(r.top<0||r.bottom>vh)c.el.scrollIntoView({block:"nearest"});
}
function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function reset(){
  clearInterval(timer);
  chars=[]; totalTyped=0; errTotal=0; finished=false; startAt=0; curEl=null; _prevLen=0;
  /* variant 每局状态清零；drillFinger 是用户选择，跨局保留 */
  combo=0; score=0; level=1; bestCombo=0; keyErrors={};
  elText.innerHTML=""; seedText();
  elT.textContent=mmss(dur); elW.textContent="0"; elA.textContent="100%";
  elRes.style.display="none"; elHint.style.display="block";
  wpmSamples=[]; clearChart();
  render(); elIn.value=""; updateHUD();
}
function stats(){
  var el=0; for(var i=0;i<totalTyped;i++){if(chars[i]&&!chars[i].ok)el++;}
  var mins=(Date.now()-startAt)/60000;
  if(mins<=0)mins=1/60000;
  var correct=totalTyped-el;
  /* accuracy 变体：被阻塞的击键不进 totalTyped，分母必须补回 errTotal，否则 acc 恒为 100% */
  var accDen=((VARIANT==="accuracy"&&VPOOL&&VPOOL.blockOnError)?(correct+errTotal):totalTyped);
  return {wpm:Math.round((correct/5)/mins), raw:Math.round((totalTyped/5)/mins),
          acc: accDen? Math.round(correct/accDen*100):100,
          err:errTotal, errNow:el, cpm:Math.round(totalTyped/mins)};
}
function showLive(){var s=stats(); elW.textContent=s.wpm; elA.textContent=s.acc+"%"; elT.textContent=mmss(Math.max(0,dur-Math.floor((Date.now()-startAt)/1000))); if(startAt){wpmSamples.push({x:(Date.now()-startAt)/1000,y:s.wpm});}}
function consistency(){
  if(wpmSamples.length<2)return 100;
  var ys=[],i; for(i=0;i<wpmSamples.length;i++)ys.push(wpmSamples[i].y);
  var m=0; for(i=0;i<ys.length;i++)m+=ys[i]; m/=ys.length;
  if(m<=0)return 0;
  var v=0; for(i=0;i<ys.length;i++)v+=(ys[i]-m)*(ys[i]-m); v/=ys.length;
  var cv=Math.sqrt(v)/m;                 /* coefficient of variation */
  return Math.max(0,Math.min(100,Math.round((1-cv)*100)));
}
function pbKey(){return "typingPB_"+mode+"_"+dur;}
function finish(){
  finished=true; clearInterval(timer);
  var s=stats(); var cons=consistency();
  document.getElementById("rWpm").textContent=s.wpm+" "+((window.TR&&TR.t)?TR.t("wpm"):"WPM");
  document.getElementById("rAcc").textContent=s.acc+"%";
  document.getElementById("rCpm").textContent=s.cpm;
  document.getElementById("rErr").textContent=s.err;
  document.getElementById("rRaw").textContent=s.raw;
  var ce=document.getElementById("rCons"); if(ce)ce.textContent=cons+"%";
  var pb=0; try{pb=parseInt(localStorage.getItem(pbKey())||"0",10)||0;}catch(e){}
  var isPB=s.wpm>pb;
  if(isPB){try{localStorage.setItem(pbKey(),String(s.wpm));}catch(e){}}
  var pl=document.getElementById("pbLine");
  if(pl){
    var tr=(window.TR&&TR.t)?TR.t:function(k){return null;};
    if(isPB&&s.wpm>0){pl.className="pb-line pb-new";pl.textContent=(tr("pb_new")||"New personal best!")+" \u2605";}
    else if(pb>0){pl.className="pb-line";pl.textContent=(tr("pb_prev")||"Personal best")+": "+pb+" WPM";}
    else{pl.className="pb-line";pl.textContent="";}
  }
  saveHist(s);
  variantResult();
  drawChart();
  render(); elRes.style.display="block"; elHint.style.display="none";
  elRes.scrollIntoView({behavior:"smooth",block:"center"});
}
function saveHist(s){
  var k="typingHistV1", rows=[];
  try{rows=JSON.parse(localStorage.getItem(k)||"[]");}catch(e){rows=[];}
  var durLabel = dur<60 ? dur+"s" : (dur/60)+" min";
  rows.unshift({d:new Date().toLocaleDateString(), sec:dur, t:durLabel, m:mode, w:s.wpm, a:s.acc, e:s.err});
  rows=rows.slice(0,10);
  try{localStorage.setItem(k,JSON.stringify(rows));}catch(e){}
  renderHist(rows);
}
function renderHist(rows){
  var b=document.getElementById("histBody"); b.innerHTML="";
  if(!rows.length){b.innerHTML='<tr><td colspan="5" class="empty">'+((window.TR&&TR.t)?TR.t("hist_empty"):"No results yet — finish a test and it will appear here.")+'</td></tr>';return;}
  rows.forEach(function(r){
    var tr=document.createElement("tr");
    var _dl=(window.TR&&TR.fmtDur&&r.sec!=null)?TR.fmtDur(r.sec,TR.lang):(r.t||"");
    var _ml=(window.TR&&TR.modeLabel)?TR.modeLabel(r.m):r.m;
    tr.innerHTML="<td>"+esc(r.d)+"</td><td>"+esc(_dl)+" · "+esc(_ml)+"</td><td class='wpm'>"+r.w+"</td><td>"+r.a+"%</td><td>"+r.e+"</td>";
    b.appendChild(tr);
  });
}
var KB_ROWS=["qwertyuiop","asdfghjkl","zxcvbnm"];
var FINGER={q:"LP",a:"LP",z:"LP",w:"LR",s:"LR",x:"LR",e:"LM",d:"LM",c:"LM",r:"LI",f:"LI",v:"LI",t:"LI",g:"LI",b:"LI",y:"RI",h:"RI",n:"RI",u:"RI",j:"RI",m:"RI",i:"RM",k:"RM",o:"RR",l:"RR",p:"RP"," ":"TH"};
var KSIZE={s:1,m:1.3,l:1.65};
function applyKbdSize(sz){
  var k=KSIZE[sz]?sz:"m", wrap=document.getElementById("kbdWrap"); if(!wrap)return;
  var els=wrap.querySelectorAll(".kbd,.hands"); for(var i=0;i<els.length;i++)els[i].style.setProperty("--ks",KSIZE[k]);
  var bs=document.querySelectorAll(".kbd-size"); for(var j=0;j<bs.length;j++){var on=bs[j].getAttribute("data-ks")===k; bs[j].classList.toggle("on",on); bs[j].setAttribute("aria-pressed",on?"true":"false");}
  try{localStorage.setItem("kbdSize",k);}catch(e){}
}
var HAND_TIPS=[['LP',40,32],['LR',78,18],['LM',126,16],['LI',174,22],['TH',214,112],['TH',262,112],['RI',306,22],['RM',352,16],['RR',406,18],['RP',442,32]];
function buildHands(){var h=document.getElementById("hands");if(!h)return;var s='<div class="hands-wrap"><img class="hands-img" src="hands.png?v=202610020900" alt="finger position guide"><svg class="hands-ov" viewBox="0 0 486 265" aria-hidden="true">';for(var i=0;i<HAND_TIPS.length;i++){var t=HAND_TIPS[i];s+='<circle class="fg" data-f="'+t[0]+'" cx="'+t[1]+'" cy="'+t[2]+'" r="15"></circle>';}h.innerHTML=s+'</svg></div>';}
function buildKbd(){
  var kb=document.getElementById("kbd"); if(!kb)return;
  var html="",r,i,c;
  for(r=0;r<KB_ROWS.length;r++){
    html+='<div class="kbd-row">'; var row=KB_ROWS[r];
    for(i=0;i<row.length;i++){ c=row[i]; html+='<span class="key f-'+(FINGER[c]||"")+'" data-k="'+c+'">'+c+'</span>'; }
    html+='</div>';
  }
  html+='<div class="kbd-row"><span class="key key-space f-TH" data-k=" ">space</span></div>';
  kb.innerHTML=html; buildHands();
  var sz="m"; try{sz=localStorage.getItem("kbdSize")||"m";}catch(e){}
  applyKbdSize(sz);
  var bs=document.querySelectorAll(".kbd-size");
  for(i=0;i<bs.length;i++){(function(b){b.addEventListener("click",function(){applyKbdSize(b.getAttribute("data-ks"));});})(bs[i]);}
}
function highlightKey(){
  var kb=document.getElementById("kbd"); if(!kb)return;
  var p=kb.querySelectorAll(".key.next"); for(var i=0;i<p.length;i++)p[i].classList.remove("next");
  var fa=document.querySelectorAll(".fg.active"); for(i=0;i<fa.length;i++)fa[i].classList.remove("active");
  if(finished)return;
  var c=chars[totalTyped]; if(!c)return;
  var ch=(c.t||"").toLowerCase(), el=null;
  try{ el = ch===" " ? kb.querySelector(".key-space") : kb.querySelector('.key[data-k="'+ch.replace(/["\\]/g,'')+'"]'); }catch(e){}
  if(el)el.classList.add("next");
  var fg=FINGER[ch]; if(fg){var fe=document.querySelectorAll('.fg[data-f="'+fg+'"]'); for(i=0;i<fe.length;i++)fe[i].classList.add("active");}
}
function clearChart(){var cv=document.getElementById("wpmChart");if(cv){cv.getContext("2d").clearRect(0,0,cv.width,cv.height);}}
function drawChart(){
  var cv=document.getElementById("wpmChart"); if(!cv||wpmSamples.length<2)return;
  var x=cv.getContext("2d"),W=cv.width,H=cv.height,pad=24;
  x.clearRect(0,0,W,H);
  var maxY=10,i; for(i=0;i<wpmSamples.length;i++)maxY=Math.max(maxY,wpmSamples[i].y);
  var maxX=wpmSamples[wpmSamples.length-1].x||1;
  var cs=getComputedStyle(document.documentElement);
  var acc=(cs.getPropertyValue("--accent")||"#ffc93c").trim();
  var ln=(cs.getPropertyValue("--line")||"#333").trim();
  x.strokeStyle=ln;x.lineWidth=1;x.beginPath();x.moveTo(pad,H-pad);x.lineTo(W-6,H-pad);x.stroke();
  function PX(p){return pad+(W-pad-6)*(p.x/maxX);} function PY(p){return (H-pad)-(H-pad-12)*(p.y/maxY);}
  x.strokeStyle=acc;x.lineWidth=2.6;x.lineJoin="round";x.beginPath();
  for(i=0;i<wpmSamples.length;i++){var px=PX(wpmSamples[i]),py=PY(wpmSamples[i]);if(i===0)x.moveTo(px,py);else x.lineTo(px,py);}
  x.stroke();
  x.lineTo(PX(wpmSamples[wpmSamples.length-1]),H-pad);x.lineTo(pad,H-pad);x.closePath();
  x.globalAlpha=.13;x.fillStyle=acc;x.fill();x.globalAlpha=1;
}
(function(){var tp=document.querySelector(".typing");if(tp){
  elIn.addEventListener("blur",function(){if(startAt&&!finished)tp.classList.add("blurred");});
  elIn.addEventListener("focus",function(){tp.classList.remove("blurred");});
}})();
/* --- optional typing sound (WebAudio, no asset) --- */
var sndOn=false; try{sndOn=localStorage.getItem("typingSnd")==="1";}catch(e){}
var AC=null;
function click_(bad){
  if(!sndOn)return;
  try{
    if(!AC)AC=new (window.AudioContext||window.webkitAudioContext)();
    var o=AC.createOscillator(),g=AC.createGain(),t=AC.currentTime;
    o.type="square"; o.frequency.value=bad?180:660;
    g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(0.07,t+0.004);
    g.gain.exponentialRampToValueAtTime(0.0001,t+0.06);
    o.connect(g); g.connect(AC.destination); o.start(t); o.stop(t+0.07);
  }catch(e){}
}
(function(){
  var tg=document.getElementById("sndToggle"); if(!tg)return;
  function paint(){var b=tg.querySelector(".snd-state"); if(b)b.textContent=sndOn?((window.TR&&TR.t&&TR.t("on"))||"on"):((window.TR&&TR.t&&TR.t("off"))||"off"); tg.setAttribute("aria-pressed",sndOn?"true":"false"); tg.classList.toggle("on",sndOn);}
  tg.addEventListener("click",function(){sndOn=!sndOn; try{localStorage.setItem("typingSnd",sndOn?"1":"0");}catch(e){} if(sndOn&&!AC){try{AC=new (window.AudioContext||window.webkitAudioContext)();}catch(e){}} paint(); click_(false);});
  paint();
  window.addEventListener("tr-relang",paint);
})();
document.addEventListener("keydown",function(e){if(e.key==="Escape"){reset();elIn.focus();}});
elIn.addEventListener("input",function(){
  if(finished)return;
  if(!startAt){startAt=Date.now();
    timer=setInterval(function(){showLive();
      if((Date.now()-startAt)/1000>=dur){finish();}
    },200);
    elHint.style.display="none";
  }
  var v=elIn.value, prev=totalTyped, i;
  /* accuracy 变体：错键阻塞前进 —— 截断到第一个错键处，被拦下的击键计入 errTotal 与错键分布。
     截断后 [_prevLen,totalTyped) 区间必然全对，所以下方通用错误计数不会重复计。 */
  if(VARIANT==="accuracy"&&VPOOL&&VPOOL.blockOnError&&v.length>_prevLen){
    var bi=-1;
    for(i=_prevLen;i<v.length;i++){if(chars[i]&&chars[i].t!==v[i]){bi=i;break;}}
    if(bi>=0){
      var kt=chars[bi]?chars[bi].t:"?";
      keyErrors[kt]=(keyErrors[kt]||0)+1;
      errTotal++;
      v=v.slice(0,bi); elIn.value=v;
      if(typeof click_==="function")click_(true);
    }
  }
  totalTyped=v.length;
  for(i=0;i<totalTyped;i++){if(chars[i])chars[i].ok=(chars[i].t===v[i]);}
  /* 累计错误只对本次新增的字符计数：改对不再减少 Errors，改错重复计数 */
  if(totalTyped>_prevLen){for(i=_prevLen;i<totalTyped;i++){if(chars[i]&&!chars[i].ok)errTotal++;}}
  /* game 变体：对本次新增字符逐个结算连击/分数/等级 */
  if(VARIANT==="game"&&totalTyped>_prevLen){
    for(i=_prevLen;i<totalTyped;i++){gameOnChar(!!(chars[i]&&chars[i].ok),chars[i]&&chars[i].el);}
  }
  if(typeof click_==="function" && v.length>_prevLen){var _lc=chars[v.length-1]; click_(_lc?!_lc.ok:false);}
  _prevLen=v.length;
  ensureSupply();
  updateDOM(prev);
  followCursor();
  /* 不再在此调用 showLive()：采样只由 200ms 定时器驱动，避免 wpmSamples 双重推入。
     也不再判断 totalTyped>=chars.length 提前结束：文本无限供给，只有计时器能结束测试。 */
});
elText.addEventListener("click",function(){elIn.focus();});
elHint.addEventListener("click",function(){elIn.focus();});
document.addEventListener("keydown",function(e){
  if(finished||e.target===elIn||e.target.tagName==="INPUT"||e.target.tagName==="TEXTAREA")return;
  if(e.metaKey||e.ctrlKey||e.altKey)return;
  var k=e.key;
  if(k.length===1||k==="Backspace"){e.preventDefault(); elIn.focus();
    if(k==="Backspace"){elIn.value=elIn.value.slice(0,-1);}
    else{elIn.value+=k;}
    elIn.dispatchEvent(new Event("input"));
  }
});
chipsD.forEach(function(c){c.addEventListener("click",function(){
  chipsD.forEach(function(x){x.classList.toggle("on",x===c); x.setAttribute("aria-pressed",x===c?"true":"false");});
  dur=parseInt(c.getAttribute("data-d"),10); reset();
});});
chipsM.forEach(function(c){c.addEventListener("click",function(){
  chipsM.forEach(function(x){x.classList.toggle("on",x===c); x.setAttribute("aria-pressed",x===c?"true":"false");});
  mode=c.getAttribute("data-m"); reset();
});});
document.getElementById("btnAgain").addEventListener("click",function(){reset();elIn.focus();});
document.getElementById("btnShare").addEventListener("click",function(){
  var s=stats();
  var txt="I typed "+s.wpm+" WPM with "+s.acc+"% accuracy on Typing.Rerivo — https://typing.rerivo.com/";
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(function(){},function(){});}
  var btn=this; btn.textContent=(window.TR&&TR.t)?TR.t("btn_copied"):"Copied!"; setTimeout(function(){btn.textContent=(window.TR&&TR.t)?TR.t("btn_share"):"Copy result";},1400);
});
window.addEventListener("tr-relang",function(){reset();try{renderHist(JSON.parse(localStorage.getItem("typingHistV1")||"[]"));}catch(e){}});
(function(){var rows=[];try{rows=JSON.parse(localStorage.getItem("typingHistV1")||"[]");}catch(e){}renderHist(rows);})();
buildKbd(); buildVariantUI(); reset();
})();
