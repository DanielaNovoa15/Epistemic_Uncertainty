"""
------------------------ Arquetipo pórticos en CR ------------------------
------------------------- @author: Daniela Novoa -------------------------
"""
#%% DEFINIR EL MODELO
from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
import analisis as an
import utilidades as ut
import pickle
#%%
wipe()
diafragma = 1                                                     # Colocar 1 si se desea diafragma en cada piso
pushlimit = 0.05                                                  # limite del pushover
model('basic','-ndm',2,'-ndf',3)                                  # Definir modelo 2D
fc = 21000
Fy = 420000
#%% PARÁMETROS DE ENTRADA
# -----------------------Definir Posición de nodos-------------------------
xloc = [0.0,2.9,6.35,9.8,12.7]                                    # Posición nodos en x
yloc = [0.0,3.2,6.4,9.6]                                          # Posición nodos en y
# -----------------------Definir longitud de losa--------------------------
zloc1 = [4.90,4.90,4.90,4.90]                                     # Longitud de la losa sobre el eje +y del plano
zloc2 = [4.88,4.88,4.88,4.88]                                     # Longitud de la losa sobre el eje -y del plano
# -----------------------------Corte en la base----------------------------
CrtBase = [91.5253,113.6772,110.464,113.6772,91.5253]             # Cortante en la base
# -------------------------Zona de amenaza sísmica-------------------------
Ciud = "CRT"                                                      # Nombre de la ciudad
PerfTp = "D"                                                      # Perfil de suelo
Group = 1                                                         # Grupo de uso
TEtabs = 0.59                                                     # Periodo fundamental de ETABS
# -------------------------------Tipo de losa------------------------------
Dic_losa = "2D"                                                   # Losa 2D o 1D
# -------------------Carga muerta y viva en los elementos------------------
Dload = 3.0                                                       # kN/m2 Carga muerta losa de entrepiso
Lload = 1.7652                                                    # kN/m2 Carga viva losa de entrepiso
LloadTch = 0.49033                                                # kN/m2 Carga viva cubierta
Mload = 2.942                                                     # kN/m Carga muerta muros perimetrales
MloadTch = 1.471                                                  # kN/m Carga muerta muros perimetrales de cubierta
# ---------------------------Nombre del Arquetipo--------------------------
Arquetipo = '0001-CRT-3P'
# print('---------------------------------------')
# print('------Modelo Arquetipo '+str(Arquetipo)+'-----')
# print('---------------------------------------')
#%% CREAR NODOS
Npisos = len(yloc)-1                                              # Número de pisos del edificio
ny = len(yloc)
nx = len(xloc)
# ----------------------Crear nodos de la estructura----------------------
for i in range(nx):
    for j in range(ny):
        nnode = 1000*(i+1)+j
        node(nnode,xloc[i],yloc[j])
# print('---------------------------------------')
# print('------------Nodos generados------------')
# print('---------------------------------------')
plt.Figure()
opsv.plot_model()
#%% DEFINIR RESTRICCIONES Y MASAS
# ------------------------Tipo de apoyo en la base------------------------
empotrado = [1,1,1]
fixY(0.0,*empotrado)                                              # Todos los nodos en y=0 empotrados
# ----------------------------Calculo de masas----------------------------
exec(open('00_Espectro.py').read())                               # Calcula el espectro de aceleraciones 
Sa = dataSa.query('Tval == @TEtabs')['Sa'].to_numpy()[0]          # Valor de Sa [g]
Masa_list = np.zeros((Npisos,len(CrtBase)))
for piso in range(Npisos):
    for indx,crt in enumerate(CrtBase):
        Masa_list[piso,indx] = ((crt/Sa)/9.81)/Npisos
Wedificio = np.sum(CrtBase)/Sa                                    # Peso del edificio
# ---------------------Asigación de masas a los nodos--------------------
for masa in Masa_list:
    for indx,val in enumerate(masa):
        for j in range(1,ny):
            nnodemass = 1000*(indx+1)+j
            mass(nnodemass,val,val,0.0)                          

# print('---------------------------------------')
# print('------------Masas asignadas------------')
# print('---------------------------------------')
#%% ASIGNACIÓN DE DIAFRAGMAS
if diafragma == 1:
    for j in range(1,ny):
        for i in range(1,nx):
            masternode = 1000 + j
            slavenode = 1000*(i+1) + j
            equalDOF(masternode,slavenode,1)
# print('---------------------------------------')
# print('-----------Diafragma asignado----------')
# print('---------------------------------------')
#%% DEFINIR MATERIALES

xlist = []
for i in range(nx-1):
    xlist.append(xloc[i+1]-xloc[i])
ylist = []
for i in range(ny-1):
    ylist.append(yloc[i+1]-yloc[i])
    
pint = 5  
Lcol = np.median(ylist)*1000
Lvig = np.median(xlist)*1000
# -------------------------Concreto sin confinar-------------------------
# Concreto P1
E = 4700*(fc/1000)**0.5*1000
ec = 2*fc/E 
fcu = 0.2*fc 
Gfc = fc/1000 
e20 = ut.e20Lobatto2(Gfc, Lcol, pint, fc/1000, E/1000, ec)
e20v = ut.e20Lobatto2(Gfc, Lvig, pint, fc/1000, E/1000, ec)
# --------------------------Concreto confinado---------------------------
k = 1.3
fcc = fc*k
ecc = 2*fcc/E
fucc = 0.2*fcc
Gfcc = 2*fcc/1000
e20cc = ut.e20Lobatto2(Gfcc, Lcol, pint, fcc/1000, E/1000, ecc)
e20ccv = ut.e20Lobatto2(Gfcc, Lvig, pint, fcc/1000, E/1000, ecc)
# ---------------------------------Acero---------------------------------
Es = 210000000.0
# Tags
Col_Conf = 1
Vig_Conf = 2
Col_Unconf = 3
Vig_Unconf = 4
Steel = 5
# Confinado
uniaxialMaterial('Concrete01', Col_Conf, -fcc, -ecc, -fucc, -e20cc)
uniaxialMaterial('Concrete01', Vig_Conf, -fcc, -ecc, -fucc, -e20ccv)
# Sin confinar
uniaxialMaterial('Concrete01', Col_Unconf, -fc, -ec, -fcu, -e20)
uniaxialMaterial('Concrete01', Vig_Unconf, -fc, -ec, -fcu, -e20v)
# Acero
uniaxialMaterial('Steel01', 6, Fy, Es, 0.01)
uniaxialMaterial('MinMax', Steel, 6, '-min', -0.008, '-max', 0.05)
#%% DEFINIR SECCIONES
exec(open('00_Secciones.py').read())                               # Extraer información de las secciones
# --------------------Sección de las vigas por piso--------------------
secvigas_list = ([sec30x35,sec30x35,sec30x35,sec30x35],
                 [sec30x35,sec30x35,sec30x35,sec30x35],
                 [sec30x35,sec30x35,sec30x35,sec30x35])
# -------------------Sección de las columnas por piso------------------
secolumn_list = ([sec35x35,sec35x35,secC_35x35,sec35x35,sec35x35],
                 [sec35x35,sec35x35,secC_35x35,sec35x35,sec35x35],
                 [sec35x35,sec35x35,secC_35x35,sec35x35,sec35x35])
# Las dimensiones de la sección se ingresan por elemento para cada piso. (en metros)
# -------------------Dimensión de las vigas por piso-------------------
dimvigas_list = ([[0.30,0.35],[0.30,0.35],[0.30,0.35],[0.30,0.35]],
                 [[0.30,0.35],[0.30,0.35],[0.30,0.35],[0.30,0.35]],
                 [[0.30,0.35],[0.30,0.35],[0.30,0.35],[0.30,0.35]])
# ------------------Dimensión de las columnas por piso-----------------
dimcolumn_list = ([[0.35,0.35],[0.35,0.35],[0.35,0.35],[0.35,0.35],[0.35,0.35]],
                  [[0.35,0.35],[0.35,0.35],[0.35,0.35],[0.35,0.35],[0.35,0.35]],
                  [[0.35,0.35],[0.35,0.35],[0.35,0.35],[0.35,0.35],[0.35,0.35]])
#%% TRANSFORMACIONES 
lineal = 1
geomTransf('Linear',lineal)
pdelta = 2
geomTransf('PDelta',pdelta)
#%% GENERAR ELEMENTOS
#-------------------------------COLUMNAS-------------------------------
TagColumns = []
for i in range(ny-1):
    for j in range(nx):
        nodeI = 1000*(j+1)+i
        nodeJ = 1000*(j+1)+(i+1)
        eltag = 10*(j+1) + i
        TagColumns.append(eltag)
        element('forceBeamColumn',eltag,nodeI,nodeJ,pdelta,secolumn_list[i][j])
# print('---------------------------------------')
# print('-----------Columnas generadas----------')
# print('---------------------------------------')
#--------------------------------VIGAS--------------------------------
TagVigas = []
for i in range(1,ny):
    for j in range(nx-1):
        nodeI = 1000*(j+1)+i
        nodeJ = 1000*(j+2)+i
        eltag = 100*(j+1) + i
        TagVigas.append(eltag)
        element('forceBeamColumn',eltag,nodeI,nodeJ,lineal,secvigas_list[i-1][j])
# print('---------------------------------------')
# print('------------Vigas generadas------------')
# print('---------------------------------------')
#%% =========================== GENERAR FIGURAS ==========================
plt.Figure()
opsv.plot_model()
plt.Figure()
opsv.plot_model(node_labels=0)
plt.Figure()
opsv.plot_model(element_labels=0)
plt.Figure()
opsv.plot_model(node_labels=0, element_labels=0)
#%% CARGAS DE GRAVEDAD
timeSeries('Linear', 1)
pattern('Plain',1,1)
# -------------------------- COLUMNAS --------------------------
# Se calcula la carga axial sobre la columna
wCol_list = []
for i in range(len(dimcolumn_list)):
    for j in range(len(dimcolumn_list[i])):
        wCol_list.append(np.product(dimcolumn_list[i][j])*24*(yloc[i+1]-yloc[i]))
# Ciclo que guarda los nodos a los que se le va a aplicar la carga axial
ColumnNode = []
for i in range(nx):
    for j in range(1,ny):
        nodeCol = 1000*(i+1) + j
        ColumnNode.append(nodeCol)
# Aplicar carga axial al nodo
NCol = len(ColumnNode) 
for k in range(NCol):
    nnodo = ColumnNode[k]
    load(nnodo,0.0,-wCol_list[k],0.0)
# --------------------------- VIGAS ----------------------------
# Calcular areas aferentes
Aaf_list = []
for i in range(len(xlist)):
    if  Dic_losa == "2D":
        if zloc1[i]/2 > xlist[i]/2 and zloc2[i]/2 > xlist[i]/2:
            afer = (xlist[i]**2)/2
        elif zloc1[i]/2 < xlist[i]/2 and zloc2[i]/2 < xlist[i]/2:
            afer = (zloc1[i]/2)*(2*xlist[i]-zloc1[i])/2+(zloc2[i]/2)*(2*xlist[i]-zloc2[i])/2
        elif zloc1[i]/2 < xlist[i]/2 and zloc2[i]/2 > xlist[i]/2:
            afer = (zloc1[i]/2)*(2*xlist[i]-zloc1[i])/2+(xlist[i]**2)/4
        elif zloc1[i]/2 > xlist[i]/2 and zloc2[i]/2 < xlist[i]/2:
            afer = (zloc2[i]/2)*(2*xlist[i]-zloc2[i])/2+(xlist[i]**2)/4
    else:
        afer = xlist[i]*zloc1[i]/2+xlist[i]*zloc2[i]/2
    Aaf_list.append(afer)
# Calcular el peso de la viga
for i in range(len(dimvigas_list)):
    wViga_list = np.zeros((Npisos,len(dimvigas_list[i])))
    for j in range(len(dimvigas_list[i])):
        wViga_list[:,j] = (np.product(dimvigas_list[i][j])*24)
# Carga distribuida sobre la viga
wvigp_list = []
for i in range(Npisos-1):
    # wvigp_list = np.zeros((Npisos-1,len(dimvigas_list[i])))
    for j in range(len(xlist)):
        wvigp_list.append(Mload+1.05*(Dload*Aaf_list[j])/xlist[j]+0.25*(Lload*Aaf_list[j])/xlist[j]+wViga_list[i][j])
# Carga distribuida sobre la cubierta
wTecho_list = []
for j in range(len(xlist)):
    wTecho_list.append(MloadTch+1.05*(Dload*Aaf_list[j])/xlist[j]+0.25*(LloadTch*Aaf_list[j])/xlist[j]+wViga_list[-1][j])
# Aplicar carga adistribuida al elemento vigas perimetrales

for i in range((Npisos-1)*len(xlist)):
    tagviga = TagVigas[i]
    eleLoad('-ele',tagviga,'-type','beamUniform',-wvigp_list[i])
# Aplicar carga adistribuida al elemento cubierta
for i,val in enumerate(TagVigas[(Npisos-1)*len(xlist):(Npisos)*len(xlist)]):
    tagviga = val
    eleLoad('-ele',tagviga,'-type','beamUniform',-wTecho_list[i])
# print('---------------------------------------')
# print('-----Cargas de gravedad aplicadas------')
# print('---------------------------------------')