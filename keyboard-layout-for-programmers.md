# Best Keyboard Layout for Programmers

Source: https://typing.rerivo.com/keyboard-layout-for-programmers.html

Programmers do not type prose, they type symbols wrapped in words. That changes the layout question: the letters are already solved, and the brackets, braces, quotes and operators are what a layout helps or hurts.

A rough count of ordinary source code: letters are still the majority of characters, but the shifted symbol row ( ) { } [ ] ; : " ' = + - _ / \ | carries a disproportionate share of the awkward reaches, and those reaches are where errors cluster.

So the question is not "which layout is fastest for English" - it is "which layout puts the symbols you type most under the fingers that can reach them without leaving the home row".

Layout | Letter changes | Symbol changes | Cost of switching
QWERTY | None | None - symbols where every tool, shortcut and tutorial expects them | Zero
Dvorak | Substantial reordering for English comfort | Number row rearranged; brackets moved | Weeks of being slower; shortcuts assume QWERTY positions
Colemak | 17 keys moved; keeps Z X C V in place for shortcuts | Mostly unchanged | Weeks, but lower than Dvorak
Programmer Dvorak | Dvorak letters | Number row replaced with symbols; digits shifted | High - digits need Shift for every number

Programmer Dvorak looks attractive on paper because symbols get the unshifted number row. In practice the digits then require Shift, which is a bad trade for anyone who types numbers - and most code contains them.

For most programmers, stay on QWERTY. The reason is not that it is optimal; it is that every editor shortcut, every bracket-matching habit and every tutorial assumes it, and your bottleneck is thinking, not the 60-70 WPM you already type.

Consider a change only if all three hold: you are past 60 WPM on QWERTY, you type code for several hours a day, and your error report shows the symbol reaches as the main source of mistakes. Even then, expect a month of being slower before any gain.

Practise the symbols you actually type. Bracket-and-quote drills beat layout changes by a wide margin.
Let the editor do the brackets. Auto-pairs, snippets and formatters remove keystrokes; a layout reorders them.
Learn five shortcuts properly. Duplicate line, move line, go to definition, rename symbol, format document.

Code typing pools to practise on: Python, JavaScript, TypeScript, Rust, Go, SQL. The general comparison is on Dvorak vs QWERTY.

## Frequently asked questions

### Is Dvorak better for programming?

Not measurably. It reorders letters for English comfort and moves brackets, which breaks shortcut muscle memory. The evidence for a coding gain is anecdotal rather than measured.

### What about Programmer Dvorak?

It puts symbols on the unshifted number row, which sounds ideal until you need a digit - then every number requires Shift. For most codebases that is a bad trade.

### Should I learn Colemak as a programmer?

Only if you are already past 60 WPM, type code for hours a day, and want comfort rather than speed. It keeps Z X C V in place, so shortcuts survive better than with Dvorak.

### What actually makes programmers type faster?

Practising symbols, using snippets and formatters, and learning editor shortcuts. Layout changes come last, if at all.

### How fast do programmers type?

Most sit at 60-90 WPM on prose and 40-55 on real code, because code is symbol-dense. No employer screens for it.
