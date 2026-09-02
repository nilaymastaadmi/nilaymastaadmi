# -*- coding: utf-8 -*-
"""Bake a recorded game into one animated SVG per theme. No JS, no runtime."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import play

ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
CELL, PAD, TOP, BOT = 34, 40, 60, 18
FRAME = 0.11

THEMES = {
    "dark":  dict(fg="#e6edf3", grid="#21262d", panel="#161b22",
                  body="#3fb950", head="#7ee787", food="#f0883e"),
    "light": dict(fg="#1f2328", grid="#e6eaef", panel="#f6f8fa",
                  body="#2da44e", head="#1a7f37", food="#bc4c00"),
}


def emit(frames, theme):
    c = THEMES[theme]
    n = len(frames)
    dur = round(n * FRAME, 2)
    gw, gh = play.W * CELL, play.H * CELL
    Wd, Ht = gw + PAD * 2, TOP + gh + BOT
    s = []
    a = s.append

    a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
      'role="img" aria-label="A snake game playing itself. It only moves toward the food when a path back to its own tail still exists.">'
      % (Wd, Ht, Wd, Ht))

    a('<text x="%d" y="36" font-family="%s" font-size="26" font-weight="700" fill="%s">'
      'Always a way back</text>' % (PAD, SANS, c["fg"]))

    a('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s"/>'
      % (PAD - 8, TOP - 8, gw + 16, gh + 16, c["panel"]))
    for x in range(play.W):
        for y in range(play.H):
            a('<circle cx="%.1f" cy="%.1f" r="1.5" fill="%s"/>'
              % (PAD + x * CELL + CELL / 2.0, TOP + y * CELL + CELL / 2.0, c["grid"]))

    def anim(attr, vals):
        return ('<animate attributeName="%s" calcMode="discrete" values="%s" dur="%ss" '
                'repeatCount="indefinite"/>' % (attr, ";".join(vals), dur))

    occupancy = {}
    for i, f in enumerate(frames):
        for cell in f["snake"][1:]:
            occupancy.setdefault(cell, set()).add(i)
    for (x, y), on in sorted(occupancy.items()):
        vals = ["1" if i in on else "0" for i in range(n)]
        a('<rect x="%.0f" y="%.0f" width="%d" height="%d" rx="6" fill="%s" opacity="0">%s</rect>'
          % (PAD + x * CELL + 3, TOP + y * CELL + 3, CELL - 6, CELL - 6,
             c["body"], anim("opacity", vals)))

    hx = ["%.0f" % (PAD + f["snake"][0][0] * CELL + 3) for f in frames]
    hy = ["%.0f" % (TOP + f["snake"][0][1] * CELL + 3) for f in frames]
    a('<rect width="%d" height="%d" rx="8" fill="%s" stroke="%s" stroke-width="2">%s%s</rect>'
      % (CELL - 6, CELL - 6, c["head"], c["panel"], anim("x", hx), anim("y", hy)))

    fx = ["%.0f" % (PAD + f["food"][0] * CELL + CELL / 2) for f in frames]
    fy = ["%.0f" % (TOP + f["food"][1] * CELL + CELL / 2) for f in frames]
    a('<circle r="7" fill="%s">%s%s</circle>' % (c["food"], anim("cx", fx), anim("cy", fy)))

    a('</svg>')
    return "".join(s)


def main():
    frames = play.run()
    os.makedirs(ASSETS, exist_ok=True)
    for t in THEMES:
        p = os.path.join(ASSETS, "snake-%s.svg" % t)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(emit(frames, t))
        print("%-20s %6.1f KB" % (os.path.basename(p), os.path.getsize(p) / 1024.0))
    print("frames %d, loop %.1fs" % (len(frames), len(frames) * FRAME))


if __name__ == "__main__":
    main()
