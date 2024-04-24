"""
----------------------------- Spectrum Factor ----------------------------
------------------------- @author: Daniela Novoa -------------------------
"""
from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
import analisis as an
import utilidades as ut
import pickle
import pandas as pd
import multiprocessing
import time
from statsmodels.distributions.empirical_distribution import ECDF
from joblib import Parallel, delayed  

# -------------------------Zona de amenaza sísmica-------------------------
Ciud = "BUC"                                           # Nombre de la ciudad
PerfTp = "C"                                           # Perfil de suelo
Group = 1                                              # Grupo de uso
TEtabs = 1.42                                          # Periodo fundamental de ETABS
TOpSees = 1.14                                        # Periodo fundamental OpenSees
# -------------------------------Registros-------------------------------
records= ["GM01.txt", "GM02.txt", "GM03.txt", "GM04.txt", "GM05.txt", "GM06.txt", "GM07.txt", "GM08.txt", "GM09.txt", "GM10.txt", "GM11.txt", "GM12.txt", "GM13.txt", "GM14.txt", "GM15.txt",
          "GM16.txt", "GM17.txt", "GM18.txt", "GM19.txt", "GM20.txt", "GM21.txt", "GM22.txt", "GM23.txt", "GM24.txt", "GM25.txt", "GM26.txt", "GM27.txt", "GM28.txt", "GM29.txt", "GM30.txt",
          "GM31.txt", "GM32.txt", "GM33.txt", "GM34.txt", "GM35.txt", "GM36.txt", "GM37.txt", "GM38.txt", "GM39.txt", "GM40.txt", "GM41.txt", "GM42.txt", "GM43.txt", "GM44.txt"]
# ---------------------------No. Datos registro---------------------------
Nsteps= [3000, 3000, 2000, 2000, 5590, 5590, 4535, 4535, 9995, 9995, 7810, 7810, 4100, 4100, 4100, 4100, 5440, 5440, 6000, 6000, 2200, 2200, 11190, 11190, 7995, 7995, 7990, 7990, 2680, 2300, 8000, 8000, 2230, 2230, 1800, 1800, 18000, 18000, 18000, 18000, 2800, 2800, 7270, 7270]
# ----------------------------Paso del registro---------------------------
DTs= [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.005,0.005,0.01,0.01,0.01,0.01,0.005,0.005,0.05,0.05,0.02,0.02,0.0025,0.0025,0.005,0.005,0.005,0.005,0.02,0.02,0.005,0.005,0.01,0.01,0.02,0.02,0.005,0.005,0.005,0.005,0.01,0.01,0.005,0.005]
Nrec = len(records)                                    # Número de registros
nEQ = len(records)

# Abre el archivo espectro para calcular el Sa de diseño
exec(open('00_Espectro.py').read())
# Calcula el Sa de diseño
Sad = dataSa.query('Tval == @TEtabs')['Sa'].to_numpy()[0]  # Valor de Sa [g]
Sa_d = Sad
#%% CARGAR DATOS DEL FEMA
filename = 'SaFEMA'
infile = open(filename,'rb')
Sa2 = pickle.load(infile)
infile.close()
filename = 'TFEMA'
infile = open(filename,'rb')
T = pickle.load(infile)
infile.close()
#%% CALCULO DE FACTORES ESPECTRALES
Tt = np.transpose(T)
suma = 0
for i in range(len(Tt)):
    if Tt[i,0] < TOpSees:
        suma = suma+1
    else:
        suma = suma
indx = suma-1
SpectrumFactor = []
for i in range(int(nEQ)):
    SpectrumFactor.append(Sad/Sa2[indx,i])

#%%
plt.rcParams["figure.figsize"] = (6.3, 4.2)
plt.plot(Tt[0:248],Sa2[:,0][0:248]*SpectrumFactor[0],'gray',label='GM01-GM18',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,1][0:248]*SpectrumFactor[1],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,2][0:248]*SpectrumFactor[2],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,3][0:248]*SpectrumFactor[3],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,4][0:248]*SpectrumFactor[4],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,5][0:248]*SpectrumFactor[5],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,6][0:248]*SpectrumFactor[6],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,7][0:248]*SpectrumFactor[7],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,8][0:248]*SpectrumFactor[8],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,9][0:248]*SpectrumFactor[9],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,12][0:248]*SpectrumFactor[12],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,13][0:248]*SpectrumFactor[13],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,14][0:248]*SpectrumFactor[14],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,15][0:248]*SpectrumFactor[15],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,32][0:248]*SpectrumFactor[32],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,33][0:248]*SpectrumFactor[33],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,40][0:248]*SpectrumFactor[40],'gray',linewidth=1.0)
plt.plot(Tt[0:248],Sa2[:,41][0:248]*SpectrumFactor[41],'gray',linewidth=1.0)
plt.plot(TOpSees,Sad,'b.',label='Sa(T1)',markersize='6')
plt.legend()
plt.xticks(np.arange(0.0, 1.65, step=0.15))
plt.yticks(np.arange(0.0, 3.0, step=0.2))
plt.xlim(0.0,1.5)
plt.title('(b)',fontweight='bold', loc="center")
plt.suptitle("", y=0.92, fontsize=12)
plt.xlabel('Period [s]',fontsize=12)
plt.ylabel('Spectral acceleration [g]',fontsize=12)
plt.show()

