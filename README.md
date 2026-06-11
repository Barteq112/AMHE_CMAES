# AMHE — CMA-ES z ograniczeniami (bbob-constrained)

Projekt: porównanie metod obsługi ograniczeń w CMA-ES na benchmarku **bbob-constrained** (COCO / `cocoex`).

## Metody

- **rzut** (`project`) — rzut osobnika w stronę średniej populacji
- **odrzucenie** (`reject`) — losowanie nowego dopuszczalnego osobnika
- **kara** (`penalty`) — kara w funkcji celu za naruszenie ograniczeń


## Docker

Po sklonowaniu repo i przy zainstalowanym Dockerze najprościej przejść kolejno przez:

```bash
docker compose up --build
docker compose run --rm amhe python benchmark_speed.py
docker compose run --rm amhe python visualize_results.py
```

Pierwsza komenda uruchamia eksperymenty z `main.py --scenario 1 2 3`. Dwie kolejne korzystają z tych samych danych zapisanych lokalnie w `results/` i `exdata/`.


Wyniki liczbowe: `results/scenario1/`, `scenario2/`, `scenario3/`.

Logi COCO: `exdata/results_coco/`.

Wyniki: `results/report/`.


## Uruchomienie eksperymentów bez dockera

```bash
pip install -r requirements.txt

python main.py --scenario 1 2 3
```

### Benchmark prędkości

```bash
python benchmark_speed.py
```

### Wykresy i opis

```bash
python visualize_results.py
```
