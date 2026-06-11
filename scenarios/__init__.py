from scenarios._common import METHODS
from scenarios import scenario1, scenario2, scenario3

RUNNERS = {
    "1": scenario1.run,
    "2": scenario2.run,
    "3": scenario3.run,
}

__all__ = ["METHODS", "RUNNERS", "scenario1", "scenario2", "scenario3"]
