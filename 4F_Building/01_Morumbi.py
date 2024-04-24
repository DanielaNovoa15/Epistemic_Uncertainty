"""
Created on Thu Mar 23 15:53:49 2023

@author: orlandoaram
"""

from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
import utilidades as ut
wipe()
model('basic','-ndm',2,'-ndf',3)

# fc = 24500
# Fy = 420000

#Creación de nodos
x1 = 4.40
x2 = 10.20
x3 = 15.10


y0 = 3.02 #3.22
y1 = 6.22 #6.40
y2 = 9.42 #9.60
y3 = 12.62 #12.80

#Suelo
node(1,0.0,0.0) #Nodo Suelo
node(2,-4.86,0.0) #Nodo Suelo
node(3,x1,0.0) #Nodo Suelo
node(4,x2,0.0) #Nodo Suelo
node(5,x3,0.0) #Nodo Suelo
#Piso 2
node(6,0.0,y0) 
node(7,-4.86,y0)
node(8,x1,y0)
node(9,x2,y0)
node(10,x3,y0)

#Piso 3
node(11,0.0,y1)
node(12,x1,y1)
node(13,x2,y1)
node(14,x3,y1)

#Piso 4
node(15,0.0,y2)
node(16,x1,y2)
node(17,x2,y2)
node(18,x3,y2)
     
#Azotea
node(19,0.0,y3)
node(20,x1,y3)
node(21,x2,y3)
node(22,x3,y3)


#EMPOTRAMIENTO######
empotrado=[1,1,1]

fix(1,*empotrado)
fix(2,*empotrado)
fix(3,*empotrado)
fix(4,*empotrado)
fix(5,*empotrado)
######


#                 DOF primary secondaries
# ops.rigidDiaphragm(1,    8,    *[2,4,6])

rigidDiaphragm(1, 6, 7, 8, 9, 10) # hace que el desplazamiento de piso1 en X sea igual que el del nodo 7
rigidDiaphragm(1, 11, 12, 13, 14)
rigidDiaphragm(1, 15, 16, 17, 18) 
rigidDiaphragm(1, 19, 20, 21, 22)

#Masas #Definir valor en cada nodo

mass(6,9.64,9.64,0)
mass(7,20.96,20.96,0)
mass(8,9.18,9.18,0)
mass(9,9.42,9.42,0)
mass(10,6.96,6.96,0)
mass(11,9.64,9.64,0)
mass(12,9.18,9.18,0)
mass(13,9.42,9.42,0)
mass(14,6.96,6.96,0)
mass(15,9.64,9.64,0)
mass(16,9.18,9.18,0)
mass(17,9.42,9.42,0)
mass(18,6.96,6.96,0)
mass(19,9.64,9.64,0)
mass(20,9.18,9.18,0)
mass(21,9.42,9.42,0)
mass(22,6.96,6.96,0)

#Definición de los materiales

# -------------------------Vigas-------------------------
pint = 5  
Lcol = 4.80*1000
# -------------------------Concreto sin confinar-------------------------
# Concreto P1
# fc = 24500 #kPa
E = 4700*(fc/1000)**0.5*1000
ec = 2*fc/E 
fcu = 0.2*fc 
Gfc = fc/1000 #Definir como MPa 
e20 = ut.e20Lobatto2(Gfc, Lcol, pint, fc/1000, E/1000, ec)
# --------------------------Concreto confinado---------------------------
k = 1.3
fcc = fc*k
ecc = 2*fcc/E
fucc = 0.2*fcc
Gfcc = 2*fcc/1000 #Defini en MPa
e20cc = ut.e20Lobatto2(Gfcc, Lcol, pint, fcc/1000, E/1000, ecc)
# ---------------------------------Acero---------------------------------
Es = 210000000.0
# Fy = 420000
# Confinado
uniaxialMaterial('Concrete01', 1, -fcc, -ecc, -fucc, -e20cc)
# Sin confinar
uniaxialMaterial('Concrete01', 2, -fc, -ec, -fcu, -e20)
# Acero
uniaxialMaterial('Steel01', 4, Fy, Es, 0.01)
uniaxialMaterial('MinMax', 3, 4, '-min', -0.008, '-max', 0.05)


#Para Columnas Regularización #Nuevo Material para columnas

# -------------------------Columnas-------------------------
pint = 5  
Lcol = 3.20*1000
# -------------------------Concreto sin confinar-------------------------
# Concreto P1
# fc = 24500 #kPa
E = 4700*(fc/1000)**0.5*1000
ec = 2*fc/E 
fcu = 0.2*fc 
Gfc = fc/1000 #Definir como MPa 
e20 = ut.e20Lobatto2(Gfc, Lcol, pint, fc/1000, E/1000, ec)
# --------------------------Concreto confinado---------------------------
k = 1.3
fcc = fc*k
ecc = 2*fcc/E
fucc = 0.2*fcc
Gfcc = 2*fcc/1000 #Defini en MPa
e20cc = ut.e20Lobatto2(Gfcc, Lcol, pint, fcc/1000, E/1000, ecc)
# ---------------------------------Acero---------------------------------
Es = 210000000.0
# Fy = 420000
# Confinado
uniaxialMaterial('Concrete01', 5, -fcc, -ecc, -fucc, -e20cc)
# Sin confinar
uniaxialMaterial('Concrete01', 6, -fc, -ec, -fcu, -e20)

#%% GRAFICO PARA OBTENER LA CONSTITUTIVA DEL CONCRETO
# plt.rcParams["figure.figsize"] = (6, 4)
# fig, ax = plt.subplots()
# ax.spines['left'].set_position('center')
# ax.spines['bottom'].set_position('center')
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# ax.xaxis.set_ticks_position('bottom')
# ax.yaxis.set_ticks_position('left')
# ax.plot([e20cc/1000,ecc/1000,0.0,-ecc/1000,-e20cc/1000],[fucc/1000,fcc/1000,0.0,-fcc/1000,-fucc/1000],color='#4A748D',label='Confined')
# ax.plot([e20/1000,ec/1000,0.0,-ec/1000,-e20/1000],[fcu/1000,fc/1000,0.0,-fc/1000,-fcu/1000],color='black',label='Unconfined')
# ax.set_xlabel('Strain [-]',position=(1, 0), labelpad=108, fontsize=11)
# ax.set_ylabel('Stress [MPa]',position=(0, 1), labelpad=148, fontsize=11)
# ax.tick_params(axis='both', labelsize=7, colors='black')
# ax.legend()
# plt.show()
#%% GRAFICO PARA OBTENER LA CONSTITUTIVA DEL ACERO
# # Parámetros del material
# Fyy = 420.0  # Resistencia a la fluencia en MPa
# Ess = 21000.0  # Módulo de elasticidad en MPa
# strain_max = 0.05  # Deformación máxima
# strain_min = -0.008  # Deformación mínima

# # Crear la curva tensión-deformación
# strain = np.linspace(strain_min, strain_max, 100)
# stress = np.zeros_like(strain)

# # Calcular la tensión
# for i in range(len(strain)):
#     if strain[i] < -Fyy / Ess:
#         stress[i] = -Fyy
#     elif strain[i] <= Fyy / Ess:
#         stress[i] = Ess * strain[i]
#     else:
#         stress[i] = Fyy

# # Crear la figura y los ejes
# fig, ax = plt.subplots()
# ax.spines['left'].set_position('center')
# ax.spines['bottom'].set_position('center')
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# # Mostrar la curva tensión-deformación
# ax.plot(strain, stress,color='k')
# ax.plot(-strain, -stress, color='k')

# # Ajustar los límites de los ejes
# ax.set_xlim(-strain_max, strain_max)
# ax.set_ylim(-Fyy - 100, Fyy + 100)

# # Etiquetas de los ejes
# ax.set_xlabel('Strain [-]',position=(1, 0), labelpad=108, fontsize=11)
# ax.set_ylabel('Stress [MPa]',position=(0, 1), labelpad=148, fontsize=11)
# ax.tick_params(axis='both', labelsize=7, colors='black')
# # Mostrar el gráfico
# plt.show()

#%%

#Area Barra Refuerzo 

As4 = 0.000129
As5 = 0.000199
As6 = 0.000284
As7 = 0.000387


#Secciones 


#Columnas 30x30
bc1= 0.30
hc1= 0.30
Ac1= bc1*hc1
Izc1= (bc1*hc1**3)/12

#Columnas 40x40
bc2= 0.40
hc2= 0.40
Ac2= bc2*hc2
Izc2= (bc2*hc2**3)/12

#Vigas 30x35
bv1= 0.30
hv1= 0.35
Av1= bv1*hv1
Izv1= (bv1*hv1**3)/12


#Seccion Fibra (Vigas)
rec = 0.04
y1vi = hv1/2
z1vi = bv1/2

y2vi = 0.5*(hv1-2*rec)/3
z2vi = 0.5*(bv1-2*rec)/3

nFibZ = 1
nFibZCore = 10
nFib = 20
nFibCover = 3
nFibCore = 16

# 4#5 - 2#5

VP2B = 1

fib_sec_1 = [['section', 'Fiber',VP2B, '-GJ', 1.0e6],
              ['patch','rect', 1, nFibCore, nFibZCore, rec-y1vi, rec-z1vi, y1vi-rec, z1vi-rec],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, -z1vi, y1vi, rec-z1vi],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, z1vi-rec, y1vi, z1vi ],
              ['patch','rect', 2, nFibCover, nFibZ, -y1vi, rec-z1vi, rec-y1vi, z1vi-rec],
              ['patch','rect', 2, nFibCover, nFibZ, y1vi-rec, rec-z1vi, y1vi, z1vi-rec],
              ['layer','straight', 3, 4, As5, y1vi-rec, z1vi-rec, y1vi-rec, rec-z1vi],
              ['layer','straight', 3, 2, As5, rec-y1vi, z1vi-rec, rec-y1vi, rec-z1vi]]


# matcolor = ['#53A53D', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(fib_sec_1, matcolor=matcolor)
# plt.axis('equal')
opsv.fib_sec_list_to_cmds(fib_sec_1)
beamIntegration('Lobatto',VP2B,VP2B,5)

# 2#6+2#5 - 2#5

VP2CD = 2

fib_sec_2 = [['section', 'Fiber',VP2CD, '-GJ', 1.0e6],
              ['patch','rect', 1, nFibCore, nFibZCore, rec-y1vi, rec-z1vi, y1vi-rec, z1vi-rec],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, -z1vi, y1vi, rec-z1vi],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, z1vi-rec, y1vi, z1vi ],
              ['patch','rect', 2, nFibCover, nFibZ, -y1vi, rec-z1vi, rec-y1vi, z1vi-rec],
              ['patch','rect', 2, nFibCover, nFibZ, y1vi-rec, rec-z1vi, y1vi, z1vi-rec],
              ['layer','straight', 3, 2, As6, y1vi-rec, z1vi-rec, y1vi-rec, rec-z1vi],
              ['layer','straight', 3, 2, As5, y1vi-rec, z2vi, y1vi-rec, -z2vi],
              ['layer','straight', 3, 2, As5, rec-y1vi, z1vi-rec, rec-y1vi, rec-z1vi]]


# matcolor = ['#BE4E7E', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(fib_sec_2, matcolor=matcolor)
# plt.axis('equal')
opsv.fib_sec_list_to_cmds(fib_sec_2)
beamIntegration('Lobatto',VP2CD,VP2CD,5)

# 4#5 - 2#5

VP2E = 3

fib_sec_3 = [['section', 'Fiber',VP2E, '-GJ', 1.0e6],
              ['patch','rect', 1, nFibCore, nFibZCore, rec-y1vi, rec-z1vi, y1vi-rec, z1vi-rec],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, -z1vi, y1vi, rec-z1vi],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, z1vi-rec, y1vi, z1vi ],
              ['patch','rect', 2, nFibCover, nFibZ, -y1vi, rec-z1vi, rec-y1vi, z1vi-rec],
              ['patch','rect', 2, nFibCover, nFibZ, y1vi-rec, rec-z1vi, y1vi, z1vi-rec],
              ['layer','straight', 3, 2, As5, y1vi-rec, z1vi-rec, y1vi-rec, rec-z1vi],
              ['layer','straight', 3, 2, As5, y1vi-rec, z2vi, y1vi-rec, -z2vi],
              ['layer','straight', 3, 2, As5, rec-y1vi, z1vi-rec, rec-y1vi, rec-z1vi]]


# matcolor = ['lightgray', 'gold', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(fib_sec_3, matcolor=matcolor)
# plt.axis('equal')
opsv.fib_sec_list_to_cmds(fib_sec_3)
beamIntegration('Lobatto',VP2E,VP2E,5)

# 2#6+2#5 - 3#5

VP3BD= 4

fib_sec_4 = [['section', 'Fiber',VP3BD, '-GJ', 1.0e6],
              ['patch','rect', 1, nFibCore, nFibZCore, rec-y1vi, rec-z1vi, y1vi-rec, z1vi-rec],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, -z1vi, y1vi, rec-z1vi],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, z1vi-rec, y1vi, z1vi ],
              ['patch','rect', 2, nFibCover, nFibZ, -y1vi, rec-z1vi, rec-y1vi, z1vi-rec],
              ['patch','rect', 2, nFibCover, nFibZ, y1vi-rec, rec-z1vi, y1vi, z1vi-rec],
              ['layer','straight', 3, 2, As6, y1vi-rec, z1vi-rec, y1vi-rec, rec-z1vi],
              ['layer','straight', 3, 2, As5, y1vi-rec, z2vi, y1vi-rec, -z2vi],
              ['layer', 'straight', 3, 1, As5, rec-y1vi, 0, 0,0],
              ['layer','straight', 3, 2, As5, rec-y1vi, z1vi-rec, rec-y1vi, rec-z1vi]]


# matcolor = ['#4188A1', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(fib_sec_4, matcolor=matcolor)
# plt.axis('equal')
opsv.fib_sec_list_to_cmds(fib_sec_4)
beamIntegration('Lobatto',VP3BD,VP3BD,5)

# 2#7+2#5 - 3#5

VP3C= 5

fib_sec_5 = [['section', 'Fiber',VP3C, '-GJ', 1.0e6],
              ['patch','rect', 1, nFibCore, nFibZCore, rec-y1vi, rec-z1vi, y1vi-rec, z1vi-rec],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, -z1vi, y1vi, rec-z1vi],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, z1vi-rec, y1vi, z1vi ],
              ['patch','rect', 2, nFibCover, nFibZ, -y1vi, rec-z1vi, rec-y1vi, z1vi-rec],
              ['patch','rect', 2, nFibCover, nFibZ, y1vi-rec, rec-z1vi, y1vi, z1vi-rec],
              ['layer','straight', 3, 2, As7, y1vi-rec, z1vi-rec, y1vi-rec, rec-z1vi],
              ['layer','straight', 3, 2, As5, y1vi-rec, z2vi, y1vi-rec, -z2vi],
              ['layer', 'straight', 3, 1, As5, rec-y1vi, 0, 0,0],
              ['layer','straight', 3, 2, As5, rec-y1vi, z1vi-rec, rec-y1vi, rec-z1vi]]


# matcolor = ['#D1C125', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(fib_sec_5, matcolor=matcolor)
# plt.axis('equal')
opsv.fib_sec_list_to_cmds(fib_sec_5)
beamIntegration('Lobatto',VP3C,VP3C,5)

# 4#5 - 3#5

VP3E= 6

fib_sec_6 = [['section', 'Fiber',VP3E, '-GJ', 1.0e6],
              ['patch','rect', 1, nFibCore, nFibZCore, rec-y1vi, rec-z1vi, y1vi-rec, z1vi-rec],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, -z1vi, y1vi, rec-z1vi],
              ['patch','rect', 2, nFib, nFibZ, -y1vi, z1vi-rec, y1vi, z1vi ],
              ['patch','rect', 2, nFibCover, nFibZ, -y1vi, rec-z1vi, rec-y1vi, z1vi-rec],
              ['patch','rect', 2, nFibCover, nFibZ, y1vi-rec, rec-z1vi, y1vi, z1vi-rec],
              ['layer','straight', 3, 2, As5, y1vi-rec, z1vi-rec, y1vi-rec, rec-z1vi],
              ['layer','straight', 3, 2, As5, y1vi-rec, z2vi, y1vi-rec, -z2vi],
              ['layer', 'straight', 3, 1, As5, rec-y1vi, 0, 0,0],
              ['layer','straight', 3, 2, As5, rec-y1vi, z1vi-rec, rec-y1vi, rec-z1vi]]


# matcolor = ['lightgray', 'gold', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(fib_sec_6, matcolor=matcolor)
# plt.axis('equal')
opsv.fib_sec_list_to_cmds(fib_sec_6)
beamIntegration('Lobatto',VP3E,VP3E,5)

#Seccion Fibra (Columna) C1 30x30

# 8#5

rec = 0.04
y1c1 = hc1/2
z1c1 = bc1/2

y2c1 = 0.5*(hv1-2*rec)/3

nFibZ = 1
nFibZCore = 8
nFib = 20
nFibCover = 3
nFibCore = 16


C1 = 7 #7

fib_sec_7 = [['section', 'Fiber',C1, '-GJ', 1.0e6],
             ['patch','rect', 5, nFibCore, nFibCore, rec-y1c1, rec-z1c1, y1c1-rec, z1c1-rec],
             ['patch','rect', 6, nFib, nFibZ, -y1c1, -z1c1, y1c1, rec-z1c1],
             ['patch','rect', 6, nFib, nFibZ, -y1c1, z1c1-rec, y1c1, z1c1 ],
             ['patch','rect', 6, nFibCover, nFibZ, -y1c1, rec-z1c1, rec-y1c1, z1c1-rec],
             ['patch','rect', 6, nFibCover, nFibZ, y1c1-rec, rec-z1c1, y1c1, z1c1-rec],
             ['layer','straight', 3, 4, As5, y1c1-rec, z1c1-rec, y1c1-rec, rec-z1c1],
             ['layer','straight', 3, 2, As5, y2c1, z1c1-rec, y2c1, rec-z1c1],
             ['layer', 'straight', 3, 2, As5, -y2c1, z1c1-rec, -y2c1, rec-z1c1],
             ['layer','straight', 3, 4, As5, rec-y1c1, z1c1-rec, rec-y1c1, rec-z1c1]]

# matcolor = ['#C64C46', 'lightgray', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(fib_sec_7, matcolor=matcolor)
# plt.axis('equal')

#Seccion Fibra (Columna) C2 40x40

# 12#5

rec = 0.04
y1c2 = hc2/2
z1c2 = bc2/2

y2c2 = 0.5*(hc2-2*rec)/3

nFibZ = 1
nFibZCore = 8
nFib = 20
nFibCover = 3
nFibCore = 16
C2 = 8

fib_sec_8 = [['section', 'Fiber',C2, '-GJ', 1.0e6],
             ['patch','rect', 5, nFibCore, nFibCore, rec-y1c2, rec-z1c2, y1c2-rec, z1c2-rec],
             ['patch','rect', 6, nFib, nFibZ, -y1c2, -z1c2, y1c2, rec-z1c2],
             ['patch','rect', 6, nFib, nFibZ, -y1c2, z1c2-rec, y1c2, z1c2 ],
             ['patch','rect', 6, nFibCover, nFibZ, -y1c2, rec-z1c2, rec-y1c2, z1c2-rec],
             ['patch','rect', 6, nFibCover, nFibZ, y1c2-rec, rec-z1c2, y1c2, z1c2-rec],
             ['layer','straight', 3, 2, As5, y2c2, z1c2-rec, y2c2, rec-z1c2],
             ['layer','straight', 3, 2, As5, -y2c2, rec-z1c2, -y2c2, z1c2-rec],
             ['layer', 'straight', 3, 4, As5, y1c2-rec, rec-z1c2, y1c2-rec, z1c2-rec],
             ['layer','straight', 3, 4, As5, rec-y1c2, z1c2-rec, rec-y1c2, rec-z1c2]]

# matcolor =  ['#6B93B2', 'lightgray', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(fib_sec_8, matcolor=matcolor)
# plt.axis('equal')

opsv.fib_sec_list_to_cmds(fib_sec_7)
beamIntegration('Lobatto',C1,C1,5)
opsv.fib_sec_list_to_cmds(fib_sec_8)
beamIntegration('Lobatto',C2,C2,5)



# Transformación lineal
Lin = 1
geomTransf('Linear',Lin)

PDz = 2
geomTransf('PDelta',PDz)

   
#Vigas
#ForceBeamColumn

element('forceBeamColumn',1,7,6,Lin,VP2B)
element('forceBeamColumn',2,6,8,Lin,VP2B)
element('forceBeamColumn',3,8,9,Lin,VP2CD)
element('forceBeamColumn',4,9,10,Lin,VP2CD)
element('forceBeamColumn',5,11,12,Lin,VP3BD)
element('forceBeamColumn',6,12,13,Lin,VP3C)
element('forceBeamColumn',7,13,14,Lin,VP3BD)
element('forceBeamColumn',8,15,16,Lin,VP3BD)    
element('forceBeamColumn',9,16,17,Lin,VP3C)
element('forceBeamColumn',10,17,18,Lin,VP3BD)
element('forceBeamColumn',11,19,20,Lin,VP3BD)
element('forceBeamColumn',12,20,21,Lin,VP3C)
element('forceBeamColumn',13,21,22,Lin,VP3BD)


#Columnas

element('forceBeamColumn',14,2,7,PDz,C1)
element('forceBeamColumn',15,1,6,PDz,C2)
element('forceBeamColumn',16,6,11,PDz,C2)
element('forceBeamColumn',17,11,15,PDz,C2)
element('forceBeamColumn',18,15,19,PDz,C2)
element('forceBeamColumn',19,3,8,PDz,C2)
element('forceBeamColumn',20,8,12,PDz,C2)
element('forceBeamColumn',21,12,16,PDz,C2)
element('forceBeamColumn',22,16,20,PDz,C2)
element('forceBeamColumn',23,4,9,PDz,C2)
element('forceBeamColumn',24,9,13,PDz,C2)
element('forceBeamColumn',25,13,17,PDz,C2)
element('forceBeamColumn',26,17,21,PDz,C2)
element('forceBeamColumn',27,5,10,PDz,C2)
element('forceBeamColumn',35,10,14,PDz,C2)
element('forceBeamColumn',36,14,18,PDz,C2)
element('forceBeamColumn',37,18,22,PDz,C2)

# plt.Figure()
# opsv.plot_model(node_labels=0)
# plt.Figure()
# opsv.plot_model(element_labels=0)
# plt.Figure()
# opsv.plot_model(node_labels=0, element_labels=0)


# plt.Figure()
# opsv.plot_model()

# Analisis Modal

# num_modos = 6
# OmegaSq = eigen(num_modos)
# OmegaSq = np.array(OmegaSq)
# Omega = OmegaSq**0.5 #Frecuencia Angular
# T = 2*3.1416/Omega #Periodos

# for i in range(num_modos):
#     print('Modo ', i+1, 'T = ', T[i], 's')    
    
    
# Cargas #Definir Valor Cargas Gravitacionales
# Cargas Gravitaionales

timeSeries('Constant', 1) #Constant Pushover #Linear TH
pattern('Plain', 1, 1)

eleLoad('-ele', 1,'-type','-beamUniform',-18.79) 
eleLoad('-ele', 2,'-type','-beamUniform',-19.02) 
eleLoad('-ele', 3,'-type','-beamUniform',-18.01) 
eleLoad('-ele', 4,'-type','-beamUniform',-9.53) 
eleLoad('-ele', 5,'-type','-beamUniform',-19.02) 
eleLoad('-ele', 6,'-type','-beamUniform',-18.01) 
eleLoad('-ele', 7,'-type','-beamUniform',-9.53) 
eleLoad('-ele', 8,'-type','-beamUniform',-19.02) 
eleLoad('-ele', 9,'-type','-beamUniform',-18.01) 
eleLoad('-ele', 10,'-type','-beamUniform',-9.53) 
eleLoad('-ele', 11,'-type','-beamUniform',-19.02) 
eleLoad('-ele', 12,'-type','-beamUniform',-18.01)
eleLoad('-ele', 13,'-type','-beamUniform',-9.53) 