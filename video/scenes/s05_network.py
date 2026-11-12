"""
Section 05: network effects.

Levi's question, a network growing link by link, Stack Overflow's ask-and-answer
loop, then its fall as an area chart (linear axis: the drop is the point). Its
answers flow into an AI model and the crowd drifts apart. What holds is a live
connection: Levi's phrase, his three examples as small networks, Meta's users
against an empty clone, and PJM's mesh inside its agreement, read word by word.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from moats_video.pipeline import charts, style
from moats_video.pipeline.beats import Beat, BeatScene

# Stack Overflow, new questions a month (S54 and the research notes).
QUESTIONS = [(2014.17, 207204), (2020.75, 141749), (2024.75, 23162), (2025.75, 5263), (2026.5, 1442)]
CHATGPT = 2022.87                  # November 2022

# A network that grows: the first three are joined to each other, every later
# one to its three nearest elders.
GROW = [(-0.6, 0.3), (0.8, 0.9), (0.6, -0.7), (-1.9, 1.2), (-2.0, -0.9), (2.1, 0.1),
        (-0.4, 1.7), (-0.5, -1.7), (-3.4, 0.2), (3.4, 1.2), (3.2, -1.2), (1.6, -1.7)]

PJM_C = np.array([0.6, -0.05, 0.0])  # centre of the PJM boundary
PJM_R = 2.2


def nearest_edges(points, d: float) -> list[tuple[int, int]]:
    """Every pair of points closer than `d`."""
    pts = [np.array(p, dtype=float) for p in points]
    return [(i, j) for i in range(len(pts)) for j in range(i + 1, len(pts))
            if np.linalg.norm(pts[i] - pts[j]) < d]


def flat_card(text: str) -> VGroup:
    """A record card one line high: the card's frame is squashed, its label kept."""
    card = style.node("figure", text, size=2.9, font_size=22)
    for part in card[:2]:
        part.stretch_to_fit_height(0.55)
    return card


def flash(links: VGroup, color: str, run_time: float) -> ShowPassingFlash:
    """Something passing along every link at once: a live connection, or current."""
    return ShowPassingFlash(links.copy().set_stroke(color, width=5, opacity=1), time_width=0.45,
                            run_time=run_time)


class S05Network(BeatScene):
    section_id = "05_network"
    title = "Network effects"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Levi questioned network effects", self.b_ask,
                 note="Levi, a network-effects hexagon with a question mark, Stack Overflow"),
            Beat("A network effect is when a product is worth more", self.b_grow,
                 note="a network grows from 3 to 12 nodes, links multiplying as each joins"),
            Beat("Stack Overflow had one", self.b_loop,
                 note="asking and answering groups, arrows looping between them, each side growing"),
            Beat("New questions peaked", self.b_peak,
                 note="area chart of new questions a month, 2014 peak 207,000, drawn on to Oct 2025"),
            Beat("In July 2026 there were about fourteen hundred", self.b_now,
                 note="the area runs to Jul 2026; the last point red, 1,400"),
            Beat("The fall began years earlier", self.b_chatgpt,
                 note="dashed marker ChatGPT, Nov 2022; the area after it red"),
            Beat("Stack Overflow now gives AI companies", self.b_licence,
                 note="a stack of answer cards flows into an AI-model diamond: access, by partnership; OpenAI"),
            Beat("My reading: what people came for", self.b_reading,
                 note="the cards are copied into the model; the crowd dims and drifts apart"),
            Beat("So the network effect that holds is a live connection", self.b_live,
                 note="a network whose links pulse"),
            Beat("Levi put it as connected, permitted capacity", self.b_phrase,
                 note="Levi; connected · permitted · capacity = network effect"),
            Beat("His examples: Bitcoin", self.b_examples,
                 note="three small networks: Bitcoin ring, Facebook cluster, the grid's mesh"),
            Beat("Meta's apps are used by three point six billion", self.b_meta,
                 note="Meta's app full of people, 3.6 billion a day; an empty clone, 0"),
            Beat("To join PJM", self.b_pjm,
                 note="a mesh inside a gold boundary; a company signs the operating agreement at the gate "
                      "and joins; 1,116 members, 67 million people"),
            Beat("Read his phrase word by word", self.b_words,
                 note="connected (links pulse), permitted (the agreement), capacity (current flows); "
                      "a clone outside gets none of the three"),
        ]

    # ------------------------------------------------------------ helpers --
    def _at(self, ctx, frac: float) -> None:
        """Wait until `frac` of this beat's window has passed (never past its end)."""
        lag = ctx.beat.start + frac * ctx.window - self.renderer.time
        if lag > 0.02:
            self.wait(lag)

    # ---------------------------------------------------------------- beats --
    def b_ask(self, ctx):
        levi = style.node("person", "Levi", size=1.5, font_size=26).move_to(LEFT * 4.4 + UP * 0.3)
        ask = style.node("moat", "?", size=1.6, font_size=40).move_to(UP * 0.3)
        ask_name = style.label_text("network effects", color=style.GOLD).next_to(ask, DOWN, buff=0.3)
        arrow = style.connect(levi, ask, color=style.WHITE)
        ctx.show(levi, tag="levi", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.5)
        self.play(GrowArrow(arrow[1]), FadeIn(arrow[0]), FadeIn(ask, scale=0.85), FadeIn(ask_name),
                  run_time=ctx.budget(0.7)[0])
        self._owned["ask"] = VGroup(arrow, ask, ask_name)
        self._at(ctx, 0.45)
        so = style.node("product", size=1.3).move_to(RIGHT * 4.4 + UP * 0.3)
        so_name = style.label_text("Stack Overflow", color=style.BLUE).next_to(so, DOWN, buff=0.3)
        ctx.show(so, so_name, tag="so", anim=lambda m: FadeIn(m, shift=LEFT * 0.3), run_time=0.5,
                 nudge=False)
        self._at(ctx, 0.72)
        self.play(*style.highlight(ask, style.GOLD), so.animate.set_opacity(0.4), run_time=0.6)

    def b_grow(self, ctx):
        ctx.clear_stage(run_time=0.35)
        edges = [(0, 1), (1, 2), (0, 2)]
        for k in range(3, len(GROW)):
            near = sorted(range(k), key=lambda j: np.hypot(GROW[j][0] - GROW[k][0], GROW[j][1] - GROW[k][1]))
            edges += [(j, k) for j in near[:3]]
        nodes, links = charts.network([np.array([x, y, 0]) for x, y in GROW], edges, radius=0.24)
        self.play(FadeIn(nodes[:3], scale=0.8), Create(links[:3]), run_time=ctx.budget(0.6)[0])
        self._owned["graph"] = VGroup(links, nodes)
        # Each joins with its three links; all twelve are in by about two thirds of the line.
        self.play(LaggedStart(*[AnimationGroup(FadeIn(nodes[k], scale=0.6), Create(links[3 * (k - 2):3 * (k - 1)]))
                                for k in range(3, len(GROW))], lag_ratio=0.5), run_time=0.45 * ctx.window)
        self._at(ctx, 0.8)
        self.play(flash(links, style.CYAN, ctx.budget(0.8)[0]))

    def b_loop(self, ctx):
        ctx.clear_stage(run_time=0.35)
        slots = [ORIGIN, *charts.ring(6, 0.62)]
        groups = []
        for x, word in ((-3.6, "asking"), (3.6, "answering")):
            centre = RIGHT * x + DOWN * 0.15
            nodes, _ = charts.network([centre + s for s in slots], [], radius=0.22)
            name = style.label_text(word, color=style.CYAN).next_to(nodes, DOWN, buff=0.3)
            groups.append((nodes, name))
        so = style.label_text("Stack Overflow", color=style.BLUE).move_to(UP * 1.85)
        ctx.show(*[m for nodes, name in groups for m in (nodes[:5], name)], so, tag="loop",
                 run_time=0.6, nudge=False)
        (ask, _), (ans, _) = groups
        top = style.glow_arrow(LEFT * 2.5 + UP * 0.45, RIGHT * 2.5 + UP * 0.45, color=style.CYAN)
        bottom = style.glow_arrow(RIGHT * 2.5 + DOWN * 0.75, LEFT * 2.5 + DOWN * 0.75, color=style.CYAN)
        for i, (arrow, joins) in enumerate(((top, ans), (bottom, ask))):
            self._at(ctx, 0.16 + 0.3 * i)
            self.play(GrowArrow(arrow[1]), FadeIn(arrow[0]), run_time=0.6)
            self._owned["loop"].add(arrow)
            new = joins[5:]
            # FadeIn from the tip, not save_state/Restore: the gate's geometry never saw restored nodes,
            # so at 30 fps the arrow read as pointing at nothing (arrow_to_nowhere, 1080p30 only).
            self.play(LaggedStart(*[FadeIn(n, target_position=arrow[1].get_end()) for n in new],
                                  lag_ratio=0.4), run_time=0.9)
            self._owned["loop"].add(new)
        self._at(ctx, 0.9)
        self.play(*[n.animate.set_stroke(width=4) for n in (*ask, *ans)], run_time=0.5)

    # The area chart, built once in b_peak and extended by the two beats after it.
    def _area(self, left: float, upto: float, color: str = style.GREEN) -> VGroup:
        """The questions curve from x = left to x = upto: a filled area with its line on top."""
        xs, ys = zip(*QUESTIONS)
        upto = max(upto, left + 0.01)
        pts = [(left, np.interp(left, xs, ys)), *[(x, y) for x, y in QUESTIONS if left < x < upto],
               (upto, np.interp(upto, xs, ys))]
        top = [self._plot.at(x, y) for x, y in pts]
        fill = Polygon(self._plot.at(left, 0), *top, self._plot.at(upto, 0), stroke_width=0)
        fill.set_fill(color, opacity=0.28).set_z_index(style.Z_BACKDROP)
        edge = VMobject(color=color, stroke_width=3.4).set_points_as_corners(top).set_z_index(style.Z_EDGE)
        return VGroup(fill, edge)

    def _grow_area(self, area: VGroup, left: float, x0: float, x1: float, run_time: float):
        """Run the area's right edge from x0 to x1."""
        self.play(UpdateFromAlphaFunc(area, lambda m, a: m.become(self._area(left, x0 + (x1 - x0) * a))),
                  run_time=run_time, rate_func=linear)

    def b_peak(self, ctx):
        ctx.clear_stage(run_time=0.35)
        self._plot = charts.Plot(LEFT * 5.6 + DOWN * 1.95, 10.6, 3.9, (2013.5, 2027), (0, 220000),
                                 x_ticks=[(y, str(y)) for y in (2014, 2018, 2022, 2026)],
                                 y_ticks=[(0, "0"), (100000, "100k"), (200000, "200k")])
        # Above the peak, clear of the area's box: the gate reads that box's edges as an outline.
        series = style.label_text("new questions a month", color=style.MUTED)
        series.move_to(self._plot.at(2018.2, 0) * RIGHT + UP * 2.2)
        ctx.show(self._plot, series, tag="plot", run_time=0.5, nudge=False)
        peak = Dot(self._plot.at(*QUESTIONS[0]), radius=0.1, color=style.GREEN)
        peak_n = style.label_text("207,000", color=style.WHITE, size="caption")
        peak_n.next_to(peak, UP, buff=0.15).align_to(peak.get_left(), LEFT)
        ctx.show(peak, peak_n, tag="peak", run_time=0.5, nudge=False)
        self._at(ctx, 0.2)
        left = QUESTIONS[0][0]
        self._fall = self._area(left, left)
        self.add(self._fall)
        self._grow_area(self._fall, left, left, QUESTIONS[3][0], 0.38 * ctx.window)
        self._owned["plot"].add(self._fall)

    def b_now(self, ctx):
        self._grow_area(self._fall, QUESTIONS[0][0], QUESTIONS[3][0], QUESTIONS[-1][0], ctx.budget(1.0)[0])
        self._at(ctx, 0.3)
        last = Dot(self._plot.at(*QUESTIONS[-1]), radius=0.1, color=style.GREEN)
        last_n = style.label_text("1,400", color=style.WHITE, size="caption").next_to(last, UR, buff=0.2)
        ctx.show(last, last_n, tag="last", anim=lambda m: FadeIn(m, scale=1.4), run_time=0.5, nudge=False)
        self._at(ctx, 0.65)
        self.play(last.animate.scale(1.6), run_time=0.4)

    def b_chatgpt(self, ctx):
        p = self._plot
        mark = DashedLine(p.at(CHATGPT, 0), p.at(CHATGPT, 220000), color=style.WHITE, stroke_width=2.2,
                          dash_length=0.12).set_z_index(style.Z_EDGE)
        # Two rows, inside the area's box above the curve; owned apart from the line and the red
        # area so the label's group carries no stroke.
        name = style.text_rows(style.label_text("ChatGPT", color=style.WHITE),
                               style.label_text("Nov 2022", color=style.WHITE))
        name.next_to(p.at(CHATGPT, 150000), RIGHT, buff=0.2)
        self.play(Create(mark), run_time=ctx.budget(0.6)[0])
        ctx.show(name, tag="chatgpt", run_time=0.4, nudge=False)
        self._at(ctx, 0.35)
        # The green past the marker is split off, and red takes its place as it sweeps right:
        # red laid over green read as brown, under a green edge.
        start, end = QUESTIONS[0][0], QUESTIONS[-1][0]
        head, tail = self._area(start, CHATGPT), self._area(CHATGPT, end)
        self.remove(self._fall)
        self._owned["plot"].remove(self._fall).add(head)
        after = self._area(CHATGPT, CHATGPT, style.RED)
        self.add(head, tail, after)
        front = lambda a: CHATGPT + (end - CHATGPT) * a
        self.play(UpdateFromAlphaFunc(after, lambda m, a: m.become(self._area(CHATGPT, front(a), style.RED))),
                  UpdateFromAlphaFunc(tail, lambda m, a: m.become(self._area(front(a), end))),
                  run_time=ctx.budget(1.4)[0], rate_func=linear)
        self.remove(tail)
        self._owned["since"] = VGroup(mark, after)
        self._at(ctx, 0.75)
        self.play(after[1].animate.set_stroke(width=6), run_time=0.5)

    def b_licence(self, ctx):
        ctx.clear_stage(run_time=0.35)
        crowd_pts = [np.array([-4.8, 0.1, 0]) + p for p in [(0, 0, 0), *charts.ring(7, 0.85)]]
        crowd, ties = charts.network(crowd_pts, nearest_edges(crowd_pts, 1.0), radius=0.2)
        crowd_name = style.label_text("the crowd", color=style.CYAN).next_to(crowd, DOWN, buff=0.3)
        cards = VGroup(*[style.tile(1.1, 0.7, style.WHITE, opacity=0.1) for _ in range(5)])
        for i, c in enumerate(cards):
            c.move_to(LEFT * 0.7 + UP * 0.1 + (RIGHT + UP) * 0.09 * (i - 2))
        cards_name = style.label_text("answers", color=style.WHITE).next_to(cards, DOWN, buff=0.3)
        wrote = style.glow_arrow(crowd.get_right() + RIGHT * 0.1, cards.get_left() + LEFT * 0.15,
                                 color=style.CYAN)
        ctx.show(ties, crowd, crowd_name, tag="crowd", run_time=0.6, nudge=False)
        ctx.show(cards, cards_name, tag="cards", run_time=0.5, nudge=False)
        self.play(GrowArrow(wrote[1]), FadeIn(wrote[0]), run_time=0.5)
        self._owned["crowd"].add(wrote)
        # Direct handles: the stage re-sorts owned groups (connectors first).
        self._crowd, self._ties, self._wrote, self._crowd_name = crowd, ties, wrote, crowd_name
        self._cards = cards
        self._at(ctx, 0.3)
        model = style.node("agent", size=1.5).move_to(RIGHT * 4.4 + UP * 0.1)
        model_name = style.label_text("AI models", color=style.VIOLET).next_to(model, DOWN, buff=0.3)
        sold = style.glow_arrow(cards.get_right() + RIGHT * 0.15, model.get_left() + LEFT * 0.1,
                                color=style.VIOLET)
        sold_name = style.label_text("access", color=style.VIOLET).next_to(sold, UP, buff=0.25)
        ctx.show(model, model_name, tag="model", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.4,
                 nudge=False)
        self.play(GrowArrow(sold[1]), FadeIn(sold[0]), FadeIn(sold_name), run_time=0.4)
        self._owned["model"].add(sold, sold_name)
        self._model = model
        self._at(ctx, 0.5)
        self._copy_cards(self._cards[-2:], ctx.budget(0.8)[0])
        self._at(ctx, 0.64)      # "OpenAI among them"
        openai = style.label_text("OpenAI", color=style.WHITE).next_to(model_name, DOWN, buff=0.2)
        ctx.show(openai, tag="openai", run_time=0.4, nudge=False)

    def _copy_cards(self, cards: VGroup, run_time: float):
        """Copies of these answer cards fly into the model and stay there, small; the stack keeps its own."""
        stack, inside = self._cards.get_center(), self._model.get_center()
        copies = VGroup(*[c.copy() for c in cards])
        self.add(copies)
        self.play(LaggedStart(*[c.animate.scale(0.35).move_to(inside + (c.get_center() - stack) * 0.35)
                                for c in copies], lag_ratio=0.35), run_time=run_time)
        # Each one: LaggedStart leaves its own group on stage holding them.
        self.remove(*copies)
        self.add(copies)
        self._owned["model"].add(copies)

    def b_reading(self, ctx):
        self.play(*style.highlight(self._cards, style.WHITE), run_time=0.5)
        self._at(ctx, 0.3)
        self._copy_cards(self._cards[:3], ctx.budget(1.6)[0])
        self.play(*style.highlight(self._model, style.VIOLET), run_time=0.5)
        # Without the crowd: it thins out and drifts apart.
        self._at(ctx, 0.6)
        centre = self._crowd[0].get_center()
        self.play(*[n.animate.shift((n.get_center() - centre) * 0.45).set_opacity(0.25)
                    for n in self._crowd[1:]],
                  self._crowd[0].animate.set_opacity(0.25), FadeOut(self._ties), FadeOut(self._wrote),
                  self._crowd_name.animate.set_opacity(0.3).shift(DOWN * 0.45), run_time=ctx.budget(1.6)[0])

    def b_live(self, ctx):
        ctx.clear_stage(run_time=0.35)
        pts = [np.array([0, 0.05, 0])] + charts.ring(6, 1.15, center=UP * 0.05) \
            + charts.ring(6, 2.0, center=UP * 0.05, start=PI / 2 + PI / 6)
        live, links = charts.network(pts, nearest_edges(pts, 1.3), radius=0.2)
        ctx.show(links, live, tag="live", run_time=0.6, nudge=False)
        for i in range(3):
            self._at(ctx, 0.12 + 0.28 * i)
            self.play(flash(links, style.CYAN, 1.2),
                      *[n.animate.set_stroke(width=4) for n in live], run_time=ctx.budget(1.2)[0])
            self.play(*[n.animate.set_stroke(width=2.4) for n in live], run_time=0.3)

    def b_phrase(self, ctx):
        ctx.clear_stage(run_time=0.35)
        levi = style.node("person", "Levi", size=1.5, font_size=26).move_to(LEFT * 5.3 + UP * 0.2)
        words = [style.title_text(w) for w in ("connected", "permitted", "capacity")]
        row = VGroup(words[0], Dot(radius=0.06, color=style.MUTED), words[1],
                     Dot(radius=0.06, color=style.MUTED), words[2]).arrange(RIGHT, buff=0.3)
        row.move_to(RIGHT * 0.9 + UP * 0.55)
        means = style.label_text("= network effect", color=style.GOLD, size="caption")
        means.next_to(row, DOWN, buff=0.5)
        ctx.lopsided("Levi on the left, his phrase across the rest of the stage")
        ctx.show(levi, tag="levi", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.4)
        self._owned["phrase"] = VGroup()
        for i in range(3):
            self._at(ctx, 0.08 + 0.13 * i)
            parts = [row[2 * i]] + ([row[2 * i - 1]] if i else [])
            self.play(*[FadeIn(p, shift=UP * 0.1) for p in parts], run_time=0.4)
            self._owned["phrase"].add(*parts)
        self._at(ctx, 0.55)
        ctx.show(means, tag="means", run_time=0.5, nudge=False)
        self._at(ctx, 0.8)
        self.play(*style.highlight(levi, style.WHITE), run_time=0.5)

    def b_examples(self, ctx):
        ctx.clear_stage(run_time=0.35)
        ring = charts.ring(7, 1.05, center=LEFT * 4.4 + UP * 0.35)
        bitcoin = charts.network(ring, [(i, j) for i in range(7) for j in range(i + 1, 7)], radius=0.16)
        hub = RIGHT * 0 + UP * 0.35
        friends = [hub] + charts.ring(6, 0.8, center=hub) + [hub + np.array(p) for p in
                                                             ((-1.3, 0.75, 0), (1.35, -0.6, 0))]
        fb_edges = [(0, k) for k in range(1, 7)] + [(k, k % 6 + 1) for k in range(1, 7)] + [(7, 2), (8, 5)]
        facebook = charts.network(friends, fb_edges, radius=0.16)
        mesh_pts = [RIGHT * (3.5 + 0.62 * c) + UP * (1.15 - 0.6 * r) for r in range(4) for c in range(4)]
        grid = charts.network(mesh_pts, nearest_edges(mesh_pts, 0.9), radius=0.13)
        # Each arrives in the middle of the row so far, and the row makes room for it: the stage
        # stays balanced while the examples are named one at a time.
        shown = []
        self._owned["examples"] = VGroup()
        for i, ((nodes, links), word) in enumerate(((bitcoin, "Bitcoin"), (facebook, "Facebook"),
                                                    (grid, "the power grid"))):
            self._at(ctx, (0.04, 0.4, 0.66)[i])
            name = style.label_text(word, color=style.CYAN).move_to([nodes.get_x(), -1.55, 0])
            example = VGroup(links, nodes, name)
            slots = ((0.0,), (-2.2, 2.2), (-4.4, 0.0, 4.4))[i]
            example.set_x(slots[-1])
            self.play(*[e.animate.set_x(x) for e, x in zip(shown, slots)],
                      FadeIn(nodes, scale=0.8), Create(links), FadeIn(name), run_time=ctx.budget(0.8)[0])
            shown.append(example)
            self._owned["examples"].add(links, nodes, name)
        self._at(ctx, 0.88)
        everything = VGroup(bitcoin[1], facebook[1], grid[1])
        self.play(flash(everything, style.CYAN, ctx.budget(1.0)[0]))

    def b_meta(self, ctx):
        ctx.clear_stage(run_time=0.35)
        app = style.node("product", size=2.6).move_to(UP * 0.45)
        app_name = style.label_text("Meta's apps", color=style.BLUE).next_to(app, DOWN, buff=0.25)
        people = VGroup(*[Dot(radius=0.06, color=style.CYAN) for _ in range(100)])
        people.arrange_in_grid(rows=10, cols=10, buff=0.1).move_to(app)
        users = style.label_text("3.6 billion a day", color=style.WHITE).next_to(app_name, DOWN, buff=0.2)
        ctx.show(app, app_name, tag="app", anim=lambda m: FadeIn(m, scale=0.9), run_time=0.5, nudge=False)
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in people], lag_ratio=0.03),
                  run_time=ctx.budget(1.8)[0])
        self._owned["app"].add(people)
        ctx.show(users, tag="users", run_time=0.4, nudge=False)
        # The clone splits off the app: the software copied, none of the people.
        self._at(ctx, 0.55)
        clone = style.node("clone", size=2.6).move_to(app)
        self.add(clone)
        # The owned groups themselves: a fresh VGroup over members of an owned group lost the
        # app and its name from the stage when the animation ended.
        self.play(self._owned["app"].animate.shift(LEFT * 3.2), users.animate.shift(LEFT * 3.2),
                  clone.animate.shift(RIGHT * 3.2), run_time=0.8)
        self._owned["clone"] = clone
        clone_name = style.label_text("a clone", color=style.BLUE).next_to(clone, DOWN, buff=0.25)
        zero = style.label_text("0", color=style.WHITE).next_to(clone_name, DOWN, buff=0.2)
        self._at(ctx, 0.72)
        ctx.show(clone_name, zero, tag="zero", run_time=0.5, nudge=False)

    def b_pjm(self, ctx):
        ctx.clear_stage(run_time=0.35)
        border = RegularPolygon(n=6, radius=PJM_R, start_angle=PI / 2).move_to(PJM_C)
        border.set_stroke(style.GOLD, width=3).set_fill(style.GOLD, opacity=0.05)
        border.set_z_index(style.Z_BACKDROP)
        half = PJM_R * np.sqrt(3) / 2                  # the boundary's flat sides
        pts = []
        for r, dy in enumerate((-1.4, -0.7, 0.0, 0.7, 1.4)):
            room = min(half, (PJM_R - abs(dy)) * np.sqrt(3)) - 0.42
            for k in range(-4, 5):
                dx = 0.7 * k + (0.35 if r % 2 else 0.0)
                if abs(dx) <= room:
                    pts.append(PJM_C + np.array([dx, dy, 0]))
        slot = min((p for p in pts if abs(p[1] - PJM_C[1]) < 1e-6), key=lambda p: p[0])
        members = [p for p in pts if p is not slot]
        nodes, links = charts.network(members, nearest_edges(members, 0.8), radius=0.13)
        pjm = style.label_text("PJM", color=style.GOLD, size="caption")
        facts = style.text_rows(*[flat_card(t) for t in ("13 states + DC", "1,116 members", "67 million people")],
                                buff=0.18)
        column = style.text_rows(pjm, facts, buff=0.35).move_to(RIGHT * 4.6 + UP * 0.2)
        column.align_to(RIGHT * 3.2, LEFT)
        ctx.show(border, links, nodes, pjm, tag="pjm", run_time=ctx.budget(1.0)[0], nudge=False)
        self._at(ctx, 0.1)
        ctx.show(facts[0], tag="states", run_time=0.4, nudge=False)
        # The gate: an operating agreement on the boundary.
        self._at(ctx, 0.22)
        gate = border.get_left() * RIGHT + PJM_C * UP
        doc = RoundedRectangle(corner_radius=0.05, width=0.5, height=0.66).move_to(gate)
        doc.set_stroke(style.WHITE, width=2.4).set_fill(style.PANEL_HI, opacity=0.96)
        rules = VGroup(*[Line(LEFT * 0.14, RIGHT * 0.14, stroke_width=2, color=style.MUTED)
                         for _ in range(3)]).arrange(DOWN, buff=0.12).move_to(doc)
        doc_name = style.text_rows(style.label_text("operating", color=style.WHITE),
                                   style.label_text("agreement", color=style.WHITE), align=RIGHT)
        doc_name.next_to(doc, LEFT, buff=0.3).shift(UP * 0.75)
        joiner = charts.network([LEFT * 5.8 + gate * UP], [], radius=0.13)[0][0]
        ctx.show(doc, rules, doc_name, joiner, tag="gate", run_time=0.5, nudge=False)
        self._doc, self._border = VGroup(doc, rules), border
        self._at(ctx, 0.3)
        self.play(joiner.animate.move_to(doc.get_left() + LEFT * 0.3), run_time=ctx.budget(1.3)[0])
        self._at(ctx, 0.42)
        self.play(doc.animate.set_stroke(style.GOLD, width=4), run_time=0.4)
        self.play(joiner.animate.move_to(slot), run_time=0.8)
        joined = VGroup(*[Line(slot, p, color=style.MUTED, stroke_width=2.2, buff=0.13)
                          .set_z_index(style.Z_EDGE) for p in members if np.linalg.norm(p - slot) < 0.8])
        self.play(Create(joined), doc.animate.set_stroke(style.WHITE, width=2.4), run_time=0.5)
        self._owned["pjm"].add(joined)
        self._links = VGroup(*links, *joined)
        self._at(ctx, 0.6)
        ctx.show(facts[1], tag="members", run_time=0.4, nudge=False)
        self._at(ctx, 0.72)
        ctx.show(facts[2], tag="people", run_time=0.4, nudge=False)
        self._at(ctx, 0.88)
        self.play(flash(self._links, style.CYAN, ctx.budget(1.0)[0]))

    def b_words(self, ctx):
        words = VGroup(*[style.caption_text(w, color=style.MUTED)
                         for w in ("connected", "permitted", "capacity")])
        style.text_rows(*words, buff=0.4).move_to(RIGHT * 4.6 + DOWN * 0.4).align_to(RIGHT * 3.2, LEFT)
        ctx.retire("states", "members", "people", run_time=0.3)
        ctx.show(words, tag="words", run_time=0.5, nudge=False)
        # Connected: the others are already there.
        self._at(ctx, 0.12)
        self.play(words[0].animate.set_color(style.WHITE), run_time=0.3)
        self.play(flash(self._links, style.CYAN, ctx.budget(1.2)[0]))
        # Permitted: you join on the network's terms.
        self._at(ctx, 0.33)
        self.play(words[1].animate.set_color(style.WHITE), *style.highlight(self._doc[0], style.GOLD),
                  self._border.animate.set_stroke(width=5), run_time=0.6)
        # Capacity: something real flows.
        self._at(ctx, 0.52)
        self.play(words[2].animate.set_color(style.WHITE), run_time=0.3)
        for _ in range(2):
            self.play(flash(self._links, style.GOLD, ctx.budget(1.1)[0]))
        # A clone copies the software and gets none of the three.
        self._at(ctx, 0.72)
        # Outside the gate, level with it, where the joiner waited.
        clone = style.node("clone", size=1.1).move_to(LEFT * 4.5 + UP * PJM_C[1])
        clone_name = style.label_text("a clone", color=style.BLUE).next_to(clone, DOWN, buff=0.22)
        ctx.show(clone, clone_name, tag="clone", anim=lambda m: FadeIn(m, shift=RIGHT * 0.3),
                 run_time=0.5, nudge=False)
        self._at(ctx, 0.78)
        # Caption size: at label size the word gaps of this phrase merge at review size.
        none = style.caption_text("none of the three", color=style.MUTED).next_to(clone_name, DOWN, buff=0.3)
        none.align_to(clone, LEFT)
        ctx.show(none, tag="none", run_time=0.4, nudge=False)
