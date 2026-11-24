"""3-апта: CSP. A,B,C,D айнымалылары (0-9 цифрлар), шектеулер — терминалдардағы шарттар.
Шешу тәсілі: кері іздеу (backtracking), шектеуді ертерек тексеру арқылы."""
import random
from dataclasses import dataclass
from typing import Callable, Tuple

NAMES = "ABCD"


@dataclass
class Clue:
    vars: Tuple[int, ...]            # шарт қай айнымалыларға қатысты
    text: str                        # ойыншыға көрсетілетін мәтін
    test: Callable[[list], bool]     # код осы шартты қанағаттандыра ма


def make_clues(s):
    """Құпия код s үшін ақиқат болатын барлық шарттар."""
    out = []
    for i in range(4):
        out.append(Clue((i,), f"{NAMES[i]} — {'тақ' if s[i] % 2 else 'жұп'} сан",
                        lambda d, i=i, p=s[i] % 2: d[i] % 2 == p))  # i=i: циклдегі мәнді бекітеді
        for j in range(4):
            if j == i:
                continue
            if s[i] > s[j]:
                out.append(Clue((i, j), f"{NAMES[i]} > {NAMES[j]}", lambda d, i=i, j=j: d[i] > d[j]))
            if i < j:
                t = s[i] + s[j]
                out.append(Clue((i, j), f"{NAMES[i]} + {NAMES[j]} = {t}", lambda d, i=i, j=j, t=t: d[i] + d[j] == t))
                eq = s[i] == s[j]
                out.append(Clue((i, j), f"{NAMES[i]} {'=' if eq else '≠'} {NAMES[j]}",
                                lambda d, i=i, j=j, eq=eq: (d[i] == d[j]) == eq))
    tot = sum(s)
    out.append(Clue((0, 1, 2, 3), f"A+B+C+D = {tot}", lambda d, t=tot: sum(d) == t))
    return out


def solve(clues):
    """Шарттарға сай барлық кодтар (backtracking)."""
    sols, d = [], [0] * 4

    def bt(i):
        if i == 4:
            sols.append(d[:])
            return
        for x in range(10):
            d[i] = x
            # тек барлық айнымалысы қойылып қойған шарттарды тексереміз
            if all(max(c.vars) > i or c.test(d) for c in clues):
                bt(i + 1)

    bt(0)
    return sols


def generate_puzzle(seed=None, pool_size=12, max_clues=8):
    """Кодты ең көп қысқартатын шартты ашкөздікпен қосамыз, шешім біреу болғанша."""
    rnd = random.Random(seed)
    while True:
        secret = [rnd.randint(0, 9) for _ in range(4)]
        pool = make_clues(secret)
        rnd.shuffle(pool)
        chosen, n = [], 10000
        while n > 1 and len(chosen) < max_clues:
            best, bn = None, n
            for c in pool[:pool_size]:
                m = len(solve(chosen + [c]))
                if m < bn:
                    best, bn = c, m
            if best is None:
                break
            chosen.append(best)
            pool.remove(best)
            n = bn
        if n == 1:
            return secret, chosen
