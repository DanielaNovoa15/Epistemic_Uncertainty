"""
---------------------------- Análisis PushOver ---------------------------
------------------------- @author: Daniela Novoa -------------------------
"""
#%% ========================= IMPORTAR LIBRERIAS =========================
from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
import analisis as an
import utilidades as ut
import pandas as pd
import pickle
import dill as pickle
#%% ======================== PARÁMETROS DE ENTRADA =======================
# --------------------------Nombre del Arquetipo--------------------------
modelname = "PRUEBA1"                                          # Nombre del arquetipo 
# ------------------------Propiedades del material------------------------
fc = 21000                                                        # fc del concreto 
Fy = 420000                                                       # Fy del acero
#%% ================= IMPORTAR INFORMACIÓN DEL ARQUETIPO =================
# ----------------------Importar datos de Arquetipo-----------------------                                     # Nombre del arquetipo
# f2 = open('01_'+str(modelname)+'.py', mode='r+',encoding='UTF-8')
f2 = open(str(modelname)+'.py', mode='r+',encoding='UTF-8')
code_str2 = f2.read()
f2.close()
exec(code_str2, locals())
#%% ======================== ANÁLISIS DE GRAVEDAD ========================
# --------------------------Análisis de gravedad--------------------------
w1 = eigen(2)
T = 2*3.1416/np.sqrt(w1)
an.gravedad()
loadConst('-time',0.0)
print('---------------------------------------')
print('----Análisis de gravedad completado----')
print('---------------------------------------')
plt.figure()
opsv.plot_mode_shape(1)
plt.figure()
opsv.plot_defo()
print('---------------------------------------')
print('----- Periodo fundamental= '+str(np.around(T,2))+' -----')
print('---------------------------------------')
#%% ========================== ANÁLISIS PUSHOVER =========================
# ---------------------------Análisis Pushover----------------------------
w2 = eigen(1)
T2 = 2*3.1416/np.sqrt(w2)

timeSeries('Linear', 2)
pattern('Plain', 2, 2)

tagsnodos = getNodeTags()
ntecho = tagsnodos[-1]
hedif = nodeCoord(ntecho)[1]

POnodes = tagsnodos[int(1):int(len(tagsnodos)/nx)]
posnodes = []
for i in range(len(POnodes)):
    posnodes.append(i+1)
valor = sum(posnodes)

for indx,val in enumerate(tagsnodos[int(1):int(len(tagsnodos)/nx)]):
    load(val,(indx+1)/valor,0.0,0.0)
    
[dtecho,Vcorte]=an.pushover2(0.05*yloc[-1], 0.001, ntecho, 1, [hedif,Wedificio])

print('---------------------------------------')
print('-----Análisis PushOver completado------')
print('---------------------------------------')




plt.figure()
opsv.plot_defo()