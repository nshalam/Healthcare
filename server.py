#flask --app data_server run
from flask import Flask
from flask import render_template
from flask import request
import json


app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    f = open("data/refined_data.json", "r")
    data = json.load(f)
    f.close()
    states=[]
    insured = {}
    for state in data:
        states.append(state["Location"])
        insured[state["Abbreviation"]]=state["Uninsured"]
        
    return render_template('index.html', states=sorted(states), data=data)

@app.route('/about')
def about():
    f = open("data/refined_data.json", "r")
    data = json.load(f)
    f.close()
    states=[]
    for state in data:
        states.append(state["Location"])
        
    return render_template('about.html', states=sorted(states))

@app.route('/state')
def state():
    location = request.args.get('name')
    with open("data/refined_data.json", "r") as f:
        data = json.load(f)
    
    states = set()
    employer = nongroup = medicaid = medicare = military = uninsured = None

    for state in data:
        states.add(state['Location'])
        if state['Location'].lower() == location.lower():
            employer = state['Employer']
            nongroup = state['Non-Group']
            medicaid = state['Medicaid']
            medicare = state['Medicare']
            military = state['Military']
            uninsured = state['Uninsured']
            population = state ['Population']

    if employer is None:  # No matching state found
        return "State not found", 404

    return render_template('state.html', state=location, population=int(population), employer=float(employer), nongroup=float(nongroup), medicaid=float(medicaid), medicare=float(medicare), military=float(military), uninsured=float(uninsured), data=data, states=sorted(states))

def navbar():
    location = request.args.get('name')
    f = open("data/refined_data.json", "r")
    data = json.load(f)
    f.close()
    states=set()
    for state in data:
        states.add(state["Location"])
    return render_template('navbar.html', state=location, data=data, states=sorted(states))
    

if __name__ == '__main__':
    app.run(debug=True)
    