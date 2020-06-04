import datetime
import json
import sys

import requests
from dateutil.relativedelta import relativedelta
import pandas as pd


class Trends():
    def __init__(self):
        if len(sys.argv) != 2:
            sys.exit("Usage: python3 data_collector.py keyword")

        self.start_date = datetime.date(2004, 1, 1)
        self.end_date = datetime.date.today()
        self.keyword = sys.argv[1]

        self.get_daily()
        print(self.daily)
        self.get_weekly()
        print(self.weekly)
        self.get_monthly()
        print(self.monthly)

    def get_daily(self):
        print("Downloading daily data...")

        start_increment = self.start_date
        end_increment = self.start_date + relativedelta(months=+6)
        dataframe = False

        while True:
            token = self.get_token(
                f"{start_increment} {end_increment}")

            url = f"https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%22{str(start_increment)}%20{str(end_increment)}%22%2C%22resolution%22%3A%22DAY%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22{self.keyword}%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token={token}&tz=-120"

            if not dataframe:
                self.daily = pd.read_csv(url, header=1)
                dataframe = True
            else:
                temp = pd.read_csv(url, header=1)
                self.daily = self.daily.append(temp, ignore_index=True)

            # Daily data can be downloaded in 6-month increments.
            start_increment += relativedelta(months=+6)
            end_increment += relativedelta(months=+6)

            if start_increment > self.end_date:
                self.daily = self.daily.rename(
                    columns={"Day": "date", "debt: (United States)": "relative_frequency"})
                return
            else:
                # Remove overlap.
                self.daily = self.daily[:-1]

    def get_weekly(self):
        print("Downloading weekly data...")

        start_increment = self.start_date
        end_increment = self.start_date + relativedelta(years=+5)
        dataframe = False

        while True:
            token = self.get_token(f"{start_increment} {end_increment}")

            url = f"https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%22{str(start_increment)}%20{str(end_increment)}%22%2C%22resolution%22%3A%22WEEK%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22{self.keyword}%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token={token}&tz=-120"

            if not dataframe:
                self.weekly = pd.read_csv(url, header=1)
                dataframe = True
            else:
                temp = pd.read_csv(url, header=1)
                self.weekly = self.weekly.append(temp, ignore_index=True)

            # Weekly data can be downloaded in 5-year increments.
            start_increment += relativedelta(years=+5)
            end_increment += relativedelta(years=+5)

            if start_increment > datetime.date.today():
                self.weekly = self.weekly.rename(
                    columns={"Week": "date", "debt: (United States)": "relative_frequency"})
                return

    def get_monthly(self):
        print("Downloading monthly data...")
        token = self.get_token(f"{self.start_date} {self.end_date}")

        url = f"https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%22{str(self.start_date)}%20{str(self.end_date)}%22%2C%22resolution%22%3A%22MONTH%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22{self.keyword}%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token={token}&tz=-120"

        self.monthly = pd.read_csv(url, header=1)
        self.monthly = self.monthly.rename(
            columns={"Month": "date", "debt: (United States)": "relative_frequency"})

    def get_token(self, timespan):
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
                    "req": '{"comparisonItem": [{"keyword": ' + f'"{self.keyword}"' + ', "time": ' + f'"{timespan}"' + ', "geo": "US"}], "category": 0, "property": ""}'}
        )

        content = response.text[4:]
        return json.loads(content)["widgets"][0]["token"]


if __name__ == "__main__":
    Trends()
