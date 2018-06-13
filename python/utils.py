from score import *


def random_init_hubs(n: int):
    hubs = []
    while True:
        randint = np.random.randint(0, N)
        if randint in hubs:
            continue
        else:
            hubs.append(randint)
        if len(hubs) == n:
            break
    return np.asarray(hubs)


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
