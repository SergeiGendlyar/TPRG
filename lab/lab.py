import numpy as np
from matplotlib import pyplot as plt
import scipy.stats as stats
import math


def read_numbers(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    raw_data = "".join(lines)
    number_strings = raw_data.split(",")
    return [int(num.strip()) for num in number_strings if num.strip()]


def plot_statistics(numbers):
    sizes = []
    means = []
    std_devs = []

    for i in range(len(numbers)):
        sizes.append(i + 1)
        means.append(np.mean(numbers[:i + 1]))
        std_devs.append(stats.tstd(numbers[:i + 1]))

    plt.plot(sizes, means, label="ожидание")
    plt.plot(sizes, std_devs, label="отклонение")
    plt.xlabel("выборка")
    plt.title("график")
    plt.legend()
    plt.show()


def compute_relative_errors(sequence):
    TARGET_MEAN = 0.5
    TARGET_STD_DEV = 0.2887

    actual_mean = np.mean(sequence)
    actual_std_dev = stats.tstd(sequence)

    print(f"ошибка математического ожидания: {abs(TARGET_MEAN - actual_mean)}")
    print(f"ошибка стандартного отклонения: {abs(TARGET_STD_DEV - actual_std_dev)}")


def normalize_sequence(sequence):
    max_value = max(sequence) + 1
    return [num / max_value for num in sequence]


def chi_square_analysis(sequence, alpha=0.05, observed=None, expected=None, categories=None):
    if categories is None:
        categories = len(np.unique(sequence))
    if observed is None:
        _, observed = np.unique(sequence, return_counts=True)
    if expected is None:
        expected = np.array([len(sequence) / categories] * categories)

    chi_stat = np.sum((observed - expected) ** 2 / expected)
    critical_value = stats.chi2.ppf(1 - alpha, categories - 1)

    return "-" if chi_stat > critical_value else "+"


def series_analysis(sequence):
    dimension = 16
    alpha = 0.05
    categories = dimension ** 2
    counts = np.zeros(categories, dtype=int)

    for j in range(len(sequence) // 2):
        index = int(sequence[2 * j] * dimension) * dimension + int(sequence[2 * j + 1] * dimension)
        counts[index] += 1

    return chi_square_analysis(sequence, alpha, counts, np.full(categories, len(sequence) / (2 * categories)),
                               categories)


def interval_analysis(sequence):
    dimension = 16
    empirical_counts = [0] * 8
    total_intervals = len(sequence) / 10
    half = 0.5
    theoretical_counts = [total_intervals * half * (1.0 - half) ** r for r in range(7)] + [
        total_intervals * (1.0 - half) ** 7]

    index = 0
    while index < len(sequence) and index < total_intervals:
        run_length = 0
        while index < len(sequence) and sequence[index] < dimension / 2:
            index += 1
            run_length += 1
        empirical_counts[min(run_length, 7)] += 1

    return "-" if index == len(sequence) else chi_square_analysis(sequence, 0.05, theoretical_counts, empirical_counts,
                                                                  8)


def partition_analysis(sequence):
    alpha = 0.05
    num_partitions = 100
    categories = int(10000 / num_partitions)
    counts = np.zeros(categories + 1, dtype=int)

    for i in range(num_partitions):
        unique_count = len(np.unique(sequence[categories * i: categories * (i + 1)]))
        counts[unique_count] += 1

    probabilities = []
    for i in range(categories + 1):
        probability = 100
        for j in range(1, i):
            probability *= 100 - j
        probabilities.append(probability / pow(100, categories))

    expected_counts = np.array([math.comb(categories + i - 1, i) / pow(100, categories) for i in range(categories + 1)])
    return chi_square_analysis(sequence, alpha, expected_counts[1:], probabilities[1:], categories)


def permutation_analysis(sequence):
    alpha = 0.05
    tuple_size = 10
    n = len(sequence)
    frequency_dict = {}
    total_permutations = math.factorial(tuple_size)

    for i in range(0, n, tuple_size):
        group = tuple(sorted(sequence[i:i + tuple_size]))
        frequency_dict[group] = frequency_dict.get(group, 0) + 1

    observed_counts = sorted(frequency_dict.values(), reverse=True)
    expected_counts = np.array([n / total_permutations] * len(observed_counts))

    return chi_square_analysis(sequence, alpha, observed_counts, expected_counts, total_permutations)


def monotonicity_analysis(sequence):
    alpha = 0.05
    A_matrix = [
        [4529.4, 9044.9, 13568, 22615, 22615, 27892],
        [9044.9, 18097, 27139, 36187, 45234, 55789],
        [13568, 27139, 40721, 54281, 67582, 83685],
        [18091, 36187, 54281, 72414, 90470, 111580],
        [22615, 45234, 67852, 90470, 113262, 139476],
        [27892, 55789, 83685, 111580, 139476, 172860]
    ]
    b_values = [1 / 6, 5 / 24, 11 / 120, 19 / 720, 29 / 5040, 1 / 840]
    n = len(sequence)
    runs = []
    i = 0

    while i < n:
        length = 1
        while i + length < n and sequence[i + length - 1] <= sequence[i + length]:
            length += 1
        runs.append(length)
        i += length

    counts = {}
    for run in runs:
        counts[run] = counts.get(run, 0) + 1

    results = []
    temp_index = 0

    for run_length in runs:
        m_value = 1 / 6
        min_value = min(run_length, 6)
        for i in range(min_value):
            for j in range(min_value):
                m_value += (sequence[temp_index + i] - n * b_values[i]) * (sequence[temp_index + j] - n * b_values[j]) * \
                           A_matrix[i][j]
        temp_index += run_length
        results.append(m_value)

    return chi_square_analysis(results, alpha)


def conflict_analysis(sequence):
    num_buckets = 1024
    sequence_length = len(sequence)
    sr_ = sequence_length / num_buckets
    p0 = 1 - sequence_length / num_buckets + math.factorial(sequence_length) / (
                2 * math.factorial(sequence_length - 2) * num_buckets ** 2)
    conf_value = sequence_length / num_buckets - 1 + p0

    return  "-" if abs(conf_value - sr_) > 10 else "+"

if __name__ == "__main__":
    filepath = input("файл: ")
    number_sequence = read_numbers(filepath)
    normalized_sequence = normalize_sequence(number_sequence)

    mean_value = np.mean(normalized_sequence)
    print(f"ожидание: {mean_value}")

    std_deviation = stats.tstd(normalized_sequence)
    print(f"отклонение: {std_deviation}")

    compute_relative_errors(normalized_sequence)

    print("Результаты статистических критериев:")
    print("Критерий хи-квадрат:", chi_square_analysis(normalized_sequence))
    print("Тест серий:", series_analysis(normalized_sequence))
    print("Тест интервалов:", interval_analysis(normalized_sequence))
    print("Тест разбиений:", partition_analysis(normalized_sequence))
    print("Тест перестановок:", permutation_analysis(normalized_sequence))
    print("Тест монотонности:", monotonicity_analysis(normalized_sequence))
    print("Тест конфликтов:", conflict_analysis(normalized_sequence))

    plot_statistics(normalized_sequence)
