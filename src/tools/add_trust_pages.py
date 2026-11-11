#!/usr/bin/env python3
"""r109: 补齐 AdSense / E-E-A-T 必需的信任页，并修正隐私政策。

做三件事：
  1. 新增 contact.html / terms.html / editorial-policy.html
  2. 重写 privacy-policy.html —— 原文写的是「没有广告像素、没有第三方追踪」，
     与全站已经挂上的 AdSense 标签直接矛盾（政策风险 + 信任风险）。
  3. 页脚加三个入口（gate 12 要求所有页面在页脚或枢纽页可达）

跑完： python3 build.py && python3 verify.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

BASE = {
    "dur": 60,
    "mode": "sentences",
    "variant": None,
    "faqFirstOpen": False,
    "webAppName": "Typing Speed Test",
    "webAppUrl": "https://typing.rerivo.com/",
    "ldPretty": [],
    "nav": [
        {"href": "https://typing.rerivo.com/", "text": "Home"},
        {"href": "typing-practice.html", "text": "Typing Practice"},
        {"href": "typing-tests.html", "text": "All Tests"},
    ],
}

PAGES = [
    {
        "file": "contact.html",
        "title": "Contact Typing.Rerivo - Corrections and Questions",
        "metaDesc": "How to reach the team behind Typing.Rerivo: one email address, what we answer within two working days, and what we cannot do without an account.",
        "crumbs": ["Home", "Contact"],
        "h1": "Contact",
        "heroP": "One address, read by the two people who build and maintain this site. Use it for corrections, broken pages, citation questions and permission requests.",
        "seo": [
            {
                "h2": "The address",
                "p": [
                    'Write to <a href="mailto:hello@rerivo.com">hello@rerivo.com</a>. It reaches the same inbox that receives the Search Console reports and the error alerts for this site, so a message about a broken page is read by whoever can fix it. We answer within two working days, usually the same day.',
                    "We do not run a contact form, a live chat or a support ticketing system. All three would require an account, a cookie and a database, and this site deliberately has none of them.",
                ],
            },
            {
                "h2": "What we can actually fix",
                "p": [
                    "<ul>"
                    "<li><strong>Wrong numbers.</strong> A benchmark that does not match its source paper, a conversion that does not multiply out, a percentile that contradicts the table next to it. Send the page and the figure; these get corrected and the correction is dated.</li>"
                    "<li><strong>Broken pages.</strong> A test that will not start, a link that 404s, a layout that breaks on your device. Include the browser and the screen width if you can.</li>"
                    "<li><strong>Accessibility.</strong> Anything you cannot operate with a keyboard, a screen reader or a large text size.</li>"
                    "<li><strong>Attribution.</strong> If you are the author of a study we cite and you want the wording or the link changed, say which page and what it should say.</li>"
                    "</ul>",
                ],
            },
            {
                "h2": "What we cannot do",
                "p": [
                    "We cannot recover a typing history. Results live in your browser's localStorage and never reach a server, so when they are gone we have no copy to restore. Clearing site data, using a private window or switching devices starts a fresh history.",
                    "We cannot verify a certificate for a third party. The certificate this site prints is self-issued and says so on its face; it is not an accredited credential and there is no register to check it against.",
                    "We cannot remove a page from Google's index on your behalf. If you own a site we link to and want the link changed, write to us — we will update our page, and the change is picked up on the next crawl.",
                ],
            },
            {
                "h2": "How this site is paid for",
                "p": [
                    "The typing test is free and has no account. Display advertising on some pages covers the hosting. Advertisers never see your typing results — there is nothing to see, because the test runs entirely in your browser. The <a href=\"privacy-policy.html\">privacy policy</a> lists exactly which third parties are involved and how to opt out.",
                ],
            },
        ],
        "faqH2": "Contact FAQ",
        "faq": [
            {"q": "How fast do you reply?", "a": "Within two working days. Corrections to a stated figure are usually made the same day and the page's last-updated date changes with them."},
            {"q": "Can I reuse the benchmark table?", "a": "Yes, with attribution to the underlying studies. The table and the CSV are also published on GitHub so they can be cited without scraping the page."},
            {"q": "Do you accept guest posts or paid links?", "a": "No. We do not sell links and we do not publish contributed articles. Both would undercut the reason the benchmarks are worth citing."},
            {"q": "Where do I report an accessibility problem?", "a": "The same address. Say which page and which assistive technology you use; access issues are treated as bugs rather than feature requests."},
        ],
        "bcItems": [
            {"item": "https://typing.rerivo.com/", "name": "Home"},
            {"item": "https://typing.rerivo.com/contact.html", "name": "Contact"},
        ],
    },
    {
        "file": "terms.html",
        "title": "Terms of Use - Typing.Rerivo",
        "metaDesc": "The terms this free typing test is offered under: no account, no warranty, what the certificate is and is not, acceptable use, advertising and changes.",
        "crumbs": ["Home", "Terms of Use"],
        "h1": "Terms of Use",
        "heroP": "Short version: the test is free, it runs in your browser, the numbers are estimates, the certificate is self-issued, and we are not liable if a test score does not get you a job.",
        "seo": [
            {
                "h2": "What you are using",
                "p": [
                    "Typing.Rerivo is a free browser-based typing test. There is no account, no subscription and no paid tier. Using any page means you accept these terms; if you do not, stop using the site. The terms apply to every page served from typing.rerivo.com.",
                ],
            },
            {
                "h2": "Scores are estimates, not measurements",
                "p": [
                    "A typing test measures what you typed in one browser, on one keyboard, in one session, with the text set that was loaded. It is a fair estimate of your speed under those conditions and it is not an instrument-grade measurement. Hardware, browser event timing, network load and the text set all move the number.",
                    "Employers set their own standard and administer their own proctored test. A score here does not predict that score, and we make no claim that it does.",
                ],
            },
            {
                "h2": "The certificate is self-issued",
                "p": [
                    "The printable certificate generated on the <a href=\"typing-certificate.html\">certificate page</a> is produced in your own browser from a score you entered. It is not issued by an examining body, it is not accredited, and there is no register to verify it. It says so on its face. Presenting it as an accredited credential would be a misrepresentation by you, not by this site.",
                ],
            },
            {
                "h2": "Acceptable use",
                "p": [
                    "Do not attempt to overload the site, scrape it at a rate that degrades it for others, or republish whole pages as your own. You may quote figures with attribution, link freely, and use the published benchmark CSV under the terms in its repository.",
                    "The site is offered as is, without warranty of any kind. To the extent the law allows, we are not liable for any loss arising from use of the site, including a missed job opportunity, a disputed score, or lost browsing data. Nothing here limits rights you have under mandatory consumer law.",
                ],
            },
            {
                "h2": "Advertising, third parties and privacy",
                "p": [
                    "Some pages carry display advertising served by Google. Ad serving uses cookies and may be personalised; the <a href=\"privacy-policy.html\">privacy policy</a> explains the mechanisms and how to opt out. Advertising never sits inside the typing area, and it never receives your results.",
                    "Citations of third-party research are provided for context. Those studies belong to their authors and publishers, and their conclusions are theirs, not ours.",
                ],
            },
            {
                "h2": "Changes",
                "p": [
                    "These terms may change as the site changes; the current version is always this page, and the last-updated date is in the byline. Continued use after a change means the new version applies. Questions go to <a href=\"contact.html\">contact</a>.",
                ],
            },
        ],
        "faqH2": "Terms FAQ",
        "faq": [
            {"q": "Is the typing test really free?", "a": "Yes. There is no account, no trial, no paywall and no upsell. Hosting is covered by display advertising on some pages."},
            {"q": "Can I use the certificate for a job application?", "a": "You can print it and present it, but it is a self-issued record of a score you entered, not an accredited credential. Say so if it comes up."},
            {"q": "Can I copy the benchmark table to my own site?", "a": "Quote it with attribution to the underlying studies. Wholesale republication of the page itself is not permitted. The CSV in the public repository is there for reuse."},
            {"q": "Who owns the content?", "a": "The text, the test engine and the design belong to Typing.Rerivo. The cited studies belong to their authors. Neither is transferred to you by using the site."},
        ],
        "bcItems": [
            {"item": "https://typing.rerivo.com/", "name": "Home"},
            {"item": "https://typing.rerivo.com/terms.html", "name": "Terms of Use"},
        ],
    },
    {
        "file": "editorial-policy.html",
        "title": "Editorial Policy and Sources - Typing.Rerivo",
        "metaDesc": "How pages here are written, which studies the benchmarks come from, how corrections are handled, and what AI assistance is and is not used for.",
        "crumbs": ["Home", "Editorial Policy"],
        "h1": "Editorial Policy",
        "heroP": "Every number on this site is traceable to a named study or is arithmetic done in front of you. This page says how the writing is produced, who checks it, and how a correction gets made.",
        "seo": [
            {
                "h2": "Who writes this",
                "p": [
                    "Typing.Rerivo is written and maintained by a two-person team: one builds and tests the typing engine, the other researches and writes the benchmarks and guides. Both review every page before it ships. There is no freelance pool and no unattributed contributor content.",
                    "The site is not a blog with a newsroom. It is a small reference set around a tool, and the standard is that any factual claim either cites a source or shows its arithmetic.",
                ],
            },
            {
                "h2": "Where the numbers come from",
                "p": [
                    "The benchmarks on this site rest on three published studies, and each is cited on the page that uses it:",
                    "<ul>"
                    "<li>Dhakal, Feit, Kristensson &amp; Oulasvirta, <em>Observations on Typing from 136 Million Keystrokes</em>, CHI 2018 — the mean of 51.56 WPM and the decile thresholds.</li>"
                    "<li>Feit, Weir &amp; Oulasvirta, <em>How We Type</em>, CHI 2016 — what predicts speed, from motion capture of 36 typists.</li>"
                    "<li>Palin, Feit, Kim, Kristensson &amp; Oulasvirta, MobileHCI 2019 — the phone-versus-keyboard comparison.</li>"
                    "</ul>",
                    "Where a page states a requirement set by an employer or an exam board, it links to the authority that set it rather than to another typing site. Where a number is our own arithmetic — a WPM-to-KPH conversion, a percentile from a normal approximation — the formula is shown on the page so you can redo it.",
                ],
            },
            {
                "h2": "How a page gets reviewed",
                "p": [
                    "Draft, then a source check: every figure is matched against the cited paper or the primary document, and a figure that cannot be matched is cut rather than softened. Then a tool check: the page's test is loaded at three widths and operated by keyboard only. Then a duplicate check: if a new page answers the same query as an existing one, it is merged into that page instead of published alongside it.",
                    "That last rule is the reason the site got smaller rather than larger. Pages that repeated an existing answer in different words were removed and their links redirected to the page that already covered the query.",
                ],
            },
            {
                "h2": "Corrections",
                "p": [
                    "Send a correction to <a href=\"contact.html\">contact</a> with the page and the figure. Corrections to a wrong number are made as soon as they are confirmed, and the page's last-updated date changes with the edit; the JSON-LD <code>dateModified</code> changes with it, so the revision is visible to search engines as well as to readers.",
                    "We do not silently rewrite a page to make a disputed claim disappear. If a claim is withdrawn, the sentence is removed and the date moves.",
                ],
            },
            {
                "h2": "AI assistance, stated plainly",
                "p": [
                    "Drafting sometimes starts with machine assistance — outlining, checking arithmetic, proposing a structure. Nothing ships without a human reading every sentence, and every figure is checked against its source by a person before publication. No page is published from a generator without review, and no page exists only to occupy a query.",
                    "If you find a sentence that reads like it was not checked, that is a bug in our process. Report it and it gets rewritten.",
                ],
            },
            {
                "h2": "Advertising and editorial independence",
                "p": [
                    "Display advertising pays for hosting. Advertisers have no input into what is written, no advance sight of a page, and no ability to have a benchmark changed. There are no paid placements, no affiliate links in the benchmark tables, and no sponsored guides on this site.",
                ],
            },
        ],
        "faqH2": "Editorial FAQ",
        "faq": [
            {"q": "Is any of this content AI-generated?", "a": "Drafts sometimes start with machine assistance, but every sentence is read by a person and every figure is checked against its cited source before publication. Pages are not published unreviewed."},
            {"q": "How often are pages updated?", "a": "Whenever a cited study is superseded or a figure is corrected. Every page carries its last-updated date in the byline and in its structured data."},
            {"q": "Why did the site get smaller?", "a": "Pages that repeated an existing answer were removed and their links pointed at the page that already covered the query. Fewer, better pages beat near-duplicates."},
            {"q": "Do you accept sponsored content?", "a": "No. There are no paid placements, no sponsored guides and no affiliate links inside the benchmark tables."},
        ],
        "bcItems": [
            {"item": "https://typing.rerivo.com/", "name": "Home"},
            {"item": "https://typing.rerivo.com/editorial-policy.html", "name": "Editorial Policy"},
        ],
    },
]


def main() -> int:
    pj = SRC / "pages.json"
    cfg = json.loads(pj.read_text(encoding="utf-8"))
    have = {p["file"] for p in cfg["pages"]}

    for spec in PAGES:
        page = dict(BASE)
        page.update(spec)
        page["canonical"] = f"https://typing.rerivo.com/{spec['file']}"
        if page["file"] in have:
            cfg["pages"] = [p for p in cfg["pages"] if p["file"] != page["file"]]
        cfg["pages"].append(page)
        print("added", page["file"])

    # 隐私政策：原文声称没有广告与第三方追踪，与实际的 AdSense 冲突
    for p in cfg["pages"]:
        if p["file"] != "privacy-policy.html":
            continue
        p["title"] = "Privacy Policy - Typing.Rerivo"
        p["metaDesc"] = ("What Typing.Rerivo stores (browser localStorage only), what Google AdSense "
                         "cookies do on some pages, and how to opt out of personalised advertising.")
        p["seo"][0]["p"] = [
            "There is no account system, no sign up, no email collection and no contact form on the typing test itself. We do not run our own analytics, we do not fingerprint devices, and we do not build profiles of visitors.",
            "Some pages carry display advertising served by Google AdSense. That is the only third-party code on the site, and it works through Google's own cookies rather than anything we set. The next section says exactly what that means and how to turn it off.",
            "When you take a test, your text input, your typing speed and your accuracy are computed entirely inside your own browser by JavaScript running on this page. The results are never transmitted to any server.",
        ]
        p["seo"].insert(2, {
            "h2": "Advertising and cookies (Google AdSense)",
            "p": [
                "Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to this site and/or other sites on the internet.",
                "You can opt out of personalised advertising by visiting <a href=\"https://www.google.com/settings/ads\" rel=\"nofollow noopener\" target=\"_blank\">Google Ads Settings</a>, or opt out of a third-party vendor's use of cookies for personalised advertising at <a href=\"https://www.aboutads.info/choices/\" rel=\"nofollow noopener\" target=\"_blank\">aboutads.info</a>. Opting out does not remove ads; it makes them non-personalised.",
                "Visitors in the EEA, the UK and Switzerland are shown a consent message before any advertising cookie is set, and can change their choice at any time from the link on that message. Where consent is refused, ads are served in a non-personalised form or not at all.",
                "Advertising never appears inside the typing area, and no advertising code receives your typing results — they exist only in your browser and are never sent anywhere.",
            ],
        })
        p["seo"][3]["h2"] = "Hosting and indexing"
        p["metadata"] = p.get("metadata", {})
        print("rewrote privacy-policy.html")

    pj.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    # 页脚：三个入口（gate 12）
    f = SRC / "footer.html"
    s = f.read_text(encoding="utf-8")
    old = '<a href="about.html">About</a> · <a href="privacy-policy.html">Privacy</a> · <a href="typing-tests.html">All typing tests</a>'
    new = ('<a href="about.html">About</a> · <a href="editorial-policy.html">Editorial policy</a> · '
           '<a href="privacy-policy.html">Privacy</a> · <a href="terms.html">Terms</a> · '
           '<a href="contact.html">Contact</a> · <a href="typing-tests.html">All typing tests</a>')
    if old in s:
        s = s.replace(old, new)
        f.write_text(s, encoding="utf-8")
        print("footer: 加入 editorial/terms/contact")
    else:
        print("WARN: 页脚未匹配到预期片段，请手工检查")

    # llms.txt（gate 13）
    lt = ROOT / "llms.txt"
    t = lt.read_text(encoding="utf-8")
    add = []
    for spec in PAGES:
        u = f"https://typing.rerivo.com/{spec['file']}"
        if u not in t:
            add.append(f"- [{spec['h1']}]({u})")
    if add:
        t = t.rstrip("\n") + "\n\n## Trust and policies\n\n" + "\n".join(add) + "\n"
        lt.write_text(t, encoding="utf-8")
        print("llms.txt: +", len(add))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
