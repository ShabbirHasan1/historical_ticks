from datetime import datetime

start_time = datetime(2021, 7, 27, 9, 30, 0)
end_time = datetime(2021, 7, 27, 16, 00, 0)
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






