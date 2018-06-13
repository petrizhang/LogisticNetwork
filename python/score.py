from typing import List
import numpy as np
from data import *
import itertools

D = np.asarray(RD)
F = np.asarray(RF)
T = np.asarray(RT)
U = np.asarray(RU)
N = 81
s = 0.001
a = 0.5
w1 = 0.5
w2 = 0.5


# batch cities score of all paths  through k to all hubs
# return a vector of the same size as cities
def hc(source_cities: List[int], passed_hub: int, all_hubs: List[int]):
    n_source_cities = len(source_cities)
    n_hubs = len(all_hubs)

    left = F[source_cities][:, [passed_hub]] * D[source_cities][:, [passed_hub]]
    right = a * F[:, [passed_hub]][all_hubs] * D[:, [passed_hub]][all_hubs]
    # print('raw left:\n', left)
    # print('raw right:\n', right)
    left = np.tile(left, [1, n_hubs])
    right = np.tile(right.T, [n_source_cities, 1])
    # print('left after tile:\n', left)
    # print('right after tile:\n', right)
    result = s * (left + right)
    # print(result)
    # print(result.sum(axis=1))
    return result.sum(axis=1)


def ht(source_cities: List[int], passed_hub: int, all_hubs: List[int]):
    n_source_cities = len(source_cities)
    n_hubs = len(all_hubs)
    left = T[source_cities][:, [passed_hub]]
    right = T[:, [passed_hub]][all_hubs]

    left = np.tile(left, [1, n_hubs])
    right = np.tile(right.T, [n_source_cities, 1])
    result = left + right
    return result.sum(axis=1)


def hscore(source_cities: List[int], passed_hub: int, all_hubs: List[int]):
    return w1 * hc(source_cities, passed_hub, all_hubs) + w2 * ht(source_cities, passed_hub, all_hubs)


def city_hub_score(cities: List[int], passed_hub: int, all_hubs: List[int]):
    """
    given cities {c1,c2,c3} and a hub h='passed_hub',
    return the score of (c1,h), (c2,h), (c3, h) ....
    :param cities: city batch to be scored
    :param passed_hub: a hub that all cities passed
    :param all_hubs: all hubs
    :return:
    """
    return hscore(cities, passed_hub, all_hubs)


def hub_score(hub_to_messure: List[int], all_hubs: List[int], cities: List[int]):
    """
    given a hub batch, return the hub score for them
    :param hub_to_messure:
    :param all_hubs:
    :param cities:
    :return:
    """
    return city_hub_score(cities, hub_to_messure, all_hubs).sum()


def network_score(all_cities: np.ndarray, owner: np.ndarray):
    odpairs = list(itertools.product(all_cities, all_cities))
    total_cost = 0.0
    total_time = 0.0
    for o, d in odpairs:
        k = int(owner[o])
        m = int(owner[d])
        total_cost += D[o, k] * F[o, k] + a * D[k, m] + D[d, m] * F[d, m]
        total_time += T[o, k] + T[k, m] + T[d, m]
    total_cost *= s
    return total_cost, total_time, w1 * total_cost + w2 * total_time
