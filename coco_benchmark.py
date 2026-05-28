"""bbob-constrained z cocoex."""

import cocoex


def make_suite(suite_options):
    return cocoex.Suite("bbob-constrained", "", suite_options)


def make_observer(result_folder="results_coco"):
    import os
    os.makedirs(result_folder, exist_ok=True)
    opts = f"result_folder: {result_folder}"
    return cocoex.Observer("bbob-constrained", opts)


def problem_label(problem):
    return problem.id.replace("bbob-constrained_", "").replace("_", " ")
