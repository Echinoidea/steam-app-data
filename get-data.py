"""
Title : Steam App Data Collection and Analysis
Author: Gabriel Hooks
Date  : 2021-07-19

GOAL:
    Collect top n titles from x category on the Steam store, gather data on each game and add to
    data base and/or excel.
    Check if a game is indie or not.
    Do statistical analysis on reviews.

Use SteamFront API and SteamSpy
Add comments.
Come to statistical conclusions and compare to my manual data collection and analysis.
"""

# standard library imports
import csv
import datetime as dt
import json
import os
import statistics
import time
from stopwatch import Stopwatch

# third-party imports
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

# customisations - ensure tables show all columns
pd.set_option("max_columns", 100)


def get_request(url, parameters=None):
    """
    Return json-formatted response of a get request using optional parameters.

    This function was created by nik-davis on GitHub
    https://github.com/nik-davis/steam-data-science-project

    :param url: url to request from.
    :type url: str
    :param parameters: parameters to pass as part of get request
    :type parameters: dict
    :return: JSON-formatted response (dict-like)
    """

    try:
        response = requests.get(url=url, params=parameters)
    except requests.exceptions.SSLError as s:
        print('SSL Error:', s)

        for i in range(5, 0, -1):
            print('\rWaiting... ({})'.format(i), end='')
            time.sleep(1)
        print('\rRetrying.' + ' ' * 10)

        # recursively try again
        return get_request(url, parameters)
    except Exception as e:
        print(f"Something went wrong {e.args}")

        for i in range(5, 0, -1):
            print('\rWaiting... ({})'.format(i), end='')
            time.sleep(1)
        print('\rRetrying.' + ' ' * 10)

        # recursively try again
        return get_request(url, parameters)

    if response:
        return response.json()
    else:
        # response is none usually means too many requests. Wait and try again
        print('No response, waiting 10 seconds...')
        time.sleep(10)
        print('Retrying.')
        return get_request(url, parameters)


def get_specific_app_id(app_name):
    """
    Return specific app ID based on an app name.

    :param app_name: The name of the Steam app.
    :type app_name: str
    :return: App ID for the given app name.
    """

    response = requests.get(url=f'https://store.steampowered.com/search/?term={app_name}&category1=998',
                            headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    app_id = soup.find(class_='search_result_row')['data-ds-appid']
    return app_id


def get_top_n_app_ids(n=100, search_filter="", sort_by="", publisher_filter='a', minimum_reviews=0):
    """
    Get the top 'n' app IDs from Steam Store.


    :param n: Number of titles to get IDs from.
    :param search_filter: Which filter to sort by. [topsellers, popularnew, etc.] Not to be confused with 'category'
     URL parameter. If left blank, it will not filter results (all Steam apps).
    :param sort_by: How to sort the resulting apps. [Released_DESC, Name_ASC, Price_ASC, Price_DESC, Reviews_DESC]. If
    left blank, it will sort by Relevance.
    :param publisher_filter: 'a' - all (both indie and non-indie), 'i' - indie only, or 'p' - publisher only. Throws
    exception if argument is anything else. Not case sensitive.
    :type publisher_filter: str
    :param minimum_reviews: The minimum number of reviews necessary for the app to be added to the data.
    :type minimum_reviews: int
    :return: List of app IDs with length of 'n'
    """

    app_ids = []

    # category1=998 means it returns only games
    url = f"https://store.steampowered.com/search/?ignore_preferences=1&sort_by={sort_by}&category1=998filter={search_filter}&page="
    page = 1

    steam_spy_url = "https://steamspy.com/api.php?request=appdetails&appid="

    skip_counter = 0

    while len(app_ids) < n:
        response = requests.get(url=url+str(page), headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"URL: {response.url}")

        for row in soup.find_all(class_='search_result_row'):
            print(steam_spy_url + str(row['data-ds-appid']))
            steam_spy_data = get_request(steam_spy_url + str(row['data-ds-appid']))

            # region Custom Filters
            if steam_spy_data['name'] == 'null' or steam_spy_data['name'] is None:
                print(f"App {row['data-ds-appid']} has no data on Steam Spy API. Skipping.")
                skip_counter += 1
                continue
            if (steam_spy_data['positive'] + steam_spy_data['negative']) < minimum_reviews:
                print(f"App {row['data-ds-appid']} only has "
                      f"{(steam_spy_data['positive'] + steam_spy_data['negative'])} reviews. Skipping.")
                skip_counter += 1
                continue
            if publisher_filter == 'i' and not (steam_spy_data['developer'] == steam_spy_data['publisher']):
                #print(f"Gathering only indie games. App {steam_spy_data['appid']} is not an indie game. Skipping.")
                #skip_counter += 1
                continue
            if publisher_filter == 'p' and (steam_spy_data['developer'] == steam_spy_data['publisher']):
                #print(f"Gathering only publisher games. App {steam_spy_data['appid']} is not a publisher game. Skipping.")
                #skip_counter += 1
                continue
            # endregion

            app_ids.append(steam_spy_data['appid'])
            print(f"{str(len(app_ids))} {steam_spy_data['name']}: {steam_spy_data['appid']}")

            if len(app_ids) == n:
                print("DONE")
                print(f"Total number of apps skipped: {skip_counter}")
                return app_ids

        page += 1
        print(f"APP ID COUNT: {len(app_ids)}")


def write_to_json(ids, filepath="apps_details_default.json"):
    """
    Collect and write app details from all apps by id from the ids parameter to a JSON file.

    :param filepath: File path for the JSON file
    :type filepath: str
    :param ids: List of app IDs
    :type ids: list
    """
    url = "http://steamspy.com/api.php?request=appdetails&appid="

    full_json_data = {}

    for app_id in ids:
        json_data = get_request(url + str(app_id))
        try:
            full_json_data[int(app_id)] = json_data
        except ValueError as e:
            print(f"App ID is invalid! ID: {app_id} // ValueError {e.args}")

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(full_json_data, f, indent=2)
            print(f"Successfully wrote data to {filepath}.")
    except Exception as e:
        print("Exception while writing app details to JSON file! {}".format(e.args))
    finally:
        f.close()


stopwatch = Stopwatch()
stopwatch.start()
ids = get_top_n_app_ids(5000, search_filter="topsellers", sort_by="", publisher_filter='p', minimum_reviews=50)
stopwatch.stop()
scrape_time = stopwatch.duration
print(f"Getting IDs took: {stopwatch.duration}")

stopwatch.reset()

stopwatch.start()
write_to_json(ids, "topsellers_publisher_5000_minreview50.json")
stopwatch.stop()
print(f"Scraping took {scrape_time}\nWriting took: {stopwatch.duration}")

#write_to_json(get_top_n_app_ids(1000, search_filter="topsellers", sort_by="", publisher_filter='i', minimum_reviews=100), "topsellers_indie_top_1000.json")
#write_to_json(get_top_n_app_ids(1000, search_filter="topsellers", sort_by="", publisher_filter='p', minimum_reviews=100), "topsellers_publisher_top_1000.json")

'''
topsellers, a, min review 50, n=5000
Total number of apps skipped: 588
Getting IDs took: 2134.6165761999996
Successfully wrote data to topsellers_all_5000_minreview50.json.
Scraping took 2134.6165761999996
Writing took: 952.5287761


topsellers, indie only, min review 50, n=5000
Total number of apps skipped: 1975 (wow!)
Getting IDs took: 3192.7207608000003
Successfully wrote data to topsellers_indie_5000_minreview50.json.
Scraping took 3192.7207608000003
Writing took: 956.6825168999999

topsellers, publisher, min review 50, n=5000
Total number skipped: 2123
Scraping took: 4303.8243391
Writing took: 1701.9063254 (for some reason)
'''

# TODO: Get top n app ids for any app that has at least x (to be determined amount) of reviews.


