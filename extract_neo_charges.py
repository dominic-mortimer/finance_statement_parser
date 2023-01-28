import os
import sys
from selenium import webdriver
import time
import re
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

def extract_neo_charges(month_of_interest):

    #####################################################################################################################
    # open some required information from saved text file
    #####################################################################################################################

    with open('info.txt', 'r') as f:
        chars_to_remove = f.readline()
        password = f.readline()
    chars_to_remove = chars_to_remove[0]

    month_to_year_dict = {
        'Oct' : '2022',
        'Nov' : '2022',
        'Dec' : '2022',
        'Jan' : '2023'
    }

    #####################################################################################################################
    # leverage selenium to login and extract charges
    #####################################################################################################################

    driver = webdriver.Chrome('chromedriver')
    driver.get('https://member.neofinancial.com/login')

    # click into email section
    email_field = driver.find_element("xpath", '/html/body/div[1]/main/div[2]/div[1]/div[2]/div/div/form/div[1]/div[1]/label')
    time.sleep(1.1)
    email_field.click()

    time.sleep(1.1)

    # enter your email
    type_field = driver.find_element('id', 'email-login')
    time.sleep(1.1) 
    type_field.send_keys('dominic.mortimer99@gmail.com')

    time.sleep(1.1)

    # click into password section
    password_field = driver.find_element('xpath', '/html/body/div[1]/main/div[2]/div[1]/div[2]/div/div/form/div[2]/div[1]/label')
    time.sleep(1.1) 
    password_field.click()

    time.sleep(1.1)

    # enter password
    type_field = driver.find_element('id', 'password-login')
    time.sleep(1.1)
    type_field.send_keys(password)

    time.sleep(1.1)

    # click the sign in option
    sign_in = driver.find_element('xpath', '/html/body/div[1]/main/div[2]/div[1]/div[2]/div/div/form/button/span[1]/span')
    time.sleep(1.1)
    sign_in.click()

    # allow time for page to load
    time.sleep(5.1)

    # click into transactions page
    element = driver.find_element('xpath', "/html/body/div[1]/div/div[3]/nav/div[2]/nav/div[1]/div[1]/div[2]/div/div/div[1]/div/div/p")
    driver.execute_script("arguments[0].click();", element)

    # ask user to scroll to desired depth
    os.system('cls' if os.name == 'nt' else 'clear')
    answer = input("\n Scroll to the depth of the transactions page you'd like to scrape, press enter when complete. \n\n")

    # let the user know that we're closing the driver
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Closing the web driver...', end='\n\n')

    # select element that holds the transactions and extract the text
    element = driver.find_element('xpath', '/html/body/div[1]/div/div[3]/main/div/div[3]/main/div')
    time.sleep(1.1)
    charges = element.text
    time.sleep(1.1)

    driver.close()
    driver.quit()

    print('Done', end='\n\n')

    ##################################################################################################################
    # separate out the charges by month
    ##################################################################################################################

    print('Extracting and cleaning charge data...')

    # initialize months of year
    months_of_year = 'January|February|March|April|May|June|July|August|September|October|November|December'

    # in list of charges, find indices for start of each month
    indices_of_month_starts = [m.start() for m in re.finditer(months_of_year, charges)]

    # initialize dict to hold charges by month
    charges_dict = {}

    # loop through all indices we pulled out up top
    for i, month_charges in enumerate(indices_of_month_starts):

        ending = len(charges) if (i + 1) == len(indices_of_month_starts) else indices_of_month_starts[i + 1]
        charges_dict[charges[month_charges:month_charges + 3]] = charges[month_charges:ending]

    ##################################################################################################################
    # loop through months, extract charges into a df
    ##################################################################################################################

    # At this point, we have a dict where the keys represent the month of interest, and the values represent the charges (as a string)
    # Let's loop through the months of interest and extract the charges into a df

    # initialize empty df
    final_df = pd.DataFrame(columns=['month', 'date', 'place', 'charge'])

    # loop through the months in the charges
    for key in charges_dict.keys():
        
        # extract the charges for month of interest and convert to list
        charge_list = charges_dict[key].split('\n')[1:]
        charge_list = charge_list if charge_list[-1] != '' else charge_list[:-1]

        # pull out the rows which correspond to rewards earned
        reward_indices = []
        rewards = []
        for i, charge in enumerate(charge_list):
            if '+$' in charge:
                reward_indices.append(i)
                rewards.append(charge)

        # delete all rows which correspond to rewards earned
        for i in sorted(reward_indices, reverse=True):
            del charge_list[i]

        # initialize place, charge and date lists (will later be converted into df)
        places = []
        charges = []
        dates = []

        # loop through the charge list
        for i, item in enumerate(charge_list):

            # append item to places, charge or date list depending on what it is
            j = i + 1
            if j % 3 == 1:
                places.append(item)
            elif j % 3 == 2:
                charges.append(item)
            else:
                dates.append(item)
                
        # create df of charges for month of interest
        df = pd.DataFrame({
            'month' : [key] * len(dates),
            'date' : dates,
            'place' : places,
            'charge' : charges
        })
        
        # we get funny characters on lines where charges were declined, for now we'll just remove these lines
        df = df.loc[~((df['date'].str.contains(chars_to_remove)) & (df['date'].str.contains('Declined'))), :]

        # pending charges have a funny format, needs fixing
        df['date'] = np.where((df['date'].str.contains(chars_to_remove)) & (df['date'].str.contains('Pending')),
                        df['date'].str.split(chars_to_remove).str[0],
                        df['date'])

        # process the charge data
        df['charge'] = df['charge'].str.replace(',', '')
        df['charge'] = df['charge'].str.replace('$', '').astype('float')
        
        # process the date data
        df['date'] = month_to_year_dict[key] + ' ' + df['date']
        df['date'] = pd.to_datetime(df['date'], format='%Y %b %d')
        
        # append back to final df
        final_df = pd.concat([df, final_df])

        os.system('cls' if os.name == 'nt' else 'clear')

    # return the subset of the df corresponding to the month of interest
    final_df = final_df.loc[final_df['month'] == month_of_interest, ['date', 'place', 'charge']]
    return final_df.sort_values('date').reset_index().drop('index', axis=1)