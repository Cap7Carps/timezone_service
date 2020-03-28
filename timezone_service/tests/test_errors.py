from timezone_service.errors import InvalidRequestError


def test_valid_message_thrown():
    request_json = '{test: test}'
    expected_message = f'''Invalid Request: `{request_json}`, should be of form: `GMT±Hours` with 0 <= hours < 12'''
    error_message = str(InvalidRequestError(request_json))

    assert error_message == expected_message


