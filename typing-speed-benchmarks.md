# Typing Speed Benchmarks

Source: https://typing.rerivo.com/typing-speed-benchmarks.html

Every number this site uses, with where it comes from. 51.56 WPM on a desktop keyboard and 36.17 WPM on a phone are the two measured averages; everything else on this page is either arithmetic or a labelled market range.

On this page

Measured averages (the only two hard numbers)
Percentile curve (derived, labelled as an approximation)
Unit conversions (arithmetic, not measurement)
Job requirement bands (market ranges, labelled)
What is not on this page, and why
How to cite this page

Measure | Desktop keyboard | Phone (touchscreen)
Mean speed | 51.56 WPM (SD 20.2) | 36.17 WPM (SD 13.22)
Uncorrected error rate | 1.17% | 2.34%
Keystrokes per character | 1.173 | 1.18
Participants | 168,960 | 37,370
Keystrokes recorded | 136,857,600 | not reported as a total
Percentile thresholds reported by the authors | top 10% > ~78 WPM; bottom 10% < ~26 WPM | 75% below 43.98 WPM
Source | Dhakal, Feit, Kristensson & Oulasvirta, CHI 2018, doi.org/10.1145/3173574.3174220 | Palin, Feit, Kim, Kristensson & Oulasvirta, MobileHCI 2019, doi.org/10.1145/3338286.3340120

Both studies used the same task - transcribe a displayed English sentence - so the device comparison is unusually clean. The mobile study compares itself to the desktop one directly and reports that average performance is about 15 WPM slower on a phone.

WPM | Percentile | CPM | Keystrokes per hour
20 | 6th | 100 | 6,000
30 | 14th | 150 | 9,000
40 | 28th | 200 | 12,000
50 | 47th | 250 | 15,000
60 | 66th | 300 | 18,000
70 | 82nd | 350 | 21,000
80 | 92nd | 400 | 24,000
90 | 97th | 450 | 27,000
100 | 99th | 500 | 30,000

Computed from a normal distribution with mean 51.56 and standard deviation 20.2. It is an approximation - real typing speed is mildly left-skewed - and it is validated by reproducing the study's own reported deciles (about 26 and 78 WPM) to within one percentile point. Enter any score to convert it.

The full curve at 5 WPM steps is available as typing-speed-benchmarks.csv (columns: wpm, percentile, percentile_rounded, cpm, keystrokes_per_hour). Reuse it with attribution. The same curve, the Python and JavaScript percentile functions and the source table are published as a repository at github.com/hello532/typing-speed-benchmarks, so a citation can point at the code as well as the page.

From | To | Formula | Example
WPM | CPM | × 5 | 40 WPM = 200 CPM
CPM | KPH | × 60 | 200 CPM = 12,000 KPH
WPM | KPH | × 300 | 40 WPM = 12,000 KPH
KPH | WPM | ÷ 300 | 10,000 KPH = 33.3 WPM
Key depressions/hour | WPM | ÷ 300 (corrections count) | 8,000 KDPH ≈ 26.7 WPM

The factor of five is the characters-per-word convention, not a physical constant. It exists so that a score on a long-word passage and a short-word passage can be compared.

Role | Advertised band | Basis
General office / admin | 40-55 WPM | Range across advertised clerical postings
US federal clerk | 40 WPM, 5 minutes, ≤3 errors | Published federal clerical standard
Data entry clerk | 8,000-12,000 KPH | Range across advertised postings
Legal secretary | 60-75 WPM | Range across advertised postings
Medical transcription | 65-80 WPM | Range across advertised postings
Court reporter (stenotype) | 225 WPM | Certification standard, not a keyboard

These are not measurements of a population; they are what employers and certifying bodies publish. Two employers in the same sector commonly differ by ten WPM, so read the posting rather than the table. Detail per role: typing speed requirements by job.

There is no average speed by country, no average by gender, and no "average for a 12-year-old" figure here, because we could not find a primary measurement for them that we were willing to cite. Sites that publish those numbers rarely link a study.

There is also no traffic or leaderboard statistic: this site stores results in the visitor's browser, so it has no server-side dataset to aggregate and will not pretend to have one.

Preferred form: "Typing.Rerivo, Typing Speed Benchmarks, https://typing.rerivo.com/typing-speed-benchmarks.html (accessed DATE)". The underlying numbers should be cited to the papers above, not to this page - the page is a convenient summary, not the source.

If you reuse the CSV, keep the column names and note that the percentile column is a normal approximation of the CHI 2018 distribution.

## Frequently asked questions

### What is the average typing speed in 2026?

51.56 WPM on a desktop keyboard, from the CHI 2018 study of 168,960 volunteers. On a phone the measured average is 36.17 WPM from a 37,370-person study.

### What percentile is 60 WPM?

About the 66th on desktop. The percentile curve here is a normal approximation of the CHI 2018 distribution (mean 51.56, SD 20.2), validated against the study's reported deciles.

### Can I download the data?

Yes - typing-speed-benchmarks.csv has 25 rows at 5 WPM steps with percentile, CPM and keystrokes per hour. Reuse it with attribution to Typing.Rerivo and the original papers.

### Why are there two different averages on different sites?

Older sources quote about 40 WPM from small office-worker samples; the 51.56 WPM figure comes from a 168,960-person online sample. Both describe real populations but not the same one.

### Is the phone number comparable to the desktop number?

Yes, unusually so: both studies used the same transcription task and the mobile paper compares itself to the desktop one directly, reporting about 15 WPM difference.
