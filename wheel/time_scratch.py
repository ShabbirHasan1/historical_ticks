from datetime import datetime
import pause

start_time = datetime(2021, 7, 28, 4, 39, 0)
end_time = datetime(2021, 7, 28, 4, 40, 0)
# start_time = datetime(2021, 7, 27, 9, 30, 0)
# end_time = datetime(2021, 7, 27, 16, 00, 0)
diff = end_time - start_time
print(diff)
num_slices = 4
time_slice = diff / num_slices
print(time_slice)
first_slice = start_time + time_slice
print(first_slice)
list_of_times = []
i = 1
for i in range(1,num_slices):
    new_time = start_time + time_slice
    list_of_times.append(new_time)
    start_time = new_time
    i += 1
print(list_of_times)

time_counter = 0
for j in list_of_times:
    trade_time = list_of_times[time_counter]
    pause.until(trade_time)
    print(f'BUY at {trade_time}')
    time_counter += 1






