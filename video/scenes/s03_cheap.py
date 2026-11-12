"""
Section 03: what got cheap, and how fast.

Four charts carry the measurements: a dumbbell of token prices (2023 to 2026), the
ARC cost-per-task scatter whose pareto frontier moves to the top-left corner, a
fan of Epoch's price declines, and METR's task-length plot on a log axis. Then the
Cloudflare/Vercel case as a gantt bar and a timeline, and what did not get cheap.
Every plotted point is from the storyboard's data list (S50, S24, S52).
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from moats_video.pipeline import charts, stage, style
from moats_video.pipeline.beats import Beat, BeatScene

# ARC-AGI-1 leaderboard (S50, read 2026-11-08): (cost per task in $, score in %).
ARC_EARLY = [
    (0.05, 4.5),     # GPT-4o, 2024-11
    (200, 75.7),     # o3-preview, 2024-12
    (0.50, 60.8),    # o3 High, 2025-04
    (0.509, 65.7),   # GPT-5 High, 2025-08
    (0.493, 75.0),   # Gemini 3 Pro, 2025-11
    (0.96, 86.2),    # GPT-5.2 XHigh, 2025-12
]
O3_PREVIEW, GEMINI_3_PRO = 1, 4
ARC_2026 = [
    (44.26, 87.5),   # Gemini 3 Deep Think preview, 2026-02
    (7.171, 96.0),   # Gemini 3 Deep Think, 2026-02
    (0.012, 84.0),   # DeepSeek V4 Flash Low, 2026-07
    (0.12, 95.5),    # Gemini 3.7 Flash High, 2026-08
    (0.047, 93.5),   # GPT-6.1 Sol Low, 2026-09
    (0.059, 98.5),   # GPT-6.1 Sol High, 2026-09
    (0.158, 98.5),   # Claude Opus 5.5 High, 2026-09
]
SOL_HIGH = 5

TOP_Y = 1.05        # the product row of the Cloudflare beats
NAME_Y = -0.3       # names under that row, low enough to clear the trust ring
LOW_Y = -1.45       # the gantt and timeline row


class S03Cheap(BeatScene):
    section_id = "03_cheap"
    title = "What got cheap"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("First, what got cheap, and how fast", self.b_tag,
                 note="a price tag swings in"),
            Beat("Start with the price of text", self.b_tokens,
                 note="a word in tokens; a dumbbell of two rows, GPT-4 at $30 read and $60 written"),
            Beat("GPT-6.1 Sol, from this September", self.b_sol,
                 note="the dots slide to $2 and $10; the bars turn green: ÷15 and ÷6"),
            Beat("That understates it, because the models also got far better", self.b_arc_axes,
                 note="the dumbbell goes; the empty ARC plot draws in"),
            Beat("Put every AI model on one chart", self.b_cloud,
                 note="the 2024-2025 dots fade in, cost axis then score axis lit"),
            Beat("The pareto frontier is the edge of that cloud", self.b_frontier,
                 note="the frontier draws; dots below it dim"),
            Beat("In December 2024, the first model to score", self.b_o3,
                 note="o3-preview lights: $200 · 76%, at today's prices; a 76% guide"),
            Beat("Eleven months later, another model scored", self.b_gemini,
                 note="Gemini 3 Pro lights: $0.49 · 75%; the guide becomes an arrow, ÷400"),
            Beat("By September 2026 the frontier reached", self.b_2026,
                 note="2026 dots; the frontier redraws to $0.06 · 98%; the old one dashed"),
            Beat("That is one test. Across many, Epoch AI", self.b_fan,
                 note="a fan on a log axis: ÷9, ÷50 median, ÷900 in a year"),
            Beat("The best models are not getting cheaper", self.b_same,
                 note="flagship price flat, same-ability price falling"),
            Beat("And the tasks got longer", self.b_metr,
                 note="METR plot, log task length; 50 min in early 2025"),
            Beat("A model tested in March 2026 reached at least sixteen hours", self.b_metr16,
                 note="16 h, its interval as a whisker, 'at least'; the points joined"),
            Beat("So a rebuild is now a task", self.b_linear,
                 note="Linear, twenty prompts, the clone; 2 evenings · $200/month"),
            Beat("In February 2026, Cloudflare said", self.b_cloudflare,
                 note="Next.js, its clone, an engineer with AI; a gantt bar under a week; coins"),
            Beat("Two days later, the CEO of Vercel", self.b_vercel,
                 note="timeline Feb 24 to Feb 26; seven red marks on the clone; migrate back"),
            Beat("The code was copyable; the trust was not", self.b_trust,
                 note="a gold ring rises round the original only"),
            Beat("Five small firms told The Information", self.b_firms,
                 note="Salesforce and HubSpot, five own-built tools; a 40 to 80% cost-cut band"),
            Beat("What got cheap is work with a checkable answer", self.b_checkable,
                 note="two task cards with green ticks"),
            Beat("What did not get cheap is deciding what to build", self.b_costly,
                 note="three gold hexagons: decide, prove, keep running"),
        ]

    # ------------------------------------------------------------ helpers --
    def _at(self, ctx, frac: float) -> None:
        """Wait until `frac` of this beat's window has passed (never past its end)."""
        lag = ctx.beat.start + frac * ctx.window - self.renderer.time
        if lag > 0.02:
            self.wait(lag)

    def _titles(self, plot: charts.Plot, x_title: str, y_title: str) -> VGroup:
        """
        Axis titles at label size, and the plot's tick labels raised to it: at Plot's tiny size the word
        gaps of "4 h" or "a year on" merge (words_merged). The y title sits above its axis, ending at it,
        so the plot's top-left stays free for data.
        """
        k = style.TYPE["label"] / style.TYPE["tiny"]
        for t in plot.labels:
            t.scale(k, about_edge=UP if t.get_center()[1] < plot.origin[1] else RIGHT)
        titles = VGroup()
        if x_title:
            xt = style.label_text(x_title, color=style.MUTED)
            corner = plot.origin + RIGHT * plot.w
            titles.add(xt.next_to(corner, UP, buff=0.2).align_to(corner, RIGHT))
        if y_title:
            yt = style.label_text(y_title, color=style.MUTED)
            yt.next_to(plot.origin + UP * plot.h, UP, buff=0.3).align_to(plot.origin + RIGHT * 0.3, RIGHT)
            titles.add(yt.shift(RIGHT * max(stage.STAGE.left + 0.12 - yt.get_left()[0], 0)))
        return titles

    def _chart(self, ctx) -> None:
        ctx.lopsided("a chart spanning the stage: its axes and lines carry no area in the balance check, "
                     "so the claim footer outweighs them")

    # -------------------------------------------------------- token prices --
    def b_tag(self, ctx):
        tag = Polygon([-0.6, 0.55, 0], [0, 1.05, 0], [0.6, 0.55, 0], [0.6, -1.0, 0], [-0.6, -1.0, 0],
                      color=style.GREEN, stroke_width=3)
        tag.set_fill(interpolate_color(ManimColor(style.PANEL), ManimColor(style.GREEN), 0.18),
                     opacity=0.96)
        hole = Circle(radius=0.1, color=style.GREEN, stroke_width=2.4).move_to([0, 0.62, 0])
        dollar = style.label_text("$", color=style.WHITE, size="title").move_to([0, -0.15, 0])
        price = VGroup(tag, hole, dollar).shift(DOWN * 0.15)
        pivot = hole.get_center()
        string = Line(pivot, pivot + UP * 1.35, color=style.MUTED, stroke_width=2.2)
        price.rotate(-0.7, about_point=pivot)
        a, b, c, d = ctx.budget(0.4, 0.5, 0.45, 0.4)
        self.play(Create(string), FadeIn(price), run_time=a)
        self.play(Rotate(price, 1.05, about_point=pivot), run_time=b)
        self.play(Rotate(price, -0.55, about_point=pivot), run_time=c)
        self.play(Rotate(price, 0.2, about_point=pivot), run_time=d)
        self._owned["tag"] = VGroup(string, price)

    def b_tokens(self, ctx):
        ctx.clear_stage(run_time=0.35)
        # A word cut into the pieces a model charges for.
        chips = VGroup()
        for piece in ("under", "standing"):
            word = style.mono_text(piece, color=style.WHITE, size="label")
            box = style.tile(word.width + 0.36, 0.5, style.CYAN, opacity=0.14).move_to(word)
            chips.add(VGroup(box, word))
        self._chart(ctx)
        chips.arrange(RIGHT, buff=0.12).move_to(UP * 0.3)
        whole = style.mono_text("understanding", color=style.WHITE, size="label").move_to(chips)
        self.play(FadeIn(whole), run_time=ctx.budget(0.5)[0])
        self._at(ctx, 0.22)
        self.play(ReplacementTransform(whole, chips), run_time=ctx.budget(0.7)[0])

        plot = charts.Plot([-3.0, -1.7, 0], 8.6, 3.0, (1, 100), (0, 3), x_log=True,
                           x_ticks=[(1, "$1"), (10, "$10"), (100, "$100")],
                           y_ticks=[(2, "read"), (1, "written")])
        titles = self._titles(plot, "$ per million tokens · log scale", "")
        self._dumb = plot
        # After "a piece of a word" the tokens have made their point: they go as the chart comes.
        self._at(ctx, 0.36)
        self.play(FadeOut(chips, shift=UP * 0.2), run_time=ctx.budget(0.4)[0])
        ctx.show(plot, titles, tag="dumbbell",
                 anim=lambda m: AnimationGroup(Create(plot.axes), FadeIn(plot.labels), FadeIn(titles)),
                 run_time=0.9, nudge=False)
        who = style.label_text("GPT-4 · Mar 2023", color=style.WHITE)
        who.move_to([3.6, 1.95, 0])
        # A list price is data (green); a white circle is Levi.
        self._old = VGroup(Dot(plot.at(30, 2), radius=0.13, color=style.GREEN),
                           Dot(plot.at(60, 1), radius=0.13, color=style.GREEN))
        self._old_values = VGroup(*[style.label_text(v, color=style.WHITE, size="tiny")
                                    .next_to(d, UP, buff=0.16) for v, d in zip(("$30", "$60"), self._old)])
        self._at(ctx, 0.45)
        self.play(FadeIn(who), FadeIn(self._old[0], scale=0.5), FadeIn(self._old_values[0]),
                  run_time=ctx.budget(0.6)[0])
        self._at(ctx, 0.62)
        self.play(FadeIn(self._old[1], scale=0.5), FadeIn(self._old_values[1]),
                  run_time=ctx.budget(0.6)[0])
        self._owned["dumbbell"].add(who, self._old, self._old_values)

    def b_sol(self, ctx):
        self._chart(ctx)
        plot = self._dumb
        who =style.label_text("GPT-6.1 Sol · Sep 2026", color=style.GREEN)
        who.move_to([-2.4, 1.95, 0])
        new = VGroup(*[d.copy() for d in self._old])
        targets = [plot.at(2, 2), plot.at(10, 1)]
        values = VGroup(*[style.label_text(v, color=style.GREEN, size="tiny")
                          .next_to(p, UP, buff=0.16 + 0.13) for v, p in zip(("$2", "$10"), targets)])
        self.add(new)
        self.play(FadeIn(who),
                  *[d.animate.move_to(p).set_color(style.GREEN) for d, p in zip(new, targets)],
                  self._old.animate.set_color(style.MUTED), self._old_values.animate.set_opacity(0.6),
                  run_time=ctx.budget(1.2)[0])
        self.play(FadeIn(values), run_time=ctx.budget(0.4)[0])
        self._at(ctx, 0.45)
        bars = VGroup(*[Line(n.get_center(), o.get_center(), color=style.GREEN, stroke_width=7)
                        .set_stroke(opacity=0.55).set_z_index(style.Z_EDGE)
                        for n, o in zip(new, self._old)])
        drops = VGroup(*[style.label_text(t, color=style.GREEN)
                         .next_to(b, UP, buff=0.14) for t, b in zip(("÷15", "÷6"), bars)])
        self.play(*[Create(b) for b in bars], run_time=ctx.budget(0.9)[0])
        self._at(ctx, 0.65)
        self.play(FadeIn(drops, shift=UP * 0.1), run_time=ctx.budget(0.5)[0])
        self._owned["dumbbell"].add(who, new, values, bars, drops)

    # ------------------------------------------------------------ ARC plot --
    def b_arc_axes(self, ctx):
        self._chart(ctx)
        self._at(ctx, 0.05)
        # Dims in place: shrunk to half, its axis title's word gaps read as merged (1080p30 gate).
        self.play(self._owned["dumbbell"].animate.set_opacity(0.15),
                  run_time=ctx.budget(0.8)[0])
        self._at(ctx, 0.35)
        ctx.clear_stage(run_time=0.3)
        plot = charts.Plot([-4.6, -1.75, 0], 9.6, 3.6, (0.01, 1000), (0, 100), x_log=True,
                           x_ticks=[(0.01, "1¢"), (0.1, "10¢"), (1, "$1"), (10, "$10"),
                                    (100, "$100"), (1000, "$1,000")],
                           y_ticks=[(25, "25%"), (50, "50%"), (75, "75%"), (100, "100%")])
        self._arc, self._arc_titles = plot, self._titles(plot, "cost per task · log scale",
                                                         "score on ARC-AGI-1")
        self.play(Create(plot.axes), run_time=ctx.budget(0.8)[0])
        self.play(FadeIn(plot.labels), FadeIn(self._arc_titles), run_time=ctx.budget(0.6)[0])
        self._owned["arc"] = VGroup(plot, self._arc_titles)

    def b_cloud(self, ctx):
        self._chart(ctx)
        xt, yt = self._arc_titles
        self.play(*style.highlight(xt, style.WHITE), run_time=ctx.budget(0.5)[0])
        self._at(ctx, 0.2)
        self._early = charts.dots(self._arc, ARC_EARLY)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in self._early], lag_ratio=0.25),
                  run_time=ctx.budget(1.6)[0])
        self._owned["arc"].add(self._early)
        self._at(ctx, 0.55)
        self.play(xt.animate.set_color(style.MUTED), yt.animate.set_color(style.WHITE),
                  run_time=ctx.budget(0.5)[0])

    def b_frontier(self, ctx):
        self._chart(ctx)
        xt, yt = self._arc_titles
        self.play(yt.animate.set_color(style.MUTED), run_time=ctx.budget(0.3)[0])
        self._front = charts.frontier(self._arc, ARC_EARLY)
        self.play(Create(self._front), run_time=ctx.budget(1.6)[0])
        self._owned["arc"].add(self._front)
        self._at(ctx, 0.5)
        edge = charts.pareto(ARC_EARLY)
        self.play(*[d.animate.set_opacity(0.3) for d, p in zip(self._early, ARC_EARLY)
                    if p not in edge], run_time=ctx.budget(0.7)[0])

    def b_o3(self, ctx):
        self._chart(ctx)
        dot = self._early[O3_PREVIEW]
        # The $0.49 dot is the next beat's: ghost it until the narration reaches it.
        self.play(dot.animate.set_opacity(1).scale(1.5),
                  self._early[GEMINI_3_PRO].animate.set_opacity(0.2), run_time=ctx.budget(0.5)[0])
        value = style.label_text("$200 · 76%", color=style.WHITE).next_to(dot, DOWN, buff=0.22)
        self._at(ctx, 0.12)
        ctx.show(value, tag="o3", run_time=0.5, nudge=False)
        self._at(ctx, 0.5)
        when = style.label_text("Dec 2024, at today's prices", color=style.MUTED)
        when.next_to(value, DOWN, buff=0.2)
        self.play(FadeIn(when), run_time=ctx.budget(0.5)[0])
        self._owned["o3"] = VGroup(value, when)
        self._at(ctx, 0.75)
        # The same score, read across: a dashed guide back to the score axis.
        self._guide = DashedLine(dot.get_left() + LEFT * 0.12, self._arc.at(0.01, 75.7),
                                 color=style.MUTED, stroke_width=2.2, dash_length=0.12)
        self._guide.set_z_index(style.Z_BACKDROP)
        self.play(Create(self._guide), run_time=ctx.budget(1.0)[0])

    def b_gemini(self, ctx):
        self._chart(ctx)
        dot, o3 = self._early[GEMINI_3_PRO], self._early[O3_PREVIEW]
        self.play(dot.animate.set_opacity(1).scale(1.5), FadeOut(self._guide), run_time=ctx.budget(0.5)[0])
        arrow = style.glow_arrow(o3.get_left() + LEFT * 0.05, dot.get_right() + RIGHT * 0.08,
                                 color=style.GREEN, buff=0.0)
        self.play(GrowArrow(arrow[1]), FadeIn(arrow[0]), run_time=ctx.budget(1.2)[0])
        self._at(ctx, 0.35)
        value = style.label_text("$0.49 · 75%", color=style.WHITE).next_to(dot, LEFT, buff=0.2)
        value.shift(UP * 0.12)
        self.play(FadeIn(value), run_time=ctx.budget(0.4)[0])
        drop = style.label_text("÷400", color=style.GREEN, size="caption").next_to(arrow, UP, buff=0.18)
        self._at(ctx, 0.7)
        self.play(FadeIn(drop, shift=UP * 0.1), run_time=ctx.budget(0.5)[0])
        self._owned["gemini"] = VGroup(value, arrow, drop)

    def b_2026(self, ctx):
        self._chart(ctx)
        ghost = DashedVMobject(self._front.copy(), num_dashes=40).set_stroke(style.MUTED, opacity=0.5)
        ghost.set_z_index(style.Z_EDGE)
        self.play(FadeOut(self._owned.pop("o3")), FadeOut(self._owned.pop("gemini")),
                  self._early[O3_PREVIEW].animate.scale(1 / 1.5).set_opacity(0.3),
                  self._early[GEMINI_3_PRO].animate.scale(1 / 1.5).set_opacity(0.3),
                  self._early[5].animate.set_opacity(0.3), self._early[0].animate.set_opacity(0.3),
                  ReplacementTransform(self._front, ghost), run_time=ctx.budget(0.6)[0])
        self._owned["arc"].add(ghost)
        late = charts.dots(self._arc, ARC_2026)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in late], lag_ratio=0.2),
                  run_time=ctx.budget(1.4)[0])
        self._at(ctx, 0.4)
        front = charts.frontier(self._arc, ARC_EARLY + ARC_2026)
        self.play(Create(front), run_time=ctx.budget(0.9)[0])
        self._at(ctx, 0.62)
        best = late[SOL_HIGH]
        value = style.label_text("$0.06 · 98%", color=style.WHITE).next_to(best, UP, buff=0.14)
        value.align_to(best, LEFT)
        self.play(best.animate.scale(1.5), FadeIn(value), run_time=ctx.budget(0.7)[0])
        self._owned["arc"].add(late, front, value)

    # ---------------------------------------------------------- the trends --
    def b_fan(self, ctx):
        self._chart(ctx)
        ctx.clear_stage(run_time=0.4)
        plot = charts.Plot([-4.4, -1.75, 0], 7.4, 3.6, (0, 1), (0.0005, 1), y_log=True,
                           x_ticks=[(0, "today"), (1, "a year on")],
                           y_ticks=[(1, "×1"), (0.1, "÷10"), (0.01, "÷100"), (0.001, "÷1,000")])
        # "price at", not "price of": the f's overhang narrows the word gap below the gate's minimum.
        ytitle = self._titles(plot, "", "price at a fixed performance · log scale")
        self.play(Create(plot.axes), FadeIn(plot.labels), FadeIn(ytitle), run_time=ctx.budget(0.8)[0])
        self._owned["fan"] = VGroup(plot, ytitle)
        self._at(ctx, 0.25)
        start = plot.at(0, 1)
        band = Polygon(start, plot.at(1, 1 / 9), plot.at(1, 1 / 900), stroke_width=0)
        band.set_fill(style.GREEN, opacity=0.12).set_z_index(style.Z_BACKDROP)
        ends, names = [], []
        for k, color in ((9, style.GREEN), (900, style.GREEN)):
            ends.append(charts.line(plot, [(0, 1), (1, 1 / k)], color=color))
            names.append(style.label_text(f"÷{k}", color=color).next_to(plot.at(1, 1 / k), RIGHT, buff=0.2))
        self.play(*[Create(e) for e in ends], FadeIn(band), run_time=ctx.budget(1.6)[0])
        self.play(*[FadeIn(n) for n in names], run_time=ctx.budget(0.4)[0])
        self._at(ctx, 0.62)
        median = charts.line(plot, [(0, 1), (1, 1 / 50)], color=style.WHITE)
        mname = style.label_text("÷50 median", color=style.WHITE).next_to(plot.at(1, 1 / 50), RIGHT, buff=0.2)
        self.play(Create(median), run_time=ctx.budget(1.0)[0])
        self.play(FadeIn(mname), run_time=ctx.budget(0.4)[0])
        self._owned["fan"].add(band, *ends, *names, median, mname)

    def b_same(self, ctx):
        self._chart(ctx)
        ctx.clear_stage(run_time=0.3)
        plot = charts.Plot([-3.6, -1.6, 0], 7.0, 3.3, (0, 1), (0, 1))
        price = self._titles(plot, "", "price")
        time = style.label_text("time", color=style.MUTED)
        time.next_to(plot.origin + RIGHT * plot.w, DOWN, buff=0.2).align_to(plot.origin + RIGHT * plot.w, RIGHT)
        best = charts.line(plot, [(0, 0.8), (1, 0.8)], color=style.WHITE)
        same = charts.line(plot, [(0, 0.8), (0.35, 0.42), (0.7, 0.2), (1, 0.08)], color=style.GREEN)
        nb = style.label_text("best models", color=style.WHITE).next_to(plot.at(1, 0.8), RIGHT, buff=0.2)
        ns = style.label_text("same ability", color=style.GREEN).next_to(plot.at(1, 0.08), RIGHT, buff=0.2)
        self.play(Create(plot.axes), FadeIn(price), FadeIn(time), FadeIn(nb), FadeIn(ns),
                  run_time=ctx.budget(0.6)[0])
        self.play(Create(best), Create(same), run_time=ctx.budget(1.4)[0], rate_func=linear)
        self._owned["same"] = VGroup(plot, price, time, best, same, nb, ns)

    def _metr_plot(self) -> VGroup:
        """METR's time horizon (S52): task length a model finishes half the time, log, 10 min to 64 h."""
        plot = charts.Plot([-4.2, -1.75, 0], 8.8, 3.6, (2024.9, 2026.5), (10, 3840), y_log=True,
                           x_ticks=[(2025, "2025"), (2026, "2026")],
                           y_ticks=[(10, "10 min"), (60, "1 h"), (240, "4 h"), (960, "16 h"),
                                    (3840, "64 h")])
        self._metr = plot
        return VGroup(plot, self._titles(plot, "", "task length for a person, at 50% success · log scale"))

    def b_metr(self, ctx):
        self._chart(ctx)
        ctx.clear_stage(run_time=0.35)
        figure = self._metr_plot()
        plot = self._metr
        self.play(Create(plot.axes), run_time=ctx.budget(0.7)[0])
        self.play(FadeIn(plot.labels), FadeIn(figure[1]), run_time=ctx.budget(0.5)[0])
        self._owned["metr"] = figure
        self._at(ctx, 0.45)
        self._p1 = Dot(plot.at(2025.15, 50), radius=0.12, color=style.GREEN)
        name = style.label_text("50 min", color=style.GREEN).next_to(self._p1, DOWN, buff=0.22)
        self.play(FadeIn(self._p1, scale=0.4), run_time=ctx.budget(0.5)[0])
        self.play(FadeIn(name), run_time=ctx.budget(0.4)[0])
        self._at(ctx, 0.7)
        guide = DashedLine(self._p1.get_left(), plot.at(2025, 50), color=style.MUTED,
                           stroke_width=2, dash_length=0.1).set_z_index(style.Z_BACKDROP)
        self.play(Create(guide), run_time=ctx.budget(0.6)[0])
        self._owned["metr"].add(self._p1, name, guide)

    def b_metr16(self, ctx):
        self._chart(ctx)
        plot = self._metr
        p2 = Dot(plot.at(2026.2, 960), radius=0.12, color=style.GREEN)
        lo, hi = plot.at(2026.2, 510), plot.at(2026.2, 3300)   # its interval, 8.5 to 55 h
        whisker = VGroup(Line(lo, hi), Line(lo + LEFT * 0.12, lo + RIGHT * 0.12),
                         Line(hi + LEFT * 0.12, hi + RIGHT * 0.12)).set_stroke(style.MUTED, width=2.4)
        whisker.set_z_index(style.Z_BACKDROP)
        join = Line(self._p1.get_center(), p2.get_center(), color=style.GREEN, stroke_width=3.4)
        join.set_z_index(style.Z_EDGE)
        self.play(FadeIn(p2, scale=0.4), run_time=ctx.budget(0.5)[0])
        self.play(Create(join), run_time=ctx.budget(0.8)[0])
        self._at(ctx, 0.35)
        up = Triangle(color=style.GREEN).set_fill(style.GREEN, opacity=0.9).scale(0.14)
        up.next_to(p2, RIGHT, buff=0.35).shift(UP * 0.12)
        shaft = Line(up.get_bottom() + DOWN * 0.4, up.get_bottom(), color=style.GREEN, stroke_width=3)
        least = style.label_text("at least 16 h", color=style.GREEN).next_to(up, RIGHT, buff=0.22)
        least.align_to(p2, DOWN)
        self.play(Create(whisker), FadeIn(up), Create(shaft), FadeIn(least), run_time=ctx.budget(0.8)[0])
        self._owned["metr"].add(p2, whisker, join, up, shaft, least)

    # ------------------------------------------------------------ rebuilds --
    def b_linear(self, ctx):
        ctx.clear_stage(run_time=0.35)
        ctx.lopsided("the pair builds left to right: original, prompts, then the rebuild")
        product = style.node("product", size=2.0).move_to(LEFT * 4.6 + UP * 0.5)
        clone = style.node("clone", size=2.0).move_to(RIGHT * 4.6 + UP * 0.5)
        pname = style.label_text("Linear", color=style.BLUE).next_to(product, DOWN, buff=0.3)
        cname = style.label_text("the clone", color=style.BLUE).next_to(clone, DOWN, buff=0.3)
        self.play(FadeIn(product, scale=0.9), FadeIn(pname), run_time=ctx.budget(0.6)[0])
        self._at(ctx, 0.18)
        # A prompt is a small message card, not a dot: a white circle is Levi in this video's grammar.
        prompts = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.34, height=0.22)
                           .set_stroke(style.DIM, width=2).set_fill(style.PANEL_HI, opacity=0.96)
                           for _ in range(20)])
        prompts.arrange_in_grid(rows=2, cols=10, buff=(0.14, 0.22)).move_to(UP * 0.5)
        count = style.label_text("20 prompts", color=style.WHITE).next_to(prompts, DOWN, buff=0.35)
        self.add(prompts)
        self.play(LaggedStart(*[p.animate.set_stroke(style.WHITE) for p in prompts], lag_ratio=0.15),
                  run_time=ctx.budget(max(ctx.window * 0.3, 1.5))[0])
        self.play(FadeIn(count), run_time=ctx.budget(0.4)[0])
        self._at(ctx, 0.55)
        self.play(FadeIn(clone, shift=LEFT * 0.4), FadeIn(cname), run_time=ctx.budget(0.7)[0])
        self._at(ctx, 0.6)
        cost = style.label_text("2 evenings · $200/month", color=style.WHITE)
        cost.next_to(count, DOWN, buff=0.3)
        self.play(FadeIn(cost, shift=UP * 0.1), run_time=ctx.budget(0.5)[0])
        self._owned["linear"] = VGroup(product, clone, pname, cname, prompts, count, cost)

    def b_cloudflare(self, ctx):
        ctx.clear_stage(run_time=0.35)
        ctx.lopsided("the case builds left to right: the original, who rebuilt it, then the rebuild")
        product = style.node("product", size=1.3).move_to([-4.4, TOP_Y, 0])
        pname = style.label_text("Next.js", color=style.BLUE).move_to([-4.4, NAME_Y, 0])
        self.play(FadeIn(product, scale=0.9), FadeIn(pname), run_time=ctx.budget(0.5)[0])
        self._product = product
        self._owned["next"] = VGroup(product, pname)
        # One engineer, directing AI. Named in words: a white circle is Levi in this video's grammar.
        self._at(ctx, 0.15)
        agent = style.node("agent", size=0.7).move_to([0.45, TOP_Y + 0.8, 0])
        person = style.label_text("1 engineer", color=style.WHITE).next_to(agent, LEFT, buff=0.3)
        self.play(FadeIn(person, scale=0.8), FadeIn(agent, scale=0.8), run_time=ctx.budget(0.5)[0])
        self._at(ctx, 0.3)
        clone = style.node("clone", size=1.3).move_to([4.4, TOP_Y, 0])
        cname = style.label_text("Cloudflare's rebuild", color=style.BLUE).move_to([4.4, NAME_Y, 0])
        arrow = style.glow_arrow(product.get_right() + RIGHT * 0.2, clone.get_left() + LEFT * 0.2,
                                 color=style.BLUE, buff=0.0)
        self.play(GrowArrow(arrow[1]), FadeIn(arrow[0]), run_time=ctx.budget(0.8)[0])
        self.play(FadeIn(clone, shift=LEFT * 0.3), FadeIn(cname), run_time=ctx.budget(0.6)[0])
        self._clone = clone
        self._owned["clone"] = VGroup(clone, cname)
        self._owned["build"] = VGroup(person, agent, arrow)
        # Under a week, on a day axis.
        self._at(ctx, 0.55)
        day = 0.8
        x0 = -4.4 - 0.65
        axis = Line([x0, LOW_Y, 0], [x0 + 7 * day, LOW_Y, 0], color=style.MUTED, stroke_width=2.2)
        ticks = VGroup(*[Line([x0 + i * day, LOW_Y - 0.08, 0], [x0 + i * day, LOW_Y + 0.08, 0],
                              color=style.MUTED, stroke_width=2) for i in range(8)])
        week = style.label_text("1 week", color=style.MUTED)
        week.next_to(ticks[-1], DOWN, buff=0.16)
        bar = style.tile(6 * day, 0.46, style.VIOLET, opacity=0.35)
        bar.move_to([x0, LOW_Y + 0.38, 0], aligned_edge=LEFT + DOWN).shift(DOWN * 0.15)
        under = style.label_text("under a week", color=style.WHITE).move_to(bar)
        self.play(Create(axis), Create(ticks), FadeIn(week), run_time=ctx.budget(0.5)[0])
        self.play(GrowFromEdge(bar, LEFT), run_time=ctx.budget(1.0)[0])
        self.play(FadeIn(under), run_time=ctx.budget(0.3)[0])
        # "for about eleven hundred dollars in tokens"
        self._at(ctx, 0.76)
        coins = VGroup()
        for i in range(6):
            coin = Ellipse(width=1.0, height=0.3, color=style.GREEN, stroke_width=2.2)
            coin.set_fill(interpolate_color(ManimColor(style.PANEL), ManimColor(style.GREEN), 0.25),
                          opacity=1).move_to([3.0, LOW_Y - 0.25 + 0.13 * i, 0])
            coins.add(coin)
        tokens = style.label_text("$1,100 in tokens", color=style.WHITE).next_to(coins, RIGHT, buff=0.3)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in coins], lag_ratio=0.2),
                  FadeIn(tokens), run_time=ctx.budget(0.9)[0])
        self._owned["cost"] = VGroup(axis, ticks, week, bar, under, coins, tokens)

    def b_vercel(self, ctx):
        ctx.clear_stage("next", "clone", run_time=0.4)
        a, b = -2.4, 2.4
        line = Line([a - 0.6, LOW_Y, 0], [b + 0.6, LOW_Y, 0], color=style.MUTED, stroke_width=2.2)
        stops = VGroup(Dot([a, LOW_Y, 0], radius=0.1, color=style.WHITE),
                       Dot([b, LOW_Y, 0], radius=0.1, color=style.RED))
        dates = VGroup(style.label_text("Feb 24", color=style.WHITE).next_to(stops[0], DOWN, buff=0.2),
                       style.label_text("Feb 26", color=style.WHITE).next_to(stops[1], DOWN, buff=0.2))
        what = VGroup(style.label_text("rebuild announced", color=style.MUTED).next_to(stops[0], UP, buff=0.2),
                      style.label_text("7 flaws found", color=style.RED).next_to(stops[1], UP, buff=0.2))
        self.play(Create(line), FadeIn(stops[0]), FadeIn(dates[0]), FadeIn(what[0]),
                  run_time=ctx.budget(0.6)[0])
        self._at(ctx, 0.12)
        self.play(FadeIn(stops[1], scale=0.5), FadeIn(dates[1]), run_time=ctx.budget(0.5)[0])
        self._owned["timeline"] = VGroup(line, stops, dates, what)
        # "said it had found seven security flaws in that rebuild": seven marks land on the clone, a little ahead
        # of the words, so the timeline alone (low on the stage) does not hold for 2.5 s (gate, stage_imbalance).
        self._at(ctx, 0.22)
        c = self._clone.get_center()
        spots = [(-0.35, 0.35), (0.3, 0.38), (0.0, 0.08), (-0.38, -0.12), (0.36, -0.08),
                 (-0.12, -0.38), (0.24, -0.4)]
        marks = VGroup()
        for dx, dy in spots:
            p = c + np.array([dx, dy, 0])
            marks.add(VGroup(Line(p + UL * 0.09, p + DR * 0.09), Line(p + DL * 0.09, p + UR * 0.09))
                      .set_stroke(style.RED, width=4))
        self.play(FadeIn(what[1]), LaggedStart(*[FadeIn(m, shift=DOWN * 0.4) for m in marks],
                                               lag_ratio=0.25), run_time=ctx.budget(1.6)[0])
        self._owned["clone"].add(marks)
        # "and posted a guide to moving from Cloudflare to Vercel".
        self._at(ctx, 0.7)
        back = style.glow_arrow(self._clone.get_left() + LEFT * 0.2, self._product.get_right() + RIGHT * 0.2,
                                color=style.WHITE, buff=0.0)
        label = style.label_text("migration guide", color=style.WHITE).next_to(back, UP, buff=0.2)
        self.play(GrowArrow(back[1]), FadeIn(back[0]), FadeIn(label), run_time=ctx.budget(0.9)[0])
        self._owned["back"] = VGroup(back, label)

    def b_trust(self, ctx):
        # With the timeline gone the pair closes in, so the middle of the stage is not left empty.
        a, b, c = ctx.budget(0.6, 0.8, 0.5)
        self.play(FadeOut(self._owned.pop("timeline")), FadeOut(self._owned.pop("back")),
                  self._owned["next"].animate.shift(RIGHT * 1.6),
                  self._owned["clone"].animate.shift(LEFT * 1.6), run_time=a)
        ring = RegularPolygon(n=6, radius=1.22).move_to(self._product)
        ring.set_stroke(style.GOLD, width=4).set_fill(style.GOLD, opacity=0.08)
        ring.set_z_index(style.Z_BACKDROP)
        trust = style.label_text("trust", color=style.GOLD).next_to(self._owned["next"][1], DOWN, buff=0.22)
        self.play(FadeIn(ring, shift=UP * 0.3, scale=0.8), FadeIn(trust), run_time=b)
        self.play(*style.highlight(self._product, style.BLUE), run_time=c)
        self._owned["next"].add(ring, trust)

    def b_firms(self, ctx):
        ctx.clear_stage(run_time=0.35)
        bought = VGroup()
        for x, name in ((-5.0, "Salesforce"), (-2.9, "HubSpot")):
            sq = style.node("product", size=1.2).move_to([x, TOP_Y, 0])
            bought.add(VGroup(sq, style.label_text(name, color=style.BLUE).next_to(sq, DOWN, buff=0.25)))
        self.play(FadeIn(bought, scale=0.9), run_time=ctx.budget(0.6)[0])
        self._at(ctx, 0.22)
        tools = VGroup(*[style.node("clone", size=0.95) for _ in range(5)]).arrange(RIGHT, buff=0.35)
        tools.move_to([2.95, TOP_Y, 0])
        built = style.label_text("built with AI", color=style.BLUE).next_to(tools, DOWN, buff=0.25)
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.3) for t in tools], lag_ratio=0.2),
                  FadeIn(built), *[sq[0].animate.set_opacity(0.35) for sq in bought],
                  run_time=ctx.budget(1.4)[0])
        self._at(ctx, 0.55)
        # Software cost cut by 40 to 80 percent, on a 0 to 100% line.
        x0, w = -3.5, 7.0
        axis = Line([x0, LOW_Y, 0], [x0 + w, LOW_Y, 0], color=style.MUTED, stroke_width=2.2)
        ticks = VGroup()
        for v, t in ((0, "0"), (0.4, "40%"), (0.8, "80%"), (1, "100%")):
            ticks.add(style.label_text(t, color=style.WHITE if t in ("40%", "80%") else style.MUTED,
                                       size="tiny").next_to([x0 + v * w, LOW_Y, 0], DOWN, buff=0.2))
        band = style.tile(0.4 * w, 0.42, style.GREEN, opacity=0.35)
        band.move_to([x0 + 0.6 * w, LOW_Y + 0.21, 0])
        cut = style.label_text("cost cut", color=style.GREEN).next_to(band, UP, buff=0.18)
        self.play(Create(axis), FadeIn(ticks), run_time=ctx.budget(0.5)[0])
        self.play(GrowFromCenter(band), FadeIn(cut), run_time=ctx.budget(0.8)[0])
        self._owned["firms"] = VGroup(bought, tools, built, axis, ticks, band, cut)

    # ------------------------------------------------------- what is costly --
    def _task_card(self, text: str) -> VGroup:
        card = RoundedRectangle(corner_radius=0.12, width=4.4, height=1.3, color=style.WHITE)
        card.set_fill(style.PANEL_HI, opacity=0.96).set_stroke(style.MUTED, width=2.2)
        words = style.caption_text(text).move_to(card).shift(LEFT * 0.35)
        tick = VMobject().set_points_as_corners([[-0.2, 0.0, 0], [-0.06, -0.16, 0], [0.24, 0.2, 0]])
        tick.set_stroke(style.GREEN, width=6).move_to(card.get_right() + LEFT * 0.55)
        return VGroup(card, words, tick)

    def b_checkable(self, ctx):
        ctx.clear_stage(run_time=0.3)
        cards = [self._task_card("build this screen").move_to([-3.1, 0.2, 0]),
                 self._task_card("pass this test").move_to([3.1, 0.2, 0])]
        for i, card in enumerate(cards):
            self._at(ctx, 0.05 + 0.4 * i)
            self.play(FadeIn(card[:2], shift=UP * 0.15), run_time=ctx.budget(0.5)[0])
            self.play(Create(card[2]), run_time=ctx.budget(0.4)[0])
        # Hold each card whole, so the next beat can move it as one.
        self.remove(*[part for card in cards for part in card])
        self.add(*cards)
        self._owned["cards"] = VGroup(*cards)

    def b_costly(self, ctx):
        ctx.lopsided("the cheap work sits small on the left; the costly three fill the right")
        cards = self._owned["cards"]
        # The line turns to what did not get cheap: the title turns with it.
        title = style.title_text("What did not get cheap")
        stage.fit(title, stage.TITLE)
        self.play(cards.animate.scale(0.7).arrange(DOWN, buff=0.45).move_to([-4.9, 0.25, 0]),
                  Transform(self._title, title), run_time=ctx.budget(0.6)[0])
        made = VGroup()
        for i, (word, x) in enumerate(zip(("decide", "prove", "keep running"), (-1.6, 1.5, 4.6))):
            self._at(ctx, 0.08 + 0.27 * i)
            hexa = style.node("moat", size=1.8).move_to([x, 0.4, 0])
            label = style.label_text(word, color=style.GOLD).next_to(hexa, DOWN, buff=0.3)
            self.play(FadeIn(hexa, scale=0.85), FadeIn(label), run_time=ctx.budget(0.6)[0])
            made.add(hexa, label)
        self._owned["costly"] = made
