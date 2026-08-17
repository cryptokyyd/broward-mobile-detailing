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


def beads(w=1400, h=800, n=110, seed=7):
    """Water beaded on a dark panel, lit from the upper left.

    Each bead is four pieces: a contact shadow, the body (a radial gradient
    that brightens at the rim the way a real droplet lenses light), a specular
    highlight up-left toward the key light, and a cooler bounce at the lower
    right. Skipping any one of them is what makes CSS-blob 'droplets' read as
    circles rather than water.
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
      <stop offset="0.5" stop-color="{BRAND}" stop-opacity="0.30"/>
      <stop offset="1" stop-color="{GLOSS}" stop-opacity="0.10"/>
    </linearGradient>
    <radialGradient id="bead" cx="0.38" cy="0.34" r="0.72">
      <stop offset="0" stop-color="{GLOSS_HI}" stop-opacity="0.30"/>
      <stop offset="0.45" stop-color="{GLOSS}" stop-opacity="0.13"/>
      <stop offset="0.82" stop-color="{GLOSS_HI}" stop-opacity="0.42"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.55"/>
    </radialGradient>
    <radialGradient id="shadow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#000000" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <filter id="soft" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="1.1"/>
    </filter>
  </defs>''')

    parts.append(f'<rect width="{w}" height="{h}" fill="url(#panel)"/>')
    # A broad diagonal sheen, so the panel reads as curved metal not flat card.
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#sweep)"/>')

    drops = []
    for _ in range(n):
        # Bias right: the headline sits on the left third and wants quiet there.
        x = w * (rnd.random() ** 0.62)
        y = rnd.uniform(0.04, 0.99) * h
        r = rnd.choice([4, 5, 6, 7, 9, 11, 14, 17, 21, 26, 32, 38, 44])
        r *= rnd.uniform(0.82, 1.18)
        # Left-edge beads fade out so they never fight the type.
        edge = min(1.0, (x / (w * 0.42)) ** 1.4)
        op = round(rnd.uniform(0.5, 1.0) * (0.25 + 0.75 * edge), 3)
        drops.append((x, y, r, op))

    # Painter's order: big beads behind small, so overlaps read as depth.
    drops.sort(key=lambda d: -d[2])

    for x, y, r, op in drops:
        g = [f'<g opacity="{op}">']
        g.append(f'<ellipse cx="{x + r*0.10:.1f}" cy="{y + r*0.20:.1f}" '
                 f'rx="{r*1.05:.1f}" ry="{r*0.95:.1f}" fill="url(#shadow)"/>')
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#bead)"/>')
        if r > 6:
            g.append(f'<ellipse cx="{x - r*0.33:.1f}" cy="{y - r*0.38:.1f}" '
                     f'rx="{r*0.26:.1f}" ry="{r*0.20:.1f}" fill="#ffffff" '
                     f'opacity="0.80" filter="url(#soft)"/>')
            g.append(f'<ellipse cx="{x + r*0.34:.1f}" cy="{y + r*0.36:.1f}" '
                     f'rx="{r*0.20:.1f}" ry="{r*0.15:.1f}" fill="{GLOSS}" '
                     f'opacity="0.55" filter="url(#soft)"/>')
        else:
            g.append(f'<circle cx="{x - r*0.28:.1f}" cy="{y - r*0.32:.1f}" '
                     f'r="{max(0.7, r*0.24):.1f}" fill="#ffffff" opacity="0.75"/>')
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

    for name, paths in MARKS.items():
        p = OUT / f"{name}.svg"
        p.write_text(mark(paths), encoding="utf-8")
        written.append(p)

    for p in written:
        print(f"{p.relative_to(OUT.parent.parent)!s:<34}{p.stat().st_size / 1024:>6.1f} KB")


if __name__ == "__main__":
    main()
