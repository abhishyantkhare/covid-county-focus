from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from controller import Controller
import logging


application = Flask(__name__)
cors = CORS(application)
gunicorn_logger = logging.getLogger('gunicorn.error')
application.logger.handlers = gunicorn_logger.handlers
controller = Controller(application.logger)
application.config['CORS_HEADERS'] = 'Content-Type'


@application.route('/<state>/<county>/cases')
def state_county_cases(state, county):
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.state_county_cases(state_upper, county_upper))


@application.route('/<state>/all/cases')
def state_cases(state):
    state_upper = state.upper()
    return jsonify(controller.state_cases(state_upper))


@application.route('/<state>/<county>/bed_capacity')
def state_county_bed_capacity(state, county):
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.state_county_bed_capacity(state_upper, county_upper))


@application.route('/<state>/<county>/deaths')
def state_county_deaths(state, county):
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.state_county_deaths(state_upper, county_upper))


@application.route('/<state>/counties')
def counties(state):
    state_upper = state.upper()
    return jsonify(controller.counties(state_upper))


@application.route('/states')
def states():
    return jsonify(controller.get_states_formatted())


@application.route('/<state>/<county>/case_projections')
def case_projections(state, county):
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.case_projections(state_upper, county_upper))


if __name__ == "__main__":
    application.run(host='0.0.0.0:8080')
