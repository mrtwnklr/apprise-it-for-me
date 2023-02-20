import logging
import requests
import os
from flask import Flask, request, jsonify

import grafana

app = Flask(__name__)

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
APPRISE_URL = os.environ.get('APPRISE_URL')

logging.basicConfig(format='%(message)s', level=LOGLEVEL)
log = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health():
    return 'OK'

@app.route('/from_grafana/notify/<apprise_key>', methods=['POST'])
def notify(apprise_key):
    log.debug('request url: %s', request.url)

    apprise_data = grafana.get_apprise_data(request)
    log.debug('passing notification data: %s', apprise_data)

    apprise_request_url = '{}/{}/{}'.format(APPRISE_URL, 'notify', apprise_key)
    requests.post(apprise_request_url, data=apprise_data)

    return jsonify(apprise_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
