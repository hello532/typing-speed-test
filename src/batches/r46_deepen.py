#!/usr/bin/env python3
"""R46：把 6 个薄页（≈1,000 字符 / 4 FAQ）补到可排名厚度。

为什么先补而不是再加页：站点 178 页里有 10 页正文 <1,350 字符，它们在 GSC 里
有曝光（教师页 17 名、advanced 16.7 名），但内容不足以支撑这个位置。补厚已有页
比再开新页更安全——不增加页面总量，直接把已有位置变成资产。

用法：python3 src/batches/r46_deepen.py [--check]
"""
import difflib
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

PATCH = {
    "typing-test-for-teachers.html": {
        "seo": [
            {"h2": "Why teachers end up typing more than they expected", "p": [
                "A teacher's day produces text constantly: lesson plans, differentiated worksheets, parent emails, marking comments, reports. None of it is billed as typing work, and all of it competes for the same hours as preparation and feedback.",
                "That is why the useful question is not \"do teachers need to type fast\" but \"which of these tasks can be made cheap\". Marking comments and parent emails are repetitive; lesson plans and feedback are not. Speed helps the first category, templates and text expansion help it more.",
            ]},
            {"h2": "What speed is actually expected", "p": [
                "No teaching qualification specifies a typing speed. The bands below come from the clerical and administrative side of education - school office, exams office, cover coordination - where postings do quote numbers.",
                "<table><tr><th>Role</th><th>Typical advertised band</th><th>What it is based on</th></tr>"
                "<tr><td>Classroom teacher (no formal requirement)</td><td>40+ WPM comfortable</td><td>Lesson planning, marking comments, emails</td></tr>"
                "<tr><td>School administrator / exams officer</td><td>45-55 WPM</td><td>Clerical postings, data entry of results</td></tr>"
                "<tr><td>Teaching assistant with admin duties</td><td>40-50 WPM</td><td>Records, reports, correspondence</td></tr>"
                "<tr><td>Online tutoring (written feedback)</td><td>50+ WPM</td><td>Written feedback volume per session</td></tr></table>",
                "If you are already at 45-50 WPM, typing is not your bottleneck and further speed work will not buy back time. The bigger wins are templates, text expansion and a marking comment bank.",
            ]},
            {"h2": "Running a class typing test without accounts", "p": [
                "Any tool that requires student accounts creates a data-protection question, which is why this site stores results only in the browser and never server-side. For classroom use that has two practical consequences: no pupil data leaves the device, and results are not visible to you remotely.",
                "The workaround is simple. Pupils take a one-minute test and report the number; you record it on paper or in your own sheet. It takes about three minutes of a lesson and gives you a baseline you can compare in six weeks.",
                "If you want a shared record, the on-screen result can be photographed on the device rather than uploaded anywhere.",
            ]},
            {"h2": "Grade bands, and why they should not become a test", "p": [
                "Published classroom benchmarks put grade 3 at roughly 10-20 WPM, grade 5 at 25-35 and grade 8 at 35-45, with wide variation by school and by how much keyboarding instruction pupils actually receive.",
                "The risk of quoting these bands to children is that speed becomes the goal. A pupil pushed to 35 WPM with two fingers has hit a ceiling that costs years later; a pupil at 22 WPM with the home row habit will pass them inside a year. Score accuracy first, and only mention speed once the fingers are right.",
            ]},
            {"h2": "Ten-minute routines that fit a school day", "p": [
                "<ul><li><strong>Starter (3 min):</strong> one timed round, accuracy reported before speed.</li>"
                "<li><strong>Drill (5 min):</strong> one row or one punctuation set, typed slowly enough to be correct.</li>"
                "<li><strong>Record (2 min):</strong> pupil writes the number down. Visible progress is the motivation; a leaderboard is not needed.</li></ul>",
                "Three sessions a week for a term is enough for most classes to move a full grade band, and it costs less curriculum time than a single extended project.",
            ]},
            {"h2": "The admin tasks worth automating first", "p": [
                "Before chasing speed, look at what you type most often. Parent emails about the same three issues, marking comments that repeat, report phrases that differ by one clause - those are template work, and a template removes the typing entirely rather than making it faster.",
                "Keep the speed work for the genuinely new text: feedback that has to be specific, and plans that have to fit this class. That is where a higher WPM actually converts into time.",
            ]},
        ],
        "faq": [
            {"q": "Do teachers need a typing qualification?", "a": "No. Teaching qualifications do not specify typing speed. School administrator and exams officer postings sometimes quote 45-55 WPM, but classroom roles do not."},
            {"q": "What typing speed is comfortable for a teacher?", "a": "Around 40-50 WPM covers lesson planning, marking comments and parent emails. Above that, the limit is usually thinking and templates rather than keyboard speed."},
            {"q": "Can pupils use this without creating accounts?", "a": "Yes. Nothing is stored server-side and results stay in the browser on the device, which is why there is no teacher dashboard and no pupil data to protect."},
            {"q": "What speed should a 10-year-old type?", "a": "Roughly 15-25 WPM at grade 4-5, with 90%+ accuracy, though bands vary widely by school. Accuracy and home-row habit matter more than the number at that age."},
            {"q": "How often should a class practise?", "a": "Ten minutes, three times a week. Short frequent sessions build the motor pattern; a single long session mostly builds fatigue."},
            {"q": "Should I use a leaderboard with pupils?", "a": "Usually no. Leaderboards reward speed over accuracy, which is the opposite of what beginners need. A private record of each pupil's own number works better."},
        ],
    },
    "advanced-typing-test.html": {
        "seo": [
            {"h2": "What \"advanced\" means here, numerically", "p": [
                "Advanced starts around 70 WPM net on a five-minute test, which is roughly the 82nd percentile of the largest published sample (mean 51.56, SD 20.2). At 80 WPM you are in the top decile; at 100 WPM, the top 1%.",
                "This page uses longer passages, mixed vocabulary and heavier punctuation so the score reflects sustained control rather than a lucky burst. A one-minute round on easy words will read 8-12 WPM higher than this test, and that difference is the point.",
            ]},
            {"h2": "The three things that separate 70 from 90", "p": [
                "<ul><li><strong>Look-ahead.</strong> At 70 WPM you read the word you are typing; at 90 you are two to four words ahead and the hands run on a buffer. This is the single biggest difference and the hardest to train.</li>"
                "<li><strong>Error economy.</strong> Advanced typists do not avoid errors, they avoid <em>costly</em> errors. They let a wrong letter go in a throwaway word and fix the ones that matter, instead of backspacing through both.</li>"
                "<li><strong>Consistency.</strong> A 90 WPM typist's ten rounds sit within a 5 WPM band; a 70 WPM typist's swing by 15. Narrowing the spread raises the average faster than sprinting raises the peak.</li></ul>",
            ]},
            {"h2": "Drills that move an advanced score", "p": [
                "Short maximum-speed bursts: ten rounds of 15 seconds, three times a week. Long rounds teach endurance you already have; bursts train the top end you cannot currently reach.",
                "Hard-text rounds: quotes with punctuation, pangrams, numbers. Speed on plain sentences does not transfer to a document with full stops and capitals, and most real work is the second kind.",
                "One ten-minute round per week, scored on the lowest of three attempts. That number is what an employer would see on a tired afternoon.",
            ]},
            {"h2": "Benchmarking honestly", "p": [
                "Quote net WPM, the test length and the accuracy together: \"78 WPM net, 98.5%, ten minutes\". A bare number invites the assumption that it came from a fifteen-second sprint on easy words.",
                "Compare like with like. Published averages are five-minute net scores on sentences; a one-minute gross score on random words is not comparable, and neither is a code-typing score, which runs 10-20 WPM lower for the same typist.",
            ]},
            {"h2": "When advanced speed stops paying", "p": [
                "Above about 80 WPM, no clerical job asks for more. The returns are personal - competitive typing, live captioning, heavy code work - rather than employability. If your goal is a job, the next 20 WPM are worth less than a certificate and a clean CV line.",
                "If your goal is the score itself, accept the timeline: 70 to 80 is months, 80 to 100 is usually years, and the last ten points are mostly consistency rather than technique.",
            ]},
        ],
        "faq": [
            {"q": "What is an advanced typing speed?", "a": "Around 70 WPM net and above, which is roughly the 82nd percentile. 80 WPM is the top decile and 100 WPM is about the top 1% of measured typists."},
            {"q": "Why is my score lower on this page?", "a": "The passages are longer with heavier punctuation and mixed vocabulary. A one-minute test on easy words typically reads 8-12 WPM higher for the same typist."},
            {"q": "How do I get from 70 to 90 WPM?", "a": "Look-ahead reading, 15-second maximum-speed bursts, and hard-text rounds. Progress is measured by narrowing the spread across ten rounds, not by the best single round."},
            {"q": "Is 70 WPM fast enough for professional work?", "a": "Yes. No clerical role requires more than about 75-80 WPM. Above that, extra speed matters only for transcription, captioning, competitive typing or heavy coding."},
            {"q": "Should I quote gross or net WPM?", "a": "Net, with the test length and accuracy. Gross scores without a stated method read as the flattering version and invite a live re-test that reads lower."},
        ],
    },
    "how-fast-can-i-type.html": {
        "seo": [
            {"h2": "The answer, in one round", "p": [
                "Take the 60-second test on this page and read net WPM from the results panel. That number is your current speed on this text at this length - not a permanent trait, and not directly comparable to a five-minute score.",
                "If you need a number to quote to an employer or on a form, run a five-minute test instead. It reads 5-10 WPM lower and it is the figure that can be reproduced.",
            ]},
            {"h2": "How you compare", "p": [
                "<table><tr><th>Your WPM</th><th>Percentile (approx.)</th><th>Reading</th></tr>"
                "<tr><td>under 26</td><td>bottom 10%</td><td>Hunting for keys; typing is the bottleneck</td></tr>"
                "<tr><td>26-40</td><td>10th-28th</td><td>Two-finger or untrained touch typing</td></tr>"
                "<tr><td>40-52</td><td>28th-50%</td><td>Average adult; enough for most office work</td></tr>"
                "<tr><td>52-65</td><td>50th-75th</td><td>Comfortable all-day typing</td></tr>"
                "<tr><td>65-78</td><td>75th-90th</td><td>Above almost every job requirement</td></tr>"
                "<tr><td>78+</td><td>top 10%</td><td>Professional typists, transcribers, developers</td></tr></table>",
                "Percentiles come from the CHI 2018 sample of 168,960 volunteers (mean 51.56 WPM, SD 20.2), approximated as a normal distribution. The <a href=\"typing-speed-percentile.html\">percentile page</a> converts any score exactly.",
            ]},
            {"h2": "Four things that change your number", "p": [
                "<ul><li><strong>Length.</strong> A 15-second burst reads 5-10 WPM above a five-minute run.</li>"
                "<li><strong>Text.</strong> Random words score lower than sentences; code and digits lower again.</li>"
                "<li><strong>Scoring.</strong> Gross WPM counts every character; net subtracts errors.</li>"
                "<li><strong>Keyboard.</strong> A laptop chiclet board is slower than a mechanical one for most people, and a phone is about 15 WPM slower again.</li></ul>",
            ]},
            {"h2": "What to do with the number", "p": [
                "If you are under 40 WPM, the fastest gain is stopping the look-at-keyboard habit: one covered round a day for two weeks typically adds 5-8 WPM. If you are between 40 and 60, work on accuracy at speed - 30-second sprints at 90% of your maximum, checked every round. Above 60, the limiting factor becomes consistency and look-ahead reading rather than force.",
                "Then re-test at the same length and time of day. Comparing a 9am five-minute score with a midnight one-minute score tells you nothing except that you were tired.",
            ]},
        ],
        "faq": [
            {"q": "How fast can I type?", "a": "Take the 60-second test on this page and read net WPM. For a number to quote, use a five-minute test - it reads 5-10 WPM lower and is reproducible."},
            {"q": "What is the average typing speed?", "a": "51.56 WPM from the CHI 2018 study of 168,960 volunteers, with a standard deviation of 20.2. Older sources quoting 40 WPM describe office-worker samples instead."},
            {"q": "Why is my score different on different sites?", "a": "Test length, text type and scoring method all move the result by 5-10 WPM. A 15-second gross score and a five-minute net score are not the same measurement."},
            {"q": "Can I type faster with two fingers?", "a": "You can reach about 35-40 WPM, then it plateaus. Two-finger typing needs a visual target for every keystroke, which caps the speed regardless of practice."},
            {"q": "How quickly can I improve?", "a": "5-8 WPM in two weeks is typical at the start, mostly from removing bad habits. Gains slow above 60 WPM, where months of consistency work replace quick fixes."},
        ],
    },
    "hard-typing-test.html": {
        "seo": [
            {"h2": "What makes text hard", "p": [
                "Four things, in order of impact: <strong>mixed capitals</strong> (Shift with the opposite hand, every time), <strong>digits</strong> (extended reaches with no tactile landmark), <strong>punctuation</strong> (often a two-key combination), and <strong>long words</strong> (more consecutive keystrokes with no space to reset).",
                "A fifth factor is unfamiliar vocabulary. You cannot predict the next letters of a word you have never seen, so reading slows and the hands wait. That is why technical passages feel harder than their letter count suggests.",
            ]},
            {"h2": "What a hard test exposes", "p": [
                "On easy text, speed is mostly finger speed. On hard text it is mostly error economy: typists at the same WPM diverge by 10-15% because one group backspaces through every slip and the other lets a throwaway word go.",
                "It also exposes Shift discipline. Watch your accuracy fall on proper nouns and sentence starts: if it drops more than elsewhere, the opposite-hand rule is not yet automatic.",
            ]},
            {"h2": "How to score well without gaming it", "p": [
                "Slow to the pace where errors stay under 2%, and hold it for the full round. A clean 45 on hard text is a better signal than a sloppy 60, because the second number cannot be reproduced on a document that matters.",
                "Do not skip capitals or punctuation to type faster. On every mainstream test an omitted character counts as an error, and in real work - a legal filing, an invoice, an email - it is worse than slow.",
            ]},
            {"h2": "When to step up to hard mode", "p": [
                "Move up when you can hold 97% accuracy on sentences at your target speed. If you are below that, hard text will only teach you to make errors faster.",
                "Use hard mode as a weekly check rather than a daily drill: it is diagnostic, not a routine. The daily work stays on the specific weakness it reveals - digits, capitals, or punctuation. Run the same hard passage twice a month: the score that matters is the second one, because it is the only one you have practised for.",
            ]},
        ],
        "faq": [
            {"q": "What is a hard typing test?", "a": "A test using text with mixed capitals, digits, punctuation and long or unfamiliar words, so the score reflects accuracy and control rather than speed on easy sentences."},
            {"q": "What score is good on hard text?", "a": "45-55 WPM net with 97% accuracy is strong. Expect 10-20% below your easy-text score; the gap is the measure of how much your speed depends on predictable words."},
            {"q": "Why do capitals slow me down?", "a": "Each capital needs Shift pressed with the opposite hand plus a quick return to the home row. Untrained typists use one hand for both, which breaks the hand position."},
            {"q": "Should I practise hard text every day?", "a": "No. Use it weekly as a diagnostic, then spend the daily sessions on the specific weakness it exposes - digits, capitals or punctuation."},
            {"q": "Do errors count on capitals?", "a": "Yes. An omitted capital or full stop is an error on every mainstream typing test, and in real documents it is worse than being slow."},
        ],
    },
    "fast-typing-test.html": {
        "seo": [
            {"h2": "What counts as fast", "p": [
                "Fast is relative but the bands are stable: 60 WPM is the 66th percentile, 78 WPM starts the top 10%, and 100 WPM is roughly the top 1%. Anything above 60 clears every clerical job requirement; above 80, extra speed is a personal project rather than an employability gain.",
                "Be careful with the word \"fast\" on a test that runs 60 seconds. A one-minute score reads 5-10 WPM higher than a five-minute score for the same typist, so a \"fast\" one-minute number can sit at average on a real working test.",
            ]},
            {"h2": "Why some people are faster", "p": [
                "Three factors, in order: whether they were ever taught to touch type, how much they type daily, and how they handle errors. Finger strength and keyboard quality matter far less than most people assume.",
                "The error-handling difference is the one people miss. Fast typists let minor slips go in throwaway words and fix the ones that matter; slower typists backspace through both, which costs the time they just gained.",
            ]},
            {"h2": "Four drills that actually move the number", "p": [
                "<ul><li><strong>Covered rounds:</strong> one a day, hands hidden. Removes the look-down cycle that caps most people at 35-40.</li>"
                "<li><strong>15-second bursts:</strong> maximum speed, ten per session, twice a week. Trains the top end you cannot reach in a minute.</li>"
                "<li><strong>Bigram work:</strong> the twenty most common letter pairs (th, he, in, er, an, re). Practising transitions moves 50-65 faster than practising words.</li>"
                "<li><strong>Accuracy rounds:</strong> 90% of your pace with zero tolerance. The gains compound into the longer tests where numbers actually live.</li></ul>",
            ]},
            {"h2": "Testing under pressure without fooling yourself", "p": [
                "Run the test in the conditions you will be judged in: same length, same time of day, an unfamiliar keyboard if an interview is coming. Then quote the number you can reproduce, not your best.",
                "If a test shows a sudden 10 WPM jump, check whether the text was unusually easy or the length unusually short before believing it. Most \"breakthroughs\" are measurement changes.",
            ]},
        ],
        "faq": [
            {"q": "What is a fast typing speed?", "a": "60 WPM is above two thirds of measured typists, 78 WPM is the top 10%, and 100 WPM is about the top 1%. Above 80, no ordinary job asks for more."},
            {"q": "Why is my one-minute score higher than my five-minute score?", "a": "The first thirty seconds are warm-up pace you cannot hold. A one-minute test reads 5-10 WPM above a five-minute test for the same typist."},
            {"q": "Can I become a fast typist with two fingers?", "a": "No. Two-finger typing plateaus around 35-40 WPM because each keystroke needs a visual target. Past that, ten fingers and no looking are the requirement."},
            {"q": "How long does it take to get fast?", "a": "From 30 to 50 WPM usually takes one to three months of short daily practice; 50 to 70 takes longer; 70 to 90 is typically measured in months to years."},
            {"q": "Does a mechanical keyboard make you faster?", "a": "Slightly, for most people - shorter travel and clearer feedback. It is worth 3-8 WPM at best, well behind touch typing and error handling."},
        ],
    },
    "paragraph-typing-test.html": {
        "seo": [
            {"h2": "Paragraph versus word-list tests", "p": [
                "A word-list test (the monkeytype style) shows one word at a time and rewards raw reaction. A paragraph test shows continuous prose, so it also measures reading ahead, punctuation, capitals, and the ability to hold a rhythm across sentences.",
                "Employers test with paragraphs because that is what the job looks like: continuous text with full stops, names, commas and the occasional number. A word-list score is a training metric; a paragraph score is a work metric.",
            ]},
            {"h2": "Why paragraphs are harder", "p": [
                "Three reasons. Punctuation and capitals add keystrokes that a word list omits. Sentence structure means the next word is predictable, but only if you read ahead - which most typists do not. And length means fatigue enters: errors in the fourth minute are usually attention, not technique.",
                "The result is a score typically 5-15% lower than the same typist's word-list number, and 5-10 WPM lower than a one-minute burst on the same text.",
            ]},
            {"h2": "Choosing a length", "p": [
                "<table><tr><th>Length</th><th>What it measures</th><th>Use it when</th></tr>"
                "<tr><td>1 minute</td><td>Burst speed</td><td>Daily warm-up, quick comparison</td></tr>"
                "<tr><td>3 minutes</td><td>Common screening length</td><td>Interview practice, exam rehearsal</td></tr>"
                "<tr><td>5 minutes</td><td>Working pace</td><td>The number you quote; matches most job standards</td></tr>"
                "<tr><td>10 minutes</td><td>Endurance</td><td>Transcription, data entry, long document work</td></tr></table>",
            ]},
            {"h2": "How to use this page", "p": [
                "Start with one minute to warm up, then run a five-minute round and record net WPM plus accuracy. If accuracy is under 96%, stop chasing speed and run accuracy rounds for a week - it is the cheaper fix.",
                "For exam-style practice, use the same length as the exam and include punctuation. For a written job test, add one round of the <a href=\"quotes-typing-test.html\">quotes test</a>, which is the closest thing to real document text. A paragraph score is only useful if you can reproduce it on a second attempt, at a different time of day, on a keyboard you have not warmed up on.",
            ]},
        ],
        "faq": [
            {"q": "What is a paragraph typing test?", "a": "A test using continuous prose rather than a word list, so it measures reading ahead, punctuation and capitals alongside raw speed."},
            {"q": "Why is my paragraph speed lower than my word-list speed?", "a": "Punctuation and capitals add keystrokes, sentence structure requires reading ahead, and length introduces fatigue. A 5-15% lower score is normal."},
            {"q": "How long should the paragraph be?", "a": "Five minutes for a number you can quote, three minutes to match most screening tests, ten minutes for transcription and data-entry work."},
            {"q": "Do employers use paragraphs or word lists?", "a": "Paragraphs, because that is what the work looks like. Word-list scores are useful for training but they are not what screening tools measure."},
            {"q": "Is this the same as a passage typing test?", "a": "Yes. Paragraph, passage and prose tests all mean continuous text; the differences are length and difficulty, not format."},
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
        if body < 1800:
            errs.append(f"{f}: 新正文 {body} < 1800")
        if len(patch["faq"]) < 5:
            errs.append(f"{f}: FAQ {len(patch['faq'])} < 5")
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
