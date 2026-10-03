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

var POOL=/*{{POOL}}*/;

(function(){var R={en:"Click to resume",zh:"点击继续打字",es:"Haz clic para continuar",hi:"जारी रखने के लिए क्लिक करें",ar:"انقر للمتابعة"};for(var k in R){if(I18N[k])I18N[k].resume=R[k];}})();
(function(){var R={en:"Keyboard",zh:"键盘大小",es:"Teclado",hi:"कीबोर्ड",ar:"لوحة المفاتيح"};for(var k in R){if(I18N[k])I18N[k].kbd_size=R[k];}})();
(function(){var M={
 r_cons:{en:"Consistency",zh:"稳定性",es:"Consistencia",hi:"स्थिरता",ar:"الثبات"},
 sound:{en:"Sound",zh:"音效",es:"Sonido",hi:"ध्वनि",ar:"الصوت"},
 on:{en:"on",zh:"开",es:"sí",hi:"चालू",ar:"تشغيل"},
 off:{en:"off",zh:"关",es:"no",hi:"बंद",ar:"إيقاف"},
 pb_new:{en:"New personal best!",zh:"刷新个人最佳！",es:"¡Nuevo récord personal!",hi:"नया व्यक्तिगत सर्वश्रेष्ठ!",ar:"أفضل رقم شخصي جديد!"},
 pb_prev:{en:"Personal best",zh:"个人最佳",es:"Récord personal",hi:"व्यक्तिगत सर्वश्रेष्ठ",ar:"أفضل رقم شخصي"}
};for(var key in M){var R=M[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
/* a11y: aria-label 也跟随语言切换（[data-aria] 元素）*/
(function(){var A={
 skip:{en:"Skip to typing test",zh:"跳到打字测试",es:"Saltar a la prueba",hi:"टाइपिंग टेस्ट पर जाएँ",ar:"تخطّي إلى اختبار الكتابة"},
 input_aria:{en:"Typing input",zh:"打字输入框",es:"Campo de escritura",hi:"टाइपिंग इनपुट",ar:"حقل الكتابة"},
 timer_aria:{en:"Time remaining",zh:"剩余时间",es:"Tiempo restante",hi:"शेष समय",ar:"الوقت المتبقي"},
 chart_aria:{en:"WPM over time line chart",zh:"WPM 随时间变化折线图",es:"Gráfico de PPM en el tiempo",hi:"समय के साथ WPM रेखाचित्र",ar:"رسم بياني للسرعة عبر الزمن"}
};for(var key in A){var R=A[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
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
  var da=document.querySelectorAll("[data-aria]");
  for(var n=0;n<da.length;n++){var ka=da[n].getAttribute("data-aria");var av=TR.t(ka);if(av)da[n].setAttribute("aria-label",av);}
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
