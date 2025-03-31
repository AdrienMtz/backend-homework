import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 

@app.route('/api/alive')
def alive():
    if request.method == 'GET' :
        return jsonify({'text':'Alive', 'status_code' : 200})
    else :
        return jsonify({'text':'Méthode non autorisée', 'status_code' : 405})

@app.route('/api/associations')
def associations():
    if request.method == 'GET' :
        ids = associations_df['id'].to_list()
        return jsonify({'content':ids, 'status_code' : 200})
    else :
        return jsonify({'text':'Méthode non autorisée', 'status_code' : 405})

@app.route('/api/association/<int:id>')
def detail_asso(id : 'str'):
    if request.method == 'GET' :
        if id in associations_df['id'].to_list() :
            detail = associations_df.loc[id, 'description']
            return jsonify({'content' : detail, 'status_code' : 200})
        else :
            return jsonify({'error' : 'Association not found', 'status_code':404})
    else :
        return jsonify({'text':'Méthode non autorisée', 'status_code' : 405})

@app.route('/api/evenements')
def evenements()
    if request.method == 'GET' :
        events = evenements_df['nom'].to_list()
        return jsonify({'content':events, 'status_code' : 200})
    else :
        return jsonify({'text':'Méthode non autorisée', 'status_code' : 405})

@app.route('/api/evenement/<int:id>')
def detail_event(id : 'str'):
    if request.method == 'GET' :
        if id in evenements_df['id'].to_list() :
            detail = evenements_df.loc[id, 'description']
            return jsonify({'content' : detail, 'status_code' : 200})
        else :
            return jsonify({'error' : 'Event not found', 'status_code':404})
    else :
        return jsonify({'text':'Méthode non autorisée', 'status_code' : 405})

@app.route('/api/association/<int:id>/evenements')
def events_asso(id : 'str'):
    if request.method == 'GET' :
        if id in associations_df['id'].to_list() :
            events = evenements_df[evenements_df['association_id'] == id]['nom'].to_list()
            return jsonify({'content' : events, 'status_code' : 200})
        else :
            return jsonify({'error' : 'Association not found', 'status_code':404})
    else :
        return jsonify({'text':'Méthode non autorisée', 'status_code' : 405})

@app.route('/api/associations/type/<type>')
def detail(type : 'str'):
    if request.method == 'GET' :
        liste_type = associations_df[associations_df['type'] == type]['nom']
        return jsonify({'content' : liste_type, 'status_code' : 200})
    else :
        return jsonify({'text':'Méthode non autorisée', 'status_code' : 405})


if __name__ == '__main__':
    app.run(debug=False)

