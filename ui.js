/* ui.js — language switcher (5 langs incl. RTL Arabic) + 3 color themes.
   Translates UI chrome via [data-i18n]/[data-i18n-html]; provides native
   practice-text banks via window.TR.pool(lang). Persists in localStorage.
   Does not alter SEO article/FAQ (kept English for indexing). Zero deps. */
(function(){
"use strict";

var I18N={
 en:{_name:"English",time:"Time",text:"Text",m_sentences:"Sentences",m_quotes:"Quotes",m_numbers:"Numbers",m_words:"Words",
   st_time:"Time",wpm:"WPM",accuracy:"Accuracy",r_cpm:"Chars/min",r_errors:"Errors",r_raw:"Raw WPM",
   hint:'Click here or press <b>any key</b> to start typing',btn_again:"Test again",btn_share:"Copy result",btn_copied:"Copied!",
   hist_title:"Your typing history (saved in this browser)",h_date:"Date",h_test:"Test",
   hist_empty:"No results yet — finish a test and it will appear here."},
 zh:{_name:"中文",time:"时间",text:"文本",m_sentences:"句子",m_quotes:"名言",m_numbers:"数字",m_words:"单词",
   st_time:"时间",wpm:"字/分",accuracy:"准确率",r_cpm:"字符/分",r_errors:"错误",r_raw:"原始速度",
   hint:'点击此处或按<b>任意键</b>开始打字',btn_again:"再测一次",btn_share:"复制成绩",btn_copied:"已复制！",
   hist_title:"你的打字记录（保存在此浏览器）",h_date:"日期",h_test:"测试",
   hist_empty:"还没有记录 —— 完成一次测试后会显示在这里。"},
 es:{_name:"Español",time:"Tiempo",text:"Texto",m_sentences:"Frases",m_quotes:"Citas",m_numbers:"Números",m_words:"Palabras",
   st_time:"Tiempo",wpm:"PPM",accuracy:"Precisión",r_cpm:"Caract./min",r_errors:"Errores",r_raw:"PPM bruto",
   hint:'Haz clic aquí o pulsa <b>cualquier tecla</b> para empezar',btn_again:"Repetir",btn_share:"Copiar resultado",btn_copied:"¡Copiado!",
   hist_title:"Tu historial de mecanografía (guardado en este navegador)",h_date:"Fecha",h_test:"Prueba",
   hist_empty:"Aún no hay resultados: completa una prueba y aparecerá aquí."},
 hi:{_name:"हिन्दी",time:"समय",text:"पाठ",m_sentences:"वाक्य",m_quotes:"उद्धरण",m_numbers:"संख्याएँ",m_words:"शब्द",
   st_time:"समय",wpm:"WPM",accuracy:"सटीकता",r_cpm:"वर्ण/मिनट",r_errors:"त्रुटियाँ",r_raw:"रॉ WPM",
   hint:'यहाँ क्लिक करें या <b>कोई भी कुंजी</b> दबाकर टाइप करना शुरू करें',btn_again:"फिर से टेस्ट करें",btn_share:"परिणाम कॉपी करें",btn_copied:"कॉपी हो गया!",
   hist_title:"आपका टाइपिंग इतिहास (इस ब्राउज़र में सहेजा गया)",h_date:"तारीख",h_test:"टेस्ट",
   hist_empty:"अभी तक कोई परिणाम नहीं — एक टेस्ट पूरा करें और यह यहाँ दिखेगा।"},
 ar:{_name:"العربية",time:"الوقت",text:"النص",m_sentences:"جُمل",m_quotes:"اقتباسات",m_numbers:"أرقام",m_words:"كلمات",
   st_time:"الوقت",wpm:"ك/د",accuracy:"الدقة",r_cpm:"حرف/دقيقة",r_errors:"الأخطاء",r_raw:"السرعة الخام",
   hint:'انقر هنا أو اضغط <b>أي مفتاح</b> لبدء الكتابة',btn_again:"إعادة الاختبار",btn_share:"نسخ النتيجة",btn_copied:"تم النسخ!",
   hist_title:"سجل الكتابة الخاص بك (محفوظ في هذا المتصفح)",h_date:"التاريخ",h_test:"الاختبار",
   hist_empty:"لا توجد نتائج بعد — أكمل اختبارًا وسيظهر هنا."}
};

var POOL={
 zh:{sentences:["学习打字是一项非常实用的技能。","每天练习一点点，手指就会熟悉键盘。","保持良好的姿势可以让打字更快更准确。","准确比速度更重要，速度会随着准确提升。","认真练习，你的打字速度会稳步提高。"],
   quotes:["千里之行，始于足下。","业精于勤，荒于嬉。","不积跬步，无以至千里。","书山有路勤为径，学海无涯苦作舟。"],
   words:"的 一 是 不 了 人 我 在 有 他 这 中 大 来 上 国 个 到 说 们 为 子 和 你 地 出 道 也 时 年 得 就 那 要 下 以 生 会 自 着 去 之 过 家 学 对 可 她 里 后".split(" ")},
 es:{sentences:["Aprender a escribir rápido es una habilidad muy útil.","Practica un poco cada día y tus dedos conocerán el teclado.","Una buena postura hace que escribir sea más rápido y preciso.","La precisión es más importante que la velocidad al escribir.","El zorro marrón salta sobre el perro perezoso junto al río."],
   quotes:["El secreto de salir adelante es empezar. - Mark Twain","La calidad no es un acto, es un hábito. - Aristóteles","No esperes la oportunidad, créala. - George Bernard Shaw","El éxito es la suma de pequeños esfuerzos repetidos cada día."],
   words:"el la de que y a en un ser se no haber por con su para como estar tener le lo todo pero más hacer o poder decir este ir otro ese si me ya ver porque dar cuando él muy sin vez mucho saber qué sobre mi".split(" ")},
 hi:{sentences:["तेज़ टाइप करना सीखना एक बहुत उपयोगी कौशल है।","हर दिन थोड़ा अभ्यास करें और आपकी उंगलियाँ कीबोर्ड सीख लेंगी।","अच्छी मुद्रा से टाइपिंग तेज़ और अधिक सटीक होती है।","टाइप करते समय गति से अधिक सटीकता महत्वपूर्ण है।","रोज़ अभ्यास करने से आपकी गति बढ़ती जाएगी।"],
   quotes:["आगे बढ़ने का रहस्य शुरुआत करना है।","गुणवत्ता एक आदत है, एक कार्य नहीं।","अवसर की प्रतीक्षा मत करो, उसे बनाओ।","सफलता छोटे-छोटे प्रयासों का योग है।"],
   words:"और का के की है में से को पर यह था एक नहीं हैं जो वह कर ने तो भी हो गया कि अपने सकता लिए होता करने वाले बाद लेकिन दिया जाता कई किया रहा इस तक साथ".split(" ")},
 ar:{sentences:["تعلُّم الكتابة بسرعة مهارة مفيدة جدًا.","تدرّب قليلًا كل يوم وستتعلم أصابعك لوحة المفاتيح.","الجلسة الصحيحة تجعل الكتابة أسرع وأكثر دقة.","الدقة أهم من السرعة عند الكتابة.","التدريب اليومي يرفع سرعتك باطّراد."],
   quotes:["سرُّ التقدم هو البدء.","الجودة ليست فعلًا بل عادة.","لا تنتظر الفرصة، اصنعها.","النجاح حصيلة جهود صغيرة تتكرر كل يوم."],
   words:"من في على إلى عن مع هذا ذلك التي الذي كان قد لا ما هو هي نحن أنت كل بعض عند بين قبل بعد حيث لكن أو ثم كما حتى إذا لأن منذ خلال ضد نحو".split(" ")}
};

var LANGS=["en","zh","es","hi","ar"];
var THEMES=[["dark","🌙"],["light","☀️"],["ocean","🌊"]];
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}

var TR={lang:"en"};
TR.t=function(k){var d=I18N[TR.lang]||I18N.en;return (d[k]!=null?d[k]:I18N.en[k])||"";};
TR.pool=function(l){return POOL[l]||null;};
var UNITS={en:{s:"s",m:" min"},zh:{s:"秒",m:"分"},es:{s:" s",m:" min"},hi:{s:" सेकंड",m:" मिनट"},ar:{s:" ث",m:" د"}};
TR.fmtDur=function(sec,l){var u=UNITS[l]||UNITS.en;return sec<60?(sec+u.s):((sec/60)+u.m);};
TR.modeLabel=function(m){return TR.t("m_"+m)||m;};
window.TR=TR;
function updateDurChips(){
  var ch=document.querySelectorAll(".chip.dur");
  for(var i=0;i<ch.length;i++){var d=parseInt(ch[i].getAttribute("data-d"),10);if(!isNaN(d))ch[i].textContent=TR.fmtDur(d,TR.lang);}
}

function translate(){
  var d=I18N[TR.lang]||I18N.en;
  var els=document.querySelectorAll("[data-i18n]");
  for(var i=0;i<els.length;i++){var k=els[i].getAttribute("data-i18n");if(d[k]!=null||I18N.en[k]!=null)els[i].textContent=TR.t(k);}
  var hs=document.querySelectorAll("[data-i18n-html]");
  for(var j=0;j<hs.length;j++){var kk=hs[j].getAttribute("data-i18n-html");hs[j].innerHTML=TR.t(kk);}
}

function setLang(l,fire){
  if(LANGS.indexOf(l)<0)l="en"; TR.lang=l; ls("trLang",l);
  document.documentElement.lang=l;
  document.documentElement.dir=(l==="ar")?"rtl":"ltr";
  translate();
  updateDurChips();
  if(fire)window.dispatchEvent(new Event("tr-relang"));
}
function setTheme(t){
  if(t==="dark")document.documentElement.removeAttribute("data-theme");
  else document.documentElement.setAttribute("data-theme",t);
  ls("trTheme",t);
  var btns=document.querySelectorAll(".tr-theme-btn");
  for(var i=0;i<btns.length;i++)btns[i].setAttribute("aria-pressed", btns[i].getAttribute("data-theme")===t?"true":"false");
}

function buildBar(){
  var css=document.createElement("style");
  css.textContent=
   ".tr-bar{display:flex;align-items:center;gap:12px;margin-left:auto;}"+
   ".tr-sel{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:999px;"+
     "padding:6px 30px 6px 13px;font-size:.85rem;font-weight:600;cursor:pointer;font-family:inherit;"+
     "-webkit-appearance:none;appearance:none;transition:border-color .15s,background .15s;"+
     "background-image:url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'><path d='M1 1l4 4 4-4' stroke='%238b8fa3' stroke-width='1.6' fill='none' stroke-linecap='round'/></svg>\");"+
     "background-repeat:no-repeat;background-position:right 12px center;}"+
   "html[dir=rtl] .tr-sel{padding:6px 13px 6px 30px;background-position:left 12px center;}"+
   ".tr-sel:hover{border-color:var(--borderhi);background-color:var(--panelhi);}"+
   ".tr-themes{display:inline-flex;gap:4px;background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:3px;}"+
   ".tr-theme-btn{border:none;background:transparent;cursor:pointer;border-radius:999px;width:30px;height:28px;"+
     "font-size:.95rem;line-height:1;display:inline-flex;align-items:center;justify-content:center;transition:background .15s;padding:0;}"+
   ".tr-theme-btn:hover{background:var(--panelhi);}"+
   ".tr-theme-btn[aria-pressed=true]{background:linear-gradient(180deg,var(--accent2),var(--accent));box-shadow:0 3px 10px -4px var(--accentglow);}";
  document.head.appendChild(css);

  var bar=document.createElement("div"); bar.className="tr-bar";
  var sel=document.createElement("select"); sel.className="tr-sel"; sel.setAttribute("aria-label","Language");
  for(var i=0;i<LANGS.length;i++){var o=document.createElement("option");o.value=LANGS[i];o.textContent=I18N[LANGS[i]]._name;sel.appendChild(o);}
  sel.value=TR.lang;
  sel.addEventListener("change",function(){setLang(sel.value,true);});
  bar.appendChild(sel);

  var tw=document.createElement("div"); tw.className="tr-themes";
  var cur=ls("trTheme")||"dark";
  for(var k=0;k<THEMES.length;k++){
    (function(th){var btt=document.createElement("button");btt.className="tr-theme-btn";btt.setAttribute("data-theme",th[0]);
      btt.setAttribute("type","button");btt.setAttribute("aria-label",th[0]+" theme");btt.textContent=th[1];
      btt.setAttribute("aria-pressed", th[0]===cur?"true":"false");
      btt.addEventListener("click",function(){setTheme(th[0]);});tw.appendChild(btt);})(THEMES[k]);
  }
  bar.appendChild(tw);

  var header=document.querySelector("header.top");
  if(header){header.appendChild(bar);}
  else{bar.style.position="fixed";bar.style.top="12px";bar.style.right="12px";bar.style.zIndex="50";document.body.appendChild(bar);}
}

function init(){
  buildBar();
  setLang(ls("trLang")||"en",false);
  setTheme(ls("trTheme")||"dark");
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);
else init();
})();
