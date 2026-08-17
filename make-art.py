#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates the site's vector artwork into assets/media/.

    python make-art.py

Why vector and not photography: an SVG is a few KB, stays sharp on any screen,
costs no extra request weight worth worrying about, and — the practical part —
it can be authored here rather than sourced. Real job photographs beat this the
day they exist; until then this is a deliberate look rather than an empty slot.

Deterministic: a fixed seed means rerunning produces byte-identical files, so
this never shows up as noise in a diff.
"""
import random, pathlib

OUT = pathlib.Path(__file__).parent / "assets" / "media"
OUT.mkdir(parents=True, exist_ok=True)

# Brand tokens, duplicated here as hex because SVG has no access to the CSS
# custom properties. Keep in step with :root in styles.css.
STEEL_DEEP = "#12141c"
STEEL      = "#1d2130"
BRAND      = "#2f57c9"
GLOSS      = "#5fb7e0"
GLOSS_HI   = "#9fd8ef"


def beads(w=1400, h=800, n=330, seed=7, rmax=25.0, bias=True):
    """Water beaded on dark paint, lit from the upper left.

    `bias` biases the field to the right and fades it out on the left, which is
    what a landscape banner wants: the headline sits on the left third and
    needs quiet there. Turn it off for the portrait variant, where the copy
    spans the full width and there is no side to fade towards — that one wants
    an even, fainter field instead. `rmax` caps bead size: a phone crops a far
    smaller slice of the artwork, so its beads have to be drawn smaller to
    survive being scaled up.

    The hard part is not drawing circles, it is not drawing *bubbles*. A soap
    bubble is large, evenly translucent, and ringed with light the whole way
    round. A water bead on dark paint is the opposite on every count, and these
    four cues are what separate them:

      1. Scale and crowding. Beads are small and many — hundreds of tiny ones
         with a scattering of large. A field of evenly large spheres is foam.
      2. They are domes, not spheres. Surface tension against a contact angle
         leaves them wider than they are tall, so each one is an ellipse.
      3. The middle goes *darker*, not lighter. A bead is a lens, and what it
         has to show is the dark paint underneath it.
      4. The bright part is a crescent low on the bead, where light refracts
         through and exits. That crescent is the strongest water cue there is,
         and a full bright rim — which is what the first version drew — undoes
         it by turning the bead straight back into a bubble.
    """
    rnd = random.Random(seed)
    parts = []

    parts.append(f'''<defs>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{STEEL_DEEP}"/>
      <stop offset="0.55" stop-color="{STEEL}"/>
      <stop offset="1" stop-color="{STEEL_DEEP}"/>
    </linearGradient>
    <linearGradient id="sweep" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="{BRAND}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{BRAND}" stop-opacity="0.26"/>
      <stop offset="1" stop-color="{GLOSS}" stop-opacity="0.09"/>
    </linearGradient>
    <!-- The reflection band a curved panel throws. Without it the beads have
         nothing to sit on and the whole field floats. -->
    <linearGradient id="sheen" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0.30" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="0.50" stop-color="#ffffff" stop-opacity="0.055"/>
      <stop offset="0.70" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <!-- Lens: a bright pinprick off-centre, darkening through the body, and
         only a thin cool rim. The old version ended on white at 0.55, which is
         precisely the bubble ring this is avoiding. -->
    <radialGradient id="bead" cx="0.36" cy="0.31" r="0.80">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.13"/>
      <stop offset="0.42" stop-color="#000000" stop-opacity="0.20"/>
      <stop offset="0.86" stop-color="#000000" stop-opacity="0.12"/>
      <stop offset="1" stop-color="{GLOSS_HI}" stop-opacity="0.26"/>
    </radialGradient>
    <radialGradient id="shadow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#000000" stop-opacity="0.42"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <filter id="soft" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="0.7"/>
    </filter>
    <!-- The crescent needs far more blur than the specular. Sharp, it reads as
         a pale disc sitting inside the bead rather than light leaving it. -->
    <filter id="melt" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="2.2"/>
    </filter>
  </defs>''')

    parts.append(f'<rect width="{w}" height="{h}" fill="url(#panel)"/>')
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#sweep)"/>')
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#sheen)"/>')

    drops = []
    for _ in range(n):
        x = w * (rnd.random() ** 0.62) if bias else rnd.random() * w
        y = rnd.uniform(0.03, 0.99) * h
        # A power law rather than a uniform pick from a size list. The exponent
        # is what keeps the field mostly tiny with a few large beads, which is
        # how water actually distributes itself across a panel.
        r = 1.8 + (rnd.random() ** 2.7) * rmax
        if bias:
            # Left-edge beads fade out so they never fight the type.
            edge = min(1.0, (x / (w * 0.42)) ** 1.4)
            op = round(rnd.uniform(0.55, 1.0) * (0.22 + 0.78 * edge), 3)
        else:
            op = round(rnd.uniform(0.45, 0.85), 3)
        drops.append((x, y, r, op))

    # Painter's order: big beads behind small, so overlaps read as depth.
    drops.sort(key=lambda d: -d[2])

    for x, y, r, op in drops:
        ry = r * 0.86                      # a dome, not a sphere
        g = [f'<g opacity="{op}">']
        # Contact shadow: tight, and just below, so the bead sits on the paint.
        # Drawn wider than the bead — against the hero's blue glow a shadow the
        # same size as the bead disappears under it and the field floats.
        g.append(f'<ellipse cx="{x:.1f}" cy="{y + ry*0.34:.1f}" '
                 f'rx="{r*1.24:.1f}" ry="{ry*1.00:.1f}" fill="url(#shadow)"/>')
        g.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" '
                 f'ry="{ry:.1f}" fill="url(#bead)"/>')
        if r > 4.5:
            # The refraction crescent, low and opposite the key light. An
            # ellipse rather than an arc: at this scale it reads identically
            # and costs a fraction of the path data.
            g.append(f'<ellipse cx="{x + r*0.14:.1f}" cy="{y + ry*0.58:.1f}" '
                     f'rx="{r*0.56:.1f}" ry="{ry*0.15:.1f}" fill="{GLOSS_HI}" '
                     f'opacity="0.34" filter="url(#melt)"/>')
            g.append(f'<ellipse cx="{x - r*0.34:.1f}" cy="{y - ry*0.40:.1f}" '
                     f'rx="{r*0.20:.1f}" ry="{ry*0.15:.1f}" fill="#ffffff" '
                     f'opacity="0.78" filter="url(#soft)"/>')
        else:
            # Below about 4px the crescent is sub-pixel; one lit dot is all
            # that survives, and it is enough to read as water.
            g.append(f'<circle cx="{x - r*0.30:.1f}" cy="{y - ry*0.34:.1f}" '
                     f'r="{max(0.55, r*0.30):.1f}" fill="#ffffff" opacity="0.70"/>')
        g.append('</g>')
        parts.append("".join(g))

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" '
            f'role="presentation">\n  ' + "\n  ".join(parts) + '\n</svg>\n')


def mark(paths, w=240, h=180, seed=0):
    """A tile watermark: oversized line art, cropped by the tile edge."""
    body = "\n      ".join(paths)
    # Held at 0.5: a watermark that competes with the heading stops being a
    # watermark. The tile copy is the content; this is texture behind it.
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" fill="none" stroke="{GLOSS}" '
            f'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" '
            f'role="presentation">\n    <g opacity="0.5">\n      {body}\n    </g>\n</svg>\n')


# Line art, drawn rather than pulled from an icon set so the weight and the
# corner radii match the rest of the site.
MARKS = {
    # A car silhouette under falling water — the whole-vehicle service.
    "mk-full": [
        '<path d="M34 116h172M46 116c0-24 10-34 22-38l14-20h56l14 20c12 4 22 14 22 38"/>',
        '<circle cx="72" cy="118" r="14"/><circle cx="168" cy="118" r="14"/>',
        '<path d="M82 78h76" opacity=".55"/>',
        '<path d="M60 40c0 6-5 8-5 14a5 5 0 0 0 10 0c0-6-5-8-5-14Z" opacity=".8"/>',
        '<path d="M120 26c0 7-6 9-6 16a6 6 0 0 0 12 0c0-7-6-9-6-16Z" opacity=".8"/>',
        '<path d="M182 44c0 6-5 8-5 13a5 5 0 0 0 10 0c0-5-5-7-5-13Z" opacity=".8"/>',
    ],
    # A seat, with an extraction wand.
    "mk-interior": [
        '<path d="M62 138V70c0-16 10-26 26-26h34c16 0 26 10 26 26v10"/>',
        '<path d="M62 104h86c14 0 20 8 20 20v14"/>',
        '<path d="M52 138h130"/>',
        '<path d="M186 34l-22 46" opacity=".8"/><path d="M178 30l14 8-6 12-14-8Z" opacity=".8"/>',
    ],
    # A wash mitt over a panel, with suds.
    "mk-exterior": [
        '<path d="M40 128c30-16 62-24 96-24s60 6 84 18"/>',
        '<path d="M74 84c0-14 8-22 22-22h44c14 0 22 8 22 22v14H74Z"/>',
        '<path d="M96 62V46c0-8 6-12 14-12h24c8 0 14 4 14 12v16" opacity=".7"/>',
        '<circle cx="52" cy="52" r="9" opacity=".7"/><circle cx="74" cy="34" r="6" opacity=".55"/>',
        '<circle cx="188" cy="46" r="8" opacity=".7"/><circle cx="206" cy="66" r="5" opacity=".5"/>',
    ],
    # A shield with a bead rolling off it — the coating.
    "mk-ceramic": [
        '<path d="M120 30l58 22v44c0 34-24 56-58 68-34-12-58-34-58-68V52Z"/>',
        '<path d="M120 62c0 14-12 18-12 30a12 12 0 0 0 24 0c0-12-12-16-12-30Z"/>',
        '<path d="M92 118c8 10 18 16 28 20" opacity=".5"/>',
    ],
    # A polisher head with swirl marks resolving into clean paint.
    "mk-correction": [
        '<circle cx="112" cy="96" r="42"/><circle cx="112" cy="96" r="22" opacity=".6"/>',
        '<path d="M112 54V32h20" opacity=".8"/>',
        '<path d="M170 60c14 6 22 14 26 22" opacity=".45"/>',
        '<path d="M176 88c12 4 18 10 20 16" opacity=".45"/>',
        '<path d="M180 116c10 3 15 8 16 12" opacity=".45"/>',
    ],
    # A headlight, hazy half and clear half.
    "mk-headlight": [
        '<path d="M46 66c26-14 58-22 92-22 30 0 52 6 72 16v72c-20 10-42 16-72 16-34 0-66-8-92-22Z"/>',
        '<circle cx="120" cy="94" r="26"/><circle cx="120" cy="94" r="11" opacity=".6"/>',
        '<path d="M62 78v34" opacity=".45"/><path d="M78 70v50" opacity=".35"/>',
    ],
}


def main():
    written = []
    p = OUT / "hero-beads.svg"
    p.write_text(beads(), encoding="utf-8")
    written.append(p)

    # Portrait variant. A phone crops a tall narrow slice, and `cover` on the
    # landscape file scales it about 1.9x — so a handful of enormous beads fill
    # the band and the rest of the field is never seen. Drawn to the shape it
    # is actually displayed at, with smaller beads to survive the upscale.
    p = OUT / "hero-beads-tall.svg"
    p.write_text(beads(w=560, h=1200, n=300, seed=11, rmax=12.0, bias=False),
                 encoding="utf-8")
    written.append(p)

    for name, paths in MARKS.items():
        p = OUT / f"{name}.svg"
        p.write_text(mark(paths), encoding="utf-8")
        written.append(p)

    for p in written:
        print(f"{p.relative_to(OUT.parent.parent)!s:<34}{p.stat().st_size / 1024:>6.1f} KB")


if __name__ == "__main__":
    main()
