from pathlib import Path
import openpyxl

# Own bankaccount IBAN
ING_IBAN = 'NL@@INGB@@@@@@@@@@'

# Name of the bankaccount in KMyMoney
KMYMONEYACCOUNT = 'Betaalrekening'

# Search for new csv file in this location
FOLDER_CSVS = Path.joinpath(Path.home(), 'Downloads')

# Filename of the map file, set to False to covert csv to qif without mapping
MAP_FILE = Path('bankstatementmapping.xlsx')  # False
MAP_SHEET = 'Map'

# Folders to archive csv file and generated qif file
FOLDER_CSV_ARCHIVE = Path('csv/')
FOLDER_QIF_ARCHIVE = Path('qif/')


def find_csvfile(folder=FOLDER_CSVS):
    """
    Return a Path for a csv file which has the accountnumber in its filename.

    If there is more than one csv file for this account, the script should be
    rerun to process each file. As csv files are supposed to be moved to the
    archive folder after processing, a next run will return the next csv file
    with this ING accountnumber.

    Returns False is there is no file
    """
    if not isinstance(folder, Path):
        folder = Path(folder)
    files = [path for path in folder.iterdir() if ING_IBAN in path.name]
    return files[0] if len(files) > 0 else False


def load_csv(csv_filename):
    """
    Loads the csv file and, based on the ING coding, combines a number of
    the included fields into a description.

    Returns a list of list of strings with the date, amount and description
    """
    with open(csv_filename, 'r') as f:
        rawdata = f.readlines()
    data = [line[1:-2].split('","') for line in rawdata]
    if data[0][1] != 'Naam / Omschrijving':
        raise ValueError("File does not contain transaction data, " +
                         " check contents of {}".format(csv_filename))
    csvdata = []
    for datum, naam, rek, tegenrek, code, afbij, \
            bedrag, mutatiesoort, mededeling in data[1:]:
        date = f'{datum[6:8]}/{datum[4:6]}/{datum[:4]}'

        amount = bedrag.replace(',', '.')
        if afbij == "Af":
            amount = '-'+amount

        if code == 'BA':
            desc = f'Pin: {naam} - {mededeling}'
        elif code == 'DV':
            desc = f'ING: {naam} - {mededeling}'
        elif code == 'GM':
            desc = f'Geldopname: {naam} - {mededeling}'
        elif code == 'GT':
            if tegenrek == '':
                desc = f'Sparen: {naam} - {mededeling}'
            else:
                desc = f'Overboeking: {mededeling}'
        elif code == 'IC':
            desc = f'Incasso: {mededeling}'
        elif code == 'OV':
            desc = f'Overboeking: {mededeling}'
        else:  # overige codes, nog eens uitzoeken welke er zijn
            desc = f'{naam} ({tegenrek}) - {mededeling}'

        csvdata.append([date, amount, desc])
    return csvdata


def csv_filename_renamer(csv_file):
    """
    Converts the ING naming convention into naming convention
    with date YYYYMMDD to YYYYMMDD first.
    """
    account, fromdate, todate = csv_file.name[:-4].split('_')

    day, month, year = fromdate.split('-')
    fromdate = f'{year}-{month}-{day}'

    day, month, year = todate.split('-')
    todate = f'{year}-{month}-{day}'

    return f'{fromdate}_{todate}_{account}.csv'


def load_mapdict(filename_mapfile=MAP_FILE):
    """
    Load the Excel file and convert to a dict with the detection string as key
    and the standard Payee and Category for that as a tuple value.

    Expects the Excel file to have rows which have the detection string in
    column B and the accompanying Payee and Category in columns C and D
    """
    mapfile = openpyxl.open(filename_mapfile, 'r')
    print(f'Loading mapping from sheet {MAP_SHEET} of {filename_mapfile}')
    sheet = mapfile[MAP_SHEET]
    mapping = {str(value[1]): (str(value[2]), str(value[3]))  # Cols B, C and D
               for value in sheet.values if value[1] is not None}
    mapfile.close()
    return mapping


def map_transactions(transactions, mapping):
    """
    Compare all transactions to a dictionary with payees and categories
    """
    mappedtransactions = []
    mapcounter = 0
    for date, amount, desc in transactions:
        for identifier in mapping.keys():
            if identifier in desc:
                payee, category = mapping[identifier]
                mapcounter += 1
                break
            else:
                payee, category = '', ''
        mappedtransactions.append([date, amount, desc, payee, category])

    print(f'Mapped {mapcounter} out of {len(transactions)} ' +
          f'transactions ({100.*mapcounter/len(transactions):.0f}%)')
    return mappedtransactions


def write_transactions_to_qif(transactions, qiffile, verbose=False):
    """
    Take a list of transaction dictionaries and write to QIF file

    transactions: list of transactions
    qiffile: filename to write contents to
    """
    with open(qiffile, 'w') as f:
        # Write opening statement for KMyMoney
        f.write('!Account\n')
        f.write(f'N{KMYMONEYACCOUNT}\n')
        f.write('TBank\n')
        f.write('^\n')
        f.write('!Type:Bank\n')
        f.write('^\n')

        # Loop over transactions and write to file
        if len(transactions[0]) == 5:
            for date, amount, desc, payee, category in transactions:
                f.write(f'D{date}\n')
                f.write(f'T{amount}\n')
                if payee != '':
                    f.write(f'P{payee}\n')
                if category != '':
                    f.write(f'L{category}\n')
                f.write(f'M{desc}\n')
                f.write('^\n')
        else:
            for date, amount, desc in transactions:
                f.write(f'D{date}\n')
                f.write(f'T{amount}\n')
                f.write(f'M{desc}\n')
                f.write('^\n')


if __name__ == "__main__":
    csv_file = find_csvfile()
    if csv_file:
        print(f'Found new csv file {csv_file}...')
        transactions = load_csv(csv_file)
        csv_newname = csv_filename_renamer(csv_file)
        qif_file = Path.joinpath(FOLDER_QIF_ARCHIVE,
                                 csv_newname.replace('.csv', '.qif'))
        if MAP_FILE:
            mapping = load_mapdict()
            transactions = map_transactions(transactions, mapping)

        FOLDER_QIF_ARCHIVE.mkdir(parents=True, exist_ok=True)
        write_transactions_to_qif(transactions, qif_file)

        FOLDER_CSV_ARCHIVE.mkdir(parents=True, exist_ok=True)
        csv_file.rename(Path.joinpath(FOLDER_CSV_ARCHIVE, csv_newname))

        print(f'Succes! Result saved to {qif_file}.')

    else:
        print('No csv file found!')
