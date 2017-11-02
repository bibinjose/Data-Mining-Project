"""

To trim the data to one lakh records
"""
import random
import os
cwd = os.getcwd()
output_file="loan_data.csv"
#Open the csv file
with open("C:/usf/dm project/loandata/loan.csv", "rb") as loan_data:
    records = [record for record in loan_data]
#To get the attribute list
attributes=records[0]
#Get 1 lakh random records
random_choice = random.sample(records[1:], 100000)
with open(output_file, "w") as sink:
     #Write the attribute to output file
     sink.write("".join(attributes.decode('ascii')))
sink.close()
with open(output_file, "ab") as sink:
    #Write 1 lakh random records
    sink.write(b"".join((random_choice)))
sink.close()

print("Slicing finished \nGet "+output_file+" from "+cwd)