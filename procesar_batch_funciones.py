import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema
from scipy.signal import savgol_filter
import json

# Extrae datos del archivo json creado por el programa de medición
def procesar(pathtofile,filename,enableplot,fig0,fig1,fig2):
	
	datos = json.load(open(pathtofile))
	qc1 = datos["QC"]["promedioQC1"]
	qc2 = datos["QC"]["promedioQC2"]
	qc3 = datos["QC"]["promedioQC3"]
	mem_df= pd.json_normalize(datos["resultados"]["datos"]).apply(pd.to_numeric)
	temp_ini = mem_df['temp.z'].values[0]*(-6.48e-6)+89.3
	
		
	x = mem_df['acu.t'].values/1000
	y = mem_df['dat.pre'].values*-.0046
	temp_all = mem_df['temp.z'].values*(-6.48e-6)+89.3
	
	idx_max = argrelextrema(y, np.greater,order=3)[0]
	idx_min = argrelextrema(y, np.less,order=3)[0]
	
	if idx_max[0] > idx_min[0]:
		primeromax = True
	else:
		primeromax = False
	
	ymax = [y[i] for i in idx_max]
	ymin = [y[i] for i in idx_min]
	
	if len(ymax)>len(ymin):
	  ymax = ymax[:len(ymin)]
	  #t = [x[i] for i in idx_min]
	
	if len(ymin)>len(ymax):
	  ymin = ymin[:len(ymax)]
	  #t = [x[i] for i in idx_max]
	#else:
	 # t = [x[i] for i in idx_max]
	
	if primeromax:
		t = [x[i] for i in idx_max]
		temp = [temp_all[i] for i in idx_max]
	else:
		t = [x[i] for i in idx_min]
		temp = [temp_all[i] for i in idx_min]
	
	ampli = [(xx - yy)/2 for xx, yy in zip(ymax, ymin)]
	ampli_smooth = savgol_filter(ampli, 31, 7)
	
	ct=-1
	A1=-1
	A5=-1
	A10=-1
	Abase=-1
	Pmed10=-1
	Pmed0=-1
	temp_A10=-1
	
	Pmed0 = round(ymin[5]+ ampli_smooth[5],2)
	
	for i, num in enumerate(ampli_smooth):
	    if num > 60 and ct == -1:
	        ct = round(t[i],2)
	        break
	if ct>-1:
		for i, num in enumerate(t):
		  if num > ct+600 and  A10 == -1:
		    A10 = round(ampli_smooth[i],2)
		    Pmed10 = round(ymin[i]+ A10,2)
		    temp_A10 = round(temp[i],2)
		  elif num > ct+300 and  A5 == -1:
		    A5 = round(ampli_smooth[i],2)
		  elif num > ct+60 and  A1 == -1:
		    A1 = round(ampli_smooth[i],2)
		  elif num > ct*.75 and Abase == -1:
		    Abase = round(ampli_smooth[i],2)
	
	
	if enableplot:
		
		fig0.add_traces(go.Scatter(x=x, y=y, name=filename))
		#fig0.add_traces(go.Scatter(x=t, y=ymax-ampli_smooth, name=filename+"_pmed"))
		
		#fig0.add_traces(go.Scatter(x=x[idx_max], y=y[idx_max], name=filename+"_top"))
		#fig0.add_traces(go.Scatter(x=x[idx_min], y=y[idx_min], name=filename+"_bottom"))
		
		
		#fig1.add_traces(go.Scatter(x=t, y=ampli, name=filename+"_amplitude"))
		fig1.add_traces(go.Scatter(x=t, y=ampli_smooth, name=filename+"_amplitude_smooth"))
		
		fig2.add_traces(go.Scatter(x=t, y=ampli_smooth+ymin, name=filename+"_pmed"))
	
	return [Abase,ct,A1,A5,A10, Pmed0, Pmed10, qc1, qc2, qc3, temp_ini, temp_A10]
	
	# procesar2 solo extrae datos del json pero no procesa la curva
def procesar2(pathtofile,filename):
	datos = json.load(open(pathtofile))
	qc1 = datos["QC"]["promedioQC1"]
	qc2 = datos["QC"]["promedioQC2"]
	try:
		qc3 = datos["QC"]["promedioQC3"]
	except Exception as e:
		print("No hay QC3:", str(e))
		qc3 = None
	
	mem_df= pd.json_normalize(datos["resultados"]["datos"]).apply(pd.to_numeric)
		
	temp_ini = mem_df['temp.z'].values[0]*(-6.48e-6)+89.3
	temp_fin = mem_df['temp.z'].values[-1]*(-6.48e-6)+89.3
	
	
	
	
	
	return [qc1, qc2, qc3, temp_ini, temp_fin]
