#!/usr/bin/env python3
"""R51：补厚第二批薄页（游戏/简单/标点/大写/入门/限时）。

同一逻辑：这 6 页正文 ~1,100-1,400 字符，低于站点中位数（2,300），
且它们承接的查询是有量的（punctuation / capital letter / beginner / timed）。
补的是**页面独有**的内容（每种模式到底在练什么、错误从哪里来、怎么判定过关），
不是把同一段话换几个词。

用法：python3 src/batches/r51_deepen2.py [--check]
"""
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

PATCH = {
    "typing-test-game.html": {
        "seo": [
            {"h2": "A typing test game, without the gimmicks", "p": [
                "This page runs the same typing engine as every other test here, with a shorter default round and a score you can beat. There is no account, no leaderboard and no reward loop - the game is the number, and the number is honest.",
                "That matters more than it sounds. Most typing games reward raw speed, so players learn to type fast and sloppily, then plateau at 40 WPM with 90% accuracy. A game that shows accuracy next to speed teaches the habit that actually raises the score.",
            ]},
            {"h2": "How to play it as a game", "p": [
                "<ul><li><strong>Beat your own high score</strong>, not someone else's. The result panel keeps your history in this browser, so the only fair comparison is your last five rounds.</li>"
                "<li><strong>Play three-round sets.</strong> One warm-up, one scored, one accuracy-only. The third is what stops the first two from teaching bad habits.</li>"
                "<li><strong>Change one variable per set</strong> - 15 seconds to 60, sentences to quotes, easy to hard. Changing two at once makes the result unreadable.</li></ul>",
            ]},
            {"h2": "Why short rounds feel better than they measure", "p": [
                "A 15-second round is fun because it is a sprint: no fatigue, no drift, and the score comes fast. It is also 5-10 WPM higher than the same typist's five-minute score, so a game built only on sprints teaches you to overestimate yourself.",
                "The fix is simple: use the short round for the fun, and check in with a five-minute round once a week. If the two numbers drift apart by more than 10 WPM, the sprint is flattering you.",
            ]},
            {"h2": "Three challenges worth trying", "p": [
                "<ol><li><strong>No-backspace run:</strong> a mistake is not corrected, you just keep going. Most players gain 4-6 WPM immediately and discover how much time they were spending on corrections.</li>"
                "<li><strong>Same text, three lengths:</strong> run the same text at 15 seconds, 60 seconds and 3 minutes. The spread tells you whether your problem is speed or stamina.</li>"
                "<li><strong>Accuracy ladder:</strong> three rounds aiming for 100%, 98%, then 95%. You will find that the 95% round is the fastest of the three, which is the whole lesson.</li></ol>",
            ]},
        ],
        "faq": [
            {"q": "Is this typing game free?", "a": "Yes, and there is no account. Scores are stored in your own browser, which is why there is no public leaderboard to chase."},
            {"q": "How do I beat my high score?", "a": "Play in three-round sets: warm-up, scored, accuracy-only. Shortening the round or switching to easier text raises the score without improving your typing, so change one variable at a time."},
            {"q": "Are my scores saved?", "a": "In this browser only, in localStorage. Nothing is sent to a server, and clearing site data removes the history."},
            {"q": "How do I level up fastest?", "a": "Accuracy first. Three rounds at 100%, 98% and 95% accuracy will show you that the 95% round is the fastest - speed follows control, not the other way round."},
            {"q": "Why is my 15-second score so much higher?", "a": "Sprints avoid fatigue and drift and typically read 5-10 WPM above a five-minute score. Use a five-minute round once a week as the honest number."},
        ],
    },
    "easy-typing-test.html": {
        "seo": [
            {"h2": "What makes this easy", "p": [
                "Three adjustments: common short words, no digits or unusual punctuation, and a one-minute default so the round ends before fatigue arrives. The point is to remove everything except the skill being built - finding keys without looking.",
                "Easy is not the same as slow. Type at the pace where you make almost no errors; if accuracy is below 95%, slow down further rather than pushing. At this stage speed is a side effect of accuracy, not a separate goal.",
            ]},
            {"h2": "A four-week starting plan", "p": [
                "<table><tr><th>Week</th><th>Daily drill</th><th>What should change</th></tr>"
                "<tr><td>1</td><td>Two 60-second easy rounds, hands covered for one</td><td>You stop looking at the keyboard for most words</td></tr>"
                "<tr><td>2</td><td>Same, plus one home-row-only round</td><td>Accuracy above 95% consistently</td></tr>"
                "<tr><td>3</td><td>Two-minute rounds, no backspace allowed</td><td>Corrections stop eating your time</td></tr>"
                "<tr><td>4</td><td>Three-minute rounds, then one five-minute check</td><td>A reproducible number you can quote</td></tr></table>",
            ]},
            {"h2": "The three habits that decide your ceiling", "p": [
                "<ul><li><strong>Looking at the keyboard.</strong> Every glance costs a beat and prevents the mental map from forming. Cover your hands once a day, even if it feels slow.</li>"
                "<li><strong>Backspacing through every slip.</strong> At beginner speeds, corrections cost more than the errors. Practise finishing rounds without correcting.</li>"
                "<li><strong>Two-finger typing.</strong> It works to about 35-40 WPM and then stops. If you are under 30 WPM, learning the home row now is cheaper than fixing it later.</li></ul>",
            ]},
            {"h2": "What to do after the easy test", "p": [
                "Once you hold 95% accuracy at 30 WPM on easy text, move to the <a href=\"beginner-typing-test.html\">beginner test</a> with normal sentences, then to the <a href=\"1-minute-typing-test.html\">one-minute test</a>. The easy page is a starting gate, not a home.",
                "If you are already above 40 WPM, this page will flatter you - switch to the <a href=\"hard-typing-test.html\">hard typing test</a>, which includes capitals, digits and long words.",
            ]},
        ],
        "faq": [
            {"q": "What makes this an easy typing test?", "a": "Common short words, no digits or unusual punctuation, and a one-minute default. It isolates key-finding from everything else."},
            {"q": "I am a slow typist - where do I start?", "a": "Two 60-second rounds a day, hands covered for one of them, and no backspacing. That combination removes the two habits that cap beginners at 30-40 WPM."},
            {"q": "Is it free?", "a": "Yes, with no account and no ads in the typing area. Results stay in your browser."},
            {"q": "What WPM should I expect first?", "a": "Most untrained adults start at 20-30 WPM with 90-95% accuracy. Below 20 WPM is usually two-finger typing rather than a lack of ability."},
            {"q": "When should I move to a harder test?", "a": "When you hold 95% accuracy at 30 WPM on easy text. Moving earlier just moves the errors to harder text."},
        ],
    },
    "punctuation-typing-test.html": {
        "seo": [
            {"h2": "Why punctuation is where accuracy breaks", "p": [
                "Letters sit under your fingers; punctuation does not. The comma, full stop, apostrophe and semicolon need extended reaches and often a Shift press, and none of them appear often enough in normal practice to become automatic.",
                "There is a second reason: punctuation carries meaning. A missing apostrophe changes a word, a wrong comma changes a clause, and a full stop in the wrong place ends a sentence early. Typists who treat it as decoration produce text that has to be re-read.",
            ]},
            {"h2": "The marks that cost the most time", "p": [
                "<table><tr><th>Mark</th><th>Where it is</th><th>Why it slows you down</th></tr>"
                "<tr><td>Apostrophe '</td><td>Right of the semicolon</td><td>Right little finger, already the weakest, with no Shift</td></tr>"
                "<tr><td>Comma ,</td><td>Right of M</td><td>Same finger as the apostrophe; frequent in real sentences</td></tr>"
                "<tr><td>Full stop .</td><td>Right of the comma</td><td>Followed by a capital, so it is a two-key rhythm</td></tr>"
                "<tr><td>Shifted symbols : ? ! \"</td><td>Top row with Shift</td><td>Two keys at once, opposite hands, and a return to the home row</td></tr></table>",
                "If your error report concentrates on the right-hand column of the keyboard, that is not a knowledge problem - it is a reach problem, and it responds to short daily drills.",
            ]},
            {"h2": "How to drill punctuation without boredom", "p": [
                "Use real sentences, not symbol lists. A list of punctuation marks trains the key but not the rhythm; sentences train the transition from word to mark and back, which is what actually fails under time pressure.",
                "Then run one round where you deliberately slow to 80% and check every mark. The next round, type normally and see whether the accuracy carried over. Two rounds is a session; ten minutes is enough.",
            ]},
            {"h2": "Where punctuation decides a test result", "p": [
                "Exam passages include capitals and punctuation, and an omitted character counts as an error on every mainstream test. Candidates who skip punctuation to gain speed usually lose more in the error allowance than they gain in WPM.",
                "For the exam-shaped version, see <a href=\"typing-test-for-jobs.html\">typing tests for jobs</a>; for the capitals half of the problem, the <a href=\"capital-letter-typing-test.html\">capital letter test</a>.",
            ]},
        ],
        "faq": [
            {"q": "What is a punctuation typing test?", "a": "A test using sentences with full punctuation and capitals, so the score reflects how you handle marks rather than only letters."},
            {"q": "Why do I make so many punctuation errors?", "a": "Punctuation needs extended reaches, often with Shift, and appears too rarely in normal typing to become automatic. Right-hand marks are the usual weak spot."},
            {"q": "Is the punctuation test free?", "a": "Yes, no account, and results stay in your browser."},
            {"q": "Which punctuation marks slow typists down most?", "a": "The apostrophe and comma, both under the right little finger, and shifted symbols such as : ? ! which need two keys at once."},
            {"q": "Do punctuation errors count on exams?", "a": "Yes. An omitted or wrong mark is an error, and most tests apply an error allowance that a punctuation-skipping strategy will exhaust."},
        ],
    },
    "capital-letter-typing-test.html": {
        "seo": [
            {"h2": "Capital letters are a two-hand problem", "p": [
                "A capital needs Shift pressed with the hand that is <em>not</em> typing the letter, then a quick return to the home row. Most people learn to use the same hand for both, which breaks the hand position and costs three keystrokes of rhythm for every capital.",
                "On a sentence with six capitals in twenty words, that is roughly a 5% speed penalty and a much larger accuracy penalty, because the hand has to find the home row again after each one.",
            ]},
            {"h2": "Shift or Caps Lock", "p": [
                "Shift for a single capital, Caps Lock for a run of them. Anything else mixes habits: Caps Lock for one letter means you press it twice and lose the rhythm either way, and forgetting to turn it off produces a burst of errors.",
                "If your operating system has a sticky-keys or Shift-lock behaviour, turn it off before practising. It masks the exact reach you are trying to build, and it will not be there on the keyboard an employer hands you.",
            ]},
            {"h2": "A drill that transfers", "p": [
                "Type proper nouns and sentence starts for one minute, then check which hand pressed Shift. If the same hand typed the letter, the error is structural, not speed-related - and it will keep appearing in every exam passage.",
                "Then run a two-minute round with normal sentence case and compare the accuracy to your all-lowercase score. A drop of more than 3% means capitals are the weak link.",
            ]},
            {"h2": "Where it matters most", "p": [
                "Names, places, product names, legal defined terms and the start of every sentence. In legal and medical documents a wrong capital can change the meaning; in exam passages it is a scored error.",
                "For the punctuation half of the same skill, see the <a href=\"punctuation-typing-test.html\">punctuation test</a>; for the exam context, <a href=\"typing-test-for-jobs.html\">typing tests for jobs</a>.",
            ]},
        ],
        "faq": [
            {"q": "What is a capital letter typing test?", "a": "A test using sentence case and proper nouns, so it measures how you handle Shift as well as letter location."},
            {"q": "Why are capital letters hard to type?", "a": "They need Shift with the opposite hand plus a return to the home row. Using the same hand for both breaks the hand position and costs rhythm on every capital."},
            {"q": "Is the capital letter test free?", "a": "Yes, no account needed, results stored in your browser."},
            {"q": "Do I use Shift or Caps Lock?", "a": "Shift for a single capital, Caps Lock for a run of them. Mixing the two creates habits that fail under time pressure."},
            {"q": "How much speed do capitals cost?", "a": "About 3-5% on ordinary sentences, and more on text dense with proper nouns. Accuracy usually drops more than speed."},
        ],
    },
    "beginner-typing-test.html": {
        "seo": [
            {"h2": "A first test that does not punish you", "p": [
                "The default round is short, the words are common, and the score is reported with accuracy beside it. A beginner's first number should be a baseline, not a verdict - most untrained adults start at 20-30 WPM with 90-95% accuracy, and that is normal.",
                "If your accuracy is below 85%, the speed number is not meaningful yet. Slow down until errors are rare; the speed will follow within two weeks and it will be a real number rather than a lucky one.",
            ]},
            {"h2": "What a beginner should actually practise", "p": [
                "<ul><li><strong>Home row first.</strong> asdf jkl; until the fingers return without looking.</li>"
                "<li><strong>No looking down.</strong> One covered round a day. This is the single largest gain available at this stage.</li>"
                "<li><strong>No backspace.</strong> Finish rounds with mistakes in them. Corrections cost more than errors at beginner speed.</li>"
                "<li><strong>Ten minutes daily.</strong> Short and frequent beats a long weekly session, because the skill is motor memory.</li></ul>",
            ]},
            {"h2": "Your first realistic targets", "p": [
                "<table><tr><th>Stage</th><th>WPM</th><th>Accuracy</th><th>What it unlocks</th></tr>"
                "<tr><td>First week</td><td>15-25</td><td>90%+</td><td>Finishing a round without panic</td></tr>"
                "<tr><td>First month</td><td>25-35</td><td>95%</td><td>Comfortable email and messaging</td></tr>"
                "<tr><td>Three months</td><td>35-45</td><td>96-97%</td><td>Entry-level office requirements</td></tr>"
                "<tr><td>Six months</td><td>45-60</td><td>97%+</td><td>Most clerical job floors</td></tr></table>",
                "These are typical progressions for someone practising ten minutes a day, not guarantees. The variable that matters is consistency, not talent.",
            ]},
            {"h2": "What to do after your first month", "p": [
                "Move to the <a href=\"1-minute-typing-test.html\">one-minute test</a> for the classic benchmark, and add the <a href=\"home-row-typing-test.html\">home row test</a> as a weekly check on technique. When you can hold 95% accuracy at 35 WPM, the <a href=\"40-wpm-typing-test.html\">40 WPM plan</a> is the next step.",
                "Avoid jumping to hard text or code typing before the map is automatic - it moves the errors rather than removing them.",
            ]},
        ],
        "faq": [
            {"q": "What is a good speed for a beginner?", "a": "20-30 WPM is normal for an untrained adult, with 90-95% accuracy. Reaching 35-45 WPM within three months of daily ten-minute practice is typical."},
            {"q": "Should beginners focus on speed or accuracy?", "a": "Accuracy. At beginner speed corrections cost more than errors, and a sloppy fast habit is much harder to undo than a slow careful one."},
            {"q": "How long does it take to learn to type?", "a": "Four to six weeks to type without looking, and two to four months to reach 60 WPM, assuming ten to fifteen minutes of daily practice."},
            {"q": "Is this beginner test free?", "a": "Yes, no account, no ads inside the typing area, and results stay in your browser."},
            {"q": "Should I learn the home row first?", "a": "Yes. It is the anchor every other reach returns to, and skipping it is what produces the two-finger ceiling at 35-40 WPM."},
        ],
    },
    "timed-typing-test.html": {
        "seo": [
            {"h2": "What changes when the clock is running", "p": [
                "A timed test adds two things a free practice session does not: a fixed end point, and a score you can compare with someone else's. That is why employers use them and why practice rounds so often do not transfer - the pressure is part of the task.",
                "The practical consequence is that you should practise under the same clock. A typist who only practises untimed will underperform by 5-10 WPM the first time a countdown appears.",
            ]},
            {"h2": "Choosing a duration that measures what you need", "p": [
                "<table><tr><th>Duration</th><th>What it measures</th><th>Typical use</th></tr>"
                "<tr><td>15-30 seconds</td><td>Burst speed</td><td>Warm-up, key drills</td></tr>"
                "<tr><td>1 minute</td><td>Short-form benchmark</td><td>Daily check, casual comparison</td></tr>"
                "<tr><td>3 minutes</td><td>Screening length</td><td>Interview and exam rehearsal</td></tr>"
                "<tr><td>5 minutes</td><td>Working pace</td><td>The number you quote; federal standard</td></tr>"
                "<tr><td>10 minutes</td><td>Endurance</td><td>Transcription, data entry, long documents</td></tr></table>",
            ]},
            {"h2": "How the clock changes your errors", "p": [
                "Short rounds produce errors of haste: a skipped letter, a wrong key under speed. Long rounds produce errors of attention: a dropped capital in minute six, a comma missed when the sentence changes direction.",
                "That is why the same typist can have 98% accuracy on a one-minute test and 94% on a ten-minute one. If your job involves sustained typing, the ten-minute number is the honest one.",
            ]},
            {"h2": "Beat your own clock, not someone else's", "p": [
                "Record the same length every week and compare against yourself. The only useful comparison across people is the same duration, the same text type and the same scoring method - change any of the three and the comparison is noise.",
                "For the standard benchmarks by duration, see the <a href=\"wpm-chart.html\">WPM chart</a>; for the length most employers use, the <a href=\"5-minute-typing-test.html\">five-minute test</a>.",
            ]},
        ],
        "faq": [
            {"q": "What is a timed typing test?", "a": "A test with a fixed countdown, so the score reflects speed under time pressure rather than open-ended practice."},
            {"q": "What is the most common test length?", "a": "One minute for casual benchmarking, three minutes for screening and five minutes for formal standards such as the US federal clerical test."},
            {"q": "Does the timer stop when I make a mistake?", "a": "No. The clock runs continuously, which is why corrections cost time and uncorrected errors cost accuracy - you choose which penalty to take."},
            {"q": "Can I choose my own time?", "a": "Yes, from 15 seconds to 10 minutes. Keep the same length when comparing scores across weeks."},
            {"q": "Why is my accuracy lower on longer tests?", "a": "Long rounds produce errors of attention rather than haste - a dropped capital in minute six, a missed comma when the sentence turns. That is the fatigue effect the longer test is designed to reveal."},
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
