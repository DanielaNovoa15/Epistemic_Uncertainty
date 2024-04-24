"""
--------------------- Espectro de Aceleraciones --------------------
---------------------- @author: Daniela Novoa ----------------------
"""
from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
import analisis as an
import utilidades as ut
import pickle
import pandas as pd
#%% LLAMAR BASES DE DATOS
filename = 'ZAS_AaAv' 
infile = open(filename,'rb')
bdAaAv = pickle.load(infile)
infile.close()
filename = 'ZAS_Fa' 
infile = open(filename,'rb')
bdFa = pickle.load(infile)
infile.close()
filename = 'ZAS_Fv' 
infile = open(filename,'rb')
bdFv = pickle.load(infile)
infile.close()
#%% CALCULO DE COEFICIENTES
cc = Ciud
tp = PerfTp
gu = Group
Tfdm = TEtabs
idAaAv = bdAaAv.query('Nombre == @cc')['ID'].to_numpy()[0]# Obtiene el valor de Aa

Aa = bdAaAv.Aa[idAaAv-1]
Av = bdAaAv.Av[idAaAv-1]
Fa = bdFa.query('Tipo_perfil == @tp')['Aa='+str(Aa)].to_numpy()[0]
Fv = bdFv.query('Tipo_perfil == @tp')['Av='+str(Av)].to_numpy()[0]
#%% ESPECTRO DE ACELERACIONES
To = 0.1*(Av*Fv)/(Aa*Fa)
Tc = 0.48*(Av*Fv)/(Aa*Fa)
Tl = 2.4*Fv
TVal = np.linspace(0,3.29,330)

Sa_list = []
for Tsa in TVal:
    if Tsa == 0:
        Sa = Aa*Fa*gu
    elif Tsa <= To:
        Sa = 2.5*Aa*Fa*gu*(0.4+0.6*(Tsa/To))
    elif Tsa <= Tc:
        Sa = 2.5*Aa*Fa*gu
    elif Tsa <= Tl:
        Sa = (1.2*Av*Fv*gu)/Tsa
    elif Tsa >= Tl:
        Sa = (1.2*Av*Fv*Tl*gu)/(Tsa**2)
    Sa_list.append(Sa)
#%%
dcc = {'Tval':TVal,'Sa':Sa_list}
dataSa = pd.DataFrame(dcc)
#%%
# sb.set_theme(style="ticks")
# plt.plot(TVal,Sa_list,'m',linewidth=2)
# plt.plot([Tfdm,Tfdm],[0.0,np.max(Sa_list)],'bo--',linewidth=.8)
# plt.title('Espectro de aceleraciones')
# plt.xlabel('T [s]')
# plt.ylabel('Sa [g]')
# plt.xlim(0,3.29,0.5)
# plt.ylim(0,np.max(Sa_list)+0.05,0.2) 

