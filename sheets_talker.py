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
sheet_name = 'STEM Challenge Spreadsheet'
worksheet = client.open(sheet_name).sheet1

# read a cell
value = worksheet.get('A1') # works with multiple cells
print(value)

# update a cell
worksheet.update('A1', 'Hello') # works with multiple cells
