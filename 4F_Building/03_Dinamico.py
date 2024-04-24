"""
---------------------------- Análisis Dinámico ---------------------------
------------------------- @author: Daniela Novoa -------------------------
"""
#%% IMPORTAR LIBRERIAS
from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
import analisis as an
import utilidades as ut
import pickle
import dill as pickle
import pandas as pd
import multiprocessing
import time
from statsmodels.distributions.empirical_distribution import ECDF
from joblib import Parallel, delayed  
#%% PARÁMETROS DE ENTRADA
# --------------------------Nombre del Arquetipo---------------------------
modelname = "01_Morumbi"                                 # Nombre del arquetipo 
# -------------------------Zona de amenaza sísmica-------------------------
Ciud = "CRT"                                               # No        mbre de la ciudad
PerfTp = "D"                                               # Perfil de suelo
Group = 1                                                  # Grupo de uso
TEtabs = 0.78                                              # Periodo fundamental de ETABS
TOpSees = 0.67                                             # Periodo fundamental OpenSees
# -------------------Elementos y nodos para gravar info-------------------
node_record = [2,7,11,15,19]                               # Nodos guardar información
ele_record = [27]                                          # Elementos guardar información
node_control = 22 
# ---------------------Parámetros del modelo dinámico---------------------
FE = 1.0                                                   # Factor escalar del modelo
n = 0                                                      # Número de modelos
#%% INFORMACIÓN DE REGISTROS
# -------------------------------Registros-------------------------------
records= ["GM01.txt", "GM02.txt", "GM03.txt", "GM04.txt", "GM05.txt", "GM06.txt", "GM07.txt", "GM08.txt", "GM09.txt", "GM10.txt", "GM11.txt", "GM12.txt", "GM13.txt", "GM14.txt", "GM15.txt",
          "GM16.txt", "GM17.txt", "GM18.txt", "GM19.txt", "GM20.txt", "GM21.txt", "GM22.txt", "GM23.txt", "GM24.txt", "GM25.txt", "GM26.txt", "GM27.txt", "GM28.txt", "GM29.txt", "GM30.txt",
          "GM31.txt", "GM32.txt", "GM33.txt", "GM34.txt", "GM35.txt", "GM36.txt", "GM37.txt", "GM38.txt", "GM39.txt", "GM40.txt", "GM41.txt", "GM42.txt", "GM43.txt", "GM44.txt"]
# ---------------------------No. Datos registro---------------------------
Nsteps= [3000, 3000, 2000, 2000, 5590, 5590, 4535, 4535, 9995, 9995, 7810, 7810, 4100, 4100, 4100, 4100, 5440, 5440, 6000, 6000, 2200, 2200, 11190, 11190, 7995, 7995, 7990, 7990, 2680, 2300, 8000, 8000, 2230, 2230, 1800, 1800, 18000, 18000, 18000, 18000, 2800, 2800, 7270, 7270]
# ----------------------------Paso del registro---------------------------
DTs= [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.005,0.005,0.01,0.01,0.01,0.01,0.005,0.005,0.05,0.05,0.02,0.02,0.0025,0.0025,0.005,0.005,0.005,0.005,0.02,0.02,0.005,0.005,0.01,0.01,0.02,0.02,0.005,0.005,0.005,0.005,0.01,0.01,0.005,0.005]                                                
# ---------------------------**SpectrumFactor**---------------------------
nEQ = len(records)                                         # Número de terremotos
# Abre el archivo espectro para calcular el Sa de diseño
exec(open('00_Espectro.py').read())
# Calcula el Sa de diseño
Sad = dataSa.query('Tval == @TEtabs')['Sa'].to_numpy()[0]  # Valor de Sa [g]
# Calula los factores espectrales
exec(open('00_SpectrumFactor.py').read())                  # Leer archivo.py proceso de calculo de factores espectrales                           
#%% VARIABILIDAD DEL MATERIAL
index2 = range(len(records))                               # Rango terremotos
mfc = 24500                                                # Valor medio de datos fc
cv = 0.15
sfc = cv*mfc                                               # Desviación estandar de la distribución para fc
Fc = np.random.normal(mfc,sfc,n)                           # Función de probabilidad de densidad (normal) para fc
mfy = 420000                                               # Valor medio de datos fy
cv2 = 0.1
sfy = cv2*mfy                                              # Desviación estandar de la distribución para fy
fy = np.random.normal(mfy,sfy,n)                           # Función de probabilidad de densidad (normal) para fy
variables=[]
for i in range(n):
    variables.append([Fc[i],fy[i]])                        # Variable almacena los fc y fy de la distribución
variables.append([mfc,mfy])                                # La variable almacena también el fc y fy nominales
n = n + 1
#%% IMPORTAR INFORMACIÓN DEL ARQUETIPO
# ----------------------Importar datos de Arquetipo-----------------------                              # Nombre del arquetipo 
f2 = open(str(modelname)+'.py', mode='r+',encoding='UTF-8')
code_str2 = f2.read()
f2.close()
#%% ANÁLISIS IDA 1 FACTOR ESCALAR
def runDyn(ind,var):
    fc = var[0]
    Fy = var[1]
    # -------------------------llamar Arquetipo---------------------------
    exec(code_str2, locals())
    # -----------------------Análisis de gravedad-------------------------
    w1 = eigen(1)
    T = 2*3.1416/np.sqrt(w1)
    an.gravedad()
    loadConst('-time',0.0)
    # ------------------------Análisis dinámico---------------------------
    tiempo,techo,Eds,node_disp,node_vel,node_acel,drift = an.dinamicoIDA4P(records[ind], DTs[ind], Nsteps[ind], DTs[ind], 9.81*SpectrumFactor[ind]*FE, 0.025, node_control, 1, ele_record, node_record)
    wipe()
    return tiempo,techo,Eds,node_disp,node_vel,node_acel,drift, fc, Fy, ind
#%% PROCESAR INFORMACION CON LOS NUCLEOS DEL PC
num_cores = multiprocessing.cpu_count()
stime = time.time()
resultados = Parallel(n_jobs=num_cores)(delayed(runDyn)(ii,ff) for ii in index2 for ff in variables) # loop paralelo
etime = time.time()
ttotal = etime - stime
print('---------------------------------------')
print('-----Análisis Dinámico completado------')
print('------ Tiempo de ejecución '+str(np.around(ttotal,2))+'------')
print('---------------------------------------') 
#%% Guardar resultados
filename = str(modelname)+'_results'+str(n)+'Mod_'+str(FE)+'FE'
outfile = open(filename,'wb')
pickle.dump(resultados,outfile)
outfile.close()
