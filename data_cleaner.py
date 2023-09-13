import pandas as pd

def clean_data(dataframe):
    df = dataframe

    df['Manufacturer'] = df['Equipment'].str.extract(r'^(.*?) -')
    df['Product'] = df['Equipment'].str.extract(r'-(.*?)(?= Asset No)')
    df['Asset No'] = df['Equipment'].str.extract(r'Asset No: (\d+)')
    df['Serial No'] = df['Equipment'].str.extract(r'Serial No: ([\w\d\s\-_!@#$%^&*()+=?<>{}|~.,]+)')
    df['Tags'] = df['Unnamed: 1']
    df['Age (Years)'] = pd.to_numeric(df['Age (Years)'])
    df['All Calls'] = pd.to_numeric(df['All Calls'])
    df['Open Calls'] = pd.to_numeric(df['Open Calls'])
    df['Lifetime Spend'] = df['Lifetime Spend'].str.replace('£', '')
    df['Nominal Replacement Cost'] = df['Nominal Replacement Cost'].str.replace('£','')
    df.drop(columns=['Equipment', 'Unnamed: 1', 'On Site?', 'Condition', 'Under Warranty?'], inplace=True)

    df = df[['Manufacturer', 'Product', 'Asset No', 'Serial No', 'Tags', 'Age (Years)', 'All Calls', 'Open Calls', 'Lifetime Spend', 'Nominal Replacement Cost']]

    cleaned_df = df
    return cleaned_df
