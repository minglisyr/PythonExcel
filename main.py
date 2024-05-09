# install OpenPyxl
import openpyxl
from openpyxl import Workbook, load_workbook

# load workbook
book =  load_workbook('testworkbook.xlsx')
sheet = book['TestSheet']
print(sheet['A2'].value)

sheet['A2'].value = 'Eve'

book.save('testworkbook.xlsx')