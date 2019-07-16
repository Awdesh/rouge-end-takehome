import asyncio
import json
import os
import pytest
import show_open_food_trucks
from unittest import mock


@pytest.fixture(scope='module')
def json_object():
    json_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'test_response.json')
    with open(json_path) as jf_object:
        return json.load(jf_object)


@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@mock.patch('os.environ.get', return_value='app-token')
def test_get_mobile_food_locations__success(mock_token, json_object,
                                            event_loop):
    """Verifies that objects arre displayed."""
    mock_response_object = mock.Mock()
    mock_response_object.status_code = 200
    mock_response_object.json = mock.MagicMock(return_value=json_object)

    with mock.patch('requests.get',
                    return_value=mock_response_object) as mock_request_object, \
            mock.patch(
                'show_open_food_trucks.display') as mock_display_function, \
            mock.patch('builtins.input',
                       side_effect=lambda *args: 'N') as mock_input_function:

        event_loop.run_until_complete(
                show_open_food_trucks.get_mobile_food_locations())

        assert mock_request_object.call_count == 1
        args, kwargs = mock_request_object.call_args_list[0]
        assert args[0] == show_open_food_trucks.URL
        assert kwargs['headers'] == {'X-App-Token': 'app-token'}
        assert 'params' in kwargs
        # Asserts that objects are displayed.
        assert mock_display_function.call_count == 1
        assert mock_input_function.call_count == 1
        assert (mock_input_function.call_args[0][0] ==
                ('Would you like to continue? Enter Y to continue, and N '
                 'to abort :'))


@mock.patch('os.environ.get', return_value='app-token')
def test_get_mobile_food_locations__failure(mock_token, json_object,
                                            event_loop):
    """Verifies that objects arre displayed."""
    mock_response_object = mock.Mock()
    # Response is not a 200
    mock_response_object.status_code = 500
    mock_response_object.json = mock.MagicMock(return_value=json_object)

    with mock.patch('requests.get',
                    return_value=mock_response_object) as mock_request_object, \
            mock.patch(
                'show_open_food_trucks.display') as mock_display_function:
        event_loop.run_until_complete(
            show_open_food_trucks.get_mobile_food_locations())
        assert mock_request_object.call_count == 1
        args, kwargs = mock_request_object.call_args_list[0]
        assert args[0] == show_open_food_trucks.URL
        assert kwargs['headers'] == {'X-App-Token': 'app-token'}
        assert 'params' in kwargs
        # Display not called
        assert mock_display_function.call_count == 0


@mock.patch('os.environ.get', return_value=None)
def test_get_mobile_food_locations__no_app_token(mock_token, json_object,
                                                 event_loop):
    """Verifies that objects arre displayed."""
    mock_response_object = mock.Mock()
    # Response is not a 200
    mock_response_object.status_code = 200
    mock_response_object.json = mock.MagicMock(return_value=json_object)

    with mock.patch('requests.get',
                    return_value=mock_response_object) as mock_request_object, \
            mock.patch(
                'show_open_food_trucks.display') as mock_display_function, \
            mock.patch('builtins.input',
                       side_effect=lambda *args: 'N') as mock_input_function:
        event_loop.run_until_complete(
            show_open_food_trucks.get_mobile_food_locations())

        # Assertions
        assert mock_request_object.call_count == 1
        args, kwargs = mock_request_object.call_args_list[0]
        assert args[0] == show_open_food_trucks.URL
        assert 'headers' not in kwargs
        assert 'params' in kwargs
        # Asserts that objects are displayed.
        assert mock_display_function.call_count == 1
        assert mock_input_function.call_count == 1
        assert (mock_input_function.call_args[0][0] ==
                ('Would you like to continue? Enter Y to continue, and N '
                 'to abort :'))


@mock.patch('os.environ.get', return_value='app-token')
def test_get_mobile_food_locations__fewer_than_ten_results(mock_token,
                                                           json_object,
                                                           event_loop):
    """Verifies that objects arre displayed."""
    mock_response_object = mock.Mock()
    # Response is not a 200
    mock_response_object.status_code = 200
    mock_response_object.json = mock.MagicMock(return_value=json_object[:5])

    with mock.patch('requests.get',
                    return_value=mock_response_object) as mock_request_object, \
            mock.patch(
                'show_open_food_trucks.display') as mock_display_function, \
            mock.patch('builtins.input',
                       side_effect=lambda *args: 'N') as mock_input_function:
        event_loop.run_until_complete(
            show_open_food_trucks.get_mobile_food_locations())

        # Assertions
        assert mock_request_object.call_count == 1
        args, kwargs = mock_request_object.call_args_list[0]
        assert args[0] == show_open_food_trucks.URL
        assert 'headers' in kwargs
        assert 'params' in kwargs
        # Asserts that objects are displayed.
        assert mock_display_function.call_count == 1
        # Command line input is not called because the fewer than 10 results are
        # returned.
        assert mock_input_function.call_count == 0
