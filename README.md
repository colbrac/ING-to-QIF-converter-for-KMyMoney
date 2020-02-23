# ING to QIF converter for KMyMoney
 Script that converts ING bank csv to qif format ready for consumption by KMyMoney, including a simple recurring transaction classification function

The Dutch ING bank allows for downloading transactions in a csv file. I use this script to convert the csv file to a qif file to manually import the transactions into KMyMoney, the awesome open source Personal Finance software. Try it out! 

## Automatic labelling of transactions
Recurring transactions are recognised and automatically assigned a category based on a string which can be anywhere in the transaction. The list of strings and the accompanying Payee and Category for KMyMoney are listed in an .xlsx file for easy editing.

## File handling
Processed csv's are moved from the Downloads folder to a (configurable) archive folder. csv and qif files are renamed for better sorting.

## Run standalone
The easiest way to use this script is to edit ing2qif.py itself and run it standalone:
- Edit the ing2qif.py file to fill in the ING IBAN number and the KMyMoney account name.
- Optionally change the folder in which the script looks for csv files.
- Optionally edit the locations where the csv files will be archived and the qif files created.
- Edit the bankstatementmapping.xlsx file to automatically categorise transactions or set variable to False to skip the mapping.
- Run the ing2qif.py file.
- Import the resulting qif file in KMyMoney.

## Run as library
When you have more than 1 ING account, you could create scripts per account that import ing2qif and change only the variables. Personally I created several sheets in the xlsx for the different accounts. The scripts 'proces-<myaccount>.py' then take the following form:

```
import ing2qif as iq

iq.ING_IBAN = 'NL@@INGB@@@@@@@@@@'
iq.MAP_SHEET = 'Different sheet name'
iq.KMYMONEYACCOUNT = 'Different account name'

iq.run()
```

## Run script from start menu in Windows 10 with (mini)conda environment
In my personal usecase the csv file is downloaded to the downloads folder, I run the script and import the resulting qif manually in KMyMoney. To run the script I open a Conda-enabled shell, navigate to the script folder and run the script. To simplify running the script I added a .bat file to the folder with the script with the following content:

```
@echo off
CALL C:\Users\<username>\Miniconda3\Scripts\activate.bat
python proces-<myaccount>.py
conda deactivate
```

Then I made a copy of the 'Anaconda Prompt' shortcut in the Windows Start Menu folder which points to this .bat file.

## License
This script is provided under the MIT License. Please see the license file for more details.
