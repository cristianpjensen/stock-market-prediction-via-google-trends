# Documentation

## `make_dataset.py`

### Purpose

The purpose of this file is to pull data from Google Trends. Google Trends doesn't have an API, so that is the gap that `make_dataset.py` is filling. It first pulls all data in the appropriate timeframes (due to daily and weekly data only being available in specific lengths of time). Then it adjusts the data, because all data is relative within its timeframe.

### `keywords.txt`

`keywords.txt` plays a big role in the function of the script. This txt-file contains the keywords that `make_dataset.py` will pull. In case the script terminates (due to too many requests not being allowed by Google), you don't need to remove the already downloaded keywords from `keywords.txt`. The script skips over already downloaded keywords.

### Usage

To use the script, you need to put in the keywords you want to download. Afterward, you can simply use `python3 src/data/make_dataset.py` (or `make data`) in your terminal and it will start downloading the search volume history of all keywords specified by the `keywords.txt`-file. This takes a considerate amount of time, due to Google not allowing too many requests consecutively. Thus the requests are spaced out by 90 seconds. In case a request has failed three times in a row, the script terminates. 

## `build_features.py`

### Purpose

The purpose of this file is to provide functions, which can be used to create features of the raw data.

### Documentation

| Function | Arguments | Description |
| :-- | --- | --- |
| `research(series, length)` | - `series` (pandas.Series): Series of the Google Trends data; <br> - `length` (int, optional): Length of the moving average used in the calculation. Defaults to 3. | The same feature used in the paper by Tobias Preis et al. <br> <img src="https://render.githubusercontent.com/render/math?math=Research_t = n_t - \frac{n_{t-1} %2B n_{t-2} %2B \cdots %2B n_{t-length}}{length}"> |
| `delta(series, length)` | - `series` (pandas.Series): Series of Google Trends data; <br> - `length` (int, optional): Difference between the two values of which the delta is calculated. Defaults to 3. | Feature based on the delta between two values `length` away. <br> <img src="https://render.githubusercontent.com/render/math?math=Delta_t = n_t - n_{t-length}"> |
| `sma(series, length)` | - `series` (pandas.Series): Series of Google Trends data. <br> - `length` (int, optional): Window of the moving average. Defaults to 6. | Simple moving average. <br> <img src="https://render.githubusercontent.com/render/math?math=SMA_t = \frac{n_t %2B n_{t-1} %2B \cdots %2B n_{t-length}}{length}"> |
| `ema(series, length)` | - `series` (pandas.Series): Series of Google Trends data. <br> - `length` (int, optional): Window of the moving average. Defaults to 6. | Exponential moving average. <br> <img src="https://render.githubusercontent.com/render/math?math=EMA_t = n_t * \frac{2}{length %2B 1} + EMA(2_{t-1}) * (1 - \frac{2}{length %2B 1})"> |
| `lag(series, length)` | - `series` (pandas.Series): Series of stock closing price. <br> - `length` (int, optional): Amount of lag features. Defaults to 1. | Create `length` amount of lag features. <br> <img src="https://render.githubusercontent.com/render/math?math=lag_t = n_{t-length}"> |
| `target_binary(series)` | - `series` (pandas.Series): Series of stock closing price. | Convert a series of stock prices to binary: up (1), down (0). This is used for classifier algorithms. |
| `target_bins(series, bins)` | - `series` (pandas.Series): Series of stock closing price. <br> - `bins` (int, optional): Amount of bins used. Defaults to 6. | Convert a series of stock prices to bins; used for classifier algorithms. |

To see even more extensive documentation, use `help(FUNCTION)` in a jupyter notebook.
