#!/usr/bin/env python3
"""R53：补厚剩余 4 个语种页（韩语 / 西班牙语 / 日语 / 乌尔都语）。

语种页唯一值得写的是「这门语言的输入机制与拉丁语系不同在哪」：
韩语的音节块组字、西语的变音与 ñ、日语的 IME 变换、乌尔都语的 Nastaliq 连写。
写不出这一层的语种页就是薄页，所以这四页只写机制 + 练习法 + 计分口径。

用法：python3 src/batches/r53_langs2.py [--check]
"""
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

PATCH = {
    "korean-typing-test.html": {
        "seo": [
            {"h2": "Hangul is assembled, not typed letter by letter", "p": [
                "Korean is written in syllable blocks, and each block is composed from 2-4 jamo (consonant and vowel letters). You type the jamo in sequence and the input method assembles them into a block as you go: ㄱ + ㅏ = 가, and adding a final consonant changes the block again.",
                "That has two consequences for typing speed. First, your keystroke count is per jamo, not per visible character, so characters per minute and keystrokes per minute diverge sharply. Second, a wrong jamo does not produce a wrong letter - it produces a different block, which is harder to spot when proofreading.",
            ]},
            {"h2": "Why the 2-beolsik layout matters", "p": [
                "Most Korean typists use the 2-beolsik (두벌식) layout, which maps consonants to the left hand and vowels to the right. That division is why Korean touch typing can be fast: the hands alternate rather than competing for the same keys.",
                "The 3-beolsik layouts assign final consonants to the right hand and have a higher theoretical ceiling, but they are rare and not worth learning unless you already type Korean professionally. If you are learning, use 2-beolsik because it is what every Korean keyboard ships with.",
            ]},
            {"h2": "What actually slows Korean typing", "p": [
                "<ul><li><strong>Batchim (final consonants)</strong> - the third or fourth jamo in a block, which moves the hand back to the consonant side.</li>"
                "<li><strong>Block boundaries</strong> - knowing when a syllable ends is a language skill, not a typing skill, and it is where learners hesitate.</li>"
                "<li><strong>Homophone selection</strong> - less severe than Chinese IMEs, but still present for Sino-Korean words.</li></ul>",
                "Practise on real sentences rather than jamo lists. The jamo are easy; the block assembly under time pressure is not.",
            ]},
            {"h2": "How the score is reported", "p": [
                "This page reports WPM and CPM from the committed text. For Korean, CPM is the more meaningful number because it counts visible characters, while the keystroke count behind it is roughly 2-3 times higher.",
                "For comparison across languages, use CPM: the five-characters-per-word convention was designed for alphabetic scripts and understates the work in a block-based one. The general benchmarks are on <a href=\"average-typing-speed.html\">average typing speed</a>.",
            ]},
        ],
        "faq": [
            {"q": "How does Korean typing work on a normal keyboard?", "a": "You type jamo (consonant and vowel letters) and the input method assembles them into syllable blocks. Two to four keystrokes produce one visible character."},
            {"q": "Which layout should I learn?", "a": "2-beolsik (두벌식). It ships with every Korean keyboard, splits consonants and vowels between hands, and has a high enough ceiling for professional work."},
            {"q": "Why is my Korean WPM lower than my English WPM?", "a": "Each visible character needs two to four keystrokes, so characters per minute and words per minute diverge. Compare CPM across languages rather than WPM."},
            {"q": "What is batchim and why does it slow me down?", "a": "Batchim is the final consonant in a syllable block. Typing it moves the hand back to the consonant side, which breaks the alternation that makes Korean typing fast."},
            {"q": "Is this Korean test free?", "a": "Yes, with no account. Results stay in your browser, and the practice pool is real Korean sentences rather than random jamo."},
        ],
    },
    "spanish-typing-test.html": {
        "seo": [
            {"h2": "What Spanish adds to a Latin keyboard", "p": [
                "Four characters do most of the damage: <strong>ñ</strong>, the accented vowels <strong>á é í ó ú</strong>, the inverted marks <strong>¿ ¡</strong>, and the dieresis <strong>ü</strong> in words like pingüino. On a Spanish layout they have dedicated keys; on an English layout they need dead keys or Alt codes, which is a different skill entirely.",
                "If you are preparing for an exam or a job in a Spanish-speaking country, practise on the layout you will actually face. Typing Spanish on an English keyboard trains a workaround, not the skill.",
            ]},
            {"h2": "Why the accents matter more than they look", "p": [
                "Accents change meaning, not just spelling: si (if) and sí (yes), el (the) and él (he), esta and está. Omitting one is a real error in the language, not a typo, which is why Spanish typing tests treat a missing accent as a mistake.",
                "The inverted question and exclamation marks are typed at the start of the sentence, so they require a look-ahead: you have to decide the sentence is a question before you begin it. That is why they show up in error reports.",
            ]},
            {"h2": "QWERTY, AZERTY and the Latin American layout", "p": [
                "<table><tr><th>Layout</th><th>Where</th><th>What changes</th></tr>"
                "<tr><td>Spanish QWERTY</td><td>Spain</td><td>Ñ next to L; accents on dedicated keys</td></tr>"
                "<tr><td>Latin American QWERTY</td><td>Most of Latin America</td><td>Similar to Spain's, with differences in symbol placement</td></tr>"
                "<tr><td>AZERTY</td><td>Not used for Spanish</td><td>Different letter order; avoid for Spanish practice</td></tr></table>",
                "The differences are small but they cost accuracy for the first week. Practise on the layout you will be tested on.",
            ]},
            {"h2": "Practising for real Spanish text", "p": [
                "Start with sentences that include at least one accent and one punctuation mark per line - that is what ordinary Spanish looks like. Then add a numbers round, because dates and amounts are where Spanish-language office work actually lives.",
                "For exam preparation, see the requirement bands on <a href=\"typing-speed-requirements.html\">typing speed requirements</a>; for the general benchmark, <a href=\"average-typing-speed.html\">average typing speed</a>.",
            ]},
        ],
        "faq": [
            {"q": "What is a good Spanish typing speed?", "a": "200-250 characters per minute (40-50 words per minute) is comfortable office speed. Spanish words are longer on average, so compare CPM when comparing across languages."},
            {"q": "Do accents count as errors?", "a": "Yes. Accents change meaning in Spanish - si and sí, el and él - so a missing accent is a language error, and Spanish typing tests treat it as a mistake."},
            {"q": "Should I use a Spanish keyboard layout?", "a": "If you are preparing for an exam or job in a Spanish-speaking country, yes. Typing Spanish on an English layout with dead keys trains a workaround rather than the skill you will be tested on."},
            {"q": "Why do the inverted ¿ and ¡ slow me down?", "a": "They are typed at the start of a sentence, so you must decide the sentence is a question before you begin typing it. That look-ahead is an extra decision per sentence."},
            {"q": "Is this Spanish test free?", "a": "Yes, no account, and the practice pool is real Spanish sentences with accents and ñ rather than stripped-down text."},
        ],
    },
    "japanese-typing-test.html": {
        "seo": [
            {"h2": "Japanese typing is two skills in sequence", "p": [
                "You type romaji, the input method converts it to kana, and a second conversion turns kana into kanji. So a single word can require typing, converting, and choosing from a candidate list - three decisions per word where English requires none.",
                "That is why Japanese typing speed depends heavily on conversion accuracy rather than raw keystrokes. A typist who converts correctly on the first try is faster than one who types faster but re-converts twice.",
            ]},
            {"h2": "Romaji input versus kana input", "p": [
                "Romaji input maps Latin letters to kana (ka → か) and is what most learners use, because it works on any keyboard. Kana input maps each kana to a single key on a Japanese keyboard; it has a higher ceiling because each kana is one keystroke instead of two or three.",
                "For most people romaji is the right choice: the keyboard is standard, the learning curve is shorter, and the ceiling is high enough for office work. Switch to kana input only if you type Japanese for hours a day.",
            ]},
            {"h2": "The conversions that cost the most", "p": [
                "<ul><li><strong>Kanji selection</strong> - homophones are common (こうしょう has dozens of kanji readings), so candidate lists matter.</li>"
                "<li><strong>Katakana words</strong> - loanwords are long and the conversion is rarely the first candidate.</li>"
                "<li><strong>Names</strong> - place and person names often need manual conversion.</li>"
                "<li><strong>Punctuation</strong> - the Japanese comma 、 and full stop 。 are separate keys from their Latin counterparts.</li></ul>",
            ]},
            {"h2": "How the score is reported", "p": [
                "This page reports WPM and CPM from the committed text. For Japanese, characters per minute is the meaningful figure, and it is typically much lower than an English WPM for the same typist - a reflection of the conversion work, not of slower fingers.",
                "Compare within Japanese over time rather than against English scores. For the general benchmarks, see <a href=\"average-typing-speed.html\">average typing speed</a>.",
            ]},
        ],
        "faq": [
            {"q": "How does Japanese typing work?", "a": "You type romaji, the input method converts it to kana, then a second conversion selects kanji from a candidate list. Each word can involve typing, converting and choosing."},
            {"q": "Is romaji or kana input faster?", "a": "Kana input has a higher ceiling because each kana is one keystroke, but it requires a Japanese keyboard or layout and a longer learning curve. Romaji is the practical choice for most people."},
            {"q": "Why is my Japanese WPM so low?", "a": "Conversion decisions cost time that keystroke speed cannot recover. Japanese characters per minute are typically far below an equivalent English WPM - compare within Japanese over time."},
            {"q": "What are the hardest parts?", "a": "Kanji selection for homophones, katakana loanwords, and names. All three require candidate-list navigation rather than faster typing."},
            {"q": "Is this Japanese test free?", "a": "Yes, no account, and the practice pool uses real Japanese sentences mixing kanji, hiragana and katakana."},
        ],
    },
    "urdu-typing-test.html": {
        "seo": [
            {"h2": "Nastaliq is a joining script with context-dependent shapes", "p": [
                "Urdu is written right to left in Nastaliq, where most letters change shape depending on what joins them on either side. You still press one key per letter - the shaping is the font's job - but the visual result is not one glyph per keystroke, which makes proofreading harder than in Latin script.",
                "Four characters decide accuracy: <strong>ڑ</strong> (retroflex r), <strong>ں</strong> (noon ghunna), <strong>ے</strong> (bari ye) and the difference between <strong>ہ</strong> and <strong>ھ</strong>. These are the pairs that show up in error reports, and they are the ones worth drilling.",
            ]},
            {"h2": "Layout and the RTL cursor", "p": [
                "The standard Urdu layout keeps Latin letters on the same physical keys and adds Urdu legends, so a touch typist can switch languages without moving hands. That is the good news: your existing muscle memory transfers.",
                "The complication is direction. In a right-to-left field the cursor moves left as you type, and mixing Urdu with Latin words or digits reverses the visual order of that run. If accuracy collapses when a sentence contains a number, that is bidirectional text handling rather than typing speed.",
            ]},
            {"h2": "Where Urdu typing is tested", "p": [
                "Pakistani government and clerical posts commonly ask for a typing certificate or a timed sample, with speeds quoted in words per minute and, for some posts, in keystrokes. Because requirements are set per employer, read the notice rather than assuming a national standard.",
                "If the test is proctored, rehearse on a different keyboard at least twice: legend placement and key travel change your error rate more than practice volume does.",
            ]},
            {"h2": "Practising that transfers", "p": [
                "Use real sentences rather than letter lists, and drill the four confusable characters in isolation for thirty seconds before each session. Then run a full-length round and check accuracy on those characters specifically.",
                "For the English side of the same skill, see <a href=\"english-typing-test.html\">English typing test</a>; for the general benchmark, <a href=\"average-typing-speed.html\">average typing speed</a>.",
            ]},
        ],
        "faq": [
            {"q": "Does Urdu typing count characters or letters?", "a": "Letters - one keystroke per letter. The joined Nastaliq shapes you see are produced by the font, not by extra keystrokes."},
            {"q": "Which characters cause the most errors?", "a": "ڑ, ں, ے and the ہ/ھ pair. They are visually similar in context and appear less often than common letters, so they stay less practised."},
            {"q": "Why does my accuracy drop when a sentence has numbers?", "a": "Mixing right-to-left Urdu with left-to-right digits reverses the visual order of that run. It is a bidirectional text issue rather than a typing-speed problem."},
            {"q": "What is a good Urdu typing speed?", "a": "200-250 characters per minute (40-50 words per minute) is comfortable office speed. Government and clerical tests commonly ask 20-30 words per minute for entry-level posts."},
            {"q": "Do I need a special keyboard?", "a": "No. The Urdu layout keeps Latin letters on the same keys, so you add it in your operating system and switch with a shortcut."},
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
    print(f"已补厚 {len(PATCH)} 个语种页")
    return 0


if __name__ == "__main__":
    sys.exit(main())
