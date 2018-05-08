timestamps = [1,2,3,4,5,6,7,8,9,10]

timestamps_last_list = [14,13,12,11,9,5,17,18,19]

for i, line in enumerate(timestamps_last_list):
    try:
        timestamps_last_index = timestamps.index(timestamps_last_list[i])
    except Exception:
        pass
    print("i",i)
print("timestamps_last_index",timestamps_last_index)
print("timestamps[timestamps_last_index]",timestamps[timestamps_last_index])
timestamps = timestamps[timestamps_last_index:]
# print(j,'timestamps[-1]',timestamps[-1])
