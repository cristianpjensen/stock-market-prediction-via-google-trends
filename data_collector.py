import datetime
import json
import sys
import os
import urllib.request

import requests
from dateutil.relativedelta import relativedelta


HEADER = "date,relative_frequency\n"


def main():
    if len(sys.argv) != 4:
        sys.exit("Usage: python3 data_collector.py keyword start_date end_date")

    # Turn the dates into datetime types.
    try:
        start_date = datetime.date.fromisoformat(sys.argv[2])
    except:
        if sys.argv[2].lower() == "start":
            start_date = datetime.date(year=2004, month=1, day=1)
        else:
            sys.exit("Invalid start_date format.")

    try:
        end_date = datetime.date.fromisoformat(sys.argv[3])
    except:
        if sys.argv[3].lower() == "today":
            end_date = datetime.date.today()
        else:
            sys.exit("Invalid end_date format.")

    # Check if the dates given are within Google Trends timerange.
    if start_date < datetime.date(year=2004, month=1, day=1):
        sys.exit("Google Trends data wasn't collected pre-2004.")
    elif end_date > datetime.date.today():
        sys.exit("Future Google Trends data isn't collected yet.")

    keyword = sys.argv[1]

    # Create necessary folders.
    try:
        os.mkdir("data")
    except:
        pass

    try:
        os.mkdir(f"data/{keyword}")
    except:
        pass

    try:
        os.mkdir(f"data/{keyword}/{str(start_date)}_{end_date}")
        os.mkdir(f"data/{keyword}/{str(start_date)}_{end_date}/unadjusted")
        os.mkdir(
            f"data/{keyword}/{str(start_date)}_{end_date}/unadjusted/daily")
        os.mkdir(
            f"data/{keyword}/{str(start_date)}_{end_date}/unadjusted/weekly")
    except:
        sys.exit("You have already collected data for that keyword in that timespan.")

    # Pull data.
    get_monthly(keyword, start_date, end_date)
    get_weekly(keyword, start_date, end_date)
    get_daily(keyword, start_date, end_date)


def get_daily(keyword, start_date, end_date):
    print("Downloading daily data...")

    start_increment = start_date
    end_increment = start_date + relativedelta(months=+6)
    index = 0

    while True:
        token = get_token(keyword, f"{start_increment} {end_increment}")

        url = f"https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%22{str(start_increment)}%20{str(end_increment)}%22%2C%22resolution%22%3A%22DAY%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22{keyword}%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token={token}&tz=-120"
        urllib.request.urlretrieve(
            url, f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/daily/temp.csv")

        # Remove first two lines.
        with open(f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/daily/temp.csv", "r") as f:
            with open(f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/daily/{index}_daily_{keyword}.csv", "w") as f1:
                for _ in range(3):
                    next(f)
                f1.write(HEADER)
                lines = f.readlines()
                if end_increment < end_date:
                    lines.pop()
                f1.writelines(lines)

        os.remove(
            f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/daily/temp.csv")

        start_increment += relativedelta(months=+6)
        end_increment += relativedelta(months=+6)

        if start_increment > datetime.date.today():
            break

        index += 1


def get_weekly(keyword, start_date, end_date):
    print("Downloading weekly data...")

    start_increment = start_date
    end_increment = start_date + relativedelta(years=+5)
    index = 0

    while True:
        token = get_token(keyword, f"{start_increment} {end_increment}")

        url = f"https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%22{str(start_increment)}%20{str(end_increment)}%22%2C%22resolution%22%3A%22WEEK%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22{keyword}%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token={token}&tz=-120"
        urllib.request.urlretrieve(
            url, f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/weekly/temp.csv")

        # Remove first two lines.
        with open(f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/weekly/temp.csv", "r") as f:
            with open(f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/weekly/{index}_weekly_{keyword}.csv", "w") as f1:
                for _ in range(3):
                    next(f)
                f1.write(HEADER)
                for line in f:
                    f1.write(line)

        os.remove(
            f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/weekly/temp.csv")

        start_increment += relativedelta(years=+5)
        end_increment += relativedelta(years=+5)

        if start_increment > datetime.date.today():
            break

        index += 1


def get_monthly(keyword, start_date, end_date):
    print("Downloading monthly data...")
    token = get_token(keyword, f"{start_date} {end_date}")

    url = f"https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%22{str(start_date)}%20{str(end_date)}%22%2C%22resolution%22%3A%22MONTH%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22{keyword}%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token={token}&tz=-120"
    urllib.request.urlretrieve(
        url, f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/temp.csv")

    # Remove first two line
    with open(f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/temp.csv", "r") as f:
        with open(f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/monthly_{keyword}.csv", "w") as f1:
            for _ in range(3):
                next(f)
            f1.write(HEADER)
            for line in f:
                f1.write(line)

    os.remove(
        f"data/{keyword}/{str(start_date)}_{str(end_date)}/unadjusted/temp.csv")


def get_token(keyword, timespan):
    """
    Retrieves a token from Google Trends, based on the keyword and timespan.

    This function is a deritative of a function within Pytrends by github.com/GeneralMills.
    Licensed under the Apache license, version 2.0.
    Changes made by github.com/cristianpjensen to fit Njord's use case.
    """
    session = requests.session()

    response = session.get(
        url="https://trends.google.com/trends/api/explore",
        timeout=(2, 5),
        cookies=dict(filter(lambda i: i[0] == "NID", requests.get(
            "https://trends.google.com/?geo=US",
            timeout=(2, 5)
        ).cookies.items())),
        params={"hl": "en-US", "tz": -120,
                "req": '{"comparisonItem": [{"keyword": ' + f'"{keyword}"' + ', "time": ' + f'"{timespan}"' + ', "geo": "US"}], "category": 0, "property": ""}'}
    )

    content = response.text[4:]
    return json.loads(content)["widgets"][0]["token"]


if __name__ == "__main__":
    main()
