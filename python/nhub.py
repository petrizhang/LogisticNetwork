from data import *
from score import *
import numpy as np


def replace(a: np.ndarray, olde, newe):
    newarray = a.copy()
    newarray[newarray == olde] = newe
    return newarray


def print_hubs(hubs: np.ndarray, owner: np.ndarray):
    for h in hubs:
        cities = np.where(owner == h)[0]
        print(f"{h}:{cities}")


def print_result(result):
    (hubs, owner), (total_cost, total_time, score) = result
    n = len(hubs)
    print(f"{'*'*20} Solution for {n}-hub {'*'*20}")
    print(f"Find best result of:")
    print(f"Network Design:")
    print_hubs(hubs, owner)
    print(f"Metrics:")
    print(f"  - total operation cost: {total_cost}")
    print(f"  - total travel time: {total_time}")
    print(f"  - overall score: {score}")
    print(f"{'*'*20} End {'*'*20}")


source_cities = range(1, 30)
passed_hub = 2
hubs = [3, 4, 5, 6]

# hc(1,2,[3,4]) = array([76.547688, 70.748717])
# print(hc(source_cities, passed_hub, hubs))
# print(ht(source_cities, passed_hub, hubs))
# print(hscore(source_cities, passed_hub, hubs))
# print(city_hub_score(source_cities, passed_hub, hubs))
# print(hub_score([passed_hub, passed_hub], source_cities, hubs))

n = 5


def choose_initial_hub(n: int):
    pair_distance = {}
    for i in range(0, N):
        for j in range(0, N):
            pair_distance[(i, j)] = D[i, j]
    sorted_pair_distance = sorted(pair_distance.items(), key=lambda x: x[1], reverse=True)
    hubs = []
    for (i, j), d in sorted_pair_distance:
        if i not in hubs:
            hubs.append(i)
            if len(hubs) == n:
                return hubs
        if j not in hubs:
            hubs.append(j)
            if len(hubs) == n:
                return hubs


def owned_by(h: int, owner: np.ndarray):
    return np.where(owner == h)[0]


def n_hub_once(n: int):
    # randomly choose initial hubs
    hubs = []
    while True:
        randint = np.random.randint(0, N)
        if randint in hubs:
            continue
        hubs.append(randint)
        if len(hubs) == n:
            break
    hubs = np.asarray(hubs)
    # hubs = np.asarray(choose_initial_hub(n))
    print(f'initial hubs:{hubs}')

    all_cities = list(range(0, N))
    owner = -1 * np.ones([N, ])

    round = 1
    while True:
        print(f"{'=' * 20} start of round {round}{'=' * 20}")
        print(hubs)
        cities_to_assign = all_cities
        # calculate owner score for all cities and hubs
        cities_owner_score = np.asarray([city_hub_score(cities_to_assign, h, hubs) for h in hubs]).T
        hub_index = cities_owner_score.argmin(axis=1)

        # update owner for all cities
        owner[cities_to_assign] = hubs[hub_index]
        owner[hubs] = hubs

        print_hubs(hubs, owner)

        # calclulate hub score to update hubs
        # hubs_score = [hub_score(h, hubs, owned_by(h)) for h in hubs]
        # print('hubs:', hubs.tolist())
        # print('hubs score:', hubs_score)
        # sort hubs based on hubs_score with descending order
        # sorted_hubs = hubs[np.argsort(hubs_score)[::-1]]
        # print('sorted hub:', sorted_hubs)

        new_hubs = hubs.copy()
        for h in hubs:
            print('-' * 40)
            print(f'Reselect hub for hub-{h} region:')
            cities_to_assign = owned_by(h, owner)

            no_hubs_and_h = list(set(all_cities) - (set(hubs) - {h}))
            cities_score = [hub_score(c, replace(new_hubs, h, c), cities_to_assign) for c in no_hubs_and_h]
            print('Cities score:')
            print("\tcity\tscore")
            for city, score in zip(no_hubs_and_h, cities_score):
                print(f"\t{city}\t\t{score}")

            best_city = no_hubs_and_h[np.argmin(cities_score)]
            print(f'Best hub choice is city: {best_city}')
            if best_city == h:
                print("Best hub doesn't change.")
                continue
            else:
                print(f'Replace the old hub: {h}')
                owner[owner == h] = best_city
                owner[best_city] = best_city
                new_hubs = replace(new_hubs, h, best_city)
        if np.all(new_hubs == hubs):
            print(f"{'=' * 20} end of round {round}{'=' * 20}")
            break
        else:
            hubs = new_hubs
            # print(f'New hubs now are: {new_hubs}.')
            # print('Continue to search.')
        print(f"{'=' * 20} end of round {round}{'=' * 20}")
        round += 1

    return hubs, owner


def n_hub(n: int, iter=20):
    all_cities = range(0, N)
    result = []
    for i in range(iter):
        hubs, owner = n_hub_once(n)
        result.append(((hubs, owner), network_score(all_cities, owner)))
    min_result = min(result, key=lambda x: x[1][2])

    return min_result


results = [n_hub(i) for i in range(3,10)]
for r in results:
    print_result(r)
