# install OpenPyxl
import openpyxl
from openpyxl import Workbook, load_workbook

# load workbook
book =  load_workbook('testworkbook.xlsx')
sheet = book['TestSheet']
print(sheet['A2'].value)

sheet['A2'].value = 'Linda'

book.save('testworkbook.xlsx')

