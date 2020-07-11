import pandas as pd
import yfinance as yf
import sys


class FeatureEngineer():
    """
    Feature engineers the Google Trends data, according to the specifications of the user.

    Available features:
      - interval (daily or weekly);
      - amount of days to go into the past, used by rolling and delta;
      - type (delta, dweek, or rolling);
      - target (binary or bins).
    """

    def __init__(self, INTERVAL="weekly", N=21, OFFSET=3, TYPE="delta", TARGET="binary"):
        """
        - `self.N` = amount of days to go in the past, for `Delta_N` and `Average_N`.
        - `self.INTERVAL` = daily or weekly data.
        - `self.OFFSET` = needed, because data is only available after three days.
        - `self.KW_LIST` = a list of all search terms of which the data has been collected.
        - `self.TYPE` = the type of feature the data is (delta, dweek, rolling).
        - `self.TARGET` = the type of target used (binary or bins).

        To use standard values, use `-` instead of values in the CLI.
        """

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
        self.INTERVAL = INTERVAL
        self.N = N
        self.OFFSET = OFFSET
        self.TYPE = TYPE
        self.TARGET = TARGET

        if len(sys.argv) != 5:
            sys.exit(
                "\nUsage: python3 feature_engineering.py INTERVAL N (days) TYPE TARGET (- to use default setting).\n")

        if sys.argv[1] != "-":
            self.INTERVAL = sys.argv[1]

        if sys.argv[2] != "-":
            self.N = sys.argv[2]

        if sys.argv[3] != "-":
            self.TYPE = sys.argv[3]

        if sys.argv[4] != "-":
            self.TARGET = sys.argv[4]

        if self.INTERVAL == "weekly":
            self.OFFSET = 0
            self.N = int(self.N / 7)

        self.import_data()
        self.insert_target()
        self.insert_type()
        self.insert_lag()
        self.insert_index()

        self.df.round(3).to_csv(
            f"data/feature_engineered/{self.INTERVAL}_{self.TYPE}_{self.TARGET}.csv", index=False)

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
        if self.INTERVAL == "daily":
            self.ticker_df = yf.download("DJIA", period="max")
        elif self.INTERVAL == "weekly":
            self.ticker_df = yf.download("DJIA", period="max", interval="1wk")
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
                i = self.N
                while i < len(self.df):
                    self.df.loc[i, f"{kw}"] = self.kw_df.loc[i,
                                                             f"{kw}"] - self.kw_df.loc[i-self.N, f"{kw}"]
                    i += 1

                self.df[f"{kw}"] = self.df[f"{kw}"].shift(self.OFFSET)

        elif self.TYPE == "dweek":
            for kw in self.KW_LIST:
                i = self.N
                while i < len(self.kw_df):
                    self.df.loc[i, f"{kw}"] = self.kw_df.loc[i-7:i, f"{kw}"].mean(
                    ) - self.kw_df.loc[i-self.N-7:i-self.N, f"{kw}"].mean()
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
        self.df = self.ticker_df.merge(self.df, on="Date")
        self.df = self.df.drop("Date", axis=1)

    def insert_lag(self):
        """Adds a lag of 1 day feature."""

        self.df.insert(1, "lag_1", self.df["Target"].shift(1))

        self.df = self.df.drop(0)

    def insert_index(self):
        """Sets the index on the second column, because the Target has to be the first column for Google Cloud AI Platform."""

        self.df.insert(1, "index", pd.Series(self.df.index).astype("int32"))


if __name__ == "__main__":
    FeatureEngineer()
