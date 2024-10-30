import argparse
import math
import os
import time

# Генерация начального значения для seed на основе текущего времени
seed = int(time.time())  # Генерируем начальный seed один раз


# Линейный конгруэнтный генератор (LCG)
def lcg(seed, a=1664525, c=1013904223, m=2 ** 32):
    """Генерирует псевдослучайное число от 0 до 1 на основе линейного конгруэнтного метода"""
    seed = (a * seed + c) % m
    return seed, seed / m


# Функции для каждого распределения
def generate_uniform(data, p1, p2, seed):
    generated = []
    for _ in data:
        seed, rnd = lcg(seed)
        generated.append(p1 + (p2 - p1) * rnd)
    return generated


def generate_triangular(data, p1, p2, p3, seed):
    generated = []
    for _ in data:
        seed, rnd1 = lcg(seed)
        seed, rnd2 = lcg(seed)
        u = min(rnd1, rnd2) if rnd1 < (p2 - p1) / (p3 - p1) else max(rnd1, rnd2)
        generated.append(p1 + (p3 - p1) * u)
    return generated


def generate_exponential(data, p1, seed):
    generated = []
    for _ in data:
        seed, rnd = lcg(seed)
        generated.append(-p1 * math.log(1 - rnd))
    return generated


def generate_normal(data, p1, p2, seed):
    generated = []
    for _ in data:
        seed, rnd1 = lcg(seed)
        seed, rnd2 = lcg(seed)
        z = math.sqrt(-2 * math.log(rnd1)) * math.cos(2 * math.pi * rnd2)
        generated.append(p1 + p2 * z)
    return generated


def generate_gamma(data, p1, p2, seed):
    generated = []
    for _ in data:
        total = 0
        for _ in range(int(p1)):  # параметр k задается как целое число
            seed, rnd = lcg(seed)
            total += -math.log(1 - rnd)
        generated.append(total * p2)
    return generated


def generate_lognormal(data, p1, p2, seed):
    normal_data = generate_normal(data, p1, p2, seed)
    return [math.exp(x) for x in normal_data]


def generate_logistic(data, p1, p2, seed):
    generated = []
    for _ in data:
        seed, rnd = lcg(seed)
        generated.append(p1 + p2 * math.log(rnd / (1 - rnd)))
    return generated


def generate_binomial(data, p1, p2, seed):
    generated = []
    for _ in data:
        count = 0
        for _ in range(int(p1)):
            seed, rnd = lcg(seed)
            if rnd < p2:
                count += 1
        generated.append(count)
    return generated


# Обработка параметров командной строки
def parse_arguments():
    parser = argparse.ArgumentParser(description="Преобразование ПСЧ в другое распределение.")
    parser.add_argument("--f", dest="filename", required=True, help="Имя файла с входной последовательностью.")
    parser.add_argument("--d", dest="distribution", required=True,
                        choices=["st", "tr", "ex", "nr", "gm", "ln", "ls", "bi"], help="Код распределения.")
    parser.add_argument("--p1", dest="p1", type=float, required=True, help="Первый параметр.")
    parser.add_argument("--p2", dest="p2", type=float, required=False, help="Второй параметр.")
    parser.add_argument("--p3", dest="p3", type=float, required=False,
                        help="Третий параметр (для треугольного и гамма-распределений).")
    return parser.parse_args()


# Основная функция
def main():
    args = parse_arguments()

    # Чтение входных данных
    with open(args.filename, 'r') as file:
        data = [float(num) for line in file for num in line.split()]

    # Определение распределения и генерация значений
    global seed  # Используем глобально заданный начальный seed
    if args.distribution == "st":
        transformed_data = generate_uniform(data, args.p1, args.p2, seed)
    elif args.distribution == "tr":
        transformed_data = generate_triangular(data, args.p1, args.p2, args.p3, seed)
    elif args.distribution == "ex":
        transformed_data = generate_exponential(data, args.p1, seed)
    elif args.distribution == "nr":
        transformed_data = generate_normal(data, args.p1, args.p2, seed)
    elif args.distribution == "gm":
        transformed_data = generate_gamma(data, args.p1, args.p2, seed)
    elif args.distribution == "ln":
        transformed_data = generate_lognormal(data, args.p1, args.p2, seed)
    elif args.distribution == "ls":
        transformed_data = generate_logistic(data, args.p1, args.p2, seed)
    elif args.distribution == "bi":
        transformed_data = generate_binomial(data, int(args.p1), args.p2, seed)
    else:
        raise ValueError("Неподдерживаемое распределение")

    # Сохранение результата
    output_filename = f"distr-{args.distribution}.dat"
    with open(output_filename, 'w') as file:
        file.write("\n".join(map(str, transformed_data)))

    print(f"Результат сохранен в {output_filename}")


if __name__ == "__main__":
    main()
