from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)  

import json
from urllib.request import urlopen
from datetime import datetime
from flask import jsonify, render_template
                                                                                                                                                                                                                                                      
                                                                                                                                       
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

@app.route('/commits/')
def commits():
    # Récupération des commits depuis le repo d'origine
    response = urlopen("https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits")
    raw = response.read()
    json_content = json.loads(raw.decode("utf-8"))

    # Dictionnaire : minute → nombre de commits
    minute_counts = {}

    for commit in json_content:
        date_string = commit["commit"]["author"]["date"]  # ex "2024-02-11T11:57:27Z"

        # Extraire la minute
        date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        minute = date_obj.minute  # ex 57

        # Compter les commits par minute
        if minute not in minute_counts:
            minute_counts[minute] = 1
        else:
            minute_counts[minute] += 1

    # Transformer en tableau exploitable par Google Charts
    results = [{"minute": m, "count": c} for m, c in minute_counts.items()]

    return jsonify(results=results)

@app.route("/commits_graph/")
def commits_graph():
    return render_template("commits.html")


  
if __name__ == "__main__":
  app.run(debug=True)
