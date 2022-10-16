import pdfplumber as pdfp
import pandas as pd
import numpy as np
import warnings
import os
import time

warnings.filterwarnings('ignore')

###################################################################################################################
# Get the year and month that the user wants to analyze
###################################################################################################################

# clear the screen and get the input
os.system('cls' if os.name == 'nt' else 'clear')

year_ = input('\n What year are you looking to analyze? \n\n')
assert int(year_) in (2021, 2022), 'Invalid year entered'
month_ = input('\n What month are you looking to analyze? (1 - 12) \n\n')
assert int(month_) in list(np.arange(1, 13)), 'Invalid month entered'

# re-structure the input in such a way that we can use it
if int(month_) < 10:
    month_ = '0' + month_
month = year_[-2:] + '-' + month_

time.sleep(1)
print(f'\n\n Processing data for {month}...')
time.sleep(2)

###################################################################################################################
# loading the data
###################################################################################################################

pages = []

# open pdf statement, read each page and extract the text line by line, save results
with pdfp.open(f'Credit Card Statements/{month}.pdf') as pdf:

    for page in pdf.pages:
        pages.append(page.extract_text().split('\n'))

    for i, page in enumerate(pages):
        if i == 0:
            df = pd.DataFrame(page, columns=['text'])
        else:
            new_df = pd.DataFrame(page, columns=['text'])
            df = pd.concat([df, new_df])

###################################################################################################################
# some data cleaning
###################################################################################################################

# drop null values
df = df.dropna()

# select only lines that have a date associated with them
df = df.loc[df['text'].str[:3].str.contains('JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC'), :]

# split the date, description and amount out into their own columns
df['date'] = df['text'].str.split(' ').str[0]
df['place'] = df['text'].str.split(' ').str[2]
df['amount'] = df['text'].str.split(' ').str[3]

# reset the index and drop unnecessary columns
df = df.reset_index().drop(['index', 'text'], axis=1)
df = df.rename(columns={
    'date' : 'Date', 
    'place' : 'Place', 
    'amount' : 'Amount'
})

# touch up the amount column so that it will be formatted as a number in google sheet
df['Amount'] = df['Amount'].str.replace(',', '').str.replace('\$', '')

###################################################################################################################
# exclude entries which are recurring payments
###################################################################################################################

recurring_payments = 'spotify'\
                     '|fido'\
                     '|payment-thankyou'\
                     '|tsiinternet'
  
os.system('cls' if os.name == 'nt' else 'clear')
print('Recurring payments (not included in analysis): ', end='\n\n')
for item in recurring_payments.split('|'):
    print(f'\t{item}')

answer = input('\n Do the recurring payments look correct? (y/n): ')
assert answer == 'y', 'Better update it!'

df = df.loc[~df['Place'].str.lower().str.contains(recurring_payments), :]

###################################################################################################################
# set up the keywords which will be used to group the charges
###################################################################################################################

on_the_go_coffee = 'timhortons'\
                   '|starbuck'\
                   '|coffee'\
                   '|timothy'\
                   '|balzac'\
                   '|madawaskacoffee'\
                   '|secondcup'

beer_and_weed = 'lcbo'\
                '|beerstore'\
                '|oneplant'

take_out = 'subway'\
           '|domino'\
           '|a&w'\
           '|zoup'\
           '|amazing'\
           '|maestro'\
           '|emily'\
           '|vipei'\
           '|bigbrother'\
           '|booster'\
           '|freshly'\
           '|northwinds'\
           '|jerk'\
           '|milkylane'\
           '|burrito'\
           '|jusdanfoods'\
           '|cornwall'\
           '|bastard'\
           '|rolltation'\
           '|shawarma'\
           '|carleton'\
           '|doordash'\
           '|mcdonald'\
           '|caesar'

bars_and_restaurants = 'jackastor'\
                       '|portly'\
                       '|oldestone'\
                       '|magwyer'\
                       '|kelsey'\
                       '|chuuk'\
                       '|lacarnita'\
                       '|smitty'\
                       '|milestone'\
                       '|wildwing'\
                       '|popeyes'\
                       '|prenup'\
                       '|moose'\
                       '|sabai'\
                       '|borealis'\
                       '|thepint'\
                       '|chicago'\
                       '|spaghetti'\
                       '|bmofield'\
                       '|yummykorean'\
                       '|eggsmart'\
                       '|aokcraft'\
                       '|legendsmusic'\
                       '|aramark'\
                       '|cineplex'

clothing = 'zara'\
           '|h&m'\
           '|aeo'\
           '|softmoc'\
           '|vans'\
           '|jack&jones'\
           '|oldnavy'\
           '|sportchek'

grocery = 'rcss'\
          '|freshco'\
          '|wal-mart'\
          '|nofrills'\
          '|loblaws'\
          '|zehrs'\
          '|metro'\
          '|foodbasics'\
          '|nikufarms'

gas = 'shell'\
      '|petro'\
      '|macewen barrys'\
      '|pioneer'

###################################################################################################################
# assert that we're not double counting any charges by placing them in multiple categories
###################################################################################################################

cats = {
    'on_the_go_coffee' : on_the_go_coffee,
    'take_out' : take_out,
    'bars_and_restaurants' : bars_and_restaurants,
    'clothing' : clothing,
    'grocery' : grocery,
    'gas' : gas
}

for cat1 in cats:
    
    for cat2 in cats:
        
        if cat1 == cat2:
            continue
        else:
            for merchant in cats[cat1].split('|'):
                assert merchant not in cats[cat2].split('|'), \
                f'{cat1} contains duplicate values with {cat2}, duplicate value: {merchant}'

                
###################################################################################################################
### show the user what is in each category
###################################################################################################################

for i, cat in enumerate(cats):
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n')
        
    print(f'{cat}: \n')
    for item in cats[cat].split('|'):
        
        print(f'\t{item}')
        
    answer = input('\n Does this category look correct? (y/n): ')
    assert answer == 'y', 'Better change it!'

    
###################################################################################################################
### show the user what is leftover (i.e. what was not caught by their keywords)
###################################################################################################################

# clear the terminal screen
os.system('cls' if os.name == 'nt' else 'clear')

# generate full list of categorized charges
full_list = on_the_go_coffee + '|' + beer_and_weed + '|' + take_out + '|' + \
            bars_and_restaurants + '|' + clothing + '|' + grocery + '|' + gas

# use this to find uncategorized charges
tmp = df.loc[~df['Place'].str.lower().str.contains(full_list), ['Place', 'Amount']]
tmp.index = np.arange(1, len(tmp) + 1)
print('\n\n', f'{tmp.shape[0]} leftover (uncategorized) charges: \n\n', tmp, '\n\n')

# check with user that the uncategorized charges are correct
answer = input('These will all go into the misc category, anything in here that you would like to add to a category? (y/n): ')
assert answer == 'n', 'Please add to the categories as needed'

# touch up the final version of the misc charges
misc_charges = tmp['Place'].unique()
misc = ''

for misc_charge in misc_charges:
    misc = misc + '|' + misc_charge
    
misc = misc.strip('|').lower()

###################################################################################################################
### aggregate the totals by category, show final output
###################################################################################################################

# clear the terminal screen
os.system('cls' if os.name == 'nt' else 'clear')

# aggregate regular categories
cat_names = [cat for cat in cats]
final_df = pd.DataFrame(columns=cat_names)
for cat in cats:
    final_df.loc[0, cat] = df.loc[df['Place'].str.lower().str.contains(cats[cat]), 'Amount'].astype('float64').sum()

# aggregate the misc category
final_df.loc[0, 'misc'] = df.loc[df['Place'].str.lower().str.contains(misc), 'Amount'].astype('float64').sum()

# show output
print('Final output: ', end='\n\n')
for col in final_df.columns:
    col1 = col + ': '
    print(f'{col1}{round(final_df[col][0])}')
print('\n\n')