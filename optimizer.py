"""CMA-ES (biblioteka cma) na problemach bbob-constrained."""

import time

import numpy as np
import cma

from constraints import fix_candidate, violation, is_feasible


def eval_fitness(x, problem, method, penalty_weight=1e4):
    val = float(problem(x))
    if method == "penalty" and not is_feasible(problem, x):
        val += penalty_weight * violation(problem, x)
    return val


def run_cmaes(problem, method="project", max_evals=2000, seed=0, sigma_scale=0.2):
    """
    problem — obiekt cocoex z suite bbob-constrained
    method: project | reject | penalty
    """
    x0 = np.array(problem.initial_solution, dtype=float)
    lb = np.array(problem.lower_bounds, dtype=float)
    ub = np.array(problem.upper_bounds, dtype=float)
    sigma = sigma_scale * float(np.mean(ub - lb))

    opts = {
        "maxfevals": max_evals,
        "verb_disp": 0,
        "verb_log": 0,
        "seed": seed,
    }
    es = cma.CMAEvolutionStrategy(x0.tolist(), sigma, opts)

    history = []
    evals = 0
    repair_time_s = 0.0
    t_start = time.perf_counter()

    while not es.stop() and evals < max_evals:
        solutions = es.ask()
        fitnesses = []
        fixed = []

        for sol in solutions:
            x = np.array(sol, dtype=float)
            t_repair = time.perf_counter()
            x = fix_candidate(x, problem, method, es)
            repair_time_s += time.perf_counter() - t_repair
            fixed.append(x.tolist())
            fitnesses.append(eval_fitness(x, problem, method))
            evals += 1

        es.tell(fixed, fitnesses)

        history.append((evals, float(es.result.fbest), float(np.mean(fitnesses))))

    best_x = np.array(es.result.xfavorite)
    if method in ("project", "reject"):
        t_repair = time.perf_counter()
        best_x = fix_candidate(best_x, problem, method, es)
        repair_time_s += time.perf_counter() - t_repair

    wall_time_s = time.perf_counter() - t_start

    return {
        "method": method,
        "best_f": float(es.result.fbest),
        "best_x": best_x.tolist(),
        "evals": evals,
        "history": history,
        "problem_id": problem.id,
        "problem_name": problem.name,
        "dimension": problem.dimension,
        "target_hit": bool(problem.final_target_hit),
        "wall_time_s": wall_time_s,
        "repair_time_s": repair_time_s,
    }
