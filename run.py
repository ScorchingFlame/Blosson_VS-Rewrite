# from time import sleep
# # from typing import Literal
# from numpy import number
import xlrd, atexit
import os
from tempfile import NamedTemporaryFile

class FileHandler():

    def __init__(self):
        self.file = NamedTemporaryFile(suffix='.xlsx', delete=False)
        # register function called when quit
        atexit.register(self._cleanup)

    def write_into(self, btext):
        self.file.write(btext)
        self.file.seek(0)
    def _cleanup(self):
        # because self.file has been created without delete=False, closing the file causes its deletion 
        self.file.close()
        os.unlink(self.file.name)

fh = FileHandler()
fh.write_into(open('./sheet.xlsx', "rb").read())

print(fh.file.name)
# sleep(60)
loc = (fh.file.name)

a : xlrd.Book = xlrd.open_workbook(loc)

sheet = a.sheet_by_index(0)

sheet.cell_value(0,0)

if not sheet.row_values(0) == ["AdmissionNumber", "Name", "STD", "House"]:
    exit()

# k = [int, str, int, Literal["WINTER", "SUMMER", "SPRING"]]
# sleep(60)
tp = []
for i in range(1, sheet.nrows-1):
    meh = [x if type(x) == str else int(x) for x in sheet.row_values(i)]
    meh.append(0)
    tp.append(tuple(meh))

print(tp)