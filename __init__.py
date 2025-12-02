from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen

import sqlite3

                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #com22

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

@app.route('/commits_data/')
def commits_data():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits = response.json()

    minutes_count = {}

    for commit in commits:
        commit_obj = commit.get('commit', {})
        author = commit_obj.get('author', {})
        date_str = author.get('date')  # ex: "2024-02-11T11:57:27Z"
        if date_str:
            date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.minute
            minutes_count[minute] = minutes_count.get(minute, 0) + 1

    # transformer en liste pour Google Charts : [{minute: 12, count: 3}, ...]
    results = []
    for minute, count in sorted(minutes_count.items()):
        results.append({'minute': minute, 'count': count})

    return jsonify(results=results)

@app.route('/commits/')
def commits():
    return render_template('commits.html')


  
if __name__ == "__main__":
  app.run(debug=True)
