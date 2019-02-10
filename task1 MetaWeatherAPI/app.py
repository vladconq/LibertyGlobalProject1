import asyncio
import logging
import sys
import psycopg2
from flask import Flask, jsonify, request

import weatherinfo

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

CITY = 'st petersburg'
app = Flask(__name__)


@app.route('/')
def home_page():
    """
    this function handles requests to the home page
    :return: json response
    """
    message = {
        'status': 200,
        'message': 'Welcome to MetaWeatherAPI!',
        'sample request': 'http://127.0.0.1:5000/weather/2019-01-02'
    }
    resp = jsonify(message)

    return resp


@app.errorhandler(404)
def page_not_found(error):
    """
    this function handles non-existing addresses
    :param error: code of error
    :return: json response
    """
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)

    return resp


@app.route('/weather/<selected_date>', methods=['GET'])
def get_weather(selected_date: str):
    """
    this function returns the weather for the specified date
    :param selected_date: desired date
    """
    conn = psycopg2.connect(weatherinfo.db_params)
    cur = conn.cursor()

    cur.execute('SELECT * FROM weather_info')
    colnames = [desc[0] for desc in cur.description]

    select_query = ("SELECT * FROM weather_info WHERE applicable_date='{}'").format(selected_date)
    cur.execute(select_query)

    message = []
    for row in cur.fetchall():
        message.append(dict(zip(colnames, row)))

    conn.commit()
    conn.close()

    resp = jsonify(message)
    return resp


if __name__ == '__main__':
    woeid = weatherinfo.get_woeid(CITY)
    logging.info('OK! Received woeid city.')

    dates = weatherinfo.get_dates()
    logging.info('OK! Received a list of dates for the last month.')

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(weatherinfo.run_weather_task(woeid, dates))
    weather_info = loop.run_until_complete(future)
    logging.info('OK! Received weather data for specified dates.')

    weatherinfo.fill_db(weather_info)
    logging.info('OK! Database successfully filled.')

    app.run(debug=True, use_reloader=False)
