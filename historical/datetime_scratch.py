from datetime import datetime

# querytime = datetime.datetime.today()
# print(querytime)

now = datetime.now()
current_time = now.strftime("%Y%m%d %H:%M:%S")
print(current_time)