import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yaml
import time

with open("config.yml", "r") as file:
    configu = yaml.safe_load(file)

def open_worksheet(config_file):
	with open(config_file, "r") as file:
		configu = yaml.safe_load(file)

	# Replace 'path_to_credentials.json' with the actual path to your credentials JSON file.
	credentials = ServiceAccountCredentials.from_json_keyfile_name(configu['credential_file'], ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])

	# Authenticate with the Google Sheets API
	gc = gspread.authorize(credentials)

	# Replace 'your_spreadsheet_id' with the ID of your Google Sheet (from the URL).
	spreadsheet = gc.open_by_key(configu['spreadsheet'])

	# Replace 'Sheet1' with the name of your desired worksheet.
	worksheet = spreadsheet.worksheet(configu['worksheet'])
	return worksheet

def find_column_number_by_text(worksheet, text_to_find):
    # Assuming row 4 contains the column headers where you want to search for 'nombre'.
    # Fetch row 4 as a list of values.
    headers_row = worksheet.row_values(4)

    # Find the index of the cell with the specified text.
    try:
        column_number = headers_row.index(text_to_find) + 1
        return column_number
    except ValueError:
        return None

def find_row(key_value):
    # Assuming the key identifier is in column A
    cell = worksheet.find(key_value)
    return cell.row

def find_row_by_identifier_in_column_b(worksheet,key_value):
    try:
        # Assuming the key identifier is in column B
        cell = worksheet.find(key_value, in_column=2)
        return cell.row
    except gspread.exceptions.CellNotFound:
        return None

def modify_row(worksheet, row, col_a, col_a_value):	
    worksheet.update_cell(row, col_a, col_a_value)
    
def modify_row_with_retry(worksheet, target_row, column, value):
    while True:
        try:
            modify_row(worksheet, target_row, column, value)
            break  # If modification is successful, exit the loop
        except Exception as e:
            if "RATE_LIMIT_EXCEEDED" in str(e).upper():
                print("Error:", str(e))
                print("Waiting for 10 seconds before retrying...")
                time.sleep(10)
            else:
                print("Unhandled Error:", str(e))
                break  # Exit the loop if it's an unhandled error
    
