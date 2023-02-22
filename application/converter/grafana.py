from flask import current_app


class GrafanaConverter:
    STATUS_TYPE_MAPPING = {"firing": "failure", "resolved": "success"}

    def get_apprise_type(self, status):
        return self.STATUS_TYPE_MAPPING.get(status.lower(), status)

    # Apprise: supported fields are:
    #            body, title, notification_type, tag and format
    #          see https://github.com/caronc/apprise-api#api-details
    # Grafana: see https://grafana.com/docs/grafana/latest/alerting/manage-notifications/webhook-notifier/ # noqa: E501
    def get_apprise_data(self, request):
        request_data = request.json
        current_app.logger.debug("request data: %s", request_data)

        apprise_data = {}
        apprise_data["body"] = request_data.get("message", "")
        apprise_data["title"] = request_data.get("title", "")
        apprise_data["notification_type"] = request_data.get("status", "")

        # copy following commonLabels to apprise_data when specified:
        #   tag, format, notification_type and title
        commonLabels = request_data.get("commonLabels")
        if commonLabels:
            for param_name in ["tag", "format", "notification_type", "title"]:
                param_value = commonLabels.get(param_name)
                if param_value:
                    apprise_data[param_name] = param_value

        # try to convert resulting notification_type or leave it as-is
        if apprise_data["notification_type"] in self.STATUS_TYPE_MAPPING:
            apprise_data["notification_type"] = self.get_apprise_type(
                apprise_data["notification_type"]
            )

        return apprise_data
