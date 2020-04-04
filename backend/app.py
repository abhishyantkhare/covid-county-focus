from flask import Flask, jsonify
from controller import Controller

app = Flask(__name__)
controller = Controller()


@app.route('/<state>/<county>/cases')
def cases(state, county):
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.cases(state_upper, county_upper))


@app.route('/<state>/<county>/bed_capacity')
def bed_capacity(state, county):
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.bed_capacity(state_upper, county_upper))


@app.route('/<state>/<county>/deaths')
def deaths(state, county):
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.deaths(state_upper, county_upper))


@app.route('/<state>/counties')
def counties(state):
    state_upper = state.upper()
    return jsonify(controller.counties(state_upper))


@app.route('/states')
def states():
    return jsonify(controller.get_states_formatted())
