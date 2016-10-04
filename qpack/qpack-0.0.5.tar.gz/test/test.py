import imp
import time
import msgpack
import qpack

COUNT = 10000

data = [1, 2, 3, {'b': True}, {'What?': 'Iriske is {}'
    .format('lief'), 'Hoe oud is ze?': 3}]


# data = {
#     'series float': [
#         [1471254705, 0.1],
#         [1471254707, 0.0],
#         [1471254710, 0.0]],
#     'series integer': [
#         [1471254705, 5],
#         [1471254708, -3],
#         [1471254710, -7]],
#     'aggr': [
#         [1447249033, 531], [1447249337, 0.0], [1447249633, 535], [1447249937, 0.0],
#         [1447250249, 532], [1447250549, 0.0], [1447250868, 530], [1447251168, 0.0],
#         [1447251449, 54], [1447251749, 0.0], [1447252049, 0.0], [1447252349, 0.0],
#         [1447252649, True], [1447252968, 0.0], [1447253244, 0.0], [1447253549, 0.0],
#         [1447253849, 534], [1447254149, 0.0], [1447254449, 0.0], [1447254748, 0.0]
#     ]
# }

print(data)
import sys

a = msgpack.packb(data)
b = qpack.packb(data)

print(a)
print(b)

print(len(a), sys.getrefcount(a))
print(len(b), sys.getrefcount(b))

start = time.time()
for i in range(COUNT):
    msgpack.packb(data)
print('MsgPack (C-module) Pack Time: {}'.format(time.time() - start))

start = time.time()
for i in range(COUNT):
    qpack.packb(data)
print('QPack (C-module)   Pack Time: {}'.format(time.time() - start))


print(sys.getrefcount(5), sys.getrefcount(True))
A = msgpack.unpackb(a)
print(sys.getrefcount(5), sys.getrefcount(True))
B = qpack.unpackb(b)
print(sys.getrefcount(5), sys.getrefcount(True))

print(A)
print(B)

start = time.time()
for i in range(COUNT):
    msgpack.unpackb(a)
print('MsgPack (C-module) UnPack Time: {}'.format(time.time() - start))

start = time.time()
for i in range(COUNT):
    qpack.unpackb(b)
print('QPack (C-module)   UnPack Time: {}'.format(time.time() - start))

