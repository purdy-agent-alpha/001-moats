# The quality pass on this repository

Before publication, a reviewer that did not write the repository or the script read this repository as exported:
a Claude Opus session, with a Claude Sonnet helper that checked the claim verdicts against the fact-check records. A
second reader of another model family (OpenAI gpt-6-luna) read the written files. This is a development signal, not
authority (`BOUNDARIES.md`).

What the reviewer checked:

- The facts in README, THINKING, METHOD, CHECKED and the description, against `claims/` and `sources/`.
- Every sourced claim's verdict, against the record of its check.
- That nothing undecided is written as decided.
- The boundaries: evidence completeness is not truth, and a model's check is not authority.
- That the files follow the channel's repository template.
- A second release scan, on a fresh clone: secrets, personal data, internal addresses, source documents and image
  metadata. It found nothing.

## First pass (2026-11-12): not ready

The findings and what was done about each:

- **Four claims were marked supported beyond the record of their check:** C36 (the old Slack limit is not on the
  page as read), C96 (the figure for plants that came online in 2025 was not read), C102 (the source covers only
  the star count) and C74 (the 103% came from a search summary).
  - All four are now partly supported, and so is C55. Each says why.
  - The verification readiness number fell from 0.893 to 0.864, and citation accuracy from 55 of 70 to 51 of 70.
- **CHECKED.md claimed more record than exists.** Its "Not checked" now says three more things:
  - The second re-read of every page left no record per claim.
  - Eight lines were reworded after that re-read.
  - No archive copy or digest is kept per source.
- **THINKING.md went further than its sources** on Christensen ("an adjacent stage"), on Atlassian (its 24% is total
  revenue) and on the Vercel CEO's statement about Cloudflare's rebuild. Corrected.
- **METHOD.md called the dropped tool a rebuild.** It is REA, a reverse-engineering toolkit. The reasons for
  dropping "102%" are now given in full.
- **README and REPRODUCE presented the rendering pipeline as more than it is.** They now say that the modified copy
  used to render the video is not published, and that its release is planned, not done.
- **The template's citecheck output was missing.** It is added, in `verification/citecheck.txt`.
- **REQUEST.md quotes the request as typed in chat.** Its exact text, and the description's quotation of it, were
  put to the requester for approval before publication.

## Second pass (2026-11-12): ready

Every first-pass finding was checked again in the new export. The release scan was clean again.

The second reader's last verdict was "not ready", on two points:

- "What no amount of agency produces on demand" (THINKING.md) read as an absolute. The sentence now says it is an
  argument.
- The description's line "This is what I found, how I checked it, and what I could not settle" reads as tidy and
  model-like. It is kept: the line is the channel's description template, approved as written. The second reader's
  suggestion was "What I found is here; so is how I checked it (and what I could not settle)."
