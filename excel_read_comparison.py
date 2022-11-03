import os
import time
import pandas as pd
import openpyxl
from excel_utils import ExcelRead, ExcelWrite, ExcelReadT, ExcelWriteT

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
excel_file_name = PROJECT_PATH + '/' + 'file_example_XLSX_5000.xlsx'
excel_output_file_name = PROJECT_PATH + '/' + 'file_example_XLSX_5000_output.xlsx'


start_time = time.time()

excelreadrow = ExcelRead() # read by rows
data = excelreadrow.openpyxl_read_excel(excel_file_name)

excelrowwrite = ExcelWrite();
if os.path.isfile(excel_output_file_name) != True:
    excelrowwrite.openpyxl_write_new_excel_file(excel_output_file_name)
excelrowwrite.openpyxl_write_existing_excel_file(excel_output_file_name, data)

end_time = time.time()
print('Reading and writing a excel by row with openpyxl library:\t' + (str)(end_time - start_time) + 's.')



start_time = time.time()

excelreadcol = ExcelReadT() # read by columns
data = excelreadcol.openpyxl_read_excel(excel_file_name)

excelcolwrite = ExcelWriteT();
if os.path.isfile(excel_output_file_name) != True:
    excelcolwrite.openpyxl_write_new_excel_file(excel_output_file_name)
excelcolwrite.openpyxl_write_existing_excel_file(excel_output_file_name, data)

end_time = time.time()
print('Reading and writing a excel by column with openpyxl library:\t' + (str)(end_time - start_time) + 's.')



start_time = time.time()

data = pd.read_excel(excel_file_name, index_col=0, engine="openpyxl")
df = pd.DataFrame(data)
df.to_excel(excel_output_file_name)

end_time = time.time()
print('Reading and writing a excel with pandas (openpyxl engine):\t' + (str)(end_time - start_time) + 's.')
