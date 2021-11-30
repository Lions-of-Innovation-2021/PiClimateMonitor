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

def get_values(range):
    return worksheet.get(range)

def set_values(range, values):
    worksheet.update(range, values)
