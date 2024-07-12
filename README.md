# Data Scraping
This back-end code is designed to scrape data from multiple URLs. The project’s primary purpose is to extract information from climate change articles for non-profit or study-related purposes.

## Purpose
The tool is intended for non-profit use or academic research.

## Data Collection Process
The app accesses a file named `data.xlsx`, which contains a list of URLs.
It then searches for specific tags on those web pages.
The collected data is saved into a file called `ClimateChangeData.xlsx`.

## Adding New URLs
If you want to scrape data from different websites, simply modify the `data.xlsx` file in the `Data` folder.

## Empty Data
Occasionally, you may encounter empty data entries.
This can happen because some websites employ robots that detect scraping tools like this one.
These robots introduce delays when opening pages, and since the tool collects data too quickly, it might appear empty.

> [!CAUTION]
> Remember to use this tool responsibly and within the specified guidelines. 🌍🔍
