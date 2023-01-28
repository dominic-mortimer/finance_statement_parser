import pandas as pd
import numpy as np
import os
import extract_neo_charges as enc


def charge_categorizer(month_of_interest):

    # can either run the extraction script, or if doing quick analysis can load example data
    df = enc.extract_neo_charges(month_of_interest)

    # uncomment to load example data
    # df = pd.read_csv('example_total_charges.csv')
    # df = df.loc[df['month'] == month_of_interest, :].sort_values('date').reset_index().drop('index', axis=1)

    # quick edits to data
    df['place'] = df['place'].str.lower()
    df['charge'] = df['charge'] * -1

    ###################################################################################################################
    # show the list of charges and ask if anything should be ignored this time around
    ###################################################################################################################

    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n All charges: ')
    pd.set_option('display.max_rows', None)
    print(df[['date', 'place', 'charge']], end='\n\n')
    pd.reset_option('max_rows')

    payments_to_ignore = 'westjet'\
                        '|paybackwithpoints'\
                        '|bessadakia'\
                        '|payment received'\
                        '|bestseller ecom canada'\
                        '|rogers mobility'\
                        '|spotify'\
                        '|fido'\
                        '|tsiinternet'\
                        '|insurancecompanymarkham'\
                        '|physio studio'\
                        '|whitby physio centre'\
                        '|air canada online'

    # use this to find charges to ignore
    tmp = df.loc[df['place'].str.contains(payments_to_ignore), ['place', 'charge']]
    tmp.index = np.arange(1, len(tmp) + 1)
    print('\n\n', f'{tmp.shape[0]} recurring charges / charges to ignore: \n\n', tmp, '\n\n')

    # check with user that the charges to ignore are correct
    answer = input('These will all be ignored in the analysis, anything in here that you would like to add to a category? (y/n): ')
    assert answer == 'n', 'Please add to the categories as needed'

    # remove the charges to ignore from the charges df
    df = df.loc[~df['place'].str.lower().str.contains(payments_to_ignore), :]

    ###################################################################################################################
    # set up the keywords which will be used to group the charges
    ###################################################################################################################

    on_the_go_coffee = 'tim hortons'\
                    '|starbuck'\
                    '|coffee'\
                    '|timothy'\
                    '|balzac'\
                    '|madawaska coffee'\
                    '|second cup'\
                    '|arvo coffe'

    beer_and_weed = 'lcbo'\
                    '|the beer store'\
                    '|oneplant'\
                    '|hemisphere cannabis'

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
            '|caesar'\
            '|pizza'\
            '|papajohn'\
            '|shakeshack'\
            '|einsteinbrosbagel'\
            '|bagelsvancouver'\
            '|pizza hut'\
            '|hakka legend'\
            '|ritual-poke poke'\
            '|krispy kreme cafe'

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
                        '|cineplex'\
                        '|bar-main'\
                        '|petitami'\
                        '|brewhouse'\
                        '|irishtimespub'\
                        '|poncho'\
                        '|kingsheadpub'\
                        '|thecentralseattle'\
                        '|chachalounge'\
                        '|jamcafe'\
                        '|superflux'\
                        '|mileoneeatinghouse'\
                        '|trattoria'\
                        '|king taps'\
                        '|satay sate'\
                        '|rivoli'\
                        '|horseshoe tavern'\
                        '|activate games'\
                        '|roadhouse'\
                        '|casino resor'\
                        '|st lawrence'\
                        '|batl axe throwing'\
                        '|haute goat'

    clothing = 'zara'\
            '|h&m'\
            '|aeo'\
            '|softmoc'\
            '|vans'\
            '|jack&jones'\
            '|oldnavy'\
            '|sportchek'\
            '|winners'\
            '|spencergifts'\
            '|boathouse'\
            '|gymshark'

    grocery = 'canadian superstore'\
            '|freshco'\
            '|walmart'\
            '|no frills'\
            '|loblaws'\
            '|zehrs'\
            '|metro'\
            '|foodbasics'\
            '|niku farms'\
            '|safeway'\
            '|costco'\
            '|food market'

    gas = 'shell'\
        '|petro'\
        '|macewen barrys'\
        '|pioneer'\
        '|esso'

    ###################################################################################################################
    # assert that we're not double counting any charges by placing them in multiple categories
    ###################################################################################################################

    cats = {
        'on_the_go_coffee' : on_the_go_coffee,
        'beer_and_weed' : beer_and_weed,
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
    ### show the user what is leftover (i.e. what was not caught by their keywords)
    ###################################################################################################################

    # clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # generate full list of categorized charges
    full_list = on_the_go_coffee + '|' + beer_and_weed + '|' + take_out + '|' + \
                bars_and_restaurants + '|' + clothing + '|' + grocery + '|' + gas

    # use this to find uncategorized charges
    tmp = df.loc[~df['place'].str.lower().str.contains(full_list), ['place', 'charge']]
    tmp.index = np.arange(1, len(tmp) + 1)
    print('\n\n', f'{tmp.shape[0]} leftover (uncategorized) charges: \n\n', tmp, '\n\n')

    # check with user that the uncategorized charges are correct
    answer = input('These will all go into the misc category, anything in here that you would like to add to a category? (y/n): ')
    assert answer == 'n', 'Please add to the categories as needed'

    ###################################################################################################################
    ### aggregate the totals by category, show final output
    ###################################################################################################################

    # clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # aggregate regular categories
    cat_names = [cat for cat in cats]
    final_df = pd.DataFrame(columns=cat_names)

    # set up the category field for the 'all_charges' df
    df['category'] = ''

    # loop through the categories, add the total charges to the final_df, and add the category label to the 'all_charges' df
    for cat in cats:
        final_df.loc[0, cat] = df.loc[df['place'].str.lower().str.contains(cats[cat]), 'charge'].astype('float64').sum()
        df['category'] = np.where(df['place'].str.lower().str.contains(cats[cat]),
                                    cat,
                                    df['category'])

    df['category'] = np.where(df['category'] == '', 'misc', df['category'])

    # aggregate the misc category
    final_df.loc[0, 'misc'] = df.loc[df['category'] == 'misc', 'charge'].astype('float64').sum()

    # show output
    print('\n\n')
    print('Final result: ', end='\n\n')
    for col in final_df.columns:
        charge = round(final_df[col][0])
        print(f'{col} : ${charge}.00')
    print('\n\n')

    # show the user what has been spent so far this month
    tmp = final_df.drop('grocery', axis=1)
    print(f'Current spend for {month_of_interest}: ', f'${round(tmp.sum(axis=1)[0])}.00')

    return (df, final_df)