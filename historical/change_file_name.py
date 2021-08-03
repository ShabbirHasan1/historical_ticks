import pandas as pd

lst = [3, 4, 5]
df = pd.DataFrame(lst)
print(df)
df.to_csv('test.csv')

# https://stackoverflow.com/questions/65365261/export-multiple-csv-file-using-different-filename-in-python