import json
import requests

class App(dict):
    def __str__(self):
        return json.dumps(self)


url = "https://project551-1f44c.firebaseio.com/weather.json"
fp = open("weather.json", 'w')
f = open("weather_description.csv", 'r')
dict_date_time = {}

head = 1
whole_list = []
prev_day = ""
day_dict ={}
for line in f:
    if head == 1:
        head = 0
        continue
    line = line.split(',')
    day = line[0][:10]
    time = line[0][11:13]
    day_dict[time] = line[5]
    if prev_day != "":
        if day != prev_day:
            whole_list.append([prev_day, day_dict])
            prev_day = day
            day_dict = {}
    else:
        prev_day = day

whole_list.append([prev_day, day_dict])

pairs = App(whole_list)
json.dump(pairs,fp)
fp = open('weather.json', 'r')
response = requests.put(url, fp)
print(response)


f.close()
fp.close()
