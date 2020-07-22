import pandas as pd
import yfinance as yf
import sys
import getopt
import os


class FeatureEngineer():
    """
    Feature engineers the Google Trends data, according to the specifications of the user.

    Available features:
      - interval (daily or weekly);
      - amount of days to go into the past, used by rolling and delta;
      - type (delta, dweek, or rolling);
      - target (binary or bins).
    """

    def __init__(self):
        """
        - `self.N` = amount of days to go in the past, for `Delta_N` and `Average_N`.
        - `self.INTERVAL` = daily or weekly data.
        - `self.OFFSET` = needed, because data is only available after three days.
        - `self.KW_LIST` = a list of all search terms of which the data has been collected.
        - `self.TYPE` = the type of feature the data is (delta, dweek, rolling).
        - `self.TARGET` = the type of target used (binary or bins).

        To use standard values, use `-` instead of values in the CLI.
        """

        self.get_parameters()
        self.import_data()
        self.insert_target()
        self.insert_type()
        self.insert_lag()

        if self.curated:
            self.df.round(3).to_csv(
                f"data/feature_engineered/{self.INTERVAL}-{self.TYPE}-{self.TARGET}-curated.csv", index=False)
        else:
            self.df.round(3).to_csv(
                f"data/feature_engineered/{self.INTERVAL}-{self.TYPE}-{self.TARGET}.csv", index=False)

    def get_parameters(self):
        """Gets the parameters given by the user. If no parameter was given, then standard parameters will be used."""
        self.KW_LIST = ["debt", "color", "stocks", "restaurant", "portfolio", "inflation", "housing", "dow_jones", "revenue",
                        "economics", "credit", "markets", "return", "unemployment", "money", "religion", "cancer", "growth",
                        "investment", "hedge", "marriage", "bonds", "derivatives", "headlines", "profit", "society", "leverage",
                        "loss", "cash", "office", "fine", "stock_market", "banking", "crisis", "happy", "car", "nasdaq",
                        "gains", "finance", "sell", "invest", "fed", "house", "metals", "travel", "returns", "gain",
                        "default", "present", "holiday", "water", "rich", "risk", "gold", "success", "oil", "war", "economy",
                        "chance", "lifestyle", "greed", "food", "movie", "nyse", "ore", "opportunity", "health", "earnings",
                        "arts", "culture", "bubble", "buy", "trader", "tourism", "politics", "energy", "consume", "consumption",
                        "freedom", "dividend", "world", "conflict", "kitchen", "forex", "home", "cash", "transaction", "garden",
                        "fond", "train", "labor", "fun", "environment", "ring"]

        argv = sys.argv[1:]

        self.INTERVAL = "weekly"
        self.N = 3
        self.OFFSET = 0
        self.TYPE = "pct_change"
        self.TARGET = "binary"
        self.curated = False

        try:
            opts, args = getopt.getopt(argv, "i:n:o:t:r:c:",
                                       ["interval=", "n=", "offset=", "type=",
                                        "target=", "curation="])
        except getopt.GetoptError:
            print("Usage: feature_engineering.py -i <interval> -n <n> -o <offset> -t <feature type> -r <target type> -c <curation boolean>")
            sys.exit(2)

        for opt, arg in opts:
            if opt in ["-i", "--interval"]:
                if arg in ["daily", "weekly"]:
                    self.INTERVAL = arg
                else:
                    print(
                        "The interval has to be `daily` or `weekly`. Consult the documentation.")
                    sys.exit(2)

            if opt in ["-n", "--n"]:
                try:
                    arg = int(arg)
                except ValueError:
                    print(f"{arg} is not an integer.")

                if 0 < arg < 100:
                    self.N = arg
                else:
                    print("0 < N < 100.")
                    sys.exit(2)

            if opt in ["-o", "--offset"]:
                try:
                    arg = int(arg)
                except ValueError:
                    print(f"{arg} is not an integer.")

                if 0 <= arg < 100:
                    self.OFFSET = arg
                else:
                    print("0 <= offset < 100.")
                    sys.exit(2)

            if opt in ["-t", "--type"]:
                if arg in ["delta", "pct_change", "rolling"]:
                    self.TYPE = arg
                else:
                    print(
                        "The feature type has to be `delta`, `pct_change`, or `rolling`. Consult the documentation.")
                    sys.exit(2)

            if opt in ["-r", "--target"]:
                if arg in ["binary", "bins"]:
                    self.TARGET = arg
                else:
                    print(
                        "The target has to be `binary` or `bins. Consult the documentation.")
                    sys.exit(2)

            if opt in ["-c", "--curated"]:
                if arg == "True":
                    self.curated = True
                    self.KW_LIST = ["debt", "stocks", "dow_jones", "markets", "unemployment", "money", "stock_market",
                                    "crisis", "nasdaq", "finance", "invest"]
                elif arg == "False":
                    self.curated = False
                else:
                    print(
                        "Curated has to be `True` or `False`. Consult the documentation.")
                    sys.exit(2)

    def import_data(self):
        """Imports data from Yahoo finance and the data files, containing Google Trends data."""

        self.kw_df = pd.DataFrame()

        # Google Trends data.
        date = False
        for kw in self.KW_LIST:

            if not date:
                self.kw_df["Date"] = pd.read_csv(
                    f"data/{self.INTERVAL}/{kw}.csv")["Date"]
                date = True

            self.kw_df[f"{kw}"] = pd.read_csv(
                f"data/{self.INTERVAL}/{kw}.csv")["Adjusted"]

        # Historical stock price data.
        with HiddenOutput():
            if self.INTERVAL == "daily":
                self.ticker_df = yf.download("DJIA", period="max")
            elif self.INTERVAL == "weekly":
                self.ticker_df = yf.download(
                    "DJIA", period="max", interval="1wk")
                self.kw_df["Date"] = pd.to_datetime(
                    self.kw_df["Date"], format="%Y-%m-%d")
                self.kw_df["Date"] += pd.DateOffset(1)

        # Manipulate stock price data.
        self.ticker_df["Change"] = self.ticker_df["Close"].pct_change()
        self.ticker_df = self.ticker_df.drop(
            ["Open", "High", "Low", "Adj Close", "Volume", "Close"], axis=1)
        self.ticker_df = self.ticker_df.reset_index()

        self.kw_df["Date"] = pd.to_datetime(
            self.kw_df["Date"], format="%Y-%m-%d")

    def insert_target(self):
        """Inserts the type of target specified by the user."""

        if self.TARGET == "binary":
            self.ticker_df["Target"] = pd.cut(self.ticker_df["Change"],
                                              bins=[-float("inf"),
                                                    0, float("inf")],
                                              labels=[0, 1])
        elif self.TARGET == "bins":
            self.ticker_df["Target"] = pd.cut(self.ticker_df["Change"],
                                              bins=[-float("inf"), -0.025, -0.02, -0.015, -0.01, -0.005,
                                                    0, 0.005, 0.01, 0.015, 0.02, 0.025, float("inf")],
                                              labels=[-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])

        self.ticker_df = self.ticker_df.drop("Change", axis=1)

    def insert_type(self):
        """Inserts the data features, specified by the user."""

        self.df = pd.DataFrame()
        self.df["Date"] = self.kw_df["Date"]

        if self.TYPE == "delta":
            for kw in self.KW_LIST:
                i = self.N+1
                while i < len(self.df):
                    self.df.loc[i, f"{kw}"] = self.kw_df.loc[i-1,
                                                             f"{kw}"] - self.kw_df.loc[i-self.N-1, f"{kw}"]
                    i += 1

                self.df[f"{kw}"] = self.df[f"{kw}"].shift(self.OFFSET)

        elif self.TYPE == "pct_change":
            for kw in self.KW_LIST:
                i = self.N+1
                while i < len(self.df):
                    self.df.loc[i, f"{kw}"] = (
                        self.kw_df.loc[i-1, f"{kw}"] - self.kw_df.loc[i-self.N-1, f"{kw}"]) / self.kw_df.loc[i-1, f"{kw}"]
                    i += 1

                self.df[f"{kw}"] = self.df[f"{kw}"].shift(self.OFFSET)

        elif self.TYPE == "rolling":
            for kw in self.KW_LIST:
                i = self. N
                while i < len(self.kw_df):
                    self.df[f"{kw}"] = self.kw_df[f"{kw}"].rolling(
                        self.N).mean()
                    i += 1

                self.df[f"{kw}"] = self.df[f"{kw}"].shift(self.OFFSET)

        self.df = self.df[self.N+self.OFFSET:]
        self.df = self.df.reset_index()

        self.df = self.ticker_df.merge(self.df, on="Date")
        self.df = self.df.drop("Date", axis=1)

        self.df["index"] -= (self.N + 1)

    def insert_lag(self):
        """Adds a lag of 1 day feature."""

        self.df.insert(2, "lag_1", self.df["Target"].shift(1))
        self.df = self.df.drop(0)


class HiddenOutput():
    """Hides the output of YFinance."""

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


if __name__ == "__main__":
    FeatureEngineer()
