# assets/media

## What is here now

`make-art.py` at the repo root generates all of it — vector, hand-authored,
deterministic (fixed seed, so a rerun is a no-op in the diff).

| File | Where |
|---|---|
| `hero-beads.svg` | Landscape — home hero, and the opening band of all 64 other pages |
| `hero-beads-tall.svg` | Portrait — the same bands under 700px |
| `mk-*.svg` | Tile watermarks, one per service |

~190 KB raw, ~25 KB over the wire once the CDN compresses it (these are text
and they gzip about 8:1), sharp at any resolution.

Two orientations because `cover` on a tall narrow band scales the landscape
file about 1.9x: a handful of enormous beads fill the screen and the rest of
the field is never seen. The portrait file is drawn at roughly the shape it is
displayed at, with smaller beads to survive the upscale.

### The contrast floor

The gradient over the artwork is not styling to taste — it is what keeps the
type readable over a busy ground, and the numbers are measured rather than
guessed. The binding constraint is `.trust__l`, the smallest type on the page,
which runs the full width of the band and so meets the transparent end of the
ramp. At the far stop it sits at 4.80:1 against the ground; WCAG AA wants 4.5.

So: **lightening the far end of the `.hero` ramp past 0.42 alpha drops that
below AA.** If you want more of the artwork showing, raise the bead count or
lower the specular opacity in `make-art.py` instead — that adds texture
without adding peak brightness.

## Replacing it with photography

Slots the site uses if the files are present, and silently skips if
they are not. They are CSS backgrounds, so a missing file leaves the graphite
ground showing rather than a broken-image icon — the page is never worse for
an empty slot, and nothing needs regenerating when you drop files in.

| Filename | Where it appears | Good size |
|---|---|---|
| `hero-beading.png` | Home hero, full-bleed behind the headline | ~1400×800, landscape |
| `svc-full.png` | "Full detail" tile (the large one) | ~620×460 |
| `svc-interior.png` | "Interior detail" tile | ~620×460 |
| `svc-exterior.png` | "Exterior detail" tile | ~620×460 |
| `svc-ceramic.png` | "Ceramic coating" tile | ~620×460 |
| `svc-correction.png` | "Paint correction" tile | ~620×460 |
| `svc-headlight.png` | "Headlight restoration" tile | ~620×460 |

`.jpg` works too — change the extension in `build-pages.py` (`media=` on each
service) and in the `.hero` rule at the bottom of `styles.css`.

## Keep these honest

These slots are decorative: atmosphere and craft, the same role stock
photography plays on any service site. That is fine.

What is **not** fine is putting invented before/after pairs in the `.ba`
frames and presenting them as work you did. This site's entire argument is
that the price and the work are straight. Fabricated proof is the one thing
that would undermine it, and it is also the thing a detailer buying your
leads will notice fastest. Leave the before/after frames empty until you have
real photographs from real jobs.

## Weight

Full-size generations run 1–2 MB each, which is far too heavy for a phone on
5G in a driveway. Resize to the sizes above and save at JPEG quality ~70
before committing. Everything here sits under a heavy dark gradient, so
aggressive compression is not visible.
