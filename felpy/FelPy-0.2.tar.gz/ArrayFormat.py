import random

class Formatter():

    def __init__(self, args):
        self.builder = []
        self.add(args)


    def add(self, toAdd):
        if (type(toAdd) is list):
            for item in toAdd:
                self.builder.append(item)
        else:
            self.builder.append(toAdd)

    def randomize(self):
        used = []
        top = len(self.builder)
        print(top)
        for i in range(0,top):
            while True:
                rand = random.randrange(0,top)
                if (rand not in used):
                    used.append(rand)
                    break
        builder2 = []
        for num in used:
            builder2.append(self.builder[used[num]])
        self.builder=builder2

    def formatOutput(self, x, y):
        if x*y > len(self.builder):
            raise IndexError('The array cannot be put in a grid that small')
        final = []
        for i in range(0,x):
            row = []
            for j in range(0,y):
                row.append(self.builder[i+j*x])
            final.append(row)
        return final
