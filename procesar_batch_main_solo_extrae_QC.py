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

worksheet = 0
	
with open(output_file, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['Path', 'Filename','QC1','QC2','QC3'])
	for root, dirs, files in os.walk(path):
		for file in files:
			if os.path.splitext(file)[1] == '.txt':
				filepath = os.path.join(root, file)
				filename = os.path.splitext(file)[0]
				# Las mediciones que incluyen estas secuencias de caracteres no se consideran en el análisis:
				if all(keyword not in filename for keyword in ['PD', 'CC', 'TEST', 'FREC']):
					print('FILEPATH',filepath)
					try:
						outproces = procesar2(filepath,filename)
						writer.writerow([filepath, filename, outproces[0], outproces[1], outproces[2]])
						print ("QC1",outproces[0],", QC2:",outproces[1],", QC3:",outproces[2])
						
					except Exception as e:
						print("Error:", str(e))
					
