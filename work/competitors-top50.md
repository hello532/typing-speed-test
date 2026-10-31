# Competitors Top 50 — SERP research for typing.rerivo.com

**Collected:** 2026-10-31 (Asia/Hong_Kong). **Target site:** `typing.rerivo.com` (free online typing test, ~140 existing pages).
**Method:** (1) direct HTTP fetch of every candidate homepage + `/sitemap.xml` + sampled sub-pages with a desktop Chrome UA, parsing `<title>`, `<meta name=description>`, `<h1>`, JSON-LD `@type` values, `<details>`/FAQ markup and sitemap URL patterns; (2) Bing en-US SERP capture for 44 query strings via HTML scrape and `format=rss`; (3) Exa semantic search/fetch for query families Bing mangled and for sites that block bots.
**No traffic, backlink, DR or ranking-volume figure in this file is measured.** Anything of that kind is written as `not observed`.

**Page-type legend** (derived from sitemap paths + anchor text I actually parsed): `T` test tool · `D` duration/mode variants · `L` lessons/course · `G` games · `R` race/multiplayer · `B` blog/guides · `Lg` by-language · `C` certificate · `J` jobs/exams · `K` kids/school · `KB` keyboard layouts · `S` stats/benchmarks · `TL` calculators/tools.

---

## 1. The 50 strongest verified-live English typing sites

Selection rule (so the cut is auditable): live English homepage that actually serves a typing test/practice product, ranked by *observed* signals only — appearance across independent SERP families in my own captures, feature breadth from sitemap/nav, and served-page depth (sitemap URL count). Big brands were not assumed; each row is a fetch I performed. `n=` is sitemap URL count where a sitemap was served.

| # | domain | page types visible | homepage `<title>` (verbatim) | meta description (len → quote) | structured data / FAQ block | apparent strength (observable) |
|---|---|---|---|---|---|---|
| 1 | typing.com | T·D·L·G·B·Lg·C·J·K | Learn to Type \| Type Better \| Type Faster - Typing.com - Typing.com | 148 → "World's most popular free typing program! Typing.com's K–12 typing curriculum features touch typing, digital citizenship…" | no JSON-LD on home; no FAQ block on home | n=1,840; 1,507 lesson-path URLs; B2B paths `/teachers /homeschool /schools_districts /curriculum`; brand duplicated in title |
| 2 | typingclub.com | T·L·B·Lg·C·J·K | `Learn Touch Typing Free - TypingClub` | 120 → "Learn touch typing online using TypingClub's free typing courses. It includes 650 typing games, typing tests and videos." | `Organization`,`WebSite` only | n=1,604; 802 localized paths (`/es_MX/`,`/de/`,`/fr/`); `/library` marketplace |
| 3 | typingtest.com | T·D(30s–10min)·L·B·C·S | Free Typing Test - Check Your WPM \| TypingTest.com | 122 → "Take a free online typing test to check your WPM, typing speed, and accuracy. Get instant results…" | `Answer`,`FAQPage`,`Question` on home **and** on test pages | only 14 sitemap URLs yet dominant across nearly every test-intent SERP I captured; 6 duration hubs + `/benchmark.php`, `/trainer/`, `/bigram-blitz/` |
| 4 | 10fastfingers.com | T·Lg(60+)·R·D·B | `10FastFingers - Typing Test, Competitions, Practice & Typing Games` | 157 → "Free typing test: check your typing speed in WPM, join typing competitions, practice with custom texts and play typing g…" | `Organization`,`WebSite`,`BreadcrumbList`,`ListItem` | n=371; competition + multiplayer layer; ~50 `/typing-test/{language}` pages |
| 5 | monkeytype.com | T·D(modes)·KB(themes)·leaderboard | Monkeytype \| A minimalistic, customizable typing test | 162 → "The most customizable typing test website with a minimal design and a ton of features. Test yourself in various modes, t…" | none on home | n=9, SPA; brand carried by product culture, **zero** lessons/blog content |
| 6 | keybr.com | T·L(algorithmic)·Lg(60)·KB | `Practice` | 59 → "Typing practice lessons to improve your speed and accuracy." | none on home | n=234; 60 language paths; **title tag is the single word "Practice"** — weakest title on this list |
| 7 | ratatype.com | T·L·C·KB·B | `Ratatype — Online Touch Typing Tutor and Typing Practice` | 189 → "Learn how to type faster 🎯. Take typing lessons on touch typing tutor Ratatype 💻, practice your keyboarding skills onlin…" | `Answer`,`FAQPage`,`Question` | no sitemap.xml served; `/typing-test/` page is 2,830 words with FAQ + certificate funnel; hreflang on 13 links |
| 8 | typing.academy | T·L·pro-tier·Lg | `TypingAcademy: Learn touch typing with our free typing practice` | 132 → "Learn to type with 10 fingers and practice your typing skills online. We offer everything you need to master touch typin…" | none on home | sitemap 404; H1 reads "Learn touch typing with **TypeLift**" → rebrand in flight (observed mismatch title↔H1) |
| 9 | typeracer.com | T·R·G·leaderboard·quotes | `TypeRacer - Play Typing Games and Race Friends` | 323 → "Test your typing skills today! Play against real live people from all over the world. TypeRacer is the best free massive…" | none observed | race-first brand; sitemap 522 (blocked); practice gated behind login |
| 10 | nitrotype.com | G·R·K·teams·standings | Nitro Type \| Competitive Typing Game \| Race Your Friends | 156 → "Amp up your typing speed while competing against others around the globe in our fun online typing game! Free to play and…" | `Offer`,`WebApplication` | game-first, teen audience; no lessons, no blog observed; 3 words of body text on home |
| 11 | typesy.com | software/app·L·K·KB·B·pricing | Typesy \| Touch Typing & Keyboarding Software & App | **50** → "Typesy \| Touch Typing & Keyboarding Software & App" (desc = title, 50 chars) | `AggregateRating`,`Answer`,`FAQPage` | n=500; app funnel (Win/Mac/iOS); description is a duplicate of the title |
| 12 | typingmaster.com | software·L·T·G·school | Typing Practice, Tests & Typing Tutor Software \| TypingMaster | 156 → "Increase your typing speed with TypingMaster 12 for Windows. Take a free 1-week course with interactive lessons, games…" | `AggregateRating`,`Answer`,`FAQPage` | n=39; legacy desktop brand with thin web surface |
| 13 | typingpal.com | L·Lg(235)·G·school·B(255) | Learn Touch Typing Online \| Typing Pal | 163 → "Typing Pal: Learn to Type Faster on your Keyboard! Take our speed test and learn the best touch typing method. Hundreds…" | none observed | n=470; education/teacher channel; large blog path count |
| 14 | typingmentor.com | T·L·custom-text·D | Free Typing Practice Online \| TypingMentor | 138 → "Practice typing online for free with common words, custom text, Zen mode, timed or word-count sessions, punctuation, num…" | `BreadcrumbList`,`ListItem`,`Offer` | **n=2,843 — largest URL footprint in the sample** |
| 15 | typingstudy.com | L(25,403 lesson URLs)·Lg(501)·G·KB | `Touch Typing Practice Online` | 100 → "Free online touch typing course and typing tests. Interactive typing lessons, games and speed tests." | none observed | **n=26,497**; extreme programmatic lesson × language coverage |
| 16 | agilefingers.com | L·Lg(1,121)·G·K·S | Typing Practice - Learn Touch Typing \| AgileFingers | 128 → "Master touch typing skills through interactive free online typing practice, including a typing course, games, and a typi…" | `Answer`,`Course`,`FAQPage`; 5 `<details>` | n=2,649; 1,121 localized prefixes; hreflang on 43 links |
| 17 | sense-lang.org | L·courses·G·T | `Learn How to Type - Free Typing Classes & Lessons Online` | 153 → "Since 2001, our learning method has been proven to help millions of people around the world learn, practice, and improve…" | none observed | legacy course brand; sitemap 404; "since 2001" as trust asset |
| 18 | rapidtyping.com | L·G(189)·Lg(56)·T | `Typing Tutor` | 128 → "Site about touch typing technics, here you can download typing tutor, get online typing test and to play in online typin…" | none observed | n=400; course + game mix; title carries no brand |
| 19 | speedtypingonline.com | T·G(101)·L(50)·D | `Free Online Typing Test - Results in 60 seconds!` | 158 → "Free online typing test to see how fast you type! Features lots of text options and many test lengths. Easy and fun way…" | none observed | n=184; classic multi-test page; 301 KB home HTML |
| 20 | typing.io | code typing·Lg | Typing Practice for Programmers \| typing.io | 95 → "Typing.io is a typing tutor for programmers. Practice typing the hard-to-reach symbols in code." | none | n=3; single-product programmer niche |
| 21 | speedtyper.dev | code typing·snippets·leaderboard | SpeedTyper.dev \| Typing practice for programmers | 323 → "speedtyper.dev is a typing application for programmers. Battle against other developers by typing challenges from real o…" | none | dev-only niche, 323-link surface |
| 22 | typelit.io | books·library·progress | `Practice typing by retyping ENTIRE books — TypeLit.io | 154 → "Free Typing Practice \| Boost your typing speed while reading great books like Alice in Wonderland, 1984, Dracula…" | AggregateRating`,`Answer`,`Article`,`FAQPage`,`Audience` | n=274; unique "type a whole book" hook; home prints "Sources: Project Gutenberg + Wikipedia" |
| 23 | thetypingcat.com | L(555)·courses·G·B·KB | `The Typing Cat - Free Online Typing Tutor, Courses & Games` | 193 → "Learn touch typing with free structured courses, speed tests, typing games, and code-typing practice for HTML & JavaScri…" | `AggregateRating`,`BreadcrumbList` | n=625; lesson library + code typing; heavy 229 KB home |
| 24 | keyhero.com | T·leaderboard·stats | `Typing Test · Improve your WPM speed` | 142 → "Typing Test and exercises to improve your WPM (word per minute) speed. Check your typing speed against our Community and…" | none | legacy minimal test; sitemap served but empty |
| 25 | typingbee.com | K·G(11)·classroom | Typing for Kids \| TypingBee | **24** → "Typing website for kids." (24 chars — shortest observed) | none | n=29; K-6 school niche only; almost no on-page SEO |
| 26 | typinggames.zone | G(155)·B·leaderboard | `TypingGames.Zone - 155 Fun Typing Games: Learn to Type` | 150 → "Kids & Adults, get typing like a pro! Fun & educational games like KeyTower, TypeRush & Guitar Type make learning FUN!…" | `Offer`,`Thing`,`Product` | n=160; pure game directory; number in title ("155") is a CTR device |
| 27 | typinggames.io | G·B(3,406 blog-path URLs) | `TypingGames - Anime Edition` | 0 → **no meta description served** | none observed | n=3,408 (3,406 under `/blog/`); thin 9 KB home; anime reskin, no test product |
| 28 | freetypinggame.net | L·G·T·C·D·Lg | Free typing games, typing lessons and typing tests. \| FreeTypingGame.net | 182 → "Play Free typing games, typing lessons and typing tests online. 30 keyboarding lessons including homerow. Have fun comp…" | none observed | 1999-era design; no sitemap; still ranks for "typing games" |
| 29 | powertyping.com | L·G·K·KB(Dvorak) | `Free typing tutor online with free typing lessons.` | **265** → "Free typing tutor online with typing lessons for Qwerty, Simplified Dvorak, and Programmer Dvorak keyboards. In typing l…" | none | n=32; needs `<title>` work; Dvorak/Programmer-Dvorak angle |
| 30 | learn2type.com | L(10)·T·C | `Typing Test and Free Learn to Type Tutor Online` | 167 → "Learn to Type online with typing test and free typing lessons. Master the skills of touch typing with online speed tests…" | none | n=36; legacy, thin |
| 31 | typingpractice.org | T·L(38)·D(21)·Lg(76)·C(7) | Typing Practice Online \| TypingPractice.Org | 144 → "Typing Practice online for free with AI-powered error analysis, typing tests, lessons, games, multilingual typing tools…" | `AggregateRating`,`ContactPoint` | n=237; practice-first + certificate pages; "AI-powered error analysis" claim |
| 32 | typingtestpractice.com | T·L(43)·D(6) | `Typing speed Test - TypingTestPractice.com` | 134 → "Free online typing test to see how fast you type! Easy and fun way to test and improve your typing speed with typing pra…" | none | n=113; practice/test pair only |
| 33 | typetest.io | T·G(7)·D | `TypeTest.io - Test Your Typing Speed and Improve Your WPM` | 155 → "A clean and simple typing test website. Take timed tests of different durations to find out your WPM, track your progres…" | none | n=17; minimal app, 94 KB home |
| 34 | typingspeedcheck.com | T·L(11) | `Free Typing Speed Test Check Your WPM Online` | 154 → "Take our free typing speed test and check your WPM instantly. Practice typing, improve speed, and track accuracy no sign…" | `Answer`,`EntryPoint`,`FAQPage`,`Offer` | n=24; small but fully semantic-marked |
| 35 | typing-speed.net | T·WPM/CPM toggle | `Typing Speed Test - Online & free!` | 226 → "Test your writing speed: Find out how many letters and words you can type per minute - Easy, online and completely free." | none | minimal product; longest description observed (226) |
| 36 | wpmtest.org | T·D | `WPM Test - Free Word Per Minute Typing Test Online` | 133 → "WPM Test offers a free word per minute typing test online and also a certification. It shows the real-time typing result…" | `Answer` present (FAQ text) | n=7; exact-match domain, almost no content |
| 37 | typingtest.now | T·D(15s–10min)·G·B·Lg(ES)·C·J·K·classroom·leaderboard·TL·glossary | `Free Typing Test — Check Your WPM Online — TypingTest.now` | 146 → "Free online typing test. Measure your WPM and accuracy, improve your speed, and track progress over time. 16 themes, 5 m…" | **`Answer`,`AggregateRating`,`BreadcrumbList`,`CollectionPage`,`FAQPage`,`ItemList`,`ListItem`,`Offer`,`Org`**; 7 `<details>` | n=395; heaviest schema deployment observed; full `/es/` mirror; live-stats blocks on test pages |
| 38 | typingtest.me | T·D(5)·C·B(9) | Free Typing Test - Check Your Speed in 60 Seconds \| TypingTest.me | 146 → "Stop guessing your WPM. Smash a 60-second test with honest scores, live accuracy, consistency rank, and a FREE printable…" | `ImageObject`,`Organization`,`WebPage`,`WebSite`; 10 `<details>` | n=22; "honest scores" positioning + free print certificate |
| 39 | typingowl.com | T·D·C·J(12)·data-entry·R·ranked·L·leaderboard·Lg | Free Typing Test – Check Your Typing Speed & Accuracy \| Typing Owl | 163 → "Take a free typing test online to measure your WPM and accuracy. Practice typing, improve your speed, track progress, an…" | `Answer`,`BreadcrumbList`,`ContactPoint`,`FAQPage`,`HowTo`,`Offer`; 12 `<details>` | n=123; job/data-entry cluster (`/data-entry-test`, `/certificate`, `/ranked-typing`) |
| 40 | typingmonk.com | T·D(46)·C·S·KB·10-key·code·daily | TypingMonk - Free Typing Speed Test \| Test Your WPM & Accuracy Online | 168 → "Free online typing test in English. Test your WPM and accuracy with 1-, 3-, or 5-minute typing tests. Keyboard speed pra…" | `Answer`,`BreadcrumbList`,`ContactPoint`,`EntryPoint`,`FAQPage`,`ListItem`,`Org`,`Person` | n=147; `/wpm-chart` has 4 tables + 1 cited external source; table-led content depth |
| 41 | jobtypingtest.com | J(role pages)·D·C($9.99)·TL | Free Typing Test â JobTypingTest.com \| JobTypingTest.com | 86 → "Free typing speed test. Pick your time, start typing, see your WPM. No sign-up needed." | `Answer`,`BreadcrumbList`,`FAQPage`,`ListItem`,`Organization`,`Question` | n=45; 10 role pages (911 dispatcher → USPS → federal); **title contains mojibake `â` and duplicated brand suffix** |
| 42 | toptypingtest.com | 10-key·J(151)·Lg(4 locales)·D(25)·C(7) | 10-Key Speed Test - Numpad & Data Entry Tests \| TopTypingTest | 125 → "Free professional 10-key and numpad typing speed test. Measure your KPH for data entry, accounting, payroll, and office…" | `Organization`,`WebSite` | n=343; numpad/data-entry specialist; 4 locales (`/es/ /fr/ /de/ /pt/`) |
| 43 | online-typing.com | Exam(SSC)·Lg(Indian)·L·G·D·leaderboard | Free Typing Test — Check WPM & Accuracy \| OnlineTyping | 144 → "Take a free online typing test and check your WPM and accuracy in real time. Instant results, a free typing certificate,…" | `ContactPoint`,`EntryPoint`,`ImageObject` | n=84; `/exams/ssc-*`, `/in/{language}-typing-test` — India exam intent |
| 44 | onlinetyping.org | T·L·G·10-key·B(38)·Lg·leaderboard | `Online Typing Test - Typing Speed Test in just 60 seconds` | 139 → "Free online typing test portal, where you can test your typing speed with in 60 seconds. Also here you can learn and pra…" | `EducationalOrganization`,`WebSite` | n=117; "60 seconds" positioning in title |
| 45 | official-typing-test.com | T(1/3/5/10 min)·C(paid)·proctor info·L | Official-Typing-Test.com \| Typing Certificate - Online Typing Test | 110 → "Corporate testing software. Typing certificates. Free WPM typing tests. Free 10 key tests. No signup required." | none | n=21; 2013-era site; **sells** certificates (`/orderCertificate`); self-claims "over 1 million tests per month" (unverified) |
| 46 | typequicker.com | T·D(6)·B(24)·C·J·K | Typing Practice \| Learn to Type Faster | 164 → "TypeQuicker helps you type faster with AI-powered typing practice. Learn how to type faster, learn to type, and build fa…" | `Answer`,`FAQPage`,`ImageObject`,`Offer`; 6 `<details>` | n=203; 587 KB home (heaviest measured); practice + progress-chart angle |
| 47 | neattyping.com | T·TL·B·C·K | Free Typing Test & Online Learning Tools \| NeatTyping | 117 → "Free typing test, multiplication chart, memory games and reading tools for students, teachers and parents. No signup." | `Answer`,`FAQPage`,`Offer`,`Organization` | sitemap 404; teacher/parent tools-hub positioning; hreflang on 13 links |
| 48 | typing-practice.io | T·D(15s/30s/60s/no-timer)·L·G·J·K | `Typing Practice - Free Online Typing Practice` | 146 → "Free typing practice with 15s, 30s, 60s or no-timer modes. Type words, sentences or home row keys and see your WPM and a…" | `Answer`,`EntryPoint`,`FAQPage`,`Offer`,`Question`,`SearchAction`,`WebApplication` | n=84; "no-timer" mode as differentiator in title/H1 |
| 49 | thetypingpractice.com | L(per-finger)·G·B(18)·C·J·Lg(5 locales)·progress | Free Typing Practice & Test - Improve Your Speed \| The Typing Practice | 140 → "Free online typing practice with real-time WPM tracking, typing games, and detailed analytics. Improve your typing speed…" | `AggregateRating`,`AlignmentObject`,`BreadcrumbList`,`HowTo`,`ListItem`,`Offer`; 7 `<details>` | n=70; per-finger lesson URLs (`/lessons/home-row-f-j` …); `/es /pt /fr /de /id /tl` |
| 50 | typeblastgame.com | G·WPM-verdict pages·comparison pages | TypeBlast — Free Infinite Typing Game \| Play Online, No Signup | 193 → "Play TypeBlast — a free infinite typing game with endless falling words and unlimited rounds. No signup, no download. Bl…" | `Answer`,`Article`,`BreadcrumbList`,`FAQPage`,`ImageObject`,`ListItem`,`Person`,`QAPage` | n=51 built from **15 `/is-{40…150}-wpm-good` pages + 4 `/games-like-{nitro-type,ztype,typeracer,monkeytype}` pages**; byline + "Updated October 11, 2026" |

### 1b. Verified live, outside the top 50 (same fetch method)

| domain | `<title>` | n= |
|---|---|---|
| typingguild.com | `Typing Speed Test Online (Free, Powerful)` | 375 |
| typingdoctor.com | `TypingDoctor — Typing Test + Personalized Typing Coach` | 102 |
| klavatype.com | `Klava — Free Touch Typing Trainer and Typing Speed Test` | 126 |
| typingtom.com | Free Online Touch Typing Practice \| Typing Tom | n/a |
| typingspeedhub.com | Typing Speed Test + Practice \| Typing Speed Hub | 42 |
| ninjatyping.com | `Ninja Typing - Free Typing Test for Corporate & Govt Exams` | 57 |
| learn10key.com | Learn 10 Key.com \| Free Data Entry Tests | 9 |
| testmytyping.com | Free Typing Test Online - Check Your WPM & Accuracy \| TestMyTyping.com | n/a |
| wordcounter4u.com | `Free Word Counter, Typing Test & Writing Tools` | 652 |
| typingzoo.com | Typing Test - Check Your WPM Online \| Free Typing Speed Test | 14 |
| typingtester.io | Free Typing Test — Check Your WPM \| TypingTester.io | 23 |
| typespeedtest.com | `Free Typing Speed Test — Measure Your WPM in 60 Seconds` | 24 |
| fastfingertype.com | Free Typing Test, Typing Games & Writing Tools \| FastFingerType | 72 |
| fastfingers.net | `Fastfingers – Free Typing Test (English & 10-Finger Practice)` | 76 |
| typingcore.com | `Free Online Typing Test and Tips - Typing Core` | 72 |
| zty.pe | `ZType – Typing Game - Type to Shoot` | n/a |
| typings.gg | `typings` | n/a |
| wpm-test.com | `WPM Test - The typing speed test` | n/a |
| typing-speed-test.aoeu.eu | `Typing Test @ AOEU — Your typing speed in CPM and WPM` | n/a |
| typing-speed-test.com | `Typing Speed Test Online` | 3 |
| how-to-type.com | `How To Type - Free typing test, typing lessons and typing practice.` | n/a (403 to curl; read via Exa) |
| americanstandardtypingcertificates.com | `Accredited Online Typing Test Certificate for Employment` | n/a (read via Exa) |
| typingbaba.com | `Typing Baba - India's Leading Typing Website` | 157 |
| indiatyping.com | Hindi Typing \| Typing Test \| Hindi Typing Tutor \| Hindi Typing Software | n/a |

### 1c. Domains from the brief (and SERP lookalikes) that are NOT usable competitors

| domain | what I actually got | verdict |
|---|---|---|
| typingspeedtest.online | HTTP 200, `<title>FATCAI99 : Operator Resmi Situs Toto Macau…` | **expired → gambling site** (has `AggregateRating`/`Answer` schema bolted on) |
| typingarena.com | HTTP 200, `<title>Typing Arena â Online Casino Real Money…` | **expired → casino** |
| typingcat.com | HTTP 200, 1.4 KB "typingcat.com - Coming Soon 🚀" | parked |
| typingspeed.com | HTTP 200, "This domain may be for sale" (Above.com) | for sale |
| typingdots.com | HTTP 200, "pak to pak — we grow consumer apps" | repurposed agency |
| livetyping.com | HTTP 200, "Web and Mobile App Development in Washington DC" | repurposed agency |
| pctalk.com | HTTP 200, title pctalk.com \| Venture | repurposed |
| typingguru.com / typingleague.com / typingtestfree.com / typingspeedtest.com / typex.app | HTTP 200, **114 bytes, empty body** | dead/parked |
| typingtest.net | HTTP 200, 476 B JS cookie-challenge (`window.location.replace`) | live status unconfirmed — bot wall |
| how-to-type.net | 503 "Connection Closed" via local proxy **and** CRAWL_TIMEOUT via Exa | **unverified** (the real content site is `how-to-type.com`) |
| typing-sprint.com | 503 / CRAWL_TIMEOUT | unverified |
| wpm.training | 400; Exa `CRAWL_SSL_ERROR` | unverified |
| keysmash.io, epictyper.com, typewriter.gg, typing-zone.com, typingtester.net, cps-test.com, click-speed-test.com, typingfast.org, typingradar.com, typing-fun.com, freeonlinewritingpractice.com, typeorders.com | connection failed on both paths | unverified — do **not** cite these as live |
| thecalculatorsite.com | live, but `/sitemap.xml` 404 and a typing-speed article path 404/410 | **no typing test** — drop from competitor set |
| wordcounter.net | live, `/typing-test` → 404 | **no typing test** — drop |
| typingtest.io | HTTP 403 "Just a moment…" (Cloudflare) | unverified |

---

## 2. SERP intent map — what format wins each query family

Bing en-US, captured 2026-10-31. Two known artifacts I hit and am flagging up front: **(a)** Bing serves one cached 8-result block (typing.com / typingclub / typing.com lessons / typingtest.com / typingowl / typing-practice.io / ratatype / monkeytype) for many *low-volume* variants — I discard those rows as non-evidence; **(b)** Bing **parses numeric prefixes away**: `1 minute typing test` → results about the number 1, `2 minute typing test` → the number 2, `is 60 wpm good` → "60 Minutes" CBS. That mangling is itself a finding (see 2b).

| query family | what actually ranked (observed) | winning page format | format logic | fit for typing.rerivo.com |
|---|---|---|---|---|
| **typing test** | typingtest.com, typing.com, livechat.com (!), 10fastfingers, monkeytype, typespeedtest.com, speedtypingonline, typing-speed.net, typing-club.com | **bare test tool at root**, one screen, no scroll needed to start typing | user wants the widget, not a story; brands win on root URL | you have the tool; need root-level "no scroll to input" + WPM/accuracy above the fold |
| **wpm test** | typingtest.com, typing.com, monkeytype, online-typing.com, livechat.com, typequicker.com, typingtest.com/1-minute | **test tool + "what is WPM" paragraph** on the same URL | WPM is a synonym layer; same page double-dips both queries | `wpm-test-online` exists → add a 60-word definition + formula above the tool |
| **1 minute typing test** | Bing mangled; Exa nearest set = typingtest.now/typing-test/1-minute, holykeys.app, altto.co.uk, presspace.org, dotyping.com, type-faster.com, boosttyping.com, protypingtest.in; direct: typingtest.com/test/one-minute-typing-test | **dedicated single-duration tool page + certificate + live stats** | duration pages are cheap to build and each one owns a query | you already have 1/2/3/5/10-min + 30s; the differentiator now is *live stats + certificate on the same page*, not the timer |
| **typing practice** | typing.com lessons, typingtest.com practice, typingclub, neattyping ("No Time Limit"), keybr, speedtypingonline, thetypingpractice | **free course/lesson hub**, not a test | intent = improvement, not measurement | `typing-practice` is a test-shaped page; needs lesson-shaped sibling with drill links |
| **typing games** | typing.com/typing-games, typeracer, typing.com keyboard-jump, typinggames.zone (155), typingbee, nitrotype, freetypinggame, thetypingpractice games, thetypingcat | **game hub / single game**, brand-heavy, kids-safe framing | play intent, low commercial value, high bounce | `typing-games` + `typing-test-game` exist; the gap is *single named games* ("Keyboard Jump"-style pages) |
| **typing certificate** | typingtest.com/certificate, americanstandardtypingcertificates.com, typingtest.me, typingmonk, official-typing-test.com, jobtypingtest ($9.99), rockettyping, presspace, enjoytyping | **certificate landing page** = sample image + free/paid + verification + employer FAQ | buyer wants proof-of-legitimacy and speed | `typing-certificate` exists → missing: verifiable ID/QR, sample PDF, "will employers accept it" honesty block |
| **average typing speed** | typingtest.now ("Data From 100k Tests"), typing.com, typingspeedhub/statistics, thetypingpractice/typing-speed-chart, speedtypingonline, "Typing Speed Statistics… (2026)", "What Is a Good Typing Speed? [2026 WPM Benchmarks]" | **statistics/report page**: sample size + percentile table + year | informational; wins on *data provenance*, not tooling | `average-typing-speed` exists → add sample size, percentile table, cited studies, "updated" date |
| **typing test for jobs / data entry** | data entry: "Free Data Entry Speed Test - Typing Com", typingmonk, toptypingtest, "The Practice Test", jobtypingtest, typingowl/data-entry-test, learn10key, official-typing-test; jobs: jobtypingtest role pages, online-typing "for Adults — Workforce WPM Test" | **role/industry-specific test page with KPH + threshold table** | employer-driven, high commercial intent, weak incumbents | you have `data-entry-typing-test` + job pages; gap = **role pages** (nurse, 911 dispatcher, USPS, legal, call center) |
| **typing test for kids** | Bing cached-block (non-evidence); inventory evidence: typingbee.com (kids-only), typing.com "Browse by grade", typingclub classroom, typinggames.zone "Kids & Adults", thetypingpractice "for Kids & Students" | **grade-banded kids page + teacher/parent framing + no-ad promise** | parents/teachers search by grade and by "safe/free" | `typing-test-for-kids`, `typing-games-for-kids` exist → add grade-banded WPM expectations + classroom/teacher block |
| **touch typing** | Bing collapsed to entity "Touch" (KATSEYE/Merriam-Webster); inventory evidence: typingstudy ("Touch Typing Practice Online"), typingclub, typing.academy (H1 "Learn touch typing with TypeLift"), typing.com lessons, keybr, typingtom, agilefingers, klavatype | **course page with lesson 1 visible**, keyboard diagram, finger map | learning intent, long session, needs a curriculum promise | `touch-typing-test` is a test; add a course-shaped page with finger chart + 12-lesson path |
| **typing test 5 minutes** | typing.com 5-min, typingtest.com 5-min, freetypingtest.in, typingtom, fastfingers.net, typequicker, typingzoo, babatypingtest.in, typingtester.io | duration page again, but **.in domains compete hard** | near-zero barrier → dozens of low-authority pages rank | your 5-min page needs a reason to exist beyond the timer (endurance drop stat, employer use) |
| **typing test 10 key / data entry** | onlinetyping.org, testmytyping, typing.com numeric-keypad lesson, typingmonk, typingtest.now, speedtypingonline, learn10key, official-typing-test | **numpad test with KPH output + "KPH requirements by role" table** | KPH (not WPM) is the unit employers use | `ten-key-typing-test` exists → add KPH↔WPM conversion + role thresholds |
| **english typing test** | typingtest.com, typing.com, 10fastfingers, typingbaba, indiatyping, typingcore | **language-scoped test page** for the non-US English market | "english typing test" is largely an India/South-Asia query | you have `english-typing-test` + 10 language pages; localize KPH/exam framing for .in intent |
| **how to type faster** | typingclub, typing.com lessons, **wikiHow**, ninjatyping ("7 Steps… 2026 Guide"), how-to-type.com, typequicker, speedtypingonline | long-form guide, 7-step list, wikiHow dominates | editorial, E-E-A-T heavy; needs drills + numbers | you have 5+ how-to pages; the win is step counts + before/after WPM + embedded drills |

**2b. Query-parsing exploit (new, observed):** because Bing strips leading numerals, the *word-form* and *unit* variants are the defensible surface — "one minute typing test", "sixty second typing test", "60-second typing test", "two minute typing test". Your existing numeric-slug pages (`1-minute-typing-test`) should carry these as on-page H1/H2 variants and internal anchor text, not just in the slug.

**2c. Format competition summary (the key output):** three formats split this SERP space and they do **not** compete with each other —
1. **Tool page** (root or `/test/{duration}`) wins every measurement query (typing test, wpm test, duration variants, 10-key).
2. **Data/report page** (sample size, percentile table, year in title) wins `average typing speed`, `what is a good wpm`, `wpm chart`.
3. **Role/exam page** (job title or exam name in the URL) wins `typing test for {job}`, `data entry`, `ssc/bank`.
Lesson/course pages only win `touch typing` and `how to type faster`; game pages own only `typing games`; certificate pages own `typing certificate` and are the only ones with a paid SKU.

---

## 3. Content-gap list — 32 targets a new/low-authority site can take

Ranked by (observed weak incumbent) × (fits an existing rerivo page cluster). "Beatable because" cites what I actually saw.

| # | query | why competition is beatable | page must contain |
|---|---|---|---|
| 1 | `wpm to kph calculator` | jobtypingtest + typingspeedhub rank with one formula table; you have `keystrokes-per-hour-test` but **no converter tool** | live two-way converter, formula, 40/50/60 WPM reference rows, "what employers measure" note |
| 2 | `kph to wpm` | same, reverse intent; nobody owns the reverse string | reverse converter on the same URL, canonical to #1 |
| 3 | `net wpm calculator` / `gross vs net wpm` | typingdoctor has `/gross-vs-net-wpm` but serves **one global title** on every URL (observed duplication) | worked example with errors, formula, why certificates quote net |
| 4 | `typing speed percentile` | typingdoctor has the page but no unique title; no big brand owns it | percentile table + "you are faster than X%" calculator using your own test data |
| 5 | `is 40/50/70/80/90/100 wpm good` (verdict cluster) | typeblastgame built 15 near-identical pages and ranks; incumbents ignore the pattern | verdict-first H1, percentile, "what it's good for", adjacent-score links, 30-sec test CTA |
| 6 | `average typing speed by profession` | thetypingpractice chart has 4 rows and 562 words | 12+ professions, KPH where relevant, source line, sortable table |
| 7 | `typing test for nurses` | typingdoctor page exists but title/desc are the site's global pair | shift-chart/EMR phrasing, 45–60 WPM target, 3-min test embed |
| 8 | `typing test for 911 dispatcher` | only jobtypingtest has it (45-URL site) | CAD-style alphanumeric drill, 40 WPM/95% threshold, sample call codes |
| 9 | `usps postal exam typing test` | jobtypingtest ranks with a single page; no authority | exam format, address/mail-sorting drill, threshold table, dated note |
| 10 | `typing test for customer service / call center` | typingdoctor + jobtypingtest only; both thin | 35–45 WPM target, chat-response drill, accuracy emphasis |
| 11 | `typing test for legal secretary / paralegal` | nobody in my 100-site sample covers it well | legal-term dictation text, 60–80 WPM, formatting accuracy |
| 12 | `typing test for accountants` (10-key) | toptypingtest/learn10key only; no WPM↔KPH bridge | numpad drill with decimals, KPH targets, payroll example |
| 13 | `typing speed by grade (1st–8th)` | typing.com has grade paths but not a benchmark table | grade × WPM table with source, "what to expect each year" |
| 14 | `average typing speed for a 12 year old` | your `average-typing-speed-by-age` covers age; nobody owns the exact child query with numbers | single-age answer block + table + citation |
| 15 | `typing test for seniors / over 60` | typingdoctor has `/typing-test-for-seniors`, thin + duplicate title | larger type UI, slower default timer, dexterity notes |
| 16 | `typing speed on phone vs keyboard` | brand-new sites cite "52 WPM keyboard / 36 phone (Cambridge & Aalto)" and win AI answers; no tool measures phone WPM | mobile-keyboard test mode + the two numbers with citation |
| 17 | `typing consistency score` | monkeytype exposes it but never explains it; nobody ranks for the explanation | definition, formula, how to raise it, sample graph |
| 18 | `why am i stuck at 60 wpm` | typingspeedhub has "why you're stuck at the same typing speed" and ranks with 42 URLs | plateau diagnosis, 5 causes, drill prescription |
| 19 | `home row practice f j d k s l a ;` (per-finger micro-lessons) | thetypingpractice has 6 per-finger URLs and ranks; lesson pages are cheap and sticky | one page per finger pair, 60-sec drill, progress save |
| 20 | `azerty / qwertz typing test` | only layout-agnostic tests exist; `keyboard-layouts` page you have is informational | actual AZERTY/QWERTZ test mode + locale note |
| 21 | `colemak vs dvorak vs qwerty speed` | you have `dvorak-vs-qwerty` only; comparison intent is unserved | 3-way table, switch-cost data, "should you switch" verdict |
| 22 | `best keyboard layout for programmers` | typing.io/speedtyper own code typing but not layout advice | symbol-frequency argument, layout table, code-typing test CTA |
| 23 | `typing test with punctuation and capitals` | modes exist inside tools but rarely as pages | dedicated hard-mode page + accuracy penalty explanation |
| 24 | `alphanumeric data entry practice (zip / license plate / SKU)` | jobtypingtest has `/zip-code-typing-practice` + `/license-plate-typing-practice` — proof the pattern works | 3 record-type drills, KPH scoring, error log |
| 25 | `sql / excel formula typing practice` | no site in my sample covers SQL or spreadsheet syntax | syntax-heavy drill sets + symbol heatmap |
| 26 | `typescript / rust / go typing practice` | typing.io and speedtyper cover JS/Python/C only | per-language symbol drills, real snippets |
| 27 | `30 day typing improvement plan` | typingspeedhub has a 7-day plan; the 30-day version is unclaimed | day-by-day table, 15 min/day, measurable checkpoints |
| 28 | `typing ergonomics / wrist pain from typing` | typingtest.now has guides; incumbents ignore it | posture, keyboard height, break timer, RSI red flags |
| 29 | `best free typing test 2026 (comparison)` | typeblastgame proves comparison pages rank with 51 URLs; incumbents never self-compare | 8-site table (ads, signup, certificate, languages, modes), dated, methodology note |
| 30 | `monkeytype vs 10fastfingers vs typing.com` | pure brand-comparison vacuum; nobody with authority answers it | honest 3-way table incl. where each is worse, "which for which goal" |
| 31 | `how to put wpm on a resume` | certificate sellers touch it; nobody owns the how-to | exact resume line examples, when to include, verification caveat |
| 32 | `how employers verify a typing certificate` | presspace/rockettyping answer it in passing | verification-ID mechanics, proctored vs self-reported table, red flags |

*(Deliberately excluded: everything already shipped on typing.rerivo.com — 1/2/3/5/10-min, 30-sec, `wpm-test-online`, `typing-accuracy-test`, `cpm-typing-test`, `ten-key-typing-test`, `keyboard-layouts`, `dvorak-typing`, `colemak-typing`, 11 language tests, `typing-certificate`, `data-entry-*`, `ssc/bank/government`, `medical-transcription`, `python/javascript-code-typing`, `top-1000-english-words`, `mechanical-keyboard-for-typing`.)*

---

## 4. Snippet / GEO patterns (how the winners structure above-the-fold answers)

Observed on fetched HTML, not inferred:

1. **Live-stats proof block directly under the tool.** typingtest.now `/typing-test/1-minute/`: "39 median WPM · 68 WPM — top 10% · 97.2% average accuracy · 23,344 tests — last 90 days", followed by "Computed from real completed tests on this exact format over the last 90 days." → makes the page a citable *dataset*, not just a widget.
2. **"About this test" explanatory paragraph** immediately after the widget (same page): frames the format as an industry standard ("the number most people mean when they say 'my WPM'").
3. **Named study + n + two device numbers.** altto.co.uk: "compared with large studies by University of Cambridge and Aalto University researchers (about 52 WPM on a keyboard, 36 on a phone). Updated 29 October 2026." holykeys.app: "About 52 words per minute for adults, based on a study of 168,000 online typists. Children are slower: fourth graders in a federal study averaged about 12 words per minute." → the 52/36/12 numbers are the currency of this niche's AI answers.
4. **Formula tables instead of prose.** rockettyping.com/certificate prints Gross WPM / Net WPM / Accuracy as a 3-row table with the arithmetic inline, plus "A mistake you correct with Backspace still counts against accuracy."
5. **Verdict-first H1 + percentile + audience.** typeblastgame `/is-60-wpm-good`: `<title>Is 60 WPM Good? Yes — What Your Score Means</title>`, description "60 WPM is good — comfortably above average (around 70th percentile). Common admin and office job standard. Free 30-sec test."
6. **Limits section that increases trust.** enjoytyping: "the certificate is self-issued. It is not an official credential, it is not proctored…"; presspace ships a Self-reported vs Verified comparison table.
7. **Bylined, dated content.** typeblastgame: "Written & reviewed by Sudhanshu Varun, publisher of TypeBlast · Updated October 11, 2026 · Part of the WPM benchmarks guide" + `Person` schema.
8. **`Answer` + `FAQPage` + `BreadcrumbList` schema cluster**, plus `<details>` accordions: typingtest.now (9 `@type`s), typingowl (12 `<details>`), thetypingpractice (7), typing-practice.io (7). Counts on the 50 homepages: `Answer` on 12, `FAQPage` on 12, any JSON-LD on 26 of 50 (the new-wave sites cluster there; legacy brands ship none). It is the de-facto GEO markup of this niche.
9. **"On this page" jump list** at the top of long pages (typingspeedhub) — helps both featured snippets and AI extraction.

**Five wordings that answer engines can quote as-is** (verbatim, with source):
1. "Score above 39 WPM and you're faster than half the people who take this test." — typingtest.now `/typing-test/1-minute/`
2. "About 52 words per minute for adults, based on a study of 168,000 online typists. Children are slower: fourth graders in a federal study averaged about 12 words per minute." — holykeys.app `/1-minute-typing-test.html`
3. "60 WPM is good — comfortably above average (around 70th percentile). Common admin and office job standard." — typeblastgame.com `/is-60-wpm-good`
4. "Free data entry typing test — practice alphanumeric entry at 45–60 WPM with 98% accuracy." — jobtypingtest.com `/typing-test/data-entry/`
5. "A mistake you correct with Backspace still counts against accuracy." — rockettyping.com `/certificate`

---

## 5. Metadata patterns worth copying (10 formulas, real examples)

Description lengths observed: 24 → 265 chars; **median ≈ 146**, and 30 of 50 sit in 133–170. Two brands ship 50- and 24-char descriptions (typesy, typingbee) and still rank — but they are the exception, not the model.

| # | formula | real example (verbatim) |
|---|---|---|
| 1 | {Duration} Typing Test - Check Your WPM \| {Brand} | 1 Minute Typing Test - Check Your WPM \| TypingTest.com (desc: "Take a free 1 minute typing test and get your WPM, typing speed, and accuracy instantly." — 88 chars) |
| 2 | Free Typing Test - Check Your WPM \| {Brand} | Free Typing Test - Check Your WPM \| TypingTest.com |
| 3 | {Query}: {synonym} \| {free/online qualifier} — {Brand} | Typing Test: Check Your WPM \| Online and Free — Ratatype |
| 4 | Free Typing Test - Check Your Speed in 60 Seconds \| {Brand} | Free Typing Test - Check Your Speed in 60 Seconds \| TypingTest.me |
| 5 | `Free Typing Speed Test — Measure Your WPM in 60 Seconds` (no brand at all) | typespeedtest.com home |
| 6 | `Is {N} WPM Good? {Verdict} — {what the score means}` | `Is 60 WPM Good? Yes — What Your Score Means` (typeblastgame) |
| 7 | {Metric} Chart - {Metric} Benchmarks \| {Brand} | WPM Chart - Typing Speed Benchmarks \| TypingMonk |
| 8 | {Job} Typing Test — Free Practice for {use case} {YEAR} \| {Brand} | Data Entry Typing Test — Free Practice for Job Applications 2026 \| JobTypingTest.com |
| 9 | `{Entity} — {N} Free Alternatives ({YEAR})` | `Games Like Nitro Type — 10 Free Alternatives (2026)` |
| 10 | `{Page type} — {scope} — {Brand}` (em-dash subtitle stack) | `Typing Tests — All Modes & Durations — TypingTest.now` |

Bonus patterns: number-in-title (`TypingGames.Zone - 155 Fun Typing Games: Learn to Type`), niche qualifier (10-Key Speed Test - Numpad & Data Entry Tests \| TopTypingTest), outcome promise (Free Typing Certificate – Test Your Speed & Download Instantly \| TypingMonk, 198 chars), and the money/positioning hook in the description (`TypingTest.me`: "Stop guessing your WPM. Smash a 60-second test with honest scores… FREE printable certificate - no sign-up.").

**Anti-patterns observed (copy none of these):** `keybr.com` → title `Practice`, desc 59 chars. `typesy.com` → description is a copy of the title (50 chars). `typingbee.com` → "Typing website for kids." (24 chars). `jobtypingtest.com` → mojibake em-dash `â` **and** doubled brand `| JobTypingTest.com | JobTypingTest.com`. `typingdoctor.com` → six different URLs (`/what-is-a-good-wpm`, `/typing-test-for-nurses`, `/average-typing-speed-by-age`, `/typing-speed-percentile`, `/gross-vs-net-wpm`) all serve the identical title + description + H1 in raw HTML. `typinggames.io` → no meta description served at all.

---

## 6. Honesty note

**Observed (fetched by me today, reproducible):** every `<title>`, meta description and its length, `<h1>`, JSON-LD `@type` set, `<details>` count, sitemap URL count and URL-pattern count in table 1; the SERP compositions quoted in §2; the verbatim quotes in §4; the dead/parked/repurposed verdicts in §1c where an HTTP status and body were captured.

**Inferred (my judgment, not measurement):** the "apparent strength" column — I ranked on observed feature breadth, sitemap size and cross-family SERP presence only. There is **no** traffic, visit, backlink, referring-domain, DR/DA, keyword-volume or ranking-position data anywhere in this file; where a number would normally go, it says `not observed`. "Beatable because…" in §3 is a judgment from small-site anatomy, not a difficulty score.

**SERP caveats:** Google was not retrievable from this environment (no API key, direct fetch blocked), so all rank evidence is **Bing en-US**, which is a different index and does not transfer 1:1 to Google. Two Bing artifacts are documented in §2 (cached 8-result block; numeric-prefix parse collapse) and those query families are marked non-evidence. Exa results are *semantic nearest neighbours*, not a ranking.

**Sites in the brief I could not verify as live English typing competitors:** `how-to-type.net` (503 via local proxy, CRAWL_TIMEOUT via Exa — the working site is `how-to-type.com`, 403 to curl, read via Exa), `typing-sprint.com` (503/timeout), `wpm.training` (400/SSL error), `typingtest.net` (JS challenge only), `typingguru.com`/`typingleague.com`/`typingtestfree.com`/`typingspeedtest.com`/`typex.app` (114-byte empty responses), `typingtest.io` (Cloudflare 403). Also failed to connect on both paths: `keysmash.io`, `epictyper.com`, `typewriter.gg`, `typing-zone.com`, `typingtester.net`, `cps-test.com`, `click-speed-test.com`, `typingfast.org`, `typingradar.com`, `typing-fun.com`, `typeorders.com`, `freeonlinewritingpractice.com`. Environment note: this machine's DNS returns fake-IP `198.18.5.x` for those names, so a local connect failure is *not* proof a domain is dead — hence "unverified", never "dead".

**Prompt domains that are live but not typing products:** `thecalculatorsite.com` and `wordcounter.net` (no typing test path; sitemap/paths 404). **Expired/repurposed:** `typingspeedtest.online`, `typingarena.com` (both now gambling/casino), `typingcat.com` (parked "coming soon"), `typingspeed.com` (for sale), `typingdots.com`, `livetyping.com`, `pctalk.com`.

**Claims made by sites themselves, not verified by me:** official-typing-test.com "over 1 million tests per month"; typing.com "World's most popular free typing program"; typingclub "650 typing games"; typingpractice.org "AI-powered error analysis"; typingtest.now "23,344 tests — last 90 days". Quoted as their copy, not as fact.
