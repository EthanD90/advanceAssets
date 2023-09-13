import undetected_chromedriver as uc 
import time 
import os
import pandas as pd
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from keycloak import KeycloakOpenID
from bs4 import BeautifulSoup
from data_cleaner import clean_advance_data

# Initialise dotenv to enable parsing of .env file
load_dotenv()
user = os.environ.get('KEYCLOAK_USER')
key_pass = os.environ.get('KEYCLOAK_PASS')

# Advance use Keycloak as their authentication redirect. Setup a token token query for each connection to the auth URL.
keycloak_openid = KeycloakOpenID(server_url = "https://keycloak.intequip.co.uk/auth/",
                                 client_id = "OneClick",
                                 realm_name = "Advance"
                                 )
token = keycloak_openid.token(user, key_pass)

# auth_URL is to direct the undetected_chromedriver to the initial login page for authentication
auth_URL = "https://www.intequip.co.uk/OneClick/secure/postloginredirect"
# Initialise the undetected_chromedriver and pass options to run headless and suppress security pop-ups
chromeOptions = uc.ChromeOptions() 
chromeOptions.add_argument('--headless')
prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled": False}
chromeOptions.add_experimental_option("prefs", prefs)
driver = uc.Chrome(use_subprocess=True, options=chromeOptions) 

# Set driver to auth_url to start authentication process and wait for login to appear
driver.get(auth_URL)
time.sleep(2)
#print(str(driver.current_url)) #<<< Uncomment for debugging >>>

# Setup access credentials from .env to pass to Keycloak authentication screen, enter credentials and login.
uname = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
uname.send_keys(user)
password.send_keys(key_pass)
driver.find_element(By.ID, "kc-login").click()
time.sleep(5)
#print(str(driver.current_url)) #<<< Uncomment for debugging >>>

# Find and click the Asset Detail link to access the asset tables for each venue
driver.find_element(By.ID, "centerForm:j_idt74").click()
time.sleep(5)
#print(str(driver.current_url))

# Create list of row numbers relating to each venue for asset scraping
venues = [2, 3, 4]
# Initialise empty list to store dataframes from for loop
cleaned_data = []
# Open table_head document and store the string in thead. This will be passed to full_html to construct the HTML tables for parsing
file = open('./table_head.txt', 'r')
thead = file.read()

for venue in venues:
    # Find and click the relevant table row based on the venue in the current iteration
    driver.find_element(By.XPATH, f"//table/tbody/tr[{venue}]").click()
    #print(str(driver.current_url)) #<<< Uncomment for debugging >>>
    time.sleep(2)
    print('Retrieving data from Venue_{}: {}'.format(venue, driver.current_url))

    # Find and access HTML of the venue asset table using the CLASS_NAME of the relevant <div>
    page1_html = driver.find_element(By.CLASS_NAME, "ui-datatable-tablewrapper")
    page1_html = page1_html.get_attribute("innerHTML")

    # Filter only on-site assets by looking for first occurence of the class names on each row 
    soup = BeautifulSoup(page1_html, 'html.parser')
    rows = soup.select('tbody#centerForm\\:assetListTable_data tr')
    filtered_rows = [row for row in rows if row.select_one('td i.mdi').get('class') == ['mdi', 'mdi-check', 'green', 'fa-15x']]
    filtered_html = '\n'.join(str(row) for row in filtered_rows)

    # Check number on-site assets in filtered html from page 1 of the assets table
    asset_count = str(filtered_html).count('<tr aria-selected')

    """
    _______________________________________________________________________
    The following IF statment checks if the returned asset list in the HTML
    is exactly 50 items. The table pagination is 50, so if we reach this
    number, we have to find and click the NEXT button on the paginator
    element. 
    We then repeat the process of extracting the on-site assets using
    BeatifulSoup html.parser and return the combined HTML of each page
    OR we return only the first page if asset_count < 50.
    _______________________________________________________________________
    """
    if asset_count == 50:
        driver.find_element(By.CSS_SELECTOR, "[aria-label='Next Page']").click()
        time.sleep(3)
        pageN_html = driver.find_element(By.CLASS_NAME, "ui-datatable-tablewrapper")
        pageN_html = pageN_html.get_attribute('innerHTML')
        soupN = BeautifulSoup(pageN_html, 'html.parser')
        rowsN = soupN.select('tbody#centerForm\\:assetListTable_data tr')
        filtered_rowsN = [row for row in rowsN if row.select_one('td i.mdi').get('class') == ['mdi', 'mdi-check', 'green', 'fa-15x']]
        filtered_htmlN = '\n'.join(str(row) for row in filtered_rowsN)
        full_html = f'<table>{thead}<tbody>{filtered_html}{filtered_htmlN}</tbody></table>'
    else:
        full_html = f'<table>{thead}<tbody>{filtered_html}</tbody></table>'

    # Use pandas to return a list of dataframes from the full_html
    # Access the first list element and pass this to a pd.DataFrame()
    df = pd.read_html(full_html)
    df = df[0]
    df = pd.DataFrame(df)

    """
    __________________________________________________________________________
    Below we pass the dataframe to the clean_advance_data helper function to:
    1) Extract Equipment cell data into 4 new columns - 
        * Manufacturer
        * Product
        * Asset No
        * Serial No
    2) Rename columns to be more logical
    3) Change dtypes of numeric fields from object > numeric
    4) Remove special characters from currency columns
    5) Drop empty columns
    6) Rearrange the columns to be more logical

    A new Venue column is then added to the dataframe based on the {venue}
    integer value, cleaned dataframe is then appended to the cleaned_data
    list.
    __________________________________________________________________________
    """
    cleaned_df = clean_advance_data(df)

    if venue == 2:
        cleaned_df = cleaned_df.copy()
        cleaned_df['Venue'] = 'Venue 1'
    elif venue == 3:
        cleaned_df = cleaned_df.copy()
        cleaned_df['Venue'] = 'Venue 2'
    else:
        cleaned_df = cleaned_df.copy()
        cleaned_df['Venue'] = 'Venue 3'
    cleaned_data.append(cleaned_df)

    driver.back() #<<< Steps the browser driver back to the venues table
    time.sleep(3)

# Create a dataframe by concatenating all cleaned_data in the list then save to a csv file
now = time.strftime('%Y%m%d-%H%M%S')
df_allVenues = pd.concat(cleaned_data, ignore_index=True)
df_allVenues.to_csv('./output/allVenues__OSassets_'+now+'.csv', index=False)
