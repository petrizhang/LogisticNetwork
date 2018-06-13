from nhub import *


def different_a():
    a_range = [0.001, 0.01, 0.05, 0.1, 0.2, 0.8, 1.0]
    k = 4
    results = []
    for a in a_range:
        utils.score.a = a
        result = n_hub(k, 20)
        results.append(result[1])

    alpha_frame = pd.DataFrame(results, index=a_range)
    alpha_frame.to_csv("alpha.csv", sep=',')


if __name__ == '__main__':
    different_a()
