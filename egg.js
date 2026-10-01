/* Easter egg: Konami code (↑↑↓↓←→←→ B A) summons a trendy kawaii cartoon cat.
   Pure SVG + CSS, zero deps. Esc / click to dismiss. */
(function(){
  window.__eggReady=1;
  var seq=["ArrowUp","ArrowUp","ArrowDown","ArrowDown","ArrowLeft","ArrowRight","ArrowLeft","ArrowRight","b","a"];
  var pos=0;
  document.addEventListener("keydown",function(e){
    var k=e.key.length===1?e.key.toLowerCase():e.key;
    pos=(k===seq[pos])?pos+1:((k===seq[0])?1:0);
    if(pos===seq.length){pos=0;launch();}
  },true);

  function launch(){
    if(document.getElementById("neko-egg"))return;
    var css=document.createElement("style");
    css.textContent=[
"#neko-egg{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;",
"background:rgba(10,11,15,.55);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);animation:nk-fade .35s ease;}",
"#neko-egg .card{position:relative;padding:30px 34px 26px;border-radius:26px;text-align:center;",
"background:linear-gradient(145deg,rgba(255,255,255,.14),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.22);",
"box-shadow:0 24px 70px rgba(0,0,0,.5);animation:nk-pop .55s cubic-bezier(.18,1.5,.5,1);}",
"#neko-egg .cat{width:200px;height:200px;animation:nk-bob 2.4s ease-in-out infinite;}",
"#neko-egg h3{margin:14px 0 4px;font:800 1.35rem/1.2 system-ui,sans-serif;color:#fff;letter-spacing:-.5px;}",
"#neko-egg p{margin:0;font:500 .92rem/1.4 system-ui,sans-serif;color:#c9cbe0;}",
"#neko-egg .hint{margin-top:12px;font-size:.76rem;color:#8b8fa3;}",
"#neko-egg .ear{transform-origin:center;animation:nk-ear 3s ease-in-out infinite;}",
"#neko-egg .tail{transform-origin:12px 150px;animation:nk-tail 1.6s ease-in-out infinite;}",
"#neko-egg .paw{transform-origin:center;animation:nk-wave 1.1s ease-in-out infinite;}",
"#neko-egg .lid{transform-origin:center;animation:nk-blink 3.6s infinite;}",
"@keyframes nk-fade{from{opacity:0}to{opacity:1}}",
"@keyframes nk-pop{0%{transform:scale(.4) translateY(40px);opacity:0}100%{transform:scale(1) translateY(0);opacity:1}}",
"@keyframes nk-bob{0%,100%{transform:translateY(0) rotate(-1deg)}50%{transform:translateY(-10px) rotate(1deg)}}",
"@keyframes nk-ear{0%,90%,100%{transform:rotate(0)}94%{transform:rotate(-8deg)}}",
"@keyframes nk-tail{0%,100%{transform:rotate(-10deg)}50%{transform:rotate(16deg)}}",
"@keyframes nk-wave{0%,100%{transform:rotate(0)}50%{transform:rotate(-26deg)}}",
"@keyframes nk-blink{0%,92%,100%{transform:scaleY(1)}96%{transform:scaleY(.08)}}",
"@keyframes nk-conf{to{transform:translateY(360px) rotate(720deg);opacity:0}}",
".nk-conf{position:absolute;top:-10px;width:9px;height:14px;border-radius:2px;animation:nk-conf 1.3s linear forwards;}"
    ].join("");
    document.head.appendChild(css);

    var o=document.createElement("div");o.id="neko-egg";
    o.innerHTML=
      '<div class="card">'+
      '<svg class="cat" viewBox="0 0 200 210" fill="none" xmlns="http://www.w3.org/2000/svg">'+
        '<defs>'+
          '<linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">'+
            '<stop offset="0" stop-color="#ffd6a5"/><stop offset="1" stop-color="#ffb3c6"/></linearGradient>'+
          '<linearGradient id="g2" x1="0" y1="0" x2="1" y2="1">'+
            '<stop offset="0" stop-color="#a0c4ff"/><stop offset="1" stop-color="#bdb2ff"/></linearGradient>'+
        '</defs>'+
        '<path class="tail" d="M18 150 q-26 -34 6 -62 q10 -8 20 2" stroke="url(#g2)" stroke-width="13" stroke-linecap="round"/>'+
        '<ellipse cx="100" cy="168" rx="52" ry="40" fill="url(#g2)"/>'+
        '<g class="ear"><path d="M58 54 L46 18 L84 42 Z" fill="url(#g1)"/>'+
        '<path d="M142 54 L154 18 L116 42 Z" fill="url(#g1)"/></g>'+
        '<circle cx="100" cy="86" r="56" fill="url(#g1)"/>'+
        '<circle cx="78" cy="92" r="4" fill="#5a3a3a" class="lid"/>'+
        '<circle cx="122" cy="92" r="4" fill="#5a3a3a" class="lid"/>'+
        '<ellipse cx="76" cy="106" rx="9" ry="6" fill="#ff8fab" opacity=".6"/>'+
        '<ellipse cx="124" cy="106" rx="9" ry="6" fill="#ff8fab" opacity=".6"/>'+
        '<path d="M94 98 q6 7 12 0" stroke="#5a3a3a" stroke-width="3" stroke-linecap="round"/>'+
        '<path d="M60 86 h-22 M60 94 h-20 M140 86 h22 M140 94 h20" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".7"/>'+
        '<path class="paw" d="M150 150 q16 -4 16 14" stroke="url(#g1)" stroke-width="12" stroke-linecap="round"/>'+
      '</svg>'+
      '<h3>You found the secret cat! 🐱</h3>'+
      '<p>Keep typing fast and this little one purrs for you. 🐾</p>'+
      '<div class="hint">press Esc or click anywhere to close</div>'+
      '</div>';
    document.body.appendChild(o);

    // confetti
    var cols=["#ffd6a5","#ffb3c6","#a0c4ff","#bdb2ff","#caffbf","#9bf6ff"];
    for(var i=0;i<40;i++){
      var c=document.createElement("div");c.className="nk-conf";
      c.style.left=(Math.random()*100)+"%";
      c.style.background=cols[i%cols.length];
      c.style.animationDelay=(Math.random()*.5)+"s";
      c.style.transform="translateY(0) rotate("+(Math.random()*360)+"deg)";
      o.appendChild(c);
    }
    function close(){o.remove();}
    o.addEventListener("click",close);
    document.addEventListener("keydown",function esc(e){if(e.key==="Escape"){close();document.removeEventListener("keydown",esc);}});
  }
})();
