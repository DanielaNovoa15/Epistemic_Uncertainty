"""
------------------------ Factores de amplificación -----------------------
------------------------- @author: Daniela Novoa -------------------------
"""
#%% IMPORTAR LIBRERIAS
from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import analisis as an
import utilidades as ut
import multiprocessing
import time
import seaborn as sb
import pickle
import NewmarkL as new
import pandas as pd
import vfo.vfo as vfo
from statsmodels.distributions.empirical_distribution import ECDF
from joblib import Parallel, delayed 
import dill as pickle
#%% PARÁMETROS DE ENTRADA
modelname = "ISAI"                                     # Nombre del arquetipo 
# ----------------------------Datos del modelo---------------------------
Nmod = 300                                             # Número de modelos
Npisos = 3                                             # Número de pisos
FE = 1.0
# -------------------------Propiedades nominales-------------------------
fcNom = 21000                                          # fc del concreto 
aa = [3.2/9.6,6.4/9.6,9.6/9.6]                         # altura normalizada
# -------------------------Zona de amenaza sísmica-------------------------
Ciud = "CRT"                                           # Nombre de la ciudad
PerfTp = "D"                                           # Perfil de suelo
Group = 1                                              # Grupo de uso
TEtabs = 0.79                                          # Periodo fundamental de ETABS
TOpSees = 0.67                                         # Periodo fundamental OpenSees 
# #%% CARGAR EL PICKLE DE LOS RESULTADOS DINÁMICOS
# filename = 'results300Mod'                             # Nombre del archivo a cargar
# infile = open(filename,'rb')
# resultados = pickle.load(infile)                       # Tupla que almacena los resultados
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
# #%% INFORMACIÓN DE LOS REGISTROS
# Estos resultados van por modelo. 44 registros de un modelo y despues los siguientes 44 del otro.
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
# Calula los factores espectrales
exec(open('00_SpectrumFactor.py').read())                  # Leer archivo.py proceso de calculo de factores espectrales    
SpectrumFactorR = np.array(SpectrumFactor)*9.81            # Variable a entregar
# #%% PROCESADO DE TODOS LOS DATOS
# # Aquí se generan las variables que seán almacenadas en un dataframe                       
# tgm = []                           # Almacena el tiempo del sismo
# for i in range(Nrec):
#     t = Nsteps[i]*DTs[i]*0.98                           # Calcula el tiempo del sismo
#     tgm.append(t)                                      # Almacena en una lista el tiempo del sismo para la cantidad de modelos analizados
# tgm = tgm*Nmod
# # Model = [i+1 for i in range(Nmod)]*Nrec                 # Modelo de análisis

# modelo,record,max_d,fc,fy,acel,Dts,acel_rec,t_record = [],[],[],[],[],[],[],[],[] # registro, maxima deriva, fc, fy, aceleración relativa, dt, aceleración del registro, tiempo máximo del registro
# # Este ciclo recorre todos los resultados y calcula las máximas derivas por modelo y registro
# ss = time.time()
# for indx1, res in enumerate(resultados):
#     modelo.append(int(indx1/Nrec) + 1)
#     record.append(res[9]+1)                            # Almacena el registro del análisis
#     t_record.append(np.around(res[0][-1],2))           # Almacena el tiempo máximo del registro 
#     max_d.append(np.max(np.abs(res[6])))               # Almacena la máxima deriva del piso en que ocurrió
#     fc.append(res[7])                                  # Almacena el fc del modelo
#     fy.append(res[8])                                  # Almacena el fy del modelo
#     acel.append(res[5])                                # Almacena las aceleraciones relativas por piso para cada registro por modelo
#     Dts.append(res[0][1])                              # Almacena el paso del registro por modelo
#     factoran = SpectrumFactorR[res[9]]
#     acel_rec.append(np.hstack((0,np.loadtxt(records[res[9]])*factoran))) # Almacena la aceleración del registro
# se = time.time()                                       # Calcula el tiempo que se demoró el programa en crear las variables del DataFrame
# # Se ajusta el valor de la deriva máxima por convergencia
# val_col = 0.5                                          # Valor max_d cuando no converge
# converg = t_record > tgm                               # 1 si converge, 0 si no
# dmax_aj = max_d*converg + val_col*(1-converg)          # deriva máxima corregida 
# print('---------------------------------------')
# print('------Los datos fueron procesados------')
# print('------ Tiempo de ejecución '+str(np.around(se-ss,2))+'------')
# print('---------------------------------------') 
# #%% CREAR EL DATAFRAME DE DERIVAS MÁXIMAS
# # ---DFD será el dataframe que contendrá modelo,record,deriva maxima----
# dic = {'modelo':modelo, 'record':record, 't_record':t_record,'tgm':tgm, 'max_d': max_d, 'fc': fc, 'fy': fy, 'converg':converg, 'dmax_aj':dmax_aj,'acel':acel,'Dts':Dts,'acel_rec':acel_rec}  
# dfd = pd.DataFrame(dic)
# print('---------------------------------------')
# print('-------DataFrame de Datos creado-------')
# print('---------------------------------------')
# #%% EXTRAER DEL DATAFRAME DERIVAS MÁXIMAS LOS REGISTROS QUE NO FALLAN Y LOS QUE FALLAN
# lim_col = 0.06                                         # Limite de la probabilidad de colapso    
# indnf = (lim_col >= dfd['dmax_aj']) & (dfd['t_record'] >= dfd['tgm'])      # indices de los registros que no fallaron                     
# # dfnf es un dataframe de los registros que no fallan, es decir, que tienen una deriva menor que lim_colapso y que el tiempo del analisis es mayor al tiempo del registro
# dfnf = dfd.query('t_record >= tgm & @lim_col >= dmax_aj')
# print('---------------------------------------')
# print('--DataFrame reg. que No Fallan creado--')
# print('---------------------------------------')
# #%% GUARDAR EL DATAFRAME DE ACELERACIONESS
# filename = str(modelname)+'dataframederivasDEF' # Nombre del archivo a almacenar
# outfile = open(filename,'wb')
# pickle.dump(dfnf,outfile)
# outfile.close()
# #%% PROCESADO DE LAS ACELERACIONES
# # dfa es el dataframe de aceleraciones y dfanf en donde estan donde NO FALLAN
# # el DataFrame almacena datos del modelo, registro, aceleracion relativa, fc, fy
# # Dts del registro y aceleracion del registro
# dic2 = {'modelo':modelo, 'record':record, 'acel':acel, 'fc': fc, 'fy': fy, 'Dts':Dts,'acel_rec':acel_rec}
# dfa = pd.DataFrame(dic2)
# dfanf = dfa.loc[indnf] #DataFrame de las acelearciones que NO FALLAN
# # dfanf_Dts es el dataframe de aceleraciones donde estan solo los datos donde
# # el Dts del registro es igual a 0.01 segundos
# dfanf_Dts = dfanf.query('Dts==0.01')
# #%% ACELERACIÓN ABSOLUTA
# # El ciclo calcula la aceleración absolta de piso
# aabs = []
# for indx4 in range(len(dfanf_Dts)):
#     aa = dfanf_Dts.acel.iloc[indx4]                     # Obtener del dataframe las aceleraciones relativas 
#     arec = dfanf_Dts.acel_rec.iloc[indx4]               # Obtener del dataframe las aceleraciones del registro
#     acabs = np.zeros((len(arec),Npisos))                # Crear una matriz de ceros para almacenar la aceleración absoluta por piso
#     for indx5 in range(Npisos):
#         aa_abs = aa[:,indx5+1] + arec                   # Suma de aceleración relativa de un piso y la aceleración del registro correspondiente
#         acabs[:,indx5] = aa_abs                         # Almacenar la información en la matriz de ceros
#     aabs.append(acabs)
# # El DataFrame ahora tiene una columna con las aceleraciones absolutas por piso
# dfanf_Dts['acel_abs']=aabs
# print('---------------------------------------')
# print('----Aceleración absoluta calculada ----')
# print('---------------------------------------')
#%% GUARDAR RESULTADOS DEL ANÁLISIS
# filename = str(modelname)+'dataframeacelDef' # Nombre del archivo a almacenar
# outfile = open(filename,'wb')
# pickle.dump(dfanf_Dts,outfile)
# outfile.close()
#%% CARGAR EL DATAFRAME DE ACELERACIONES
# filename = str(modelname)+'dataframeacel2'                 # Nombre del archivo a cargar
filename = str(modelname)+'dataframeacelDef'                 # Nombre del archivo a cargar
infile = open(filename,'rb')
dfanf_Dts = pickle.load(infile)
infile.close()
# #%% ACELERACIÓN DEL COMPONENTE (MÁXIMA EN VALOR ABSOLUTO) (Newmark)
# # Este codigo funciona para cualquier cantidad de pisos y periodos.
# # La tupla tiene la longitud del dataframe de donde se obtuvo la info.
# # Dentro de cada resultado hay 2 arrays: El primero corresponde a las aceleraciones
# # del componente y el segundo a el desplazamiento. Los arrays almacenan por columnas
# # los resultados por piso y por filas los resultados por periodo.
# # stime = time.time()
TcVar = np.linspace(0.06,3.0,100)                       # Valores de periodo de componente
Nper = len(TcVar)                                       # Longitud del array TcVar

# def comp_per(indx6):
#     acomp = np.zeros((Nper,Npisos))                    # Crear matriz de ceros que almacene la aceleración del componente por piso
#     dcomp = np.zeros((Nper,Npisos))                    # Crear matriz de ceros que almacene el desplazamiento del componente por piso
#     acelpiso = dfanf_Dts.acel_abs.iloc[indx6]          # Obtener del dataframe la aceleración absoluta de piso
#     for indx7 in range(Npisos):
#         accomp = acelpiso[:,indx7]                     # Obtener la aceleración absoluta de un piso
#         for indx8, per in enumerate(TcVar):
#             T,U,V,A = new.newmarkLA(per,0.05,accomp,0.01,'max') # Calcula desplazamiento, velocidad y aceleración del componente con el método de Newmark
#             acomp[indx8,indx7] = A                     # Almacenar en la matriz de ceros el resultado de aceleraciones del componente
#             dcomp[indx8,indx7] = U                     # Almacenar en la matriz de ceros el resultado de desplazamientos del componente
#     return acomp,dcomp

# index6 = range(len(dfanf_Dts))
# # Por temas de fluido eléctrico, se decidió partir el número total de simulaciones en nparts
# nparts = 10
# variables2 = np.array_split(index6, nparts) # divide en nparts las N simulaciones. Las devuelve en un arreglo de numpy
# variables1 = [list(array) for array in variables2] # la volvemos a hacer como una lista
# num_cores = multiprocessing.cpu_count() 
# stime = time.time()
# resultcomp = []
# # EL ciclo a continuación recorre las partes creadas y las corre una a una
# for indx,varia in enumerate(variables1):
#     print('Corriendo la parte ', indx)
#     # esta parte del ciclo guarda en un picke los resultados de cada parte en la que se dividió el número de simulaciones
#     with open('logfile.txt', 'w') as f:
#         print('Corriendo la parte ', indx, file = f)
#         print('Terminó de correr')
#     res = Parallel(n_jobs=num_cores,prefer="threads")(delayed(comp_per)(ff) for ff in varia)
#     print('Terminó de correr la parte ', indx)
    
#     filename = str(modelname)+'_resultscompDef'+str(Nmod)+'Mod'+'_FE'+str(FE)+'_parte'+str(indx)
#     outfile = open(filename,'wb')
#     pickle.dump(res,outfile)
#     outfile.close()
    
#     # de todas formas guarda en una sola variable los resultados
#     resultcomp = resultcomp + res
    
# etime = time.time()
# ttotal = etime - stime
# print('---------------------------------------')
# print('-----Análisis Dinámico completado------')
# print('------ Tiempo de ejecución '+str(np.around(ttotal,2))+'------')
# print('---------------------------------------') 

# filename = str(modelname)+'_resultsCompDef'+str(Nmod)+'Mod' # Nombre del archivo a almacenar
# outfile = open(filename,'wb')
# pickle.dump(resultcomp,outfile)
# outfile.close()
#%% CARGAR RESULTADOS DEL ANÁLISIS
# filename = str(modelname)+'_resultsComp2'+str(Nmod)+'Mod'  # Nombre del archivo a cargar
filename = str(modelname)+'_resultsCompDef'+str(Nmod)+'Mod'  # Nombre del archivo a cargar
infile = open(filename,'rb')
resultcomp = pickle.load(infile)
infile.close()
#%% MODIFICAR DATAFRAME CON NUEVOS DATOS
result = resultcomp
acele_comp = []
acele_compg = []

ffap = np.zeros((Nper,Npisos,len(dfanf_Dts)))
Fap = []
accl22 = np.zeros((Nper,Npisos,len(dfanf_Dts)))
acl_PGa = []
for indx8, val in enumerate(dfanf_Dts['modelo'].index.tolist()):
    acele_comp.append(result[indx8][0])
    acele_compg.append(result[indx8][0]/9.81)
    maxrecord = np.abs(dfanf_Dts.acel_rec[val]).max()
    for pso in range(Npisos):
        maxaceabs = np.abs(dfanf_Dts.acel_abs[val][:,pso]).max()
        ffap[:,pso,indx8] = result[indx8][0][:,pso]/maxaceabs
        accl22[:,pso,indx8] = result[indx8][0][:,pso]/maxrecord
    Fap.append(ffap[:,:,indx8])
    acl_PGa.append(accl22[:,:,indx8])
# Se añaden las nuevas columnas al dataframe inicial
dfanf_Dts['acelPGA'] = acl_PGa
dfanf_Dts['acel_comp']=acele_comp
dfanf_Dts['fact_amp']=Fap
dfanf_Dts['acel_compG']=acele_compg
#%% FACTOR DE AMPLIFICACION POR PERIODO->Tupla de longitud = Nper. FA por No.Record
fapp = np.zeros((len(dfanf_Dts),Npisos))                 # Crear matriz de ceros para almacenar los factores de amplificación por piso
aclPga = np.zeros((len(dfanf_Dts),Npisos))
aclComp = np.zeros((len(dfanf_Dts),Npisos))
aclCompG = np.zeros((len(dfanf_Dts),Npisos))
def median(indx9):
    for indx10 in range(len(Fap)):
        fapp[indx10,:] = Fap[indx10][indx9]              # Resultado por periodo por piso
        aclPga[indx10,:] = acl_PGa[indx10][indx9]
        aclComp[indx10,:] = acele_comp[indx10][indx9]
        aclCompG[indx10,:] = acele_compg[indx10][indx9]
    return fapp,aclPga,aclComp,aclCompG
index9 = range(Nper)
num_cores = multiprocessing.cpu_count()                  # Num nucleos en el PC
factor_ampl = Parallel(n_jobs=num_cores)(delayed(median)(ff) for ff in index9) # loop paralelo
print('---------------------------------------')
print('---Factor de amplificación calculado---')
print('---------------------------------------')
#%% FACTOR DE AMPLIFICACIÓN POR PERIODO PARA EL MODELO NOMINAL
dfnominal = dfanf_Dts.query('fc == @fcNom')
fapnominal = np.zeros((len(dfnominal),Npisos))
aclpganom = np.zeros((len(dfnominal),Npisos))
aclCompnom = np.zeros((len(dfnominal),Npisos))
aclCompnomG = np.zeros((len(dfnominal),Npisos))
def median(indx9):
    for indx,val in enumerate(dfnominal['modelo'].index.tolist()):
        fapnominal[indx,:] = dfnominal['fact_amp'][val][indx9]
        aclpganom[indx,:] = dfnominal['acelPGA'][val][indx9]
        aclCompnom[indx,:] = dfnominal['acel_comp'][val][indx9]
        aclCompnomG[indx,:] = dfnominal['acel_compG'][val][indx9]
    return fapnominal,aclpganom,aclCompnom,aclCompnomG
index9 = range(Nper)
num_cores = multiprocessing.cpu_count()                  # Num nucleos en el PC
tuplanominal = Parallel(n_jobs=num_cores)(delayed(median)(ff) for ff in index9) # loop paralelo
print('---------------------------------------')
print('-Factor de amplificación Nom calculado-')
print('---------------------------------------')
#%% MEDIANA, PERCENTIL 84 Y 16 DE FA
# Se calculan la mediana, percentil 84% y percentil 16% de los factores de 
# amplificación por piso

Median = np.zeros((Nper,Npisos))
MedianNom= np.zeros((Nper,Npisos))
Perc_84 = np.zeros((Nper,Npisos))
PercNom_84 = np.zeros((Nper,Npisos))
Perc_16 = np.zeros((Nper,Npisos))
PercNom_16 = np.zeros((Nper,Npisos))
for i in range(Nper):
    for j in range(Npisos):
        Median[i,j] = np.median(factor_ampl[i][0][:,j])
        MedianNom[i,j] = np.median(tuplanominal[i][0][:,j])
        Perc_84[i,j] = np.percentile(factor_ampl[i][0][:,j],84)
        PercNom_84[i,j] = np.percentile(tuplanominal[i][0][:,j],84)
        Perc_16[i,j] = np.percentile(factor_ampl[i][0][:,j],16)
        PercNom_16[i,j] = np.percentile(tuplanominal[i][0][:,j],16)

MedianPGA = np.zeros((Nper,Npisos))
MedianNomPGA= np.zeros((Nper,Npisos))
Perc_84PGA = np.zeros((Nper,Npisos))
PercNom_84PGA = np.zeros((Nper,Npisos))
Perc_16PGA = np.zeros((Nper,Npisos))
PercNom_16PGA = np.zeros((Nper,Npisos))
for i in range(Nper):
    for j in range(Npisos):
        MedianPGA[i,j] = np.median(factor_ampl[i][1][:,j])
        MedianNomPGA[i,j] = np.median(tuplanominal[i][1][:,j])
        Perc_84PGA[i,j] = np.percentile(factor_ampl[i][1][:,j],84)
        PercNom_84PGA[i,j] = np.percentile(tuplanominal[i][1][:,j],84)
        Perc_16PGA[i,j] = np.percentile(factor_ampl[i][1][:,j],16)
        PercNom_16PGA[i,j] = np.percentile(tuplanominal[i][1][:,j],16)

MedianComp = np.zeros((Nper,Npisos))
MedianNomComp= np.zeros((Nper,Npisos))
Perc_84Comp = np.zeros((Nper,Npisos))
PercNom_84Comp = np.zeros((Nper,Npisos))
Perc_16Comp = np.zeros((Nper,Npisos))
PercNom_16Comp = np.zeros((Nper,Npisos))
for i in range(Nper):
    for j in range(Npisos):
        MedianComp[i,j] = np.median(factor_ampl[i][2][:,j])
        MedianNomComp[i,j] = np.median(tuplanominal[i][2][:,j])
        Perc_84Comp[i,j] = np.percentile(factor_ampl[i][2][:,j],84)
        PercNom_84Comp[i,j] = np.percentile(tuplanominal[i][2][:,j],84)
        Perc_16Comp[i,j] = np.percentile(factor_ampl[i][2][:,j],16)
        PercNom_16Comp[i,j] = np.percentile(tuplanominal[i][2][:,j],16)
        
MedianCompG = np.zeros((Nper,Npisos))
MedianNomCompG= np.zeros((Nper,Npisos))
Perc_84CompG = np.zeros((Nper,Npisos))
PercNom_84CompG = np.zeros((Nper,Npisos))
Perc_16CompG = np.zeros((Nper,Npisos))
PercNom_16CompG = np.zeros((Nper,Npisos))
Perc_50CompG = np.zeros((Nper,Npisos))
PercNom_50CompG = np.zeros((Nper,Npisos))
for i in range(Nper):
    for j in range(Npisos):
        MedianCompG[i,j] = np.median(factor_ampl[i][3][:,j])
        MedianNomCompG[i,j] = np.median(tuplanominal[i][3][:,j])
        Perc_84CompG[i,j] = np.percentile(factor_ampl[i][3][:,j],84)
        PercNom_84CompG[i,j] = np.percentile(tuplanominal[i][3][:,j],84)
        Perc_16CompG[i,j] = np.percentile(factor_ampl[i][3][:,j],16)
        PercNom_16CompG[i,j] = np.percentile(tuplanominal[i][3][:,j],16)
        Perc_50CompG[i,j] = np.percentile(factor_ampl[i][3][:,j],50)
        PercNom_50CompG[i,j] = np.percentile(tuplanominal[i][3][:,j],50)
        
#%%
        


print('---------------------------------------')
print('----------Medianas calculadas----------')
print('---------------------------------------')
print('---------------------------------------')
print('----------Perc. 84% Calculado----------')
print('---------------------------------------')
print('---------------------------------------')
print('----------Perc. 16% Calculado----------')
print('---------------------------------------')
#%% GRAFICOS
# Grafica la mediana de los factores de amplificación
# cmap = sb.cubehelix_palette(n_colors=5,start=2,rot=-0.9,as_cmap=True)

# '#FA8072' -> Naranja
# '#DA70D6' -> Rosado
# '#008080' -> Verde
# '#A52A2A' -> Rojo
# '#4B0082' -> Morado
# '#0343DF' -> Azul
plt.rcParams["figure.figsize"] = (6, 4)
# aceleración normalizada con PGA
nameleg = []
nameleg2 = []
colors = ['#0343DF','#008080','#A52A2A','#0343DF','#008080','#A52A2A']
lineStyle = ['solid','solid','solid','dashdot','dashdot','dashdot']
nameleg = ['1st Floor (300 Models)','2nd Floor (300 Models)','3rd Floor (300 Models)']
nameleg2 = ['1st Floor (Nominal Model)','2nd Floor (Nominal Model)','3rd Floor (Nominal Model)']
for i in range(Npisos):
    plt.plot(TcVar,MedianPGA[:,i],label=nameleg[i],color=colors[i],linestyle=lineStyle[i],linewidth=1.0)
    plt.plot(TcVar,MedianNomPGA[:,i],label=nameleg2[i],color=colors[i+3],linestyle=lineStyle[i+3],linewidth=1.0)
plt.xlabel('Period [s]')
plt.ylabel('Acceleration/PGA')
plt.title('a. Floor amplification factor - Normalized by the PGA',fontweight='bold')
plt.legend(title='Legend',loc='lower center',ncol=2,handletextpad=0.0,handleheight=0.5,bbox_to_anchor=(0.5, -0.47))
plt.xticks(np.arange(0.0, 3.3, step=0.3))
plt.show()
# aceleración normalizada con PFA
for i in range(Npisos):
    plt.plot(TcVar,Median[:,i],label=nameleg[i],color=colors[i],linestyle=lineStyle[i],linewidth=1.0)
    plt.plot(TcVar,MedianNom[:,i],label=nameleg2[i],color=colors[i+3],linestyle=lineStyle[i+3],linewidth=1.0)
plt.xlabel('Period [s]', fontsize = 12.5)
plt.ylabel('PCA/PFA', fontsize = 12.5)
plt.title('',fontweight='bold', fontsize = 14)
plt.legend(title='Legend',loc='lower center',ncol=2,handletextpad=0.0,handleheight=0.5,bbox_to_anchor=(0.5, -0.5))
plt.xticks(np.arange(0.0, 3.3, step=0.3))
plt.show()
# aceleracion sin normalizar
fig, ax = plt.subplots()
for i in range(Npisos):
    plt.plot(TcVar,MedianComp[:,i],label=nameleg[i],color=colors[i],linestyle=lineStyle[i],linewidth=1.0)
    plt.plot(TcVar,MedianNomComp[:,i],label=nameleg2[i],color=colors[i+3],linestyle=lineStyle[i+3],linewidth=1.0)
ax.set_xlabel('Period [s]')
ax.set_ylabel('Acceleration [m/s$^{2}$]')
ax.set_title('c. Component acceleration',fontweight='bold')
legend = ax.legend(title='Legend',loc='lower center',ncol=2,handletextpad=0.0,handleheight=0.5,bbox_to_anchor=(0.5, -0.47))
# legend.get_frame().set_facecolor('white')
# for text in legend.get_texts():
#     text.set_fontsize(8)
ax.set_xticks(np.arange(0.0, 3.3, step=0.3))
plt.show()
# aceleracion sin normalizar en g
fig, ax = plt.subplots()
for i in range(Npisos):
    plt.plot(TcVar,MedianCompG[:,i],label=nameleg[i],color=colors[i],linestyle=lineStyle[i],linewidth=1.0)
    plt.plot(TcVar,MedianNomCompG[:,i],label=nameleg2[i],color=colors[i+3],linestyle=lineStyle[i+3],linewidth=1.0)
ax.set_xlabel('Period [s]', fontsize = 12.5)
ax.set_ylabel('PCA [g]', fontsize = 12.5)
ax.set_title('',fontweight='bold', fontsize = 14)
legend = ax.legend(title='Legend',loc='lower center',ncol=2,handletextpad=0.0,handleheight=0.5,bbox_to_anchor=(0.5, -0.5))
# legend.get_frame().set_facecolor('white')
# for text in legend.get_texts():
#     text.set_fontsize(8)
ax.set_xticks(np.arange(0.0, 3.3, step=0.3))
plt.show()
#%% Maximos
# aceleracion sin normalizar en g

MaxCompG = np.zeros((Nper,Npisos))
MaxNomCompG= np.zeros((Nper,Npisos))
for i in range(Nper):
    for j in range(Npisos):
        MaxCompG[i,j] = np.max(factor_ampl[i][3][:,j])
        MaxNomCompG[i,j] = np.max(tuplanominal[i][3][:,j])

colors = ['orange','green','#A52A2A','#0343DF','#008080','#A52A2A']
lineStyle = ['solid','solid','solid','dashdot','dashdot','dashdot']
nameleg = ['1st Floor','2nd Floor ','3rd Floor']
fig, ax = plt.subplots()
for i in range(Npisos):
    plt.plot(TcVar,np.abs(1-(MaxCompG[:,i]/MaxNomCompG[:,i]))*100,'o-',label=nameleg[i],color=colors[i],markersize=2.0,linewidth=1.0)
ax.set_xlabel('Period [s]', fontsize = 12.5)
ax.set_ylabel('Increment percentage [%]', fontsize = 12.5)
ax.set_title('',fontweight='bold', fontsize = 14)
plt.legend()
ax.set_xticks(np.arange(0.0, 3.3, step=0.3))
plt.show()
#%% Grafica por piso la mediana, p84 y p16 de los factores de amplificación
numero = ['a','b','c']
for i in range(Npisos):
    plt.plot(TcVar,Perc_16[:,i],color='#FA8072',label='P16')
    plt.plot(TcVar,Median[:,i],color='#4B0082',label='P50')
    plt.plot(TcVar,Perc_84[:,i],color='#008080',label='P84')
    plt.plot(TcVar,PercNom_16[:,i],color='#A52A2A',linestyle = 'dashed',label='P16$_{Nominal}$')
    plt.plot(TcVar,MedianNom[:,i],color='#DA70D6',linestyle = 'dashed',label='P50$_{Nominal}$')
    plt.plot(TcVar,PercNom_84[:,i],color='#0343DF',linestyle = 'dashed',label='P84$_{Nominal}$')
    plt.xlabel('Period [s]')
    plt.ylabel('PCA/PFA')
    titulo = numero[i] + '. ' + nameleg[i][0:10]
    plt.title('',fontweight='bold')
    plt.ylim(0.7,6.5,1.0)
    plt.legend()
    plt.show()
#%% OTRA PROPUESTA
numero = ['a','b','c']
for i in range(Npisos):
    plt.plot(TcVar,Perc_16[:,i],color='#FA8072',label='P16')
    plt.plot(TcVar,PercNom_16[:,i],color='#FA8072',linestyle = 'dashed',label='P16$_{Nominal}$')
    plt.plot(TcVar,Median[:,i],color='#4B0082',label='P50')
    plt.plot(TcVar,MedianNom[:,i],color='#4B0082',linestyle = 'dashed',label='P50$_{Nominal}$')
    plt.plot(TcVar,Perc_84[:,i],color='#008080',label='P84')
    plt.plot(TcVar,PercNom_84[:,i],color='#008080',linestyle = 'dashed',label='P84$_{Nominal}$')
    plt.xlabel('Period [s]', fontsize = 12.3)
    plt.ylabel('PCA/PFA', fontsize = 12.3)
    titulo = numero[i] + '. ' + nameleg[i][0:10]
    plt.title('',fontweight='bold', fontsize = 13.5)
    plt.ylim(0.7,6.5,1.0)
    plt.legend()
    plt.show()
#%% GRAFICO DISPERCION
for i in range(Npisos):
    plt.plot(TcVar,Perc_16CompG[:,i],color='#FA8072',label='P-16')
    plt.plot(TcVar,MedianCompG[:,i],color='#4B0082',label='Median')
    plt.plot(TcVar,Perc_84CompG[:,i],color='#008080',label='P-84')
    plt.plot(TcVar,PercNom_16CompG[:,i],color='#FA8072',linestyle = 'dashed',label='P-16$_{Nominal}$')
    plt.plot(TcVar,MedianNomCompG[:,i],color='#4B0082',linestyle = 'dashed',label='Median$_{Nominal}$')
    plt.plot(TcVar,PercNom_84CompG[:,i],color='#008080',linestyle = 'dashed',label='P-84$_{Nominal}$')
    plt.xlabel('Period [s]',fontsize = 12.3)
    plt.ylabel('PCA [g]',fontsize = 12.3)
    titulo = numero[i] + '. ' + nameleg[i][0:10]
    plt.title('',fontweight='bold',fontsize = 13.5)
    plt.ylim(0.1,3.0,1.0)
    plt.legend()
    plt.show()
# #%%
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
# from pylab import*

# aa = [3.2/9.6,6.4/9.6,9.6/9.6]  
# xlist = np.zeros((Nper,Npisos))
# ylist = np.zeros((Nper,Npisos))
# for i in range(Nper):
#     for j in range(Npisos):
#         xlist[i,j] = aa[j] #Altura normalizada
#         ylist[:,j] = TcVar/TOpSees

# plt.rcParams["figure.figsize"] = (8, 6)
# fig = plt.figure()
# axes = fig.add_subplot(projection='3d')
# axes.plot_surface(ylist, xlist, Median,cmap='plasma')
# axes.set_title('a. ISAI',fontweight='bold')
# axes.set_ylabel('F$_{Height}$/T$_{Height}$')
# axes.set_xlabel('T$_{c}$/T$_{F}$')
# axes.set_zlabel('Acceleration/PFA')

# # axes.set_xlim3d(left=0, right=6)
# axes.set_ylim3d(bottom=0.2, top=1) 
# axes.set_zlim3d(bottom=1.0, top=4.5) 

# fig.show()