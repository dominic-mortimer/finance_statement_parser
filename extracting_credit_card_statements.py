###################################################################################################################
### import required libraries
###################################################################################################################

import pdfplumber as pdfp
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

###################################################################################################################
### load the data
###################################################################################################################

# choose a month
month = '22-07'
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
### some data cleaning
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

# drop rows with recurring charges, or entries which are recurring payments
df = df.loc[~df['Place'].str.lower().str.contains('spotify|fido|payment-thankyou|tsiinternet'), :]

###################################################################################################################
### set up the keywords which will be used to group the charges
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
                       '|aramark'

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
          '|foodbasics'

gas = 'shell'\
      '|petro'\
      '|macewen barrys'\
      '|pioneer'

###################################################################################################################
### assert that we're not double counting any charges by placing them in multiple categories
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
    
    print('\n')
        
    print(f'{cat}: \n')
    for item in cats[cat].split('|'):
        
        print(f'\t{item}')
        
    answer = input('\n Does this category look correct? (y/n): ')
    assert answer == 'y', 'Better change it!'