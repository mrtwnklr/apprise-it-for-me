import requests
from flask import current_app, abort, jsonify, request

from application.converter.converterloader import ConverterLoader

@current_app.route('/from_<source>/notify/<apprise_key>', methods=['POST'])
def notify(source, apprise_key):
    current_app.logger.debug('request url: %s', request.url)

    converter = ConverterLoader.load(source)
    try:
        apprise_data = converter.get_apprise_data(request)
    except Exception as exception:
        current_app.logger.error("Error applying converter: %s", exception)
        abort(500, description='Error applying converter for source: ' + source)

    current_app.logger.debug('passing notification data: %s', apprise_data)
    apprise_request_url = '{}/{}/{}'.format(current_app.config['APPRISE_URL'], 'notify', apprise_key)
    requests.post(apprise_request_url, data=apprise_data, params=request.args)

    return jsonify(apprise_data)
