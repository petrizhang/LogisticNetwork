import argparse
import utils
import pandas as pd
import numpy as np


def n_hub_once(n: int):
    # randomly choose initial hubs
    hubs = utils.random_init_hubs(n)
    print(f'initial hubs:{hubs}')

    all_cities = list(range(0, utils.score.N))
    owner = -1 * np.ones([utils.score.N, ])

    round = 1
    while True:
        print(f"{'=' * 20} start of round {round}{'=' * 20}")
        print(hubs)
        if len(set(hubs)) != n:
            print("!!!Damage Error!!!")
            break
        cities_to_assign = all_cities
        # calculate owner score for all cities and hubs
        cities_owner_score = np.asarray(
            [utils.score.city_hub_score(cities_to_assign, h, hubs) for h in hubs]).T
        hub_index = cities_owner_score.argmin(axis=1)

        # update owner for all cities
        owner[cities_to_assign] = hubs[hub_index]
        owner[hubs] = hubs

        utils.print_hubs(hubs, owner)

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
            cities_to_assign = utils.owned_by(h, owner)

            no_hubs_and_h = list(set(all_cities) - (set(new_hubs) - {h}))
            cities_score = [utils.score.hub_score(c, utils.replace(new_hubs, h, c), cities_to_assign) for c in
                            no_hubs_and_h]
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
                new_hubs = utils.replace(new_hubs, h, best_city)
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
    all_cities = range(0, utils.score.N)
    result = []
    for i in range(iter):
        hubs, owner = n_hub_once(n)
        result.append(((hubs, owner), utils.score.network_score(hubs, all_cities, owner)))
    min_result = min(result, key=lambda x: x[1]['overall score'])

    return min_result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-iter','--iteration',type=int, help="iteration rounds")
    parser.add_argument('-n','--nhub',type=int, help='the number of hubs')
    args = parser.parse_args()
    k = 5
    iteration = 10 
    if args.iteration:
        iteration = int(args.iteration)
    if args.nhub:
        k = int(args.nhub)
    result = n_hub(k, iteration)
    (hubs, owner), _ = result
    utils.print_result(result)
    # print(utils.score.delivery_time(hubs, range(81), owner))

if __name__ == '__main__':
    main()
