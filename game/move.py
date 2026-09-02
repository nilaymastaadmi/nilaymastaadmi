# -*- coding: utf-8 -*-
"""Apply one move from an issue. Title and actor arrive via env, never via shell."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine, build

VALID = ("up", "down", "left", "right")

title = os.environ.get("ISSUE_TITLE", "")
actor = os.environ.get("ISSUE_ACTOR", "anon")

raw = title.split(":", 1)[1] if ":" in title else ""
move = raw.strip().lower()
# Whitelist. Anything else is discarded rather than interpreted.
if move not in VALID:
    move = ""

st = engine.load()
was_over = not st["alive"]
st, outcome = engine.step(st, move, actor)
engine.save(st)
build.main()

if outcome == "ignored":
    msg = ("That title did not contain a direction. Use `snake:up`, `snake:down`, "
           "`snake:left` or `snake:right`. Nothing was changed.")
elif outcome == "reversed":
    msg = ("The snake will not turn back into its own neck, so that move was skipped "
           "rather than counted as a death. Try a different direction.")
elif outcome == "died":
    d = st["last_death"]
    msg = ("Well. The snake went %s at score %d, and you are now in the hall of fame "
           "for it. The board resets on the next move." % (d["how"], d["score"]))
elif outcome == "ate":
    msg = ("Fed it. Score is %d and the snake is %d long. High score is %d."
           % (st["score"], len(st["snake"]), st["high_score"]))
else:
    started = " You started game #%d." % st["games"] if was_over else ""
    msg = ("Moved %s.%s Score %d, %d moves so far."
           % (move, started, st["score"], st["moves"]))

with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
    f.write("comment<<EOFMSG\n%s\nEOFMSG\n" % msg)
    f.write("outcome=%s\n" % outcome)
print(msg)
