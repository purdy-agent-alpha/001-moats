"""
Section 04: which moats die and which hold.

First half: the five sources of 02 in a row at the top; under it, one small
demonstration per line (the dying moat stays a hexagon: dimmed, struck in red),
then the data moat as two lines closing the gap between them. Second half: a
clone on the left and the hexagons it cannot generate gathering on the right;
Slack's record throttles an outside app; then 118 companies claiming a moat.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from moats_video.pipeline import charts, style
from moats_video.pipeline.beats import Beat, BeatScene

ROW_Y = 1.55                       # the row of the five sources
XS = [-5.2, -2.6, 0.0, 2.6, 5.2]   # five columns across the stage
HEX = 1.0
LANE_Y = -0.6                      # the secret-code demonstration's network line


class S04Die(BeatScene):
    section_id = "04_die"
    title = "Which moats hold"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("So which of the five sources die", self.b_row,
                 note="the five sources of 02 in a row"),
            Beat("Secret code goes first", self.b_secret,
                 note="packets flow from the app over a network line to a dashed clone; secret code struck"),
            Beat("Switching costs built on friction go with it", self.b_lockin,
                 note="three frictions under switching costs; struck"),
            Beat("My guess: an agent will run the migration", self.b_migrate,
                 note="an agent carries three data cards from the old product to a new one"),
            Beat("Agents mostly use your API, not your screens", self.b_seats,
                 note="three users collapse into one agent; two of their three seats go"),
            Beat("A pile of data on its own is a scale effect", self.b_data,
                 note="two lines: the leader's edge (gold band) narrows as a rival's line rises to meet it"),
            Beat("What still buys time is what a rebuild cannot supply", self.b_holds,
                 note="new picture: the clone alone on the left"),
            Beat("Being the system of record", self.b_record,
                 note="record hexagon; a customer's data flows into it"),
            Beat("And the owner of that record decides", self.b_slack,
                 note="a pipe from the record to an outside app thins from 1,000 a request to 15; a gate, "
                      "1 request a minute"),
            Beat("Licences, audits and compliance", self.b_licence,
                 note="licences, then moving money"),
            Beat("Liability: a vendor can sign an indemnity", self.b_liability,
                 note="liability hexagon; the clone dims: nobody behind it"),
            Beat("Everyone now claims a moat", self.b_claims,
                 note="118 dots fill a grid: at least 118, Q1 2026"),
        ]

    # ------------------------------------------------------------ helpers --
    def _at(self, ctx, frac: float) -> None:
        """Wait until `frac` of this beat's window has passed (never past its end)."""
        lag = ctx.beat.start + frac * ctx.window - self.renderer.time
        if lag > 0.02:
            self.wait(lag)

    def _strike(self, hexa, label, owner: str, run_time: float = 0.6):
        """Dim a moat and strike it. The hexagon stays a hexagon."""
        line = style.strike(hexa)
        self.play(hexa.animate.set_opacity(0.3), label.animate.set_opacity(0.45),
                  Create(line), run_time=run_time)
        self._owned[owner].add(line)

    # ---------------------------------------------------------------- beats --
    def b_row(self, ctx):
        names = ["brands, licences", "switching costs", "network effects", "lower costs", "niche markets"]
        row, self._hexes = VGroup(), []
        for x, name in zip(XS, names):
            hexa = style.node("moat", size=HEX).move_to(RIGHT * x + UP * ROW_Y)
            label = style.label_text(name, color=style.GOLD).next_to(hexa, DOWN, buff=0.22)
            row.add(VGroup(hexa, label))
            self._hexes.append((hexa, label))
        self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in row], lag_ratio=0.15),
                  run_time=ctx.budget(1.0)[0])
        self._owned["row"] = row
        self._at(ctx, 0.6)
        self.play(*[a for hexa, _ in self._hexes for a in style.highlight(hexa, style.GOLD)],
                  run_time=ctx.budget(0.6)[0])

    def b_secret(self, ctx):
        app = style.node("product", size=1.0).move_to(LEFT * 4.6 + UP * LANE_Y)
        app_name = style.label_text("Linear", color=style.BLUE).next_to(app, DOWN, buff=0.22)
        copy = style.node("clone", size=1.0).move_to(RIGHT * 4.6 + UP * LANE_Y)
        copy_name = style.label_text("the clone", color=style.BLUE).next_to(copy, DOWN, buff=0.22)
        wire = Line(app.get_right() + RIGHT * 0.15, copy.get_left() + LEFT * 0.15,
                    color=style.MUTED, stroke_width=2.4).set_z_index(style.Z_EDGE)
        wire_name = style.label_text("network", color=style.MUTED).next_to(wire, UP, buff=0.3)
        secret = style.node("moat", size=0.8).move_to(LEFT * 0.9 + DOWN * 1.75)
        secret_name = style.label_text("secret code", color=style.GOLD).next_to(secret, RIGHT, buff=0.25)
        ctx.show(app, app_name, wire, wire_name, secret, secret_name, tag="demo", run_time=0.6,
                 nudge=False)
        self._at(ctx, 0.2)
        # What the app sends over the network is all the clone needs.
        packets = VGroup(*[style.tile(0.2, 0.2, style.CYAN, opacity=0.6) for _ in range(5)])
        packets.move_to(wire.get_start())
        self.add(packets)
        span = wire.get_end() - wire.get_start()
        self.play(LaggedStart(*[p.animate(rate_func=linear).shift(span) for p in packets],
                              lag_ratio=0.3), run_time=ctx.budget(2.0)[0])
        # Each one: LaggedStart leaves its own group on stage holding them.
        self.remove(*packets)
        self.play(FadeIn(copy, scale=0.9), FadeIn(copy_name), run_time=0.5)
        self._owned["demo"].add(copy, copy_name)
        self._at(ctx, 0.62)
        self._strike(secret, secret_name, "demo")

    def b_lockin(self, ctx):
        ctx.clear_stage("row", run_time=0.35)
        hexa, label = self._hexes[1]
        self.play(*style.highlight(hexa, style.GOLD), run_time=0.4)
        items = style.text_rows(*[style.label_text(w, color=style.WHITE)
                                  for w in ("interface", "export", "migration")], align=ORIGIN)
        items.next_to(label, DOWN, buff=0.35)
        for i, item in enumerate(items):
            self._at(ctx, 0.04 + 0.13 * i)
            self.play(FadeIn(item, shift=UP * 0.1), run_time=0.4)
        # The source argues friction goes: the hexagon is struck while the line names the frictions.
        self._at(ctx, 0.62)
        self.play(items[2].animate.set_color(style.VIOLET), run_time=0.3)
        self._strike(hexa, label, "row")

    def b_migrate(self, ctx):
        """Alpha's guess, its own beat and chip: an agent carries the data across."""
        old = style.node("product", size=0.9).move_to(LEFT * 0.4 + DOWN * 1.55)
        new = style.node("product", size=0.9).move_to(RIGHT * 5.0 + DOWN * 1.55)
        agent = style.node("agent", size=0.8).move_to(old.get_right() + RIGHT * 0.85)
        cards = VGroup(*[style.tile(0.3, 0.2, style.CYAN, opacity=0.5) for _ in range(3)])
        cards.arrange(DOWN, buff=0.07).move_to(old)
        ctx.show(old, new, agent, tag="mig", run_time=0.5, nudge=False)
        self.add(cards)
        self._at(ctx, 0.3)
        stop = new.get_left() + LEFT * 0.85
        self.play(agent.animate.move_to(stop), cards.animate.move_to(stop), run_time=ctx.budget(1.2)[0])
        self.play(cards.animate.move_to(new).set_opacity(0.0), *style.highlight(new, style.BLUE),
                  run_time=0.5)
        self.remove(cards)

    def b_seats(self, ctx):
        ctx.clear_stage("row", run_time=0.35)
        users = VGroup(*[style.node("customer", size=0.62) for _ in range(3)])
        users.arrange(RIGHT, buff=0.45).move_to(RIGHT * 0.8 + DOWN * 0.3)
        seats = VGroup(*[style.tile(0.5, 0.3, style.MUTED, opacity=0.35) for _ in range(3)])
        for seat, user in zip(seats, users):
            seat.move_to(user).shift(DOWN * 0.95)
        per_seat = style.label_text("per seat", color=style.MUTED).next_to(seats, LEFT, buff=0.4)
        self.play(LaggedStart(*[FadeIn(u, scale=0.8) for u in users], lag_ratio=0.2),
                  run_time=ctx.budget(0.6)[0])
        ctx.show(seats, per_seat, tag="seats", run_time=0.5, nudge=False)
        self._at(ctx, 0.5)
        # One agent does the work of several users: two of the three seats go.
        agent = style.node("agent", size=0.95).move_to(users)
        self.play(*[u.animate.move_to(agent).scale(0.4).set_opacity(0) for u in users], run_time=0.8)
        self.remove(*users)
        ctx.show(agent, tag="agent", anim=lambda m: FadeIn(m, scale=0.7), run_time=0.5)
        self._at(ctx, 0.72)
        self.play(seats[0].animate.set_fill(style.RED, opacity=0.5).set_stroke(style.RED),
                  seats[2].animate.set_fill(style.RED, opacity=0.5).set_stroke(style.RED), run_time=0.5)
        self.play(FadeOut(seats[0]), FadeOut(seats[2]),
                  per_seat.animate.next_to(seats[1], LEFT, buff=0.4), run_time=0.6)
        self._owned["seats"].remove(seats[0], seats[2])

    def b_data(self, ctx):
        ctx.clear_stage(run_time=0.4)
        ctx.lopsided("the chart stands on its axes at the left; the data hexagon waits on the right")
        plot = charts.Plot(LEFT * 5.9 + DOWN * 1.9, 8.0, 3.8, (0, 4), (0, 1), x_title="time", y_title="edge")
        lead_pts = [(0, 0.88), (1, 0.84), (2, 0.78), (3, 0.71), (4, 0.64)]
        rival_pts = [(0, 0.25), (1, 0.38), (2, 0.5), (3, 0.59), (4, 0.64)]
        leader = charts.line(plot, lead_pts, color=style.GOLD)
        rival = charts.line(plot, rival_pts, color=style.BLUE)

        def band(upto: float) -> Polygon:
            """The leader's edge: the gap between the two lines, as far as x = upto."""
            xs = [x for x, _ in lead_pts if x < upto] + [upto]
            top = [plot.at(x, np.interp(x, *zip(*lead_pts))) for x in xs]
            bottom = [plot.at(x, np.interp(x, *zip(*rival_pts))) for x in reversed(xs)]
            return Polygon(*top, *bottom, stroke_width=0).set_fill(style.GOLD, opacity=0.22)

        edge = band(0.01).set_z_index(style.Z_BACKDROP)
        lead = style.label_text("the leader", color=style.GOLD).next_to(plot.at(0.1, 0.88), UP, buff=0.2)
        lead.align_to(plot.at(0.6, 0), LEFT)
        riv = style.label_text("a rival", color=style.BLUE).next_to(plot.at(0.6, 0.25), DOWN, buff=0.3)
        # A short line: every step takes a share of the window, so the data moat is struck before it ends.
        ctx.show(plot, lead, riv, tag="plot", run_time=0.5, nudge=False)
        self.add(edge)
        self.play(Create(leader), Create(rival),
                  UpdateFromAlphaFunc(edge, lambda m, a: m.become(band(max(4 * a, 0.01)))
                                      .set_z_index(style.Z_BACKDROP)),
                  run_time=0.35 * ctx.window, rate_func=linear)
        self._owned["plot"].add(leader, rival, edge)
        hexa = style.node("moat", size=1.3).move_to(RIGHT * 4.6 + UP * 0.2)
        name = style.label_text("data", color=style.GOLD).next_to(hexa, DOWN, buff=0.25)
        self._at(ctx, 0.55)
        ctx.show(VGroup(hexa, name), tag="datamoat", anim=lambda m: FadeIn(m, scale=0.85),
                 run_time=0.4, nudge=False)
        self._at(ctx, 0.75)
        self._strike(hexa, name, "datamoat", run_time=0.4)

    def b_holds(self, ctx):
        ctx.clear_stage(run_time=0.35)
        ctx.lopsided("the clone stands alone on the left; what it cannot make arrives on the right")
        clone = style.node("clone", size=2.2).move_to(LEFT * 5.0 + UP * 0.2)
        name = style.label_text("a clone", color=style.BLUE).next_to(clone, DOWN, buff=0.3)
        ctx.show(VGroup(clone, name), tag="clone", anim=lambda m: FadeIn(m, scale=0.9),
                 run_time=0.5, nudge=False)
        # Empty outlines mark where what a clone cannot make will arrive.
        slots = VGroup(*[RegularPolygon(n=6, radius=self.HOLD_HEX / 2, color=style.DIM).set_stroke(width=2)
                         .move_to(RIGHT * x + UP * y) for x, y in self.SLOTS[:3]])
        ctx.show(slots, tag="slots", run_time=0.5, nudge=False)
        self._at(ctx, 0.5)
        self.play(*style.highlight(clone, style.BLUE), run_time=0.8)

    # The things that hold: three in a row on the right, liability centred under them.
    SLOTS = [(-0.9, 1.15), (2.0, 1.15), (4.9, 1.15), (2.0, -1.0)]
    HOLD_HEX = 1.55

    def _hold(self, i: int, word: str) -> VGroup:
        x, y = self.SLOTS[i]
        hexa = style.node("moat", size=self.HOLD_HEX).move_to(RIGHT * x + UP * y)
        label = style.label_text(word, color=style.GOLD, size="caption")
        label.next_to(hexa, DOWN, buff=0.22)
        return VGroup(hexa, label)

    def b_record(self, ctx):
        ctx.lopsided("the held moats gather on the right, one per line, opposite the clone")
        ctx.retire("slots", run_time=0.2)
        record = self._hold(0, "system of record")
        self._record = record[0]
        ctx.show(record, tag="record", anim=lambda m: FadeIn(m, scale=0.85),
                 run_time=ctx.budget(0.6)[0], nudge=False)
        self._at(ctx, 0.35)
        customer = style.node("customer", size=0.85)
        customer.move_to(record[0].get_center() + LEFT * 2.0)
        flow = style.glow_arrow(customer.get_right() + RIGHT * 0.08,
                                record[0].get_left() + LEFT * 0.28, color=style.CYAN, buff=0.0)
        self.play(FadeIn(customer, scale=0.8), GrowArrow(flow[1]), FadeIn(flow[0]),
                  run_time=ctx.budget(0.9)[0])
        self._owned["record"].add(customer, flow)
        self._at(ctx, 0.7)
        self.play(*style.highlight(record[0], style.GOLD), run_time=0.6)

    def _stream(self, pipe, n: int, lag: float, run_time: float, stop: float = 1.0):
        """`n` messages travel along the pipe, `stop` of the way; then they are gone."""
        msgs = VGroup(*[Dot(radius=0.06, color=style.CYAN) for _ in range(n)])
        msgs.move_to(pipe.get_left() + RIGHT * 0.1)
        self.add(msgs)
        span = (pipe.get_width() - 0.2) * stop
        self.play(LaggedStart(*[m.animate(rate_func=linear).shift(RIGHT * span) for m in msgs],
                              lag_ratio=lag), run_time=run_time)
        self.remove(*msgs)

    def b_slack(self, ctx):
        ctx.lopsided("the held moats gather on the right, one per line, opposite the clone")
        rec = self._record
        app = style.node("product", size=1.0).move_to(RIGHT * self.SLOTS[2][0] + UP * self.SLOTS[2][1])
        app_name = style.label_text("outside app", color=style.BLUE).next_to(app, DOWN, buff=0.22)
        x0, x1 = rec.get_right()[0] + 0.12, app.get_left()[0] - 0.12
        pipe = style.tile(x1 - x0, 0.3, style.CYAN, opacity=0.12).move_to(
            RIGHT * (x0 + x1) / 2 + UP * rec.get_center()[1]).set_z_index(style.Z_BACKDROP)
        slack = style.label_text("Slack", color=style.WHITE).next_to(rec, UP, buff=0.22)
        ctx.show(pipe, app, app_name, slack, tag="slack", run_time=0.6, nudge=False)
        rate = style.label_text("1,000 messages a request", color=style.WHITE)
        rate.next_to(pipe, UP, buff=0.4)
        self.play(FadeIn(rate), run_time=0.4)
        # A thousand a request flows until the line reaches "to fifteen".
        for frac in (0.0, 0.25, 0.5):
            self._at(ctx, frac)
            self._stream(pipe, 26, 0.04, run_time=ctx.budget(2.6)[0])
        # May 2025: fifteen a request.
        self._at(ctx, 0.68)
        fifteen = style.label_text("15 messages a request", color=style.RED).move_to(rate)
        # The old limit stays above the new one, ghosted, so the drop reads in a still.
        was = rate.copy().set_color(style.MUTED).scale(0.8).shift(UP * 0.5)
        self.play(pipe.animate.stretch_to_fit_height(0.08), Transform(rate, was), run_time=0.5)
        self.play(FadeIn(fifteen), run_time=0.3)
        # One request a minute: a gate drops across the pipe, and the fifteen wait at it.
        self._at(ctx, 0.8)
        gate = style.tile(0.14, 0.62, style.WHITE, opacity=0.7).move_to(pipe)
        per_min = style.label_text("1 request a minute", color=style.WHITE).next_to(pipe, DOWN, buff=0.45)
        self.play(FadeIn(gate, shift=DOWN * 0.3), FadeIn(per_min), run_time=0.6)
        self._owned["slack"].add(rate, fifteen, gate, per_min)
        self._stream(pipe, 3, 0.3, run_time=ctx.budget(1.2)[0], stop=0.47)
        self._at(ctx, 0.92)
        self.play(*style.highlight(rec, style.GOLD), run_time=0.6)

    def b_licence(self, ctx):
        ctx.lopsided("the held moats gather on the right, one per line, opposite the clone")
        ctx.clear_stage("clone", "record", run_time=0.35)
        ctx.show(self._hold(1, "licences"), tag="licence",
                 anim=lambda m: FadeIn(m, scale=0.85), run_time=ctx.budget(0.6)[0], nudge=False)
        self._at(ctx, 0.6)
        ctx.show(self._hold(2, "moving money"), tag="money",
                 anim=lambda m: FadeIn(m, scale=0.85), run_time=ctx.budget(0.6)[0], nudge=False)

    def b_liability(self, ctx):
        ctx.show(self._hold(3, "liability"), tag="liability",
                 anim=lambda m: FadeIn(m, scale=0.85), run_time=ctx.budget(0.6)[0], nudge=False)
        self._at(ctx, 0.5)
        # Nobody stands behind a weekend clone.
        clone, name = self._owned["clone"]
        self.play(clone.animate.set_opacity(0.2), name.animate.set_opacity(0.4), run_time=0.7)
        self._at(ctx, 0.6)
        nobody = style.label_text("nobody behind it", color=style.MUTED)
        nobody.next_to(name, DOWN, buff=0.3)
        self.play(FadeIn(nobody, shift=UP * 0.1), run_time=0.5)
        self._owned["clone"].add(nobody)

    def b_claims(self, ctx):
        ctx.clear_stage(run_time=0.35)
        # Dots big enough that the grid, not the claim footer under it, carries the frame's weight.
        claims = VGroup(*[Dot(radius=0.17, color=style.GREEN) for _ in range(118)])
        claims.arrange_in_grid(rows=8, cols=15, buff=0.16).move_to(LEFT * 1.9 + UP * 0.05)
        count = style.title_text("118")
        least = style.label_text("at least", color=style.MUTED, size="caption")
        what = style.label_text("companies", color=style.MUTED, size="caption")
        when = style.label_text("Q1 2026", color=style.MUTED, size="caption")
        side = style.text_rows(least, count, what, when, align=LEFT)
        side.next_to(claims, RIGHT, buff=0.8)
        self._at(ctx, 0.05)
        # In a scattered order, so the grid fills evenly rather than top to bottom.
        order = np.random.default_rng(4).permutation(len(claims))
        self.play(LaggedStart(*[FadeIn(claims[i]) for i in order], lag_ratio=0.04),
                  run_time=ctx.budget(4.5)[0])
        self._owned["claims"] = claims
        self._at(ctx, 0.5)
        ctx.show(least, count, what, tag="count", run_time=0.6, nudge=False)
        self._at(ctx, 0.7)
        ctx.show(when, tag="when", run_time=0.5, nudge=False)
        self._at(ctx, 0.88)
        self.play(count.animate.set_color(style.GREEN), run_time=0.6)
