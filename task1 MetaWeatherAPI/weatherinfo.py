import asyncio
import datetime
import psycopg2
import requests
from calendar import monthrange
from aiohttp import ClientSession

db_params = """
    dbname = 'metaweather'
    user = 'user'
    password = 'password'
    host = 'localhost'
"""


def get_woeid(city: str) -> int:
    """
    this function determines the woeid of the specified city
    :param city: the city for which the woeid is defined
    :return: woeid for specified city
    """
    url = 'https://www.metaweather.com/api/location/search/?query={}'.format(city)
    response = requests.get(url).json()
    woeid = int(response[0]['woeid'])

    return woeid


def get_dates() -> list:
    """
    this function allows to determine the corresponding dates for the last month
    :return: list with dates
    """
    dates = []
    first_day_of_current_month = datetime.date.today().replace(day=1)
    last_month = (first_day_of_current_month - datetime.timedelta(days=1)).month
    last_year = (first_day_of_current_month - datetime.timedelta(days=1)).year
    number_of_days_in_month = monthrange(last_year, last_month)[1]

    for day in range(1, number_of_days_in_month + 1):
        date = '{}/{}/{}'.format(last_year, last_month, day)
        dates.append(date)

    return dates


async def fetch_weather_info(url: str, session: ClientSession):
    """
    this function gets the page content
    :param url: the address of the desired page
    :param session: current open session to connect
    :return: page content
    """
    async with session.get(url) as response:
        return await response.json()


async def run_weather_task(woeid: int, dates: list) -> list:
    """
    this function creates tasks for viewing specified addresses
    :param woeid: woeid for specified city
    :param dates: list with dates
    :return: page content
    """
    url = 'https://www.metaweather.com/api/location/{}/{}'
    tasks = []

    # Fetch all responses
    async with ClientSession() as session:
        for date in dates:
            task = asyncio.ensure_future(fetch_weather_info(url.format(woeid, date), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

    # Expand nested list
    weather_info = []
    flat_list = [item for sublist in responses for item in sublist]

    for item in flat_list:
        time_info = [tuple(item.values()) for _ in flat_list]  # make tuple from dict values
        weather_info.append(time_info[0])

    return weather_info


def fill_db(weather_info: list):
    """
    this function fills the database with content from the received pages.
    :param weather_info: page content
    """
    conn = psycopg2.connect(db_params)
    cur = conn.cursor()

    records_list_template = ','.join(['%s'] * len(weather_info))
    insert_query = 'INSERT INTO weather_info VALUES {}'.format(records_list_template)
    try:
        cur.execute(insert_query, weather_info)
    except psycopg2.IntegrityError:
        pass  # Database is full, do not need to do anything

    conn.commit()
    conn.close()
