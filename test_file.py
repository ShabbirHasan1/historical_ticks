from pandas import DataFrame
counter = 0
a = 0

while counter < 5:
    your_list = [a, a + counter, a + counter + 1]
    df = DataFrame(your_list, columns = ['Numbers'])
    print(df)
    counter = counter + 1



