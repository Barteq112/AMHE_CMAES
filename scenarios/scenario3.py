"""
Scenariusz 3 — stabilność na granicy (funkcje z 1 ograniczeniem).

  python -m scenarios.scenario3
  python scenarios/scenario3.py
"""

import argparse

from scenarios._common import execute

KEY = "3"
NAME = "Stabilność na granicy (funkcje z 1 ograniczeniem)"
SUITE_OPTIONS = (
    "dimensions: 5 function_indices: 1, 7, 13, 19, 25, 31, 37, 43, 49 "
    "instance_indices: 1-3"
)
BUDGET_MULT = 100
COCO_SUBDIR = "scenario3"
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
