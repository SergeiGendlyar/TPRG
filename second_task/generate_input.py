import time


# Линейный конгруэнтный генератор (LCG) для генерации случайных чисел без использования модуля random
def lcg(seed, a=1664525, c=1013904223, m=2 ** 32):
    seed = (a * seed + c) % m
    return seed, seed / m


# Функция для генерации чисел и записи их в файл
def generate_input_file(filename, num_values=10000, seed=None):
    if seed is None:
        seed = int(time.time())  # Установка начального значения seed на основе времени

    with open(filename, 'w') as file:
        for _ in range(num_values):
            seed, rnd = lcg(seed)
            file.write(f"{rnd * 100:.2f} ")  # Число с точностью до 2 знаков, разделитель — пробел
            if _ % 10 == 9:  # Добавление новой строки после каждых 10 чисел
                file.write("\n")


# Генерация файла input.txt
generate_input_file("input.txt")
