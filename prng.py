import argparse
import random


def linear_congruential(length, params):
    seed, a, c, m = map(int, params.split(';'))
    result = []
    for _ in range(length):
        seed = (a * seed + c) % m
        result.append(seed)
    return result


def additive(length, params):
    seed, m, *others = map(int, params.split(';'))

    # Check if m is less than or equal to 1
    if m <= 1:
        m = 2  # Set m to a default value of 2

    result = []
    for _ in range(length):
        seed = (seed + random.randint(1, m - 1)) % m
        result.append(seed)
    return result


def five_parameter(length, params):
    seed, m, a, c, e = map(int, params.split(';'))
    result = []
    for _ in range(length):
        seed = (a * seed + c + e) % m
        result.append(seed)
    return result


def lfsr(length, params):
    seed, size, *taps = map(int, params.split(';'))
    state = seed
    result = []
    for _ in range(length):
        lsb = state & 1
        state >>= 1
        feedback = 0
        for tap in taps:
            feedback ^= (state >> (tap - 1)) & 1
        state |= (feedback << (size - 1))
        result.append(state)
    return result



def nfsr(length, params):
    seed, size, *taps = map(int, params.split(';'))
    state = seed
    result = []
    for _ in range(length):
        lsb = state & 1
        state >>= 1
        feedback = 0
        for tap in taps:
            feedback ^= (state >> (size - tap)) & 1
        state |= feedback << (size - 1)
        result.append(state)
    return result


def mersenne_twister(length, params):
    mt = random.sample(range(0, 2 ** 32), 624)
    result = []
    for _ in range(length):
        if not mt:
            mt = random.sample(range(0, 2 ** 32), 624)
        y = mt.pop(0)
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        result.append(y)
    return result


def rc4(length, params):
    key = list(map(int, params.split(';')))
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    result = []
    for _ in range(length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        result.append(S[(S[i] + S[j]) % 256])
    return result


def bbs(length, params):
    c, m, x, l = map(int, params.split(';'))
    result = []
    for _ in range(length):
        x = (x * x + c) % m
        result.append(x)
    return result


def rsa_generator(n, e, w, seed, n_count):
    result = []
    x = seed
    for _ in range(n_count):
        x = pow(x, e, n)
        result.append(x)
    return result


def main():
    parser = argparse.ArgumentParser(description='Generate pseudorandom numbers using different methods.')
    parser.add_argument('-g', '--method', metavar='method', type=str, help='Method of PRNG to use', required=True,
                        choices=['lc', 'add', '5p', 'lfsr', 'nfsr', 'mt', 'rc4', 'bbs', 'rsa'])
    parser.add_argument('-n', '--length', metavar='length', type=int, help='Length of the sequence', required=True)
    parser.add_argument('-i', '--params', metavar='params', type=str, nargs='+',
                        help='Parameters for the method separated by semicolons', required=True)
    parser.add_argument('-f', '--filename', metavar='filename', type=str, help='Output file name', required=False)
    args = parser.parse_args()

    params = ';'.join(args.params)

    print('Method:', args.method)
    print('Length:', args.length)
    print('Params:', params)
    print('Filename:', args.filename)

    if args.method == 'lc':
        result = linear_congruential(args.length, params)
        print('Result:', result)
    elif args.method == 'add':
        result = additive(args.length, params)
        print('Result:', result)
    elif args.method == '5p':
        result = five_parameter(args.length, params)
        print('Result:', result)
    elif args.method == 'lfsr':
        result = lfsr(args.length, params)
        print('Result:', result)
    elif args.method == 'nfsr':
        result = nfsr(args.length, params)
        print('Result:', result)
    elif args.method == 'mt':
        result = mersenne_twister(args.length, params)
        print('Result:', result)
    elif args.method == 'rc4':
        result = rc4(args.length, params)
        print('Result:', result)
    elif args.method == 'bbs':
        result = bbs(args.length, params)
        print('Result:', result)
    elif args.method == 'rsa':
        n, e, w, seed, n_count = map(int, params.split(';'))
        result = rsa_generator(n, e, w, seed, args.length)
        print('Result:', result)

    if args.filename:
        with open(args.filename, 'w') as f:
            for num in result:
                f.write(str(num) + '\n')

if __name__ == '__main__':
    main()
