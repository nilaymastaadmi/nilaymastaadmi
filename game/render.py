# -*- coding: utf-8 -*-
"""Render the shared board to two theme-matched SVGs."""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

CELL, PAD_X, TOP, BOT = 34, 40, 86, 52

THEMES = {
    "dark":  dict(fg="#e6edf3", muted="#9198a1", grid="#21262d", rule="#30363d",
                  body="#3fb950", head="#56d364", food="#f0883e", dead="#f85149",
                  panel="#161b22"),
    "light": dict(fg="#1f2328", muted="#59636e", grid="#eaeef2", rule="#d1d9e0",
                  body="#2da44e", head="#1a7f37", food="#bc4c00", dead="#cf222e",
                  panel="#f6f8fa"),
}


def render(st, theme):
    c = THEMES[theme]
    gw, gh = st["w"] * CELL, st["h"] * CELL
    W = gw + PAD_X * 2
    H = TOP + gh + BOT
    alive = st["alive"]
    s = []
    a = s.append

    a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
      'height="%d" role="img" aria-label="A communal snake game board, %d by %d. '
      'Current score %d, high score %d, %d moves played.">'
      % (W, H, W, H, st["w"], st["h"], st["score"], st["high_score"], st["moves"]))

    # header
    a('<text x="%d" y="40" font-family="%s" font-size="25" font-weight="700" '
      'fill="%s">one snake, everybody\'s</text>' % (PAD_X, SANS, c["fg"]))
    a('<text x="%d" y="66" font-family="%s" font-size="13.5" fill="%s">'
      'anyone with a GitHub account can move it. there is no second snake.</text>'
      % (PAD_X, SANS, c["muted"]))

    dot = "  ·  "
    stat = dot.join([
        "score %d" % st["score"],
        "high %d by %s" % (st["high_score"], st["high_score_by"] or "nobody yet"),
        "%d moves" % st["moves"],
        "game #%d" % st["games"],
    ])
    a('<text x="%d" y="40" text-anchor="end" font-family="%s" font-size="13" '
      'fill="%s">%s</text>' % (W - PAD_X, MONO, c["muted"], _esc(stat)))

    # board panel + grid dots
    a('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s"/>'
      % (PAD_X - 8, TOP - 8, gw + 16, gh + 16, c["panel"]))
    for x in range(st["w"]):
        for y in range(st["h"]):
            cx = PAD_X + x * CELL + CELL / 2.0
            cy = TOP + y * CELL + CELL / 2.0
            a('<circle cx="%.1f" cy="%.1f" r="1.5" fill="%s"/>' % (cx, cy, c["grid"]))

    # food
    if st["food"] and alive:
        fx = PAD_X + st["food"][0] * CELL + CELL / 2.0
        fy = TOP + st["food"][1] * CELL + CELL / 2.0
        a('<circle cx="%.1f" cy="%.1f" r="8" fill="%s">'
          '<animate attributeName="r" values="7;10.5;7" dur="1.8s" '
          'repeatCount="indefinite"/>'
          '<animate attributeName="opacity" values="1;0.65;1" dur="1.8s" '
          'repeatCount="indefinite"/></circle>' % (fx, fy, c["food"]))

    # snake
    body_col = c["body"] if alive else c["dead"]
    head_col = c["head"] if alive else c["dead"]
    n = len(st["snake"])
    for i, (x, y) in enumerate(st["snake"]):
        px = PAD_X + x * CELL + 3
        py = TOP + y * CELL + 3
        size = CELL - 6
        if i == 0:
            a('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="8" fill="%s"/>'
              % (px, py, size, size, head_col))
            ex = _eyes(st["dir"])
            for ox, oy in ex:
                a('<circle cx="%.1f" cy="%.1f" r="2.4" fill="%s"/>'
                  % (px + size * ox, py + size * oy, c["panel"]))
        else:
            op = 0.95 - (i / float(max(n, 2))) * 0.45
            a('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="6" fill="%s" '
              'opacity="%.2f"/>' % (px, py, size, size, body_col, op))

    # footer
    if alive:
        msg = "the snake is alive. click an arrow under this board to move it one square."
        col = c["muted"]
    else:
        d = st.get("last_death") or {}
        msg = ("game over. @%s walked it %s at score %d. the next click starts game #%d."
               % (d.get("user", "someone"), d.get("how", "into something"),
                  d.get("score", 0), st["games"] + 1))
        col = c["dead"]
    a('<text x="%d" y="%d" font-family="%s" font-size="13" fill="%s">%s</text>'
      % (PAD_X, TOP + gh + 30, MONO, col, _esc(msg)))

    a('</svg>')
    return "\n".join(s)


def _eyes(d):
    m = {"right": [(0.72, 0.3), (0.72, 0.7)], "left": [(0.28, 0.3), (0.28, 0.7)],
         "up": [(0.3, 0.28), (0.7, 0.28)], "down": [(0.3, 0.72), (0.7, 0.72)]}
    return m.get(d, m["right"])


def _esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def write_all(st):
    os.makedirs(ASSETS, exist_ok=True)
    out = []
    for t in THEMES:
        p = os.path.join(ASSETS, "snake-%s.svg" % t)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(render(st, t))
        out.append(p)
    return out
