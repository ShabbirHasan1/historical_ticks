import pandas as pd

# https://stackoverflow.com/questions/20845213/how-to-avoid-python-pandas-creating-an-index-in-a-saved-csv

df1 = pd.read_csv('tick_history_subset.csv', index_col=0)
print(df1)
