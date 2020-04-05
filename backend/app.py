from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from controller import Controller

application = Flask(__name__)
cors = CORS(application)
controller = Controller()
application.config['CORS_HEADERS'] = 'Content-Type'


@application.route('/<state>/<county>/cases')
def cases(state, county):
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.cases(state_upper, county_upper))


@application.route('/<state>/<county>/bed_capacity')
def bed_capacity(state, county):
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.bed_capacity(state_upper, county_upper))


@application.route('/<state>/<county>/deaths')
def deaths(state, county):
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.deaths(state_upper, county_upper))


@application.route('/<state>/counties')
def counties(state):
    state_upper = state.upper()
    return jsonify(controller.counties(state_upper))


@application.route('/states')
def states():
    return jsonify(controller.get_states_formatted())


if __name__ == "__main__":
    application.run(host='0.0.0.0:8080')
