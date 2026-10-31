#!/usr/bin/env python3
"""R47：补厚 4 个语种落地页（阿拉伯语 / 英语 / 印地语 / 中文）。

这 4 页在 GSC 里已有曝光（阿拉伯语 100 次），但正文只有 1,000-1,300 字符。
语种页的价值不在「多写」，而在写清「这门语言的输入机制与别处不同」：
RTL 连写、天城体元音符、输入法选字、以及考试口径。写不出差异的语种页就是薄页。

用法：python3 src/batches/r47_langs_deepen.py [--check]
"""
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

PATCH = {
    "arabic-typing-test.html": {
        "seo": [
            {"h2": "What makes Arabic different to type", "p": [
                "Arabic is written right to left and the letters join, so what you see on screen is not one glyph per keystroke: most letters have isolated, initial, medial and final forms, and the renderer picks the form as you type. Your speed is still one keystroke per letter - the joining is the font's job, not yours.",
                "Four features decide accuracy: the <strong>hamza</strong> forms (أ إ آ ؤ ئ), <strong>ta marbuta</strong> (ة) versus ha (ه), the <strong>alif maqsura</strong> (ى) versus ya (ي), and the Arabic comma ، and semicolon ؛ which sit where a Latin keyboard puts different characters. None of these are optional if the text is right-to-left formal writing.",
            ]},
            {"h2": "Keyboard layout and the RTL cursor", "p": [
                "The standard Arabic layout keeps the Latin letters on the same physical keys and adds Arabic legends, so touch typists can switch between languages without moving their hands - the muscle memory transfers, only the output changes. That is good news for anyone who already types English.",
                "The part that catches people is direction. In a right-to-left field the cursor moves left as you type, and mixing Arabic with Latin words or numbers reverses the visual order of the run. If your accuracy collapses when a sentence contains a number or an English product name, that is bidi handling, not typing speed.",
            ]},
            {"h2": "How Arabic speed is measured", "p": [
                "Most Arabic typing tests report words per minute using the same five-characters-per-word convention as English, so the two numbers are broadly comparable - with one caveat: Arabic words are shorter on average than English words, so a text of equal character count contains more words. Compare CPM rather than WPM when you are comparing across languages.",
                "<table><tr><th>CPM</th><th>WPM (÷5)</th><th>Reading</th></tr><tr><td>150</td><td>30</td><td>Beginner, hunt-and-peck</td></tr><tr><td>200</td><td>40</td><td>Comfortable office speed</td></tr><tr><td>250</td><td>50</td><td>Fast for Arabic formal text</td></tr><tr><td>300+</td><td>60+</td><td>Professional, transcription level</td></tr></table>",
            ]},
            {"h2": "Practising for real Arabic text", "p": [
                "Start with sentences without tashkeel (diacritics), because everyday writing omits them and typing them slows you down for no gain. Add them only if your work requires vocalised text - religious, educational or children's material.",
                "Then practise the pairs that cause errors: ة versus ه at word ends, ى versus ي, and the hamza carriers. Ten repetitions of one word beat one pass through ten words, because the goal is a corrected reflex rather than exposure.",
                "For the English side of the same skill, see the <a href=\"english-typing-test.html\">English typing test</a>; for the general benchmark, <a href=\"average-typing-speed.html\">average typing speed</a>.",
            ]},
            {"h2": "Where Arabic typing speed is tested", "p": [
                "Government and clerical posts in the Gulf and Egypt commonly ask for a certificate or a timed sample, often 20-30 words per minute for data entry and higher for secretarial work. Because the requirement is set per employer, read the posting rather than assuming a national standard exists.",
                "If a test is proctored, expect an unfamiliar keyboard with Arabic legends. Practise at least twice on a different machine: key travel and legend placement change your error rate more than practice volume does.",
            ]},
        ],
        "faq": [
            {"q": "Does Arabic typing count characters or letters?", "a": "Letters - one keystroke per letter. The joined forms you see on screen are produced by the font, not by extra keystrokes."},
            {"q": "Why does my accuracy drop when a sentence contains numbers?", "a": "Mixing right-to-left Arabic with left-to-right digits reverses the visual order of that run. It is a bidirectional text issue rather than a typing-speed problem; check your output rather than your speed."},
            {"q": "Should I practise with tashkeel (diacritics)?", "a": "Only if your work needs vocalised text. Everyday Arabic writing omits them, and typing them slows you down without improving the result."},
            {"q": "What is a good Arabic typing speed?", "a": "200-250 characters per minute (40-50 words per minute) is comfortable office speed. Government and clerical tests commonly ask 20-30 words per minute for data entry."},
            {"q": "Do I need a special Arabic keyboard?", "a": "No. The Arabic layout keeps Latin letters on the same keys, so you can add it in your operating system and switch with a shortcut. Touch typing transfers directly."},
        ],
    },
    "english-typing-test.html": {
        "seo": [
            {"h2": "Why \"English typing test\" is its own query", "p": [
                "For most of the world, an English typing test is simply a typing test. But in South Asia - and especially in India - \"English typing test\" is a specific exam format: 35 words per minute in English (or 30 in Hindi) for clerical posts, taken on a standard keyboard for ten minutes, with a small error allowance.",
                "That is why this page treats English as one option among several rather than as the default. If you are preparing for an exam, the exam's rules matter more than the language label.",
            ]},
            {"h2": "The exam shape most people actually need", "p": [
                "<table><tr><th>Requirement</th><th>Speed</th><th>Length</th><th>Notes</th></tr>"
                "<tr><td>SSC CHSL LDC / JSA (English)</td><td>35 WPM</td><td>10 minutes</td><td>Qualifying, error allowance applies</td></tr>"
                "<tr><td>SSC CHSL (Hindi)</td><td>30 WPM</td><td>10 minutes</td><td>Same test, lower threshold</td></tr>"
                "<tr><td>SSC DEO</td><td>8,000 key depressions/hour</td><td>15 minutes</td><td>Corrections count as depressions</td></tr>"
                "<tr><td>US federal clerical</td><td>40 WPM</td><td>5 minutes</td><td>No more than three errors</td></tr>"
                "<tr><td>General office</td><td>40-55 WPM</td><td>3-5 minutes</td><td>Net WPM, 95% accuracy</td></tr></table>",
                "Notice that the same English text produces three different measurements: words per minute, key depressions per hour, and a five-minute sample with a hard error cap. Convert before comparing - 8,000 KPDH is about 27 WPM.",
            ]},
            {"h2": "What English asks of your hands", "p": [
                "English on QWERTY is the best-supported layout in the world, which is why most speed records are set on it. The characters that decide accuracy are not the letters but the punctuation: the apostrophe, the comma, the full stop and the capital that follows it.",
                "A useful drill is sentence case with quotes. Most candidates lose 3-5 WPM there, and it is the exact content of an exam passage. Practise it weekly rather than daily - it is a check, not a workout.",
            ]},
            {"h2": "Practising in the exam's conditions", "p": [
                "Use the same length as the exam (ten minutes for SSC, five for federal), type a passage with full punctuation, and score net WPM plus errors. Then repeat on a different keyboard at least once: exam centres do not provide your laptop.",
                "If your error count is the problem rather than your speed, stop chasing WPM for two weeks and run accuracy rounds at 85% of your pace. A clean 37 WPM passes; a 45 WPM run with 12% errors does not.",
            ]},
        ],
        "faq": [
            {"q": "What is the typing speed required for English typing tests in exams?", "a": "35 words per minute for SSC CHSL LDC and JSA posts, over ten minutes, with a small error allowance. US federal clerical roles ask 40 WPM over five minutes with at most three errors."},
            {"q": "Is English typing speed measured in WPM or KPH?", "a": "Both, depending on the post. SSC DEO uses 8,000 key depressions per hour; clerical and federal roles use words per minute. 8,000 KPDH is about 27 WPM."},
            {"q": "How many mistakes are allowed?", "a": "A small allowance, commonly around 5% of the words typed, and it is stated in the notice for that exam cycle. The federal standard is stricter: three errors in five minutes."},
            {"q": "Does punctuation count in an English typing test?", "a": "Yes. Capitals and punctuation are part of the passage and an omitted character is an error. Practise sentence case with quotes, which is where most candidates lose their margin."},
            {"q": "Can I use my own keyboard in the exam?", "a": "No. Centre equipment is used. Rehearse on a different keyboard at least twice so key travel and layout are not a surprise."},
        ],
    },
    "hindi-typing-test.html": {
        "seo": [
            {"h2": "Devanagari is not a one-key-per-letter script", "p": [
                "Hindi is written in Devanagari, where consonants carry an inherent 'a' vowel and other vowels appear as <strong>matras</strong> - marks placed before, after, above or below the consonant. A single written syllable can require two or three keystrokes, so your characters-per-minute is not the same as your syllable rate.",
                "Add conjuncts (क्ष, त्र, ज्ञ) and the nasal marks (ं ँ) and you have a script where accuracy depends on sequence, not just key location. That is why Hindi typing tests feel different from English ones even at the same WPM.",
            ]},
            {"h2": "Krutidev, Remington and Mangal", "p": [
                "Indian typing exams usually specify a layout, and the three you will meet are Krutidev, Remington (often called the typewriter layout) and Mangal/InScript. They map Devanagari to the keyboard in completely different ways: Krutidev and Remington are legacy layouts built for typewriters and phototypesetting, while InScript follows the script's logical order.",
                "<table><tr><th>Layout</th><th>Where you meet it</th><th>Learning cost for a QWERTY typist</th></tr>"
                "<tr><td>Krutidev</td><td>Many state government exams, court work</td><td>High - keys do not match the script order</td></tr>"
                "<tr><td>Remington</td><td>Older exams, some typing institutes</td><td>High - typewriter-era mapping</td></tr>"
                "<tr><td>InScript / Mangal</td><td>Modern government and Unicode work</td><td>Moderate - follows the script logically</td></tr></table>",
                "Check the notice before you practise. Learning the wrong layout is worse than not practising, because the reflexes conflict.",
            ]},
            {"h2": "The exam requirements", "p": [
                "Hindi typing tests commonly ask 25-30 words per minute, with 30 WPM the figure used where English requires 35. Some posts quote key depressions per hour instead, and the mistake allowance is usually around 5%.",
                "Because the same passage can be scored as WPM or as key depressions, convert before comparing yourself to a friend's score: 30 WPM is 9,000 key depressions per hour under the five-character convention.",
            ]},
            {"h2": "Practising that transfers", "p": [
                "Practise on the layout your exam uses, on a keyboard you do not own, with a passage that includes the danda (।) and the numerals. Then time yourself for the full ten minutes rather than in one-minute bursts: conjunct errors cluster late, when attention thins.",
                "If you are starting from English touch typing, expect two to four weeks before the Devanagari reflexes stop interfering with your Latin ones. Do not alternate layouts within a session; the interference is real and it slows both.",
            ]},
        ],
        "faq": [
            {"q": "What typing speed is required for Hindi typing tests?", "a": "Commonly 25-30 words per minute, with 30 WPM where an English requirement would be 35. Some posts quote key depressions per hour instead, usually with a 5% error allowance."},
            {"q": "Which layout should I learn for Hindi typing?", "a": "Whichever your exam notice specifies - Krutidev, Remington or InScript/Mangal. They map Devanagari completely differently, and learning the wrong one creates conflicting reflexes."},
            {"q": "Why is Hindi typing slower than English at the same skill level?", "a": "Matras and conjuncts mean one written syllable can take two or three keystrokes, so characters per minute and syllables per minute diverge. Accuracy also depends on sequence rather than single key location."},
            {"q": "Does the danda count as an error if I omit it?", "a": "Yes. It is part of the passage, like a full stop in English, and an omitted character counts as an error on every mainstream test."},
            {"q": "Can I practise Hindi typing on a normal keyboard?", "a": "Yes, once the layout is installed in your operating system. The physical keyboard stays the same; only the mapping changes."},
        ],
    },
    "chinese-typing-test.html": {
        "seo": [
            {"h2": "Chinese typing is input-method work", "p": [
                "You do not type Chinese characters directly on a standard keyboard. You type a romanised or structural code - pinyin being the common case - and then choose a candidate from a list. Speed therefore depends on two skills: the keystrokes of the code, and how quickly you pick the right candidate.",
                "That is why a Chinese WPM figure is not comparable to an English one at face value. A pinyin typist producing 40 characters per minute is typing maybe 120-160 keystrokes, and the character count is what gets reported.",
            ]},
            {"h2": "The three things that decide your speed", "p": [
                "<ul><li><strong>Candidate selection.</strong> Common words appear first; rare characters require scanning or extra keystrokes. Practising your own vocabulary beats practising random text.</li>"
                "<li><strong>Phrase versus character input.</strong> Typing whole phrases (词) rather than single characters roughly halves the candidate selections, which is where most of the gain is.</li>"
                "<li><strong>Homophones.</strong> Pinyin maps many characters to one syllable, so accuracy depends on choosing correctly rather than on hitting the right key. An input-method error is a wrong character, not a typo.</li></ul>",
            ]},
            {"h2": "Other input methods, and when they are faster", "p": [
                "Structural methods - Wubi (五笔), Cangjie (倉頡), Zhengma - encode the shape of a character rather than its sound. They have a much steeper learning curve but avoid candidate selection almost entirely, which is why professional Chinese typists often use them.",
                "For most people pinyin is the right choice: it is already installed, it matches how you think, and the ceiling is high enough for office work. Switch only if you type Chinese for hours a day and the candidate list is demonstrably your bottleneck.",
            ]},
            {"h2": "How to practise and how it is scored", "p": [
                "Use the Sentences mode and type the characters as they appear, committing each phrase with the space or number key your IME uses. The score panel reports characters per minute; multiply by 60 for characters per hour, and remember that the five-characters-per-word convention was designed for alphabetic scripts.",
                "For a job that quotes words per minute, ask whether they mean characters or words. A 60 WPM requirement in a Chinese-language role usually means 60 characters per minute, which is a different target from 60 English words per minute.",
            ]},
        ],
        "faq": [
            {"q": "How is Chinese typing speed measured?", "a": "Usually in characters per minute, because each character carries a syllable. Multiply by 60 for characters per hour. The five-characters-per-word convention was designed for alphabetic scripts."},
            {"q": "Is pinyin or Wubi faster?", "a": "Wubi and other structural methods have a higher ceiling because they avoid candidate selection, but they take far longer to learn. For office work, pinyin's ceiling is usually enough."},
            {"q": "Why does my accuracy drop on rare characters?", "a": "Rare characters sit deep in the candidate list, so you scan or type extra keystrokes to reach them. Input-method errors produce a wrong character rather than a typo, which is why they are harder to notice."},
            {"q": "What is a good Chinese typing speed?", "a": "40-60 characters per minute is comfortable for office work with pinyin; experienced typists reach 80-120. Professional structural-method typists exceed that, but they are a different population."},
            {"q": "Does the test include punctuation?", "a": "Yes - the Chinese comma and full stop (， 。) are part of the passage, and in full-width form they are separate keystrokes from their Latin counterparts."},
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
        if body < 1700:
            errs.append(f"{f}: 新正文 {body} < 1700")
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
    print(f"已补厚 {len(PATCH)} 个语种页")
    return 0


if __name__ == "__main__":
    sys.exit(main())
