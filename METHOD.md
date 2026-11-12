# Method

How the question became a video, by Alpha, an AI research agent. The research ran from 2026-10-19 to 2026-11-10; a
first version of the video was made and sent back by Levi Purdy on 2026-11-09, and this version answers his review.

## Sub-questions

1. What is a moat? (Buffett's letters, Helmer's 7 Powers, Morningstar's five sources.)
2. What got cheap, and by how much? (Price per token; cost per task on the ARC-AGI-1 leaderboard and its Pareto
   frontier; Epoch AI's price trends; METR's task-length measure; rebuilds of real products and what they cost.)
3. Which moats die? (Secret code, the cost to switch, seat pricing; churn data; firms dropping SaaS contracts.)
4. What are network effects really? (Stack Overflow's decline; Facebook; a power-grid operator's membership.)
5. In the limit, when agents can do whole jobs, what stays hard? (Christensen's conservation of attractive profits;
   agency and its price; how agents are allowed to pay; legal standing.)
6. For a software company: retention, growth, the customer relationship (HubSpot's filings and calls).
7. For an investor: how the market repriced software, and where capacity is scarce (grid queues, transformer lead
   times, capacity auction prices).

## Where it searched

Web search, then the pages themselves; the filings on SEC EDGAR; arXiv; the ARC Prize leaderboard's embedded data;
METR's and Epoch AI's own pages; company press releases and changelogs; earnings call transcripts; Wayback Machine
copies where a page had moved. Each source's record, with the date it was read and whether the page itself, its
abstract, a snippet or only a search summary was read, is in `sources/sources.yaml`.

## Models and tools

- Research, script and scenes: Alpha, running on Anthropic Claude models (Claude Opus for the research and writing,
  Claude models that did not write the script for the independent fact checks and quality passes), in Claude Code.
- Second reader of the narration: OpenAI gpt-6-luna, given the narration and a facts sheet.
- Frame review: Google gemini-3.1-pro-preview, one still per beat.
- Voice: Fish Audio Drama 3, speaking a voice designed for Alpha that imitates no one; every take checked word for
  word with Whisper (medium).
- Pictures: Manim Community v0.22.1 and ffmpeg 9.0.2, through Levi Purdy's verification-compiler video pipeline and
  its frame gate.

## Dead ends and dropped claims

- GitHub stars counted as use. Levi caught it in the first version: stars are attention. A tool with a hundred
  thousand stars (REA, a reverse-engineering toolkit) was dropped; only rebuilds people used, paid for, or that an incumbent had to answer were kept (the
  video says so in section 9).
- A tool attributed to the wrong project, and a figure its cited page did not contain: both caught by the checks on
  the first version and fixed before Levi saw it.
- "Net revenue retention slipping to 102%", beside "grew twenty percent" and "cracks in retention, not revenue":
  the 20% was growth as reported, flattered by currency (17% in constant currency); revenue growth was falling too
  (21% at the end of 2024, 17% now, 12% guided), so the cracks were not only in retention; and 102% sounds like a
  loss, when over 100% means existing customers still spend more than a year before. HubSpot also restated the
  series from 2026. Rewritten to compare 2026 quarters only (103%, then 101%), with gross retention and growth
  beside it.
- A 61-month median wait to connect a power plant to the grid came from a figure that was not read; the video says
  "more than five years", which the page's text says.
- A page cited for transformer lead times did not give the 128-week figure; replaced by Wood Mackenzie (S46).
- A 16% fall for Thomson Reuters came from a page before it was read; the video now says "double digits: fourteen
  percent, by one report", since reports give 11, 14.2 and 17% for different markets and hours.
- A Forbes source that could not be opened was dropped. Christensen's book was not opened; the narration
  paraphrases the one sentence read in a snippet, and no more.
- Stack Overflow's fall was kept only after its figures were checked (207,204 new questions in March 2014, 1,442 in
  July 2026).
