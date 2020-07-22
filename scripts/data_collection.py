import datetime
import json
import os
import random
import sys
from time import sleep

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta


class Trends():
    """
    Pulls daily, weekly, and monthly data from Google Trends, and adjusts
    them so that it is weekly data which is relative to each other.
    It does this based on the weekly and monthly data.
    """

    def __init__(self):

        self.start_date = datetime.date(2004, 1, 1)
        self.end_date = datetime.date.today()

        with open("scripts/keywords.txt", "r") as f:
            for line in f:
                self.keyword = line.strip()

                # Spaces aren't allowed in URLs.
                self.keyword_url = self.keyword.replace(" ", "%20")

                # Files shouldn't contain spaces.
                self.keyword_file = self.keyword.replace(" ", "_")

                # Make sure that the keyword hasn't already been downloaded.
                if os.path.exists(f"data/weekly/{self.keyword_file}.csv") and os.path.exists(f"data/daily/{self.keyword_file}.csv"):
                    continue

                i = 0
                while True:
                    if i >= 3:
                        sys.exit("Too many errors.")
                    try:
                        print(self.keyword)

                        self.pull_daily()
                        self.pull_weekly()
                        self.pull_monthly()

                        self.adjust_weekly()
                        self.adjust_daily()

                        self.download()

                        sleep(90)

                        break
                    except:
                        i += 1

                        print("Error")
                        sleep(120)

    def pull_daily(self):
        """Pulls the daily data of the keyword specified from Google Trends."""

        print("Downloading daily data...")

        # 6-month increments.
        start_increment = self.start_date
        end_increment = self.start_date + relativedelta(months=+6)
        dataframe = False

        while True:
            token = self.get_token(f"{start_increment} {end_increment}")

            url = f"https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%22{str(start_increment)}%20{str(end_increment)}%22%2C%22resolution%22%3A%22DAY%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22{self.keyword_url}%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token={token}&tz=-120"

            if not dataframe:
                self.daily = pd.read_csv(url, header=1)
                dataframe = True
            else:
                temp = pd.read_csv(url, header=1)
                self.daily = self.daily.append(temp, ignore_index=True)

            # Next increment.
            start_increment += relativedelta(months=+6)
            end_increment += relativedelta(months=+6)

            if start_increment > self.end_date:
                self.daily = self.daily.rename(
                    columns={"Day": "Date", f"{self.keyword}: (United States)": "relative_frequency"})
                return
            else:
                # Remove overlap.
                self.daily = self.daily[:-1]

    def pull_weekly(self):
        """Pulls the weekly data of the keyword specified from Google Trends."""

        print("Downloading weekly data...")

        # 5-year increments.
        start_increment = self.start_date
        end_increment = self.start_date + relativedelta(years=+5)
        dataframe = False

        while True:
            token = self.get_token(f"{start_increment} {end_increment}")

            url = f"https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%22{str(start_increment)}%20{str(end_increment)}%22%2C%22resolution%22%3A%22WEEK%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22{self.keyword_url}%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token={token}&tz=-120"

            if not dataframe:
                self.weekly = pd.read_csv(url, header=1)
                dataframe = True
            else:
                temp = pd.read_csv(url, header=1)
                self.weekly = self.weekly.append(temp, ignore_index=True)

            # Next increment.
            start_increment += relativedelta(years=+5)
            end_increment += relativedelta(years=+5)

            if start_increment > datetime.date.today():
                self.weekly = self.weekly.rename(
                    columns={"Week": "Date", f"{self.keyword}: (United States)": "relative_frequency"})
                return

    def pull_monthly(self):
        """Pulls the monthly data of the keyword specified from Google Trends."""

        print("Downloading monthly data...")

        token = self.get_token(f"{self.start_date} {self.end_date}")

        url = f"https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%22{str(self.start_date)}%20{str(self.end_date)}%22%2C%22resolution%22%3A%22MONTH%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22country%22%3A%22US%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22{self.keyword_url}%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token={token}&tz=-120"

        self.monthly = pd.read_csv(url, header=1)
        self.monthly = self.monthly.rename(
            columns={"Month": "Date", f"{self.keyword}: (United States)": "relative_frequency"})

    def get_token(self, timespan):
        """
        Retrieves a token from Google Trends, based on the keyword and timespan.

        This function is a deritative of a function within Pytrends by github.com/GeneralMills.
        Licensed under the Apache license, version 2.0.
        Changes made by github.com/cristianpjensen to fit Njord's use case.
        """
        sleep(random.randint(0, 2))

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

    def adjust_weekly(self):
        """
        Adjusts the weekly data, based on the monthly data.

        Puts in one data point - from the monthly data - per 5-year increment,
        and computes the data inbetween via the percentage change of the
        unadjusted weekly data.
        """

        print("Adjusting weekly data...")

        # 0's to 1's, because you can't divide by 0.
        self.monthly.replace(0, 1)
        self.weekly.replace(0, 1)

        self.weekly["percentage_change"] = \
            1 + self.weekly["relative_frequency"].pct_change()
        self.weekly["Adjusted"] = ""

        # Put in monthtly data point in each 5-year increment.
        i = 0
        while True:
            try:
                self.weekly.loc[i * 261, "Adjusted"] = \
                    self.monthly.loc[i * 60, "relative_frequency"]
                i += 1
            except:
                break

        for i in range(len(self.weekly)):
            if self.weekly["Adjusted"][i] == "":
                prc = float(self.weekly["percentage_change"][i])
                prev_value = float(self.weekly["Adjusted"][i-1])
                new_value = prev_value * prc
                self.weekly.loc[i, "Adjusted"] = new_value

        self.weekly["Adjusted"] = (
            self.weekly["Adjusted"] / self.weekly["Adjusted"].max())

        self.weekly["Adjusted"] = self.weekly["Adjusted"].astype("float64")
        self.weekly["Adjusted"] = self.weekly["Adjusted"].round(2)

        self.weekly = self.weekly.drop(
            ["relative_frequency", "percentage_change"], axis=1)

    def adjust_daily(self):
        """
        Adjusts the daily data, based on the weekly data.

        Puts in one data point - from the weekly data - per 6-month increment,
        and computes the data inbetween via the percentage change of the
        unadjusted daily data.
        """

        print("Adjusting daily data...")
        self.daily = self.daily.replace(0, 1)
        self.daily["percentage_change"] = 1 + \
            self.daily["relative_frequency"].pct_change()
        self.daily["Adjusted"] = ""

        start_increment = self.start_date
        end_increment = start_increment + relativedelta(months=+6)
        end = self.end_date

        # Compute all values after the data point, within it's increment.
        i = 0
        while True:
            imported = False
            while True:
                if i >= len(self.daily):
                    break

                # Insert the weekly data points in each 6-month increment.
                if not imported:
                    try:
                        self.daily.loc[i, "Adjusted"] = self.weekly["Adjusted"].where(
                            self.weekly["Date"] == str(start_increment)).dropna().values[0]
                        imported = True
                    except:
                        pass
                else:
                    prc = float(self.daily["percentage_change"][i])
                    prev_value = float(self.daily["Adjusted"][i-1])
                    new_value = prev_value * prc
                    self.daily.loc[i, "Adjusted"] = new_value

                start_increment += relativedelta(days=+1)
                i += 1

                if start_increment >= end_increment:
                    break

            start_increment = end_increment
            end_increment += relativedelta(months=+6)

            if start_increment > end:
                break

        # Compute all values before the data point, within it's increment.
        i = 0
        while True:
            if i >= len(self.daily) - 1:
                break

            if self.daily.loc[i, "Adjusted"] == "":
                j = 0
                while True:
                    if self.daily.loc[i+j, "Adjusted"] == "":
                        j += 1
                    else:
                        prc = float(self.daily["percentage_change"][i+j])
                        new_value = float(self.daily["Adjusted"][i+j])
                        prev_value = new_value / prc
                        self.daily.loc[i+j-1, "Adjusted"] = prev_value

                        j -= 1

                    if j <= 0:
                        break

            i += 1

        self.daily = self.daily.drop(
            ["relative_frequency", "percentage_change"], axis=1)

        self.daily["Adjusted"] = (
            self.daily["Adjusted"] / self.daily["Adjusted"].max())

        self.daily["Adjusted"] = self.daily["Adjusted"].astype("float64")
        self.daily["Adjusted"] = self.daily["Adjusted"].round(2)

    def download(self):
        """Download the daily and weekly data into CSV-files."""
        print("Converting to CSV format...")

        self.weekly.to_csv(f"data/weekly/{self.keyword_file}.csv", index=False)
        self.daily.to_csv(f"data/daily/{self.keyword_file}.csv", index=False)


if __name__ == "__main__":
    Trends()
