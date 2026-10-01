#!/usr/bin/env python3
"""给3个内页的内链列表补上 typing-practice 链接。"""
import re
li = '      <li><a href="typing-practice.html">Typing Practice</a> — longer drills to build accuracy and speed.</li>\n    </ul>'
for f in ["1-minute-typing-test.html", "words-per-minute-test.html"]:
    t = open(f, encoding="utf-8").read()
    n = t.count("    </ul>")
    assert n == 1, (f, n)
    t = t.replace("    </ul>", li)
    open(f, "w", encoding="utf-8").write(t)
    print("patched", f)
