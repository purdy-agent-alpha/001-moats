"""
Visual system for the moats video ("Code is cheap. What keeps a company alive?").

Copied from Levi's video 2 style module and kept to its rules: one source of
truth for palette, type scale and shape grammar. Scenes never hardcode a colour
or a font size; they ask for a role.

The palette is video 2's. The shape grammar below is this video's own, written
before the first scene (notes/video-standard.md, rule 2.3): a shape and its
colour mean one thing for the whole video, and emphasis brightens a shape in its
own colour, never turns it into another kind.

    product    blue square         what a company ships: code, an app
    clone      blue dashed square  a rebuild of a product: same shape, no body
    moat       gold hexagon        what a clone cannot generate on demand
                                   (a record, a licence, liability, support,
                                   connected power). A moat that dies stays a
                                   hexagon: it is dimmed and struck in red.
    customer   cyan circle         a customer or an account
    agent      violet diamond      an AI agent acting for someone (Alpha, the narrator, too)
    person     white circle        Levi, who directs the work and asks the questions
    figure     record card         one number from a source; its stroke is the
                                   colour of its claim kind
    castle     a product with a gold hexagon ring round it: a business and its moat
    network    small cyan circles joined by grey lines (pipeline/charts.py): people
                                   or members connected to each other; a live link
                                   pulses, a lost one goes red

Charts (Levi: "they were all just bar graphs"): each figure takes the shape of
its data, from pipeline/charts.py: a scatter with its pareto frontier, a line over
time (log where the data spans orders of magnitude), a waffle of a hundred squares
for a share, a slope chart for before and after, a waterfall for how a number is
made, a network graph for who is connected. Bars only where the data is a few
magnitudes side by side. Measured data is green, a frontier or reference line white,
a guide or a projection dashed.

Claim kinds (rule 3.3), on a chip in the caption lane with the source:
    measured  green   a filing, a price, a count, a survey, a trial
    reported  grey    a news report of what someone did
    argued    grey    an essay or analyst's argument
    guess     amber   my inference, no source behind it
    levi      white   Levi's own view as he gave it
Red is reserved for loss: a struck moat, a falling bar, a price drop.
"""
from __future__ import annotations

from manim import *

# ---------------------------------------------------------------- palette ---
BG = "#00020A"
PANEL = "#070C1A"
PANEL_HI = "#0C1426"
GRID = "#1F2B42"
WHITE = "#F4F7FF"
MUTED = "#8791A8"
DIM = "#4A5468"

CYAN = "#20F7D2"
BLUE = "#4D8DFF"
VIOLET = "#B45CFF"
GOLD = "#FFCB4D"
RED = "#FF4D6D"
GREEN = "#49F28D"
AMBER = "#FF9E45"

# Shape grammar: the contract the storyboard promises the viewer.
NODE_KINDS = {
    "product": {"color": BLUE, "shape": "square"},
    "clone": {"color": BLUE, "shape": "dashed_square"},
    "moat": {"color": GOLD, "shape": "hexagon"},
    "customer": {"color": CYAN, "shape": "circle"},
    "agent": {"color": VIOLET, "shape": "diamond"},
    "figure": {"color": GREEN, "shape": "record"},
    "person": {"color": WHITE, "shape": "circle"},
}

CLAIM_KINDS = {
    "measured": GREEN,
    "reported": MUTED,
    "argued": MUTED,
    "guess": AMBER,
    "levi": WHITE,
}

# ------------------------------------------------------------- type scale ---
# Sizes are in Manim font_size units, tuned so the smallest is still legible
# after a 480p preview downscale. QA enforces MIN_FONT_SIZE.
TYPE = {
    "title": 40,
    "caption": 28,
    "label": 22,
    "node": 17,
    "field": 17,
    # 17, not 16. Pango's space advance rounds down a whole pixel below 17pt, so
    # every multi-word label set at 16 rendered with a ~3.5px word gap at review
    # size and read as one word — "makes an" as "makesan". At 17 the same phrases
    # come out at 6px. One point of type size, and a whole class of defect.
    "tiny": 17,
}
MIN_FONT_SIZE = 15
MONO = "DejaVu Sans Mono"

# Texts need air between them, not merely an absence of overlap. Below this gap
# two lines read as one block. Both the placement helper and the gate use this
# number, so a layout that satisfies the placer cannot fail the gate.
MIN_TEXT_GAP = 0.16

# The placer aims for MIN_TEXT_GAP + this, never for MIN_TEXT_GAP itself. Aiming
# exactly at a threshold lands on the wrong side of it about half the time once
# floating point is involved: the first version placed three labels at a
# computed 0.16 and the gate read all three back as 0.15999 and failed them.
PLACEMENT_MARGIN = 0.03

# ----------------------------------------------------------- draw layers ---
# Manim's renderer flattens the whole scene and sorts it by ``z_index`` with a
# *stable* sort, so a z_index is the only way to state a layering rule that
# holds across group boundaries. Sibling reordering cannot: an edge living
# inside a `chain` VGroup will always draw over a node that sits in a different
# top-level group, however carefully the two groups sort their own children.
# That is exactly the bug that put connectors on top of the code node for 23
# seconds in section 1.
#
# Lower draws earlier, i.e. further back.
Z_BACKDROP = -20   # zone bands, grids, anything content sits on top of
Z_EDGE = -10       # connectors: never in front of what they join
Z_NODE = 0         # shapes, cards, labels — the default
Z_SLATE = 50       # the review identifier, above everything


def _word_metrics(t: Text, source: str) -> tuple[float, float]:
    """
    (smallest gap between words, median gap between letters) — in scene units.

    Counting glyphs to find the word boundaries is the obvious approach and it is
    wrong: Pango ligates some pairs, so "verification" renders as eleven glyphs
    for twelve characters and every boundary after it is off by one. That made
    the check measure the gap between two letters and report the phrase as
    merged when it was fine.

    So don't rely on the mapping. There are exactly as many word gaps as there
    are spaces, and a word gap is normally wider than a letter gap — so take the
    N widest gaps as the word gaps. The estimate can only be too generous, which
    makes the check conservative: it under-reports rather than inventing faults.
    """
    import numpy as _np
    glyphs = [g for g in t.submobjects if len(g.get_all_points())]
    n_spaces = source.count(" ")
    if len(glyphs) < 2 or n_spaces == 0:
        return (99.0, 0.0)
    gaps = sorted(
        (glyphs[i + 1].get_left()[0] - glyphs[i].get_right()[0]
         for i in range(len(glyphs) - 1)), reverse=True)
    n = min(n_spaces, len(gaps))
    return (float(gaps[n - 1]), float(_np.median(gaps[n:])) if len(gaps) > n else 0.0)


def _stamp(t: Text, source: str | None = None) -> Text:
    """
    Remember how big this text was built, and how big its geometry was then.

    Manim computes ``Text.font_size`` from the mobject's height, which a 3D
    scene's upright rotation drives to zero. The pair recorded here lets QA
    recover the rendered size from the point cloud instead, which rotation
    cannot disturb and scaling still moves.
    """
    import numpy as _np
    pts = t.get_all_points()
    t.qa_pt0 = float(t.font_size)
    t.qa_diag0 = (float(_np.linalg.norm(pts.max(axis=0) - pts.min(axis=0)))
                  if len(pts) else 0.0)
    t.qa_word_gap0, t.qa_letter_gap0 = _word_metrics(t, source if source is not None else "")
    return t


def title_text(text: str) -> Text:
    return _stamp(Text(text, color=WHITE, font_size=TYPE["title"], weight=BOLD), text)


def caption_text(text: str, color: str = WHITE) -> Text:
    return _stamp(Text(text, color=color, font_size=TYPE["caption"], weight=MEDIUM), text)


def label_text(text: str, color: str = WHITE, size: str = "label") -> Text:
    return _stamp(Text(text, color=color, font_size=TYPE[size]), text)


def mono_text(text: str, color: str = WHITE, size: str = "field") -> Text:
    return _stamp(Text(text, font=MONO, color=color, font_size=TYPE[size]), text)


# ----------------------------------------------------------------- shapes ---
def _base_shape(kind: str, color: str, size: float) -> VMobject:
    shape_name = NODE_KINDS.get(kind, {}).get("shape", "record")
    if shape_name == "hexagon":
        shape = RegularPolygon(n=6, radius=size / 2, color=color)
    elif shape_name == "square":
        shape = Square(side_length=size, color=color)
    elif shape_name == "dashed_square":
        # A clone has the product's outline and none of its body: no fill, and a
        # dashed stroke. Returned early so the panel fill below never lands on it.
        return DashedVMobject(Square(side_length=size, color=color).set_stroke(color, width=2.6),
                              num_dashes=24)
    elif shape_name == "circle":
        shape = Circle(radius=size / 2, color=color)
    elif shape_name == "diamond":
        shape = Square(side_length=size * 0.8, color=color).rotate(PI / 4)
    elif shape_name == "document":
        shape = RoundedRectangle(corner_radius=0.05, width=size * 0.86, height=size * 1.1, color=color)
    else:
        shape = RoundedRectangle(corner_radius=0.07, width=size * 1.3, height=size * 0.8, color=color)
    # Filled in its own colour at 0.18 over an opaque panel: outlines alone on a
    # dark ground read as confetti (video 2, HANDOFF.md section 4).
    shape.set_fill(interpolate_color(ManimColor(PANEL), ManimColor(color), 0.18), opacity=0.96)
    shape.set_stroke(color, width=2.6)
    return shape


def node(kind: str, text: str = "", size: float = 1.0, color: str | None = None,
         font_size: int | None = None) -> VGroup:
    """
    An artifact node. Returns VGroup(aura, shape, label) — always that order, so
    highlight helpers can stroke the shape without mangling the label.

    The label is auto-fitted inside the shape; a label that cannot fit at the
    minimum legible size raises, rather than silently overflowing.
    """
    if kind not in NODE_KINDS:
        # A misspelt or foreign kind used to fall back to a white record without a
        # word, which is how the selftest's video-2 kinds silently stopped one check.
        raise ValueError(f"node kind {kind!r} is not in this video's grammar: {sorted(NODE_KINDS)}")
    color = color or NODE_KINDS[kind]["color"]
    shape = _base_shape(kind, color, size)
    aura = shape.copy().set_stroke(color, width=9, opacity=0.12).set_fill(opacity=0)
    group = VGroup(aura, shape)
    group.qa_role = "node"
    group.qa_kind = kind
    if text:
        fs = font_size or TYPE["node"]
        label = _stamp(Text(text, color=WHITE, font_size=fs, weight=MEDIUM), text)
        inner = shape.width * 0.78
        if label.width > inner:
            scale = inner / label.width
            if fs * scale < MIN_FONT_SIZE:
                raise ValueError(
                    f"node({kind!r}, {text!r}) cannot fit its label at >= "
                    f"{MIN_FONT_SIZE}pt inside size={size}. Shorten the label or grow the node."
                )
            label.scale(scale)
        label.move_to(shape)
        label.qa_role = "label"
        group.qa_label = label
        group.add(label)
    return group


def highlight(n: Mobject, color: str = GOLD):
    """
    Animations that light a mobject without touching any text inside it.

    Nodes made by `node()` are VGroup(aura, shape, label) and get the aura
    treatment; anything else — a plain rectangle, a packet outline — just gets a
    heavier stroke. Assuming the node shape and indexing blindly turned every
    highlight on a plain shape into a render-time crash.
    """
    if getattr(n, "qa_role", None) == "node" and len(n.submobjects) >= 2:
        return [
            n[0].animate.set_stroke(color, width=13, opacity=0.6),
            n[1].animate.set_stroke(color, width=4),
        ]
    # Never stroke text. `set_stroke` on a group reaches the glyphs too, and a
    # 5-wide stroke on a letterform closes up its counters — the text goes bold,
    # muddy and harder to read, which is the opposite of highlighting it.
    targets = [s for s in n.get_family()
               if not _is_text_like(s) and len(getattr(s, "points", []))]
    if not targets:
        return [n.animate.set_color(color)]
    return [s.animate.set_stroke(color, width=5) for s in targets]


def _is_text_like(mob: Mobject) -> bool:
    if getattr(mob, "text", None) is not None:
        return True
    parent_text = getattr(mob, "qa_role", None) == "label"
    return parent_text or type(mob).__name__.startswith("VMobjectFromSVGPath")


def glow_arrow(start, end, color: str = CYAN, width: float = 3.4, buff: float = 0.16) -> VGroup:
    aura = Arrow(start, end, color=color, stroke_width=width * 2.6, buff=buff).set_opacity(0.16)
    core = Arrow(start, end, color=color, stroke_width=width, buff=buff)
    group = VGroup(aura, core)
    # Tag only the stroke that actually has points. The wrapping VGroup has none,
    # and asking it for an endpoint raises.
    core.qa_role = "edge"
    group.qa_layer = "edge"      # the stage sends these to the back on show
    # Belt and braces: the back-seating below is a scene-order fix, this is a
    # renderer-order fix, and only the second one survives being re-parented
    # into somebody else's VGroup.
    group.set_z_index(Z_EDGE, family=True)
    return group


def connect(a: Mobject, b: Mobject, color: str = CYAN, width: float = 3.4) -> VGroup:
    """
    Arrow between two mobjects, anchored on the line between their centres so the
    head always lands on the boundary it is pointing at — never inside the label.
    """
    start = a.get_center()
    end = b.get_center()
    direction = end - start
    norm = np.linalg.norm(direction)
    if norm < 1e-6:
        raise ValueError("connect() needs two mobjects at different positions")
    unit = direction / norm
    return glow_arrow(
        a.get_boundary_point(unit) + unit * 0.06,
        b.get_boundary_point(-unit) - unit * 0.06,
        color=color, width=width, buff=0.0,
    )


def text_rows(*mobs: Mobject, buff: float | None = None, align=LEFT) -> VGroup:
    """
    Stack label rows with a gap the crowding check will accept.

    Writing `arrange(DOWN, buff=MIN_TEXT_GAP)` looks exactly right and fails:
    the rows land at precisely the threshold, and the gate reads the same
    distance back as 0.15999. Rows built through here clear the bar instead of
    balancing on it.
    """
    if buff is None:
        buff = MIN_TEXT_GAP + PLACEMENT_MARGIN
    return VGroup(*mobs).arrange(DOWN, buff=buff, aligned_edge=align)


def cursor_for(mob: Mobject, color: str = GOLD, width: float = 4.0,
               pad: float = 0.22) -> Circle:
    """
    A ring that actually goes round the thing it marks.

    A fixed-radius circle marks a one-word node and cuts straight through a
    longer one — "traversal" spent fifteen seconds with a gold line through the
    middle of it. Size the ring from the node, not from a constant.
    """
    r = max(mob.width, mob.height) / 2 + pad
    ring = Circle(radius=r, color=color, stroke_width=width)
    ring.move_to(mob.get_center())
    return ring


def allow_overlap(mob: Mobject, *others: Mobject, reason: str = ""):
    """
    Declare that `mob` is *meant* to sit over `others`.

    A stamp landing across a quote is a deliberate composition, not a layout bug.
    Declaring it keeps the overlap checker strict everywhere else instead of
    forcing the tolerance up globally, which is how these checks stop working.
    """
    def texts(m):
        return [str(getattr(s, "text", "")) for s in m.get_family()
                if getattr(s, "text", None)]

    mine = texts(mob)
    theirs = [t for o in others for t in texts(o)]
    for sub in mob.get_family():
        if getattr(sub, "text", None):
            sub.qa_allow_overlap = theirs
            sub.qa_allow_reason = reason
    for o in others:
        for sub in o.get_family():
            if getattr(sub, "text", None):
                sub.qa_allow_overlap = mine
                sub.qa_allow_reason = reason
    return mob


def strip_labels(*nodes: Mobject) -> None:
    """
    Remove the text from nodes, immediately and permanently.

    Deliberately not an animation. Two reasons, both learned the hard way:

    * `FadeOut` on a label is a no-op that then *restores* the opacity, because
      the label is a submobject the scene does not hold directly.
    * Returning `.animate` chains puts two animations on one family; the group's
      own `.animate.scale(...)` captured its target before the opacity changed,
      so it faithfully restored every label it was supposed to remove.

    Call this immediately before the play that moves or scales the node, so the
    text goes as the shape transforms. A label evaporating off a shape that then
    sits still reads as a rendering glitch — and the QA gate will say so.
    """
    for node in nodes:
        for sub in node.get_family():
            if getattr(sub, "text", None):
                sub.set_opacity(0)


def restroke(mob: Mobject, color: str, width: float = 3.0):
    """
    Change a mobject's stroke without touching any text inside it.

    `mob.animate.set_stroke(...)` reaches every submobject, so calling it on a
    node group strokes the label as well and thickens the letterforms until they
    are hard to read. Use this anywhere a group might contain text.
    """
    targets = [s for s in mob.get_family()
               if not _is_text_like(s) and len(getattr(s, "points", []))]
    if not targets:
        return [mob.animate.set_color(color)]
    return [s.animate.set_stroke(color, width=width) for s in targets]


# ------------------------------------------------------------ this video ---
def claim_footer(kind: str, source: str = "") -> VGroup:
    """
    A dot in the claim kind's colour, then one line: the kind word in that
    colour, a middle dot, the short source name in grey.

    One Text, not a chip plus a label: the caption lane holds one thing at a
    time (the gate's caption_stack). No pill round the word: any outline round
    part of a Text runs through the Text's box (outline_over_text). Set at the
    caption size: at 17 and 22 the word gaps of a source name merged.
    """
    color = CLAIM_KINDS[kind]
    word = "Levi's view" if kind == "levi" else kind
    # Single spaces only: the gate finds word gaps by counting spaces.
    text = f"{word} · {source}" if source else word
    line = _stamp(Text(text, color=MUTED, font_size=TYPE["caption"]), text)
    VGroup(*line[:len(word.replace(" ", ""))]).set_color(color if kind in ("measured", "guess") else WHITE)
    dot = RoundedRectangle(corner_radius=0.06, width=0.24, height=0.24)
    dot.set_fill(color, opacity=1.0).set_stroke(width=0)
    return VGroup(dot, line).arrange(RIGHT, buff=0.22)


def tile(width: float, height: float, color: str, opacity: float = 0.18) -> Rectangle:
    """A bar or panel filled in its own colour, never a bare outline."""
    r = Rectangle(width=width, height=height, color=color)
    r.set_fill(color, opacity=opacity).set_stroke(color, width=2.2)
    return r


def strike(mob: Mobject, color: str = RED, width: float = 5.0) -> Line:
    """A red line through a moat that dies. The shape stays what it was."""
    line = Line(mob.get_corner(DL) + LEFT * 0.08, mob.get_corner(UR) + RIGHT * 0.08,
                color=color, stroke_width=width)
    return line
