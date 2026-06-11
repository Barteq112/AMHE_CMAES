"""
Scenariusz 2 — wpływ wymiarowości (D=2, 10, 20).

  python -m scenarios.scenario2
  python scenarios/scenario2.py
"""

import argparse

from scenarios._common import execute

KEY = "2"
NAME = "Wpływ wymiarowości (D=2, 10, 20)"
SUITE_OPTIONS = "function_indices: 1, 2, 3, 7, 19, 43 instance_indices: 1"
BUDGET_MULT = 50
COCO_SUBDIR = "scenario2"
DIMENSIONS = [2, 10, 20]


def run(seed=42):
    return execute(
        KEY,
        NAME,
        SUITE_OPTIONS,
        BUDGET_MULT,
        COCO_SUBDIR,
        seed=seed,
        dimensions=DIMENSIONS,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=NAME)
    p.add_argument("--seed", type=int, default=42)
    run(seed=p.parse_args().seed)
