# -*- coding: utf-8 -*-
"""Play a full game of snake with a safe-greedy AI and record every frame."""
from collections import deque

W, H = 21, 11
DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def neighbours(p):
    for dx, dy in DIRS:
        q = (p[0] + dx, p[1] + dy)
        if 0 <= q[0] < W and 0 <= q[1] < H:
            yield q


def bfs(start, goal, blocked):
    """Shortest path start -> goal avoiding blocked. Returns list of cells or None."""
    if start == goal:
        return [start]
    prev = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        for nxt in neighbours(cur):
            if nxt in prev or (nxt in blocked and nxt != goal):
                continue
            prev[nxt] = cur
            if nxt == goal:
                path = [nxt]
                while prev[path[-1]] is not None:
                    path.append(prev[path[-1]])
                return list(reversed(path))
            q.append(nxt)
    return None


def free_space(start, blocked):
    seen = {start}
    q = deque([start])
    while q:
        cur = q.popleft()
        for nxt in neighbours(cur):
            if nxt not in seen and nxt not in blocked:
                seen.add(nxt)
                q.append(nxt)
    return len(seen)


def simulate(snake, path):
    """Advance a copy of the snake along path (not eating) and return the body."""
    body = list(snake)
    for cell in path[1:]:
        body.insert(0, cell)
        body.pop()
    return body


def choose(snake, food):
    head = snake[0]
    body = set(snake)

    # Prefer the shortest route to the food, but only if, after eating it, the
    # head can still reach its own tail. Otherwise the snake seals itself in.
    path = bfs(head, food, body - {snake[-1]})
    if path and len(path) > 1:
        after = simulate(snake, path)
        after.insert(0, food)          # eating grows it by one
        if bfs(food, after[-1], set(after) - {after[-1]}):
            return path[1]

    # No safe route to food: chase the tail to buy time.
    tail_path = bfs(head, snake[-1], set(snake) - {snake[-1]})
    if tail_path and len(tail_path) > 1:
        return tail_path[1]

    # Last resort: whichever legal square leaves the most room.
    best, best_room = None, -1
    for nxt in neighbours(head):
        if nxt in body:
            continue
        room = free_space(nxt, body - {snake[-1]})
        if room > best_room:
            best, best_room = nxt, room
    return best


def food_spots(snake_len):
    """Deterministic pseudo-random food, so the animation is reproducible."""
    seed = 20260902
    while True:
        seed = (1103515245 * seed + 12345) % (2 ** 31)
        yield seed


def run(max_moves=240):
    mid = H // 2
    snake = [(6, mid), (5, mid), (4, mid)]
    gen = food_spots(len(snake))
    def new_food(body):
        while True:
            s = next(gen)
            cell = (s % W, (s // W) % H)
            if cell not in body:
                return cell
    food = new_food(set(snake))
    frames = [{"snake": list(snake), "food": food, "score": 0}]
    score = 0
    for _ in range(max_moves):
        nxt = choose(snake, food)
        if nxt is None or nxt in set(snake[:-1]):
            break
        snake.insert(0, nxt)
        if nxt == food:
            score += 1
            food = new_food(set(snake))
        else:
            snake.pop()
        frames.append({"snake": list(snake), "food": food, "score": score})
    return frames


if __name__ == "__main__":
    f = run()
    print("frames: %d   final score: %d   final length: %d"
          % (len(f), f[-1]["score"], len(f[-1]["snake"])))
