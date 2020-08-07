import pandas as pd
import yfinance as yf


def research(series, length=3):
    """
    The feature which is also used in the research paper by Tobias Preis et al.

    Args:
        series (pandas.Series): Series of the Google Trends data.
        length (int, optional): Length of the moving average used in the
            calculation. Defaults to 3.

    Returns:
        pandas.Series: Series containing the feature.

    Raises:
        ValueError: If length is less than 1 or greater than the length of the
            series.
        TypeError: If `series` is not of pandas.Series type or `length` is not an
            integer.

    """

    if not isinstance(length, int):
        raise TypeError(f'`length` has to be of type int.')

    if not isinstance(series, pd.Series):
        raise TypeError(f'`series` must be of type pandas.Series.')

    if length < 1 or length > series.size:
        raise ValueError('`length` may not be less than 1 or greater than the \
                          size of the series.')

    N = series.rolling(window=length).mean().shift(1)
    delta_n = series - N

    return delta_n


def delta(series, length=3):
    """
    Feature based on the delta between two values `length` away.

    Args:
        series (pandas.Series): Series of Google Trends data.
        length (int, optional): Difference between the two values of which the
            delta is calculated. Defaults to 3.

    Returns:
        pandas.Series: Series containing the feature.

    Raises:
        ValueError: If length is less than 1 or greater than the length of the
            series.
        TypeError: If `series` is not of pandas.Series type or `length` is not an
            integer.

    """

    if not isinstance(length, int):
        raise TypeError(f'`length` has to be of type int.')

    if not isinstance(series, pd.Series):
        raise TypeError(f'`series` must be of type pandas.Series.')

    if length < 1 or length > series.size:
        raise ValueError('`length` may not be less than 1 or greater than the \
                          size of the series.')

    return series.diff(periods=length)


def pct_change(series, length=3):
    """
    Feature based on the percentage change between two values `length` away.

    Args:
        series (pandas.Series): Series of Google Trends data.
        length (int, optional): Percentage change between the two values of which
            the delta is calculated. Defaults to 3.

    Returns:
        pandas.Series: Series containing the feature.

    Raises:
        ValueError: If length is less than 1 or greater than the length of the
            series.
        TypeError: If `series` is not of pandas.Series type or `length` is not an
            integer.

    """

    if not isinstance(length, int):
        raise TypeError(f'`length` has to be of type int.')

    if not isinstance(series, pd.Series):
        raise TypeError(f'`series` must be of type pandas.Series.')

    if length < 1 or length > series.size:
        raise ValueError('`length` may not be less than 1 or greater than the \
                          size of the series.')

    return series.pct_change(periods=length)


def sma(series, length=6):
    """
    Simple moving average.

    Args:
        series (pandas.Series): Series of Google Trends data.
        length (int, optional): Window of the moving average. Defaults to 6.

    Returns:
        pandas.Series: Series containing the feature.

    Raises:
        ValueError: If length is less than 1 or greater than the length of the
            series.
        TypeError: If `series` is not of pandas.Series type or `length` is not an
            integer.

    """

    if not isinstance(length, int):
        raise TypeError(f'`length` has to be of type int.')

    if not isinstance(series, pd.Series):
        raise TypeError(f'`series` must be of type pandas.Series.')

    if length < 1 or length > series.size:
        raise ValueError('`length` may not be less than 1 or greater than the \
                          size of the series.')

    return series.rolling(window=length)


def ema(series, length=6):
    """
    Exponential moving average.

    Args:
        series (pandas.Series): Series of Google Trends data.
        length (int, optional): Window of the moving average. Defaults to 6.

    Returns:
        pandas.Series: Series containing the feature.

    Raises:
        ValueError: If length is less than 1 or greater than the length of the
            series.
        TypeError: If `series` is not of pandas.Series type or `length` is not an
            integer.

    """

    if not isinstance(length, int):
        raise TypeError(f'`length` has to be of type int.')

    if not isinstance(series, pd.Series):
        raise TypeError(f'`series` must be of type pandas.Series.')

    if length < 1 or length > series.size:
        raise ValueError('`length` may not be less than 1 or greater than the \
                          size of the series.')

    return series.ewm(span=length, adjust=False)


def lag(series, length=1):
    """
    Create `length` amount of lag features.

    Args:
        series (pandas.Series): Series of stock closing price.
        length (int, optional): Amount of lag features. Defaults to 1.

    Returns:
        pandas.DataFrame: DataFrame containing all the lag features.

    Raises:
        ValueError: If length is less than 1 or greater than the length of the
            series.
        TypeError: If `series` is not of pandas.Series type or `length` is not an
            integer.

    """

    if not isinstance(length, int):
        raise TypeError(f'`length` has to be of type int.')

    if not isinstance(series, pd.Series):
        raise TypeError(f'`series` must be of type pandas.Series.')

    if length < 1 or length > series.size:
        raise ValueError('`length` may not be less than 1 or greater than the \
                          size of the series.')

    lag_df = pd.DataFrame()
    for i in range(1, length):
        lag_df[f'lag_{i}'] = series.shift(i)

    return lag_df


def target_binary(series):
    """
    Convert a series of stock prices to binary: up (1), down (0). This is used for
    classifier algorithms.

    Args:
        series (pandas.Series): Series of stock closing price.

    Returns:
        pandas.Series: Series containing the stock closing price in binary.

    Raises:
        TypeError: If `series` is not of pandas.Series type.

    """

    if not isinstance(series, pd.Series):
        raise TypeError('`series` must be of type pandas.Series.')

    pct_change = series.pct_change()
    binary_series = pd.cut(
        pct_change, bins=[-float('inf'), 0, float('inf')], labels=False)

    return binary_series


def target_bins(series, bins=6):
    """
    Convert a series of stock prices to bins; used for classifier algorithms.

    Args:
        series (pandas.Series): Series of stock closing price.
        bins (int, optional): Amount of bins used. Defaults to 6.

    Returns:
        pandas.Series: Series containing the stock closing price in specified
            amount of bins.

    Raises:
        TypeError: If `series` is not of pandas.Series type or `bins` is not an
            integer.

    """

    if not isinstance(bins, int):
        raise TypeError('`bins` must be of type int.')

    if not isinstance(series, pd.Series):
        raise TypeError('`series` must be of type pandas.Series.')

    pct_change = series.pct_change()
    bins_series = pd.cut(pct_change, bins=bins, labels=False)

    return bins_series
