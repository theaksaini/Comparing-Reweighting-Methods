import numpy as np

from ga import GA


def _fitness_sum_pair(program):
    s = float(np.sum(program))
    return (s, -s)


def test_ga_initialize_population_sets_fitness():
    ga = GA(
        ind_size=3,
        pop_size=4,
        max_gens=2,
        random_state=0,
        mut_rate=0.1,
        cross_rate=0.5,
        fitness_func=_fitness_sum_pair,
        use_nsga=False,
    )
    ga.initialize_population()

    assert len(ga.population) == 4
    assert all(ind.fitness is not None for ind in ga.population)


def test_ga_step_optimize_ga_mode_updates_population():
    ga = GA(
        ind_size=4,
        pop_size=6,
        max_gens=2,
        random_state=1,
        mut_rate=0.2,
        cross_rate=0.7,
        fitness_func=_fitness_sum_pair,
        use_nsga=False,
    )
    ga.initialize_population()
    ga.step_optimize()

    assert len(ga.population) == 6
    assert all(ind.fitness is not None for ind in ga.population)


def test_ga_step_optimize_nsga_mode_runs():
    ga = GA(
        ind_size=2,
        pop_size=4,
        max_gens=2,
        random_state=2,
        mut_rate=0.1,
        cross_rate=0.9,
        fitness_func=_fitness_sum_pair,
        use_nsga=True,
    )
    ga.initialize_population()
    ga.step_optimize()

    assert len(ga.population) == 4
    assert all(ind.fitness is not None for ind in ga.population)
