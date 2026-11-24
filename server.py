"""Flask сервері: ойынды береді + демонстрацияға арналған шағын API."""
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from ai import maze
from ai.astar import astar
from ai.csp import generate_puzzle, solve

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app = Flask(__name__, static_folder=str(STATIC_DIR))


@app.get("/")
def index():
    """Браузер http://127.0.0.1:5000 ашқанда ойын файлын береді."""
    return send_from_directory(str(STATIC_DIR), "blackout.html")


@app.get("/api/maze")
def api_maze():
    """Лабиринт + A* жолы. Мысалы: /api/maze?n=15&seed=1"""
    try:
        n = int(request.args.get("n", 21))
        seed = request.args.get("seed", type=int)
        g = maze.generate(n, seed)
    except ValueError as e:  # қате енгізуді өңдеу
        return jsonify(error=str(e)), 400
    far = max(maze.bfs_dist(g, (1, 1)).items(), key=lambda kv: kv[1])[0]
    path, expanded = astar(g, (1, 1), far)
    return jsonify(n=n, grid=g, goal=far, path=path, expanded=expanded)


@app.get("/api/puzzle")
def api_puzzle():
    """CSP жұмбағы. Мысалы: /api/puzzle?seed=3 (secret тек демонстрация үшін)"""
    seed = request.args.get("seed", type=int)
    secret, clues = generate_puzzle(seed)
    return jsonify(clues=[c.text for c in clues], solutions=len(solve(clues)), secret=secret)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)