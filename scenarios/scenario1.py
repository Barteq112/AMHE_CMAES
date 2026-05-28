"""
Scenariusz 1 — porównanie skuteczności (D=5, pełny bbob-constrained).

  python -m scenarios.scenario1
  python scenarios/scenario1.py
"""

import argparse

from scenarios._common import execute

KEY = "1"
NAME = "Porównanie skuteczności (D=5, pełny zestaw)"
SUITE_OPTIONS = "dimensions: 5 function_indices: 1-54 instance_indices: 1-3"
BUDGET_MULT = 100
COCO_SUBDIR = "scenario1"
DIMENSIONS = None


def run(seed=42):
    return execute(
        KEY, NAME, SUITE_OPTIONS, BUDGET_MULT, COCO_SUBDIR,
        seed=seed, dimensions=DIMENSIONS,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=NAME)
    p.add_argument("--seed", type=int, default=42)
    run(seed=p.parse_args().seed)
