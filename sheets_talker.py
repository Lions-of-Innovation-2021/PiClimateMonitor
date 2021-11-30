# Talks to google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

#api: https://docs.gspread.org/en/latest/api.html#gspread.worksheet.Worksheet
sheet_name = 'STEM Challenege Spreadsheet'
worksheet = client.open(sheet_name).sheet1

# read a cell
cell = worksheet.cell(0, 0) #row, col
print(cell.value)

worksheet.get('A1') # works with multiple cells

# update a cell
worksheet.update_cell(0, 0, 'Text') #row, col
worksheet.update_acell('A1', 'Text') #works with one cell

worksheet.update('A1', 'Hello') # works with multiple cells
