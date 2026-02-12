#####################################################################################################
#
# NSGA-II tool box for the selection and evolutionary process.
#
# https://github.com/EpistasisLab/StarBASE-GP/blob/main/Source/nsga_tool.py
#####################################################################################################

import numpy as np
from typeguard import typechecked
from typing import List, Tuple
import numpy.typing as npt

@typechecked # for debugging purposes
def non_dominated_sorting(obj_scores: npt.NDArray[float], weights: npt.NDArray[float]) -> Tuple[List[npt.NDArray[int]],npt.NDArray[int]]:
    """
    Perform non-dominated sorting for a maximization problem using NumPy arrays of type float.

    Parameters:
    obj_scores (np.ndarray): A 2D array where each row represents the objective values for a solution.

    Returns:
    Tuple(fronts, rank):
    fronts (list of numpy array of int): Each sublist contains the indices of solutions in the corresponding Pareto front.
    rank (numpy array of int): The front rank of each solution in the population.
    """

    # quick check to make sure that elements in scores are numpy arrays with float
    assert all(isinstance(x, np.ndarray) for x in obj_scores)
    assert isinstance(obj_scores[0][0], (float, np.floating))
    assert all(len(x) == len(weights) for x in obj_scores)

    pop_size = obj_scores.shape[0]
    # final fronts returned
    fronts = [[]]
    # what front is solutions 'p' in
    rank = np.zeros(pop_size, dtype=int)
    # how many 'q' solutions dominate 'p' solution
    domination_count = np.zeros(pop_size, dtype=int)
    # what 'q' solutions are dominated by 'p' solution
    dominated_solutions = [[] for _ in range(pop_size)]

    # update obj_scores based on weights
    obj_scores = obj_scores * weights

    for p in range(pop_size):
        for q in range(pop_size):
            if dominates(obj_scores[p], obj_scores[q]):
                dominated_solutions[p].append(q)
            elif dominates(obj_scores[q], obj_scores[p]):
                domination_count[p] += 1

        if domination_count[p] == 0:
            rank[p] = 0
            fronts[0].append(p)

    i = 0
    while len(fronts[i]) > 0:
        next_front = []
        for p in fronts[i]:
            for q in dominated_solutions[p]:
                domination_count[q] -= 1
                assert domination_count[q] >= 0 #check that it's always positive
                if domination_count[q] == 0:
                    rank[q] = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    fronts.pop()

    fronts = [np.array(front, dtype=int) for front in fronts]
    return fronts, rank

# calculate the crowding distance for all individuals within the population
@typechecked
def crowding_distance(obj_scores: npt.NDArray[float], count: int, front_map: List[npt.NDArray[int]]) -> npt.NDArray[float]:
    """
    Calculate the crowding distance for each individual in the population.

    Parameters:
    - obj_scores: List of performances on obj_scores for each individual. We are assuming that the
                position of scores are the same as the position of the individuals in the population.
    - count: Number of obj_scores.

    Returns:
    - crowding_distances: List of crowding distances corresponding to each individual.
    """

    # quick check to make sure that elements in scores are numpy arrays with float
    assert all(isinstance(x, np.ndarray) for x in obj_scores)
    # make sure all elements are of the correct type
    assert isinstance(obj_scores[0][0], (float, np.floating))

    # initialize the crowding distances to negative for guards
    crowding_distances = np.full(len(obj_scores), -1.0, dtype=float)

    for front in front_map:
        # set inital front crowding distances to zero for addition
        crowding_distances[front] = 0.0

        for m in range(count):
            # Sort the front scores based on the m-th objective
            sorted_indices = np.argsort([ind[m] for ind in obj_scores[front]], kind='mergesort')
            sorted_front = obj_scores[front[sorted_indices]]

            # calculate the range of the m-th objective
            min_obj = sorted_front[0][m]
            max_obj = sorted_front[-1][m]

            # skip if both max and min are the same
            if max_obj == min_obj:
                continue

            # set the crowding distance of boundary points to infinity
            crowding_distances[front[sorted_indices[0]]] = np.inf
            crowding_distances[front[sorted_indices[-1]]] = np.inf

            # calculate crowding distances for intermediate points
            for i in range(1, len(front) - 1):
                next_obj = sorted_front[i + 1][m]
                prev_obj = sorted_front[i - 1][m]
                crowding_distances[front[sorted_indices[i]]] += (next_obj - prev_obj) / (max_obj - min_obj)

    # make sure all crowding distances are non-negative
    assert np.all(crowding_distances >= 0.0)

    return crowding_distances

@typechecked # for debugging purposes
def dominates(solution1: npt.NDArray[float], solution2: npt.NDArray[float]) -> bool:
    """
    Check if solution1 dominates solution2.

    Parameters:
    solution1 (numpy array of float): The first solution's objective values.
    solution2 (numpy array of float): The second solution's objective values.

    Returns:
    bool: True if solution1 dominates solution2, False otherwise.
    """

    # check that solutions scores are of the same dimension
    assert solution1.shape == solution2.shape
    better_in_all = np.all(solution1 >= solution2)
    better_in_at_least_one = np.any(solution1 > solution2)

    return bool(better_in_all and better_in_at_least_one)

@typechecked # for debugging purposes
def non_dominated_binary_tournament(ranks: npt.NDArray[int], distances: npt.NDArray[float], rng: np.random.Generator) -> int:

    # make srue that ranks and distances are the same size
    assert ranks.shape == distances.shape

    # get two randome number between 0 and the population size
    t1,t2 = rng.integers(0, len(ranks), size=2, dtype=int)

    # make sure they are not the same solution
    while t1 == t2:
        t1,t2 = rng.integers(0, len(ranks), size=2, dtype=int)

    # check if the two solutions are in the same front
    if ranks[t1] == ranks[t2]:
        # the one with the greatest crowding distance wins
        return int(t1) if distances[t1] > distances[t2] else int(t2)

    # if they are in different fronts, the lower rank one wins
    else:
        return int(t1) if ranks[t1] < ranks[t2] else int(t2)
    

@typechecked # for debugging purposes
def non_dominated_truncate(fronts: List[npt.NDArray[int]], distances: npt.NDArray[float], N) -> npt.NDArray[int]:
    # make sure that fronts and distances are the nonempty
    assert sum([len(x) for x in fronts]) > 0 and len(distances) > 0
    # make sure that fronts and distances are the same size
    assert sum([len(x) for x in fronts]) == len(distances)
    # check that first object in fronts is a numpy array
    assert isinstance(fronts[0], np.ndarray)

    # surviving solutions
    survivors = []

    # go through each front and add the solutions to the survivors
    for front in fronts:
        # add solutions without ordering based on distance (as is)
        if len(survivors) + len(front) <= N:
            survivors.extend(front)
        else:
            # sort the front by crowding distance in decending order
            sorted_distance = np.flip(np.argsort(distances[front], kind='mergesort'))
            sorted_front = front[sorted_distance]
            survivors.extend(sorted_front[:N-len(survivors)])
            break

    assert len(survivors) == N
    return np.array(survivors, dtype=int)