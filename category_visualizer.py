

import pandas as pd
import numpy as np
import plotly.graph_objects as go

# run the script to clean the data
import extracting_credit_card_statements as eccs

all_charges, final_df = eccs.extracting_credit_card_statements()

###################################################################################################################
### set up and show the figure
###################################################################################################################

# instantiate
fig = go.Figure()

# create the df
tmp = all_charges.groupby('category').sum().reset_index()[['category', 'Amount']]
tmp['amount_txt'] = round(tmp['Amount'])
tmp['amount_txt'] = '$' + tmp['amount_txt'].astype('str') + '0'

# create the trace
trace1 = go.Bar(x=tmp['category'], y=tmp['Amount'], text=tmp['amount_txt'], textposition='outside')

# add the trace
fig.add_trace(trace1)

# visual edits and show
fig.update_layout(title='Visualization of Charges by Category')
fig.update_yaxes(title='Charges')
fig.show()