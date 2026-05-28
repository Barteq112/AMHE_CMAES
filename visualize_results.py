"""
Podsumowanie i wykresy z folderów results/scenario*.

  python visualize_results.py --scenario 1
  python visualize_results.py --scenario 1 --out results/report_sc1
"""

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

METHODS = ["project", "reject", "penalty"]
METHOD_LABELS = {
    "project": "rzut",
    "reject": "odrzucenie",
    "penalty": "kara",
}
COLORS = {"project": "#2ecc71", "reject": "#e74c3c", "penalty": "#3498db"}


def keep_methods(rows):
    return [r for r in rows if r.get("method") in METHODS]


def load_porownanie(path: Path):
    if not path.is_file():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_from_json_runs(scenario_dir: Path):
    """Gdy brak porownanie.csv — zbierz z plików s*_*.json (najnowszy per problem+metoda)."""
    best = {}
    for p in scenario_dir.glob("s*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        method = data.get("method")
        if not method:
            m = re.search(r"_(project|reject|penalty)_", p.name)
            method = m.group(1) if m else None
        if method not in METHODS:
            continue

        pid = re.search(r"f(\d+)_i(\d+)_d(\d+)", p.name)
        func_id = int(pid.group(1)) if pid else 0
        inst = int(pid.group(2)) if pid else 0
        dim = int(pid.group(3)) if pid else data.get("dim", 0)

        problem_id = f"f{func_id:03d}_i{inst:02d}_d{dim:02d}"
        key = (problem_id, method)
        mtime = p.stat().st_mtime
        if key not in best or mtime > best[key][0]:
            best[key] = (mtime, {
                "problem_id": problem_id,
                "problem": f"f{func_id:03d} i{inst:02d} d{dim:02d}",
                "dim": dim,
                "method": method,
                "best_f": float(data["best_f"]),
                "evals": data.get("evals", ""),
                "target_hit": data.get("target_hit", False),
            })

    rows = [v[1] for v in best.values()]
    for r in rows:
        r["scenario"] = scenario_dir.name.replace("scenario", "")
    return keep_methods(rows)


def load_scenario(scenario_num: str, base: Path):
    sdir = base / f"scenario{scenario_num}"
    if not sdir.is_dir():
        return []
    rows = load_porownanie(sdir / "porownanie.csv")
    if not rows:
        rows = load_from_json_runs(sdir)
    else:
        for r in rows:
            r["scenario"] = scenario_num
        rows = keep_methods(rows)
    return rows


def add_ranks(rows):
    """Ranga 1 = najlepszy best_f w danej grupie (problem_id, dim)."""
    groups = defaultdict(list)
    for r in rows:
        key = (r.get("problem_id", r.get("problem", "")), str(r.get("dim", "")))
        groups[key].append(r)

    for group in groups.values():
        sorted_g = sorted(group, key=lambda x: float(x["best_f"]))
        for rank, row in enumerate(sorted_g, start=1):
            row["rank"] = rank
            row["won"] = rank == 1
    return rows


def plot_method_wins(rows, title, out_path):
    if not rows:
        return
    wins = {m: 0 for m in METHODS}
    ranks = {m: [] for m in METHODS}
    for r in rows:
        m = r["method"]
        if m in wins:
            if r.get("won"):
                wins[m] += 1
            ranks[m].append(float(r.get("rank", 4)))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    labels = [METHOD_LABELS.get(m, m) for m in METHODS]
    x = np.arange(len(METHODS))

    axes[0].bar(x, [wins[m] for m in METHODS], color=[COLORS[m] for m in METHODS])
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=15, ha="right")
    axes[0].set_ylabel("liczba wygranych (najlepszy best_f)")
    axes[0].set_title("Wygrane na problem")

    avg_rank = [np.mean(ranks[m]) if ranks[m] else np.nan for m in METHODS]
    axes[1].bar(x, avg_rank, color=[COLORS[m] for m in METHODS])
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=15, ha="right")
    axes[1].set_ylabel("średnia ranga (mniej = lepiej)")
    axes[1].set_ylim(1, len(METHODS) + 0.2)
    axes[1].set_title("Średnia ranga")

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def plot_scenario2_dims(rows, out_path):
    """Średnia ranga metody w zależności od wymiaru."""
    if not rows:
        return
    dims = sorted({int(r["dim"]) for r in rows})
    data = {m: [] for m in METHODS}
    for d in dims:
        sub = [r for r in rows if int(r["dim"]) == d]
        for m in METHODS:
            rs = [float(r["rank"]) for r in sub if r["method"] == m]
            data[m].append(np.mean(rs) if rs else np.nan)

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(dims))
    w = 0.2
    for i, m in enumerate(METHODS):
        ax.bar(x + (i - 1.5) * w, data[m], width=w, label=METHOD_LABELS[m], color=COLORS[m])

    ax.set_xticks(x)
    ax.set_xticklabels([f"D={d}" for d in dims])
    ax.set_ylabel("średnia ranga (mniej = lepiej)")
    ax.set_title("Scenariusz 2 — wpływ wymiarowości")
    ax.legend()
    ax.set_ylim(1, len(METHODS) + 0.2)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def plot_convergence_sample(scenario_dir: Path, out_path, problem_hint="f001"):
    """Kilka krzywych zbieżności z plików historii CSV."""
    files = sorted(scenario_dir.glob(f"s*{problem_hint}*.csv"), key=lambda p: p.stat().st_mtime)
    if not files:
        files = sorted(scenario_dir.glob("s*.csv"))[:4]
    picked = {}
    for f in files:
        for m in METHODS:
            if f"_{m}_" in f.name and m not in picked:
                picked[m] = f
        if len(picked) == len(METHODS):
            break

    if not picked:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    for m, fpath in picked.items():
        evals, bests = [], []
        with fpath.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                evals.append(int(row["evals"]))
                bests.append(float(row["best_f"]))
        ax.plot(evals, bests, label=METHOD_LABELS[m], color=COLORS[m], linewidth=1.5)

    ax.set_xlabel("liczba ewaluacji")
    ax.set_ylabel("najlepsze best_f")
    ax.set_title(f"Przykładowa zbieżność ({scenario_dir.name}, {problem_hint})")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def write_summary(all_rows, out_dir: Path, scenarios=None):
    lines = ["# Podsumowanie AMHE CMA-ES\n"]
    for sc in scenarios or ["1", "2", "3"]:
        rows = [r for r in all_rows if str(r.get("scenario")) == sc]
        if not rows:
            lines.append(f"\n## Scenariusz {sc}\n\nBrak danych.\n")
            continue
        lines.append(f"\n## Scenariusz {sc}\n")
        lines.append(f"- liczba przebiegów: {len(rows)}\n")
        for m in METHODS:
            sub = [r for r in rows if r["method"] == m]
            if not sub:
                continue
            wins = sum(1 for r in sub if r.get("won"))
            avg_r = np.mean([float(r["rank"]) for r in sub])
            hits = sum(1 for r in sub if str(r.get("target_hit", "")).lower() == "true")
            lines.append(
                f"- **{METHOD_LABELS[m]}**: wygrane={wins}/{len(sub)}, "
                f"śr. ranga={avg_r:.2f}, target_hit={hits}\n"
            )

    names = {
        "1": "pełny zestaw D=5",
        "2": "wymiarowość D=2,10,20",
        "3": "granica (1 ograniczenie)",
    }
    lines.append("\n## Pliki wykresów\n")
    for sc, desc in names.items():
        if scenarios and sc not in scenarios:
            continue
        lines.append(f"- scenariusz {sc} ({desc}): `scenario{sc}_*.png`\n")

    (out_dir / "podsumowanie.md").write_text("".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        nargs="+",
        choices=["1", "2", "3"],
        help="tylko wybrane scenariusze (domyślnie: wszystkie, dla których są dane)",
    )
    parser.add_argument("--results", default="results", help="folder z scenario1/2/3")
    parser.add_argument("--out", default="results/report", help="gdzie zapisać wykresy")
    args = parser.parse_args()

    base = Path(args.results)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    wanted = args.scenario or ["1", "2", "3"]
    all_rows = []
    for sc in wanted:
        rows = load_scenario(sc, base)
        all_rows.extend(rows)

    if not all_rows:
        print(f"Brak wyników w results/scenario* dla: {wanted}")
        return

    # rangi liczone osobno w obrębie każdego scenariusza
    ranked = []
    for sc in wanted:
        part = [r for r in all_rows if str(r.get("scenario")) == sc]
        ranked.extend(add_ranks(part))
    all_rows = ranked

    s1 = [r for r in all_rows if str(r.get("scenario")) == "1"]
    s2 = [r for r in all_rows if str(r.get("scenario")) == "2"]
    s3 = [r for r in all_rows if str(r.get("scenario")) == "3"]

    if s1:
        plot_method_wins(s1, "Scenariusz 1 — porównanie metod (D=5)", out / "scenario1_ranking.png")
        plot_convergence_sample(base / "scenario1", out / "scenario1_convergence.png")
    if s2:
        plot_method_wins(s2, "Scenariusz 2 — wszystkie wymiary", out / "scenario2_ranking.png")
        plot_scenario2_dims(s2, out / "scenario2_by_dimension.png")
        plot_convergence_sample(base / "scenario2", out / "scenario2_convergence.png", "f001_i01_d02")
    if s3:
        plot_method_wins(s3, "Scenariusz 3 — optimum na granicy", out / "scenario3_ranking.png")
        plot_convergence_sample(base / "scenario3", out / "scenario3_convergence.png", "f001")

    write_summary(all_rows, out, scenarios=wanted)

    print(f"Zapisano wykresy i podsumowanie w: {out.resolve()}")
    for p in sorted(out.glob("*")):
        print(f"  - {p.name}")


if __name__ == "__main__":
    main()
