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
	worksheet = open_worksheet("config.yml")
	column_dict = {}
	column_dict["A_base"]=find_column_number_by_text(worksheet,"Amplitud_base")
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
	
with open(output_file, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['Path', 'Filename','A_base','ct','A1','A5','A10','Pmed_base','Pmed_A10'])
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
						writer.writerow([filepath, filename, outproces[0], outproces[1], outproces[2], outproces[3], outproces[4], outproces[5], outproces[6]])
						print ("A_base",outproces[0],", CT:",outproces[1],", A10:",outproces[4],", Pmed_base:",outproces[5],", Pmed_A10:",outproces[6],", QC1:",outproces[7],", QC2:",outproces[8],", QC3:",outproces[9])
						
					except Exception as e:
						print("Error:", str(e))
					
					if escribePlanilla:
						try:
							target_row = find_row_by_identifier_in_column_b(worksheet,filename)
							modify_row_with_retry (worksheet,target_row,column_dict["A_base"],outproces[0])
							modify_row_with_retry (worksheet,target_row,column_dict["CT"],outproces[1])
							modify_row_with_retry (worksheet,target_row,column_dict["A1"],outproces[2])
							modify_row_with_retry (worksheet,target_row,column_dict["A5"],outproces[3])
							modify_row_with_retry (worksheet,target_row,column_dict["A10"],outproces[4])
							modify_row_with_retry (worksheet,target_row,column_dict["Pmed_base"],outproces[5])
							modify_row_with_retry (worksheet,target_row,column_dict["Pmed_A10"],outproces[6])
							modify_row_with_retry (worksheet,target_row,column_dict["QC1"],outproces[7])
							modify_row_with_retry (worksheet,target_row,column_dict["QC2"],outproces[8])
							modify_row_with_retry (worksheet,target_row,column_dict["QC3"],outproces[9])
							modify_row_with_retry (worksheet,target_row,column_dict["Procesamiento"],"max-min")
							
						except Exception as e:
							print("Error:", str(e))
							
    
if enablePlot:
	fig0.show()
	fig1.show()
	fig2.show()
