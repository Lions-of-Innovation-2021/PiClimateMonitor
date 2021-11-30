import sheets_talker
#Analyze Data
#Variable values will be replaced by the values from the sensors
temperature = 0 #Fahrenheit
humidity = 0 / 100 #We want humidity as a decimal
smoke = 0 #Remember that smoke is measured in output on a 3.3V scale
risk = temperature - (temperature * humidity)

box_id = 0
box_sheet_range = ''

def init_box():
  box_id = sheets_talker.worksheet.row_count+1
  print(box_id)
  box_sheet_range = 'A' + str(box_id) + ':B' + str(box_id)
  print(box_sheet_range)
  sheets_talker.worksheet.add_rows(1) #add a new row for the box

init_box()
sheets_talker.worksheet.update(box_sheet_range, [[str(box_id), str(risk)]])
