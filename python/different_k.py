from nhub import *


def bestk():
    results = []
    for i in range(2, 12):
        result = n_hub(i, 20)
        results.append(result[1])

    bestk_frame = pd.DataFrame(results, index=range(2, 12))
    bestk_frame.to_csv("bestk.csv", sep=',')


if __name__ == '__main__':
    bestk()
