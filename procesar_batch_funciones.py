import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema
from scipy.signal import savgol_filter


def procesar(pathtofile,filename,enableplot,fig0,fig1,fig2):

	mem_df = pd.read_csv(pathtofile, delimiter=' ').apply(pd.to_numeric)
	
	x = mem_df['acu.t'].values/1000
	y = mem_df['dat.pre'].values*-.0046
	
	idx_max = argrelextrema(y, np.greater,order=3)[0]
	idx_min = argrelextrema(y, np.less,order=3)[0]
	
	ymax = [y[i] for i in idx_max]
	ymin = [y[i] for i in idx_min]
	
	if len(ymax)>len(ymin):
	  ymax = ymax[:len(ymin)]
	  t = [x[i] for i in idx_min]
	
	if len(ymin)>len(ymax):
	  ymin = ymin[:len(ymax)]
	  t = [x[i] for i in idx_max]
	else:
	  t = [x[i] for i in idx_max]
	
	ampli = [(xx - yy)/2 for xx, yy in zip(ymax, ymin)]
	ampli_smooth = savgol_filter(ampli, 51, 3)
	
	ct=-1
	A1=-1
	A5=-1
	A10=-1
	pbase=-1
	Pmed10=-1
	Pmed0=-1
	
	Pmed0 = ymin[5]+ ampli_smooth[5]
	
	for i, num in enumerate(ampli_smooth):
	    if num > 60 and ct == -1:
	        ct = round(t[i],2)
	        break
	if ct>-1:
		for i, num in enumerate(t):
		  if num > ct+600 and  A10 == -1:
		    A10 = round(ampli_smooth[i],2)
		    Pmed10 = ymin[i]+ A10
		  elif num > ct+300 and  A5 == -1:
		    A5 = round(ampli_smooth[i],2)
		  elif num > ct+60 and  A1 == -1:
		    A1 = round(ampli_smooth[i],2)
		  elif num > 100 and pbase == -1:
		    pbase = round(ampli_smooth[i],2)
	
	deltaPmed = round(Pmed10 - Pmed0,2)
	
	if enableplot:
		
		fig0.add_traces(go.Scatter(x=x, y=y, name=filename))
		#fig0.add_traces(go.Scatter(x=t, y=ampli_smooth+ymin, name=filename+"_pmed"))
		#fig0.add_traces(go.Scatter(x=x[idx_max], y=y[idx_max], name=filename+"_top"))
		#fig0.add_traces(go.Scatter(x=x[idx_min], y=y[idx_min], name=filename+"_bottom"))
		
		
		#fig1.add_traces(go.Scatter(x=t, y=ampli, name=filename+"_amplitude"))
		fig1.add_traces(go.Scatter(x=t, y=ampli_smooth, name=filename+"_amplitude_smooth"))
		
		fig2.add_traces(go.Scatter(x=t, y=ampli_smooth+ymin, name=filename+"_pmed"))
	
	return [pbase,ct,A1,A5,A10, deltaPmed]
	
	# print ("P_base",pbase)
	# print ("CT:",ct)	
	# print ("A1:",A1)
	# print ("A5:",A5)
	# print ("A10:",A10)
	
