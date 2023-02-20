import logging
import requests
import os
from flask import abort, Flask, jsonify, request

from converterloader import ConverterLoader

app = Flask(__name__)

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
APPRISE_URL = os.environ.get('APPRISE_URL')

logging.basicConfig(format='%(message)s', level=LOGLEVEL)
log = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health():
    return 'OK'

@app.route('/from_<source>/notify/<apprise_key>', methods=['POST'])
def notify(source, apprise_key):
    log.debug('request url: %s', request.url)

    converter = ConverterLoader.load(source)
    try:
        apprise_data = converter.get_apprise_data(request)
    except Exception as exception:
        current_app.logger.error("Error applying converter: %s", exception)
        abort(500, description='Error applying converter for source: ' + source)

    log.debug('passing notification data: %s', apprise_data)
    apprise_request_url = '{}/{}/{}'.format(APPRISE_URL, 'notify', apprise_key)
    requests.post(apprise_request_url, data=apprise_data, params=request.args)

    return jsonify(apprise_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
