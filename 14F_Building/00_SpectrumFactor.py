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
