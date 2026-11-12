"""
Section 09: how this was made. The research process is the picture (the
channel's best visual), so the checking is drawn as a flow the viewer can follow:
Levi's frame gate, then my own checks for the facts in front of it; a claim
travelling through them; two errors caught and fixed; Levi's loop back to the
script; the GitHub-stars correction; and the guess that stays amber.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from moats_video.pipeline import stage, style
from moats_video.pipeline.beats import Beat, BeatScene

FLOW_Y = -0.3
FLOW_XS = [-5.2, -2.6, 0.0, 2.6, 5.2]
ABOVE_Y = 0.95   # where things travelling along the flow ride


def card(text: str, color: str = style.MUTED, w: float = 1.9, h: float = 0.95) -> VGroup:
    """A step of the process: a tile in its colour with its name inside."""
    name = style.label_text(text)
    box = style.tile(max(w, name.width + 0.7), h, color)
    name.move_to(box)
    return VGroup(box, name)


def tick(color: str = style.WHITE, size: float = 0.42) -> VMobject:
    mark = VMobject(color=color, stroke_width=5)
    mark.set_points_as_corners([LEFT * 0.5 + UP * 0.05, DOWN * 0.4 + LEFT * 0.1, RIGHT * 0.5 + UP * 0.5])
    return mark.scale(size)


def flag(text: str) -> VGroup:
    """An error caught: a red pennant on a pole, its name beside it."""
    pole = Line(DOWN * 0.28, UP * 0.28, color=style.MUTED, stroke_width=3)
    cloth = Triangle(color=style.RED).rotate(-PI / 2).scale(0.17)
    cloth.set_fill(style.RED, opacity=0.9).next_to(pole.get_top(), RIGHT, buff=0).shift(DOWN * 0.13)
    name = style.label_text(text, color=style.RED).next_to(pole, RIGHT, buff=0.42)
    return VGroup(pole, cloth, name)


class S09Method(BeatScene):
    section_id = "09_method"
    title = "How this was made"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("How I made this", self.b_flow,
                 note="Levi's frame gate checks a strip of frames; then my four fact checks line up in front of it"),
            Beat("Every claim on screen carries a tag and a source", self.b_claim,
                 note="a claim chip travels the flow; another model and a reviewer light as it reaches them"),
            Beat("On the first version, those checks caught", self.b_caught,
                 note="two red flags stop at the reviewer, then turn green: fixed"),
            Beat("Then Levi watched it and sent it back", self.b_loop,
                 note="Levi at the end of the flow; a loop back to the script carries his three questions"),
            Beat("He also caught me counting GitHub stars", self.b_stars,
                 note="a star gauge fills to 100,000 and is struck; three kept rebuilds (clones) replace it"),
            Beat("What the checks cannot prove are my guesses", self.b_guess,
                 note="three claim kinds pass into the checked zone; the guess stays outside, amber"),
        ]

    # ------------------------------------------------------------ helpers --
    def _at(self, ctx, frac: float) -> None:
        """Wait until `frac` of this beat's window has passed (never past its end)."""
        lag = ctx.beat.start + frac * ctx.window - self.renderer.time
        if lag > 0.02:
            self.wait(lag)

    def _ride(self, ctx, mob: Mobject, x: float, run_time: float = 0.8):
        ctx.play(mob.animate.move_to([x, mob.get_y(), 0]), run_time=run_time)

    # -------------------------------------------------------------- beats --
    def b_flow(self, ctx):
        # Levi's pipeline first: a gate that checks every frame of a strip.
        gate = card("frame gate", style.WHITE).move_to(UP * 0.7)
        source = style.label_text("from The Software AI Isn't Allowed To Write", color=style.MUTED)
        source.next_to(gate, UP, buff=0.3)
        frames = VGroup(*[Rectangle(width=1.0, height=0.56, color=style.MUTED, stroke_width=2.4)
                          for _ in range(6)]).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.1)
        frames.set_fill(style.PANEL_HI, opacity=0.9)
        ticks = VGroup(*[tick().move_to(f) for f in frames])
        self.play(FadeIn(gate, shift=DOWN * 0.15), FadeIn(source), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in frames], lag_ratio=0.15), run_time=1.0)
        self._at(ctx, 0.2)
        self.play(LaggedStart(*[AnimationGroup(f.animate.set_stroke(style.WHITE, width=3), Create(t))
                                for f, t in zip(frames, ticks)], lag_ratio=0.3), run_time=2.4)

        # Then my own checks for the facts, in front of it.
        self._at(ctx, 0.5)
        self.play(FadeOut(frames), FadeOut(ticks), FadeOut(source),
                  gate.animate.move_to([FLOW_XS[4], FLOW_Y, 0]), run_time=0.8)
        script = card("script", style.WHITE).move_to([FLOW_XS[0], FLOW_Y, 0])
        sources = card("sources", style.WHITE).move_to([FLOW_XS[1], FLOW_Y, 0])
        model = style.node("agent", size=1.2).move_to([FLOW_XS[2], FLOW_Y, 0])
        reviewer = style.node("agent", size=1.2).move_to([FLOW_XS[3], FLOW_Y, 0])
        model_name = style.label_text("another model", color=style.VIOLET).next_to(model, DOWN, buff=0.3)
        reviewer_name = style.label_text("reviewer", color=style.VIOLET).next_to(reviewer, DOWN, buff=0.3)
        steps = [script, sources, model, reviewer, gate]
        # Edge to edge, level: connect() aims from a card's corner when two shapes differ.
        arrows = [style.glow_arrow(a.get_right() + RIGHT * 0.06, b.get_left() + LEFT * 0.06,
                                   color=style.MUTED, buff=0.0) for a, b in zip(steps, steps[1:])]
        new = [script, sources, VGroup(model, model_name), VGroup(reviewer, reviewer_name)]
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in new], lag_ratio=0.3), run_time=1.6)
        self.play(*[GrowArrow(a[1]) for a in arrows], *[FadeIn(a[0]) for a in arrows], run_time=0.8)
        self._owned["flow"] = VGroup(*arrows, *steps, model_name, reviewer_name)
        self.steps = steps

        self._at(ctx, 0.66)
        mine = style.label_text("my checks for the facts", color=style.VIOLET)
        mine.move_to([(FLOW_XS[0] + FLOW_XS[3]) / 2, ABOVE_Y, 0])
        ctx.show(mine, tag="mine", run_time=0.6, nudge=False)

    def b_claim(self, ctx):
        script, sources, model, reviewer, _ = self.steps
        chip = card("a claim", style.MUTED).scale(0.7)   # a plain token: the real tag lives in the caption footer
        chip.move_to([FLOW_XS[0], ABOVE_Y, 0])
        ctx.show(chip, tag="chip", anim=lambda m: FadeIn(m, shift=DOWN * 0.2), run_time=0.5, nudge=False)
        # "my checks for the facts" stays until the chip rides into its place: long enough to read.
        self._at(ctx, 0.18)
        ctx.retire("mine", run_time=0.3)
        self._ride(ctx, chip, FLOW_XS[1])
        # "A model from another company reads the script against the sources"
        self._at(ctx, 0.38)
        self._ride(ctx, chip, FLOW_XS[2])
        ctx.play(*style.highlight(model, style.VIOLET), run_time=0.5)
        # "and a reviewer that did not write it checks the figures"
        self._at(ctx, 0.7)
        self._ride(ctx, chip, FLOW_XS[3])
        ctx.play(*style.highlight(reviewer, style.VIOLET), run_time=0.5)

    def b_caught(self, ctx):
        ctx.retire("chip", run_time=0.3)
        reviewer = self.steps[3]
        flags = [flag("wrong project"), flag("figure not on page")]
        for f, y in zip(flags, (ABOVE_Y + 0.55, ABOVE_Y - 0.2)):
            f.move_to([FLOW_XS[0], y, 0], aligned_edge=LEFT)
        rest = reviewer.get_x() - 0.3
        for i, f in enumerate(flags):
            self._at(ctx, 0.05 + 0.3 * i)
            ctx.show(f, tag=f"flag{i}", run_time=0.4, nudge=False)
            ctx.play(f.animate.shift(RIGHT * (rest - f.get_left()[0])), run_time=1.3)
            ctx.play(*style.highlight(reviewer, style.RED), run_time=0.4)
        # "Both were fixed before Levi saw it."
        self._at(ctx, 0.62)
        # A tick against each flag, where it stands, rather than one word off to the side.
        fixed = VGroup(*[tick(size=0.3).next_to(f, RIGHT, buff=0.3) for f in flags])
        ctx.play(*[f[1].animate.set_fill(style.WHITE).set_stroke(style.WHITE) for f in flags],
                 *[f[2].animate.set_color(style.WHITE) for f in flags],
                 *style.highlight(reviewer, style.VIOLET), FadeIn(fixed), run_time=0.7)
        self._owned["fixed"] = fixed

    def b_loop(self, ctx):
        ctx.retire("flag0", "flag1", "fixed", run_time=0.3)
        flow = self._owned["flow"]
        script, gate = self.steps[0], self.steps[4]
        ctx.play(flow.animate.scale(0.85).move_to(LEFT * 1.2 + UP * 0.25), run_time=0.9)
        levi = style.node("person", "Levi", size=1.15, font_size=22)
        levi.move_to([5.5, gate.get_y(), 0])
        watch = style.glow_arrow(gate.get_right() + RIGHT * 0.06, levi.get_left() + LEFT * 0.06,
                                 color=style.WHITE, buff=0.0)
        ctx.show(levi, tag="levi", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.5, nudge=False)
        ctx.play(GrowArrow(watch[1]), FadeIn(watch[0]), run_time=0.5)
        self._owned["watch"] = watch

        # "and sent it back": a loop under the flow, back into the script.
        self._at(ctx, 0.25)
        low = flow.get_bottom()[1] - 0.35
        corners = [levi.get_bottom() + DOWN * 0.06, [levi.get_x(), low, 0], [script.get_x(), low, 0]]
        path = VMobject(color=style.WHITE, stroke_width=3.4).set_points_as_corners(corners)
        path.set_z_index(style.Z_EDGE)
        back = style.glow_arrow([script.get_x(), low, 0], script.get_bottom() + DOWN * 0.06,
                                color=style.WHITE, buff=0.0)
        self.play(Create(path), run_time=ctx.budget(1.0)[0], rate_func=linear)
        self.play(GrowArrow(back[1]), FadeIn(back[0]), run_time=ctx.budget(0.35)[0])
        self._owned["loop"] = VGroup(path, back)

        # The three questions it came back with, each carried from Levi's end.
        asks = ["what is a moat?", "network effects?", "the limit?"]
        xs = [script.get_x() + 1.6, script.get_x() + 4.85, script.get_x() + 7.7]
        for i, (text, x, frac) in enumerate(zip(asks, xs, (0.36, 0.52, 0.68))):
            self._at(ctx, frac)
            q = style.label_text(text, color=style.WHITE).move_to([levi.get_x() - 0.9, low - 0.42, 0])
            ctx.show(q, tag=f"ask{i}", run_time=0.3, nudge=False)
            ctx.play(q.animate.move_to([x, low - 0.42, 0]), run_time=0.8)

    def b_stars(self, ctx):
        ctx.clear_stage(run_time=0.4)
        star = Star(n=5, outer_radius=0.62, color=style.WHITE).set_fill(style.WHITE, opacity=0.2)
        star.set_stroke(style.WHITE, width=2.6)
        name = style.label_text("GitHub stars", color=style.WHITE).next_to(star, DOWN, buff=0.3)
        track = style.tile(4.2, 0.38, style.DIM, opacity=0.25)
        fill = style.tile(4.2, 0.38, style.WHITE, opacity=0.55)
        count = style.label_text("100,000", color=style.WHITE)
        gauge = VGroup(VGroup(star, name), track).arrange(RIGHT, buff=0.6).move_to(UP * 0.35)
        fill.move_to(track)
        count.next_to(track, UP, buff=0.25).align_to(track, RIGHT)
        self.play(FadeIn(star, scale=0.7), FadeIn(name), FadeIn(track), run_time=0.6)
        self.play(GrowFromEdge(fill, LEFT), Rotate(star, angle=TAU, run_time=1.6), run_time=1.6)
        ctx.show(count, tag="count", run_time=0.4, nudge=False)
        stars = VGroup(star, name, track, fill, count)

        # "Stars are attention."
        self._at(ctx, 0.2)
        attention = style.label_text("attention, not use", color=style.WHITE)
        attention.next_to(track, DOWN, buff=0.35)
        cross = style.strike(star)
        ctx.play(Create(cross), FadeIn(attention), run_time=0.6)

        # "So I dropped a tool with a hundred thousand of them": the stars dim where they stand,
        # then make room for what was kept; "attention, not use" stays readable.
        self._at(ctx, 0.36)
        dropped = VGroup(stars, cross, attention)
        ctx.play(stars.animate.set_opacity(0.5), run_time=0.7)
        self._owned["dropped"] = dropped

        # "and kept only rebuilds that people used, paid for, or that an incumbent had to answer."
        # Each kept rebuild is a clone (the grammar's blue dashed square), named by what proved it.
        kept = [VGroup(style.node("clone", size=0.7), style.label_text(t)).arrange(RIGHT, buff=0.35)
                for t in ("used", "paid for", "answered by the incumbent")]
        VGroup(*kept).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(RIGHT * 3.3 + UP * 0.35)
        # A little ahead of the words, so the last card is up long enough to read.
        for i, (c, frac) in enumerate(zip(kept, (0.56, 0.64, 0.72))):
            self._at(ctx, frac)
            if i == 0:
                ctx.play(dropped.animate.shift(RIGHT * (stage.STAGE.left + 0.3 - dropped.get_left()[0])),
                         run_time=0.6)
            ctx.show(c, tag=f"kept{i}", anim=lambda m: FadeIn(m, shift=LEFT * 0.3), run_time=0.5,
                     nudge=False)

    def b_guess(self, ctx):
        ctx.clear_stage(run_time=0.4)
        checked = stage.Region("checked", 0.4, stage.STAGE.right, stage.STAGE.bottom + 0.1,
                               stage.STAGE.top - 0.1)
        zone = stage.zone(checked, "checked against sources", style.MUTED, fill_opacity=0.07)
        chips = VGroup(*[style.claim_footer(k) for k in ("measured", "reported", "argued", "guess")])
        chips.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(LEFT * 3.6 + DOWN * 0.15)
        # A short line: the three steps fit in its first half, so the ticks are whole well
        # before the guess grows on "guesses".
        t_in, t_move, t_tick = ctx.budget(0.7, 0.8, 0.5)
        self.play(FadeIn(zone), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in chips], lag_ratio=0.2),
                  run_time=t_in)
        self._owned["zone"] = zone
        self._owned["chips"] = chips
        # Three kinds pass into the checked zone; the guess stays outside.
        into = checked.center[0] - 1.2 - chips[0].get_left()[0]
        self.play(LaggedStart(*[c.animate.shift(RIGHT * into) for c in chips[:3]], lag_ratio=0.2),
                  run_time=t_move)
        marks = VGroup(*[tick().next_to(c, RIGHT, buff=0.35) for c in chips[:3]])
        self.play(*[Create(m) for m in marks], run_time=t_tick)
        self._owned["marks"] = marks
        self._at(ctx, 0.5)
        guess = chips[3]
        ctx.play(guess.animate.scale(1.25).move_to([guess.get_x(), chips[1].get_y(), 0]), run_time=0.6)
