# ING to QIF convertor for KMyMoney
 Script that converts ING bank csv to QIF format ready for consumption by KMyMoney, including a simple recurring transaction classification function

The Dutch ING bank allows for downloading transactions in a csv file. I use this script to convert the csv file to a QIF file to manually import the transactions into KMyMoney, the awesome open source Personal Finance software. Try it out! Recurring transactions are recognised and automatically assigned a category based on a string which can be anywhere in the transaction. The list of strings and the accompanying Payee and Category for KMyMoney are listed in an xlsx file for easy editing.