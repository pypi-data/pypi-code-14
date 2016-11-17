from itertools import count

def eratosphenes_sieve(iterable):
    num = next(iterable)
    yield num
    yield from eratosphenes_sieve(i for i in iterable if i % num != 0)

def primes_under(n):
    yield from eratosphenes_sieve(iter(range(2, n)))

print(list(primes_under(1001)))

