"""
Updates the Google Trends data to be up to date. Takes in earlier data and
outputs a new CSV-file that contains up to date data. This can then be used as
input for the machine learning algorithm.
"""

import datetime
import json
import os
import random
import sys
from time import sleep

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta


def main():
    update_daily()
    update_weekly()


def update_daily():
    """
    Updates the daily Google Trends data.
    """

    with open('src/data/keywords.txt', 'r') as f:
        for line in f:
            keyword = line.strip()
            keyword_url = keyword.replace(' ', '%20')
            keyword_file = keyword.replace(' ', '_')

            current = pd.read_csv(f'data/raw/daily/{keyword_file}.csv')

            start_date = datetime.datetime.strptime(
                current.loc[len(current)-1, 'Date'], '%Y-%m-%d').date()
            end_date = datetime.date.today()

            token = get_token(keyword, f'{start_date} {end_date}')

            url = 'https://trends.google.com/trends/api/widgetdata/multilin' \
                f'e/csv?req=%7B%22time%22%3A%22{str(start_date)}%20' \
                f'{str(end_date)}%22%2C%22resolution%22%3A%22DAY%22%2C%22locale' \
                '%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%' \
                '7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%' \
                '22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22va' \
                f'lue%22%3A%22{keyword_url}%22%7D%5D%7D%7D%5D%2C%22requestOptio' \
                'ns%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22' \
                f'%2C%22category%22%3A0%7D%7D&token={token}&tz=-120'

            new = pd.read_csv(url, header=1)
            new = new.rename(
                columns={f'{keyword}: (United States)': 'Adjusted'})
            new['change'] = 1 + new['Adjusted'].pct_change()
            new = new[1:]

            length = len(current)
            for index, row in new.iterrows():
                index += length
                current.loc[index-1, 'Date'] = row['Day']
                current.loc[index-1, 'Adjusted'] = \
                    current.loc[index-2, 'Adjusted'] * row['change']

            current.to_csv(
                f'data/interim/daily/{keyword_file}.csv', index=False)


def update_weekly():
    """
    Updates the weekly Google Trends data.
    """

    with open('src/data/keywords.txt', 'r') as f:
        for line in f:
            keyword = line.strip()
            keyword_url = keyword.replace(' ', '%20')
            keyword_file = keyword.replace(' ', '_')

            current = pd.read_csv(f'data/raw/daily/{keyword_file}.csv')

            start_date = datetime.datetime.strptime(
                current.loc[len(current)-1, 'Date'], '%Y-%m-%d').date()
            end_date = start_date + relativedelta(years=+5)

            token = get_token(keyword, f'{start_date} {end_date}')

            url = 'https://trends.google.com/trends/api/widgetdata/multilin' \
                f'e/csv?req=%7B%22time%22%3A%22{str(start_date)}%20' \
                f'{str(end_date)}%22%2C%22resolution%22%3A%22WEEK%22%2C%22locale' \
                '%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%' \
                '7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%' \
                '22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22va' \
                f'lue%22%3A%22{keyword_url}%22%7D%5D%7D%7D%5D%2C%22requestOptio' \
                'ns%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22' \
                f'%2C%22category%22%3A0%7D%7D&token={token}&tz=-120'

            new = pd.read_csv(url, header=1)
            new = new.rename(
                columns={f'{keyword}: (United States)': 'Adjusted'})
            new['change'] = 1 + new['Adjusted'].pct_change()
            new = new[1:]

            length = len(current)
            for index, row in new.iterrows():
                index += length
                current.loc[index-1, 'Date'] = row['Week']
                current.loc[index-1, 'Adjusted'] = \
                    current.loc[index-2, 'Adjusted'] * row['change']

            current.to_csv(
                f'data/interim/weekly/{keyword_file}.csv', index=False)


def get_token(keyword, timespan):
    """
    Retrieves a token from Google Trends, based on the keyword and timespan.

    This function is a deritative of a function within Pytrends by 
    github.com/GeneralMills. Licensed under the Apache license, version 2.0.
    Changes made by github.com/cristianpjensen to fit Njord's use case.

    Args:
        keyword (str): Keyword for which the token should be retrieved.
        timespan (str): Start and end date of the timespan with a space in
            between.

    Returns:
        str: Token, which can be used in the url for downloading the data.

    Raises:
        TypeError: When ``keyword`` or ``timespan`` is not of type string.

    """

    if not isinstance(keyword, str) or not isinstance(timespan, str):
        raise TypeError('keyword or timespan is not of type string.')

    session = requests.session()

    response = session.get(
        url='https://trends.google.com/trends/api/explore',
        timeout=(2, 5),
        cookies=dict(filter(lambda i: i[0] == 'NID', requests.get(
            'https://trends.google.com/?geo=US',
            timeout=(2, 5)
        ).cookies.items())),
        params={'hl': 'en-US', 'tz': -120,
                'req': '{"comparisonItem": [{"keyword": ' + f'"{keyword}"' +
                ', "time": ' + f'"{timespan}"' +
                ', "geo": "US"}], "category": 0, "property": ""}'}
    )

    content = response.text[4:]
    return json.loads(content)['widgets'][0]['token']


if __name__ == '__main__':
    main()
