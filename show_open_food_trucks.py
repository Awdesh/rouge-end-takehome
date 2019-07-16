"""Entry point to show the food resources."""


import asyncio
import datetime
import logging
import operator
import os
import requests
import typing

from logging import config

config.fileConfig('logging.conf')
logger = logging.getLogger('root')


URL = 'https://data.sfgov.org/resource/jjew-r69b.json'
MAX_LIMIT = 10
Location = typing.Tuple[str, str]


async def get_mobile_food_locations():
    """
    Fetches the mobile food locations MAX_LIMIT elements at a time.
    """
    offset: int = 0
    app_token: str = os.environ.get('SODA_APP_TOKEN')
    now: 'datetime.datetime' = datetime.datetime.now()
    day_of_week: str = now.strftime('%A')
    time_tuple = now.timetuple()
    time_string: str = '{hour}:{minute}'.format(hour=time_tuple.tm_hour,
                                                minute=time_tuple.tm_min)

    while True:
        logging.info('Fetching {} records at an offset of {}'.format(MAX_LIMIT,
                                                                     offset))
        params: dict = {'$limit': MAX_LIMIT, '$offset': offset,
                        '$where': ('start24 <= "{}" '
                                   'AND end24 > "{}"'.format(time_string,
                                                             time_string)),
                        'dayofweekstr': '{day}'.format(day=day_of_week)}

        if app_token:
            r = requests.get(URL, headers={'X-App-Token': app_token},
                             params=params)
        else:
            r = requests.get(URL, params=params)
        if r.status_code != 200:
            break

        response: dict = r.json()
        if not response:
            logging.info('Exiting as no records were found.')
            break
        heap_list: typing.List[Location] = list()
        for resp in response:
            heap_list.append((resp.get('applicant', ''),
                              resp.get('location', '')))

        display(sorted(heap_list, key=operator.itemgetter(0)))
        offset += MAX_LIMIT
        continue_command = input(
            'Would you like to continue? Enter Y to continue, and N to abort :')
        if continue_command != 'Y' or continue_command == 'N':
            logging.info('Request aborted. Exiting the program immediately.')
            break


def display(locations: typing.List[Location]):
    """
    Displays the list of tuple of strings in which each tuple consists of a name
    and location.

    Args:
        locations: list of tuples
    """
    print('Name      Address')
    for loc in locations:
        print('{name}    {location}'.format(name=loc[0], location=loc[1]))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(get_mobile_food_locations())
    finally:
        loop.close()
