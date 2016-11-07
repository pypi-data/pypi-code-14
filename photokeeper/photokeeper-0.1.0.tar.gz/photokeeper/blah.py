from tqdm import tqdm
from time import sleep

#t = tqdm(total=100)
for i in range(1000):
    sleep(1)
    print(i//10)
    #t.update(i//10)
#t.close()

