from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import Controller
import logging
from opentelemetry import metrics
from opentelemetry.ext.otcollector.metrics_exporter import (
    CollectorMetricsExporter,
)
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.metrics.export.controller import PushController

application = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
application.logger.handlers = gunicorn_logger.handlers
controller = Controller(application.logger)
application.config['CORS_HEADERS'] = 'Content-Type'

# Meter is responsible for creating and recording metrics
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)
# exporter to export metrics to Prometheus
prefix = "Covid19County"

# create a CollectorMetricsExporter

exporter = CollectorMetricsExporter(
    service_name="covid19_county_backend", endpoint="host.docker.internal:55678"
)

# controller collects metrics created from meter and exports it via the
# exporter every interval
telemetryController = PushController(meter, exporter, 5)


request_counter = meter.create_metric(
    name="requests",
    description="number of requests",
    unit="1",
    value_type=int,
    metric_type=Counter,
)


def state_county_labels(): return {
    'state': request.view_args['state'], 'county': request.view_args['county']}


@application.route('/<state>/<county>/cases')
def state_county_cases(state, county):
    request_counter.add(1, state_county_labels())
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.state_county_cases(state_upper, county_upper))


@application.route('/<state>/all/cases')
def state_cases(state):
    request_counter.add(1, state_county_labels())
    state_upper = state.upper()
    return jsonify(controller.state_cases(state_upper))


@application.route('/<state>/<county>/bed_capacity')
def state_county_bed_capacity(state, county):
    request_counter.add(1, state_county_labels())
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.state_county_bed_capacity(state_upper, county_upper))


@application.route('/<state>/all/bed_capacity')
def state_bed_capacity(state):
    request_counter.add(1, state_county_labels())
    state_upper = state.upper()
    return jsonify(controller.state_bed_capacity(state_upper))


@application.route('/<state>/<county>/deaths')
def state_county_deaths(state, county):
    request_counter.add(1, state_county_labels())
    if not county:
        return jsonify([])
    state_upper = state.upper()
    county_upper = county.upper()
    return jsonify(controller.state_county_deaths(state_upper, county_upper))


@application.route('/<state>/all/deaths')
def state_deaths(state):
    request_counter.add(1, state_county_labels())
    state_upper = state.upper()
    return jsonify(controller.state_deaths(state_upper))


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


if __name__ == '__main__':
    application.run(host='0.0.0.0:8080')
