"""7-апта: Байес сүзгісі / HMM (forward алгоритмі). Жасырын күй — ойыншының ұяшығы.
Бақылаулар — күзетшінің көруі және аяқ дыбысы."""
import math
from .maze import neighbors


class BeliefFilter:
    def __init__(self, grid, stay=0.35):
        self.g, self.stay = grid, stay
        cells = [(x, y) for y, row in enumerate(grid) for x, v in enumerate(row) if v == 0]
        self.b = {c: 1 / len(cells) for c in cells}  # басында барлық ұяшық бірдей ықтимал

    def predict(self):
        """Қозғалыс моделі: орнында қалады (stay) немесе кездейсоқ көршіге өтеді."""
        nb_ = {}
        for c, p in self.b.items():
            ns = neighbors(self.g, *c)
            nb_[c] = nb_.get(c, 0) + p * self.stay
            for n in ns:
                nb_[n] = nb_.get(n, 0) + p * (1 - self.stay) / len(ns)
        self.b = nb_

    def _norm(self):
        """Қосындыны 1-ге келтіреді."""
        s = sum(self.b.values())
        if s < 1e-12:  # барлық гипотеза жойылса — басынан бастаймыз
            n = len(self.b)
            self.b = {c: 1 / n for c in self.b}
        else:
            self.b = {c: p / s for c, p in self.b.items()}

    def observe_seen(self, pos):
        """Күзетші ойыншыны көрді: сенім бір ұяшыққа жиналады."""
        self.b = {c: (1.0 if c == pos else 0.0) for c in self.b}

    def observe_not_visible(self, visible, factor=0.01):
        """Теріс дәлел: көрінетін ұяшықтарда ойыншы жоқ."""
        for c in visible:
            if c in self.b:
                self.b[c] *= factor
        self._norm()

    def observe_noise(self, guard, observed, sigma=2.5):
        """Дыбыс қашықтықтың шулы бағасын береді (Гаусс ықтималдығы)."""
        for c in self.b:
            d = math.hypot(c[0] - guard[0], c[1] - guard[1])
            self.b[c] *= math.exp(-((d - observed) ** 2) / (2 * sigma ** 2)) + 0.02
        self._norm()

    def most_likely(self):
        """Ең ықтимал ұяшық (argmax) — күзетші осыған барады."""
        return max(self.b, key=self.b.get)

    def entropy(self):
        """Белгісіздік: 0 бит — нақты біледі, ~8 бит — ештеңе білмейді."""
        return -sum(p * math.log2(p) for p in self.b.values() if p > 0)
