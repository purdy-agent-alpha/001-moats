"""
The video's sections, in order. The one list every pipeline step reads.

The source pipeline kept five copies of this table (gate, assemble, Gemini,
rank, dashboard); one copy means a new section cannot be gated but not
assembled.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Section:
    id: str        # timing and audio file stem, e.g. "01_open"
    module: str    # scene file stem under scenes/
    scene: str     # scene class
    title: str     # human title, used in review output
    heading: str   # prefix of the "### " heading in drafts/script.md

    @property
    def code(self) -> str:
        return self.id.split("_")[0]


SECTIONS = [
    Section("01_open", "s01_open", "S01Open", "1 · Code is cheap", "1. Cold Open"),
    Section("02_moat", "s02_moat", "S02Moat", "2 · What a moat is", "2. What Is"),
    Section("03_cheap", "s03_cheap", "S03Cheap", "3 · What got cheap", "3. What Got"),
    Section("04_die", "s04_die", "S04Die", "4 · Which moats die", "4. Which Moats"),
    Section("05_network", "s05_network", "S05Network", "5 · Network effects", "5. Network"),
    Section("06_limit", "s06_limit", "S06Limit", "6 · In the limit", "6. In The"),
    Section("07_saas", "s07_saas", "S07Saas", "7 · Running a SaaS company", "7. Running"),
    Section("08_investing", "s08_investing", "S08Investing", "8 · An investing note", "8. An Investing"),
    Section("09_method", "s09_method", "S09Method", "9 · How this was made", "9. How This"),
    Section("10_close", "s10_close", "S10Close", "10 · The answer", "10. Close"),
]


def by_scene(scene: str) -> Section:
    return next(s for s in SECTIONS if s.scene == scene)


def by_code(code: str) -> Section | None:
    return next((s for s in SECTIONS if s.code == code), None)


def select(prefixes: list[str] | None) -> list[Section]:
    if not prefixes:
        return list(SECTIONS)
    return [s for s in SECTIONS if any(s.id.startswith(p) for p in prefixes)]
