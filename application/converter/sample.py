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
