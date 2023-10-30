import requests
import json
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker


# API point is from " https://apikijangportal.bnm.gov.my "

# Define the endpoint URL (Uniform Resource Identifier)
endpoint_url = "https://api.bnm.gov.my/public/msb/1.10"  

# Create a list to store the data for each month
data_list = []

# Define the header parameters
headers = {
    "Accept": "application/vnd.BNM.API.v1+json"
}

# Make the GET request
response = requests.get(endpoint_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = json.loads(response.text)
    
    # Print or manipulate the data as needed
    print(data)
else:
    print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")

# Extracted Json data 
pprint(data_list)
json_data=data_list

# Extract the 'data' dictionary
data_dict = data['data']

# Create a DataFrame from the data dictionary
df = pd.DataFrame(data_dict, index=[0])

# Get the year and month from the original data dictionary
year = df['year_dt'].values[0]
month = df['month_dt'].values[0]

# Map the month number to its name
month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

# Generate the title with year and month
title = f'Loan Applied in {month_names[month]} {year} by Purpose'

# Drop the unnecessary columns
df.drop(columns=['year_dt','month_dt','pur','pur_pas_car','tot_loa_app'], inplace=True)

# Rename the column headers
df.rename(columns={
    'pur_sec': 'Purchase of Securities',
    'pur_tra_veh':'Purchase of Transport Vehicles',
    'pur_res_pro':'Purchase of Residential Property',
    'pur_non_res_pro':'Purchase of Non-residential Property',
    'pur_fix_ass_oth_lan_and_bui':'Purchase of Fixed Assets other than Land and Building',
    'per_use': 'Personal uses',
    'cre_car':'Credit Card',
    'pur_con_goo':'Purchase of Consumer Durable Goods',
    'con': 'Construction',
    'wor_cap': 'Working Capital',
    'oth_pur':'Other Purposes'
    }, inplace=True)

# Print the DataFrame to verify the structure
print(df)

# Convert specific columns to numeric (replace 'column_name' with the actual column names)
df['Purchase of Securities'] = pd.to_numeric(df['Purchase of Securities'], errors='coerce')
df['Purchase of Transport Vehicles'] = pd.to_numeric(df['Purchase of Transport Vehicles'], errors='coerce')
df['Purchase of Residential Property'] = pd.to_numeric(df['Purchase of Residential Property'], errors='coerce')
df['Purchase of Non-residential Property'] = pd.to_numeric(df['Purchase of Non-residential Property'], errors='coerce')
df['Purchase of Fixed Assets other than Land and Building'] = pd.to_numeric(df['Purchase of Fixed Assets other than Land and Building'], errors='coerce')
df['Personal uses'] = pd.to_numeric(df['Personal uses'], errors='coerce')
df['Credit Card'] = pd.to_numeric(df['Credit Card'], errors='coerce')
df['Purchase of Consumer Durable Goods'] = pd.to_numeric(df['Purchase of Consumer Durable Goods'], errors='coerce')
df['Construction'] = pd.to_numeric(df['Construction'], errors='coerce')
df['Working Capital'] = pd.to_numeric(df['Working Capital'], errors='coerce')
df['Other Purposes'] = pd.to_numeric(df['Other Purposes'], errors='coerce')

# Select only the numeric columns to perform the division
numeric_columns = df.select_dtypes(include=[float, int])

# Divide the numeric columns by 1000
df[numeric_columns.columns] = numeric_columns / 1000

# Reset the index to remove the default numeric index
df.reset_index(drop=True, inplace=True)

# Now, you can create a bar chart
df.plot(kind='bar', legend=True,edgecolor='black', linewidth=1.2, figsize=(12, 6))
plt.title(title)
plt.xlabel('Purpose')
plt.ylabel('Total (RM billion)')

# Format the y-axis labels to display 2 decimal places
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.2f}'.format(x)))

plt.savefig('Loan Applied by Purposes.jpg')
plt.show()
