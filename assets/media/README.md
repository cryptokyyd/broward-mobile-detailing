# assets/media

Image slots the site will use if the files are present, and silently skip if
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
