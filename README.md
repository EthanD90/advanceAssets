# asset_data_scraper

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

2. Install the required Python packages.

```bash
pip install undetected-chromedriver pandas python-dotenv selenium python-keycloak beautifulsoup4 data-cleaner
```

3. Create a .env file in the project directory and add your Keycloak username and password.

```bash
KEYCLOAK_USER=your_username
KEYCLOAK_PASS=your_password
```

4. Run the script.

```bash
python asset_scraper.py
```

### Usage
The script automates the authentication process with Keycloak and scrapes asset data from the web application.
Cleaned asset data is saved to a CSV file in the ./output directory.

### Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

