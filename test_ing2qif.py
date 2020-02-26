import ing2qif


def test_csv_filename_renamer_with_Path():
    testpath = ing2qif.Path('testfolder/testname_01-03-2020_15-04-2020.csv')
    output = ing2qif.csv_filename_renamer(testpath)
    assert output == '2020-03-01_2020-04-15_testname.csv'


def test_csv_filename_renamer_with_string():
    testfilename = 'testname_01-03-2020_15-04-2020.csv'
    output = ing2qif.csv_filename_renamer(testfilename)
    assert output == '2020-03-01_2020-04-15_testname.csv'
