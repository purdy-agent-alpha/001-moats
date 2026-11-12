"""
Section 02: what a moat is.

The word (a gold hexagon, Buffett), his 2007 letter as a record card, the castle
with clones stopping at its ring, Helmer's persistent returns as two lines with
the gap between them filled, the castle keeping its customers from a new
product, Morningstar's five sources on a pentagon, narrow and wide moats as
ranges on a time axis, a moat rebuilt in a loop that fades each turn, and the
five sources in a row under the section's question.

Every wait inside a beat is a fraction of its window (`_at`), so a re-timed
voice needs no edit.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from moats_video.pipeline import charts, style
from moats_video.pipeline.beats import Beat, BeatScene

# Morningstar's five sources, in the order the narration names them.
SOURCES = ["brands and licences", "switching costs", "network effects", "lower costs", "niche markets"]


def castle(centre, ring: float = 3.4, product: float = 1.3) -> VGroup:
    """VGroup(ring, product): a product inside an unfilled gold hexagon, the ring drawn behind."""
    moat = style.node("moat", size=ring).move_to(centre)
    moat[1].set_fill(opacity=0.0)
    moat.set_z_index(style.Z_BACKDROP, family=True)
    return VGroup(moat, style.node("product", size=product).move_to(centre))


class S02Moat(BeatScene):
    section_id = "02_moat"
    title = "What a moat is"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Investors took the word from Warren Buffett", self.b_word,
                 note="a gold hexagon, moat; Buffett under it"),
            # The first line is short and its source chip long: start this beat a little after its line,
            # so the chip stays up long enough to read.
            Beat("In his 2007 letter he wrote", self.b_letter, lead=-1.3,
                 note="a record card: an enduring moat, Berkshire letter 2007"),
            Beat("Picture a castle earning good money", self.b_castle,
                 note="a product in a gold ring; three clones approach and stop at the ring"),
            Beat("The strategist Hamilton Helmer", self.b_helmer,
                 note="returns over time: a line that stays high, a rival climbing and stopping short; "
                      "the gap fills and persistent lights"),
            Beat("So a good product is not a moat", self.b_product,
                 note="a new product appears; the customers lean to it and come back to the castle"),
            Beat("Morningstar, which rates moats for investors", self.b_sources,
                 note="five hexagons on a pentagon round a centre, named as the line names them"),
            Beat("A wide moat, in its terms", self.b_wide,
                 note="a time axis 0 to 25 years: narrow to 10, wide past 20"),
            Beat("Buffett adds a warning", self.b_rebuilt,
                 note="a moat inside a looping arrow, fading each turn, then struck"),
            Beat("So the question under this video", self.b_question,
                 note="the five hexagons in a row; the product shrinks, cost to 0; a question mark"),
        ]

    def _at(self, ctx, frac: float, run_time: float = 0.6) -> float:
        """Wait until `frac` of this beat's window has passed; return `run_time` cut to what is left."""
        lag = ctx.beat.start + frac * ctx.window - self.renderer.time
        if lag > 0.02:
            self.wait(lag)
        left = ctx.beat.start + ctx.window - self.renderer.time - 0.1
        return max(min(run_time, left), 0.08)

    # ---------------------------------------------------------------- beats --
    def b_word(self, ctx):
        moat = style.node("moat", "moat", size=2.4, font_size=32).move_to(UP * 0.35)
        who = style.label_text("Buffett", color=style.WHITE, size="caption").next_to(moat, DOWN, buff=0.35)
        a, b = ctx.budget(0.9, 0.5)
        self.play(DrawBorderThenFill(moat), run_time=a)
        ctx.show(who, tag="who", anim=lambda m: FadeIn(m, shift=UP * 0.1), run_time=b, nudge=False)
        self._owned["moat"] = moat

    def b_letter(self, ctx):
        moat = self._owned["moat"]
        ctx.retire("who", run_time=0.3)
        self.play(moat.animate.scale(0.75).move_to(LEFT * 3.8 + UP * 0.2), run_time=ctx.budget(0.6)[0])
        quote = style.caption_text("“an enduring moat”")
        source = style.label_text("Berkshire letter, 2007", color=style.MUTED)
        lines = style.text_rows(quote, source)
        card = style.node("figure", size=3.7, color=style.MUTED)
        card.stretch_to_fit_height(lines.height + 0.9)
        card.move_to(RIGHT * 1.9 + UP * 0.2)
        lines.move_to(card)
        ctx.show(VGroup(card, lines), tag="card", anim=lambda m: FadeIn(m, shift=LEFT * 0.3),
                 run_time=0.7, nudge=False)
        # "a truly great business must have an enduring moat": a gold line under "enduring".
        # (Recolouring a slice of the Text's glyphs detaches them: the gate then reads the quote as gone.)
        y = quote.get_bottom()[1] - 0.07
        under = Line([quote[3].get_left()[0], y, 0], [quote[10].get_right()[0], y, 0],
                     color=style.GOLD, stroke_width=4)
        self.play(Create(under), run_time=self._at(ctx, 0.42, 0.5))
        self._owned["under"] = under
        # "one that protects excellent returns on capital"
        ctx.play(*style.highlight(moat, style.GOLD), run_time=self._at(ctx, 0.72, 0.5))

    def b_castle(self, ctx):
        ctx.clear_stage(run_time=0.35)
        centre = UP * 0.2
        home = castle(centre)
        ctx.waive("node_overlap", "the hexagon is drawn round the product on purpose: a castle and its moat")
        self.play(GrowFromCenter(home[0]), DrawBorderThenFill(home[1]), run_time=ctx.budget(0.9)[0])
        self._owned["castle"] = home
        # "Competitors will keep attacking it"
        stops = [LEFT * 2.35 + UP * 0.95, LEFT * 2.35 + DOWN * 0.55, RIGHT * 2.55 + UP * 0.2]
        clones = VGroup(*[style.node("clone", size=1.1).move_to(p + np.sign(p[0]) * RIGHT * 3.4)
                          for p in stops])
        self.play(FadeIn(clones), run_time=self._at(ctx, 0.3, 0.4))
        self.play(*[c.animate.move_to(p) for c, p in zip(clones, stops)],
                  run_time=self._at(ctx, 0.35, 1.4), rate_func=rush_into)
        self._owned["clones"] = clones
        # "the moat is what makes their life difficult": the ring lights, they fall back.
        ctx.play(*style.highlight(home[0], style.GOLD),
                 *[c.animate.shift(np.sign(c.get_x()) * RIGHT * 0.45) for c in clones],
                 run_time=self._at(ctx, 0.72, 0.6))

    def b_helmer(self, ctx):
        ctx.clear_stage(run_time=0.35)
        plot = charts.Plot(LEFT * 5.4 + DOWN * 1.75, 9.4, 3.7, (0, 10), (0, 1), y_title="returns")
        # "time" under the axis end, not above it where the filled gap's edge would cut through it.
        corner = plot.at(10, 0)
        time = style.label_text("time", color=style.MUTED, size="tiny").next_to(corner, DOWN, buff=0.18)
        time.align_to(corner, RIGHT)
        ctx.lopsided("a line chart across the stage: the source chip in the caption lane outweighs its thin lines")
        ctx.show(plot, time, tag="plot", run_time=0.7, nudge=False)
        high = 0.8
        # White, not green: a conceptual line, no measured data behind it.
        ours = charts.line(plot, [(0, high), (10, high)], color=style.WHITE)
        power = style.label_text("power", color=style.GOLD).next_to(plot.at(10, high), RIGHT, buff=0.25)
        self.play(Create(ours), FadeIn(power), run_time=self._at(ctx, 0.08, 1.6), rate_func=linear)
        self._owned["ours"] = VGroup(ours, power)
        # "the conditions that create the potential for persistent differential returns"
        rival_pts = [(1.0, 0.06), (3.0, 0.3), (5.0, 0.48), (7.0, 0.56), (10.0, 0.6)]
        rival = DashedVMobject(charts.line(plot, rival_pts, color=style.BLUE), num_dashes=40)
        rival.set_z_index(style.Z_EDGE)
        name = style.label_text("rival", color=style.BLUE).next_to(plot.at(10, 0.6), RIGHT, buff=0.25)
        self.play(Create(rival), run_time=self._at(ctx, 0.3, 2.6), rate_func=rush_from)
        self.play(FadeIn(name), run_time=0.3)
        self._owned["rival"] = VGroup(rival, name)
        gap = Polygon(*[plot.at(x, high) for x in (1.0, 10.0)],
                      *[plot.at(x, y) for x, y in reversed(rival_pts)])
        gap.set_fill(style.GOLD, opacity=0.2).set_stroke(width=0)
        gap.set_z_index(style.Z_BACKDROP)
        self.play(FadeIn(gap), run_time=self._at(ctx, 0.62, 0.7))
        self._owned["gap"] = gap
        # "Persistent is the word that matters."
        word = style.caption_text("persistent", color=style.GOLD).move_to(plot.at(7.6, 0.69))
        ctx.show(word, tag="word", anim=lambda m: FadeIn(m, scale=1.2), run_time=self._at(ctx, 0.8, 0.5),
                 nudge=False)
        ctx.play(gap.animate.set_fill(opacity=0.32), run_time=self._at(ctx, 0.92, 0.4))

    def b_product(self, ctx):
        ctx.clear_stage(run_time=0.35)
        home = castle(LEFT * 3.9 + UP * 0.2, ring=3.2, product=1.2)
        ctx.waive("node_overlap", "the hexagon is drawn round the product on purpose: a castle and its moat")
        ys = [1.3, 0.55, -0.2, -0.95]
        customers = VGroup(*[style.node("customer", size=0.55).move_to([-1.0 + 0.25 * (i % 2), y, 0])
                             for i, y in enumerate(ys)])
        self.play(FadeIn(home), FadeIn(customers), run_time=ctx.budget(0.6)[0])
        self._owned["castle"] = VGroup(home, customers)
        # "So a good product is not a moat": a new product, no ring round it.
        new = style.node("product", size=1.6).move_to(RIGHT * 3.9 + UP * 0.2)
        good = style.label_text("a good product", color=style.BLUE).next_to(new, DOWN, buff=0.3)
        ctx.show(VGroup(new, good), tag="new", anim=lambda m: FadeIn(m, shift=LEFT * 0.6),
                 run_time=self._at(ctx, 0.08, 0.7), nudge=False)
        # "the moat is why your customers do not walk over to the new one"
        self.play(customers.animate.shift(RIGHT * 1.3), run_time=self._at(ctx, 0.5, 0.9))
        self.play(customers.animate.shift(LEFT * 1.3), *style.highlight(home[0], style.GOLD),
                  run_time=self._at(ctx, 0.68, 0.9))

    def b_sources(self, ctx):
        ctx.clear_stage(run_time=0.35)
        centre = DOWN * 0.1
        # Clockwise from the top: the order the narration names them.
        angles = [PI / 2 - TAU * i / 5 for i in range(5)]
        points = [centre + np.array([3.0 * np.cos(a), 1.6 * np.sin(a), 0]) for a in angles]
        sides = [RIGHT, RIGHT, RIGHT, LEFT, LEFT]
        hub = Dot(centre, radius=0.1, color=style.GOLD)
        slots = VGroup(*[RegularPolygon(n=6, radius=0.55, color=style.DIM).set_stroke(width=2).move_to(p)
                         for p in points])
        spokes = VGroup(*[Line(centre, p, buff=0.6, color=style.DIM, stroke_width=2) for p in points])
        spokes.set_z_index(style.Z_BACKDROP)
        self.play(FadeIn(hub), Create(spokes), FadeIn(slots), run_time=ctx.budget(0.8)[0])
        self._owned["frame"] = VGroup(hub, spokes, slots)
        # "names five sources: brands, patents and licences; switching costs; ..."
        for i, (p, side, word, frac) in enumerate(zip(points, sides, SOURCES, (0.25, 0.37, 0.48, 0.58, 0.67))):
            hexagon = style.node("moat", size=1.1).move_to(p)
            label = style.label_text(word, color=style.WHITE).next_to(hexagon, side, buff=0.25)
            ctx.show(VGroup(hexagon, label), tag=f"source{i}", anim=lambda m: FadeIn(m, scale=0.8),
                     run_time=self._at(ctx, frac, 0.5), nudge=False)
        ctx.play(*style.highlight(hub, style.GOLD), run_time=self._at(ctx, 0.9, 0.4))

    def b_wide(self, ctx):
        ctx.clear_stage(run_time=0.35)
        plot = charts.Plot(LEFT * 4.4 + DOWN * 1.6, 9.8, 3.4, (0, 25), (0, 2),
                           x_ticks=[(0, "0"), (10, "10"), (20, "20")], x_title="years")
        rows = {"narrow": 1.45, "wide": 0.55}
        names = VGroup(*[style.label_text(n, color=style.WHITE).next_to(plot.at(0, y), LEFT, buff=0.3)
                         for n, y in rows.items()])
        ctx.lopsided("a time axis across the stage: the source chip in the caption lane outweighs its thin lines")
        ctx.show(VGroup(plot, names), tag="plot", run_time=0.6, nudge=False)

        def span(x0, x1, y, opacity=0.35):
            bar = style.tile(plot.at(x1, y)[0] - plot.at(x0, y)[0], 0.55, style.GOLD, opacity=opacity)
            return bar.move_to((plot.at(x0, y) + plot.at(x1, y)) / 2)

        narrow = span(0, 10, rows["narrow"])
        self.play(GrowFromEdge(narrow, LEFT), run_time=self._at(ctx, 0.1, 0.9))
        # "is one expected to last more than twenty years"
        wide = span(0, 20, rows["wide"])
        self.play(GrowFromEdge(wide, LEFT), run_time=self._at(ctx, 0.25, 1.4))
        beyond = DashedVMobject(span(20, 25, rows["wide"], opacity=0.0), num_dashes=24)
        self.play(Create(beyond), run_time=self._at(ctx, 0.45, 0.6))
        self._owned["spans"] = VGroup(narrow, wide, beyond)
        # "A moat is a measure of time": a marker runs along the axis.
        marker = Dot(plot.at(0, 0), radius=0.12, color=style.GOLD)
        self.play(FadeIn(marker), run_time=self._at(ctx, 0.62, 0.2))
        self.play(marker.animate.move_to(plot.at(25, 0)), plot.labels[-1].animate.set_color(style.GOLD),
                  run_time=self._at(ctx, 0.65, 1.8), rate_func=linear)
        self._owned["marker"] = marker

    def b_rebuilt(self, ctx):
        ctx.clear_stage(run_time=0.35)
        centre = UP * 0.25
        moat = style.node("moat", size=2.0).move_to(centre)
        loop = Arc(radius=1.7, start_angle=PI / 2, angle=TAU * 0.8, color=style.BLUE, stroke_width=4)
        loop.add_tip(tip_length=0.28, tip_width=0.28)
        loop.move_arc_center_to(centre)
        loop.set_z_index(style.Z_EDGE, family=True)
        rebuilt = style.label_text("continuously rebuilt", color=style.MUTED).next_to(loop, DOWN, buff=0.3)
        self.play(FadeIn(moat), Create(loop), FadeIn(rebuilt), run_time=ctx.budget(0.8)[0])
        self._owned["loop"] = VGroup(moat, loop, rebuilt)
        # "a moat that must be continuously rebuilt": each turn of the loop leaves the moat fainter.
        for frac, opacity in ((0.08, 0.65), (0.24, 0.4), (0.4, 0.18)):
            self.play(Rotate(loop, TAU, about_point=centre), moat.animate.set_opacity(opacity),
                      run_time=self._at(ctx, frac, 1.2))
        # "will eventually be no moat at all": struck as it is said, then the loop stops.
        cut = style.strike(moat[1])
        self.play(Create(cut), run_time=self._at(ctx, 0.55, 0.4))
        self._owned["cut"] = cut
        ctx.play(loop.animate.set_color(style.DIM),
                 run_time=self._at(ctx, 0.72, 0.6))

    def b_question(self, ctx):
        ctx.clear_stage(run_time=0.35)
        xs = [-5.0, -2.5, 0.0, 2.5, 5.0]
        hexes = VGroup(*[style.node("moat", size=1.05).move_to([x, -0.05, 0]) for x in xs])
        # Labels at the legible size are wider than a column: alternate them in two rows.
        names = VGroup(*[style.label_text(w, color=style.WHITE).next_to(h, DOWN, buff=0.25 + 0.45 * (i % 2))
                         for i, (w, h) in enumerate(zip(SOURCES, hexes))])
        self.play(LaggedStart(*[FadeIn(VGroup(h, n), shift=UP * 0.2) for h, n in zip(hexes, names)],
                              lag_ratio=0.15), run_time=ctx.budget(1.0)[0])
        self._owned["row"] = VGroup(hexes, names)
        # "when building the castle costs almost nothing"
        # The product on the left and the question on the right, balanced over the row.
        product = style.node("product", size=1.1).move_to([-3.7, 1.6, 0])
        cost = style.label_text("cost → 0", color=style.BLUE).next_to(product, RIGHT, buff=0.35)
        ctx.show(product, tag="product", run_time=self._at(ctx, 0.2, 0.4), nudge=False)
        self.play(product.animate.scale(0.3), FadeIn(cost), run_time=self._at(ctx, 0.3, 1.2))
        self._owned["cost"] = cost
        # "which barriers still buy time?"
        ask = style.label_text("?", color=style.GOLD, size="title").move_to([2.6, 1.6, 0])
        ctx.show(ask, tag="ask", anim=lambda m: FadeIn(m, scale=1.4), run_time=self._at(ctx, 0.62, 0.4),
                 nudge=False)
        self.play(LaggedStart(*[style.highlight(h, style.GOLD)[0] for h in hexes], lag_ratio=0.2),
                  run_time=self._at(ctx, 0.72, 1.2))
