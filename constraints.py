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


def project_toward_mean(x, mean, problem, max_iters=10):
    """Rzut w stronę średniej populacji z użyciem wyszukiwania binarnego."""
    x = np.asarray(x, dtype=float)
    mean = np.asarray(mean, dtype=float)
    if is_feasible(problem, x):
        return x.copy()

    d = mean - x
    if np.linalg.norm(d) < 1e-14:
        lb, ub = _lb_ub(problem)
        return clip_to_box(x, lb, ub)

    if not is_feasible(problem, mean):
        lb, ub = _lb_ub(problem)
        return clip_to_box(mean, lb, ub)

    t_inf = 0.0
    t_feas = 1.0

    for _ in range(max_iters):
        t_mid = (t_inf + t_feas) / 2.0
        p = x + t_mid * d

        if is_feasible(problem, p):
            t_feas = t_mid
        else:
            t_inf = t_mid

    return x + t_feas * d


def fix_candidate(x, problem, method, es, tries=100):
    if method == "project":
        return project_toward_mean(x, np.array(es.mean), problem)

    if method == "reject":
        if is_feasible(problem, x):
            return np.asarray(x, dtype=float)

        for _ in range(tries):
            new_x = np.asarray(es.ask(1)[0], dtype=float)
            if is_feasible(problem, new_x):
                return new_x

        # fallback
        lb, ub = _lb_ub(problem)
        return clip_to_box(np.asarray(x, dtype=float), lb, ub)

    if method == "penalty":
        return np.asarray(x, dtype=float)

    raise ValueError(f"nieznana metoda: {method}")
