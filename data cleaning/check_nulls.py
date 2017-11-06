
import pandas as pd
input_file=input("Enter the input csv file name :")
input_data=pd.DataFrame.from_csv(input_file)
null_columns = input_data.isnull().sum(axis=0).sort_values(ascending=False)/float(len(input_data))
print(null_columns)
