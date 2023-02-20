#! /bin/bash

APPRISE_SERVER=${1:-localhost}
APPRISE_GATEWAY_PORT=${2:-8001}

# simple health check
curl -X GET \
      "http://${APPRISE_SERVER}:${APPRISE_GATEWAY_PORT}/health"

# default request from source 'grafana' and apprise key 'config-key':
curl -X POST -H "Content-Type: application/json" \
      -d "@grafana-request.json" \
      "http://${APPRISE_SERVER}:${APPRISE_GATEWAY_PORT}/from_grafana/notify/config-key"

# request from source 'grafana' and apprise key 'config-key'
# -> override tag and type with grafana commonLabels:
curl -X POST -H "Content-Type: application/json" \
      -d "@grafana-request-with-common-labels.json" \
      "http://${APPRISE_SERVER}:${APPRISE_GATEWAY_PORT}/from_grafana/notify/config-key"
