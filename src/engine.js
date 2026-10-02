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
function pickText(mode){
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
var dur=60, mode="sentences", text="", chars=[], timer=null, startAt=0, finished=false, errCount=0, totalTyped=0;
var wpmSamples=[]; var _prevLen=0;
function mmss(s){return Math.floor(s/60)+":"+String(s%60).padStart(2,"0");}
function render(){
  var h="";
  for(var i=0;i<chars.length;i++){
    var c=chars[i];
    if(i===totalTyped && !finished){h+='<span class="cur">'+esc(c.t)+'</span>';continue;}
    if(i<totalTyped){h+='<span class="'+(c.ok?"ok":"bad")+'">'+esc(c.t)+'</span>';}
    else{h+=esc(c.t);}
  }
  elText.innerHTML=h;
  highlightKey();
}
function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function reset(){
  clearInterval(timer); text=pickText(mode);
  chars=[]; for(var i=0;i<text.length;i++){chars.push({t:text[i],ok:false});}
  totalTyped=0; errCount=0; finished=false; startAt=0;
  elT.textContent=mmss(dur); elW.textContent="0"; elA.textContent="100%";
  elRes.style.display="none"; elHint.style.display="block";
  wpmSamples=[]; clearChart();
  render(); elIn.value="";
}
function stats(){
  var el=0; for(var i=0;i<totalTyped;i++){if(chars[i]&&!chars[i].ok)el++;}
  var mins=(Date.now()-startAt)/60000;
  if(mins<=0)mins=1/60000;
  var correct=totalTyped-el;
  return {wpm:Math.round((correct/5)/mins), raw:Math.round((totalTyped/5)/mins),
          acc: totalTyped? Math.round(correct/totalTyped*100):100, err:el,
          cpm:Math.round(totalTyped/mins)};
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
  var bs=document.querySelectorAll(".kbd-size"); for(var j=0;j<bs.length;j++)bs[j].classList.toggle("on",bs[j].getAttribute("data-ks")===k);
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
  var v=elIn.value;
  totalTyped=v.length;
  errCount=0;
  for(var i=0;i<totalTyped;i++){if(chars[i]){chars[i].ok=(chars[i].t===v[i]); if(!chars[i].ok)errCount++;}}
  if(typeof click_==="function" && v.length>_prevLen){var _lc=chars[v.length-1]; click_(_lc?!_lc.ok:false);}
  _prevLen=v.length;
  render();
  showLive();
  if(totalTyped>=chars.length){finish();}
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
  chipsD.forEach(function(x){x.classList.remove("on");}); c.classList.add("on");
  dur=parseInt(c.getAttribute("data-d"),10); reset();
});});
chipsM.forEach(function(c){c.addEventListener("click",function(){
  chipsM.forEach(function(x){x.classList.remove("on");}); c.classList.add("on");
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
buildKbd(); reset();
})();
