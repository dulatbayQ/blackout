"""Үш алгоритмнің консольдағы демонстрациясы (браузер де, сервер де керек емес)."""
import random
from ai import maze
from ai.astar import astar
from ai.csp import generate_puzzle, solve
from ai.hmm import BeliefFilter

print("=== 2-апта: A* ===")
g = maze.generate(21, seed=7)
far = max(maze.bfs_dist(g, (1, 1)).items(), key=lambda kv: kv[1])[0]
path, expanded = astar(g, (1, 1), far)
print(f"(1,1) -> {far}: жол ұзындығы {len(path) - 1}, ашылған түйін {expanded}")

print("\n=== 3-апта: CSP (backtracking) ===")
secret, clues = generate_puzzle(seed=3)
for k in range(len(clues) + 1):
    print(f"шарт саны: {k}, үміткер: {len(solve(clues[:k]))}" + (f"  (+ «{clues[k-1].text}»)" if k else ""))
print("құпия код:", secret)

print("\n=== 7-апта: Байес сүзгісі / HMM ===")
rnd = random.Random(1)
f = BeliefFilter(g)
guard, player = (1, 1), far
print(f"басында: энтропия {f.entropy():.2f} бит")
for step in range(1, 6):
    f.predict()
    d = max(0, ((guard[0]-player[0])**2 + (guard[1]-player[1])**2) ** .5 + rnd.gauss(0, 2))
    f.observe_noise(guard, d)
    print(f"{step}-қадам: ең ықтимал ұяшық {f.most_likely()}, энтропия {f.entropy():.2f} бит")
