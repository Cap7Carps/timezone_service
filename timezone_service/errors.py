
class InvalidRequestError(Exception):

    def __init__(self, request_json):
        self.request_json = request_json

    def __str__(self):
        req = str(self.request_json)
        message = f'''Invalid Request: `{req}`, should be of form: `GMT±Hours` with 0 <= hours < 12'''
        return message

