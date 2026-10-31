#!/usr/bin/env python3
"""R52：补厚第三批薄页（WPM 在线测试 / 数字 / 键盘练习 / 面试 / 不看键盘 / 自定义）。

这些页承接的都是**高意图**查询（wpm test online、number typing test、
keyboard practice、typing test for interview），却只有 1,200-1,500 字符。
补的是「这一页独有的机制」：WPM 的定义与三种算法、数字键区的独立技能、
键盘布局熟悉度、面试测试的形态、盲打的三个阶段、自定义文本的四种真实用法。

用法：python3 src/batches/r52_deepen3.py [--check]
"""
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

PATCH = {
    "wpm-test-online.html": {
        "seo": [
            {"h2": "What WPM is, and the three ways it is counted", "p": [
                "<strong>WPM</strong> is words per minute, where one word is five characters including spaces. That convention exists so a score on a long-word passage and a short-word passage can be compared. Three variants then diverge:",
                "<table><tr><th>Method</th><th>Formula</th><th>Reads</th></tr>"
                "<tr><td>Gross (raw)</td><td>all characters ÷ 5 ÷ minutes</td><td>Highest - counts mistakes</td></tr>"
                "<tr><td>Net</td><td>(characters − errors) ÷ 5 ÷ minutes</td><td>What employers test</td></tr>"
                "<tr><td>Adjusted (AWPM)</td><td>all characters ÷ 5 ÷ minutes, errors counted</td><td>School and exam scoring</td></tr></table>",
                "This page reports net WPM and raw WPM separately, so you can see which one a posting is quoting. A 60 WPM gross score at 94% accuracy nets about 56.",
            ]},
            {"h2": "Why an online WPM test is a snapshot, not a verdict", "p": [
                "One round measures one attempt under one set of conditions: your keyboard, your alertness, the passage you got. The number moves 5-10 WPM between a 15-second burst and a five-minute round, and by a similar margin between morning and end of day.",
                "The honest way to use it is as a trend. Run the same length, at the same time of day, three times a week, and watch the average move. A single high score is a good day, not a new level.",
            ]},
            {"h2": "What to compare your score against", "p": [
                "Use five-minute net scores on sentences, and compare against the measured distribution: mean 51.56 WPM, top 10% above about 78, bottom 10% below about 26 (CHI 2018, 168,960 volunteers). Employer floors cluster at 40 WPM for clerical work and 50-60 for legal and medical support.",
                "Do not compare a one-minute score against a published five-minute average - the difference is systematic, not personal.",
            ]},
            {"h2": "Getting a number you can quote", "p": [
                "Run a five-minute test, read net WPM and accuracy, and keep a screenshot with the date. That is the number to put on a form, a CV or an application - and the one an employer's test will roughly reproduce.",
                "If a posting quotes keystrokes per hour instead, convert: WPM × 300 = KPH, so 45 WPM is 13,500 KPH. The <a href=\"wpm-to-kph-converter.html\">converter</a> does it in both directions.",
            ]},
        ],
        "faq": [
            {"q": "What is a good WPM score?", "a": "Around 50 WPM net is the measured average. 40 WPM clears most clerical floors, 60 is fast, and 78+ is the top 10%."},
            {"q": "Is an online WPM test accurate?", "a": "It is accurate for the conditions you took it in. One round is a snapshot; three rounds of the same length at the same time of day give a number worth quoting."},
            {"q": "What is the difference between gross and net WPM?", "a": "Gross counts every character typed; net subtracts errors first. Employers test net, and it always reads equal to or lower than gross."},
            {"q": "Why is my score lower on longer tests?", "a": "The first thirty seconds are warm-up pace you cannot hold. Longer rounds also expose attention errors that a short burst hides."},
            {"q": "How many keystrokes per hour is my WPM?", "a": "Multiply by 300. 40 WPM is 12,000 KPH, 50 WPM is 15,000 KPH, and 10,000 KPH is about 33 WPM."},
        ],
    },
    "number-typing-test.html": {
        "seo": [
            {"h2": "The digit row is a separate skill", "p": [
                "Letters sit under your fingers. Digits sit on the row above, reached by an extended finger with no tactile landmark to confirm the position. That is why someone who types prose at 60 WPM often drops to 30-35 WPM on numbers, and why data-entry employers test digits separately.",
                "There are two ways to enter numbers and they are not interchangeable. The number row is right when digits are mixed into text (an address, a reference code). The numeric keypad is right when the work is amounts, quantities or codes entered field by field.",
            ]},
            {"h2": "What employers actually measure", "p": [
                "<table><tr><th>Unit</th><th>Formula</th><th>Typical requirement</th></tr>"
                "<tr><td>Keystrokes per hour (KPH)</td><td>characters per minute × 60</td><td>8,000-12,000 for data entry</td></tr>"
                "<tr><td>Key depressions per hour (KDPH)</td><td>all keys, corrections included</td><td>8,000 for SSC DEO</td></tr>"
                "<tr><td>Fields per hour</td><td>completed records</td><td>role-specific</td></tr>"
                "<tr><td>Accuracy</td><td>correct fields ÷ total</td><td>97-99%</td></tr></table>",
                "A correction costs you twice: once as a keystroke against the hour, and once as a field that has to be re-checked. That is why digit accuracy is worth more than digit speed.",
            ]},
            {"h2": "How to practise without a spreadsheet", "p": [
                "Two minutes of Numbers mode, twice a day, graded on errors rather than speed. Then add the parts that break in real work: decimals, negative signs, and the Tab key between fields.",
                "If you are learning the keypad, use the 4-5-6 home row (index on 4, middle on 5, ring on 6, thumb on 0) and press Enter after each figure, because that is how accounting software behaves.",
            ]},
            {"h2": "Where numeric speed pays", "p": [
                "Data entry, accounting, insurance claims, medical billing, warehouse admin and dispatch all live on digits. Each has its own page on this site with the specific thresholds - see <a href=\"10000-keystrokes-per-hour-test.html\">10,000 KPH</a> for the data-entry benchmark and <a href=\"ten-key-typing-test.html\">10-key typing</a> for the keypad version.",
            ]},
        ],
        "faq": [
            {"q": "Why is my number typing speed so much lower?", "a": "Digits sit on the row above the home row and have no tactile landmark, so every digit needs a reach and a visual check. A 40-50% drop from prose speed is normal."},
            {"q": "Should I use the number row or the keypad?", "a": "The keypad for amounts and long numeric strings, the number row when digits are mixed into text. Learning ten-key properly takes about a week and pays for itself in data-entry work."},
            {"q": "What is a good numeric typing speed?", "a": "8,000-12,000 keystrokes per hour is the band employers quote for data entry. That is roughly 27-40 WPM equivalent, with accuracy at 97% or better."},
            {"q": "Do corrections count in a numeric test?", "a": "In key-depression scoring, yes - every backspace is another keystroke against the hour. That is why typing it right the first time matters more than typing fast."},
            {"q": "How much practice does it take?", "a": "Two minutes twice a day for two to three weeks is enough to see a clear gain, mostly from the digit row ceasing to need a visual check."},
        ],
    },
    "keyboard-practice.html": {
        "seo": [
            {"h2": "Practice that targets the keyboard, not the text", "p": [
                "Most typing practice gives you text and hopes the keyboard sorts itself out. This page inverts it: the on-screen keyboard highlights the next key and the finger that owns it, so the drill is about where the keys are rather than what the sentence says.",
                "That is the right order for a beginner. Learn the map first, then the words. A typist who knows the map can type any text; a typist who has memorised sentences cannot type an unfamiliar word.",
            ]},
            {"h2": "What to look at, and what not to", "p": [
                "Look at the on-screen keyboard for the first few rounds, then at the text, then - eventually - neither. The progression matters: watching the on-screen guide builds the map, watching your hands builds a dependency.",
                "One rule that does most of the work: cover your hands for one round per session. It is uncomfortable for three days and then it stops being an issue, and it is the difference between a ceiling at 40 WPM and no ceiling.",
            ]},
            {"h2": "Layouts and the keys that move", "p": [
                "<ul><li><strong>QWERTY</strong> - the default on most machines; the layout this page uses.</li>"
                "<li><strong>QWERTZ</strong> - German-speaking countries; Y and Z swap, umlauts get their own keys.</li>"
                "<li><strong>AZERTY</strong> - France and Belgium; A/Q and Z/W swap, M moves next to L.</li>"
                "<li><strong>Dvorak and Colemak</strong> - alternative English layouts that reduce finger travel; see <a href=\"dvorak-vs-qwerty.html\">Dvorak vs QWERTY</a> before switching.</li></ul>",
                "If you work across layouts, practise each one separately. Alternating within a session creates interference that slows both.",
            ]},
            {"h2": "A ten-minute keyboard session", "p": [
                "Two minutes on the home row with the guide visible, two minutes on the row you miss most, three minutes on normal text, and three minutes covered. Log one number at the end - the accuracy figure, not the speed.",
                "That is the whole session. It is short enough to repeat daily, which is the only variable that reliably matters.",
            ]},
        ],
        "faq": [
            {"q": "How do I practise typing on a keyboard?", "a": "Ten minutes a day: home row with the on-screen guide, then your weakest row, then normal text, then one covered round. Log accuracy rather than speed."},
            {"q": "What is the home row?", "a": "The middle row of letters - A S D F on the left, J K L ; on the right - where your fingers rest between keystrokes. The bumps on F and J let you find it without looking."},
            {"q": "Should I look at the keyboard while practising?", "a": "At first at the on-screen guide, not your hands. Cover your hands for one round per session so the mental map forms rather than a visual dependency."},
            {"q": "Is this keyboard practice free?", "a": "Yes, with no account. Results stay in your browser."},
            {"q": "Does the layout matter?", "a": "For learning, yes - practise the layout you actually use. QWERTY, QWERTZ, AZERTY and alternative layouts move different keys, and mixing them in one session creates interference."},
        ],
    },
    "typing-test-for-interview.html": {
        "seo": [
            {"h2": "What an interview typing test usually looks like", "p": [
                "Three formats cover most cases: a short online test sent before the interview (one to three minutes, often automated), a timed exercise on the employer's machine during the visit, and a work sample where typing is incidental to a task such as entering records or drafting a reply.",
                "The first two measure speed and accuracy under a clock. The third measures whether the output is usable, which is why candidates who type fast but sloppily fail work samples even with a good score.",
            ]},
            {"h2": "How to prepare in a week", "p": [
                "<table><tr><th>Day</th><th>Drill</th><th>Goal</th></tr>"
                "<tr><td>1-2</td><td>Three five-minute rounds, same conditions</td><td>A baseline you can reproduce</td></tr>"
                "<tr><td>3-4</td><td>Two rounds on an unfamiliar keyboard</td><td>Remove the hardware surprise</td></tr>"
                "<tr><td>5</td><td>One timed round with punctuation and capitals</td><td>Accuracy under realistic text</td></tr>"
                "<tr><td>6</td><td>One work-sample rehearsal: enter ten records cleanly</td><td>Field accuracy, not speed</td></tr>"
                "<tr><td>7</td><td>Rest; one short warm-up only</td><td>Fresh hands on the day</td></tr></table>",
            ]},
            {"h2": "On the day", "p": [
                "Ask which scoring method and length the test uses before you start. Then type at 90% of your best pace for the first thirty seconds - almost everyone loses more in corrections than they gain in the opening sprint.",
                "If the test allows a practice sentence, take it. That is where you discover whether the keyboard has a different layout or a stiff spacebar, and it costs ten seconds.",
            ]},
            {"h2": "What to say about your speed", "p": [
                "Quote net WPM, the test length and accuracy: \"58 WPM net, 98%, five-minute test\". If the interviewer's test then reads 52, the number is consistent; if you had quoted a 15-second burst of 70, it looks like a discrepancy.",
                "For the preparation plans behind those numbers, see the <a href=\"40-wpm-typing-test.html\">40 WPM</a> and <a href=\"60-wpm-typing-test.html\">60 WPM</a> pages, and the <a href=\"typing-test-for-jobs.html\">jobs page</a> for role thresholds.",
            ]},
        ],
        "faq": [
            {"q": "What typing speed is expected in an interview test?", "a": "It depends on the role: 40 WPM for clerical and reception, 45-55 for data entry and dispatch, 60+ for legal and medical support. The posting usually states the floor."},
            {"q": "Is the interview typing test scored on gross or net WPM?", "a": "Net, in almost every case - errors are deducted. Ask before you start if the format is not stated."},
            {"q": "Can I use my own laptop?", "a": "Rarely. Most tests run on employer equipment, which is why rehearsing on an unfamiliar keyboard matters more than one more practice round."},
            {"q": "What if I make a mistake during the test?", "a": "Correct it if the correction is quick, otherwise keep going. A single error costs less than thirty seconds of backspacing."},
            {"q": "How should I quote my speed on an application?", "a": "Net WPM, accuracy and test length - \"58 WPM net, 98%, five-minute test\". It is reproducible, and a live test that reads slightly lower is normal."},
        ],
    },
    "how-to-type-without-looking.html": {
        "seo": [
            {"h2": "The three stages of not looking", "p": [
                "<ol><li><strong>You look because you do not know where the key is.</strong> Fix: the on-screen keyboard and home-row drills, with the guide visible.</li>"
                "<li><strong>You know the key but look anyway to confirm.</strong> Fix: covered rounds. This is the stage that lasts longest, and the only cure is typing with the hands hidden.</li>"
                "<li><strong>You look when you make a mistake.</strong> Fix: finish the word before checking. Most \"looks\" happen after errors, not before them.</li></ol>",
                "Most people are stuck in stage two and believe they are in stage one. The test is simple: type a sentence with your hands under a cloth. If accuracy collapses, you are in stage two and the fix is covered practice, not more key drills.",
            ]},
            {"h2": "Why looking is so expensive", "p": [
                "Each glance costs an eye movement, a re-focus and a re-orientation - roughly a quarter of a second, plus the risk of losing your place in the text. At one glance per word, that is 15-25 seconds of lost typing per minute.",
                "It also prevents the mental map from forming. The map is built by reaching for a key and being right, which is exactly what looking replaces with a visual shortcut.",
            ]},
            {"h2": "A two-week plan", "p": [
                "Days 1-3: one covered round a day, 30 seconds long, no target. Just get through it. Days 4-7: two covered rounds, 60 seconds. Days 8-11: covered rounds on the words you miss most, then a normal round to compare. Days 12-14: one covered round per session, permanently.",
                "Expect accuracy to fall by 10-20% during the covered rounds. It recovers within a week and the resulting speed is higher than where you started, because the glance was the ceiling.",
            ]},
            {"h2": "What to do when you get stuck", "p": [
                "If a particular key keeps failing, practise that key in isolation for thirty seconds, then return to text. If the whole round collapses, shorten it - a 15-second covered round you finish beats a 60-second one you abandon.",
                "And keep one normal round per session. The goal is to type without looking, not to type under a cloth forever.",
            ]},
        ],
        "faq": [
            {"q": "How long does it take to stop looking at the keyboard?", "a": "Two to four weeks of covered rounds, at 30-60 seconds a day. Accuracy dips 10-20% for the first week before recovering above where you started."},
            {"q": "Why do I look at the keyboard even when I know the key?", "a": "That is the confirmation habit, and it is the longest stage. Key drills do not fix it; only typing with the hands hidden does."},
            {"q": "Should I cover my hands completely?", "a": "Yes for the covered rounds - a cloth or a sheet of paper. Partial covering lets you cheat by peeking, which keeps the habit alive."},
            {"q": "Will covering my hands make me slower permanently?", "a": "No. Accuracy drops for about a week, then speed rises above your previous ceiling because the glance was the limiting factor."},
            {"q": "I keep losing my place in the text. What helps?", "a": "Shorten the round and read one word ahead rather than one line ahead. Losing place is usually a reading-ahead problem, not a typing problem."},
        ],
    },
    "custom-typing-test.html": {
        "seo": [
            {"h2": "Four ways people actually use a custom test", "p": [
                "<ul><li><strong>Interview rehearsal</strong> - paste a passage in the style of the employer's test (legal clause, medical note, code snippet) and practise at the same length.</li>"
                "<li><strong>Weak-key drilling</strong> - paste the words you keep missing, twenty times each, and run a minute on them.</li>"
                "<li><strong>Domain vocabulary</strong> - drug names, part numbers, legal defined terms. Typing your own vocabulary beats typing random sentences.</li>"
                "<li><strong>Classroom use</strong> - paste a passage from the week's reading so practice reinforces content rather than competing with it.</li></ul>",
                "The custom text is stored in your browser for the session; nothing is uploaded, which is what makes the classroom use case workable.",
            ]},
            {"h2": "What to paste, and what not to", "p": [
                "Paste plain text. Formatting, smart quotes and non-breaking spaces can all produce characters your keyboard cannot type, which turns a practice round into a hunt for a Unicode symbol.",
                "Keep it between 100 and 400 words. Shorter and the round repeats, which makes memorisation inflate your score; longer and you will never finish a five-minute round.",
            ]},
            {"h2": "Settings that matter", "p": [
                "<table><tr><th>Setting</th><th>Use it when</th></tr>"
                "<tr><td>Duration</td><td>Match the real test length; use 60 seconds for warm-ups only</td></tr>"
                "<tr><td>Text mode</td><td>Sentences for prose, Numbers for codes and amounts</td></tr>"
                "<tr><td>Layout</td><td>QWERTY by default; change it if you actually type on Dvorak or Colemak</td></tr>"
                "<tr><td>Theme and width</td><td>Comfort only - they do not change the score</td></tr></table>",
            ]},
            {"h2": "Limits worth knowing", "p": [
                "A custom test cannot tell you whether the passage is representative. If you paste easy words, you will score higher than on an employer's test and believe you are ready.",
                "Use it for targeted practice, and the standard tests for benchmarking. For the benchmark itself, see the <a href=\"1-minute-typing-test.html\">one-minute test</a> or the <a href=\"5-minute-typing-test.html\">five-minute test</a>.",
            ]},
        ],
        "faq": [
            {"q": "What is a custom typing test?", "a": "A test where you supply the text - your own vocabulary, a sample passage or an interview-style document - and the engine measures speed and accuracy on it."},
            {"q": "How much text should I paste?", "a": "100-400 words. Under 100 the round repeats and memorisation inflates the score; over 400 you will not finish a five-minute round."},
            {"q": "Is my pasted text uploaded?", "a": "No. It stays in the browser for the session; there is no server-side storage and no account."},
            {"q": "Can I practise code in a custom test?", "a": "Yes, though the dedicated code pages (Python, JavaScript, TypeScript, Rust, SQL) have symbol-dense pools written for that purpose."},
            {"q": "Why does my custom score differ from the standard tests?", "a": "Because the text differs. A custom passage with easy words or no punctuation will read higher than a standard sentence test - use the standard tests for benchmarks."},
        ],
    },
}


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    pages = {p["file"]: p for p in cfg["pages"]}
    errs = []
    for f, patch in PATCH.items():
        if f not in pages:
            errs.append(f"{f}: 不存在")
            continue
        body = sum(len(x) for s in patch["seo"] for x in s["p"])
        if body < 1600:
            errs.append(f"{f}: 新正文 {body} < 1600")
        if len(patch["faq"]) < 5:
            errs.append(f"{f}: FAQ 不足 5")
    if errs:
        for e in errs:
            print("  ·", e)
        print("❌ 未写入")
        return 1
    if "--check" in sys.argv:
        print("✅ 校验通过")
        return 0
    for f, patch in PATCH.items():
        pages[f].update(patch)
    CFG.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"已补厚 {len(PATCH)} 页")
    return 0


if __name__ == "__main__":
    sys.exit(main())
