import pandas as pd
from numpy.random import randint

rand_num = randint(10, size=8)
print(rand_num)
rand_lst = rand_num.tolist()

df = pd.DataFrame(rand_lst)
print(df)
