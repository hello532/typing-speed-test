# Rust Typing Practice

Source: https://typing.rerivo.com/rust-typing-practice.html

Rust is the most punctuation-dense mainstream language: lifetimes, turbofish-free generics, match arms, ? and => on nearly every line. This drill types 36 real lines from ordinary Rust code.

Three characters dominate: & for borrows, ' for lifetimes and char literals, and < > for generics. Each sits on the top row or the right pinky, and lifetimes put the apostrophe immediately after an ampersand - a two-key sequence that prose never asks for.

Then there is the shape of idiomatic Rust: `match` arms with indentation, iterator chains broken across lines, and `?` at the end of expressions. The line breaks are part of the syntax you are training, not formatting noise.

Thirty-six lines covering the constructs that appear in real files: a struct with a generic parameter, a lifetime-annotated function, a `match` with an error branch, a `HashMap` build, an iterator chain with `filter_map`, a trait implementation, a `#[derive]` attribute, an async function signature with `anyhow::Result`, and a test module.

The lines are short enough to finish inside a minute round and varied enough that you cannot memorise the sequence.

Alternate two rounds per session: one straight accuracy round at your normal pace, one where you deliberately slow to 80% and watch the right hand. The second round is where the improvement happens; the first is where you measure it.

Track the errors rather than the WPM for the first week. In symbol-dense code, error count is the leading indicator and speed follows it, not the other way round.

Same engine, different grammar: Python, JavaScript, TypeScript, SQL. If you want the general number, use the programmer typing benchmarks page.

## Frequently asked questions

### What typing speed do Rust developers have?

No one measures this formally. In practice most developers type prose at 60-90 WPM and real Rust at 40-55 WPM because of symbol density and line breaks.

### Why do lifetimes slow typing down?

A lifetime needs an apostrophe immediately followed by a letter, and borrows need ampersands. Both sit on the top row and the right pinky, so the sequence interrupts the home-row rhythm.

### Is this real Rust?

Yes, 36 lines of ordinary Rust: generics, lifetimes, match arms, iterator chains, trait impls, async signatures and a test module.

### Does typing speed matter for a Rust job?

Not directly. It matters only when the keyboard becomes the bottleneck for long files, documentation or review comments - below about 40 WPM on code, that happens regularly.

### How much practice is enough?

Five minutes a day for two to three weeks. Symbol accuracy responds quickly; after that, speed follows without extra drills.
