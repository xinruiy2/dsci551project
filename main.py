from flask import Flask, request
import requests
import json
from datetime import date, timedelta

app = Flask(__name__, static_url_path = '')
@app.route('/')
def root():
    return app.send_static_file("main.html")


@app.route("/second", methods = ['GET'])
def getvalue():
    s = ""
    start = str(request.args.get('start'))
    end = str(request.args.get('end'))
    weather = str(request.args.get('weather'))
    print(start)
    print(end)
    print(weather)
    #Firebase
    sdate = date(int(start[0:4]), int(start[5:7]), int(start[8:]))
    edate = date(int(end[0:4]), int(end[5:7]), int(end[8:]))
    data={}
    dif = edate-sdate
    response = json.loads(requests.get("https://project551-1f44c.firebaseio.com/traffic.json").text)
    for i in range(dif.days + 1):
        day = sdate + timedelta(days=i)
        data[str(day)] = response[str(day)]
    #print(data)
    # url = ""
    # r = requests.get(url)
    # print(url)
    return data

if __name__ == '__main__':
    app.run(debug = True)
