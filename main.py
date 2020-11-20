from flask import Flask, request
import requests
import json
import mysql.connector
from datetime import date, timedelta
from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext, Row
from pyspark.sql import SQLContext, Row
from pyspark.sql.types import IntegerType


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
	cnx = mysql.connector.connect(user = 'root', password = 'root', host = '127.0.0.1',database = '551project')
	response = json.loads(requests.get("https://project551-1f44c.firebaseio.com/traffic.json?orderBy=\"$key\"&startAt=\""+start+"\"&endAt=\""+end+"\"").text)
	res = {}
	for date in response:
		res[date] = {}
		for hour in response[date]:
			cursor = cnx.cursor()
			query = "select weather from weather_LA where date = '%s' and hour = '%s'" % (date, hour)
			cursor.execute(query)
			for item in cursor:
				if item[0] == weather:
					res[date][hour] = response[date][hour]
	pairs = App(res)
	return pairs


if __name__ == '__main__':
    app.run(debug = True)
