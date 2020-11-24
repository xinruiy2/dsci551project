import json
import requests

class App(dict):
    def __str__(self):
        return json.dumps(self)


url = "https://project551-1f44c.firebaseio.com/traffic.json"
fp = open("traffic.json", 'w')
f = open("traffic-collision-data-from-2010-to-present.csv", 'r')

count = 0
traffic_list = []
head = 1
prev_day = ""
time_dict = {}
hour_list = []
for line in f:
    if head == 1:
        head = 0
        continue
    line = line.split(',')
    day = line[2][:10]
    area = line[5]
    time = line[3]
    if len(time) <= 2:
        time = "00"
    elif len(time) == 3:
        time = "0" + time[0]
    else:
        time = time[:2]
    if prev_day == "":
        prev_day = day
    else:
        if prev_day != day:
            binding_list = []
            for key in time_dict.keys():
                binding_list.append([key, hour_list[time_dict[key]]])
            binding_dict = App(binding_list)
            traffic_list.append([prev_day, binding_dict])
            hour_list = []
            time_dict = {}
            prev_day = day
    if time in time_dict:
        if area in hour_list[time_dict[time]]:
            hour_list[time_dict[time]][area] += 1
        else:
            hour_list[time_dict[time]][area] = 1
    else:
        time_dict[time] = len(hour_list)
        hour_list.append({})
        hour_list[-1][area] = 1

if len(hour_list) !=0:
    binding_list = []
    for key in time_dict.keys():
        binding_list.append([key, hour_list[time_dict[key]]])
    binding_dict = App(binding_list)
    traffic_list.append([prev_day, binding_dict])

pairs = App(traffic_list)
json.dump(pairs,fp)
fp = open('traffic.json', 'r')
response = requests.put(url, fp)
print(response)


f.close()
fp.close()
