# AMHE — CMA-ES z ograniczeniami (bbob-constrained)

Projekt: porównanie metod obsługi ograniczeń w CMA-ES na benchmarku **bbob-constrained** (COCO / `cocoex`).

## Metody

- **rzut** (`project`) — rzut osobnika w stronę średniej populacji  
- **odrzucenie** (`reject`) — losowanie nowego dopuszczalnego osobnika  
- **kara** (`penalty`) — kara w funkcji celu za naruszenie ograniczeń  

## Uruchomienie eksperymentów

```bash
pip install -r requirements.txt

python -m scenarios.scenario1   # pełny zestaw, D=5
python -m scenarios.scenario2   # wymiarowość D=2,10,20
python -m scenarios.scenario3   # optimum na granicy

python main.py --scenario 1 2   # wybrane przez main.py
```

Wyniki liczbowe: `results/scenario1/`, `scenario2/`, `scenario3/`.  
Logi COCO (opcjonalnie ECDF): `exdata/results_coco/`.

## Wykresy i opis

```bash
python visualize_results.py
```

**Opis wykresów (scenariusz → plik PNG):** [results/report/README.md](results/report/README.md)
