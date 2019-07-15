"""Make sure to install requests before running."""


import datetime
import heapq
import model
import os
import requests
import typing


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

    heap_list: typing.List['model.Location'] = list()
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
        for resp in response:
            heapq.heappush(
                heap_list, model.Location(name=resp.get('applicant', ''),
                                          location=resp.get('location', '')))
        offset += 10
        if len(response) < 10:
            break
        continue_command = input(
            'Would you like to continue? Enter Y to continue, and N to abort? ')
        if continue_command != 'Y':
            break
    return heap_list


if __name__ == '__main__':
    heap_list = get_mobile_foods()
    for heap in heap_list:
        print(heap)
