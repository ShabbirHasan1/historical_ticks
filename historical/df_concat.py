import pandas as pd

lst = [4,5,6,7,8]
lst1 = [3,4,3,2,1]

df = pd.DataFrame(list(zip(lst, lst1)))
print(df)
df.to_csv('lists.csv')

lst3 = [5,6,7,8,0]
lst4 = [9,2,8,3,6]
df1 = pd.DataFrame(list(zip(lst3,lst4)))
print(df1)

# https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
frames = [df, df1]
result = pd.concat(frames, ignore_index=True)
# result = df.append(df1)
print(result)

