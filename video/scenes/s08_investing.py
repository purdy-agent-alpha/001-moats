"""
Section 08: an investing note. Analysis, not advice: nothing here reads as a
recommendation to buy.

Software repriced (a dot plot of revenue multiples on a log axis; one-day drops
as small multiples), its revenue still growing (record cards) as Jevons would
expect (a demand curve), but no longer priced as protected. Power is scarce at
the connection, not the panel: auctions at their cap (gauges), the shortfall
(a bar with a broken axis), the waits (gantt rows on one time axis). Every beat
takes its times from its own window (`_at`), so a re-time needs no edit here.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from moats_video.pipeline import charts, stage, style
from moats_video.pipeline.beats import Beat, BeatScene

LEFT_COL, RIGHT_COL = stage.columns(2, gap=0.8)
COL3 = stage.columns(3, gap=0.6)
HEAD_Y = 2.05
WEEKS_PER_YEAR = 52.18


def label(text: str, color: str = style.WHITE, size: str = "label") -> Text:
    return style.label_text(text, color=color, size=size)


def gauge(radius: float = 1.4) -> VGroup:
    """VGroup(dial, cap mark, needle, hub): a half dial whose right end is the cap; the needle starts at zero."""
    dial = Arc(radius=radius, start_angle=PI, angle=-PI, color=style.MUTED, stroke_width=6)
    cap = Line(RIGHT * (radius - 0.22), RIGHT * (radius + 0.22), color=style.WHITE, stroke_width=5)
    needle = Line(ORIGIN, LEFT * (radius - 0.15), color=style.GREEN, stroke_width=5)
    hub = Dot(ORIGIN, radius=0.09, color=style.GREEN)
    return VGroup(dial, cap, needle, hub)


class S08Investing(BeatScene):
    section_id = "08_investing"
    title = "An investing note"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("The second angle is money", self.b_money,
                 note="software (product square) and power (hexagon); not investment advice"),
            Beat("Investors have already repriced software", self.b_median,
                 note="dot plot on a log axis: the median cloud company at 4.5x next year's revenue"),
            Beat("get nearly nineteen times", self.b_spread,
                 note="two more rows: 18.7x for fast growers, 3.7x for slow"),
            Beat("When a legal plug-in for an AI assistant came out", self.b_drops,
                 note="small multiples: drops as reported, Thomson Reuters -14%, RELX -14%, Wolters Kluwer -10.5%"),
            Beat("No rebuild happened; even owners of proprietary data", self.b_priced,
                 note="Alpha's reading, under the panels: no rebuild, priced as exposed"),
            Beat("Yet software revenue has not stopped", self.b_growth,
                 note="record cards: ServiceNow +21%, Atlassian +24%"),
            Beat("That fits an old pattern, Jevons's paradox", self.b_jevons,
                 note="demand curve: price falls, use grows wider, each unit's margin thinner"),
            Beat("What seems to have stopped is investors paying for that growth", self.b_unprotected,
                 note="the moat round software's growth is struck"),
            Beat("When Levi asked for this video, his note was", self.b_levi,
                 note="Levi's note, in his words: energy and physical resources grow, software flat"),
            Beat("Physical power does look different. In PJM", self.b_cap,
                 note="three gauges, each needle at the price cap"),
            Beat("The last auction came up six thousand eight hundred", self.b_short,
                 note="what was cleared, what reliability needs, the red gap of 6,800 MW"),
            Beat("A power plant that came online in 2025", self.b_connect,
                 note="gantt row: asking to connect to running, past the 5 years mark"),
            Beat("In 2025, power transformers took an average", self.b_transformer,
                 note="a second gantt row, 128 weeks, on the same time axis"),
            Beat("But the panels are not the scarce part", self.b_panels,
                 note="used panels at ten cents a watt"),
            Beat("The scarce part is the connection", self.b_connection,
                 note="the connection is the moat: four things gather by the hexagon"),
            Beat("So the money, I think, is in owning", self.b_own,
                 note="panels recede; the hexagon: network, permission, physical"),
            Beat("What would break this view", self.b_break,
                 note="three small pictures: prices under the cap, shorter waits, multiples recover"),
        ]

    # ------------------------------------------------------------ helpers --
    def _at(self, ctx, frac: float) -> None:
        """Wait until `frac` of this beat's window has passed (never past its end)."""
        lag = ctx.beat.start + frac * ctx.window - self.renderer.time
        if lag > 0.02:
            self.wait(lag)

    # ------------------------------------------------------------- software --
    def b_money(self, ctx):
        software = style.node("product", size=2.0).move_to(LEFT_COL.center + UP * 0.3)
        power = style.node("moat", size=2.3).move_to(RIGHT_COL.center + UP * 0.3)
        s_name = label("software", style.BLUE).next_to(software, DOWN, buff=0.3)
        p_name = label("power", style.GOLD).next_to(power, DOWN, buff=0.3)
        self.play(DrawBorderThenFill(software), DrawBorderThenFill(power),
                  FadeIn(s_name), FadeIn(p_name), run_time=ctx.budget(0.8)[0])
        self._at(ctx, 0.3)
        note = label("not investment advice", style.MUTED)
        note.move_to(stage.STAGE.center + DOWN * 1.75)
        ctx.show(note, tag="note", run_time=0.5, nudge=False)

    ROWS = [(0.9, "median"), (0.0, "growing over 22%"), (-0.9, "growing under 15%")]

    def b_median(self, ctx):
        """A dot plot on a log axis, one row per group of companies."""
        ctx.clear_stage(run_time=0.35)
        plot = charts.Plot([-2.8, -1.75, 0], 8.6, 3.1, (1, 30), (0, 1), x_log=True,
                           x_ticks=[(1, "1×"), (3, "3×"), (10, "10×"), (30, "30×")])
        head = label("× next year's revenue", style.MUTED).move_to([plot.at(5.5, 0)[0], HEAD_Y, 0])
        plot.axes.remove(plot.axes[1])          # a dot plot has no value axis
        # One lane per group, tall enough to hold its dot's value: thin guide lines left the
        # stage so empty that the claim footer outweighed the chart in the balance check.
        x0, x1 = plot.at(1, 0)[0], plot.at(30, 0)[0]
        guides = VGroup(*[Rectangle(width=x1 - x0, height=0.84).set_stroke(width=0)
                          .set_fill(style.GRID, opacity=0.5).move_to([(x0 + x1) / 2, y + 0.14, 0])
                          for y, _ in self.ROWS])
        guides.set_z_index(style.Z_BACKDROP - 1, family=True)   # under the axis
        names = VGroup(*[label(name, style.MUTED).move_to([-3.1, y, 0], aligned_edge=RIGHT)
                         for y, name in self.ROWS])
        self._plot = plot
        ctx.show(plot, guides, head, tag="plot", run_time=0.6, nudge=False)
        self._at(ctx, 0.15)
        ctx.show(names[0], tag="n0", run_time=0.4, nudge=False)
        self._names = names
        self._at(ctx, 0.48)
        self._dot(ctx, 4.5, 0, "4.5×")
        self._at(ctx, 0.8)
        self.play(Indicate(self._owned["d0"][0], color=style.GREEN, scale_factor=1.5), run_time=0.6)

    def _dot(self, ctx, value: float, row: int, text: str) -> VGroup:
        y = self.ROWS[row][0]
        dot = Dot([self._plot.at(value, 0)[0], y, 0], radius=0.14, color=style.GREEN)
        val = label(text, size="caption").next_to(dot, UP, buff=0.12)
        return ctx.show(dot, val, tag=f"d{row}", anim=lambda m: FadeIn(m, scale=0.6), run_time=0.5,
                        nudge=False)

    def b_spread(self, ctx):
        ctx.show(self._names[1], tag="n1", run_time=0.3, nudge=False)
        self._dot(ctx, 18.7, 1, "18.7×")
        self._at(ctx, 0.5)
        ctx.show(self._names[2], tag="n2", run_time=0.3, nudge=False)
        self._dot(ctx, 3.7, 2, "3.7×")

    def b_drops(self, ctx):
        """One-day drops as small multiples: the same step, three companies."""
        ctx.clear_stage(run_time=0.35)
        drops = [("Thomson Reuters", 14), ("RELX", 14), ("Wolters Kluwer", 10.5)]
        panels = []
        for col, (name, pct) in zip(COL3, drops):
            # A panel round each multiple: bare axes left the stage too empty to balance the footer.
            frame = style.tile(col.width - 0.2, 3.25, style.GRID, opacity=0.35).move_to([col.center[0], 0.1, 0])
            frame.set_z_index(style.Z_BACKDROP - 1)    # under the axes, which sit at Z_BACKDROP
            plot = charts.Plot([col.left + 0.4, -1.3, 0], col.width - 0.8, 2.3, (0, 2), (80, 101), x_title="the plug-in")
            before = Line(plot.at(0, 100), plot.at(1, 100), color=style.GREEN, stroke_width=4)
            fall = Line(plot.at(1, 100), plot.at(1, 100 - pct), color=style.RED, stroke_width=4)
            after = Line(plot.at(1, 100 - pct), plot.at(2, 100 - pct), color=style.RED, stroke_width=4)
            name_t = label(name).next_to(plot, UP, buff=0.3)
            level = label("100", style.MUTED, size="tiny").next_to(before, UP, buff=0.06).align_to(before, LEFT)
            value = label(f"−{pct:g}%", style.RED, size="caption")
            value.next_to(plot.at(2, 100 - pct), UP, buff=0.22).align_to(plot.at(2, 0), RIGHT)
            panels.append((VGroup(frame, plot, before, name_t, level), VGroup(fall, after, value)))
        head = label("share price, as reported", style.MUTED).move_to(UP * HEAD_Y)
        ctx.show(head, *[base for base, _ in panels], tag="panels", run_time=0.6, nudge=False)
        # Thomson Reuters as it is named; the other two, the same report's figures, after it.
        for i, frac in enumerate((0.45, 0.57, 0.66)):
            drop = panels[i][1]
            self._at(ctx, frac)
            self.play(Create(drop[0]), run_time=0.3, rate_func=rush_into)
            self.play(Create(drop[1]), FadeIn(drop[2]), run_time=0.4)
            self._owned["panels"].add(drop)

    def b_priced(self, ctx):
        """Alpha's reading of the drops: its own beat, so it carries its own guess chip."""
        note = label("no rebuild", style.MUTED, size="caption").move_to(DOWN * 1.95)
        self._at(ctx, 0.05)
        ctx.show(note, tag="priced", run_time=0.4, nudge=False)
        # Two labels, not three: a third left each up under its reading time (gate, text_too_brief, 2026-11-10).
        for frac, text in ((0.5, "priced as exposed"),):
            self._at(ctx, frac)
            new = label(text, style.MUTED, size="caption").move_to(DOWN * 1.95)
            # One after the other: a cross-fade puts two labels in one place (gate, text_overlap, 2026-11-10).
            self.play(FadeOut(self._owned["priced"]), run_time=0.25)
            self.play(FadeIn(new), run_time=0.25)
            self._owned["priced"] = VGroup(new)

    def b_growth(self, ctx):
        ctx.clear_stage(run_time=0.35)
        cards = [("+21%", "ServiceNow subscriptions", -2.9, 0.1), ("+24%", "Atlassian revenue", 2.9, 0.5)]
        for i, (value, name, x, frac) in enumerate(cards):
            self._at(ctx, frac)
            card = style.node("figure", value, size=2.0, font_size=44).move_to([x, 0.35, 0])
            name_t = label(name, style.MUTED).next_to(card, DOWN, buff=0.3)
            ctx.show(card, name_t, tag=f"card{i}", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.6,
                     nudge=False)
        self._at(ctx, 0.85)
        self.play(*[a for i in range(2) for a in style.highlight(self._owned[f"card{i}"][0], style.GREEN)],
                  run_time=0.5)

    def _jevons_state(self, plot, p: float) -> VGroup:
        """At price p: the point on the demand curve, the spend box under it, the gold margin per unit."""
        q = self._demand(p)
        box = Rectangle(width=plot.at(q, 0)[0] - plot.origin[0], height=plot.at(0, p)[1] - plot.origin[1])
        # Blue, software's colour: this is an illustration of a guess, not measured data (green).
        box.set_fill(style.BLUE, opacity=0.16).set_stroke(style.BLUE, width=2)
        box.move_to(plot.origin, aligned_edge=DL)
        margin = Rectangle(width=box.width, height=box.height * 0.22)
        margin.set_fill(style.GOLD, opacity=0.6).set_stroke(style.GOLD, width=1.5)
        margin.move_to(box.get_top(), aligned_edge=UP)
        point = Dot(plot.at(q, p), radius=0.12, color=style.WHITE)
        return VGroup(box, margin, point).set_z_index(style.Z_BACKDROP)

    @staticmethod
    def _demand(p: float) -> float:
        # Elastic demand (exponent over 1): as price falls, spending grows. Jevons's case.
        return 10 * (0.6 / p) ** 1.3

    def b_jevons(self, ctx):
        ctx.clear_stage(run_time=0.35)
        plot = charts.Plot([-5.6, -1.8, 0], 8.0, 3.7, (0, 8), (0, 4), x_title="use", y_title="price")
        curve = VMobject(color=style.WHITE, stroke_width=3).set_points_smoothly(
            [plot.at(self._demand(p), p) for p in np.linspace(3.4, 0.79, 24)])
        curve.set_z_index(style.Z_EDGE)
        when = label("Jevons, 1865", style.MUTED, size="caption").move_to([4.6, 1.6, 0])
        ctx.lopsided("the curve fills the left; the legend stands on the right")
        ctx.show(plot, tag="plot", run_time=0.5, nudge=False)
        self.play(Create(curve), FadeIn(when), run_time=ctx.budget(1.0)[0])
        self._owned["curve"] = VGroup(curve, when)
        self._at(ctx, 0.2)
        state = self._jevons_state(plot, 3.3)
        key = VGroup(style.tile(0.4, 0.22, style.GOLD, opacity=0.6), label("margin per unit", style.GOLD))
        key.arrange(RIGHT, buff=0.25).move_to([4.6, 0.4, 0])
        ctx.show(state, key, tag="state", run_time=0.6, nudge=False)
        for frac, p in ((0.3, 2.0), (0.45, 1.3), (0.6, 0.85)):
            self._at(ctx, frac)
            self.play(Transform(state, self._jevons_state(plot, p)), run_time=ctx.budget(1.0)[0])

    def b_unprotected(self, ctx):
        ctx.clear_stage(run_time=0.35)
        software = style.node("product", size=1.6).move_to(UP * 0.45)
        ctx.show(software, tag="sw", run_time=0.5, nudge=False)
        self._at(ctx, 0.2)
        moat = style.node("moat", size=3.4).move_to(software)
        moat.set_z_index(style.Z_BACKDROP, family=True)
        moat[1].set_fill(opacity=0.0)
        name = label("software growth", style.BLUE).next_to(moat, DOWN, buff=0.25)
        ctx.waive("node_overlap", "the hexagon is drawn round the product on purpose: the protection "
                                  "its growth was priced as having")
        ctx.show(moat, name, tag="moat", run_time=0.6, nudge=False)
        self._at(ctx, 0.55)
        # The ring is struck, not the product: the red line stops at the square's edges (as in 10).
        full = style.strike(moat[1])
        cut = VGroup(Line(full.get_start(), software.get_corner(DL), color=style.RED, stroke_width=5),
                     Line(software.get_corner(UR), full.get_end(), color=style.RED, stroke_width=5))
        self.play(Create(cut), moat.animate.set_opacity(0.4), run_time=0.6)
        self._owned["moat"].add(cut)

    def b_levi(self, ctx):
        ctx.clear_stage(run_time=0.35)
        power = style.node("moat", size=2.2).move_to(RIGHT_COL.center + UP * 0.25)
        p_name = label("energy, physical resources", style.GOLD).next_to(power, DOWN, buff=0.3)
        head = label("Levi's note, Oct 2026", style.MUTED).move_to(UP * HEAD_Y)
        # White, the colour of the Levi's-view chip: green is for measured figures.
        rise = style.glow_arrow(power.get_top() + UP * 0.1, power.get_top() + UP * 1.2,
                                color=style.WHITE, buff=0.0)
        ctx.show(head, power, p_name, tag="power", run_time=0.6, nudge=False)
        ctx.waive("arrow_to_nowhere", "an upward arrow on the hexagon means growth; it aims at no object by design")
        self.play(GrowArrow(rise[1]), FadeIn(rise[0]), run_time=0.7)
        self._owned["rise"] = rise
        self._at(ctx, 0.5)
        software = style.node("product", size=1.9).move_to(LEFT_COL.center + UP * 0.25)
        s_name = label("software", style.BLUE).next_to(software, DOWN, buff=0.3)
        # Software stays flat: a level dash where the hexagon has its rise.
        flat = Line(software.get_right() + RIGHT * 0.3, software.get_right() + RIGHT * 1.2,
                    color=style.MUTED, stroke_width=5)
        ctx.show(software, s_name, flat, tag="software", run_time=0.6, nudge=False)
        self._at(ctx, 0.75)
        self.play(software.animate.set_opacity(0.4), run_time=0.5)

    # ---------------------------------------------------------------- power --
    def b_cap(self, ctx):
        """Three auctions, three gauges, each needle swept to the cap."""
        ctx.clear_stage(run_time=0.35)
        head = label("PJM capacity price, each auction", style.MUTED).move_to(UP * HEAD_Y)
        ctx.lopsided("the three auctions arrive one at a time, left to right")
        ctx.show(head, tag="head", run_time=0.4, nudge=False)
        for i, (x, year, frac) in enumerate(zip((-4.3, 0.0, 4.3), ("2026/27", "2027/28", "2028/29"),
                                               (0.03, 0.2, 0.37))):
            self._at(ctx, frac)
            g = gauge().shift([x, -0.5, 0])
            centre = g[3].get_center()
            yr = label(year, style.MUTED).next_to(centre, DOWN, buff=0.4)
            cap = label("cap", size="tiny").next_to(g[1], DOWN, buff=0.18)
            ctx.show(g, yr, cap, tag=f"g{i}", run_time=0.4, nudge=False)
            self.play(Rotate(g[2], angle=-PI, about_point=centre), run_time=0.6,
                      rate_func=rate_functions.ease_out_cubic)
            self.play(g[2].animate.set_color(style.WHITE), run_time=0.2)   # at the cap, not a loss: no red

    def b_short(self, ctx):
        """Cleared against needed: the bar's axis is broken, so the gap shows at its real size."""
        ctx.clear_stage(run_time=0.35)
        floor, gw = -1.7, 0.088              # scene units per gigawatt above the break
        ctx.lopsided("a bar stands on its baseline; what reliability needs is drawn above it next")
        need_y = floor + 3.3
        got = style.tile(3.0, 3.3 - 6.8 * gw, style.GREEN, opacity=0.3)
        got.move_to([0, floor, 0], aligned_edge=DOWN)
        cut = VGroup(*[Line(LEFT * 1.8, RIGHT * 1.8, color=style.BG, stroke_width=7).rotate(0.12)
                       .move_to([0, floor + 0.35 + d, 0]) for d in (0, 0.16)])
        axis = Line([-4.2, floor, 0], [4.2, floor, 0], color=style.DIM, stroke_width=2)
        cleared = label("cleared, 2028/29", style.MUTED).next_to(got, DOWN, buff=0.22)
        ctx.show(axis, got, cut, cleared, tag="got", run_time=0.6, nudge=False)
        self._at(ctx, 0.25)
        need = DashedLine([-4.2, need_y, 0], [4.2, need_y, 0], color=style.WHITE, stroke_width=3)
        need_name = label("reliability needs", style.WHITE).next_to(need, UP, buff=0.18).align_to(need, RIGHT)
        ctx.show(need, need_name, tag="need", anim=Create, run_time=0.6, nudge=False)
        self._at(ctx, 0.5)
        gap = style.tile(3.0, 6.8 * gw, style.RED, opacity=0.3).next_to(got, UP, buff=0)
        short = label("6,800 MW short", style.RED, size="caption").next_to(gap, LEFT, buff=0.35)
        self.play(GrowFromEdge(gap, DOWN), FadeIn(short), run_time=ctx.budget(0.9)[0])
        self._owned["gap"] = VGroup(gap, short)
        self._at(ctx, 0.8)
        self.play(gap.animate.set_fill(opacity=0.6), run_time=0.5)

    def b_connect(self, ctx):
        """Gantt row: from asking to connect to running, past the five years mark."""
        ctx.clear_stage(run_time=0.35)
        plot = charts.Plot([-3.6, -1.7, 0], 9.6, 3.3, (0, 6), (0, 1), x_title="years")
        plot.axes.remove(plot.axes[1])
        five = DashedLine(plot.at(5, 0), plot.at(5, 1), color=style.WHITE, stroke_width=2.4)
        five.set_z_index(style.Z_EDGE)
        five_t = label("5 years", size="caption").next_to(five, UP, buff=0.15)
        ctx.lopsided("the time axis waits for its two rows, the first on this line")
        ctx.show(plot, five, five_t, tag="axis", run_time=0.5, nudge=False)
        self._plot = plot
        self._at(ctx, 0.15)
        bar, name = self._row(plot, 0.72, 5.0, "power plant")
        tail = VGroup(*[style.tile(0.16, bar.height, style.GREEN, opacity=0.3 - 0.07 * k)
                        .set_stroke(opacity=0.6 - 0.15 * k) for k in range(4)])
        tail.arrange(RIGHT, buff=0).next_to(bar, RIGHT, buff=0)
        ask = label("asked to connect", style.MUTED).next_to(bar, UP, buff=0.18).align_to(bar, LEFT)
        ctx.show(name, ask, tag="row0_t", run_time=0.4, nudge=False)
        self.play(GrowFromEdge(bar, LEFT), run_time=ctx.budget(2.2)[0], rate_func=linear)
        # "more than five years": the bar runs on past the mark, fading.
        self.play(LaggedStart(*[FadeIn(t) for t in tail], lag_ratio=0.4), run_time=0.6)
        self._owned["row0"] = VGroup(bar, tail)
        self._at(ctx, 0.62)
        run = label("running", style.MUTED).next_to(tail, RIGHT, buff=0.2)
        ctx.show(run, tag="run", run_time=0.4, nudge=False)

    def _row(self, plot, y_frac: float, years: float, name: str) -> tuple[Rectangle, Text]:
        bar = style.tile(plot.at(years, 0)[0] - plot.origin[0], 0.6, style.GREEN, opacity=0.3)
        bar.move_to(plot.at(0, y_frac), aligned_edge=LEFT)
        return bar, label(name).next_to(plot.at(0, y_frac), LEFT, buff=0.3)

    def b_transformer(self, ctx):
        plot = self._plot
        bar, name = self._row(plot, 0.25, 128 / WEEKS_PER_YEAR, "transformer")
        order = label("ordered", style.MUTED).next_to(bar, UP, buff=0.18).align_to(bar, LEFT)
        ctx.show(name, order, tag="row1_t", run_time=0.4, nudge=False)
        self._at(ctx, 0.12)
        self.play(GrowFromEdge(bar, LEFT), run_time=ctx.budget(1.6)[0], rate_func=linear)
        self._owned["row1"] = bar
        val = label("128 weeks", size="caption").next_to(bar, RIGHT, buff=0.3)
        ctx.show(val, tag="row1_v", run_time=0.4, nudge=False)
        self._at(ctx, 0.75)
        self.play(*style.highlight(bar, style.GREEN), run_time=0.5)

    def b_panels(self, ctx):
        ctx.clear_stage(run_time=0.35)
        panels = VGroup(*[style.tile(0.85, 0.55, style.MUTED, opacity=0.22) for _ in range(12)])
        # Centred while they are alone; they step left when the connection arrives.
        panels.arrange_in_grid(rows=3, cols=4, buff=0.18).move_to([0, 0.25, 0])
        used = label("used panels", style.MUTED).next_to(panels, UP, buff=0.3)
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in panels], lag_ratio=0.08),
                  FadeIn(used), run_time=ctx.budget(1.0)[0])
        self._owned["panels"] = VGroup(panels, used)
        self._at(ctx, 0.5)
        price = label("$0.10 a watt", size="caption").next_to(panels, DOWN, buff=0.35)
        ctx.show(price, tag="price", run_time=0.5, nudge=False)

    def b_connection(self, ctx):
        self.play(*[self._owned[t].animate.shift(LEFT * 3.6) for t in ("panels", "price")], run_time=0.5)
        hub = style.node("moat", size=2.2).move_to([2.0, 0.25, 0])
        h_name = label("the connection", style.GOLD).next_to(hub, DOWN, buff=0.3)
        ctx.show(hub, h_name, tag="hub", run_time=0.6, nudge=False)
        panels = self._owned["panels"][0]
        link = style.glow_arrow(panels.get_right() + RIGHT * 0.2, hub.get_left() + LEFT * 0.2,
                                color=style.GOLD)
        ctx.show(link, tag="link", run_time=0.5, nudge=False)
        words = ("right to connect", "permits", "long-lead hardware", "agreements")
        found = VGroup()
        for i, (word, y) in enumerate(zip(words, (1.35, 0.6, -0.15, -0.9))):
            self._at(ctx, 0.25 + 0.1 * i)
            t = label(word).move_to([3.6, y, 0], aligned_edge=LEFT)
            self.play(FadeIn(t, shift=LEFT * 0.25), run_time=0.45)
            found.add(t)
        self._owned["needs"] = found

    def b_own(self, ctx):
        ctx.recede("panels", "price", opacity=0.22, run_time=0.5)
        hub = self._owned["hub"]
        self.play(*style.highlight(hub[0], style.GOLD), run_time=0.6)
        self._at(ctx, 0.4)
        what = label("network · permission · physical", style.GOLD).next_to(hub, DOWN, buff=0.25)
        ctx.show(what, tag="what", run_time=0.5, nudge=False)
        self._at(ctx, 0.7)
        self.play(hub[0].animate.scale(1.08), run_time=0.6)

    def b_break(self, ctx):
        ctx.clear_stage(run_time=0.35)
        w = 2.4
        # 1. prices clear under the cap
        cap = DashedLine(LEFT * w / 2, RIGHT * w / 2, color=style.MUTED, stroke_width=3)
        bar1 = style.tile(1.0, 1.4, style.AMBER, opacity=0.3).next_to(cap, DOWN, buff=0.35)
        # 2. connection waits get shorter
        bar2 = style.tile(w, 0.55, style.AMBER, opacity=0.3)
        # 3. software retention holds and multiples recover
        sw = style.node("product", size=1.2)
        up = style.glow_arrow(sw.get_right() + RIGHT * 0.2 + DOWN * 0.3,
                              sw.get_right() + RIGHT * 1.1 + UP * 0.5, color=style.AMBER, buff=0.0)
        cols = []
        for col, pic, name in zip(COL3, (VGroup(cap, bar1), VGroup(bar2), VGroup(sw, up)),
                                  ("prices below the cap", "shorter waits", "retention holds,\nmultiples up")):
            pic.scale(1.3).move_to(col.center + UP * 0.6)
            cols.append(VGroup(pic, label(name).move_to(col.center + DOWN * 1.0)))
        ctx.lopsided("three columns arrive one at a time, left to right")
        ctx.waive("arrow_to_nowhere", "the rising arrow beside the product means multiples recovering")
        for i, frac in enumerate((0.03, 0.25, 0.45)):
            self._at(ctx, frac)
            ctx.show(cols[i], tag=f"b{i}", run_time=0.6, nudge=False)
            if i == 1:
                self.play(bar2.animate.stretch(0.55, 0, about_edge=LEFT), run_time=0.8)
