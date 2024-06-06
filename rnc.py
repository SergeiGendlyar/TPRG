import random
import argparse
import math

# Функции для генерации различных распределений

def uniform_distribution(size, interval):
    return [random.uniform(interval[0], interval[1]) for _ in range(size)]

def triangular_distribution(size, left, mode, right):
    return [random.triangular(left, mode, right) for _ in range(size)]

def exponential_distribution(size, scale):
    return [random.expovariate(1 / scale) for _ in range(size)]

def normal_distribution(size, mean, std_dev):
    return [random.normalvariate(mean, std_dev) for _ in range(size)]

def gamma_distribution(size, shape, scale):
    return [random.gammavariate(shape, scale) for _ in range(size)]

def lognormal_distribution(size, mean, std_dev):
    return [random.lognormvariate(mean, std_dev) for _ in range(size)]

def logistic_distribution(size, loc, scale):
    return [loc + scale * math.log(p / (1 - p)) for p in [random.random() for _ in range(size)]]

def binomial_distribution(size, n, p):
    n = int(n)  # Приведение n к целому числу
    return [sum(1 for _ in range(n) if random.random() < p) for _ in range(size)]

# Словарь для соответствия кодов распределений и функций генерации

distribution_functions = {
    'st': uniform_distribution,
    'tr': triangular_distribution,
    'ex': exponential_distribution,
    'nr': normal_distribution,
    'gm': gamma_distribution,
    'ln': lognormal_distribution,
    'ls': logistic_distribution,
    'bi': binomial_distribution
}

def main(args):
    # Проверка наличия функции для выбранного распределения
    if args.distribution not in distribution_functions:
        print("Ошибка: Неподдерживаемое распределение")
        return

    # Генерация чисел с выбранным распределением
    if args.distribution == 'st':
        interval = args.parameters
        data = distribution_functions[args.distribution](args.size, interval)
    elif args.distribution == 'tr':
        left, mode, right = args.parameters
        data = distribution_functions[args.distribution](args.size, left, mode, right)
    elif args.distribution == 'ex':
        scale = args.parameters[0]
        data = distribution_functions[args.distribution](args.size, scale)
    elif args.distribution == 'nr':
        mean, std_dev = args.parameters
        data = distribution_functions[args.distribution](args.size, mean, std_dev)
    elif args.distribution == 'gm':
        shape, scale = args.parameters
        data = distribution_functions[args.distribution](args.size, shape, scale)
    elif args.distribution == 'ln':
        mean, std_dev = args.parameters
        data = distribution_functions[args.distribution](args.size, mean, std_dev)
    elif args.distribution == 'ls':
        loc, scale = args.parameters
        data = distribution_functions[args.distribution](args.size, loc, scale)
    elif args.distribution == 'bi':
        n, p = args.parameters
        data = distribution_functions[args.distribution](args.size, n, p)

    # Сохранение результата в файл
    output_file = f"distr-{args.distribution}.dat"
    with open(output_file, 'w') as f:
        for number in data:
            f.write(f"{number}\n")

    print(f"Данные сохранены в файл {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Программа для преобразования последовательности ПСЧ в другую последовательность ПСЧ с заданным распределением.")
    parser.add_argument("-f", "--input_file", dest="input_file", help="Имя файла с входной последовательностью.")
    parser.add_argument("-d", "--distribution", dest="distribution", choices=distribution_functions.keys(), help="Код распределения для преобразования последовательности.")
    parser.add_argument("-p1", "--parameters", dest="parameters", nargs='+', type=float, help="Параметры для генерации ПСЧ заданного распределения.")
    parser.add_argument("--size", type=int, default=1000, help="Размер выходной последовательности. По умолчанию 1000.")

    args = parser.parse_args()
    main(args)