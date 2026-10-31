#!/usr/bin/env python3
"""R25 内容重写：把两个高曝光页换成可引用、可对比的内容。

- typing-speed-requirements.html：按真实长尾（8000 key depressions / DEO / call center /
  30 wpm 含义）重写，三单位互转 + 公开标准举例 + 4 周补齐计划。
- average-typing-speed.html：换成 CHI 2018 的 51.56 WPM 主口径 + 分档表 + 百分位，
  解释为什么别处还写 40 WPM。
用法：python3 src/batches/r25_rewrite.py [--check]
"""
import difflib
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

REQ = {
    "title": "Typing Speed Requirements by Job: WPM, KPH and KDPH",
    "metaDesc": "What typing speed each job asks for, in WPM, keystrokes per hour and key depressions: office 40-55, data entry 8,000-12,000 KPH, legal 60-75.",
    "h1": "Typing Speed Requirements by Job",
    "heroP": ("Job ads quote speed in three different units - <strong>WPM, keystrokes per hour and key depressions per hour</strong> - "
              "and they rarely say which one the test uses. This page converts between them and lists what each role actually screens for."),
    "tldr": ("Office and clerical roles ask 40-55 WPM. Data entry is quoted in keystrokes per hour, usually 8,000-12,000 KPH (27-40 WPM). "
             "Legal and medical transcription sits at 60-80 WPM. Accuracy floors are 95-98% almost everywhere, and net WPM is what counts."),
    "seo": [
        {"h2": "Requirements at a glance", "p": [
            "<table><tr><th>Role</th><th>Speed quoted</th><th>In WPM</th><th>Accuracy floor</th><th>Test length</th></tr>"
            "<tr><td>General office / admin</td><td>40-55 WPM</td><td>40-55</td><td>95%</td><td>3-5 min</td></tr>"
            "<tr><td>Receptionist / front desk</td><td>40-50 WPM</td><td>40-50</td><td>95-98%</td><td>1-5 min</td></tr>"
            "<tr><td>Data entry clerk</td><td>8,000-12,000 KPH</td><td>27-40</td><td>97-98%</td><td>3-5 min</td></tr>"
            "<tr><td>10-key / numeric entry</td><td>8,000-12,000 KPH</td><td>27-40</td><td>field-level</td><td>2-5 min</td></tr>"
            "<tr><td>911 dispatcher</td><td>35-45 WPM</td><td>35-45</td><td>95%</td><td>1-5 min</td></tr>"
            "<tr><td>Medical transcriptionist</td><td>65-80 WPM</td><td>65-80</td><td>98-99%</td><td>audio file</td></tr>"
            "<tr><td>Legal secretary</td><td>60-75 WPM</td><td>60-75</td><td>98%</td><td>3-5 min</td></tr>"
            "<tr><td>US federal clerk</td><td>40 WPM</td><td>40</td><td>3 errors max</td><td>5 min</td></tr>"
            "<tr><td>SSC CHSL LDC / JSA (India)</td><td>35 WPM English, 30 Hindi</td><td>35 / 30</td><td>~5% allowance</td><td>10 min</td></tr>"
            "<tr><td>Court reporter</td><td>225 WPM stenotype</td><td>not comparable</td><td>95%</td><td>dictation</td></tr></table>",
            "The bands overlap because employers set their own floor. Read the posting for the exact figure and the unit it is quoted in.",
        ]},
        {"h2": "What 8,000 key depressions per hour means", "p": [
            "A key depression is one keystroke, including the corrections you make. 8,000 KDPH is 8,000 ÷ 60 = 133 keystrokes per minute, "
            "about 26.7 WPM at five characters per word. 10,000 KPH is 33 WPM; 12,000 KPH is 40 WPM.",
            "The correction penalty is what trips people up. Someone who types 40 WPM but backspaces constantly can miss an 8,000 KPH bar, "
            "because every correction is another key depression against the same hour. Practise typing it right the first time.",
        ]},
        {"h2": "Government and civil service examples", "p": [
            "These are examples from public postings and published standards, not universal rules - always read the notice for the cycle you are applying in.",
            "<ul><li><strong>US federal clerical and office-automation roles</strong> are commonly published as 40 WPM on a five-minute sample with no more than three errors.</li>"
            "<li><strong>County and municipal clerical postings</strong> typically quote 40 net WPM, with 50 net WPM for senior reception or HR support roles.</li>"
            "<li><strong>Public-safety dispatch</strong> ranges from 30 to 45 correct WPM depending on the agency; several run a CritiCall-style battery on top of the typing test.</li>"
            "<li><strong>India SSC CHSL</strong> separates the posts: 35 WPM English or 30 WPM Hindi for LDC and JSA, and 8,000 key depressions per hour for DEO.</li></ul>",
        ]},
        {"h2": "Converting between the three units", "p": [
            "WPM to KPH: multiply by 300 (five characters per word, sixty minutes per hour). WPM to CPM: multiply by 5. KPH to WPM: divide by 300. "
            "KDPH to WPM: divide by 300 as well, but corrections count against you.",
            "So a 45 WPM score is 13,500 KPH, and an 8,000 KPH requirement is about 27 WPM. If a posting quotes a number you have never measured, "
            "convert it before deciding whether you qualify - the units exaggerate the gap in both directions.",
        ]},
        {"h2": "How to close the gap in four weeks", "p": [
            "Week one: measure honestly. Take a five-minute test in the mode the job uses - sentences for clerical work, numbers for data entry - "
            "and record net WPM plus accuracy. That number, not your best one-minute burst, is your starting point.",
            "Week two: accuracy first. Type at 85% of your best pace until accuracy holds above 98% for three consecutive rounds. "
            "Most people gain 4-6 net WPM this way without typing any faster, because they stop paying the correction tax.",
            "Week three: length. Move to rounds the same length as the real test. A five-minute test at 45 WPM is a different skill from a one-minute test at 55.",
            "Week four: simulate. Same time of day, unfamiliar keyboard, no pause. Then re-measure against the band for your target role.",
        ]},
        {"h2": "Sources and how to read them", "p": [
            "The bands above come from publicly advertised job requirements and published examination standards across clerical, medical, legal and "
            "public-safety postings. They are ranges, not guarantees: two employers in the same sector can differ by ten WPM.",
            "Where a figure has an official source - the federal 40 WPM standard, the SSC CHSL notice, the 225 WPM NCRA stenotype standard - this page "
            "names it. Where it is a market range, the page says so. If a recruiter quotes a number that contradicts your test, ask which unit and which "
            "scoring method before assuming you failed.",
        ]},
    ],
    "faq": [
        {"q": "What typing speed is required for most jobs?", "a": "40 to 55 WPM covers most office, clerical and administrative roles, usually with a 95% accuracy floor. Data entry is quoted differently: 8,000 to 12,000 keystrokes per hour, which is 27 to 40 WPM."},
        {"q": "How many WPM is 8,000 key depressions per hour?", "a": "About 26.7 WPM. 8,000 ÷ 60 = 133 keystrokes per minute, and 133 ÷ 5 = 26.7. Corrections count as key depressions, so backspacing lowers the real figure."},
        {"q": "Is 40 WPM enough for a government job?", "a": "For the US federal clerical standard, yes: it is commonly published as 40 WPM on a five-minute sample with no more than three errors. State and local postings vary, and India's SSC CHSL LDC asks 35 WPM English or 30 WPM Hindi."},
        {"q": "What does 30 WPM typing speed mean?", "a": "Thirty words per minute is 150 characters per minute, or 9,000 keystrokes per hour. It clears the floor for general clerical work and for dispatch in many agencies, but is below the 40-50 WPM band most office postings quote."},
        {"q": "Do employers count gross or net WPM?", "a": "Net WPM, almost always. Errors are subtracted before the score is reported, which is why a clean 42 beats a sloppy 55 in screening. Ask which method the test uses if the posting only says WPM."},
        {"q": "What speed does a stenographer need?", "a": "Court reporting certification is 225 WPM on a stenotype machine, not a keyboard, and entry-level programmes often graduate at 180 to 200 WPM. Keyboard speed is a separate skill used for transcript editing."},
    ],
}

AVG = {
    "title": "Average Typing Speed: What Is a Good WPM in 2026?",
    "metaDesc": "Average typing speed is 51.56 WPM in the largest published study, not the 40 WPM figure copied everywhere. What good, fast and top-10% mean, by age and job.",
    "tldr": ("The largest measured sample (136 million keystrokes, 168,960 people) puts mean typing speed at 51.56 WPM. The commonly quoted 40 WPM comes from "
             "older office-worker samples. Top 10% exceed about 78 WPM; bottom 10% are under 26."),
    "seo": [
        {"h2": "The number, and where it comes from", "p": [
            "The most-cited modern measurement is Dhakal, Feit, Kristensson and Oulasvirta, \"Observations on Typing from 136 Million Keystrokes\" (CHI 2018). "
            "It recorded 136,857,600 keystrokes from 168,960 volunteers and reports a mean of <strong>51.56 WPM</strong> with a standard deviation of 20.2, "
            "an uncorrected error rate of 1.17%, and 1.173 keystrokes per character. The paper is open at doi.org/10.1145/3173574.3174220.",
            "Most pages still quote 40 WPM. That figure comes from older, smaller samples of office workers and students, and it has been copied forward without "
            "being re-measured. Both describe real populations: 40 WPM is closer to \"typical office worker on a work task\", 51.56 WPM to \"person who chose to "
            "take an online typing test\".",
        ]},
        {"h2": "What counts as good, fast and exceptional", "p": [
            "<table><tr><th>Band</th><th>Net WPM</th><th>Percentile (approx.)</th><th>What it means</th></tr>"
            "<tr><td>Slow</td><td>under 26</td><td>bottom 10%</td><td>Hunting for keys; typing is the bottleneck</td></tr>"
            "<tr><td>Below average</td><td>26-40</td><td>10th-28th</td><td>Two-finger or untrained touch typing</td></tr>"
            "<tr><td>Average</td><td>40-52</td><td>28th-50th</td><td>Enough for most office work</td></tr>"
            "<tr><td>Good</td><td>52-65</td><td>50th-75th</td><td>Comfortable all-day typing</td></tr>"
            "<tr><td>Fast</td><td>65-78</td><td>75th-90th</td><td>Above most job requirements</td></tr>"
            "<tr><td>Top decile</td><td>78-100</td><td>90th-99th</td><td>Professional typists, developers, transcribers</td></tr>"
            "<tr><td>Exceptional</td><td>100+</td><td>top 1%</td><td>Competitive typing, world-record territory</td></tr></table>",
            "The percentile column is a normal approximation of that distribution, and it reproduces the study's own reported deciles to within about one point. "
            "The <a href=\"typing-speed-percentile.html\">percentile page</a> does the arithmetic for any score.",
        ]},
        {"h2": "Average typing speed by age", "p": [
            "Speed peaks in the late teens to thirties in most published samples and declines slowly after that, but the spread within an age band is far larger "
            "than the difference between bands. A 55-year-old who touch types beats a 20-year-old who does not, every time.",
            "The practical reading: age is a weak predictor compared with whether someone was ever taught to touch type. If they were not, the gap is trainable at "
            "any age - the <a href=\"average-typing-speed-by-age.html\">age breakdown</a> has the numbers by decade.",
        ]},
        {"h2": "Average typing speed by profession", "p": [
            "<ul><li><strong>Data entry:</strong> 45-65 WPM, often quoted as 13,500-19,500 KPH, with 97-98% accuracy.</li>"
            "<li><strong>Administrative and secretarial:</strong> 50-70 WPM depending on seniority.</li>"
            "<li><strong>Transcription:</strong> 65-80 WPM sustained over audio, which is harder than the same speed over visible text.</li>"
            "<li><strong>Software developers:</strong> no formal requirement; most sit above 70 WPM, and code typing differs because of brackets and symbols.</li>"
            "<li><strong>Writers and journalists:</strong> 60-80 WPM, where the limit is usually thinking rather than typing.</li></ul>",
            "Role-by-role figures, in the units employers actually use, are on the <a href=\"typing-speed-requirements.html\">typing speed requirements</a> page.",
        ]},
        {"h2": "Why your score differs from these numbers", "p": [
            "Test length: a 15-second burst reads 5-10 WPM higher than a five-minute run. Text type: random words score lower than sentences, code lower again, "
            "digits are a different skill. Scoring: gross WPM is higher than net. Keyboard: a laptop chiclet keyboard is slower than a mechanical one for most people.",
            "So before concluding you are below average, check what you measured. A five-minute net score on sentences is what this page's bands refer to; "
            "a one-minute gross score on random words is not comparable.",
        ]},
        {"h2": "Test yourself against the bands", "p": [
            "Run a five-minute sentence test, then read net WPM and accuracy from the results panel. Compare the net figure against the table above, and check "
            "whether accuracy is inside the 97-98% band most employers require - a fast score at 92% accuracy is not the same asset as a slightly slower clean one.",
        ]},
    ],
    "faq": [
        {"q": "What is the average typing speed?", "a": "51.56 WPM in the largest published measurement, from 136,857,600 keystrokes recorded from 168,960 volunteers (Dhakal et al., CHI 2018). The older 40 WPM figure reflects office-worker samples rather than self-selected test takers."},
        {"q": "Is 40 WPM good?", "a": "It is around the 28th percentile of the CHI 2018 distribution and clears the floor for most clerical and reception roles. It is below the 50-70 WPM band that legal, medical and transcription roles ask for."},
        {"q": "What is a fast typing speed?", "a": "Above 78 WPM puts you in the top 10% of the measured population. Above 100 WPM is roughly the top 1%, and competitive typists exceed 130 WPM in short bursts on known text."},
        {"q": "Does typing speed decline with age?", "a": "Slightly, and far less than the variation between people of the same age. Whether someone was taught touch typing predicts speed much better than age does."},
        {"q": "Why do I score lower on longer tests?", "a": "The first thirty seconds are warm-up pace you cannot hold. A five-minute net score is typically 5-10 WPM below a 15-second burst, and the longer number is the one that reflects a working day."},
        {"q": "How is typing speed measured?", "a": "Correct characters divided by five, then divided by the minutes elapsed. Five characters count as one word. Net WPM subtracts errors first; gross WPM does not."},
    ],
}

TARGETS = {"typing-speed-requirements.html": REQ, "average-typing-speed.html": AVG}


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    pages = {x["file"]: x for x in cfg["pages"]}
    errs = []
    for name, patch in TARGETS.items():
        pg = pages[name]
        merged = dict(pg, **patch)
        if len(merged["title"]) > 62:
            errs.append(f"{name}: title {len(merged['title'])} > 62")
        if len(merged["metaDesc"]) > 158:
            errs.append(f"{name}: desc {len(merged['metaDesc'])} > 158")
        for other in cfg["pages"]:
            if other["file"] == name:
                continue
            r = difflib.SequenceMatcher(None, merged["metaDesc"], other["metaDesc"]).ratio()
            if r > 0.70:
                errs.append(f"{name} vs {other['file']}: {r:.2f}")
    if errs:
        for e in errs:
            print("  ·", e)
        print("❌ 不合规，未写入")
        return 1
    if "--check" in sys.argv:
        print("✅ 校验通过")
        return 0
    for name, patch in TARGETS.items():
        pages[name].update(patch)
    CFG.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"已重写 {len(TARGETS)} 页")
    return 0


if __name__ == "__main__":
    sys.exit(main())
