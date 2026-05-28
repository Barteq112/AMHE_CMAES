# Wyniki i wykresy — AMHE (CMA-ES + bbob-constrained)

Ten folder powstaje po uruchomieniu:

```bash
python visualize_results.py
python visualize_results.py --scenario 1    # tylko wybrane scenariusze
python visualize_results.py --out results/report
```

Porównywane są **3 metody** obsługi ograniczeń w CMA-ES:

| Kod | Nazwa | Opis |
|-----|--------|------|
| `project` | rzut | Osobnik poza obszarem dopuszczalnym jest przesuwany w stronę średniej populacji, aż trafi na brzeg |
| `reject` | odrzucenie | Niedopuszczalny osobnik jest zastępowany losowym punktem z dopuszczalnego obszaru |
| `penalty` | kara | Do wartości funkcji celu dodawana jest kara za naruszenie ograniczeń |

Benchmark: **bbob-constrained** (biblioteka `cocoex`).

---

## Pliki wspólne

- **`podsumowanie.md`** — tabela tekstowa: liczba przebiegów, liczba „wygranych”, średnia ranga, `target_hit` dla każdej metody i scenariusza.

---

## Scenariusz 1 — porównanie skuteczności (D = 5)

**Cel:** pełny zestaw funkcji bbob-constrained w 5 wymiarach (funkcje 1–54, instancje 1–3).

**Uruchomienie:** `python -m scenarios.scenario1`  
**Dane źródłowe:** `results/scenario1/` (`porownanie.csv`, pliki `s1_*.csv` / `s1_*.json`)

### Wykresy

- **`scenario1_ranking.png`**
  - Lewy panel: **ile problemów** (funkcja + instancja) dana metoda wygrała — ma najniższe `best_f` wśród trzech metod na tym samym zadaniu.
  - Prawy panel: **średnia ranga** (1 = najlepsza, 3 = najgorsza) na wszystkich problemach scenariusza 1.
  - Służy do ogólnego porównania: która metoda najczęściej daje najlepszy wynik na pełnym benchmarku w 5D.

- **`scenario1_convergence.png`**
  - Przykładowa **krzywa zbieżności** dla jednego problemu (domyślnie coś z rodziny f001): oś X = liczba ewaluacji, oś Y = najlepsze dotąd `best_f`.
  - Trzy linie = rzut, odrzucenie, kara — widać, jak szybko spada wartość celu w trakcie jednego runu.

---

## Scenariusz 2 — wpływ wymiarowości (D = 2, 10, 20)

**Cel:** sprawdzić, jak metody radzą sobie przy rosnącej liczbie wymiarów (w tym czy **odrzucenie** słabnie przy D = 10 i 20). Wybrane funkcje: f1, f2, f3, f7, f19, f43; mniejszy budżet ewaluacji niż w scenariuszu 1.

**Uruchomienie:** `python -m scenarios.scenario2`  
**Dane źródłowe:** `results/scenario2/`

### Wykresy

- **`scenario2_ranking.png`**
  - Jak `scenario1_ranking.png`, ale **zebrane dla wszystkich wymiarów** (2, 10, 20) naraz — ogólny ranking metod w tym eksperymencie.

- **`scenario2_by_dimension.png`**
  - **Średnia ranga** metody osobno dla **D = 2**, **D = 10** i **D = 20**.
  - Służy do wniosku z PDF: czy np. odrzucenie wyraźnie psuje się przy 10 i 20 wymiarach (wyższa ranga = gorzej).

- **`scenario2_convergence.png`**
  - Przykładowa zbieżność dla problemu w **2D** (np. f001) — porównanie trzech metod na jednym zadaniu niskiego wymiaru.

---

## Scenariusz 3 — stabilność na granicy ograniczeń

**Cel:** funkcje z **jednym** ograniczeniem (f1, f7, f13, f19, f25, f31, f37, f43, f49) — optimum leży na aktywnym ograniczeniu; test, która metoda dobrze szuka rozwiązania **przy brzegu** obszaru dopuszczalnego.

**Uruchomienie:** `python -m scenarios.scenario3`  
**Dane źródłowe:** `results/scenario3/`

### Wykresy

- **`scenario3_ranking.png`**
  - Wygrane i średnia ranga — tylko na zadaniach „na granicy” (D = 5, warianty z 1 ograniczeniem).

- **`scenario3_convergence.png`**
  - Przykładowa krzywa zbieżności dla jednego z tych problemów (np. f001 z 1 ograniczeniem).

---

## Jak czytać ranking (ważne)

- Porównanie jest po wartości **`best_f`** zapisanej przez CMA-ES (niżej = lepiej w rankingu na danym problemie).
- Wszystkie trzy metody starają się trzymać ograniczeń; wynik **nie** jest tym samym co oficjalny wykres **ECDF** z COCO (ten powstaje z logów w `exdata/results_coco/` i `cocopp`).
- Kolumna **`target_hit`** w `podsumowanie.md` pochodzi z COCO — informuje, czy algorytm osiągnął zadany próg celu przy dopuszczalnym postępie (wartość > 0 bywa cenniejsza niż sama „wygrana” po `best_f`).

---

## Szybkie odświeżenie wykresów

Po dokończeniu lub zmianie wyników w `results/scenario*/`:

```bash
python visualize_results.py              # wszystkie scenariusze z danymi
python visualize_results.py --scenario 3 # tylko scenariusz 3
```

Nowe pliki PNG i `podsumowanie.md` nadpiszą poprzednie w tym folderze.
