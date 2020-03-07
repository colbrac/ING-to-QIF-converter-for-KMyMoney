import ing2qif


def test_csv_filename_renamer_with_Path():
    testpath = ing2qif.Path('testfolder/testname_01-03-2020_15-04-2020.csv')
    output = ing2qif.csv_filename_renamer(testpath)
    assert output == '2020-03-01_2020-04-15_testname.csv'


def test_csv_filename_renamer_with_string():
    testfilename = 'testname_01-03-2020_15-04-2020.csv'
    output = ing2qif.csv_filename_renamer(testfilename)
    assert output == '2020-03-01_2020-04-15_testname.csv'


def test_map_transactions():
    transactions = [
        ['23/01/2020', '-1,23', 'ABC', '', ''],
        ['24/01/2020', '2,34', 'def', '', ''],
        ['25/01/2020', '-3,45', 'abc', '', '']
    ]
    mapping = {
        'abc': ('a', 'b'),
        'def': ('d', 'e'),
        'ghi': ('g', 'h'),
    }
    expectedtransactions = [
        ['23/01/2020', '-1,23', 'ABC', 'a', 'b'],
        ['24/01/2020', '2,34', 'def', 'd', 'e'],
        ['25/01/2020', '-3,45', 'abc', 'a', 'b']
    ]
    mappedtransactions = ing2qif.map_transactions(transactions, mapping)
    assert mappedtransactions == expectedtransactions
