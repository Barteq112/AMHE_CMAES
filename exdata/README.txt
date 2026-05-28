Logi COCO (bbob-constrained) trafiają tutaj przy uruchomieniu scenariuszy.

Struktura po poprawnym runie:
  results_coco/scenario1/none/
  results_coco/scenario1/project/
  ...

Postprocessing ECDF:
  pip install cocopp
  python -c "import cocopp; cocopp.main('exdata/results_coco/scenario1/project')"

Ten folder można bezpiecznie skasować przed nowym pełnym eksperymentem.
