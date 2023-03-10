# 🌬 apprise-it-for-me

... is a gateway for [Apprise](https://github.com/caronc/apprise):

`apprise-it-for-me` accepts HTTP POST data, transforms it into an Apprise notification payload and sends it to an [Apprise API server](https://github.com/caronc/apprise-api/).

[Apprise](https://github.com/caronc/apprise):
> allows you to send a notification to almost all of the most popular notification services available to us today such as: Telegram, Discord, Slack, Amazon SNS, Gotify, etc.

[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)
[![build](https://github.com/mrtwnklr/apprise-it-for-me/actions/workflows/build.yaml/badge.svg)](https://github.com/mrtwnklr/apprise-it-for-me)

## Table of content

- [Table of content](#table-of-content)
- [Rationale](#rationale)
- [Deployment](#deployment)
- [Usage](#usage)
  - [Common](#common)
  - [Configuration for Grafana](#configuration-for-grafana)
- [Development](#development)
  - [Variant 1: execute with Python on development host](#variant-1-execute-with-python-on-development-host)
  - [Variant 2: execute inside Docker container](#variant-2-execute-inside-docker-container)
  - [Add support for another application](#add-support-for-another-application)
  - [And last but not least](#and-last-but-not-least)

## Rationale

Many applications realize notifications via generic webhooks among others.
Some of them allow the user to configure the data structure of the webhook request.
Others don't.

Apprise, on the other hand, expects a predefined data structure.

`apprise-it-for-me` can provide application specific webhooks, convert the incoming request data and forward it to Apprise.

## Deployment

The preferred deployment method is to use the provided docker image [`mrtwnklr/apprise-it-for-me`](https://hub.docker.com/r/mrtwnklr/apprise-it-for-me/).

Execute it with the docker cli:

```bash
# specify Apprise url
# and optionally mount a custom converter into converter subdirectory
docker run --name apprise-it-for-me \
   -p 8001:8001 \
   -e APPRISE_URL=http://apprise.local:8000 \
   -v ./customconverter.py:/apprise-it-for-me/application/converter/customconverter.py:ro \
   -d mrtwnklr/apprise-it-for-me:latest
```

or via `docker-compose.yaml`:

```yaml
---
services:
  apprise-it-for-me:
    container_name: apprise-it-for-me
    image: mrtwnklr/apprise-it-for-me:latest
    environment:
      - APPRISE_URL=http://apprise.local:8000
    ports:
      - 8001:8001
    volumes:
      # mount your custom converter into container
      - ./customconverter.py:/apprise-it-for-me/application/converter/customconverter.py:ro
```

Or take a look at [`./docker-compose.yaml`](docker-compose.yaml) for building and running the container from source.

## Usage

Application support is currently limited to [Grafana](https://github.com/grafana/grafana).
**But extension is easy, [see below](#add-support-for-another-application)!**

### Common

1. Typically `apprise-it-for-me` is configured as generic webhook.
   The webhook url follows this pattern:

   > <http://`{APPRISE-IT-FOR-ME-SERVER}`:8001/from_`{APPLICATION}`/notify/`{APPRISE-KEY}`>

   e.g.: <http://metrics.local:8001/from_grafana/notify/to-ntfy>

2. Any query string is forwarded as-is to Apprise.
   This allows to specify `tag`, `title`, `format` and `type` when not already contained in the incoming request data.
   For details see [apprise-api #84](https://github.com/caronc/apprise-api/pull/84).

### Configuration for Grafana

**Example:** webhook configuration with Apprise configuration key `to-matrix`:

![Grafana webhook configuration](media/grafana.png)

**Mapping logic:**

Some fields in the Apprise notification payload are copied from the Grafana main request body.
Other fields can only be set by providing them as alert labels (see [`commonLabels` webhook fields](https://grafana.com/docs/grafana/latest/alerting/manage-notifications/webhook-notifier/)).

|Apprise field     |from Grafana field |override with `commonLabels`
|-                 |-                  |-
|body              |message            |-
|title             |title              |title
|notification_type |status             |notification_type
|format            |-                  |format
|tag               |-                  |tag

Details see [`./application/converter/grafana.py`](application/converter/grafana.py).

## Development

### Variant 1: execute with Python on development host

1. To prepare your development environment execute the following make target.
   It initializes a Python virtualenv, installs dependencies and further development tools.
   It requires Python to be already installed.

   ```bash
   make dev-install-virtualenv
   ```

2. To adjust configuration variables copy [`.env.sample`](.env.sample) to `.env` and modify it.

3. To run the development server execute the following make target:

   ```bash
   make dev-run
   ```

### Variant 2: execute inside Docker container

1. If you do not want to prepare/use a Python development environment
   you can execute your local development state in a Docker container.
   To do so execute the following make target:

   ```bash
   make dev-run-docker-compose
   ```

### Add support for another application

To support another application you need to implement the mapping from the original notification request to the Apprise notification body.

This mapping logic must be placed in a dedicated Python module under [`./application/converter/`](application/converter/).

See [`./application/converter/sample.py`](application/converter/sample.py) for a minimal sample:

```python
from flask import current_app


class SampleConverter:
    # Apprise: supported fields are:
    #            body, title, notification_type, tag und format
    #          see https://github.com/caronc/apprise-api#api-details
    def get_apprise_data(self, request):
        # load application specific request data
        request_data = request.json
        current_app.logger.debug("request data: %s", request_data)

        # fill Apprise fields from application specific request data
        apprise_data = {}
        apprise_data["body"] = request_data.get("the_body", "")
        apprise_data["title"] = request_data.get("the_title", "")
        apprise_data["notification_type"] = request_data.get("the_type", "")
        apprise_data["tag"] = request_data.get("the_tag", "")
        apprise_data["format"] = request_data.get("the_format", "")

        # return Apprise notification data
        return apprise_data
```

**Specification:**

- The module must have an unique name.
  This name will be used as `{APPLICATION}` field in the api url ([see above](#common)).
- The module must define a class.
- The class name must be built from the module name and the suffix `Converter`.
  The first character must be upper case.
- The class must define a method named `get_apprise_data`.
- The method must accept a [Flask request](https://flask.palletsprojects.com/en/2.2.x/api/#incoming-request-data) object.
  Typically, the method would consume [`request.data`](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Request.get_data) or [`request.json`](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Request.get_json).
- The method must return a filled Apprise POST request body (see [apprise-api details](https://github.com/caronc/apprise-api#api-details)).

### And last but not least

Don't forget to create a pull request! 😊
