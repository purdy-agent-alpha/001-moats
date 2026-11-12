"""
Section 07: the first angle, running a software company.

The relationship is what you own; net revenue retention as the evidence (what it
is, as a waterfall of its parts; the 2025 medians as two waffles; HubSpot's as a
line with its gross retention under it; its growth as an area); pricing moving
to usage as a slope chart; the agent stepping between you and the customer; and
the founder's list, one item per line. Every beat takes its times from its own
window (`_at`), so a re-time of the voice needs no edit here.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from moats_video.pipeline import charts, style
from moats_video.pipeline.beats import Beat, BeatScene

HEAD_Y = 2.05          # a chart's heading, just under the title lane


def fall() -> Triangle:
    """A red downward marker for a loss. A shape, not an arrow: it joins nothing."""
    t = Triangle(color=style.RED).rotate(PI).scale(0.26)
    return t.set_fill(style.RED, opacity=0.85).set_stroke(style.RED, width=2)


def arrow(a, b, color=style.CYAN):
    """A connector between two points (explicit ends, never connect() on squares)."""
    return style.glow_arrow(a, b, color=color, buff=0.0)


def label(text: str, color: str = style.WHITE, size: str = "label") -> Text:
    return style.label_text(text, color=color, size=size)


class S07Saas(BeatScene):
    section_id = "07_saas"
    title = "If you run a software company"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Now the first angle. Say you run a software company", self.b_angle,
                 note="product and customer, joined"),
            Beat("If the product can be copied in a week, the relationship", self.b_relationship,
                 note="a clone peels off the product; the link to the customer lights"),
            Beat("Here is what it rests on. Net revenue retention asks", self.b_nrr,
                 note="waterfall of NRR's parts, no numbers"),
            Beat("Across ChartMogul's data for 2025", self.b_median,
                 note="waffle: 82 of 100 filled"),
            Beat("AI-native apps", self.b_ai_native,
                 note="second waffle: 48 of 100, the other 52 red"),
            Beat("A larger company shows the same pressure more slowly", self.b_hubspot,
                 note="line: HubSpot NRR 103, 102, 101 over a white 100 line"),
            Beat("Over a hundred means existing customers still pay a little more", self.b_over,
                 note="the band over 100 shades green; gross retention, high 80s, under it"),
            Beat("Growth is slowing with it", self.b_growth,
                 note="area: revenue growth 21% to 17%, the 12% guide dashed"),
            Beat("Pricing is moving too", self.b_pricing,
                 note="slope chart: per seat 21 to 15, hybrid 27 to 41"),
            Beat("When you are paid for usage, you are paid only while", self.b_usage,
                 note="customer success moves from the cost bin to the revenue bin"),
            Beat("The new threat is an agent sitting between you", self.b_agent,
                 note="an agent diamond drops between product and customer"),
            Beat("One analyst argues that whoever owns the place where people act", self.b_middleware,
                 note="the agent lights; the product shrinks to middleware"),
            Beat("When Meta's booking agent was announced, travel stocks fell", self.b_travel,
                 note="a booking agent; three travel products, red falls"),
            Beat("So, as a founder, here is what I would do", self.b_founder,
                 note="four empty slots for the list"),
            Beat("Know every account by name, and what it gets from you", self.b_accounts),
            Beat("Become the record of the customer's decisions", self.b_record),
            Beat("Be the one who answers when it breaks", self.b_answer),
            Beat("And make the customer's agent a channel into your product", self.b_channel),
        ]

    # ------------------------------------------------------------ helpers --
    def _at(self, ctx, frac: float) -> None:
        """Wait until `frac` of this beat's window has passed (never past its end)."""
        lag = ctx.beat.start + frac * ctx.window - self.renderer.time
        if lag > 0.02:
            self.wait(lag)

    # ---------------------------------------------------------- relationship --
    def b_angle(self, ctx):
        a, b = ctx.budget(0.7, 0.6)
        product = style.node("product", size=2.0).move_to(LEFT * 3.4 + UP * 0.25)
        customer = style.node("customer", size=1.9).move_to(RIGHT * 3.4 + UP * 0.25)
        self.play(DrawBorderThenFill(product), FadeIn(customer, scale=0.85), run_time=a)
        link = arrow(product.get_right() + RIGHT * 0.12, customer.get_left() + LEFT * 0.12)
        self.play(GrowArrow(link[1]), FadeIn(link[0]), run_time=b)
        self._owned["pair"] = VGroup(product, customer)
        self._owned["link"] = link

    def b_relationship(self, ctx):
        product, customer = self._owned["pair"]
        link = self._owned["link"]
        clone = style.node("clone", size=2.0).move_to(product)
        self.add(clone)
        copied = label("copied in a week", style.BLUE)
        self.play(clone.animate.move_to(LEFT * 3.4 + DOWN * 1.35).scale(0.55),
                  product.animate.shift(UP * 0.5), customer.animate.shift(UP * 0.5),
                  link.animate.shift(UP * 0.5), run_time=0.9)
        copied.next_to(clone, RIGHT, buff=0.35)
        ctx.show(copied, tag="copied", run_time=0.4, nudge=False)
        self._owned["clone"] = clone
        self._at(ctx, 0.45)
        rel = label("the relationship", style.CYAN, size="caption")
        rel.next_to(link, UP, buff=0.3)
        ctx.show(rel, tag="rel", run_time=0.5, nudge=False)
        self._at(ctx, 0.7)
        self.play(link.animate.set_stroke(width=7), *style.highlight(customer, style.CYAN),
                  run_time=0.6)

    # ------------------------------------------------------------- retention --
    def b_nrr(self, ctx):
        """What net revenue retention is: a waterfall of its parts, no numbers."""
        ctx.clear_stage(run_time=0.4)
        steps = [("last year", 100), ("+ upgrades", 22), ("− downgrades", -9),
                 ("− cancellations", -15), ("this year", None)]
        bars = charts.waterfall(steps, unit=3.2 / 122, bar_w=1.2, gap=1.3)
        bars.move_to([0, -1.55 + bars.height / 2, 0])
        colors = [style.MUTED, style.GREEN, style.RED, style.RED, style.WHITE]
        names = VGroup(*[label(name, color).next_to([b.get_x(), -1.55, 0], DOWN, buff=0.22)
                         for (name, _), b, color in zip(steps, bars, colors)])
        head = label("net revenue retention", size="caption").move_to(UP * HEAD_Y)
        ctx.lopsided("the waterfall builds left to right, one part at a time")
        ctx.show(head, tag="head", run_time=0.5, nudge=False)
        self._owned["bars"] = VGroup(bars, names)
        for i, frac in enumerate((0.1, 0.26, 0.38, 0.5, 0.6)):
            self._at(ctx, frac)
            edge = DOWN if i in (0, 1, 4) else UP
            self.play(GrowFromEdge(bars[i], edge), FadeIn(names[i]), run_time=0.6)

    def _waffle(self, ctx, filled: int, name: str, x: float, tag: str) -> VGroup:
        """Show an empty waffle, then fill `filled` cells green. VGroup(cells, name, value)."""
        cells = charts.waffle(0, style.GREEN).move_to([x, -0.1, 0])
        head = label(name, size="caption").next_to(cells, UP, buff=0.3)
        value = label(f"{filled}%", style.GREEN, size="title").next_to(cells, DOWN, buff=0.25)
        ctx.show(cells, head, tag=tag, run_time=0.5, nudge=False)
        self._at(ctx, 0.3)
        self.play(LaggedStart(*[c.animate.set_fill(style.GREEN, opacity=0.85).set_stroke(style.GREEN, width=1)
                                for c in cells[:filled]], lag_ratio=0.02),
                  run_time=ctx.budget(1.6)[0])
        self.play(FadeIn(value, shift=UP * 0.1), run_time=0.4)
        self._owned[tag].add(value)
        return cells

    def b_median(self, ctx):
        ctx.clear_stage(run_time=0.4)
        ctx.lopsided("the first of two waffles stands on the left; the second arrives on the next line")
        cells = self._waffle(ctx, 82, "business software", -3.4, "w82")
        self._at(ctx, 0.75)
        # The 18 that went: red, as the next line's 52 will be.
        self.play(*[c.animate.set_stroke(style.RED, width=1.8) for c in cells[82:]], run_time=0.5)

    def b_ai_native(self, ctx):
        cells = self._waffle(ctx, 48, "AI-native apps", 3.4, "w48")
        self._at(ctx, 0.65)
        # "about half the money ... gone in a year": the other 52 outline in red.
        self.play(*[c.animate.set_stroke(style.RED, width=1.8) for c in cells[48:]], run_time=0.7)

    def b_hubspot(self, ctx):
        ctx.clear_stage(run_time=0.4)
        plot = charts.Plot([-5.6, -1.75, 0], 6.0, 3.5, (0.5, 3.5), (84, 108),
                           x_ticks=[(1, "Q1 2026"), (2, "Q2"), (3, "Q3")], y_ticks=[(100, "100%")])
        head = label("HubSpot net revenue retention").move_to([plot.at(2, 0)[0], HEAD_Y, 0])
        ctx.lopsided("the line chart sits left; the next line explains it in the space on the right")
        ctx.show(plot, head, tag="plot", run_time=0.6, nudge=False)
        self._plot = plot
        self._at(ctx, 0.12)
        ref = DashedLine(plot.at(0.5, 100), plot.at(3.5, 100), color=style.WHITE, stroke_width=2.4)
        ref.set_z_index(style.Z_EDGE)
        ctx.show(ref, tag="ref", anim=Create, run_time=0.6, nudge=False)
        points = [(1, 103), (2, 102), (3, 101)]
        dots = charts.dots(plot, points, radius=0.11)
        path = charts.line(plot, points)
        first = label("103%", size="caption").next_to(dots[0], UP, buff=0.22)
        last = label("101%", size="caption").next_to(dots[2], UP, buff=0.22)
        self._at(ctx, 0.28)
        ctx.show(dots[0], first, tag="q1", anim=lambda m: FadeIn(m, scale=0.7), run_time=0.5, nudge=False)
        self._at(ctx, 0.44)
        self.play(Create(path), FadeIn(dots[1]), run_time=ctx.budget(1.0)[0], rate_func=linear)
        self.play(FadeIn(dots[2], scale=0.7), FadeIn(last), run_time=0.5)
        self._owned["q3"] = VGroup(path, dots[1:], last)
        self._at(ctx, 0.8)
        self.play(Indicate(dots[2], color=style.GREEN, scale_factor=1.6), run_time=0.6)

    def b_over(self, ctx):
        plot = self._plot
        col_x = 1.0
        above = Rectangle(width=plot.w, height=plot.at(0, 108)[1] - plot.at(0, 100)[1])
        above.set_fill(style.GREEN, opacity=0.14).set_stroke(width=0)
        above.move_to(plot.at(0.5, 100), aligned_edge=DL).set_z_index(style.Z_BACKDROP)
        more = label("paying a little more", style.GREEN)
        more.move_to([col_x, plot.at(0, 103)[1], 0], aligned_edge=LEFT)
        ctx.show(above, more, tag="above", run_time=0.6, nudge=False)
        self._at(ctx, 0.38)
        # "held in the high eighties": a band, 86 to 89, not a line at a number not said.
        gross = Rectangle(width=plot.w, height=plot.at(0, 89)[1] - plot.at(0, 86)[1])
        gross.set_fill(style.GREEN, opacity=0.4).set_stroke(style.GREEN, width=1.6)
        gross.move_to(plot.at(0.5, 86), aligned_edge=DL).set_z_index(style.Z_BACKDROP)
        gname = label("gross retention: high 80s", style.GREEN)
        gname.move_to([col_x, gross.get_y(), 0], aligned_edge=LEFT)
        self.play(GrowFromEdge(gross, LEFT), FadeIn(gname), run_time=ctx.budget(0.8)[0])
        self._owned["gross"] = VGroup(gross, gname)
        self._at(ctx, 0.66)
        why = style.text_rows(label("leaving no faster,", size="caption"), label("buying less new", size="caption"))
        why.move_to([col_x, plot.at(0, 95)[1], 0], aligned_edge=LEFT)
        ctx.show(why, tag="why", anim=lambda m: FadeIn(m, shift=RIGHT * 0.2), run_time=0.5, nudge=False)

    def b_growth(self, ctx):
        """Revenue growth as an area, shrinking; the company's own guide dashed."""
        ctx.clear_stage(run_time=0.4)
        plot = charts.Plot([-4.6, -1.75, 0], 9.6, 3.4, (0, 8), (0, 30),
                           x_ticks=[(0, "Q4 2024"), (7, "now"), (8, "next")], y_title="revenue growth")
        ctx.lopsided("the area grows from the left edge of its axes across the stage")
        ctx.show(plot, tag="plot", run_time=0.5, nudge=False)
        self._at(ctx, 0.12)
        solid = Polygon(plot.at(0, 0), plot.at(0, 21), plot.at(7, 17), plot.at(7, 0))
        solid.set_fill(style.GREEN, opacity=0.3).set_stroke(width=0).set_z_index(style.Z_BACKDROP)
        top = charts.line(plot, [(0, 21), (7, 17)])
        start = label("21%", size="caption").next_to(plot.at(0, 21), LEFT, buff=0.2)
        ctx.show(start, tag="start", run_time=0.4, nudge=False)
        self._at(ctx, 0.3)
        self.play(GrowFromEdge(solid, LEFT), Create(top), run_time=ctx.budget(1.6)[0], rate_func=linear)
        now = label("17%", size="caption").next_to(plot.at(7, 17), UR, buff=0.12)
        self.play(FadeIn(now), run_time=0.4)
        self._owned["solid"] = VGroup(solid, top, now)
        self._at(ctx, 0.66)
        guide = Polygon(plot.at(7, 0), plot.at(7, 17), plot.at(8, 12), plot.at(8, 0))
        guide.set_fill(style.MUTED, opacity=0.12).set_stroke(width=0).set_z_index(style.Z_BACKDROP)
        edge = DashedLine(plot.at(7, 17), plot.at(8, 12), color=style.WHITE, stroke_width=3)
        edge.set_z_index(style.Z_EDGE)
        nxt = label("12%", size="caption").next_to(plot.at(8, 12), RIGHT, buff=0.2)
        gl = label("its guide", style.MUTED).next_to(nxt, DOWN, buff=0.2).align_to(nxt, LEFT)
        ctx.show(guide, edge, nxt, gl, tag="guide", run_time=0.6, nudge=False)

    def b_pricing(self, ctx):
        ctx.clear_stage(run_time=0.4)
        base, height, lx, rx = -1.75, 3.4, -1.6, 3.2
        pairs = charts.slope([21, 27], [15, 41], [style.RED, style.GREEN], lo=10, hi=45,
                             height=height, gap=rx - lx).shift(UP * base + RIGHT * (lx + rx) / 2)
        # The two years as faint bands, not hairlines: before the rows arrive, the bands are what
        # balances the headings above and the claim footer below (hairlines left it 61% off centre).
        rails = VGroup(*[style.tile(0.8, height, style.GRID, opacity=0.2).move_to([x, base + height / 2, 0])
                         for x in (lx, rx)]).set_z_index(style.Z_BACKDROP)
        heads = VGroup(label("share of firms", style.MUTED, size="caption").move_to([-4.2, HEAD_Y, 0]),
                       label("a year ago", style.MUTED).move_to([lx, HEAD_Y, 0]),
                       label("now", style.MUTED).move_to([rx, HEAD_Y, 0]))
        ctx.show(rails, heads, tag="cols", run_time=0.5, nudge=False)
        rows = [(pairs[0], "21%", "15%", "pure per seat"), (pairs[1], "27%", "41%", "subscription + usage")]
        # The second row a little ahead of its words, so 41% has settled by three quarters of the line.
        for (pair, a, b, name), (t0, t1) in zip(rows, ((0.2, 0.36), (0.55, 0.66))):
            left_dot, right_dot, seg = pair
            color = left_dot.get_color()
            va = label(a, color, size="caption").next_to(left_dot, LEFT, buff=0.4)
            nm = label(name, color).next_to(va, LEFT, buff=0.3)
            vb = label(b, color, size="caption").next_to(right_dot, RIGHT, buff=0.4)
            self._at(ctx, t0)
            self.play(FadeIn(nm), FadeIn(left_dot, scale=0.6), FadeIn(va), run_time=0.4)
            self._at(ctx, t1)
            self.play(Create(seg), run_time=ctx.budget(0.8)[0])
            self.play(FadeIn(right_dot, scale=0.6), FadeIn(vb), run_time=0.4)
            self._owned[name] = VGroup(pair, va, vb, nm)

    def b_usage(self, ctx):
        # Product left and customer right, as on either side of this beat; the money flows back.
        # No green: this line is a guess, and green is for measured figures.
        ctx.clear_stage(run_time=0.4)
        product = style.node("product", size=1.6).move_to(LEFT * 4.6 + UP * 0.9)
        customer = style.node("customer", size=1.6).move_to(RIGHT * 4.6 + UP * 0.9)
        flow = arrow(customer.get_left() + LEFT * 0.12, product.get_right() + RIGHT * 0.12)
        val = label("paid while they use you").next_to(flow, UP, buff=0.25)
        you = label("your product", style.BLUE, size="caption").next_to(product, DOWN, buff=0.2)
        them = label("customer", style.CYAN, size="caption").next_to(customer, DOWN, buff=0.2)
        ctx.show(customer, product, flow, val, you, them, tag="flow", run_time=0.7, nudge=False)
        self._at(ctx, 0.35)
        cost = style.tile(4.2, 0.95, style.MUTED, opacity=0.08).move_to(LEFT * 2.6 + DOWN * 1.35)
        rev = style.tile(4.2, 0.95, style.WHITE, opacity=0.12).move_to(RIGHT * 2.6 + DOWN * 1.35)
        cl = label("cost", style.MUTED).next_to(cost, DOWN, buff=0.18)
        rl = label("revenue").next_to(rev, DOWN, buff=0.18)
        cs = label("customer success", style.MUTED, size="caption").move_to(cost)
        ctx.show(cost, rev, cl, rl, tag="bins", run_time=0.5, nudge=False)
        style.allow_overlap(cs, cost, reason="the label sits inside its bin")
        self.play(FadeIn(cs), run_time=0.4)
        self._at(ctx, 0.62)
        self.play(cs.animate.move_to(rev).set_color(style.WHITE), run_time=1.0)
        self._owned["cs"] = cs

    # ----------------------------------------------------------------- agent --
    def b_agent(self, ctx):
        ctx.clear_stage(run_time=0.35)
        product = style.node("product", size=1.8).move_to(LEFT * 4.6)
        customer = style.node("customer", size=1.7).move_to(RIGHT * 4.6)
        you = label("you", style.BLUE).next_to(product, DOWN, buff=0.25)
        self._you = you
        them = label("your customer", style.CYAN).next_to(customer, DOWN, buff=0.25)
        ctx.show(product, customer, you, them, tag="ends", run_time=0.5, nudge=False)
        agent = style.node("agent", "agent", size=1.6).move_to(UP * 1.6)
        a1 = arrow(product.get_right() + RIGHT * 0.12, LEFT * 0.85)
        a2 = arrow(RIGHT * 0.85, customer.get_left() + LEFT * 0.12)
        self.play(FadeIn(agent, shift=DOWN * 0.3), run_time=ctx.budget(0.5)[0])
        self.play(agent.animate.move_to(ORIGIN), FadeIn(a1), FadeIn(a2), run_time=0.6)
        self._owned["agent"] = VGroup(agent, a1, a2)
        self._owned["prod"] = product

    def b_middleware(self, ctx):
        agent, a1, a2 = self._owned["agent"]
        product = self._owned["prod"]
        profit = label("takes the profit", style.VIOLET, size="caption").next_to(agent, UP, buff=0.35)
        self.play(*style.highlight(agent, style.VIOLET), FadeIn(profit), run_time=0.6)
        self._owned["profit"] = profit
        self._at(ctx, 0.5)
        mid = label("middleware", style.MUTED, size="caption")
        target = product.copy().scale(0.55).set_opacity(0.45)
        mid.next_to(target, DOWN, buff=0.25)
        self.play(Transform(product, target), FadeOut(self._you), run_time=0.8)
        self.play(FadeIn(mid), run_time=0.4)
        self._owned["mid"] = mid

    def b_travel(self, ctx):
        ctx.clear_stage(run_time=0.35)
        # Above centre: the falls and the passivity line hang below, over the claim footer.
        agent = style.node("agent", size=1.6).move_to(LEFT * 3.0 + UP * 0.75)
        al = label("booking agent", style.VIOLET).next_to(agent, DOWN, buff=0.25)
        ctx.show(agent, al, tag="bag", run_time=0.5, nudge=False)
        self._at(ctx, 0.3)
        trips = VGroup(*[style.node("product", size=1.0) for _ in range(3)])
        trips.arrange(RIGHT, buff=0.9).move_to(RIGHT * 2.0 + UP * 0.75)
        tl = label("travel stocks", style.BLUE).next_to(trips, UP, buff=0.3)
        ctx.show(trips, tl, tag="trips", run_time=0.5, nudge=False)
        falls = VGroup(*[fall().next_to(t, DOWN, buff=0.25) for t in trips])
        self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.25) for f in falls], lag_ratio=0.3),
                  trips.animate.shift(DOWN * 0.15), run_time=0.9)
        self._owned["falls"] = falls
        self._at(ctx, 0.68)
        passive = label("built on customer passivity", style.RED, size="caption")
        passive.next_to(falls, DOWN, buff=0.3)
        ctx.show(passive, tag="passive", run_time=0.5, nudge=False)

    # ------------------------------------------------------------- the list --
    ROWS_Y = [1.5, 0.5, -0.5, -1.5]
    ITEMS = [
        ("customer", "know every account by name"),
        ("moat", "be the record of decisions"),
        ("moat", "answer when it breaks"),
        ("agent", "their agent as a channel"),
    ]

    def _item(self, i: int) -> VGroup:
        kind, words = self.ITEMS[i]
        row = VGroup(style.node(kind, size=0.62), label(words, size="caption")).arrange(RIGHT, buff=0.45)
        row.move_to([0, self.ROWS_Y[i], 0]).align_to(LEFT * 3.6, LEFT)
        return row

    def b_founder(self, ctx):
        ctx.clear_stage(run_time=0.4)
        slots = VGroup(*[style.tile(9.4, 0.7, style.GRID, opacity=0.25).move_to([0.9, y, 0])
                         for y in self.ROWS_Y])
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in slots], lag_ratio=0.15),
                  run_time=ctx.budget(0.9)[0])
        self._owned["slots"] = slots

    def _add_item(self, ctx, i: int, run_time: float = 0.5):
        row = self._item(i)
        style.allow_overlap(row, self._owned["slots"][i], reason="each item sits in its slot")
        ctx.show(row, tag=f"item{i}", anim=lambda m: FadeIn(m, shift=RIGHT * 0.25),
                 run_time=run_time, nudge=False)
        return row

    def b_accounts(self, ctx):
        row = self._add_item(ctx, 0)
        self._at(ctx, 0.55)
        self.play(*style.highlight(row[0], style.CYAN), run_time=0.5)

    def b_record(self, ctx):
        row = self._add_item(ctx, 1)
        self._at(ctx, 0.4)
        who = label("who · what · why", style.MUTED).next_to(row, RIGHT, buff=0.5)
        style.allow_overlap(who, self._owned["slots"][1], reason="the detail sits in its item's slot")
        ctx.show(who, tag="who", run_time=0.4, nudge=False)
        self._at(ctx, 0.75)
        self.play(*style.highlight(row[0], style.GOLD), run_time=0.5)

    def b_answer(self, ctx):
        ctx.retire("who", run_time=0.3)
        row = self._add_item(ctx, 2)
        self._at(ctx, 0.6)
        self.play(*style.highlight(row[0], style.GOLD), run_time=0.5)

    def b_channel(self, ctx):
        row = self._add_item(ctx, 3)
        self._at(ctx, 0.55)
        self.play(*style.highlight(row[0], style.VIOLET), run_time=0.5)
