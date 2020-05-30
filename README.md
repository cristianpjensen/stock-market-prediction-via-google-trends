<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="images/njord_logo.svg" alt="Project logo"></a>
</p>

<h3 align="center">Njord</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]() 
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Njord attempts to predict future stock prices based on Google Trends data - using a neural network.
    <br> 
</p>

## Table of Contents
- [About](#about)
- [Data](#data)
  - [Data Collection](#data_collection)
  - [Data Visualization](#data_visualization)
  - [Restrictions](#restrictions)
  - [Method](#method)
    - [Example](#example_merge)

## About <a name = "about"></a>

The data used by Njord is directly downloaded from [Google Trends](https://trends.google.com). The concept for this project came from this [research (PDF)](https://www.nature.com/articles/srep01684.pdf). In this research was found that the search volume for certain (financial) words are linked to the stock price of the Dow Jones Industrial Average stock price, and can in most cases predict a dip in the market. The purpose of this project is to combine this research with machine learning.

## Project Status

This project is currently under development. All data has been collected and cleaned for Njord's usage.

## Installation and Setup Instructions

> TODO

## Reflection

> TODO

## Data <a name = "data"></a>

### Data Collection <a name = "data_collection"></a>

Two datasets were needed for this project; the Google Trends daily data for a specific keyword, and the stock price daily data for a specific ticker. To collect the Google Trends daily data, you have to download all 6-month increments, 5-year increments, and 2004-present within the 2004-2020 timespan. All this data will eventually be adjusted to be relative to eachother, instead of only within it's respective timepsan. To collect the stock price daily data for a specific ticker you want to predict, you have to download it from a website like [Yahoo Finance](https://finance.yahoo.com), where you can download the historical data of any ticker.

### Data Visualization <a name = "data_visualization"></a>

To prove that there indeed is a correlation between Google Trends data (e.g. 'debt'), and stock prices (e.g. Dow Jones Industrial Average). I created a graph plotting these two against eachother:

<p align="center">
  <img src="images/graphs/debt_vs_djia.svg" width=600>
</p>

<p align="center">
  The red indicates a spike in amount of searches, and the green indicates a dip in the stock market.
</p>

After all adjustments of the data to eventually get daily data - which is actually relative to eachother - the data looks like this:

<p align="center">
  <img src="images/graphs/interpolated_daily.svg" width=600>
</p>

### Restrictions <a name = "restrictions"></a>

All data on Google Trends is relative to eachother within one timeframe (0-100), and you can only get daily data in 6-month increments, weekly data in 5-year increments, and only monthly data is provided for the entire timespan available. So to aggregate all data needed for this project was quite a challenge, and because of these restrictions aren't completely accurate, however the method I used was the only method to getting daily data over the entire timespan available (which was crucial for this project). However, I was determined to make it work.

### Method <a name = "method"></a>

To get all the data relative to eachother, instead of only within it's 6-month increment. I had to merge them together based on weekly data. However, the weekly data is only available in 5-year increments, so I had to merge these 5-year increments together based on the monthly data, which is available for timespan needed for this project. To merge all the 6-month, and 5-year increments, I computed the percentage change of each data point within it's respective increment. Afterwards I got one data point (from the weekly data) per increment, and computed the missing days by applying the percentage change to the provided data point.

#### Example <a name = "example_merge"></a>

An example for the search term 'debt' - 'debt' is the best search term to predict market change - in the timespan 2007-2009:

Before adjustments:

<p align="center">
  <img src="images/graphs/example_unadjusted_graph.svg" width=600>
</p>

<p align="center">
  The black vertical lines indicate the edges of the 6-month increments.
</p>

After adjustments:

<p align="center">
  <img src="images/graphs/example_interpolated_graph.svg" width=600>
</p>

Weekly data points:

<p align="center">
  <img src="images/graphs/example_actual_weekly_graph.svg" width=600>
</p>

