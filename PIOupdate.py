#!/usr/bin/python

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import time
try:
	from win10toast import ToastNotifier
except:
	win10toast = None
	try:
		import notify2
	except:
		print('No library for notifications, exiting...')
		sys.exit()

if not win10toast == None:
	toaster = ToastNotifier()
else:
	notify2.init('PIO')

scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
spreadsheet = '186G43CyKVm1R2fwDGTIjQOzQYqWTy-wSgmTfGZ_Kmek'
term_columns = ['F', 'G', 'H']
termin = 1

def get_single_cell(sheets_api_handle, spreadsheet, range_id):
	result = sheets_api_handle.values().get(spreadsheetId=spreadsheet, range=range_id).execute()
	values = result.get('values', [])
	if values:
		for row in values:
			return row[0]
	else:
		return None

def notify(title, content):
	if not win10toast == None:
		toaster.show_toast('PIO', get_single_cell(sheet, spreadsheet, 'Poziomy!' + str(term_columns[termin-1]) + '2') + ': ' + str(grade))
	else:
		notification = notify2.Notification('PIO', get_single_cell(sheet, spreadsheet, 'Poziomy!' + str(term_columns[termin-1]) + '2') + ': ' + str(grade))
		notification.show()

def google_authorize_spreadsheet():
	creds = None

	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
			
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scope)
			
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
			
	service = build('sheets', 'v4', credentials=creds)
	return service.spreadsheets()

if len(sys.argv) == 3:
	termin = int(sys.argv[1])
	no_on_list = int(sys.argv[2])
else:
	print('usage: ' + sys.argv[0] + ' <term no> <number on list>')
	sys.exit()

range_id = 'Poziomy!' + str(term_columns[termin-1]) + str(no_on_list + 2)
print('Authorizing...')
sheet = google_authorize_spreadsheet()
print(
	'Done, listening for grade addition of "' + get_single_cell(sheet, spreadsheet, 'Poziomy!' + str(term_columns[termin-1]) + '2') 
	+ '" for "' + get_single_cell(sheet, spreadsheet, 'Poziomy!A' + str(no_on_list + 2)) + '".'
)

while True:
	grade = get_single_cell(sheet, spreadsheet, range_id)

	if grade:
		notify('PIO', get_single_cell(sheet, spreadsheet, 'Poziomy!' + str(term_columns[termin-1]) + '2') + ': ' + str(grade))
		print(get_single_cell(sheet, spreadsheet, 'Poziomy!' + str(term_columns[termin-1]) + '2') + ': ' + str(grade))
		print('Grade added, exiting...')
		break
		
	time.sleep(30)
