# ING to QIF converter for KMyMoney
 Script that converts ING bank csv to QIF format ready for consumption by KMyMoney, including a simple recurring transaction classification function

The Dutch ING bank allows for downloading transactions in a csv file. I use this script to convert the csv file to a QIF file to manually import the transactions into KMyMoney, the awesome open source Personal Finance software. Try it out! 

Recurring transactions are recognised and automatically assigned a category based on a string which can be anywhere in the transaction. The list of strings and the accompanying Payee and Category for KMyMoney are listed in an xlsx file for easy editing.

Processed csv's are moved from the Downloads folder to a (configurable) archive folder. CSV and QIF files are renamed for better sorting.


Usage:
- Edit the ing2qif.py file to fill in the ING IBAN number and the KMyMoney account name.
- Edit the bankstatementmapping.xlsx file to automatically categorise transactions or set variable to False to skip the mapping.
- Optionally edit the locations where the csv files will be archived and the qif files created.
- Run the ing2qif.py file.
- Import the resulting qif file in KMyMoney.