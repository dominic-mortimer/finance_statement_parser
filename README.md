# finance_statement_parser

The purpose of this project is to automate the process of categorizing credit card charges.  Banks do tend to offer this kind of service themselves, but I find I don't like the lack of control over the data presentation and categorization.  Details of each script are shown below.

- `extract_neo_charges.py`
    - log into profile on https://member.neofinancial.com/login and extract charges there
    - clean the extracted charges and save as csv, 
    - return the csv for the month asked for
- `charge_categorizer.py`
    - ask the user what month they're looking to analyze
    - call `extract_neo_charges.py` and ask for the month of interest
    - take the cleaned charges and categorize them based on keywords found in the charge
    - return the categorized charges
- `charge_summarizer.py`
    - call `charge_categorizer.py`
    - summarize the charges by category
    - save the summarized charges as csv
- `category_visualizer.py`
    - call `charge_categorizer.py`
    - take the categorized charges and generate a dynamic bar chart to show how spend varied across categories over the course of the month
