"""Алгоритмдер тесттері. Іске қосу: python -m pytest -q"""
import math
from ai import maze
from ai.astar import astar
from ai.csp import generate_puzzle, solve, make_clues
from ai.hmm import BeliefFilter


def test_astar_equals_bfs_length():
    """A* жолының ұзындығы BFS-тің ең қысқа қашықтығына тең."""
    g = maze.generate(21, seed=1)
    dist = maze.bfs_dist(g, (1, 1))
    for goal in list(dist)[::17]:
        path, _ = astar(g, (1, 1), goal)
        assert len(path) - 1 == dist[goal]


def test_astar_expands_not_more_than_open_cells():
    """Жол дұрыс басталып-аяқталады, ашылған түйін саны жол санынан аспайды."""
    g = maze.generate(21, seed=2)
    far = max(maze.bfs_dist(g, (1, 1)).items(), key=lambda kv: kv[1])[0]
    path, expanded = astar(g, (1, 1), far)
    assert path[0] == (1, 1) and path[-1] == far and expanded <= sum(r.count(0) for r in g)


def test_astar_no_path_to_wall():
    """Мақсат қабырға болса, жол бос."""
    g = maze.generate(11, seed=3)
    path, _ = astar(g, (1, 1), (0, 0))
    assert path == []


def test_csp_puzzle_has_unique_correct_solution():
    """Шешім жалғыз және дәл құпия код."""
    for seed in range(5):
        secret, clues = generate_puzzle(seed)
        assert solve(clues) == [secret]


def test_csp_without_clues_has_10000_candidates():
    """Шартсыз 0000-9999 аралығында 10 000 үміткер."""
    assert len(solve([])) == 10000


def test_csp_all_clues_true_for_secret():
    """Генератор жалған шарт жасамайды."""
    s = [3, 7, 0, 4]
    assert all(c.test(s) for c in make_clues(s))


def test_belief_sums_to_one_after_steps():
    """Ықтималдықтар қосындысы әрқашан 1."""
    f = BeliefFilter(maze.generate(15, seed=4))
    f.predict(); f.observe_noise((1, 1), 5.0); f.predict()
    assert math.isclose(sum(f.b.values()), 1.0, rel_tol=1e-6)


def test_belief_collapses_when_player_seen():
    """Көрсе: сенім бір ұяшықта, энтропия 0."""
    f = BeliefFilter(maze.generate(15, seed=5))
    f.observe_seen((1, 1))
    assert f.most_likely() == (1, 1) and f.entropy() == 0


def test_negative_evidence_lowers_visible_cells():
    """Көрінетін ұяшықта ойыншы жоқ десек, оның ықтималдығы түседі."""
    f = BeliefFilter(maze.generate(15, seed=6))
    before = f.b[(1, 1)]
    f.observe_not_visible([(1, 1)])
    assert f.b[(1, 1)] < before
