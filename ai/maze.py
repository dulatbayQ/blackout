"""Лабиринт жасау (DFS) және BFS. 1 = қабырға, 0 = жол."""
import random
from collections import deque


def is_open(g, x, y):
    """(x, y) ұяшығы тор ішінде және жол ма?"""
    return 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] == 0


def neighbors(g, x, y):
    """4 бағыттағы бос көршілер."""
    return [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if is_open(g, x + dx, y + dy)]


def generate(n=21, seed=None, loops=30):
    if n < 7 or n % 2 == 0:
        raise ValueError("n тақ сан және >= 7 болуы керек")
    rnd = random.Random(seed)  # seed бірдей болса, лабиринт те бірдей
    g = [[1] * n for _ in range(n)]
    g[1][1] = 0
    stack = [(1, 1)]
    while stack:
        x, y = stack[-1]
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        rnd.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 < nx < n - 1 and 0 < ny < n - 1 and g[ny][nx]:
                g[y + dy // 2][x + dx // 2] = 0  # екі бөлменің арасындағы қабырғаны бұзамыз
                g[ny][nx] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()  # бару керек жер жоқ — артқа қайтамыз
    for _ in range(loops):  # циклдар: лабиринт «мінсіз» болмай, айналма жолдар пайда болады
        x, y = rnd.randint(1, n - 2), rnd.randint(1, n - 2)
        h = is_open(g, x - 1, y) and is_open(g, x + 1, y)
        v = is_open(g, x, y - 1) and is_open(g, x, y + 1)
        if g[y][x] and h != v:
            g[y][x] = 0
    return g


def bfs_dist(g, start):
    """start-тан барлық ұяшыққа дейінгі ең қысқа қашықтық (қадам саны)."""
    dist = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        for nb in neighbors(g, *cur):
            if nb not in dist:
                dist[nb] = dist[cur] + 1
                q.append(nb)
    return dist
