
time_delta_list=['1111','2222','3333']
time_delta_list_name=['1111','2222','3333']
rsi_value_list=['1321','3213214','52151']
message_this_coin = 'add'
for i, line in enumerate(time_delta_list):
    message_this_coin += str(i + time_delta_list_name[i] +'boonbong : ' + 'rsi = ' + rsi_value_list[i])
message_this_coin += '\n sexxxxxx'

print(message_this_coin)
