"""
------------------------ Arquetipo pórticos en CR ------------------------
------------------------- @author: Daniela Novoa -------------------------
"""
#%% ========================= IMPORTAR LIBRERIAS =========================
from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
import analisis as an
import utilidades as ut
import pickle
# fc = 28000
# Fy = 420000
#%% ========================= DEFINIR EL MODELO ==========================
wipe()
diafragma = 1                                                     # Colocar 1 si se desea diafragma en cada piso
pushlimit = 0.05                                                  # limite del pushover
model('basic','-ndm',2,'-ndf',3)                                  # Definir modelo 2D
#%% ======================== PARÁMETROS DE ENTRADA =======================                                                  # Fy del acero
# -----------------------Definir Posición de nodos-------------------------
xloc = [0.0,5.64,11.71,18.32]                                     # Posición nodos en x
yloc = np.insert([0.0,3.0],2,np.linspace(6.1,42.1,13))            # Posición nodos en y
# -----------------------Definir longitud de losa--------------------------
zloc1 = [6.60,6.60,6.60,6.60]                                     # Longitud de la losa sobre el eje +y del plano
zloc2 = [7.85,7.85,7.85,7.85]                                     # Longitud de la losa sobre el eje -y del plano
# -----------------------------Corte en la base----------------------------
CrtBase = [361.23,414.97,388.46,342.69]                           # Cortante en la base
# -------------------------Zona de amenaza sísmica-------------------------
Ciud = "BUC"                                                      # Nombre de la ciudad
PerfTp = "C"                                                      # Perfil de suelo
Group = 1                                                         # Grupo de uso
TEtabs = 1.42                                                     # Periodo fundamental de ETABS
# -------------------------------Tipo de losa------------------------------
Dic_losa = "2D"                                                   # Losa 2D o 1D
# -------------------Carga muerta y viva en los elementos------------------
Dload = 3.0                                                       # kN/m2 Carga muerta losa de entrepiso
Lload = 1.8                                                       # kN/m2 Carga viva losa de entrepiso
LloadTch = 1.8                                                    # kN/m2 Carga viva cubierta
Mload = 0.0                                                       # kN/m Carga muerta muros perimetrales
MloadTch = 0.0                                                    # kN/m Carga muerta muros perimetrales de cubierta
# ---------------------------Nombre del Arquetipo--------------------------
Arquetipo = '04_BUC_14P'
# print('---------------------------------------')
# print('------Modelo Arquetipo '+str(Arquetipo)+'-----')
# print('---------------------------------------')
#%% ============================= CREAR NODOS ============================
Npisos = len(yloc)-1                                              # Número de pisos del edificio
ny = len(yloc)
nx = len(xloc)
# ----------------------Crear nodos de la estructura----------------------|
for i in range(nx):
    for j in range(ny):
        nnode = 1000*(i+1)+j
        node(nnode,xloc[i],yloc[j])
# print('---------------------------------------')
# print('------------Nodos generados------------')
# print('---------------------------------------')
# plt.figure()
# opsv.plot_model()
#%% =================== DEFINIR RESTRICCIONES Y MASAS ====================
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
for i in range(1,ny):
    for j in range(nx):
        nodemass = 1000*(j+1)+i
        mass(nodemass,Masa_list[i-1][j],Masa_list[i-1][j],0.0)
# print('---------------------------------------')
# print('------------Masas asignadas------------')
# print('---------------------------------------')
#%% ====================== ASIGNACIÓN DE DIAFRAGMAS ======================
if diafragma == 1:
    for j in range(1,ny):
        for i in range(1,nx):
            masternode = 1000 + j
            slavenode = 1000*(i+1) + j
            equalDOF(masternode,slavenode,1)
# print('---------------------------------------')
# print('-----------Diafragma asignado----------')
# print('---------------------------------------')
#%% ========================= DEFINIR MATERIALES =========================
xlist = []
for i in range(nx-1):
    xlist.append(np.around(xloc[i+1]-xloc[i],2))
ylist = []
for i in range(ny-1):
    ylist.append(np.around(yloc[i+1]-yloc[i],2))
pint = 5 
Lcol = np.median(ylist)*1000 
Lvig = np.median(xlist)*1000 
# -------------------------Concreto sin confinar-------------------------
# Concreto P1
E = 4700*(fc/1000)**0.5*1000
ec = 2*fc/E 
fcu = 0.2*fc 
Gfc = fc 
e20 = ut.e20Lobatto2(Gfc, Lcol, pint, fc/1000, E/1000, ec)
e20v = ut.e20Lobatto2(Gfc, Lvig, pint, fc/1000, E/1000, ec)
# --------------------------Concreto confinado---------------------------
k = 1.3
fcc = fc*k
ecc = 2*fcc/E
fucc = 0.2*fcc
Gfcc = 2*fcc
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
#%% GRAFICO PARA OBTENER LA CONSTITUTIVA DEL CONCRETO
plt.rcParams["figure.figsize"] = (6, 4)
fig, ax = plt.subplots()
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.plot([e20cc/1000,ecc/1000,0.0,-ecc/1000,-e20cc/1000],[fucc/1000,fcc/1000,0.0,-fcc/1000,-fucc/1000],color='#4A748D',label='Confined')
ax.plot([e20/1000,ec/1000,0.0,-ec/1000,-e20/1000],[fcu/1000,fc/1000,0.0,-fc/1000,-fcu/1000],color='black',label='Unconfined')
ax.set_xlabel('Strain [-]',position=(1, 0), labelpad=108, fontsize=11)
ax.set_ylabel('Stress [MPa]',position=(0, 1), labelpad=148, fontsize=11)
ax.tick_params(axis='both', labelsize=7, colors='black')
ax.legend()
plt.show()
#%% GRAFICO PARA OBTENER LA CONSTITUTIVA DEL ACERO
# Parámetros del material
Fyy = 420.0  # Resistencia a la fluencia en MPa
Ess = 21000.0  # Módulo de elasticidad en MPa
strain_max = 0.05  # Deformación máxima
strain_min = -0.008  # Deformación mínima

# Crear la curva tensión-deformación
strain = np.linspace(strain_min, strain_max, 100)
stress = np.zeros_like(strain)

# Calcular la tensión
for i in range(len(strain)):
    if strain[i] < -Fyy / Ess:
        stress[i] = -Fyy
    elif strain[i] <= Fyy / Ess:
        stress[i] = Ess * strain[i]
    else:
        stress[i] = Fyy

# Crear la figura y los ejes
fig, ax = plt.subplots()
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# Mostrar la curva tensión-deformación
ax.plot(strain, stress,color='k')
ax.plot(-strain, -stress, color='k')

# Ajustar los límites de los ejes
ax.set_xlim(-strain_max, strain_max)
ax.set_ylim(-Fyy - 100, Fyy + 100)

# Etiquetas de los ejes
ax.set_xlabel('Strain [-]',position=(1, 0), labelpad=108, fontsize=11)
ax.set_ylabel('Stress [MPa]',position=(0, 1), labelpad=148, fontsize=11)
ax.tick_params(axis='both', labelsize=7, colors='black')
# Mostrar el gráfico
plt.show()
#%% ========================= DEFINIR SECCIONES ==========================
filename = open('00_Secciones.py', mode='r+',encoding='UTF-8')
code_strfile1 = filename.read()
filename.close()
exec(code_strfile1, locals())                                           # Extraer información de las secciones
# --------------------Sección de las vigas por piso--------------------
secvigas_list = ([secVgA_60x50,secVgB_95x50,secVgC_60x50],
                 [sec2VgA_60x50,sec2VgA_60x50,sec2VgC_60x50],
                 [sec3VgA_60x50,sec3VgA_60x50,sec3VgC_60x50],
                 [sec4VgA_80x50,sec4VgA_80x50,sec4VgC_80x50],
                 [sec4VgA_80x50,sec4VgA_80x50,sec4VgC_80x50],
                 [sec4VgA_80x50,sec4VgA_80x50,sec4VgC_80x50],
                 [sec4VgA_80x50,sec4VgA_80x50,sec4VgC_80x50],
                 [sec4VgA_80x50,sec4VgA_80x50,sec4VgC_80x50],
                 [sec4VgA_80x50,sec4VgA_80x50,sec4VgC_80x50],
                 [sec4VgA_80x50,sec4VgA_80x50,sec4VgC_80x50],
                 [sec4VgA_80x50,sec4VgA_80x50,sec5VgC_80x50],
                 [sec4VgA_80x50,sec4VgA_80x50,sec5VgC_80x50],
                 [sec6VgA_60x50,sec6VgB_95x50,sec6VgC_60x50],
                 [sec7VgA_50x50,sec7VgB_50x50,sec7VgC_50x50])
# -------------------Sección de las columnas por piso------------------

secolumn_list = ([sec1ClA_40x70,sec1ClB_40x100,sec1ClB_40x100,secClD_40x70],
                 [sec1ClA_40x70,sec1ClB_40x100,sec1ClB_40x100,secClD_40x70],
                 [sec1ClA_40x70,sec1ClB_40x100,sec1ClB_40x100,secClD_40x70],
                 [sec1ClA_40x70,sec2ClB_40x80,sec2ClB_40x80,secClD_40x70],
                 [sec1ClA_40x70,sec3ClB_40x70,sec3ClB_40x70,secClD_40x70],
                 [sec1ClA_40x70,sec3ClB_40x70,sec3ClB_40x70,secClD_40x70],
                 [sec2ClA_40x70,sec3ClB_40x70,sec3ClB_40x70,secClD_40x70],
                 [sec2ClA_40x70,sec4ClB_40x70,sec4ClB_40x70,secClD_40x70],
                 [sec2ClA_40x70,sec4ClB_40x70,sec4ClB_40x70,sec2ClA_40x70],
                 [sec2ClA_40x70,sec4ClB_40x70,sec4ClB_40x70,sec2ClA_40x70],
                 [sec2ClA_40x70,sec4ClB_40x70,sec4ClB_40x70,sec2ClA_40x70],
                 [sec2ClA_40x70,sec4ClB_40x70,sec4ClB_40x70,sec2ClA_40x70],
                 [sec2ClA_40x70,sec4ClB_40x70,sec4ClB_40x70,sec2ClA_40x70],
                 [sec2ClA_40x70,sec4ClB_40x70,sec4ClB_40x70,sec2ClA_40x70])

# Las dimensiones de la sección se ingresan por elemento para cada piso. (en metros)
# -------------------Dimensión de las vigas por piso-------------------
dimvigas_list = ([[0.60,0.50],[0.95,0.50],[0.60,0.50]],
                  [[0.60,0.50],[0.60,0.50],[0.60,0.50]],
                  [[0.60,0.50],[0.60,0.50],[0.60,0.50]],
                  [[0.80,0.50],[0.80,0.50],[0.80,0.50]],
                  [[0.80,0.50],[0.80,0.50],[0.80,0.50]],
                  [[0.80,0.50],[0.80,0.50],[0.80,0.50]],
                  [[0.80,0.50],[0.80,0.50],[0.80,0.50]],
                  [[0.80,0.50],[0.80,0.50],[0.80,0.50]],
                  [[0.80,0.50],[0.80,0.50],[0.80,0.50]],
                  [[0.80,0.50],[0.80,0.50],[0.80,0.50]],
                  [[0.80,0.50],[0.80,0.50],[0.80,0.50]],
                  [[0.80,0.50],[0.80,0.50],[0.80,0.50]],
                  [[0.60,0.50],[0.95,0.50],[0.60,0.50]],
                  [[0.50,0.50],[0.50,0.50],[0.50,0.50]])
# ------------------Dimensión de las columnas por piso-----------------
dimcolumn_list = ([[0.40,0.70],[0.40,1.00],[0.40,1.00],[0.40,0.70]],
                  [[0.40,0.70],[0.40,1.00],[0.40,1.00],[0.40,0.70]],
                  [[0.40,0.70],[0.40,1.00],[0.40,1.00],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.80],[0.40,0.80],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.70],[0.40,0.70],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.70],[0.40,0.70],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.70],[0.40,0.70],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.70],[0.40,0.70],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.70],[0.40,0.70],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.70],[0.40,0.70],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.70],[0.40,0.70],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.70],[0.40,0.70],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.70],[0.40,0.70],[0.40,0.70]],
                  [[0.40,0.70],[0.40,0.70],[0.40,0.70],[0.40,0.70]])
#%% ========================== TRANSFORMACIONES ========================== 
lineal = 1
geomTransf('Linear',lineal)
pdelta = 2
geomTransf('PDelta',pdelta)
#%% ========================= GENERAR ELEMENTOS ==========================
#-------------------------------COLUMNAS-------------------------------
TagColumns = []
for i in range(ny-1):
    for j in range(nx):
        nodeI = 1000*(j+1)+i
        nodeJ = 1000*(j+1)+(i+1)
        eltag = 10000*(j+1) + i
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
        eltag = 100000*(j+1) + i
        TagVigas.append(eltag)
        element('forceBeamColumn',eltag,nodeI,nodeJ,lineal,secvigas_list[i-1][j])

remove('ele',200002)
remove('ele',200003)
remove('ele',200004)
remove('ele',200005)
remove('ele',200006)
remove('ele',200007)
remove('ele',200008)
remove('ele',200009)
remove('ele',200010)
remove('ele',200011)
remove('ele',200012)

# print('---------------------------------------')
# print('------------Vigas generadas------------')
# print('---------------------------------------')
# plt.Figure()
# opsv.plot_model(node_labels=0)
# plt.Figure()
# opsv.plot_model(element_labels=0)
# plt.Figure()
# opsv.plot_model(node_labels=0, element_labels=0)
#%% ========================= CARGAS DE GRAVEDAD =========================
timeSeries('Linear', 1)
pattern('Plain',1,1)
# eleLoad('-ele',*TagVigas,'-type','beamUniform',-20)
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

