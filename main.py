"""
AMHE — uruchomienie wybranych scenariuszy.

  python -m scenarios.scenario2      # tylko scenariusz 2
  python scenarios/scenario3.py     # tylko scenariusz 3

  python main.py --scenario 1 2 3   # wszystkie scenariusze
"""

import argparse
import sys

from scenarios import RUNNERS


def main():
    parser = argparse.ArgumentParser(description="AMHE CMA-ES + bbob-constrained")
    parser.add_argument(
        "--scenario",
        nargs="+",
        required=True,
        choices=list(RUNNERS.keys()),
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print("=== AMHE ===")
    print("Scenariusze:", args.scenario)

    for key in args.scenario:
        RUNNERS[key](seed=args.seed)

    print("\n=== Koniec ===")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(0)
    main()
