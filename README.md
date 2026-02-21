# Comparing Reweighting Methods

This repository contains code and experimental results for evolving sample weights using a Genetic Algorithm (GA) to optimize predictive performance and fairness in machine learning models.

The proposed method evolves dataset-level sample weights and is compared against established reweighting baselines. The current implementation supports NSGA-II for multi-objective optimization.

---

## Repository Structure

- `main.py` – Runs the Genetic Algorithm to evolve sample weights.
- `compute_hv.py` – Computes Pareto hypervolume values and aggregates results into `all_hv.csv`.
- `friedman_wilcoxon_stats.R` – Performs Friedman and Wilcoxon signed-rank tests.
- `mixed_effects_modeling.Rmd` – Performs mixed-effects modeling analysis.
- `generate_plots.R` – Generates plots used in the paper.
- `Results/` – Contains experimental outputs and processed results used in tables and figures.

---

## Reproducing Statistical Analysis (Using Existing Results)

If experimental runs are already completed and stored in `Results/`:

1. Run `friedman_wilcoxon_stats.R`
2. Run `mixed_effects_modeling.Rmd`
3. Run `generate_plots.R`

---

## Reproducing Experiments from Scratch

1. Execute `main()` in `main.py` using a shell script.
   
   For:
   - `d` datasets  
   - `r` replicates  
   - 3 weighting methods  
   - 4 objective configurations  

   Total runs required:  d × r × 3 × 4


2. Store all output files in a folder named `Results/`.

3. Run:
- `compute_hv.py` to compute hypervolume values
- `friedman_wilcoxon_stats.R`
- `mixed_effects_modeling.Rmd`
- `generate_plots.R`

---

## Notes

This repository serves as supplementary material for the associated paper submission.  
All tables and figures in the manuscript are generated directly from the contents of `Results/`.

