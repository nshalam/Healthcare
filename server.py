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
        insured[state["Abbreviation"]]=float(state["Uninsured"])
    print(insured)
        
    return render_template('index.html', states=sorted(states), insured=insured, data=data)

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
    f = open("data/refined_data.json", "r")
    data = json.load(f)
    f.close()
    
    states = set()

    employer_avg = nongroup_avg = population_avg =medicare_avg =medicaid_avg =uninsured_avg = military_avg = float()
    employer = nongroup = medicaid = medicare = military = uninsured =population = float()

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

    employer_avg += float(state['Employer'])
    nongroup_avg += float(state['Non-Group'])
    medicaid_avg += float(state['Medicaid'])
    medicare_avg += float(state['Medicare'])
    military_avg += float(state['Military'])
    uninsured_avg += float(state['Uninsured'])
    population_avg += int(state['Population'])
            

    return render_template('state.html', state=location, population_avg=int(population_avg), population=int(population), employer=round(float(employer) * 100, 2),nongroup=round(float(nongroup) * 100, 2),medicaid=round(float(medicaid) * 100, 2),medicare=round(float(medicare) * 100, 2),military=round(float(military) * 100, 2),uninsured=round(float(uninsured) * 100, 2),employer_avg=round(float(employer_avg) * 100, 2),nongroup_avg=round(float(nongroup_avg) * 100, 2),medicaid_avg=round(float(medicaid_avg) * 100, 2),medicare_avg=round(float(medicare_avg) * 100, 2),military_avg=round(float(military_avg) * 100, 2),uninsured_avg=round(float(uninsured_avg) * 100, 2),data=data, states=sorted(states))

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