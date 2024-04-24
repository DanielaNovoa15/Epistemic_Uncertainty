"""
------------------------- Probabilidades de falla ------------------------
------------------------- @author: Daniela Novoa -------------------------
"""
#%% IMPORTAR LIBRERIAS
from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
import analisis as an
import utilidades as ut
import multiprocessing
import time
import seaborn as sb
import pickle
import dill as pickle
import NewmarkL as new
import pandas as pd
import vfo.vfo as vfo
from statsmodels.distributions.empirical_distribution import ECDF
from joblib import Parallel, delayed 
#%% PARÁMETROS DE ENTRADA
modelname = "04_BUC_14PV2"                             # Nombre del arquetipo 
# ----------------------------Datos del modelo---------------------------
Nmod = 301                                             # Número de modelos
Npisos = 14                                            # Número de pisos
FE = 1.0
#%% CARGAR EL PICKLE DE LOS RESULTADOS DINÁMICOS
# filename = str(modelname)+'_results'+str(Nmod)+'Mod'+'_FE'+str(FE)   # Nombre del archivo a cargar
# infile = open(filename,'rb')
# resultados = pickle.load(infile)
# infile.close()
#%% EXAMINAR LOS DATOS
# ---------------------Tupla de resultados contiene=--------------------
    #[0]: tiempo (s)
    #[1]: techo (m)
    #[2]: fuerzas en los elementos (kN,m)
    #[3]: desplazamientos (m)
    #[4]: velocidades (m/s)
    #[5]: aceleraciones (m/s2)
    #[6]: derivas (m/m)
    #[7]: fc del modelo (kPa)
    #[8]: fy del modelo (kPa)
    #[9]: registro ()
#%% INFORMACIÓN DE LOS REGISTROS
# -------------------------------Registros-------------------------------
records= ["GM01.txt", "GM02.txt", "GM03.txt", "GM04.txt", "GM05.txt", "GM06.txt", "GM07.txt", "GM08.txt", "GM09.txt", "GM10.txt", "GM11.txt", "GM12.txt", "GM13.txt", "GM14.txt", "GM15.txt",
          "GM16.txt", "GM17.txt", "GM18.txt", "GM19.txt", "GM20.txt", "GM21.txt", "GM22.txt", "GM23.txt", "GM24.txt", "GM25.txt", "GM26.txt", "GM27.txt", "GM28.txt", "GM29.txt", "GM30.txt",
          "GM31.txt", "GM32.txt", "GM33.txt", "GM34.txt", "GM35.txt", "GM36.txt", "GM37.txt", "GM38.txt", "GM39.txt", "GM40.txt", "GM41.txt", "GM42.txt", "GM43.txt", "GM44.txt"]
# ---------------------------No. Datos registro---------------------------
Nsteps= [3000, 3000, 2000, 2000, 5590, 5590, 4535, 4535, 9995, 9995, 7810, 7810, 4100, 4100, 4100, 4100, 5440, 5440, 6000, 6000, 2200, 2200, 11190, 11190, 7995, 7995, 7990, 7990, 2680, 2300, 8000, 8000, 2230, 2230, 1800, 1800, 18000, 18000, 18000, 18000, 2800, 2800, 7270, 7270]
# ----------------------------Paso del registro---------------------------
DTs= [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.005,0.005,0.01,0.01,0.01,0.01,0.005,0.005,0.05,0.05,0.02,0.02,0.0025,0.0025,0.005,0.005,0.005,0.005,0.02,0.02,0.005,0.005,0.01,0.01,0.02,0.02,0.005,0.005,0.005,0.005,0.01,0.01,0.005,0.005]
Nrec = len(records)                                     # Número de registros
#%% PROCESADO DE TODOS LOS DATOS
# # Aquí se generan las variables que seán almacenadas en un dataframe                       
# tgm = np.zeros(Nrec*Nmod)                               # Almacena el tiempo del sismo
# for i in range(len(Nsteps)):
#     t = Nsteps[i]*DTs[i]*0.98                                # Calcula el tiempo del sismo
#     tgm[Nmod*i:Nmod*(i+1)] = t                          # Almacena en una lista el tiempo del sismo para la cantidad de modelos analizados

# Model = [i+1 for i in range(Nmod)]*Nrec                 # Modelo de análisis

# record,max_d,fc,fy,acel,Dts,acel_rec,t_record = [],[],[],[],[],[],[],[] # registro, maxima deriva, fc, fy, aceleración relativa, dt, aceleración del registro, tiempo máximo del registro
# # Este ciclo recorre todos los resultados y calcula las máximas derivas por modelo y registro
# ss = time.time()
# for indx1, res in enumerate(resultados):
#     modelo = int(indx1/Nrec) + 1
#     record.append(res[9]+1)                            # Almacena el registro del análisis
#     t_record.append(np.around(res[0][-1],2))           # Almacena el tiempo máximo del registro 
#     max_d.append(np.max(np.abs(res[6])))               # Almacena la máxima deriva del piso en que ocurrió
#     fc.append(res[7])                                  # Almacena el fc del modelo
#     fy.append(res[8])                                  # Almacena el fy del modelo
#     acel.append(res[5])                                # Almacena las aceleraciones relativas por piso para cada registro por modelo
#     Dts.append(res[0][1])                              # Almacena el paso del registro por modelo
#     acel_rec.append(np.hstack((0,np.loadtxt(records[res[9]])*9.81))) # Almacena la aceleración del registro
# se = time.time()                                       # Calcula el tiempo que se demoró el programa en crear las variables del DataFrame
# # Se ajusta el valor de la deriva máxima por convergencia
# val_col = 0.5                                          # Valor max_d cuando no converge
# converg = t_record > tgm                          # 1 si converge, 0 si no
# dmax_aj = max_d*converg + val_col*(1-converg)          # deriva máxima corregida 
# print('---------------------------------------')
# print('------Los datos fueron procesados------')
# print('------ Tiempo de ejecución '+str(np.around(se-ss,2))+'------')
# print('---------------------------------------') 
#%% CREAR EL DATAFRAME DE DERIVAS MÁXIMAS
# ---DFD será el dataframe que contendrá modelo,record,deriva maxima----
# dic = {'modelo':Model, 'record':record, 't_record':t_record,'tgm':tgm, 'max_d': max_d, 'fc': fc, 'fy': fy, 'converg':converg, 'dmax_aj':dmax_aj,'acel':acel,'Dts':Dts,'acel_rec':acel_rec}  
# dfd = pd.DataFrame(dic)
# print('---------------------------------------')
# print('-------DataFrame de Datos creado-------')
# print('---------------------------------------')
#%% CREAR EL DATAFRAME DE DERIVAS MÁXIMAS CORREGIDAS
# trecord,nmrecord,maxder,fc2,fy2,acel2,Dts2,acelrec = [],[],[],[],[],[],[],[]
# for i in range(Nmod):
#     indxnw = dfd.index[(dfd['record']==i+1)]
#     for j in indxnw:
#         trecord.append(dfd['t_record'][j])
#         nmrecord.append(dfd['record'][j])
#         maxder.append(dfd['max_d'][j])
#         fc2.append(dfd['fc'][j])
#         fy2.append(dfd['fy'][j])
#         acel2.append(dfd['acel'])
#         Dts2.append(dfd['Dts'])
#         acelrec.append(dfd['acel_rec'])
# converg2 = trecord > 0.98*tgm                          # 1 si converge, 0 si no
# dmax_aj2 = maxder*converg2 + val_col*(1-converg2)     
# dic2 = {'modelo':Model, 'record':nmrecord, 't_record':trecord,'tgm':tgm, 'max_d': maxder, 'fc': fc2, 'fy': fy2, 'converg':converg2, 'dmax_aj':dmax_aj2}  
# dfd2 = pd.DataFrame(dic2)
# print('---------------------------------------')
# print('------DataFrame de Datos 2 creado------')
# print('---------------------------------------')
#%% GUARDAR DATAFRAME DE DERIVAS
# filename = str(modelname)+'dataframeprob'+'1Mod'
# outfile = open(filename,'wb')
# pickle.dump(dfd2,outfile)
# outfile.close()
#%% CARGAR EL PICKLE DEL DATAFRAME DE DERIVAS
filename = str(modelname)+'dataframeprob'+'1Mod'   # Nombre del archivo a cargar
infile = open(filename,'rb')
dfd = pickle.load(infile)
infile.close()
dfd = dfd.rename(columns={'modelo':'Model'})
#%% EXTRAER DEL DATAFRAME DERIVAS MÁXIMAS LOS REGISTROS QUE NO FALLAN Y LOS QUE FALLAN
# ---------Se definen los cuatro limites de los estados de daño---------
lim_col = 0.06                                         # Limite de la probabilidad de colapso    
lim_lig = 0.01
lim_mod = 0.02
lim_sev = 0.04
# ---------------------Dataframe de estados de daño---------------------
# Almacena en un dataframe nuevo la condición dmáx ajustado sea mayor al límite de cada estado de daño
dfd_lig = dfd.query('dmax_aj >= @lim_lig')
dfd_mod = dfd.query('dmax_aj >= @lim_mod')
dfd_sev = dfd.query('dmax_aj >= @lim_sev')
dfd_col = dfd.query('dmax_aj > @lim_col') 
# ---------------------Dataframe agrupar por modelo---------------------
# Almacena en un dataframe el número de veces en que se sobrepasó el límite en cierto modelo
# Agrupa por modelo, cuenta cuántas veces el dmáx ajustado es mayor al límite y cuando hay un nan asigna un 0
idx = np.arange(1,302)
prob_col = dfd_col.groupby('Model').count().fillna(0)
prob_col = prob_col.reindex(idx, fill_value=0)
prob_lig = dfd_lig.groupby('Model').count().fillna(0)
prob_lig = prob_lig.reindex(idx, fill_value=0)
prob_mod = dfd_mod.groupby('Model').count().fillna(0)
prob_mod = prob_mod.reindex(idx, fill_value=0)
prob_sev = dfd_sev.groupby('Model').count().fillna(0)
prob_sev = prob_sev.reindex(idx, fill_value=0)
# -------------------Nueva columna con probabilidades-------------------
# Nueva columna en el dataframe con las probabilidades de excedencia
# Se le indica una columna cualquiera al dataframe agrupado por modelo y se divide por el número de registros
prob_col['P(SDR$_{max}$>DS$_{limit}$)'] = prob_col.t_record/Nrec
prob_lig['P(SDR$_{max}$>DS$_{limit}$)'] = prob_lig.t_record/Nrec
prob_mod['P(SDR$_{max}$>DS$_{limit}$)'] = prob_mod.t_record/Nrec
prob_sev['P(SDR$_{max}$>DS$_{limit}$)'] = prob_sev.t_record/Nrec
# ---------Nueva columna con fc y fy correspondiente al modelo----------
# Nueva columna con fc y fy correspondiente al modelo
# Agrupa por modelo, saca el valor de fc y fy por modelo, almacena el valor en MPa
namefc = "f'c [MPa]"
namefy = 'fy [MPa]'
prob_col[namefc] = ((dfd.groupby('Model').mean()/1000).fc)
prob_col[namefy] = ((dfd.groupby('Model').mean()/1000).fy)
prob_lig[namefc] = ((dfd.groupby('Model').mean()/1000).fc)
prob_lig[namefy] = ((dfd.groupby('Model').mean()/1000).fy)
prob_mod[namefc] = ((dfd.groupby('Model').mean()/1000).fc)
prob_mod[namefy] = ((dfd.groupby('Model').mean()/1000).fy)
prob_sev[namefc] = ((dfd.groupby('Model').mean()/1000).fc)
prob_sev[namefy] = ((dfd.groupby('Model').mean()/1000).fy)
print('---------------------------------------')
print('---DataFrame de probabilidades creado--')
print('---------------------------------------')
#%% GENERAR GRÁFICOS
# ---------------PROBABILIDAD DE EXCEDENCIA LÍMITE LIGERO--------------
sb.set_theme(style='whitegrid')
cmap = sb.cubehelix_palette(n_colors=6,start=6,rot=-2.0,as_cmap=True)

g = sb.relplot(
    data = prob_lig,
    x = 'Model', y = 'P(SDR$_{max}$>DS$_{limit}$)',
    hue = namefc, size = namefy,
    palette = cmap, sizes = (5,140),).set(title='a. ISAI (3 stories)')

g.ax.xaxis.grid(True, "minor", linewidth=.25)
g.ax.yaxis.grid(True, "minor", linewidth=.25)
g.ax.set_yticks(np.arange(0.00, 0.75, step=0.05))
g.ax.set_title('', fontweight='bold', fontsize = 16)
g.ax.set_xlabel('Model', fontsize = 14)
g.ax.set_ylabel('Probability of exceedance', fontsize = 14)
g.despine(left=True, bottom=True)
# #%% --------------PROBABILIDAD DE EXCEDENCIA LÍMITE MODERADO-------------
# g = sb.relplot(
#     data = prob_mod,
#     x = 'Model', y = 'P(SDR$_{max}$>DS$_{limit}$)',
#     hue = namefc, size = namefy,
#     palette = cmap, sizes = (5,130),).set(title='Probabilidad de excedencia límite Moderado')
# g.ax.xaxis.grid(True, "minor", linewidth=.25)
# g.ax.yaxis.grid(True, "minor", linewidth=.25)
# g.ax.set_yticks(np.arange(0.00, 0.16, step=0.02))
# g.ax.set_title('', fontweight='bold', fontsize = 16)
# g.ax.set_xlabel('Model', fontsize = 14)
# g.ax.set_ylabel('P(SDR$_{max}$>DS$_{limit}$)', fontsize = 14)
# g.despine(left=True, bottom=True)
# #%% ---------------PROBABILIDAD DE EXCEDENCIA LÍMITE SEVERO--------------
# g = sb.relplot(
#     data = prob_sev,
#     x = 'Model', y = 'P(SDR$_{max}$>DS$_{limit}$)',
#     hue = namefc, size = namefy,
#     palette = cmap, sizes = (5,130),).set(title='Probabilidad de excedencia límite Severo')
# g.ax.xaxis.grid(True, "minor", linewidth=.25)
# g.ax.yaxis.grid(True, "minor", linewidth=.25)
# g.ax.set_yticks(np.arange(0.00, 0.12,step=0.02))
# g.ax.set_title('', fontweight='bold', fontsize = 16)
# g.ax.set_xlabel('Model', fontsize = 14)
# g.ax.set_ylabel('P(SDR$_{max}$>DS$_{limit}$)', fontsize = 14)
# g.despine(left=True, bottom=True)
# # %% --------------PROBABILIDAD DE EXCEDENCIA LÍMITE COLAPSO--------------
g = sb.relplot(
    data = prob_col,
    x = 'Model', y = 'P(SDR$_{max}$>DS$_{limit}$)',
    hue = namefc, size = namefy,
    palette = cmap, sizes = (5,130),).set(title='Probabilidad de excedencia límite Colapso')
g.ax.xaxis.grid(True, "minor", linewidth=.25)
g.ax.yaxis.grid(True, "minor", linewidth=.25)
g.ax.set_yticks(np.arange(0.00, 0.12,step=0.02))
g.ax.set_title('', fontweight='bold', fontsize = 16)
g.ax.set_xlabel('Model', fontsize = 14)
g.ax.set_ylabel('Probability of exceedance', fontsize = 14)
g.despine(left=True, bottom=True)


