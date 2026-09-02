# -*- coding: utf-8 -*-
"""Bake a recorded game into one animated SVG per theme. No JS, no runtime."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import play

ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
CELL, PAD, TOP, BOT = 34, 40, 78, 46
FRAME = 0.11

THEMES = {
    "dark":  dict(fg="#e6edf3", muted="#9198a1", grid="#21262d", panel="#161b22",
                  body="#3fb950", head="#7ee787", food="#f0883e", bar="#238636"),
    "light": dict(fg="#1f2328", muted="#59636e", grid="#e6eaef", panel="#f6f8fa",
                  body="#2da44e", head="#1a7f37", food="#bc4c00", bar="#2da44e"),
}


def emit(frames, theme):
    c = THEMES[theme]
    n = len(frames)
    dur = round(n * FRAME, 2)
    gw, gh = play.W * CELL, play.H * CELL
    Wd, Ht = gw + PAD * 2, TOP + gh + BOT
    best = max(f["score"] for f in frames)
    s, a = [], None
    a = s.append

    a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
      'role="img" aria-label="A snake game playing itself. %d moves, final score %d, '
      'final length %d.">' % (Wd, Ht, Wd, Ht, n - 1, best, len(frames[-1]["snake"])))

    a('<text x="%d" y="38" font-family="%s" font-size="26" font-weight="700" fill="%s">'
      'snake plays itself</text>' % (PAD, SANS, c["fg"]))
    a('<text x="%d" y="60" font-family="%s" font-size="13" fill="%s">'
      '%d moves baked into one SVG. no javascript, nothing to click.</text>'
      % (PAD, MONO, c["muted"], n - 1))
    a('<text x="%d" y="38" text-anchor="end" font-family="%s" font-size="13" fill="%s">'
      'grows to %d</text>' % (Wd - PAD, MONO, c["muted"], len(frames[-1]["snake"])))

    a('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s"/>'
      % (PAD - 8, TOP - 8, gw + 16, gh + 16, c["panel"]))
    for x in range(play.W):
        for y in range(play.H):
            a('<circle cx="%.1f" cy="%.1f" r="1.5" fill="%s"/>'
              % (PAD + x * CELL + CELL / 2.0, TOP + y * CELL + CELL / 2.0, c["grid"]))

    def anim(attr, vals):
        return ('<animate attributeName="%s" calcMode="discrete" values="%s" dur="%ss" '
                'repeatCount="indefinite"/>' % (attr, ";".join(vals), dur))

    # Body: one rect per cell, switched on for the frames it is occupied.
    occupancy = {}
    for i, f in enumerate(frames):
        for cell in f["snake"][1:]:
            occupancy.setdefault(cell, set()).add(i)
    for (x, y), on in sorted(occupancy.items()):
        vals = ["1" if i in on else "0" for i in range(n)]
        if "1" not in vals:
            continue
        a('<rect x="%.0f" y="%.0f" width="%d" height="%d" rx="6" fill="%s" opacity="0">%s</rect>'
          % (PAD + x * CELL + 3, TOP + y * CELL + 3, CELL - 6, CELL - 6,
             c["body"], anim("opacity", vals)))

    # Head and food are single elements that hop between cells.
    hx = ["%.0f" % (PAD + f["snake"][0][0] * CELL + 3) for f in frames]
    hy = ["%.0f" % (TOP + f["snake"][0][1] * CELL + 3) for f in frames]
    a('<rect width="%d" height="%d" rx="8" fill="%s" stroke="%s" stroke-width="2">%s%s</rect>'
      % (CELL - 6, CELL - 6, c["head"], c["panel"], anim("x", hx), anim("y", hy)))

    fx = ["%.0f" % (PAD + f["food"][0] * CELL + CELL / 2) for f in frames]
    fy = ["%.0f" % (TOP + f["food"][1] * CELL + CELL / 2) for f in frames]
    a('<circle r="7" fill="%s">%s%s</circle>' % (c["food"], anim("cx", fx), anim("cy", fy)))

    # Length bar along the bottom.
    bw = ["%.0f" % (gw * len(f["snake"]) / float(len(frames[-1]["snake"]))) for f in frames]
    a('<rect x="%d" y="%d" width="%d" height="3" rx="1.5" fill="%s" opacity="0.18"/>'
      % (PAD, TOP + gh + 22, gw, c["bar"]))
    a('<rect x="%d" y="%d" height="3" rx="1.5" fill="%s">%s</rect>'
      % (PAD, TOP + gh + 22, c["bar"], anim("width", bw)))

    a('<text x="%d" y="%d" font-family="%s" font-size="12.5" fill="%s">'
      'it only goes for the food when it can still reach its own tail afterwards. '
      'that is the whole trick.</text>' % (PAD, TOP + gh + 42, MONO, c["muted"]))
    a('</svg>')
    return "".join(s)


def main():
    frames = play.run()
    os.makedirs(ASSETS, exist_ok=True)
    for t in THEMES:
        p = os.path.join(ASSETS, "snake-%s.svg" % t)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(emit(frames, t))
        print("%-28s %6.1f KB" % (os.path.basename(p), os.path.getsize(p) / 1024.0))
    print("frames %d  dur %.1fs  score %d  length %d"
          % (len(frames), len(frames) * FRAME, frames[-1]["score"], len(frames[-1]["snake"])))


if __name__ == "__main__":
    main()
