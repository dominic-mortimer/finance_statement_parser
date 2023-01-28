import charge_categorizer as cc
import datetime as dt
import pandas as pd
import os
import sys
import time

# assert that the command line argument was given as expected, save the value
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
assert any(x in sys.argv[1] for x in months), \
    f'We were expecting a month as a command-line argument!  Please input with one of the following values: \n\n{months}'
month_of_interest = sys.argv[1]

#######################################################################################################################
# check if we've already done this month, if so we load and print the results
#######################################################################################################################

if os.path.isfile(f'Summarized Charges/neo_{month_of_interest}.csv'):

    # clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(2)

    # let the user know that we've done this month already
    print('This month has already been categorized.', end='\n\n')
    time.sleep(1)
    print('Gathering charges and category summary...')
    time.sleep(2)

    # retrieve the saved results
    charges = pd.read_csv(f'Summarized Charges/neo_{month_of_interest}.csv')
    summary = pd.read_csv(f'Summarized Charges/neo_{month_of_interest}_summary.csv')

    # show summary
    print('\n')
    print('Final result: ', end='\n\n')
    for col in summary.columns:
        charge = round(summary[col][0])
        print(f'{col} : ${charge}.00')

    # show the total spend for the month
    print('\n')
    tmp = summary.drop('grocery', axis=1)
    print(f'Total spend for {month_of_interest}: ', f'${round(summary.sum(axis=1)[0])}.00', end='\n\n')

    # ask user if they'd like to see detailed breakdown
    answer = input('Would you like to see the detailed breakdown? (y/n): ')
    if answer == 'y':
        print('\n\n', charges)

#######################################################################################################################
# if we haven't done this month, that means it's the latest one
#######################################################################################################################

else:
        
    # extract and analyze the charges
    charges, charges_summary = cc.charge_categorizer(month_of_interest)

    # get the cutoff for being done this month
    start_of_next_month_dict = {
        'Oct' : dt.datetime(2022, 11, 1).date(),
        'Nov' : dt.datetime(2022, 12, 1).date(),
        'Dec' : dt.datetime(2023, 1, 1).date(),
        'Jan' : dt.datetime(2023, 2, 1).date()
    }
    start_of_next_month = start_of_next_month_dict[month_of_interest]

    # if we're done this month, save the results
    if dt.date.today() >= start_of_next_month:
        charges_summary.to_csv(f'Summarized Charges/neo_{month_of_interest}_summary.csv', index=False)
        charges.to_csv(f'Summarized Charges/neo_{month_of_interest}.csv', index=False)