"""
Section 01: the open. The question in the first line, the stakes inside fifteen
seconds, the thesis at about thirty (notes/video-standard.md, rule 3.4).

Motion from frame one: the product draws itself while the question is spoken,
and a clone peels off it before the line ends. Then Levi and Alpha, the first
video as a hypothesis ringed by checks, the Beeper Mini case as a line, a
network and a broken link, the answer, an agenda strip and the four claim chips
(the moats video).

Every wait inside a beat is a fraction of its window (`_at`), so a re-timed
voice needs no edit.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from moats_video.pipeline import charts, stage, style
from moats_video.pipeline.beats import Beat, BeatScene


def check_mark(color: str = style.GREEN) -> VMobject:
    """A tick, drawn: a shape, not a glyph."""
    tick = VMobject(color=color, stroke_width=5)
    tick.set_points_as_corners([LEFT * 0.2 + UP * 0.02, DOWN * 0.16 + LEFT * 0.04, RIGHT * 0.24 + UP * 0.22])
    return tick


class S01Open(BeatScene):
    section_id = "01_open"
    title = ""   # the open has no title strip: the question is the first frame
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            # lead: the first beat starts on frame one, before the voice does.
            Beat("If what you ship can be rebuilt in a week", self.b_question, lead=1.0,
                 note="product draws in, a clone peels off it, a gold hexagon with a question mark"),
            Beat("Levi Purdy asked me how the next generation", self.b_pair,
                 note="Levi (person) and Alpha (agent); a question goes one way, evidence comes back"),
            Beat("This is my first video", self.b_first,
                 note="a hypothesis card; four checks land on a ring round it"),
            Beat("In December 2023, an app that rebuilt", self.b_beeper,
                 note="a line from 0 to 100,000 downloads over 48 hours; the dashed clone beside it"),
            # This line is short and its source chip long: start it in the pause before the line,
            # and the next beat a little after its line, so the chip stays up long enough to read.
            Beat("Three days after launch", self.b_blocked, lead=1.0,
                 note="a Dec 5 to Dec 8 timeline; the clone's link into iMessage turns red and breaks"),
            Beat("The code could be copied", self.b_permission, lead=-0.3,
                 note="the clone stays; a gold hexagon, permission, rises round the network"),
            Beat("Code is cheap now", self.b_cheap,
                 note="clones multiply; the question hexagon returns, alone on the right"),
            Beat("My short answer: own what a clone cannot generate", self.b_answer,
                 note="the hexagon lights; the clones stop short of it"),
            Beat("First, what a moat is", self.b_agenda,
                 note="five marks along a line, one per part the line names, each with a word"),
            Beat("Every figure is marked", self.b_marks,
                 note="the four chips the viewer will see all video"),
        ]

    def _at(self, ctx, frac: float, run_time: float = 0.6) -> float:
        """Wait until `frac` of this beat's window has passed; return `run_time` cut to what is left."""
        lag = ctx.beat.start + frac * ctx.window - self.renderer.time
        if lag > 0.02:
            self.wait(lag)
        left = ctx.beat.start + ctx.window - self.renderer.time - 0.1
        return max(min(run_time, left), 0.08)

    # ---------------------------------------------------------------- beats --
    def b_question(self, ctx):
        product = style.node("product", size=2.2)
        product.move_to(LEFT * 3.6 + UP * 0.2)
        name = style.label_text("what you ship", color=style.BLUE)
        name.next_to(product, DOWN, buff=0.3)
        a, b, c = ctx.budget(0.9, 0.9, 0.7)
        self.play(DrawBorderThenFill(product), FadeIn(name, shift=UP * 0.1), run_time=a)
        self._owned["product"] = VGroup(product, name)

        clone = style.node("clone", size=2.2).move_to(product)
        self.add(clone)
        week = style.label_text("1 week", color=style.MUTED)
        target = RIGHT * 3.6 + UP * 0.2
        arrow = style.glow_arrow(product.get_right() + RIGHT * 0.2, target + LEFT * 1.3,
                                 color=style.BLUE)
        week.next_to(arrow, UP, buff=0.22)
        self.play(clone.animate.move_to(target), GrowArrow(arrow[1]), FadeIn(arrow[0]),
                  FadeIn(week), run_time=b)
        self._owned["clone"] = VGroup(clone, arrow, week)

        ask = style.node("moat", "?", size=1.1, font_size=40)
        ask.move_to(UP * 1.75)
        ctx.show(ask, tag="ask", anim=lambda m: FadeIn(m, scale=0.8), run_time=c)
        rt = self._at(ctx, 0.75, 0.5)
        self.play(*style.highlight(ask, style.GOLD), run_time=rt)

    def b_pair(self, ctx):
        ctx.clear_stage(run_time=0.35)
        levi = style.node("person", "Levi", size=1.9, font_size=30).move_to(LEFT * 4.2 + UP * 0.6)
        alpha = style.node("agent", "Alpha", size=2.2, font_size=30).move_to(RIGHT * 4.2 + UP * 0.6)
        levi_role = style.label_text("directs, asks", color=style.WHITE).next_to(levi, DOWN, buff=0.35)
        channel = style.label_text("his own channel", color=style.MUTED).next_to(levi_role, DOWN, buff=0.3)
        alpha_role = style.label_text("researches, checks", color=style.VIOLET)
        alpha_role.next_to(alpha, DOWN, buff=0.3).set_y(levi_role.get_y())
        ctx.show(levi, alpha, tag="pair", run_time=0.6, nudge=False)
        # "Levi Purdy asked me how the next generation of startups stay alive": his question, his words.
        rt = self._at(ctx, 0.06, 0.8)
        ask = style.glow_arrow(levi.get_right() + UP * 0.35, alpha.get_left() + UP * 0.35,
                               color=style.WHITE, buff=0.1)
        ask_label = style.label_text("how do startups stay alive?", color=style.WHITE).next_to(ask, UP, buff=0.2)
        self.play(GrowArrow(ask[1]), FadeIn(ask[0]), FadeIn(ask_label), run_time=rt)
        self._owned["ask"] = VGroup(ask, ask_label)
        # "I am Alpha, the AI research agent he runs"
        ctx.play(*style.highlight(alpha, style.VIOLET), run_time=self._at(ctx, 0.28, 0.5))
        # "He directs the work and asks the questions"
        ctx.show(levi_role, tag="role", run_time=self._at(ctx, 0.45, 0.5), nudge=False)
        # "and makes his own videos on his channel"
        ctx.show(channel, tag="channel", run_time=self._at(ctx, 0.62, 0.4), nudge=False)
        # "I do the research, and I check it": the evidence goes back (after the channel, so the beat's last
        # change lands late enough that no 5 s holds still; 2026-11-10 gate, dead_air at 13 s).
        rt = self._at(ctx, 0.8, 0.7)
        back = style.glow_arrow(alpha.get_left() + DOWN * 0.25, levi.get_right() + DOWN * 0.25,
                                color=style.VIOLET, buff=0.1)
        back_label = style.label_text("evidence", color=style.VIOLET).next_to(back, DOWN, buff=0.2)
        self.play(GrowArrow(back[1]), FadeIn(back[0]), FadeIn(back_label), FadeIn(alpha_role), run_time=rt)
        self._owned["back"] = VGroup(back, back_label, alpha_role)

    def b_first(self, ctx):
        ctx.clear_stage(run_time=0.35)
        centre = UP * 0.15
        # A plain outlined card: the record card is for one sourced number.
        card = VGroup(RoundedRectangle(corner_radius=0.12, width=2.9, height=1.5, color=style.MUTED, stroke_width=3),
                      style.label_text("hypothesis", color=style.WHITE)).move_to(centre)
        ring = Circle(radius=2.0, color=style.DIM, stroke_width=2.2).move_to(centre)
        ring.set_z_index(style.Z_BACKDROP)
        self.play(FadeIn(card, scale=0.85), Create(ring), run_time=ctx.budget(0.8)[0])
        self._owned["card"] = VGroup(ring, card)
        # "It is a hypothesis about where business moats will hold"
        ctx.play(card[0].animate.set_stroke(style.WHITE, width=4), run_time=self._at(ctx, 0.3, 0.5))
        # "and I will show you how I checked it": four checks land on the ring, all of them before
        # "checked", so the ringed card holds a while before the next beat.
        ticks = VGroup()
        for i, point in enumerate(charts.ring(4, 2.0, centre, start=PI * 3 / 4)):
            tick = check_mark().move_to(point)
            self.play(FadeIn(tick, scale=1.6), run_time=self._at(ctx, 0.55 + 0.05 * i, 0.3))
            ticks.add(tick)
        self._owned["ticks"] = ticks
        ctx.play(ring.animate.set_stroke(style.GREEN, width=3, opacity=0.6), run_time=self._at(ctx, 0.8, 0.4))

    def b_beeper(self, ctx):
        ctx.clear_stage(run_time=0.35)
        plot = charts.Plot(LEFT * 5.0 + DOWN * 1.8, 6.6, 3.6, (0, 48), (0, 100000),
                           x_ticks=[(24, "1 day"), (48, "2 days")],
                           y_ticks=[(0, "0"), (100000, "100,000")])
        ctx.show(plot, tag="plot", run_time=0.8, nudge=False)
        clone = style.node("clone", size=1.7)
        name = style.label_text("Beeper Mini", color=style.BLUE).next_to(clone, DOWN, buff=0.3)
        when = style.label_text("December 2023", color=style.MUTED).next_to(name, DOWN, buff=0.2)
        beeper = VGroup(clone, name, when).move_to(RIGHT * 4.5 + UP * 0.2)
        ctx.lopsided("the clone is an aside beside the chart")
        ctx.show(beeper, tag="clone", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.7, nudge=False)
        # "was downloaded ... more than a hundred thousand times in two days"
        rt = self._at(ctx, 0.35, 3.0)
        growth = charts.line(plot, [(0, 0), (48, 100000)], color=style.GREEN)
        self.play(Create(growth), run_time=rt, rate_func=linear)
        self._owned["growth"] = growth
        end = Dot(plot.at(48, 100000), radius=0.12, color=style.GREEN)
        count = style.label_text("100,000+ downloads", color=style.WHITE)
        # Left of the end point and wholly above the plot's top edge, which would otherwise cut through it.
        count.next_to(end, LEFT, buff=0.3).set_y(end.get_y() + 0.1 + count.height / 2)
        ctx.show(VGroup(end, count), tag="count", run_time=self._at(ctx, 0.72, 0.5), nudge=False)
        ctx.play(end.animate.scale(1.6), run_time=self._at(ctx, 0.88, 0.4))

    def b_blocked(self, ctx):
        ctx.clear_stage("clone", run_time=0.35)
        beeper = self._owned["clone"]
        a, b, c = ctx.budget(0.4, 0.5, 0.75)
        self.play(beeper.animate.move_to(LEFT * 4.8 + UP * 0.6), run_time=a)
        centre = RIGHT * 2.4 + UP * 0.6
        points = [centre] + charts.ring(6, 1.1, centre, start=PI)
        nodes, links = charts.network(points, [(0, i) for i in range(1, 7)]
                                      + [(i, i % 6 + 1) for i in range(1, 7)])
        apple = style.label_text("iMessage", color=style.CYAN).move_to(centre + DOWN * 1.9)
        link = style.glow_arrow(beeper[0].get_right() + RIGHT * 0.1, nodes[1].get_left() + LEFT * 0.05,
                                color=style.CYAN, buff=0.0)
        track = Line(LEFT * 2.0 + DOWN * 1.95, RIGHT * 2.0 + DOWN * 1.95, color=style.MUTED, stroke_width=2.2)
        ticks = VGroup(*[Line(track.point_from_proportion(t) + UP * 0.1,
                              track.point_from_proportion(t) + DOWN * 0.1, color=style.MUTED, stroke_width=2.2)
                         for t in (0, 1 / 3, 2 / 3, 1)])
        start = style.label_text("Dec 5 launch", color=style.MUTED).next_to(track, LEFT, buff=0.3)
        stop = style.label_text("Dec 8 blocked", color=style.MUTED).next_to(track, RIGHT, buff=0.3)
        marker = Triangle(color=style.WHITE, fill_opacity=1).scale(0.14).rotate(PI).move_to(track.get_start() + UP * 0.22)
        ctx.lopsided("the clone, the network and a timeline do not balance")
        net = VGroup(nodes, links, apple)
        self.play(FadeIn(net), FadeIn(link), Create(track), FadeIn(ticks), FadeIn(start), FadeIn(marker),
                  run_time=b)
        self._owned["net"] = net
        self._owned["track"] = VGroup(track, ticks, start, stop, marker)
        # "Three days after launch"
        self.play(marker.animate.move_to(track.get_end() + UP * 0.22), run_time=c, rate_func=linear)
        # "Apple shut it out": the link turns red and falls back short of the network, early
        # enough that the broken link holds before the next beat.
        # A line ending at a bar, not an arrow: an arrow into empty space reads as a lost target.
        end = nodes[1].get_left() + LEFT * 1.3
        cut = VGroup(Line(beeper[0].get_right() + RIGHT * 0.1, end),
                     Line(end + UP * 0.3, end + DOWN * 0.3)).set_stroke(style.RED, width=5)
        blocked = style.label_text("blocked", color=style.RED).move_to(cut[0].get_center() + UP * 0.4)
        self.play(FadeIn(stop), FadeOut(link), Create(cut), FadeIn(blocked), run_time=self._at(ctx, 0.64, 0.35))
        self._owned["link"] = cut
        self._owned["blocked"] = blocked

    def b_permission(self, ctx):
        ctx.retire("track", "link", "blocked", run_time=0.35)
        net = self._owned["net"]
        centre = net[0][0].get_center()
        wall = style.node("moat", size=3.6).move_to(centre)
        wall.set_z_index(style.Z_BACKDROP, family=True)
        permission = style.label_text("permission", color=style.GOLD).next_to(wall, RIGHT, buff=0.25)
        # "Apple's permission to be on its network could not"
        self.play(GrowFromCenter(wall), run_time=self._at(ctx, 0.3, 1.0))
        ctx.show(permission, tag="permission", run_time=self._at(ctx, 0.3, 0.6), nudge=False)
        self._owned["wall"] = wall
        beeper = self._owned["clone"]
        # The clone is still there; it comes close and stops short of the wall.
        ctx.play(beeper.animate.shift(RIGHT * 2.6), *style.highlight(wall, style.GOLD),
                 run_time=self._at(ctx, 0.65, 1.0))

    def b_cheap(self, ctx):
        ctx.clear_stage(run_time=0.35)
        a, b = ctx.budget(0.8, 0.6)
        clones = VGroup(*[style.node("clone", size=1.15) for _ in range(6)])
        clones.arrange_in_grid(rows=2, cols=3, buff=0.4).move_to(LEFT * 3.3)
        cheap = style.label_text("cheap", color=style.MUTED)
        cheap.next_to(clones, DOWN, buff=0.3)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in clones], lag_ratio=0.15),
                  FadeIn(cheap), run_time=a)
        self._owned["clones"] = VGroup(clones, cheap)

        ask = style.node("moat", "?", size=2.4, font_size=40)
        ask.move_to(RIGHT * 3.2)
        # "So what is still expensive?"
        ctx.show(ask, tag="ask", anim=lambda m: FadeIn(m, scale=0.8), run_time=self._at(ctx, 0.4, b))

    def b_answer(self, ctx):
        moat = self._owned.pop("ask")
        hold = style.label_text("cannot be cloned", color=style.GOLD)
        hold.next_to(moat, DOWN, buff=0.3)
        a, b = ctx.budget(0.6, 0.8)
        # The question mark goes as the hexagon grows: the answer replaces it.
        style.strip_labels(moat)
        self.play(moat.animate.scale(1.08), FadeIn(hold), run_time=a)
        self._owned["moat"] = VGroup(moat, hold)
        clones, cheap = self._owned["clones"]
        # The clones push toward the hexagon and stop short of it.
        self.play(clones.animate.shift(RIGHT * 1.0), *style.highlight(moat, style.GOLD),
                  cheap.animate.shift(RIGHT * 1.0), run_time=self._at(ctx, 0.35, b))

    def b_agenda(self, ctx):
        ctx.clear_stage(run_time=0.35)
        # The five parts the line names (it skips network effects, so the strip does too).
        xs = [-4.8 + 2.4 * i for i in range(5)]
        track = Line(LEFT * 5.6, RIGHT * 5.6, color=style.DIM, stroke_width=2.2).shift(UP * 0.3)
        track.set_z_index(style.Z_BACKDROP)
        marks = []
        marks.append(style.node("moat", size=1.2))
        marks.append(style.node("clone", size=1.0))
        dead = style.node("moat", size=1.2)
        dead.set_opacity(0.4)
        marks.append(VGroup(dead, style.strike(dead)))
        marks.append(style.node("agent", size=1.3))
        pair = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.75, height=0.75, color=style.MUTED, stroke_width=2.4)
                        for _ in range(2)]).arrange(RIGHT, buff=0.2)
        marks.append(pair)
        words = ["moat", "cheap", "die", "limit", "plans"]
        items = []
        for x, mark, word in zip(xs, marks, words):
            mark.move_to(RIGHT * x + UP * 0.3)
            text = style.label_text(word, color=style.WHITE).next_to(mark, DOWN, buff=0.4)
            text.set_y(-0.95)
            items.append(VGroup(mark, text))
        self.play(Create(track), run_time=0.5)
        self._owned["agenda"] = VGroup(track, *items)
        # Each mark as the narration reaches its part: moat, cheap, die, what is
        # left when agents can do the work, then the founder and the investor.
        for item, frac in zip(items, (0.0, 0.18, 0.3, 0.45, 0.67)):
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=self._at(ctx, frac, 0.5))
        ctx.play(*style.highlight(marks[0], style.GOLD), run_time=self._at(ctx, 0.9, 0.5))

    def b_marks(self, ctx):
        ctx.clear_stage(run_time=0.35)
        chips = VGroup(*[style.claim_footer(k) for k in ("measured", "reported", "argued", "guess")])
        chips.scale(1.5).arrange_in_grid(rows=2, cols=2, buff=(1.4, 0.7), col_alignments="ll")
        chips.move_to(stage.STAGE.center)
        # "Every figure is marked: measured, reported, argued, or my own guess." Each chip just ahead of
        # its word, so all four have landed while the last is spoken.
        for chip, frac in zip(chips, (0.3, 0.42, 0.54, 0.64)):
            self.play(FadeIn(chip, scale=0.85), run_time=self._at(ctx, frac, 0.3))
