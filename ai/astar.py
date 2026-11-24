"""2-апта: A* алгоритмі. Эвристика — манхэттен қашықтығы (торда ешқашан асыра бағаламайды)."""
import heapq
from .maze import neighbors


def astar(g, start, goal):
    """(жол, ашылған түйін саны) қайтарады. Мақсатқа жету мүмкін болмаса, жол бос."""
    h = lambda p: abs(p[0] - goal[0]) + abs(p[1] - goal[1])
    heap = [(h(start), 0, start)]          # (f, g, ұяшық); f = g + h
    came, best, closed, expanded = {}, {start: 0}, set(), 0
    while heap:
        _, gc, cur = heapq.heappop(heap)   # f ең кіші ұяшықты аламыз
        if cur in closed:
            continue
        closed.add(cur)
        expanded += 1
        if cur == goal:                    # жолды мақсаттан артқа қарай жинаймыз
            path = [cur]
            while cur in came:
                cur = came[cur]
                path.append(cur)
            return path[::-1], expanded
        for nb in neighbors(g, *cur):
            ng = gc + 1
            if ng < best.get(nb, 1e9):     # жақсырақ жол табылды
                best[nb], came[nb] = ng, cur
                heapq.heappush(heap, (ng + h(nb), ng, nb))
    return [], expanded
