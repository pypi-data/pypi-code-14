from sys import argv
result = ""
size = int(argv[1])
for i in range(size):
    result += "".join(open("/tmp/f", "r").read().split("\n")[:-1][i::size])
print(result)
