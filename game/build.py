# -*- coding: utf-8 -*-
"""Regenerate README.md from README.template.md plus the live board state."""
import os, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine, render

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "nilaymastaadmi/nilaymastaadmi"
RAW = "https://raw.githubusercontent.com/%s/main/assets" % REPO
NEW_ISSUE = "https://github.com/%s/issues/new" % REPO
START, END = "<!--SNAKE:START-->", "<!--SNAKE:END-->"


def move_link(d):
    body = ("Submit this issue and the bot moves the shared snake one square, then "
            "closes the issue. Nothing else happens. You can edit the title to "
            "up/down/left/right before submitting.")
    return "%s?title=snake:%s&body=%s" % (
        NEW_ISSUE, d, body.replace(" ", "+").replace(",", "%2C"))


def block(st):
    # ?v= busts GitHub's image proxy cache, otherwise the board looks frozen.
    v = st["moves"]
    L = []
    L.append("<picture>")
    L.append('  <source media="(prefers-color-scheme: dark)" '
             'srcset="%s/snake-dark.svg?v=%d">' % (RAW, v))
    L.append('  <source media="(prefers-color-scheme: light)" '
             'srcset="%s/snake-light.svg?v=%d">' % (RAW, v))
    L.append('  <img alt="A shared snake game board, %d by %d. Score %d, high score '
             '%d, %d moves played." src="%s/snake-light.svg?v=%d" width="100%%">'
             % (st["w"], st["h"], st["score"], st["high_score"], st["moves"], RAW, v))
    L.append("</picture>")
    L.append("")
    L.append("<div align=\"center\">")
    L.append("")
    L.append("|  |  |  |")
    L.append("|:--:|:--:|:--:|")
    L.append("|  | [**&uarr; up**](%s) |  |" % move_link("up"))
    L.append("| [**&larr; left**](%s) | *one click, one square* | [**right &rarr;**](%s) |"
             % (move_link("left"), move_link("right")))
    L.append("|  | [**&darr; down**](%s) |  |" % move_link("down"))
    L.append("")
    L.append("</div>")
    L.append("")

    if st.get("recent"):
        who = ", ".join("[@%s](https://github.com/%s) %s" % (r["user"], r["user"], r["move"])
                        for r in st["recent"])
        L.append("**Last moves:** %s" % who)
        L.append("")
    if st.get("hall"):
        L.append("<details><summary><b>Hall of fame, and of shame</b></summary>")
        L.append("")
        L.append("| Score | Ended by | How | When |")
        L.append("|---:|---|---|---|")
        for h in st["hall"]:
            L.append("| %d | [@%s](https://github.com/%s) | %s | %s |"
                     % (h["score"], h["user"], h["user"], h["how"], h["date"]))
        L.append("")
        L.append("</details>")
        L.append("")
    return "\n".join(L)


def main():
    st = engine.load()
    render.write_all(st)
    tpl = io.open(os.path.join(ROOT, "README.template.md"), encoding="utf-8").read()
    a = tpl.index(START) + len(START)
    b = tpl.index(END)
    out = tpl[:a] + "\n" + block(st) + tpl[b:]
    io.open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n").write(out)
    print("README.md rebuilt at %d moves, score %d" % (st["moves"], st["score"]))


if __name__ == "__main__":
    main()
