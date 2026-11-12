# What was checked, by whom, and what was not

Every claim's own verdict and checker is in `claims/claims.md`; the totals are in `verification/report.md`. Models
are named by maker and family; none of them is an authority, and a check by a model is a development signal
(`BOUNDARIES.md`).

| What | Who | How | When | Result |
|---|---|---|---|---|
| Every cited line against its source | a Claude model that did not write the script | opened each cited page (or its archive copy) and compared the line with the page's words | 2026-11-08 | 70 cited lines: 59 supported, 9 overstated (each line fixed), 2 sources not opened (one dropped, one paraphrased from a snippet), 0 wrong in the narration (1 in the source list, S52, fixed) |
| Every cited page again | three Claude Sonnet readers, one per third of the script | opened every cited page again, without the earlier check | 2026-11-09 | findings fixed in the script before it was spoken again |
| The argument, the facts and the boundaries | three Claude Opus reviewers that did not write it, one after another | read the narration, the source list with quotes, and the cut | 2026-11-09 to 2026-11-10 | first not ready, its findings fixed; then ready with three minor points, fixed; then ready with five minor points, taken |
| The narration as a listener hears it | OpenAI gpt-6-luna, the second reader | read the narration and a facts sheet | 2026-11-09 to 2026-11-10 | not ready, on cadence (lists of three, a repeated phrase) and on lines the reviewers found settled; left to Levi's read |
| Every link and quotation, word by word | citecheck, Alpha's deterministic checker | fetched every link; matched each claim's words with the page's sentences | 2026-11-12 | 70 references: 44 flagged for a person to read (44 no word match, mostly paraphrase; 3 fetches failed); the output is `verification/citecheck.txt` |
| The voice against the script | Whisper (medium) | every take transcribed and compared word for word | 2026-11-10 | 0 words missed; longest silence in a kept take 1.1 s |
| Every frame | Levi Purdy's video pipeline frame gate (25 checks, each proven by a planted defect) | every section rendered at 480p15 and 1080p30 | 2026-11-09 to 2026-11-10 | clean in every section |
| Stills, one per beat | Google gemini-3.1-pro-preview, then Alpha | judged each still against its line and the video's shape grammar | 2026-11-09 | three passes; blocking findings fixed or dismissed with a reason; minor findings left |
| Loudness and captions | the pipeline's assembly step | measured the delivered audio; captions from the script text | 2026-11-10 | -14.5 LUFS, true peak -1.1 dBTP; 258 caption cues, fastest 20.0 characters a second |
| The channel's episode rules | the channel's episode gate (17 checks) | read the script, storyboard, sources and claims | 2026-11-12 | 13 pass; 4 fail on rules written after this video was made (below) |
| This repository before publication | release-scan (gitleaks, secrets, personal data, internal addresses), and a reviewer that did not write it | scanned the exported repository; read it against the channel's template | 2026-11-12 | release-scan clean (two runs, one on a fresh clone); an independent reviewer (a Claude Opus session that did not write it): not ready, then ready after fixes; see `verification/quality-pass.md` |
| The video, as a whole | Levi Purdy | watched the first version and sent it back with comments on the argument (2026-11-09); approved publishing this version (2026-11-12) | 2026-11-09, 2026-11-12 | this version answers his comments |

## Not checked

- Levi Purdy did not trace any claim to its source himself; his part was the question, the review of the first version, and the approval to publish.
- Christensen's The Innovator's Solution was not opened: the narration paraphrases one sentence read in a Google Books snippet, quoted in another book.
- Two sources were read only as a search summary (S2, and the NBER paper S59) and two only as an abstract (S23, S51); their lines are marked partly supported at most.
- The 2026-11-09 re-read of every cited page left no record per claim, only a summary; nor did the rewording of eight lines after it (C11, C25, C45, C53, C60, C75, C77, C83), which the reviewers of 2026-11-10 read as reworded.
- No archive copy (Wayback Machine) and no digest of the page as read is recorded per source, so a later change at a source's address would not show here.
- Company figures (Beeper's downloads, Cloudflare's cost, Vercel's security flaws, HubSpot's guidance, Foundation Capital's market size) are the companies' own claims, reported as such; nobody checked them independently.
- The extrapolation of METR's task lengths to a working month is Alpha's arithmetic beyond what METR says it can measure; it is marked as a guess.
- The episode gate's opening and arc rules were set after this video was made: the stakes come at about 34 s (the rule asks 15 s), the plan at about 60 s (45 s), the close names no open question of its own (the unknowns are in sections 6, 8 and 9), and two diagrams follow each other in section 7. The video was not changed for them.
- The frame review's minor findings (third pass) were left, and no fourth frame pass was run after the last fixes; the changed frames were checked by eye.
