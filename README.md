# finance_statement_parser

The purpose of this project is to automate the process of categorizing credit card charges.  Banks do tend to offer this kind of service themselves, but I find I don't like the lack of control over the data presentation and categorization.  Details of each script are shown below.

- `extract_neo_charges.py`
    - log into profile on https://member.neofinancial.com/login and extract charges there
    - clean the extracted charges and save as csv, 
    - return the csv for the month asked for
- `charge_categorizer.py`
    - asks the user what month they're looking to analyze
    - calls `extract_neo_charges.py` and asks for the month of interest
    - takes the cleaned charges and categorizes them based on keywords found in the charge
    - returns the summarized, categorized charges
