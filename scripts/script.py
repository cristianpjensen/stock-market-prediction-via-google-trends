"""
This is the script, which is run every 24 hours (in trading weeks) by a GitHub
workflow. It updates data, engineers features, and makes predictions. Then,
based on those predictions, it updates ``state.csv``, which, in turn, updates
the plot in the webpage.
"""

import datetime

import joblib
import numpy as np
import pandas as pd
import yfinance as yf
from dateutil.relativedelta import relativedelta
from sklearn.neural_network import MLPClassifier

from build_features import delta, research
from update_data import update_daily


def main():
    trends_df = update_daily()
    trends_df.to_csv('data/stock_market.csv', index=False)
    state_df = pd.read_csv('data/state.csv')

    if state_df.date[len(state_df)-1] == str(datetime.date.today() - 
                                             relativedelta(days=1)):
        return 0

    trends_df = append_missing_dates(trends_df)

    features_df = top_features(trends_df)
    features_df['Date'] = pd.to_datetime(features_df['Date'])

    stock_df = pull_djia(start=state_df.date[len(state_df)-1])
    df = pd.merge(stock_df, features_df, on='Date')

    preds = make_preds(df)

    states = []
    current = state_df.position[len(state_df)-1]
    for ind, pred in enumerate(preds):
        if pred == 1:
            current *= df.Pct_change[ind]
        else:
            current /= df.Pct_change[ind]
        
        states.append(current)

    output = pd.DataFrame()

    output['date'] = df['Date'].astype('str')
    output['position'] = states

    output = pd.concat([state_df, output])

    output.to_csv('data/state.csv', index=False)


def append_missing_dates(df):
    """
    Appends the missing dates, because else there will be a problem with the
    features not going untill the current date. This is caused by Google
    Trends only giving data untill three days before the current date.

    Args:
        df (pandas.DataFrame): Google Trends data on which to add the missing
            dates.

    Returns:
        pandas.DataFrame: Dataframe with the missing dates added.

    """
    date = datetime.date.today()
    missing_dates = pd.Series([str(date - relativedelta(days=day)) for day in [2, 1]])
    missing_df = pd.DataFrame(data={'Date': missing_dates, 'Adjusted': [np.nan for _ in range(len(missing_dates))]})

    return df.append(missing_df, ignore_index=True)


def top_features(df):
    """
    Compute the top features, which have been found using the training data.

    Args:
        df (pandas.DataFrame): Google Trends dataframe.

    Returns:
        pandas.DataFrame: Dataframe containing the features.

    """
    features = pd.DataFrame()
    features['Date'] = df['Date']

    features['BBAND_L-20-2_shifted_by_3'] = (df.Adjusted.rolling(20).mean() - 2*df.Adjusted.rolling(20).std()).shift(3)
    features['BBAND_L-20-1_shifted_by_3'] = (df.Adjusted.rolling(20).mean() - df.Adjusted.rolling(20).std()).shift(3)
    features['BBAND_L-20-2_shifted_by_4'] = (df.Adjusted.rolling(20).mean() - 2*df.Adjusted.rolling(20).std()).shift(4)
    features['BBAND_L-20-1_shifted_by_4'] = (df.Adjusted.rolling(20).mean() - df.Adjusted.rolling(20).std()).shift(4)
    features['BBAND_L-20-1_shifted_by_5'] = (df.Adjusted.rolling(20).mean() - df.Adjusted.rolling(20).std()).shift(5)
    features['BBAND_L-20-2_shifted_by_5'] = (df.Adjusted.rolling(20).mean() - 2*df.Adjusted.rolling(20).std()).shift(5)
    features['delta-30_shifted_by_10'] = delta(df.Adjusted, length=30).shift(10)
    features['BBAND_L-20-1_shifted_by_9'] = (df.Adjusted.rolling(20).mean() - df.Adjusted.rolling(20).std()).shift(9)
    features['BBAND_L-10-2_shifted_by_10'] = (df.Adjusted.rolling(10).mean() - 2*df.Adjusted.rolling(10).std()).shift(10)
    features['BBAND_L-20-2_shifted_by_9'] = (df.Adjusted.rolling(20).mean() - 2*df.Adjusted.rolling(20).std()).shift(9)
    features['BBAND_L-20-1_shifted_by_10'] = (df.Adjusted.rolling(20).mean() - df.Adjusted.rolling(20).std()).shift(10)
    features['BBAND_L-20-1_shifted_by_8'] = (df.Adjusted.rolling(20).mean() - df.Adjusted.rolling(20).std()).shift(8)
    features['BBAND_L-20-2_shifted_by_8'] = (df.Adjusted.rolling(20).mean() - 2*df.Adjusted.rolling(20).std()).shift(8)
    features['BBAND_L-20-1_shifted_by_6'] = (df.Adjusted.rolling(20).mean() - df.Adjusted.rolling(20).std()).shift(6)
    features['BBAND_L-20-2_shifted_by_10'] = (df.Adjusted.rolling(20).mean() - 2*df.Adjusted.rolling(20).std()).shift(10)
    features['BBAND_L-10-1_shifted_by_5'] = (df.Adjusted.rolling(10).mean() - df.Adjusted.rolling(10).std()).shift(5)
    features['BBAND_L-20-2_shifted_by_6'] = (df.Adjusted.rolling(20).mean() - 2*df.Adjusted.rolling(20).std()).shift(6)
    features['BBAND_L-10-2_shifted_by_9'] = (df.Adjusted.rolling(10).mean() - 2*df.Adjusted.rolling(10).std()).shift(9)
    features['BBAND_L-10-2_shifted_by_5'] = (df.Adjusted.rolling(10).mean() - 2*df.Adjusted.rolling(10).std()).shift(5)
    features['BBAND_L-10-1_shifted_by_10'] = (df.Adjusted.rolling(10).mean() - df.Adjusted.rolling(10).std()).shift(10)
    features['delta-14_shifted_by_3'] = delta(df.Adjusted, length=14).shift(3)
    features['delta-14_shifted_by_7'] = delta(df.Adjusted, length=14).shift(7)
    features['BBAND_L-10-1_shifted_by_4'] = (df.Adjusted.rolling(10).mean() - df.Adjusted.rolling(10).std()).shift(4)
    features['BBAND_L-10-1_shifted_by_3'] = (df.Adjusted.rolling(10).mean() - df.Adjusted.rolling(10).std()).shift(3)
    features['delta-7_shifted_by_7'] = delta(df.Adjusted, length=7).shift(7)
    features['BBAND_L-20-1_shifted_by_7'] = (df.Adjusted.rolling(20).mean() - df.Adjusted.rolling(20).std()).shift(7)
    features['delta-90_shifted_by_4'] = delta(df.Adjusted, length=90).shift(4)
    features['BBAND_L-10-1_shifted_by_9'] = (df.Adjusted.rolling(10).mean() - df.Adjusted.rolling(10).std()).shift(9)
    features['BBAND_L-10-2_shifted_by_8'] = (df.Adjusted.rolling(10).mean() - 2*df.Adjusted.rolling(10).std()).shift(8)
    features['BBAND_L-20-2_shifted_by_7'] = (df.Adjusted.rolling(20).mean() - 2*df.Adjusted.rolling(20).std()).shift(7)
    features['delta-30_shifted_by_6'] = delta(df.Adjusted, length=30).shift(6)
    features['delta-7_shifted_by_10'] = delta(df.Adjusted, length=7).shift(10)
    features['delta-90_shifted_by_3'] = delta(df.Adjusted, length=90).shift(3)
    features['BBAND_L-10-1_shifted_by_8'] = (df.Adjusted.rolling(10).mean() - df.Adjusted.rolling(10).std()).shift(8)
    features['SMA_delta-14_shifted_by_3'] = research(df.Adjusted, length=14).shift(3)
    features['SMA_delta-14_shifted_by_7'] = research(df.Adjusted, length=14).shift(7)
    features['SMA_delta-7_shifted_by_10'] = research(df.Adjusted, length=7).shift(10)
    features['Adjusted_shifted_by_3'] = df.Adjusted.shift(3)
    features['BBAND_L-10-2_shifted_by_4'] = (df.Adjusted.rolling(10).mean() - 2*df.Adjusted.rolling(10).std()).shift(4)
    features['SMA_delta-3_shifted_by_3'] = research(df.Adjusted, length=3).shift(3)
    features['SMA_delta-90_shifted_by_3'] = research(df.Adjusted, length=30).shift(3)
    features['delta-3_shifted_by_3'] = delta(df.Adjusted, length=3).shift(3)
    features['SMA_delta-14_shifted_by_10'] = research(df.Adjusted, length=14).shift(10)
    features['delta-30_shifted_by_9'] = delta(df.Adjusted, length=30).shift(9)
    features['BBAND_L-10-1_shifted_by_6'] = (df.Adjusted.rolling(10).mean() - df.Adjusted.rolling(10).std()).shift(6)
    features['SMA_delta-30_shifted_by_3'] = research(df.Adjusted, length=30).shift(3)
    features['BBAND_L-10-2_shifted_by_3'] = (df.Adjusted.rolling(10).mean() - 2*df.Adjusted.rolling(10).std()).shift(3)
    features['BBAND_L-10-2_shifted_by_6'] = (df.Adjusted.rolling(10).mean() - 2*df.Adjusted.rolling(10).std()).shift(6)
    features['SMA_delta-7_shifted_by_7'] = research(df.Adjusted, length=7).shift(7)
    features['delta-90_shifted_by_8'] = delta(df.Adjusted, length=90).shift(8)

    return features.dropna()


def pull_djia(start):
    """
    Pulls the stock price data for the Dow Jones Industrial Average.

    Args:
        start (string): The date from which to start. Format: %Y-%m-%d.

    Returns:
        pandas.DataFrame: Dataframe containg the stock price data for the Dow
            Jones Industrial Average, starting from ``start``.

    """
    djia = yf.download('DJIA', start=start)
    djia['Pct_change'] = 1 + djia.Close.pct_change()
    djia = djia[1:]
    djia = djia.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
    
    return djia.reset_index()


def make_preds(df):
    """
    Makes predictions, based on the features data, using the model file.

    Args:
        df (pandas.DataFrame): Dataframe containg the features.

    Returns:
        np.array: An array containing 1s and 0s. 1 = up, 0 = down. This is
            used to compute the current state of the algorithm.

    """
    model = joblib.load('scripts/model.sav')

    return model.predict(df.drop(['Date', 'Close', 'Pct_change'], axis=1))


if __name__ == '__main__':
    main()
