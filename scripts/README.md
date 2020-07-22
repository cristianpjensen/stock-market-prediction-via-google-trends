# Documentation

## `feature_engineering.py`

### Purpose

The purpose of this file is to manipulate the data—which was pulled and stored by `data_collection.py`. The script takes in all the CSV-files for the different keywords. It produces a CSV-file, where the manipulated data is stored. This data is manipulated based on the parameters specified in the command-line.

There are multiple parameters, which can be customised. The default settings for `interval`, `N`, `offset`, `type`, `target`, and `curated` is `weekly`, `3`, `pct_change`, `binary`, and `False` respectively. If a setting is not set, the default setting will be used for that parameter.

In the next section is a table with a further explanation on the parameters.

### Parameters

| Parameter | Alias | Description |
| :-------- | :---: | ----------- |
| `--interval`=`daily`\|`weekly` | `-i` | Set the interval of the features. |
| `--n`=<br>`0 < N < 100` | `-n` |  Set the N. |
| `--offset`=<br>`0 <= OFFSET < 100` | `-o` | Set the offset. |
| `--type`=<br>`delta`\|`pct_change`\|`rolling` | `-t` | Set the feature type. |
| `--target`=`binary`\|`bins` | `-r` | Set the target type. |
| `--curated`=`True`\|`False` | `-c` | Determine whether or not the used keywords will be curated, based on my own observations. The curated keywords are based on an observed correlation between the keyword and the stock price of DJIA. To add/remove keywords in the curated list, you can modify the [`curated.txt`](https://github.com/cristianpjensen/Njord/blob/master/scripts/curated.txt)-file. |

### Usage

`feature_engineering.py` can only be used via the command-line. In your terminal, type in `python3 scripts/feature_engineering.py` followed by the parameters laid out above. E.g. `python3 scripts/feature_engineering.py -i weekly -n 3 -o 0 -t pct_change -r binary -curated True`. The example produces [this CSV-file](https://github.com/cristianpjensen/Njord/blob/master/data/feature_engineered/weekly-pct_change-binary.csv).
