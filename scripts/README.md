# Documentation

## `data_collection.py`

### Purpose

The purpose of this file is to pull data from Google Trends. Google Trends doesn't have an API, so that is the gap that `data_collection.py` is filling. It first pulls all data in the appropriate timeframes (due to daily and weekly data only being available in specific lengths of time). Then it adjusts the data, because all data is relative within its timeframe.

### `keywords.txt`

`keywords.txt` plays a big role in the function of the script. This txt-file contains the keywords that `data_collection.py` will pull. In case the script terminates (due to too many requests not being allowed by Google), you don't need to remove the already downloaded keywords from `keywords.txt`. The script skips over already downloaded keywords.

### Usage

To use the script, you need to put in the keywords you want to download. Afterward, you can simply use `python3 scripts/data_collection.py` in your terminal and it will start downloading the search volume history of all keywords specified by the `keywords.txt`-file. This takes a considerate amount of time, due to Google not allowing too many requests consecutively. Thus the requests are spaced out by 90 seconds. In case a request has failed three times in a row, the script terminates. 

## `feature_engineering.py`

### Purpose

The purpose of this file is to manipulate the data—which was pulled and stored by `data_collection.py`. The script takes in all the CSV-files for the different keywords. It produces a CSV-file, where the manipulated data is stored. This data is manipulated based on the parameters specified in the command-line.

There are multiple parameters, which can be customised. The default settings for `interval`, `N`, `offset`, `type`, `target`, and `curated` is `weekly`, `3`, `pct_change`, `binary`, and `False` respectively. If a setting is not set, the default setting will be used for that parameter.

In the next section is a table with a further explanation on the parameters.

### Parameters

| Parameter | Alias | Description |
| :-------- | :---: | ----------- |
| `--interval`=`daily`\|`weekly` | `-i` | The intervals in which the data occurs. Either set at daily or weekly intervals. |
| `--n`=<br>`0 < N < 100` | `-n` |  The difference between the compared data points. For example when N is set at 3, weekly intervals, and the type is delta. Then the data point at T = Δ(T-1, T-4). |
| `--offset`=<br>`0 <= OFFSET < 100` | `-o` | The offset of the data. Sometimes an offset is needed, because daily data is available three days after the fact. So, an offset of 3 is crucial. If you don't have an offset, you are giving a model data, which isn't actually available at the time you are saying it is. |
| `--type`=<br>`delta`\|`pct_change`\|`rolling` | `-t` | You also have to specify which feature you want to use.<br> * `delta`: <img src="https://render.githubusercontent.com/render/math?math=n(t) = \Delta (n_{t-1}, n_{t-(N%2B1)})">;<br> * `pct_change`: <img src="https://render.githubusercontent.com/render/math?math=n(t) = \frac{\Delta (n_{t-1}, n_{t-(N%2B1)})}{n_{t-1}}">;<br> * `rolling`: <img src="https://render.githubusercontent.com/render/math?math=\overline n_\text{SM} = \frac {n_t%2Bn_\text{t-1}%2B\cdots%2Bn_{t-(N-1)}}{N}">. |
| `--target`=`binary`\|`bins` | `-r` | The choice is either binary—up (1) or down (0). Or bins, which is `-6` through `6` ranging from `-0.025` to `0.025` with a step of `0.05`. |
| `--curated`=`True`\|`False` | `-c` | Determine whether or not the used keywords will be curated, based on my own observations. The curated keywords are based on an observed correlation between the keyword and the stock price of DJIA. To add/remove keywords in the curated list, you can modify the [`curated.txt`](https://github.com/cristianpjensen/Njord/blob/master/scripts/curated.txt)-file. |

### Usage

`feature_engineering.py` can only be used via the command-line. In your terminal, type in `python3 scripts/feature_engineering.py` followed by the parameters laid out above. E.g. `python3 scripts/feature_engineering.py -i weekly -n 3 -o 0 -t pct_change -r binary -curated True`. The example produces [this CSV-file](https://github.com/cristianpjensen/Njord/blob/master/data/feature_engineered/weekly-pct_change-binary.csv).
