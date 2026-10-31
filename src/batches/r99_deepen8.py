#!/usr/bin/env python3
"""R99：补厚 advanced / quick-brown-fox / how-fast-can-i-type 三页。

选点（GSC 28 天，位置与厚度交叉）：
  advanced-typing-test         p16.7 / 49 曝光 / 2,439
  quick-brown-fox-typing-test  p35.9 /  8 曝光 / 1,607（站内最薄的专题页之一）
  how-fast-can-i-type          p32.7 / 23 曝光 / 2,163

advanced 是站内位置最好的非头部页之一（p16.7），最值得补；
quick-brown-fox 是唯一讲「全字母句」的专题页，薄到撑不住这个题材。

用法：python3 src/batches/r99_deepen8.py [--check]
"""
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

PATCH = {
    "advanced-typing-test.html": {
        "seo_add": [
            {"h2": "What advanced text should actually test", "p": [
                "A test that calls itself advanced should raise difficulty in a way that changes the skill being measured, not just the words. Four levers do that, in ascending order of difficulty:",
                "<ol><li><strong>Punctuation density</strong> - more marks per sentence shifts the load onto Shift and the right pinky.</li>"
                "<li><strong>Vocabulary rarity</strong> - uncommon words stop you predicting the next letters, so reading slows and the hands wait.</li>"
                "<li><strong>Digit and symbol runs</strong> - codes, amounts, references; a different motor skill from prose.</li>"
                "<li><strong>Structural irregularity</strong> - line breaks, quotation nesting, capitalised defined terms.</li></ol>",
                "If a page only makes the words longer, it is a hard vocabulary test, not an advanced typing test. The distinction matters because the score only transfers to real work if the difficulty is the same kind.",
            ]},
            {"h2": "Why advanced scores are not comparable across sites", "p": [
                "At 70 WPM and above, the measurement differences that barely matter at beginner level start to dominate: a 15-second round versus five minutes, sentences versus quotes, gross versus net, and whether the pool repeats within a round. Two sites can differ by 15 WPM for the same typist without either being wrong.",
                "So compare only within a site, over time, at a fixed length. When you quote a number, quote the method with it: \"78 WPM net, sentences, five minutes\" is a measurement; \"78 WPM\" is a claim.",
            ]},
        ],
        "faq_add": [
            {"q": "What makes a typing test advanced?", "a": "Difficulty that changes the skill being measured: punctuation density, uncommon vocabulary, digit and symbol runs, and structural irregularity. Longer but simpler words are a vocabulary test, not an advanced typing test."},
        ],
    },
    "quick-brown-fox-typing-test.html": {
        "seo_add": [
            {"h2": "Where the sentence comes from", "p": [
                "The quick brown fox jumps over the lazy dog is a pangram - it contains every letter of the English alphabet at least once. Sentences like it were used from the late nineteenth century to test typewriters and telegraph equipment, because a single line could exercise every key.",
                "That history is why it is still the default demo text on keyboard and font sites. It is short, it is memorable, and it touches every letter without needing a paragraph.",
            ]},
            {"h2": "What it is good for, and what it is not", "p": [
                "<table><tr><th>Good for</th><th>Not good for</th></tr>"
                "<tr><td>Warming up every key in 15 seconds</td><td>Measuring your real speed - it is short and you memorise it</td></tr>"
                "<tr><td>Checking that every key registers</td><td>Testing punctuation, capitals or digits</td></tr>"
                "<tr><td>A first typing test for a beginner</td><td>Comparing yourself to a benchmark</td></tr></table>",
                "The memorisation point is the important one. By the fifth attempt you are recalling the sentence rather than reading it, and the score rises without your skill changing. Use it as a warm-up, then measure on text you have not seen.",
            ]},
            {"h2": "Other pangrams worth rotating", "p": [
                "Sphinx of black quartz, judge my vow; Pack my box with five dozen liquor jugs; How vexingly quick daft zebras jump; Waltz, bad nymph, for quick jigs vex. Each is a different length and a different letter distribution, which is exactly what stops memorisation from inflating the score.",
                "Two or three is enough. Rotating through sixteen is entertainment; rotating through three is practice.",
            ]},
        ],
        "faq_add": [
            {"q": "Why do typing tests use the quick brown fox?", "a": "It is a pangram - it contains every letter of the alphabet - so one short line exercises every key. It has been used to test typewriters and keyboards since the late nineteenth century."},
            {"q": "Is the quick brown fox a good speed test?", "a": "No, for measurement. It is short and quickly memorised, so the score rises without skill changing. Use it as a warm-up or a key check, and measure on unseen text."},
        ],
    },
    "how-fast-can-i-type.html": {
        "seo_add": [
            {"h2": "Find out in sixty seconds, then in five minutes", "p": [
                "The sixty-second test on this page gives you a number immediately. Treat it as a first reading, not a result: it is short enough that the warm-up advantage inflates it by 5-10 WPM.",
                "The number worth keeping comes from a five-minute round on sentences, run twice on different days. If the two scores are within 3 WPM, that is your speed. If they differ by 10, one of the two was a bad day - and the lower one is the honest figure.",
            ]},
            {"h2": "Why two people with the same score are not equal", "p": [
                "A 55 WPM score at 99% accuracy and a 55 WPM score at 92% accuracy are not the same asset. The second generates roughly one error every twelve words, which in a document is a correction every two sentences.",
                "That is why employers weight accuracy and often convert to <em>net</em> WPM before comparing. If your accuracy is under 96%, improving it will raise your usable speed faster than any speed drill.",
            ]},
        ],
        "faq_add": [
            {"q": "How do I find out how fast I type?", "a": "Take the sixty-second test on this page for a first reading, then run two five-minute rounds on different days. If they agree within 3 WPM, that is your speed; the lower of the two is the honest number."},
        ],
    },
}


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    pages = {p["file"]: p for p in cfg["pages"]}
    errs = [f"{f}: 不存在" for f in PATCH if f not in pages]
    if errs:
        print("\n".join(errs))
        return 1
    if "--check" in sys.argv:
        print("✅ 校验通过")
        return 0
    for f, patch in PATCH.items():
        pg = pages[f]
        have = {s["h2"] for s in pg["seo"]}
        for s in patch["seo_add"]:
            if s.get("h2") and s.get("p") and s["h2"] not in have:
                pg["seo"].append(s)
        haveq = {q["q"] for q in pg["faq"]}
        for q in patch["faq_add"]:
            if q["q"] not in haveq:
                pg["faq"].append(q)
    CFG.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for f in PATCH:
        pg = pages[f]
        print(f, sum(len(x) for s in pg["seo"] for x in s["p"]), "chars |", len(pg["faq"]), "faq")
    return 0


if __name__ == "__main__":
    sys.exit(main())
