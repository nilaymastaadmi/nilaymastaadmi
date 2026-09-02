"""Communal snake. One board, one snake, everyone shares it.

State lives in game/state.json. One issue = one move. No per-player state,
which is the whole joke: strangers cooperate or they do not.
"""
import json, os, random, datetime

W, H = 21, 11
DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}
HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state.json")


def new_game(keep=None):
    mid_y = H // 2
    st = {
        "w": W, "h": H,
        "snake": [[6, mid_y], [5, mid_y], [4, mid_y]],
        "dir": "right",
        "food": [W - 7, mid_y],
        "score": 0,
        "moves": 0,
        "alive": True,
        "games": 1,
        "high_score": 0,
        "high_score_by": None,
        "last_death": None,
        "recent": [],
        "hall": [],
    }
    if keep:
        for k in ("games", "high_score", "high_score_by", "hall"):
            st[k] = keep.get(k, st[k])
        st["games"] = keep.get("games", 0) + 1
    return st


def load():
    if not os.path.exists(STATE):
        return new_game()
    with open(STATE, encoding="utf-8") as f:
        return json.load(f)


def save(st):
    with open(STATE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(st, f, indent=1, sort_keys=True)
        f.write("\n")


def place_food(st, rng):
    free = [[x, y] for x in range(st["w"]) for y in range(st["h"])
            if [x, y] not in st["snake"]]
    return rng.choice(free) if free else None


def step(st, move, user):
    """Apply one move. Returns (state, outcome) where outcome is a short string."""
    move = move.lower().strip()
    if move not in DIRS:
        return st, "ignored"

    if not st["alive"]:
        st = new_game(keep=st)

    # A reversal into your own neck is a no-op, not a death. Otherwise a single
    # careless click ends a board that a dozen people built.
    if len(st["snake"]) > 1 and move == OPPOSITE[st["dir"]]:
        return st, "reversed"

    st["dir"] = move
    dx, dy = DIRS[move]
    hx, hy = st["snake"][0]
    head = [hx + dx, hy + dy]

    rng = random.Random("%s|%d|%d" % (user or "anon", st["moves"], st["score"]))
    st["moves"] += 1
    st["recent"] = ([{"user": user or "anon", "move": move}] + st["recent"])[:5]

    if not (0 <= head[0] < st["w"] and 0 <= head[1] < st["h"]):
        return _die(st, user, "into the wall"), "died"
    if head in st["snake"][:-1]:
        return _die(st, user, "into itself"), "died"

    st["snake"].insert(0, head)
    if head == st["food"]:
        st["score"] += 1
        st["food"] = place_food(st, rng)
        outcome = "ate"
    else:
        st["snake"].pop()
        outcome = "moved"

    if st["score"] > st["high_score"]:
        st["high_score"] = st["score"]
        st["high_score_by"] = user or "anon"
    return st, outcome


def _die(st, user, how):
    st["alive"] = False
    st["last_death"] = {
        "user": user or "anon",
        "how": how,
        "score": st["score"],
        "date": datetime.date.today().isoformat(),
    }
    st["hall"] = ([{"user": user or "anon", "score": st["score"], "how": how,
                    "date": datetime.date.today().isoformat()}] + st["hall"])[:5]
    return st
