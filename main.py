from flask import Flask, request
import requests
import json
import mysql.connector
from datetime import date, timedelta

app = Flask(__name__, static_url_path = '')
@app.route('/')
def root():
    return app.send_static_file("main.html")

class App(dict):
    def __str__(self):
        return json.dumps(self)

def Merge(dict1, dict2):
    ret = {**dict1, **dict2}
    return ret

@app.route("/second", methods = ['GET'])
def getvalue():
    s = ""
    start = str(request.args.get('start'))
    end = str(request.args.get('end'))
    weather = str(request.args.get('weather'))
    #Firebase
#    sdate = date(int(start[0:4]), int(start[5:7]), int(start[8:]))
#    edate = date(int(end[0:4]), int(end[5:7]), int(end[8:]))
#    data={}
#    dif = edate-sdate
#    response = json.loads(requests.get("https://project551-1f44c.firebaseio.com/traffic.json?orderBy=\"$key\"&startAt=\""+start+"\"&endAt=\""+end+"\"").text)
    #mysql
    cnx = mysql.connector.connect(user = 'root', password = 'root', host = '127.0.0.1',database = '551project')
    cursor = cnx.cursor()
    query = "select date, hour from weather_LA where weather = '%s' and date >= '%s' and date <= '%s'" % (weather, start, end)
    cursor.execute(query)
    response = []
    dict_reponse = {}
    for item in cursor:
        day = str(item[0])
        hour = str(item[1])
        if(len(hour) < 2):
            hour = '0' + hour
        # print(hour)
        curr_response = requests.get("https://project551-1f44c.firebaseio.com/traffic/" + day +".json?orderBy=\"$key\"&equalTo=\"" + hour + "\"").json()
        if day in dict_reponse:
            dict_reponse[day][0] = Merge(dict_reponse[day][0],curr_response)
        else:
            dict_reponse[day] = []
            dict_reponse[day].append(curr_response)
    for key in dict_reponse.keys():
        response.append([key, dict_reponse[key][0]])
    # print(response)
    pairs = App(response)
    # print(pairs)
    return pairs


if __name__ == '__main__':
    app.run(debug = True)
