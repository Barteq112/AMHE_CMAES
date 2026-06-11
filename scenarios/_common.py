import os

from coco_benchmark import make_observer, make_suite, problem_label
from optimizer import run_cmaes
from save_results import save_comparison_table, save_run

METHODS = ["project", "reject", "penalty"]


def execute(key, name, suite_options, budget_mult, coco_subdir, seed=42, dimensions=None):
    print(f"\n{'=' * 60}")
    print(f"SCENARIUSZ {key}: {name}")
    print(f"{'=' * 60}\n")

    coco_base = os.path.join("results_coco", coco_subdir)
    results_dir = os.path.join("results", f"scenario{key}")
    os.makedirs(results_dir, exist_ok=True)

    comparison = []
    dim_list = dimensions if dimensions else [None]

    for dim in dim_list:
        if dim is not None:
            opts = f"dimensions: {dim} {suite_options}"
            print(f"\n--- wymiar D={dim} ---\n")
        else:
            opts = suite_options

        suite = make_suite(opts)

        observers = {m: make_observer(os.path.join(coco_base, m)) for m in METHODS}
        n_probs = 0

        for problem in suite:
            n_probs += 1
            pid = problem.id
            print(f"\n[{n_probs}] {problem.name}")

            for method in METHODS:
                p = None
                try:
                    p = suite.get_problem(pid, observers[method])
                    max_evals = p.dimension * budget_mult
                    print(f"  {method} (budget={max_evals}) ...", flush=True)

                    res = run_cmaes(p, method=method, max_evals=max_evals, seed=seed)
                    tag = problem_label(p).replace(" ", "_")
                    save_run(res, f"s{key}_{tag}", p.dimension, out_dir=results_dir)

                    comparison.append({
                        "scenario": key,
                        "problem_id": pid,
                        "problem": problem_label(p),
                        "dim": p.dimension,
                        "method": method,
                        "best_f": res["best_f"],
                        "evals": res["evals"],
                        "budget": max_evals,
                        "target_hit": res["target_hit"],
                    })
                    print(f"       best_f={res['best_f']:.6g}  target_hit={res['target_hit']}")
                except Exception as e:
                    print(f"       BŁĄD: {e}")
                finally:
                    if p is not None:
                        try:
                            p.free()
                        except Exception:
                            pass

        print(f"\n  (D={dim}) problemów w suite: {n_probs}")

    table_path = save_comparison_table(comparison, out_dir=results_dir)
    print(f"\nTabela: {table_path}")
    print(f"Logi COCO: exdata/{coco_base.replace(os.sep, '/')}/<metoda>/")
    return comparison
