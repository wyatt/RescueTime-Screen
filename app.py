# -*- coding: utf-8 -*-
# Importing libraries
from flask import Flask, request, render_template
import requests
import json
import html2text
import time

# Flask config
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Insert your key from RescueTime here
key = "<YOUR_KEY>"

@app.route('/', methods=['POST', 'GET'])
def display():
    # Get RescueTime data
    jsondata = 0
    try:
        jsondata = requests.get("https://www.rescuetime.com/anapi/data?key=" + key).text
    except requests.ConnectionError:
        time.sleep(5)
        display()
    # Parse RecueTime data
    h = html2text.HTML2Text()
    jsondata = h.handle(jsondata)
    jsondata = jsondata.replace('\n', '')
    try:
        jsondata = json.loads(jsondata)
    except json.JSONDecodeError:
        time.sleep(5)
        display()
    # Calculates and formats total time
    total = 0
    for x in range(0, len(jsondata["rows"])):
        total += jsondata["rows"][x][1]
    hours = int(total/3600)
    mins = int((((total/3600)*60)%60))
    if mins < 10:
        mins = str("0" + str(mins))
    totaltime = str(str(hours) + "<span>:</span>" + str(mins))
    # Inserts data into time.html
    return render_template("time.html", total = totaltime)

# Runs app in debug mode
if __name__ == '__main__':	
    app.run(debug=True)
