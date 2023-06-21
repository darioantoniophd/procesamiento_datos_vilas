import os
import csv
import plotly.express as px
import plotly.graph_objects as go
from procesar_batch_funciones import *

output_file="/home/dario/Dropbox/MZP/desarrollo/software_medicion/procesamiento_amplitud_vilas02/mediciones_procesadas.csv"
path="/home/dario/Documents/mediciones_vilas02/data_a_procesar"
enablePlot=False

if enablePlot:
	fig0= go.Figure()
	fig0.update_layout(xaxis_title = r'$\text{Time } T \text{ in s}  $', yaxis_title = r'$\text{Pressure } \text{ in Pa}$')
	fig0.update_layout(title= r'$\text{Viscoelastic trace}$')
	fig1= go.Figure()
	fig1.update_layout(xaxis_title = r'$\text{Time } T \text{ in s}  $', yaxis_title = r'$\text{Pressure } \text{ in Pa}$')
	fig1.update_layout(title= r'$\text{Viscoelastic trace}$')
	fig2= go.Figure()
	fig2.update_layout(xaxis_title = r'$\text{Time } T \text{ in s}  $', yaxis_title = r'$\text{Pressure } \text{ in Pa}$')
	fig2.update_layout(title= r'$\text{Viscoelastic trace}$')


with open(output_file, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['Path', 'Filename','pbase','ct','A1','A5','A10','deltaPmed'])
	for root, dirs, files in os.walk(path):
		for file in files:
			if os.path.splitext(file)[1] == '.dat':
				filepath = os.path.join(root, file)
				filename = os.path.splitext(file)[0]
				# Las mediciones que incluyen estas secuencias de caracteres no se consideran en el análisis:
				if all(keyword not in filename for keyword in ['PD', 'CC', 'TEST', 'FREC']):
					print('FILEPATH',filepath)
					try:
						outproces = procesar(filepath,filename,enablePlot,fig0,fig1,fig2)
						writer.writerow([filepath, filename, outproces[0], outproces[1], outproces[2], outproces[3], outproces[4], outproces[5]])
						print ("P_base",outproces[0],", CT:",outproces[1],", A10:",outproces[4],", deltaPmed:",outproces[5])
						
					except Exception:
						print ('The file: '+filepath+' had an error.')
    
if enablePlot:
	fig0.show()
	fig1.show()
	fig2.show()
