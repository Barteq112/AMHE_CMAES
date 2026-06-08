"""
Pomiar szybkości metod obsługi ograniczeń — scenariusz 1, jeden seed.

Uruchomienie:
  python benchmark_speed.py
  python benchmark_speed.py --seed 42 --out results/report
"""

import argparse
import csv
from pathlib import Path

import numpy as np

from coco_benchmark import make_suite, problem_label
from optimizer import run_cmaes

METHODS = ["project", "reject", "penalty"]
METHOD_LABELS = {
    "project": "rzut",
    "reject": "odrzucenie",
    "penalty": "kara",
}
SUITE_OPTIONS = "dimensions: 5 function_indices: 1-54 instance_indices: 1-3"
BUDGET_MULT = 100


def run_benchmark(seed: int):
    suite = make_suite(SUITE_OPTIONS)
    rows = []

    for problem in suite:
        pid = problem.id
        label = problem_label(problem).replace(" ", "_")

        for method in METHODS:
            p = None
            try:
                p = suite.get_problem(pid)
                max_evals = p.dimension * BUDGET_MULT
                res = run_cmaes(p, method=method, max_evals=max_evals, seed=seed)
                rows.append({
                    "problem_id": pid,
                    "problem": label,
                    "method": method,
                    "seed": seed,
                    "evals": res["evals"],
                    "wall_time_s": res["wall_time_s"],
                    "repair_time_s": res["repair_time_s"],
                })
            finally:
                if p is not None:
                    try:
                        p.free()
                    except Exception:
                        pass

    return rows


def aggregate(rows):
    summary = []
    for method in METHODS:
        sub = [r for r in rows if r["method"] == method]
        if not sub:
            continue
        wall = np.array([r["wall_time_s"] for r in sub])
        repair = np.array([r["repair_time_s"] for r in sub])
        summary.append({
            "method": method,
            "label": METHOD_LABELS[method],
            "problems": len(sub),
            "total_wall_s": wall.sum(),
            "mean_wall_s": wall.mean(),
            "median_wall_s": np.median(wall),
            "total_repair_s": repair.sum(),
            "repair_share_pct": 100.0 * repair.sum() / max(wall.sum(), 1e-12),
        })
    return summary


def save_detail(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["problem_id", "problem", "method", "seed", "evals", "wall_time_s", "repair_time_s"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def save_summary(summary, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "method", "label", "problems", "total_wall_s", "mean_wall_s", "median_wall_s",
        "total_repair_s", "repair_share_pct",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(summary)


def print_table(summary, seed):
    print(f"\nScenariusz 1 — szybkość metod (seed={seed}, D=5, budżet=100*D)\n")
    header = (
        f"{'Metoda':<12} {'Łącznie [s]':>12} {'Śr./problem [s]':>16} "
        f"{'Mediana [s]':>12} {'Naprawa [%]':>12}"
    )
    print(header)
    print("-" * len(header))
    for row in summary:
        print(
            f"{row['label']:<12} "
            f"{row['total_wall_s']:12.1f} "
            f"{row['mean_wall_s']:16.3f} "
            f"{row['median_wall_s']:12.3f} "
            f"{row['repair_share_pct']:12.1f}"
        )
    print()


def main():
    parser = argparse.ArgumentParser(description="Benchmark szybkości — scenariusz 1")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="results/report", help="folder na CSV")
    args = parser.parse_args()

    print(f"Uruchamiam scenariusz 1 (seed={args.seed}) — może potrwać kilka minut...")
    rows = run_benchmark(args.seed)
    summary = aggregate(rows)

    out = Path(args.out)
    detail_path = out / f"scenario1_speed_seed{args.seed}_detail.csv"
    summary_path = out / f"scenario1_speed_seed{args.seed}.csv"
    save_detail(rows, detail_path)
    save_summary(summary, summary_path)

    print_table(summary, args.seed)
    print(f"Zapisano: {summary_path.resolve()}")
    print(f"         {detail_path.resolve()}")


if __name__ == "__main__":
    main()
