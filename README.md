# finance_statement_parser

The purpose of this project is to automate the process of categorizing credit card charges.  Banks do tend to offer this kind of service themselves, but I find I don't like the lack of control over the data presentation and categorization.  Details of each script are shown below.

- `extract_neo_charges.py`
    - log into profile on https://member.neofinancial.com/login and extract charges there
    - clean the extracted charges and save as csv, 
    - return the csv for the month asked for
- `charge_categorizer.py`
    - call `extract_neo_charges.py` and ask for the month of interest
    - take the cleaned charges and categorize them based on keywords found in the charge
    - return the categorized charges
- `get_categorized_charges.py`
    - take month of interest as input from user, check if we've already done this month
    - if already done, load the saved results and display to user
    - else, call `charge_categorizer.py` and save the results to csv
- `category_visualizer.py`
    - call `charge_categorizer.py`
    - take the categorized charges and generate a dynamic bar chart to show how spend varied across categories over the course of the month
