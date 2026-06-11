import csv
import json
import os
from datetime import datetime


def ensure_results_dir(base="results"):
    os.makedirs(base, exist_ok=True)
    return base


def save_run(result, problem_name, dim, out_dir="results"):
    out_dir = ensure_results_dir(out_dir)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag = f"{problem_name}_d{dim}_{result['method']}_{ts}"

    # historia do csv
    csv_path = os.path.join(out_dir, f"{tag}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["evals", "best_f", "mean_f"])
        for row in result["history"]:
            w.writerow(row)

    # podsumowanie json
    summary = {
        "problem": problem_name,
        "dim": dim,
        "method": result["method"],
        "best_f": result["best_f"],
        "best_x": result["best_x"],
        "evals": result["evals"],
        "csv": csv_path,
    }
    json_path = os.path.join(out_dir, f"{tag}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return csv_path, json_path


def save_comparison_table(rows, out_dir="results"):
    """rows: lista dict z kolumnami problem, method, best_f, ..."""
    out_dir = ensure_results_dir(out_dir)
    path = os.path.join(out_dir, "porownanie.csv")
    if not rows:
        return path
    keys = rows[0].keys()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    return path
