#! /home/pi/.local/lib/python3.7/site-packages
import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')

# Talks to google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from os import path

#Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
dir = path.dirname(path.abspath(__file__))
file_path = path.join(dir, file_name)

creds = ServiceAccountCredentials.from_json_keyfile_name(file_path,scope)
client = gspread.authorize(creds)

#api: https://docs.gspread.org/en/latest/api.html#gspread.worksheet.Worksheet
sheet_name = 'STEM Challenge Spreadsheet'
worksheet = client.open(sheet_name).sheet1

def get_values(range):
    return worksheet.get(range)

def set_values(range, values):
    worksheet.update(range, values)
