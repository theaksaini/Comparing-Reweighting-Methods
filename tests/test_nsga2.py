import numpy as np

import nsga2 as nsga


def test_dominates_basic():
    a = np.array([2.0, 2.0])
    b = np.array([1.0, 2.0])
    c = np.array([2.0, 3.0])

    assert nsga.dominates(a, b) is True
    assert nsga.dominates(a, c) is False
    assert nsga.dominates(c, a) is True


def test_non_dominated_sorting():
    scores = np.array([
        [1.0, 1.0],
        [2.0, 1.0],
        [1.0, 2.0],
        [2.0, 2.0],
    ])
    weights = np.array([1.0, 1.0])

    fronts, ranks = nsga.non_dominated_sorting(scores, weights)

    assert len(fronts) >= 1
    assert ranks.shape[0] == scores.shape[0]
    assert 3 in fronts[0]  # [2,2] should be non-dominated


def test_crowding_distance_per_front():
    scores = np.array([
        [1.0, 1.0],
        [2.0, 1.0],
        [1.0, 2.0],
        [2.0, 2.0],
    ])
    weights = np.array([1.0, 1.0])

    fronts, _ = nsga.non_dominated_sorting(scores, weights)
    distances = nsga.crowding_distance(scores, 2, fronts)

    assert distances.shape[0] == scores.shape[0]
    assert np.isfinite(distances).any()


def test_non_dominated_binary_tournament_prefers_rank():
    rng = np.random.default_rng(0)
    ranks = np.array([0, 1, 2, 3])
    distances = np.array([0.1, 0.2, 0.3, 0.4])

    winner = nsga.non_dominated_binary_tournament(ranks, distances, rng)
    assert winner in range(len(ranks))
