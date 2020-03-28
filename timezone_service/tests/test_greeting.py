from timezone_service.errors import InvalidRequestError
from timezone_service.greeting import GreetingClient
from timezone_service import VALID_REQUEST_REGEX

import pytest
import re
from unittest.mock import Mock


def create_client(json={}):
    attrs = {'data': bytes(str(json).encode('utf-8'))}
    mock_request = Mock(**attrs)

    client = GreetingClient(mock_request)

    return client


def test_add_timedelta():

    client = create_client()

    assert client.add_timedelta(6, 5) == 11 # Regular addition
    assert client.add_timedelta(1, 0) == 1 # No offset
    assert client.add_timedelta(0, -10) == 14 # Previous day
    assert client.add_timedelta(5, -5) == 0 # Equality 0
    assert client.add_timedelta(17, 10) == 3 # Next day


def test_determine_greeting():

    client = create_client()

    for hour in range(6, 13):
        assert client.determine_greeting(hour) == 'Good Morning!'

    for hour in range(13, 18):
        assert client.determine_greeting(hour) == 'Good Afternoon!'

    for hour in range(18, 21):
        assert client.determine_greeting(hour) == 'Good Evening!'

    for hour in range(0, 6):
        assert client.determine_greeting(hour) == 'Goodnight'

    for hour in range(21, 24):
        assert client.determine_greeting(hour) == 'Goodnight'


def test_request_dict_valid():
    client = create_client()

    assert client.check_request_dict({'timezone': 'GMT+3H'}) == 'GMT+3H'
    assert client.check_request_dict({'timezone': 'gibberish'}) == 'gibberish'


def test_request_dict_valid_whitespace():
    client = create_client()

    assert client.check_request_dict({'timezone': '  GMT+3H  '}) == 'GMT+3H'
    assert client.check_request_dict({'timezone': '   gibberish'}) == 'gibberish'
    assert client.check_request_dict({'timezone': 'test   '}) == 'test'


def test_request_dict_invalid():
    client = create_client()

    with pytest.raises(InvalidRequestError):
        client.check_request_dict({'timezone': ''})

    with pytest.raises(InvalidRequestError):
        client.check_request_dict({'timezone': None})


def test_check_request_form_valid():
    client = create_client()

    assert bool(client.check_request_form('GMT+3')) is True
    assert bool(client.check_request_form('gmt+3')) is True # lowercase
    assert bool(client.check_request_form('GMT+10')) is True
    assert bool(client.check_request_form('GMT-5')) is True
    assert bool(client.check_request_form('GMT-54')) is True
    assert bool(client.check_request_form('GMT-0')) is True


def test_check_request_form_invalid():
    client = create_client()

    with pytest.raises(InvalidRequestError):
        client.check_request_form('')

    with pytest.raises(InvalidRequestError):
        client.check_request_form('gmt++3')

    with pytest.raises(InvalidRequestError):
        client.check_request_form('GMT+200')

    with pytest.raises(InvalidRequestError):
        client.check_request_form('UTC-5')


def test_obtain_offset_from_match_obj_valid():
    client = create_client()

    match_obj = re.match(VALID_REQUEST_REGEX, 'GMT+7')
    assert client.obtain_offset_from_match_obj(match_obj) == 7

    match_obj = re.match(VALID_REQUEST_REGEX, 'GMT+0')
    assert client.obtain_offset_from_match_obj(match_obj) == 0


def test_obtain_offset_from_match_obj_invalid():
    client = create_client()

    match_obj = re.match(VALID_REQUEST_REGEX, 'GMT+13')

    with pytest.raises(InvalidRequestError):
        client.obtain_offset_from_match_obj(match_obj)



