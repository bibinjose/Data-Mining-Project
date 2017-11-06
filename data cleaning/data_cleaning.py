import pandas as pd
loan_data=input("Enter the input csv file name :")

loan_data.head()

print(loan_data)
print('The shape is {}'.format(loan_data.shape))
print('Memory : {} Mb'.format(int(loan_data.memory_usage(deep=False).sum() / 1000000)))
check_null = loan_data.isnull().sum(axis=0).sort_values(ascending=False)/float(len(loan_data))
# check_null[check_null>0.6]
loan_data.drop(check_null[check_null>0.6].index, axis=1, inplace=True)
loan_data.dropna(axis=0, thresh=30, inplace=True)
delete_me = ['policy_code', 'pymnt_plan', 'url', 'member_id', 'application_type', 'acc_now_delinq','emp_title', 'zip_code','title']
loan_data.drop(delete_me , axis=1, inplace=True)
print('The shape is {}'.format(loan_data.shape))
print('Memory : {} Mb'.format(int(loan_data.memory_usage(deep=False).sum() / 1000000)))
# print(loan_data)
# strip months from 'term' and make it an int
loan_data['term'] = loan_data['term'].str.split(' ').str[1]

# #interest rate is a string. Remove % and make it a float
# loan_data['int_rate'] = loan_data['int_rate'].str.split('%').str[0]
# loan_data['int_rate'] = loan_data.int_rate.astype(float)/100.

# extract numbers from emp_length and fill missing values with the median
loan_data['emp_length'] = loan_data['emp_length'].str.extract('(\d+)').astype(float)
loan_data['emp_length'] = loan_data['emp_length'].fillna(loan_data.emp_length.median())

col_dates = loan_data.dtypes[loan_data.dtypes == 'datetime64[ns]'].index
for d in col_dates:
    loan_data[d] = loan_data[d].dt.to_period('M')
print(loan_data['last_pymnt_d'].head())

loan_data['amount_diff_inv'] = 'same'
loan_data.loc[(loan_data['funded_amnt'] - loan_data['funded_amnt_inv']) > 0,'amount_diff_inv'] = 'low'

# Make categorical

loan_data['delinq_2yrs_cat'] = 'no'
loan_data.loc[loan_data['delinq_2yrs']> 0,'delinq_2yrs_cat'] = 'yes'

loan_data['inq_last_6mths_cat'] = 'no'
loan_data.loc[loan_data['inq_last_6mths']> 0,'inq_last_6mths_cat'] = 'yes'

loan_data['pub_rec_cat'] = 'no'
loan_data.loc[loan_data['pub_rec']> 0,'pub_rec_cat'] = 'yes'

# Create new metric
loan_data['acc_ratio'] = loan_data.open_acc / loan_data.total_acc
features = ['loan_amnt', 'amount_diff_inv', 'term',
            'installment', 'grade','emp_length',
            'home_ownership', 'annual_inc','verification_status',
            'purpose', 'dti', 'delinq_2yrs_cat', 'inq_last_6mths_cat',
            'open_acc', 'pub_rec', 'pub_rec_cat', 'acc_ratio', 'initial_list_status',
            'loan_status'
           ]

#X_clean = loan_data.loc[loan_data.loan_status != 'Current', features]
#Y_clean = loan_data.loc[loan_data.loan_status == 'Current', features]
#mask = (X_clean.loan_status == 'Charged Off')
#X_clean['target'] = 0
#X_clean.loc[mask,'target'] = 1
cat_features = ['term','amount_diff_inv', 'grade', 'home_ownership', 'verification_status', 'purpose', 'delinq_2yrs_cat', 'inq_last_6mths_cat', 'pub_rec_cat', 'initial_list_status']

# Drop any residual missing value (only 24)
#X_clean.dropna(axis=0, how = 'any', inplace = True)
mask = (loan_data.loan_status == 'Charged Off')
loan_data['target'] = 0
loan_data.loc[mask,'target'] = 1

loan_data.dropna(axis=0, how = 'any', inplace = True)

#X = pd.get_dummies(X_clean[X_clean.columns[:-2]], columns=cat_features).astype(float)

X_All = pd.get_dummies(loan_data[loan_data.columns[:-2]], columns=cat_features)
#y = X_clean['target']

#loan_data.to_csv("Loan_data_Original.csv")
#Y_clean.to_csv("Cleaned_8lakh_current.csv")
#X.to_csv("Cleaned_8lakh_OHE.csv")
X_All.to_csv("Cleaned_8lakh_All_Null_Removed.csv")
