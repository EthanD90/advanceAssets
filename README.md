﻿# asset_data_scraper

# Automated Asset Data Scraper

This Python script automates the process of scraping asset data from a web application that uses Keycloak for authentication and displays asset information in HTML tables. The scraped data is then cleaned and saved to a CSV file.

## Prerequisites

Before using this script, make sure you have the following prerequisites installed:

- [Python](https://www.python.org/) (3.x)
- [undetected_chromedriver](https://pypi.org/project/undetected-chromedriver/)
- [pandas](https://pandas.pydata.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [selenium](https://pypi.org/project/selenium/)
- [keycloak](https://pypi.org/project/python-keycloak/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [data_cleaner](https://pypi.org/project/data-cleaner/)

You also need to set up a Keycloak server and provide your Keycloak credentials in a `.env` file.

## Getting Started

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/yourusername/asset-data-scraper.git
   cd asset-data-scraper
