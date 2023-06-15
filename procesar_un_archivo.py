import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema
from scipy.signal import savgol_filter

pathtofile = "/home/dario/Dropbox/MZP/desarrollo/software_medicion/procesamiento_amplitud_vilas02/archivosdedatos/RP-VI-442.dat"

mem_df = pd.read_csv(pathtofile, delimiter=' ').apply(pd.to_numeric)

#mem_df = mem_df.tail(2000).apply(pd.to_numeric)

x = mem_df['acu.t'].values/1000
#print x

y = mem_df['dat.pre'].values*-.0046



idx_max = argrelextrema(y, np.greater,order=3)[0]
idx_min = argrelextrema(y, np.less,order=3)[0]

ymax = [y[i] for i in idx_max]
ymin = [y[i] for i in idx_min]

print('len(ymin)',len(ymin))
print('len(ymax)',len(ymax))


if len(ymax)>len(ymin):
  #ymax = ymax[-len(ymin):]
  ymax = ymax[:len(ymin)]
  t = [x[i] for i in idx_min]

if len(ymin)>len(ymax):
  #ymin = ymin[-len(ymax):]
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

for i, num in enumerate(ampli_smooth):
    if num > 60 and ct == -1:
        ct = t[i]
        break

for i, num in enumerate(t):
  if num > ct+600 and  A10 == -1:
    A10 = ampli_smooth[i]
    break
  elif num > ct+300 and  A5 == -1:
    A5 = ampli_smooth[i]
  elif num > ct+60 and  A1 == -1:
    A1 = ampli_smooth[i]
  elif num > 100 and pbase == -1:
    pbase = ampli_smooth[i]
    print("tpbase: ",num)
    print("ymax: ",ymax[i])
    print("ymin: ",ymin[i])

    

print ("P_base",pbase)
print ("CT:",ct)
print ("A1:",A1)
print ("A5:",A5)
print ("A10:",A10)

fig= go.Figure()
fig.add_traces(go.Scatter(x=x, y=y, name="data"))
fig.add_traces(go.Scatter(x=x[idx_max], y=y[idx_max], name="top"))
fig.add_traces(go.Scatter(x=x[idx_min], y=y[idx_min], name="bottom"))
fig.update_layout(xaxis_title = r'$\text{Time } T \text{ in s}  $',
                      yaxis_title = r'$\text{Pressure } \text{ in Pa}$')
fig.update_layout(title= r'$\text{Viscoelastic trace}$')

fig1= go.Figure()
fig1.add_traces(go.Scatter(x=t, y=ampli, name="amplitude"))
fig1.add_traces(go.Scatter(x=t, y=ampli_smooth, name="amplitude smooth"))

fig.show()
fig1.show()
