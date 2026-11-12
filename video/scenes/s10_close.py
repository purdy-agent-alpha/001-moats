"""
Section 10: the close. Not hidden code; a company owns the relationship, the
record and the responsibility; in the limit, connected, permitted capacity.
Then where to check all of it: the repository, the loop that fixes a wrong
figure in the open, and where the next question goes (the first two
beats are adapted from the previous video's close).
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from moats_video.pipeline import style
from moats_video.pipeline.beats import Beat, BeatScene

# This video's research repository, at the address the channel design gives it (`<NNN>-<slug>` on Alpha's GitHub).
REPO_URL = "github.com/purdy-agent-alpha/001-moats"


def label(text: str, color: str = style.WHITE, size: str = "label") -> Text:
    return style.label_text(text, color=color, size=size)


def named_hex(word: str, size: float = 1.2) -> VGroup:
    """A moat, named underneath."""
    h = style.node("moat", size=size)
    return VGroup(h, label(word, style.GOLD).next_to(h, DOWN, buff=0.25))


def card(text: str, color: str, w: float = 1.5, h: float = 0.8) -> VGroup:
    name = label(text)
    box = style.tile(max(w, name.width + 0.6), h, color)
    name.move_to(box)
    return VGroup(box, name)


def folder(text: str) -> VGroup:
    """A folder icon (a tile with a tab) and its name in mono."""
    body = style.tile(0.55, 0.38, style.BLUE, opacity=0.3)
    tab = style.tile(0.24, 0.1, style.BLUE, opacity=0.3).next_to(body, UP, buff=0).align_to(body, LEFT)
    name = style.mono_text(text, size="label").next_to(body, RIGHT, buff=0.3)
    return VGroup(body, tab, name)


def rim(box: Mobject, direction) -> np.ndarray:
    """Where a ray from a rectangle's (or an agent diamond's) centre towards `direction` leaves it."""
    u = direction / np.linalg.norm(direction)
    hw, hh = box.width / 2, box.height / 2
    if getattr(box, "qa_kind", None) == "agent":      # a diamond: |x|/hw + |y|/hh = 1
        t = 1 / (abs(u[0]) / hw + abs(u[1]) / hh)
    else:
        t = min(hw / abs(u[0]) if abs(u[0]) > 1e-6 else 1e9, hh / abs(u[1]) if abs(u[1]) > 1e-6 else 1e9)
    return box.get_center() + u * (t + 0.08)


def curved(a: Mobject, b: Mobject, color: str) -> CurvedArrow:
    d = b.get_center() - a.get_center()
    arrow = CurvedArrow(rim(a, d), rim(b, -d), angle=-PI / 5, color=color, stroke_width=3.4)
    arrow.qa_role = "edge"
    arrow.qa_layer = "edge"
    arrow.set_z_index(style.Z_EDGE, family=True)
    return arrow


class S10Close(BeatScene):
    section_id = "10_close"
    title = "The answer"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("So, what keeps a company alive when code is cheap", self.b_hide,
                 note="the product in a ring of hidden code; a clone peels off it anyway; the ring is struck"),
            Beat("A company owns what a clone has no way to make", self.b_company,
                 note="a company and a dimmed clone; relationship, record, responsibility, one per phrase"),
            Beat("In the limit, it is connected, permitted capacity", self.b_limit,
                 note="the three merge into one gold shape, which splits into its three hexagons"),
            Beat("Every source, every claim check, and the code", self.b_repo,
                 note="a repository panel, three folders, an arrow down to the repository's link"),
            Beat("If a figure here is wrong, say so there", self.b_fix,
                 note="a loop: issue, check, fix, in the open"),
            Beat("And if you have a question worth investigating", self.b_next,
                 note="a question mark travels to Levi, then to Alpha: the next investigation"),
        ]

    # ------------------------------------------------------------ helpers --
    def _at(self, ctx, frac: float) -> None:
        """Wait until `frac` of this beat's window has passed (never past its end)."""
        lag = ctx.beat.start + frac * ctx.window - self.renderer.time
        if lag > 0.02:
            self.wait(lag)

    # -------------------------------------------------------------- beats --
    def b_hide(self, ctx):
        product = style.node("product", "code", size=1.5, font_size=24).move_to(LEFT * 2.4 + UP * 0.2)
        ring = style.node("moat", size=3.1).move_to(product)
        ring.set_z_index(style.Z_BACKDROP, family=True)
        hidden = label("hidden code", style.GOLD).next_to(ring, DOWN, buff=0.25)
        self.play(GrowFromCenter(ring), DrawBorderThenFill(product), FadeIn(hidden), run_time=0.9)
        self._owned["castle"] = VGroup(ring, product, hidden)
        ctx.waive("node_overlap", "the castle: a product inside its moat ring, and the clone peeling off it")
        # The clone peels off the product and walks out of the ring.
        self._at(ctx, 0.2)
        clone = style.node("clone", size=1.5).move_to(product)
        self.add(clone)
        ctx.play(clone.animate.move_to(RIGHT * 2.6 + UP * 0.2), run_time=1.0)
        self._owned["clone"] = clone
        # "Not hidden code."
        self._at(ctx, 0.62)
        # The ring is struck, not the product: the red line stops at the square's edges.
        full = style.strike(ring[1])
        a, b = full.get_start(), full.get_end()
        cross = VGroup(Line(a, product.get_corner(DL), color=style.RED, stroke_width=5),
                       Line(product.get_corner(UR), b, color=style.RED, stroke_width=5))
        ctx.play(ring.animate.set_opacity(0.4), Create(cross), run_time=0.6)
        self._owned["cross"] = cross

    def b_company(self, ctx):
        ctx.clear_stage(run_time=0.35)
        company = style.node("product", size=1.0)
        head = label("a company", style.WHITE, size="caption")
        clone = style.node("clone", size=1.0)
        top = VGroup(company, head).arrange(RIGHT, buff=0.35)
        VGroup(top, clone).arrange(RIGHT, buff=1.4).move_to(UP * 1.35)
        ctx.show(top, tag="company", run_time=0.5, nudge=False)
        ctx.show(clone, tag="clone", anim=lambda m: FadeIn(m, shift=LEFT * 0.4), run_time=0.5)
        self._at(ctx, 0.2)
        ctx.play(clone.animate.set_opacity(0.5), run_time=0.5)
        row = VGroup(*[named_hex(w, size=1.25) for w in ("relationship", "record", "responsibility")])
        row.arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(DOWN * 0.75)
        # A little ahead of each word, so the last hexagon has settled by the time it is named.
        for item, frac in zip(row, (0.33, 0.5, 0.69)):
            self._at(ctx, frac)
            self.play(FadeIn(item, scale=0.85), run_time=ctx.budget(0.5)[0])
        self._owned["row"] = row
        self._at(ctx, 0.9)
        ctx.play(*[a for item in row for a in style.highlight(item[0], style.GOLD)], run_time=0.5)

    def b_limit(self, ctx):
        row = self._owned.pop("row")
        ctx.retire("company", "clone", run_time=0.3)
        one = style.node("moat", size=2.2).move_to(UP * 0.35)
        phrase = label("connected, permitted capacity", style.GOLD, size="caption")
        phrase.next_to(one, DOWN, buff=0.3)
        # The three a company owns gather into the one shape of section 06.
        style.strip_labels(*[item[1] for item in row])
        self.play(*[item.animate.move_to(one).set_opacity(0) for item in row], GrowFromCenter(one),
                  run_time=ctx.budget(0.8)[0])
        self.remove(*row)
        ctx.show(phrase, tag="phrase", run_time=0.4, nudge=False)

        # "permission, physical capacity and connection": it splits, one per word.
        self._at(ctx, 0.4)
        parts = VGroup(*[named_hex(w, size=1.25) for w in ("permission", "physical capacity", "connection")])
        parts.arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to(DOWN * 0.45)
        shapes = [p[0] for p in parts]
        homes = [s.get_center() for s in shapes]
        for s in shapes:
            s.move_to(one)
        self.remove(one)
        self.add(*shapes)
        ctx.play(*[s.animate.move_to(h) for s, h in zip(shapes, homes)],
                 phrase.animate.move_to(UP * 1.6), run_time=0.7)
        ctx.play(*[FadeIn(p[1], shift=UP * 0.1) for p in parts], run_time=0.3)
        self._owned["parts"] = parts
        for p, frac in zip(parts, (0.58, 0.72, 0.86)):
            self._at(ctx, frac)
            ctx.play(*style.highlight(p[0], style.GOLD), run_time=0.4)

    def b_repo(self, ctx):
        ctx.clear_stage(run_time=0.35)
        head = style.mono_text("research repository", color=style.MUTED, size="label")
        folders = [folder(t) for t in ("sources/", "claims/", "video/")]    # the repository template's folder names
        listing = VGroup(*folders).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        inside = VGroup(head, listing).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        listing.shift(RIGHT * 0.5)
        inside.move_to(UP * 0.55)
        box = style.tile(inside.width + 1.6, inside.height + 0.8, style.MUTED, opacity=0.08).move_to(inside)
        box.set_z_index(style.Z_BACKDROP)
        ctx.show(VGroup(box, head), tag="repo", run_time=0.5, nudge=False)
        for i, (f, frac) in enumerate(zip(folders, (0.06, 0.2, 0.34))):
            self._at(ctx, frac)
            ctx.show(f, tag=f"folder{i}", anim=lambda m: FadeIn(m, shift=RIGHT * 0.2), run_time=0.4,
                     nudge=False)
        # "the link is on screen and in the description": the address the channel design gives this video's repository
        self._at(ctx, 0.48)    # at "on GitHub", so the address is up long enough to read (38 characters)
        link = style.mono_text(REPO_URL, color=style.WHITE, size="label").next_to(box, DOWN, buff=0.75)
        down = style.glow_arrow(box.get_bottom() + DOWN * 0.06, link.get_top() + UP * 0.12,
                                color=style.WHITE, buff=0.0)
        ctx.play(GrowArrow(down[1]), FadeIn(down[0]), FadeIn(link), run_time=0.6)
        self._owned["link"] = VGroup(down, link)
        # "Open it, and check me."
        self._at(ctx, 0.8)
        ctx.play(*style.highlight(box, style.WHITE), run_time=0.5)

    def b_fix(self, ctx):
        ctx.clear_stage(run_time=0.35)
        centre = DOWN * 0.2
        spots = [centre + 1.9 * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, -PI / 6, 7 * PI / 6)]
        # Grammar only: I do the check (the agent diamond); issue and fix are plain grey steps
        # (green is for measured figures, violet only for an agent).
        steps = [card("issue", style.MUTED), style.node("agent", "check", size=1.3, font_size=22),
                 card("fix", style.MUTED)]
        for s, p in zip(steps, spots):
            s.move_to(p)
        arrows = [curved(a, b, style.MUTED) for a, b in zip(steps, steps[1:] + steps[:1])]
        for i, (s, a) in enumerate(zip(steps, arrows)):
            self._at(ctx, 0.04 + 0.14 * i)
            ctx.show(s, tag=f"step{i}", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.4, nudge=False)
            ctx.play(Create(a), run_time=0.4)
        self._owned["arrows"] = VGroup(*arrows)
        # "in the open"
        self._at(ctx, 0.6)
        open_ = label("in the open", style.WHITE).move_to(centre)
        ctx.show(open_, tag="open", run_time=0.4, nudge=False)
        ctx.play(LaggedStart(*[a.animate.set_color(style.WHITE) for a in arrows], lag_ratio=0.5),
                 run_time=1.2)
        ctx.play(*style.highlight(steps[2][0], style.WHITE), run_time=0.4)

    def b_next(self, ctx):
        ctx.clear_stage(run_time=0.35)
        y = -0.5
        ask = label("?", style.WHITE, size="title").move_to([-5.2, y, 0])
        yours = label("your question", style.WHITE).next_to(ask, DOWN, buff=0.3)
        levi = style.node("person", "Levi", size=1.4, font_size=26).move_to([-1.8, y, 0])
        alpha = style.node("agent", "Alpha", size=1.6, font_size=26).move_to([2.6, y, 0])
        ctx.show(ask, tag="ask", anim=lambda m: FadeIn(m, scale=0.7), run_time=0.4, nudge=False)
        ctx.show(yours, tag="yours", run_time=0.4, nudge=False)
        ctx.show(levi, tag="levi", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.5, nudge=False)
        # Alpha and its label from the start: the last beat is short, and "next investigation" shown late was up
        # 2.7 s, under its reading time (gate, text_too_brief, 2026-11-10).
        nxt = label("next investigation", style.VIOLET).next_to(alpha, DOWN, buff=0.3)
        ctx.show(alpha, nxt, tag="alpha", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.4, nudge=False)
        # "ask it there too": a copy of the question goes to Levi; the
        # question and its name stay where it started, so the name is up long enough to read.
        self._at(ctx, 0.35)
        sent = ask.copy().shift(RIGHT * 0.8 + UP * 0.6)     # clear of the one that stays, above the arrow
        self._own("sent", sent)
        ctx.play(FadeIn(sent), ask.animate.set_opacity(0.5), run_time=0.3)
        # The way it goes is drawn as it travels: from the question to Levi.
        send = style.glow_arrow(ask.get_right() + RIGHT * 0.2, levi.get_left() + LEFT * 0.08,
                                color=style.WHITE, buff=0.0)
        ctx.play(sent.animate.move_to([levi.get_x(), levi.get_top()[1] + 0.55, 0]),
                 GrowArrow(send[1]), FadeIn(send[0]), run_time=0.7)
        self._owned["send"] = send
        # "Levi picks what I look into next."
        self._at(ctx, 0.66)
        picks = style.glow_arrow(levi.get_right() + RIGHT * 0.08, alpha.get_left() + LEFT * 0.08,
                                 color=style.WHITE, buff=0.0)
        ctx.play(*style.highlight(levi, style.WHITE), GrowArrow(picks[1]), FadeIn(picks[0]),
                 sent.animate.move_to([alpha.get_x(), alpha.get_top()[1] + 0.55, 0]), run_time=0.9)
        self._owned["picks"] = picks
        self._at(ctx, 0.88)
        ctx.play(*style.highlight(alpha, style.VIOLET), run_time=0.5)
