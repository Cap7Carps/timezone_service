from timezone_service import VALID_REQUEST_REGEX

from timezone_service.errors import InvalidRequestError

import time
import json
import os
import re

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
CONF_FILEPATH = os.path.join(MODULE_PATH, 'conf', 'timezones.json')


class GreetingClient:

    def __init__(self, request):
        self.request = request
        self.request_json = json.loads(request.data.decode('utf-8'))

    def run(self):

        offset_from_gmt = self.validate_request()
        current_gmt_hour = self.get_current_hour()
        hour_desired_timezone = self.add_timedelta(current_gmt_hour, offset_from_gmt)
        greeting = self.determine_greeting(hour_desired_timezone)

        return greeting

    @staticmethod
    def get_current_hour():
        current_gmt_time = time.gmtime()
        current_gmt_hour = current_gmt_time.tm_hour

        return current_gmt_hour

    @staticmethod
    def add_timedelta(current_gmt_hour, offset_from_gmt):
        """
        :param current_gmt_hour: Current Hour in GMT
        :param offset_from_gmt: Hours to add/subtract from GMT
        :return: The hour of day at the target timezone
        """
        return (current_gmt_hour + offset_from_gmt) % 24

    @staticmethod
    def determine_greeting(hour_of_day):
        morning_hours = range(6, 13) # 6:00 - 12:59
        afternoon_hours = range(13, 18) # 13:00p - 17:59
        evening_hours = range(18, 21) # 18:00 - 20:59

        if hour_of_day in morning_hours:
            return 'Good Morning!'
        elif hour_of_day in afternoon_hours:
            return 'Good Afternoon!'
        elif hour_of_day in evening_hours:
            return 'Good Evening!'
        else:
            return 'Goodnight'

    def validate_request(self):
        """
        We expect data in the form {"timezone": "GMT±[\d]"}
        :returns: Offset from GMT
        :raises: RunTimeException
        """

        timezone = self.check_request_dict(self.request_json)
        match_obj = self.check_request_form(timezone)
        offset_from_gmt = self.obtain_offset_from_match_obj(match_obj)

        return offset_from_gmt

    def check_request_dict(self, request_json):
        timezone = request_json.get('timezone')
        if timezone:
            timezone = timezone.strip()
            return timezone

        raise InvalidRequestError(self.request_json)

    def check_request_form(self, timezone):
        """
        :param timezone: Value input by user
        :return: Regex Match Object
        """
        match_obj = re.match(VALID_REQUEST_REGEX, timezone, re.IGNORECASE)
        if match_obj:
            return match_obj

        raise InvalidRequestError(self.request_json)

    def obtain_offset_from_match_obj(self, match_obj):
        digits = match_obj.group(1)
        if abs(int(digits)) < 12:
            return int(digits)

        raise InvalidRequestError(self.request_json)
