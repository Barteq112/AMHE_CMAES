"""Obsługa ograniczeń dla problemów COCO (bbob-constrained)."""

import numpy as np


def _lb_ub(problem):
    return np.asarray(problem.lower_bounds), np.asarray(problem.upper_bounds)


def is_feasible(problem, x):
    """
    COCO: constraint(x) <= 0 oznacza spełnienie + trzeba być w regionie [lb, ub].
    """
    x = np.asarray(x, dtype=float)
    lb, ub = _lb_ub(problem)
    if np.any(x < lb) or np.any(x > ub):
        return False
    c = np.atleast_1d(problem.constraint(x))
    return bool(np.all(c <= 0))


def violation(problem, x):
    """Kwadratowa kara za naruszenie boxa i constraintów (c > 0)."""
    x = np.asarray(x, dtype=float)
    lb, ub = _lb_ub(problem)
    v = np.sum(np.maximum(lb - x, 0) ** 2 + np.maximum(x - ub, 0) ** 2)
    c = np.atleast_1d(problem.constraint(x))
    v += np.sum(np.maximum(c, 0.0) ** 2)
    return float(v)


def clip_to_box(x, lb, ub):
    return np.minimum(np.maximum(x, lb), ub)


def project_toward_mean(x, mean, problem, steps=80):
    """Rzut w stronę średniej populacji — pierwszy dopuszczalny punkt na odcinku."""
    x = np.asarray(x, dtype=float)
    mean = np.asarray(mean, dtype=float)
    if is_feasible(problem, x):
        return x.copy()

    d = mean - x
    if np.linalg.norm(d) < 1e-14:
        lb, ub = _lb_ub(problem)
        return clip_to_box(x, lb, ub)

    t_ok = 1.0
    for i in range(steps + 1):
        t = i / steps
        p = x + t * d
        if is_feasible(problem, p):
            t_ok = t
            break
    return x + t_ok * d


def random_feasible(problem, rng, tries=3000):
    lb, ub = _lb_ub(problem)
    for _ in range(tries):
        x = rng.uniform(lb, ub)
        if is_feasible(problem, x):
            return x
    return clip_to_box(rng.uniform(lb, ub), lb, ub)


def fix_candidate(x, mean, problem, method, rng):
    if method == "none":
        return np.asarray(x, dtype=float)
    if method == "project":
        return project_toward_mean(x, mean, problem)
    if method == "reject":
        if is_feasible(problem, x):
            return np.asarray(x, dtype=float)
        return random_feasible(problem, rng)
    if method == "penalty":
        return np.asarray(x, dtype=float)
    raise ValueError(f"nieznana metoda: {method}")
