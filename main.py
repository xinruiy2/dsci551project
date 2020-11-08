from flask import Flask, request
import requests


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


    # url = ""
    # r = requests.get(url)
    # print(url)
    return ""

if __name__ == '__main__':
    app.run(debug = True)
