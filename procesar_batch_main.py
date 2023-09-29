import os
import sys
print(sys.prefix)

import csv
import plotly.express as px
import plotly.graph_objects as go
from procesar_batch_funciones import *
from gsheets import *
import yaml


with open("config.yml", "r") as file:
    configu = yaml.safe_load(file)

output_file=configu['output_file']
path=configu['path']
enablePlot=configu['enablePlot']
escribePlanilla=configu['escribePlanilla']

fig0= go.Figure()
fig1= go.Figure()
fig2= go.Figure()

worksheet = 0

if enablePlot:
	
	fig0.update_layout(xaxis_title = r'$\text{Time } T \text{ in s}  $', yaxis_title = r'$\text{Pressure } \text{ in Pa}$')
	fig0.update_layout(title= r'$\text{Trazado viscoelástico - Curva cruda}$')
	fig1.update_layout(xaxis_title = r'$\text{Time } T \text{ in s}  $', yaxis_title = r'$\text{Pressure } \text{ in Pa}$')
	fig1.update_layout(title= r'$\text{Trazado viscoelástico - Amplitud}$')
	fig2.update_layout(xaxis_title = r'$\text{Time } T \text{ in s}  $', yaxis_title = r'$\text{Pressure } \text{ in Pa}$')
	fig2.update_layout(title= r'$\text{Presión media}$')

if escribePlanilla:
	gsheetapi = open_worksheet("config.yml")
	spreadsheetId = gsheetapi[0]
	worksheet = gsheetapi[1]
	service = gsheetapi[2]
	update_requests = []
	column_dict = {}
	column_dict["A_base"]=find_column_number_by_text(worksheet, "Amplitud_base")
	column_dict["CT"]=find_column_number_by_text(worksheet,"CT [seg]")
	column_dict["A1"]=find_column_number_by_text(worksheet,"A1 (60s+CT) [Pa]")
	column_dict["A5"]=find_column_number_by_text(worksheet,"A5 (300s+CT) [Pa]")
	column_dict["A10"]=find_column_number_by_text(worksheet,"A10 (600s+CT) [Pa]")
	column_dict["Pmed_base"]=find_column_number_by_text(worksheet,"Pmed_base")
	column_dict["Pmed_A10"]=find_column_number_by_text(worksheet,"Pmed_A10")
	column_dict["QC1"]=find_column_number_by_text(worksheet,"Canal cerrado Promedio QC1 [Pa]")
	column_dict["QC2"]=find_column_number_by_text(worksheet,"Canal abierto Promedio QC2 [Pa]")
	column_dict["QC3"]=find_column_number_by_text(worksheet,"Canal cerrado Promedio QC3 [Pa]")
	column_dict["Procesamiento"]=find_column_number_by_text(worksheet,"Procesamiento")
	column_dict["Tz_i"]=find_column_number_by_text(worksheet,"Tz_i")
	column_dict["Tz_A10"]=find_column_number_by_text(worksheet,"Tz_A10")
	
with open(output_file, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['Path', 'Filename','A_base','ct','A1','A5','A10','Pmed_base','Pmed_A10','QC1','QC2','QC3','Tz_i','Tz_A10'])
	for root, dirs, files in os.walk(path):
		for file in files:
			if os.path.splitext(file)[1] == '.txt':
				filepath = os.path.join(root, file)
				filename = os.path.splitext(file)[0]
				# Las mediciones que incluyen estas secuencias de caracteres no se consideran en el análisis:
				if all(keyword not in filename for keyword in ['PD', 'CC', 'TEST', 'FREC']):
					print('FILEPATH',filepath)
					try:
						outproces = procesar(filepath,filename,enablePlot,fig0,fig1,fig2)
						writer.writerow([filepath, filename, outproces[0], outproces[1], outproces[2], outproces[3], outproces[4], outproces[5], outproces[6], outproces[7], outproces[8], outproces[9], outproces[10], outproces[11]])
						print ("A_base",outproces[0],", CT:",outproces[1],", A10:",outproces[4],", Pmed_base:",outproces[5],", Pmed_A10:",outproces[6],", QC1:",outproces[7],", QC2:",outproces[8],", QC3:",outproces[9],", Tz_i:",outproces[10],", Tz_A10:",outproces[11])
						
					except Exception as e:
						print("Error 1:", str(e))
					
					if escribePlanilla:
						
						try:
							target_row = find_row_by_identifier_in_column_b(worksheet,filename)						
							# Add your update requests to the list
							request_append (update_requests,worksheet.id,target_row,column_dict["A_base"],outproces[0],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["CT"],outproces[1],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["A1"],outproces[2],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["A5"],outproces[3],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["A10"],outproces[4],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["Pmed_base"],outproces[5],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["Pmed_A10"],outproces[6],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["QC1"],outproces[7],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["QC2"],outproces[8],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["QC3"],outproces[9],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["Procesamiento"],"max-min","stringValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["Tz_i"],outproces[10],"numberValue")
							request_append (update_requests,worksheet.id,target_row,column_dict["Tz_A10"],outproces[11],"numberValue")
							
						except Exception as e:
							print("Error in request append:", str(e))
	# Execute the gsheet batch update
	if escribePlanilla:
		
	
		
		
		request_body = {
			'requests': update_requests
		}
		try:
			request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId,body=request_body)
			response = request.execute()
		
		
		
		except Exception as e:
			print("Error executing update in gsheets:", str(e))
		#print(update_requests)					
    
if enablePlot:
	fig0.show()
	fig1.show()
	fig2.show()
