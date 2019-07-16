"""Entry point to show the food resources."""


import datetime
import heapq
import logging
import os
import requests
import typing

from logging import config

config.fileConfig('logging.conf')
logger = logging.getLogger('root')


URL = 'https://data.sfgov.org/resource/jjew-r69b.json'


def get_mobile_foods() -> typing.List['model.Location']:
    """Fetches the mobile food locations 10 elements at a time.

    Returns a sorted list by name
    """
    offset: int = 0
    app_token: str = os.environ.get('SODA_APP_TOKEN')
    now: 'datetime.datetime' = datetime.datetime.now()
    day_of_week: str = now.strftime('%A')
    time_tuple = now.timetuple()
    time_string: str = '{hour}:{minute}'.format(hour=time_tuple.tm_hour,
                                                minute=time_tuple.tm_min)

    while True:
        r = None
        params: dict = {'$limit': 10, '$offset': offset,
                        '$where': ('start24 <= "{}" AND end24 > '
                                   '"{}"'.format(time_string, time_string)),
                        'dayofweekstr': '{day}'.format(day=day_of_week)}

        if app_token:
            r = requests.get(URL, headers={'X-App-Token': app_token},
                             params=params)
        else:
            r = requests.get(URL, params=params)
        if r.status_code != 200:
            break

        response = r.json()
        heap_list: typing.List[typing.Tuple(str, str)] = list()
        for resp in response:
            heapq.heappush(heap_list, (resp.get('applicant', ''),
                                       resp.get('location', '')))

        display(sorted(heap_list))
        offset += 10
        if len(response) < 10:
            break
        continue_command = input(
            'Would you like to continue? Enter Y to continue, and N to abort :')
        if continue_command != 'Y' or continue_command == 'N':
            break


def display(locations: typing.List['model.Location']):
    print('Name      Location')
    for loc in locations:
        print('{name}    {location}'.format(name=loc[0], location=loc[1]))


def display_locations():
    heap_list = get_mobile_foods()
    if not heap_list:
        return
    display(heap_list)
    print('#####')
    for sorted_location in sorted(heap_list):
        print(sorted_location)


if __name__ == '__main__':
    display_locations()
