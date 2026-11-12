"""
Section 06: in the limit. Levi asked for "thinking in the limit", so the section
reads as a chain of reasoning, and every step that is Alpha's own guess is drawn
in amber (the guess colour): the cycle of agency, the projections past what METR
measures, the promise a vendor sells, the empty slots of what is left, the
forces that would change the answer.

Pictures, in order: a quadrant (code free, agency high); profit moving along a
value chain when one layer becomes a commodity (Christensen); proportional
squares ($4.6 trillion against $1 trillion); METR's task-length plot with two
projections to a working month; a 50% gauge; an agent working a market; a grid
of people each with an agent; three moats filling their slots; the payment
permission flow; the three joining into "connected, permitted capacity".

Every beat takes its time from its window (`_at`), so a re-time needs no edit.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from moats_video.pipeline import charts, style
from moats_video.pipeline.beats import Beat, BeatScene

SLOTS = [LEFT * 4.3 + UP * 0.75, UP * 0.75, RIGHT * 4.3 + UP * 0.75]   # the three that are left
HEX = 1.8


def label(text: str, color: str = style.WHITE, size: str = "label") -> Text:
    return style.label_text(text, color=color, size=size)


def dashed_arrow(start, end, color: str = style.AMBER) -> VGroup:
    """A projection or a force that has not happened: a dashed shaft and a solid head."""
    start, end = np.array(start, dtype=float), np.array(end, dtype=float)
    unit = (end - start) / np.linalg.norm(end - start)
    shaft = DashedLine(start, end - unit * 0.18, color=color, stroke_width=3.4, dash_length=0.14)
    head = Triangle(color=color).set_fill(color, opacity=1).set_stroke(width=0).scale(0.11)
    head.rotate(math.atan2(unit[1], unit[0]) - PI / 2).move_to(end - unit * 0.1)
    return VGroup(shaft, head)


def river(widths: list[float], ys: list[float], cx: float, half: float) -> Polygon:
    """Profit as a band running down the value chain, as wide at each layer as the profit there."""
    left = [p for w, y in zip(widths, ys) for p in ([cx - w / 2, y + half, 0], [cx - w / 2, y - half, 0])]
    right = [p for w, y in zip(widths, ys) for p in ([cx + w / 2, y + half, 0], [cx + w / 2, y - half, 0])]
    band = Polygon(*left, *reversed(right), color=style.GOLD)
    return band.set_fill(style.GOLD, opacity=0.5).set_stroke(style.GOLD, width=1.6)


class S06Limit(BeatScene):
    section_id = "06_limit"
    title = "In the limit"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Now push it to the limit", self.b_quadrant,
                 note="a quadrant, cost of code against agency; a dot slides to the corner"),
            Beat("Clayton Christensen argued", self.b_chain,
                 note="a value chain of five layers with profit flowing through; one goes commodity"),
            Beat("So the question in the limit is what stays hard", self.b_hard,
                 note="the widened layer gets a question mark"),
            Beat("Much of what companies sell is agency", self.b_agency,
                 note="a product square, a cycle of four verbs round it (amber: a guess)"),
            Beat("Foundation Capital, a venture firm", self.b_squares,
                 note="proportional squares: $4.6 trillion against $1 trillion"),
            Beat("How much agency do agents have", self.b_metr,
                 note="METR's plot: task length against date, its two points"),
            Beat("Fifty minutes in early 2025", self.b_month,
                 note="the points named, the interval, a working-month line"),
            Beat("My arithmetic: at a doubling every three to seven months", self.b_project,
                 note="two amber projections to the month line; the band past what METR measures"),
            Beat("And half the time is not good enough to sell", self.b_gauge,
                 note="a 50% gauge, a mark for enough to sell, a contract card"),
            Beat("Agency gets devalued from both sides", self.b_market,
                 note="an agent between a buyer and three vendors: search, negotiate, transact"),
            Beat("Then the customer who never compares", self.b_passive,
                 note="a passive customer, a moat, struck"),
            Beat("And when every buyer and every seller has a capable agent", self.b_everyone,
                 note="a grid of people, each with an agent; agency greys"),
            Beat("What is left is what no amount of agency produces", self.b_slots,
                 note="three empty slots (amber dashed)"),
            Beat("Permission: a licence, a signature", self.b_permission,
                 note="the first fills, a signature drawn under it"),
            Beat("Physical capacity: power, land, machines", self.b_capacity,
                 note="the second, a years timeline"),
            Beat("And connection: being where everyone else already is", self.b_connection,
                 note="the third, a small network"),
            Beat("Look at how agents are being allowed to pay", self.b_pay,
                 note="person, signed mandate, agent, network gate with a registry, merchant"),
            Beat("So even an agent's agency is permission someone else grants", self.b_join,
                 note="the three hexagons join into connected, permitted capacity"),
            Beat("What would change that", self.b_change,
                 note="two amber forces aimed at the shape; 2017 floated, 2025 withdrawn"),
        ]

    # ------------------------------------------------------------ helpers --
    def _at(self, ctx, frac: float) -> None:
        """Wait until `frac` of this beat's window has passed (never past its end)."""
        lag = ctx.beat.start + frac * ctx.window - self.renderer.time
        if lag > 0.02:
            self.wait(lag)

    def _rest(self, ctx, frac: float) -> float:
        """Seconds from now until `frac` of the window, for an animation meant to fill them."""
        return max(ctx.beat.start + frac * ctx.window - self.renderer.time, 0.3)

    # ------------------------------------------------------------- 1 to 3 --
    def b_quadrant(self, ctx):
        plot = charts.Plot(LEFT * 3.0 + DOWN * 1.95, 6.0, 3.8, (0, 1), (0, 1), x_ticks=[(0, "nothing")])
        # At label size, not as a tick: at the tick size the gap in "whole jobs" closes up.
        jobs = label("whole jobs", style.MUTED).next_to(plot.at(0, 1), LEFT, buff=0.25)
        xt = label("what code costs", style.MUTED).next_to(plot.at(1, 0), RIGHT, buff=0.25)
        yt = label("what agents do alone", style.MUTED).next_to(plot.at(0, 1), UP, buff=0.2)
        yt.align_to(plot.at(0, 1), LEFT)
        mid = VGroup(DashedLine(plot.at(0.5, 0), plot.at(0.5, 1), color=style.DIM, stroke_width=2),
                     DashedLine(plot.at(0, 0.5), plot.at(1, 0.5), color=style.DIM, stroke_width=2))
        corner = Rectangle(width=3.0, height=1.9).set_stroke(width=0).set_fill(style.WHITE, opacity=0.07)
        corner.move_to((plot.at(0, 1) + plot.at(0.5, 0.5)) / 2)
        # Where agents stand: an agent diamond (a white circle would be a person).
        dot = style.node("agent", size=0.4).move_to(plot.at(0.72, 0.3))
        today = label("today", style.MUTED).next_to(dot, RIGHT, buff=0.2)
        self.play(FadeIn(plot), FadeIn(mid), FadeIn(xt), FadeIn(yt), FadeIn(jobs), run_time=ctx.budget(0.8)[0])
        self.play(FadeIn(dot, scale=0.6), FadeIn(today), run_time=0.4)
        self._at(ctx, 0.3)
        self.play(dot.animate.move_to(plot.at(0.07, 0.93)), FadeOut(today),
                  run_time=self._rest(ctx, 0.75), rate_func=smooth)
        limit = label("the limit", style.WHITE).move_to(corner)
        self.play(FadeIn(corner), FadeIn(limit), Flash(dot, color=style.VIOLET), run_time=0.6)

    def b_chain(self, ctx):
        ctx.clear_stage(run_time=0.35)
        self._ys = [1.6, 0.8, 0.0, -0.8, -1.6]
        cx = -0.3
        tiles = VGroup(*[style.tile(3.6, 0.6, style.MUTED, opacity=0.12).move_to([cx, y, 0])
                         for y in self._ys])
        before = [0.9, 1.0, 1.6, 1.0, 0.8]
        after = [0.9, 2.7, 0.14, 1.0, 0.8]
        flow = river(before, self._ys, cx, 0.3)
        profit = label("profit", style.GOLD).next_to(tiles[2], LEFT, buff=0.35)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in tiles], lag_ratio=0.12),
                  run_time=ctx.budget(0.9)[0])
        self.play(GrowFromEdge(flow, UP), FadeIn(profit), run_time=ctx.budget(1.0)[0])
        self._at(ctx, 0.45)
        commodity = label("commodity", style.MUTED).next_to(tiles[2], RIGHT, buff=0.35)
        self.play(tiles[2].animate.set_fill(style.DIM, opacity=0.5).set_stroke(style.DIM),
                  FadeIn(commodity), run_time=0.6)
        self._at(ctx, 0.62)
        self.play(Transform(flow, river(after, self._ys, cx, 0.3)),
                  profit.animate.next_to(tiles[1], LEFT, buff=0.35), run_time=self._rest(ctx, 0.92))
        self._tiles = tiles

    def b_hard(self, ctx):
        hard = self._tiles[1]
        mark = label("?", style.WHITE, "title").next_to(hard, RIGHT, buff=0.45)
        self.play(*style.highlight(hard, style.GOLD), FadeIn(mark, scale=1.6), run_time=ctx.budget(0.6)[0])
        self._at(ctx, 0.55)
        self.play(Indicate(mark, color=style.GOLD, scale_factor=1.3), run_time=0.8)

    # ------------------------------------------------------------- 4 to 5 --
    def b_agency(self, ctx):
        ctx.clear_stage(run_time=0.35)
        sold = style.node("product", "agency", size=1.5)
        self.play(DrawBorderThenFill(sold), run_time=ctx.budget(0.7)[0])
        rx, ry = 3.0, 1.75
        at = lambda deg: np.array([rx * math.cos(math.radians(deg)), ry * math.sin(math.radians(deg)), 0])
        verbs = [("notices", 90), ("decides", 0), ("acts", -90), ("follows up", 180)]
        for i, (word, deg) in enumerate(verbs):
            self._at(ctx, 0.3 + 0.13 * i)
            text = label(word, style.WHITE).move_to(at(deg))
            # Each arc leaves this verb and stops short of the next one, clockwise.
            arc = CurvedArrow(at(deg - 24), at(deg - 66), angle=-PI / 4, color=style.AMBER,
                              stroke_width=3, tip_length=0.18)
            self.play(FadeIn(text, shift=UP * 0.1), Create(arc), run_time=0.5)
        self._at(ctx, 0.88)
        self.play(Indicate(sold, color=style.BLUE, scale_factor=1.1), run_time=0.6)

    def b_squares(self, ctx):
        ctx.clear_stage(run_time=0.35)
        side = 3.0
        work = style.tile(side, side, style.WHITE, opacity=0.12).move_to([-2.0, -0.95, 0], aligned_edge=DOWN)
        soft = style.tile(side / math.sqrt(4.6), side / math.sqrt(4.6), style.BLUE, opacity=0.3)
        soft.move_to([2.6, -0.95, 0], aligned_edge=DOWN)
        names = []   # (figure, what) under each square, each shown as the narration reaches it
        for box, figure, what, color in ((work, "$4.6 trillion", "salaries and services", style.WHITE),
                                         (soft, "$1 trillion", "public enterprise software", style.BLUE)):
            rows = style.text_rows(label(figure, color, "caption"), label(what, style.MUTED), align=ORIGIN)
            names.append(rows.next_to(box, DOWN, buff=0.25))
        # "Foundation Capital, a venture firm that invests in replacing it": the work grows.
        self.play(GrowFromPoint(work, work.get_corner(DL)), run_time=self._rest(ctx, 0.22))
        self._at(ctx, 0.25)      # "puts the salaries and outsourced services"
        self.play(FadeIn(names[0][1]), run_time=0.5)
        self._at(ctx, 0.5)       # "at four point six trillion dollars"
        self.play(FadeIn(names[0][0]), work.animate.set_fill(opacity=0.2), run_time=0.6)
        self._at(ctx, 0.64)      # "against about one trillion"
        self.play(GrowFromPoint(soft, soft.get_corner(DL)), FadeIn(names[1][0]), run_time=0.8)
        self._at(ctx, 0.75)      # "for all public enterprise software companies"
        self.play(FadeIn(names[1][1]), run_time=0.5)
        self._at(ctx, 0.86)
        # The software square, laid inside the work square: it fits more than four times.
        ghost = DashedVMobject(Square(side_length=soft.width, color=style.BLUE).set_stroke(width=2.4),
                               num_dashes=24)
        ghost.move_to(soft)
        self.play(ghost.animate.move_to(work.get_corner(DL), aligned_edge=DL), run_time=1.0)

    # ------------------------------------------------------------- 6 to 8 --
    def b_metr(self, ctx):
        ctx.clear_stage(run_time=0.35)
        plot = charts.Plot(LEFT * 4.4 + DOWN * 1.95, 8.0, 3.85, (2024.75, 2028.5), (1 / 6, 400), y_log=True,
                           x_ticks=[(y, str(y)) for y in (2025, 2026, 2027, 2028)],
                           y_ticks=[(1 / 6, "10 min"), (1, "1 h"), (10, "10 h"), (100, "100 h")])
        title = label("task length, at 50% success", style.MUTED)
        title.next_to(plot.at(2024.75, 400), UP, buff=0.12).align_to(plot.at(2024.75, 400), LEFT)
        self._plot = plot
        self._pts = charts.dots(plot, [(2025.15, 50 / 60), (2026.2, 16)], radius=0.11)
        join = charts.line(plot, [(2025.15, 50 / 60), (2026.2, 16)], width=2.6)
        self.play(FadeIn(plot), FadeIn(title), run_time=ctx.budget(0.8)[0])
        self._at(ctx, 0.4)
        self.play(FadeIn(self._pts[0], scale=0.5), run_time=0.4)
        self._at(ctx, 0.6)
        self.play(Create(join), FadeIn(self._pts[1], scale=0.5), run_time=0.8)

    def b_month(self, ctx):
        plot, (early, late) = self._plot, self._pts
        self.play(Indicate(early, color=style.GREEN, scale_factor=1.8),
                  FadeIn(label("50 min", style.GREEN).move_to(early.get_center() + RIGHT * 0.65 + DOWN * 0.35)),
                  run_time=ctx.budget(0.7)[0])
        self._at(ctx, 0.3)
        whisker = Line(plot.at(2026.2, 8.5), plot.at(2026.2, 55), color=style.GREEN, stroke_width=3)
        caps = VGroup(*[Line(LEFT * 0.12, RIGHT * 0.12, color=style.GREEN, stroke_width=3).move_to(p)
                        for p in (whisker.get_start(), whisker.get_end())])
        name = label("16 h", style.GREEN).move_to(late.get_center() + RIGHT * 0.6 + DOWN * 0.35)
        least = label("at least", style.GREEN).next_to(whisker, LEFT, buff=0.3).shift(UP * 0.25)
        self.play(Indicate(late, color=style.GREEN, scale_factor=1.8), Create(whisker), FadeIn(caps),
                  FadeIn(name), FadeIn(least), run_time=0.8)
        self._at(ctx, 0.62)
        month = DashedLine(plot.at(2024.75, 170), plot.at(2028.5, 170), color=style.WHITE, stroke_width=2.6)
        word = label("a working month", style.WHITE).next_to(month, RIGHT, buff=0.2)
        self.play(Create(month), FadeIn(word), run_time=self._rest(ctx, 0.85))
        self._month = month

    def b_project(self, ctx):
        plot = self._plot
        # 16 h to 170 h is 3.4 doublings: 10 months at one every three, 24 at one every seven.
        meets = {3: 2026.2 + 3.41 * 3 / 12, 7: 2026.2 + 3.41 * 7 / 12}
        fast = dashed_arrow(plot.at(2026.2, 16), plot.at(meets[3], 170))
        slow = dashed_arrow(plot.at(2026.2, 16), plot.at(meets[7], 170))
        fast_name = label("every 3 months", style.AMBER, "tiny").move_to(plot.at(meets[3], 170) + UP * 0.25)
        # Under its own line, inside the line's box: a label straddling that box reads as struck through.
        slow_name = label("every 7 months", style.AMBER, "tiny").move_to(
            slow[0].get_start() + 0.72 * (slow[0].get_end() - slow[0].get_start()) + DOWN * 0.5)
        self._at(ctx, 0.05)
        self.play(Create(fast), run_time=ctx.budget(1.0)[0])
        self.play(FadeIn(fast_name), run_time=0.4)
        self._at(ctx, 0.25)
        self.play(Create(slow), run_time=1.0)
        self.play(FadeIn(slow_name), run_time=0.4)
        self._at(ctx, 0.45)
        when = Line(plot.at(meets[3], 170), plot.at(meets[7], 170), color=style.AMBER, stroke_width=8)
        self.play(Create(when), run_time=0.8)
        self._at(ctx, 0.62)
        band = Rectangle(width=plot.w, height=plot.h + plot.origin[1] - plot.at(2025, 16)[1])
        band.set_stroke(width=0).set_fill(style.MUTED, opacity=0.12)
        band.move_to(plot.at(2024.75, 16), aligned_edge=DL).set_z_index(style.Z_BACKDROP)
        blind = label("METR's tests stop measuring", style.MUTED, "tiny")
        # Inside the band, under the month line: above it, it crowded the plot's title.
        blind.move_to(plot.at(2024.75, 100), aligned_edge=LEFT).shift(RIGHT * 0.2)
        self.play(FadeIn(band), FadeIn(blind), run_time=0.8)
        self._at(ctx, 0.85)
        self.play(Indicate(when, color=style.AMBER, scale_factor=1.05),
                  fast.animate.set_opacity(0.6), slow.animate.set_opacity(0.6), run_time=0.8)

    # ------------------------------------------------------------ 9 to 12 --
    def b_gauge(self, ctx):
        ctx.clear_stage(run_time=0.35)
        c, r = np.array([0.0, -0.4, 0]), 1.9
        ring = dict(inner_radius=r - 0.3, outer_radius=r, start_angle=PI, arc_center=c, stroke_width=0)
        track = AnnularSector(angle=-PI, fill_color=style.DIM, fill_opacity=0.9, **ring)
        fill = AnnularSector(angle=-PI / 2, fill_color=style.GREEN, fill_opacity=0.9, **ring)
        needle = Line(c, c + LEFT * (r - 0.3), color=style.WHITE, stroke_width=4)
        hub = Dot(c, radius=0.1, color=style.WHITE)
        half = label("50% success", style.GREEN, "caption").next_to(hub, DOWN, buff=0.3)
        self.play(FadeIn(track), FadeIn(needle), FadeIn(hub), run_time=ctx.budget(0.5)[0])
        self.play(FadeIn(fill), Rotate(needle, -PI / 2, about_point=c), FadeIn(half), run_time=1.0)
        self._at(ctx, 0.15)      # "not good enough to sell"
        sell_at = c + r * np.array([math.cos(math.radians(8)), math.sin(math.radians(8)), 0])
        tick = Line(c + (sell_at - c) * 0.84, c + (sell_at - c) * 1.16, color=style.AMBER, stroke_width=5)
        sell = label("enough to sell", style.AMBER).next_to(tick, RIGHT, buff=0.2)
        self.play(Create(tick), FadeIn(sell), run_time=0.6)
        self._at(ctx, 0.55)      # "what a vendor sells then": the gauge makes room for the promise
        gauge = VGroup(track, fill, needle, hub, half, tick, sell)
        card = style.node("figure", size=2.6, color=style.AMBER).move_to([4.1, 0.2, 0])
        promise = style.text_rows(label("we answer", style.WHITE, "caption"),
                                  label("when it fails", style.WHITE, "caption"), align=ORIGIN).move_to(card)
        self.play(gauge.animate.shift(LEFT * 3.0), run_time=0.6)
        self.play(FadeIn(VGroup(card, promise), shift=LEFT * 0.4), run_time=0.6)
        self._at(ctx, 0.82)      # "the promise to answer when it fails"
        self.play(*style.highlight(card, style.AMBER), run_time=0.6)

    def b_market(self, ctx):
        ctx.clear_stage(run_time=0.35)
        y = 0.55        # high enough to weigh against the long claim footer in the balance check
        buyer = style.node("customer", size=1.0).move_to([-5.0, y, 0])
        agent = style.node("agent", size=1.1).move_to([-1.8, y, 0])
        # The three are steps the agent takes, not products: plain outlined boxes, no kind.
        vendors = [Square(side_length=0.8).set_stroke(style.MUTED, width=2.4).set_fill(style.PANEL_HI, opacity=0.9)
                   .move_to([2.6, y + dy, 0]) for dy in (1.25, 0, -1.25)]
        hand = style.connect(buyer, agent, color=style.CYAN)
        self.play(FadeIn(buyer), FadeIn(label("the buyer", style.CYAN).next_to(buyer, DOWN, buff=0.25)),
                  FadeIn(agent), LaggedStart(*[FadeIn(v) for v in vendors], lag_ratio=0.2),
                  run_time=ctx.budget(0.9)[0])
        self._at(ctx, 0.22)      # "Economists ... argue that agents will": the buyer hands over
        self.play(GrowArrow(hand[1]), FadeIn(hand[0]), run_time=0.6)
        for i, (vendor, verb) in enumerate(zip(vendors, ("search", "negotiate", "transact"))):
            self._at(ctx, 0.52 + 0.08 * i)       # "search, negotiate and transact for us"
            link = style.connect(agent, vendor, color=style.VIOLET)
            self.play(GrowArrow(link[1]), FadeIn(link[0]),
                      FadeIn(label(verb, style.WHITE).next_to(vendor, RIGHT, buff=0.3)), run_time=0.5)
        self._at(ctx, 0.8)       # "cutting the cost of using a market"
        drop = Triangle(color=style.RED).set_fill(style.RED, opacity=1).set_stroke(width=0).scale(0.13)
        cost = VGroup(drop.rotate(PI), label("cost to use a market", style.WHITE)).arrange(RIGHT, buff=0.2)
        cost.move_to([0.4, -1.75, 0])
        self.play(FadeIn(cost, shift=DOWN * 0.15), run_time=0.6)

    def b_passive(self, ctx):
        ctx.clear_stage(run_time=0.35)
        moat = style.node("moat", size=2.0).move_to([-2.4, 0.4, 0])
        name = label("a passive customer", style.GOLD, "caption").next_to(moat, DOWN, buff=0.3)
        self.play(FadeIn(moat, scale=0.85), FadeIn(name), run_time=ctx.budget(0.6)[0])
        self._at(ctx, 0.4)
        agent = style.node("agent", size=1.3).move_to([2.6, 0.4, 0])
        does = label("compares for them", style.VIOLET).next_to(agent, DOWN, buff=0.3)
        self.play(FadeIn(agent, shift=LEFT * 1.2), FadeIn(does), run_time=0.7)
        self._at(ctx, 0.68)
        self.play(moat.animate.set_opacity(0.3), name.animate.set_opacity(0.45), Create(style.strike(moat)),
                  run_time=0.6)

    def b_everyone(self, ctx):
        ctx.clear_stage(run_time=0.35)
        pairs = VGroup()
        for i in range(36):
            # Buyers are customers (cyan circles); sellers are products (blue squares), alternating.
            person = (Circle(radius=0.16, color=style.CYAN, stroke_width=2) if i % 2 == 0
                      else Square(side_length=0.3, color=style.BLUE, stroke_width=2))
            person.set_fill(style.PANEL_HI, opacity=1)
            agent = Square(side_length=0.2).rotate(PI / 4).set_stroke(style.VIOLET, width=2)
            agent.set_fill(style.VIOLET, opacity=0.35)
            pairs.add(VGroup(person, agent).arrange(RIGHT, buff=0.08))
        pairs.arrange_in_grid(rows=4, cols=9, buff=(0.4, 0.38)).move_to([-1.5, 0.2, 0])
        agency = label("agency", style.VIOLET, "title").move_to([4.6, 0.55, 0])
        self.play(FadeIn(agency), run_time=ctx.budget(0.4)[0])
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in pairs], lag_ratio=0.06),
                  agency.animate.set_color(style.MUTED), run_time=self._rest(ctx, 0.72))
        self._at(ctx, 0.75)
        self.play(FadeIn(label("like reading", style.MUTED).next_to(agency, DOWN, buff=0.3)), run_time=0.5)

    # ----------------------------------------------------------- 13 to 16 --
    def b_slots(self, ctx):
        ctx.clear_stage(run_time=0.35)
        self._slots = [DashedVMobject(RegularPolygon(n=6, radius=HEX / 2, color=style.AMBER)
                                      .set_stroke(style.AMBER, width=2.6), num_dashes=30).move_to(p)
                       for p in SLOTS]
        for i, slot in enumerate(self._slots):
            self._at(ctx, 0.1 + 0.25 * i)
            self.play(Create(slot), run_time=ctx.budget(0.6)[0])

    def _fill(self, ctx, i: int, word: str) -> VGroup:
        moat = style.node("moat", size=HEX).move_to(SLOTS[i])
        name = label(word, style.GOLD, "caption").next_to(moat, DOWN, buff=0.25)
        self.play(FadeOut(self._slots[i]), FadeIn(moat, scale=0.8), FadeIn(name), run_time=ctx.budget(0.6)[0])
        return VGroup(moat, name)

    def b_permission(self, ctx):
        ctx.lopsided("the three slots fill left to right; the empty ones are dashed, which the balance check cannot see")
        filled = self._fill(ctx, 0, "permission")
        base = filled.get_bottom() + DOWN * 0.75
        line = Line(base + LEFT * 1.0, base + RIGHT * 1.0, color=style.MUTED, stroke_width=2.2)
        self.play(Create(line), run_time=0.4)
        self._at(ctx, 0.35)
        sign = ParametricFunction(lambda t: base + np.array([t, 0.18 * math.sin(7 * t) + 0.2 - 0.12 * t, 0]),
                                  t_range=[-0.85, 0.85], color=style.WHITE, stroke_width=3)
        self.play(Create(sign), run_time=self._rest(ctx, 0.8), rate_func=linear)

    def b_capacity(self, ctx):
        ctx.lopsided("the three slots fill left to right; the empty ones are dashed, which the balance check cannot see")
        filled = self._fill(ctx, 1, "physical capacity")
        base = filled.get_bottom() + DOWN * 0.6
        line = Line(base + LEFT * 1.1, base + RIGHT * 1.1, color=style.MUTED, stroke_width=2.2)
        ticks = VGroup(*[Line(UP * 0.1, DOWN * 0.1, color=style.MUTED, stroke_width=2.2)
                         .move_to(line.point_from_proportion(k / 4)) for k in range(5)])
        years = label("years", style.MUTED, "tiny").next_to(line, DOWN, buff=0.25)
        marker = Dot(line.get_start(), radius=0.1, color=style.GOLD)
        self.play(Create(line), FadeIn(ticks), FadeIn(years), FadeIn(marker), run_time=0.5)
        self._at(ctx, 0.25)
        self.play(marker.animate.move_to(line.get_end()), run_time=self._rest(ctx, 0.9), rate_func=linear)

    def b_connection(self, ctx):
        filled = self._fill(ctx, 2, "connection")
        centre = filled.get_bottom() + DOWN * 0.75
        nodes, links = charts.network([centre] + charts.ring(6, 0.55, centre), [(0, i) for i in range(1, 7)]
                                      + [(i, i % 6 + 1) for i in range(1, 7)], radius=0.1)
        self.play(FadeIn(links), LaggedStart(*[FadeIn(n, scale=0.5) for n in nodes], lag_ratio=0.1),
                  run_time=0.8)
        self._at(ctx, 0.55)
        self.play(links.animate.set_color(style.CYAN), run_time=0.5)
        self.play(links.animate.set_color(style.MUTED), run_time=0.5)

    # ----------------------------------------------------------- 17 to 19 --
    def b_pay(self, ctx):
        ctx.clear_stage(run_time=0.35)
        y = 0.6         # high enough to weigh against the long claim footer in the balance check
        person = style.node("person", size=0.9).move_to([-5.7, y, 0])
        mandate = style.tile(1.4, 1.1, style.WHITE, opacity=0.08).move_to([-3.3, y, 0])
        limits = label("limits", style.WHITE, "tiny").move_to(mandate.get_top() + DOWN * 0.3)
        scrawl = ParametricFunction(lambda t: np.array([t, 0.07 * math.sin(9 * t), 0]), t_range=[-0.45, 0.45],
                                    color=style.WHITE, stroke_width=2.4).move_to(mandate.get_bottom() + UP * 0.3)
        agent = style.node("agent", size=1.0).move_to([-0.9, y, 0])
        gate = style.tile(1.9, 1.6, style.MUTED, opacity=0.12).move_to([1.9, y, 0])
        names = style.text_rows(*[label(n, style.WHITE, "tiny") for n in ("Visa", "Mastercard", "Google")],
                                align=ORIGIN).move_to(gate)
        shop = style.node("customer", size=0.9).move_to([5.0, y, 0])   # the merchant's account
        under = lambda m, word, color: label(word, color).next_to(m, DOWN, buff=0.3)
        # Straight along the row: connect() aims at a tile's corner, not its side.
        link = lambda a, b: style.glow_arrow(a.get_right() + RIGHT * 0.1, b.get_left() + LEFT * 0.1,
                                             color=style.CYAN, buff=0.0)
        grow = lambda arrow: (GrowArrow(arrow[1]), FadeIn(arrow[0]))
        # "how agents are being allowed to pay": the agent, the gate, the merchant.
        self.play(*[FadeIn(m) for m in (person, under(person, "person", style.WHITE), agent,
                                        under(agent, "agent", style.VIOLET), gate, shop,
                                        under(shop, "merchant", style.CYAN))], run_time=ctx.budget(0.6)[0])
        self.play(*grow(link(agent, gate)), *grow(link(gate, shop)), run_time=0.6)
        self._at(ctx, 0.18)      # "Visa, Mastercard and Google each announced a way"
        self.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in names], lag_ratio=0.3), run_time=0.8)
        self._at(ctx, 0.42)      # "the person sets the limits"
        self.play(FadeIn(VGroup(mandate, limits), shift=RIGHT * 0.15), *grow(link(person, mandate)),
                  *grow(link(mandate, agent)), run_time=0.6)
        self._at(ctx, 0.63)      # "Google's version has them sign a mandate"
        self.play(Create(scrawl), FadeIn(under(mandate, "signed mandate", style.WHITE)), run_time=0.8)
        self._at(ctx, 0.7)       # "and Mastercard lets only registered, verified agents pay"
        registry = style.tile(1.5, 0.5, style.WHITE, opacity=0.12).move_to([1.9, -1.3, 0])
        reg_name = label("registry", style.WHITE, "tiny").move_to(registry)
        check = DashedLine(gate.get_bottom(), registry.get_top(), color=style.WHITE, stroke_width=2.4)
        self.play(FadeIn(registry), FadeIn(reg_name), Create(check), run_time=0.6)
        self._at(ctx, 0.85)
        tick = VMobject(color=style.WHITE, stroke_width=5).set_points_as_corners(
            [LEFT * 0.14 + UP * 0.02, DOWN * 0.12, RIGHT * 0.2 + UP * 0.22]).next_to(registry, RIGHT, buff=0.25)
        self.play(Create(tick), Indicate(gate, color=style.WHITE, scale_factor=1.05), run_time=0.6)

    def b_join(self, ctx):
        ctx.clear_stage(run_time=0.35)
        moats = [style.node("moat", size=1.6).move_to(p + DOWN * 0.2) for p in SLOTS]
        names = [label(w, style.GOLD, "caption").next_to(m, DOWN, buff=0.25)
                 for w, m in zip(("permission", "physical capacity", "connection"), moats)]
        self.play(*[FadeIn(m, scale=0.85) for m in moats], *[FadeIn(n) for n in names],
                  run_time=ctx.budget(0.6)[0])
        self._at(ctx, 0.2)
        self.play(*style.highlight(moats[0], style.GOLD), Indicate(names[0], color=style.GOLD), run_time=0.7)
        self._at(ctx, 0.45)
        whole = style.node("moat", size=2.6).move_to(UP * 0.55)
        # Names out before the hexagons move, or an outline crosses a fading name (1080p30 gate).
        self.play(*[FadeOut(n) for n in names], run_time=0.3)
        self.play(*[m.animate.move_to(whole).scale(1.4).set_opacity(0) for m in moats],
                  FadeIn(whole, scale=0.6), run_time=0.7)
        self.remove(*moats)
        # The attribution ("Levi's phrase") is spoken; the caption footer carries claims, not the stage.
        phrase = label("connected, permitted capacity", style.GOLD, "caption")
        phrase.next_to(whole, DOWN, buff=0.3)
        self.play(FadeIn(phrase, shift=UP * 0.1), *style.highlight(whole, style.GOLD), run_time=0.7)
        self._whole = VGroup(whole, phrase)

    def b_change(self, ctx):
        whole = self._whole
        self.play(whole.animate.move_to([2.9, 0.1, 0]), run_time=ctx.budget(0.7)[0])
        target = whole[0]
        # Left edges on the timeline's start, so the left side reads as one column.
        standing = label("agents with legal standing", style.AMBER).move_to([-3.9, 1.9, 0]).align_to([-6.3, 0, 0], LEFT)
        power = label("plentiful power and hardware", style.AMBER).move_to([-3.9, -1.5, 0]).align_to([-6.3, 0, 0], LEFT)
        self._at(ctx, 0.1)
        legal = dashed_arrow(standing.get_right() + RIGHT * 0.2 + DOWN * 0.1, target.get_left() + UP * 0.45)
        self.play(FadeIn(standing), Create(legal), run_time=0.8)
        self._at(ctx, 0.3)
        self.play(FadeIn(power), Create(dashed_arrow(power.get_right() + RIGHT * 0.2 + UP * 0.1,
                                                     target.get_left() + DOWN * 0.45)), run_time=0.8)
        self._at(ctx, 0.48)
        line = Line([-6.3, 1.15, 0], [-1.2, 1.15, 0], color=style.MUTED, stroke_width=2.2)
        marks = []
        for x, year, what, color in ((-6.1, "2017", "electronic persons", style.MUTED),
                                     (-2.9, "2025", "liability rules withdrawn", style.RED)):
            dot = Dot([x, 1.15, 0], radius=0.09, color=color)
            words = style.text_rows(label(year, style.WHITE), label(what, style.MUTED))
            words.next_to(dot, DOWN, buff=0.2).align_to(dot, LEFT).shift(LEFT * 0.09)
            marks.append(VGroup(dot, words))
        self.play(Create(line), FadeIn(marks[0]), run_time=0.7)
        self._at(ctx, 0.66)
        self.play(FadeIn(marks[1]), run_time=0.6)
        # No country lets an agent be held liable: the legal-standing force stays a guess.
        self._at(ctx, 0.84)
        self.play(legal.animate.set_opacity(0.4), Indicate(target, color=style.GOLD, scale_factor=1.08),
                  run_time=0.8)
