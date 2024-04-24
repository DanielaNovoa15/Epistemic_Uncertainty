"""
------------------------- Secciones del Arquetipo ------------------------
------------------------- @author: Daniela Novoa -------------------------
"""
from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
import analisis as an
import utilidades as ut
import pickle
#%% A TENER EN CUENTA
# Col_Conf = 1 Columna confinada
# Vig_Conf = 2 Viga confinada
# Col_Unconf = 3 Columna no confinada
# Vig_Unconf = 4 Viga no confinada
# Steel = 5 Acero de refuerzo
#%% ============================= COLUMNAS =============================
# COLUMNAS (A-2, B-2, D-2, E-2) 
# 35x35 --- 3#6 // 2#6 // 3#6 
BcolC = 0.35
HcolC = 0.35
c = 0.05  # recubrimiento 
# creación de la sección de fibra
y1col = HcolC/2.0
z1col = BcolC/2.0
y0col = 0
nFibZ = 1
nFibZcore= 10
nFib = 20
nFibCover, nFibCore = 3, 16
As6 = 0.000286

sec35x35 = 1
col35x35 = [['section', 'Fiber', sec35x35, '-GJ', 1.0e6],
              ['patch', 'rect', Col_Conf, nFibCore, nFibZcore, c-y1col, c-z1col, y1col-c, z1col-c],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, z1col-c, y1col, z1col],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c],
              ['layer', 'straight', Steel, 3, As6, y1col-c, z1col-c, y1col-c, c-z1col],
              ['layer', 'straight', Steel, 2, As6, y0col, z1col-c, y0col, c-z1col],
              ['layer', 'straight', Steel, 3, As6, c-y1col, z1col-c, c-y1col, c-z1col]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(col35x35, matcolor=matcolor)
# plt.axis('equal')

# COLUMNAS (C-2) 
# 35x35 --- 4#5 // 2#5 // 2#5 // 4#5 

Bcol = 0.35
Hcol = 0.35
c = 0.05  # recubrimiento 
# creación de la sección de fibra
y1col = Hcol/2.0
z1col = Bcol/2.0
y2col = (Hcol-(2*c))/3 
nFibZ = 1
nFibZcore= 10
nFib = 20
nFibCover, nFibCore = 3, 16
As5 = 0.0002

secC_35x35 = 2
colC_35x35 = [['section', 'Fiber', secC_35x35, '-GJ', 1.0e6],
              ['patch', 'rect', Col_Conf, nFibCore, nFibZcore, c-y1col, c-z1col, y1col-c, z1col-c],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, z1col-c, y1col, z1col],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c],
              ['layer', 'straight', Steel, 4, As5, y1col-c, z1col-c, y1col-c, c-z1col],
              ['layer', 'straight', Steel, 2, As5, y2col/2, z1col-c, y2col/2, c-z1col],
              ['layer', 'straight', Steel, 2, As5, -y2col/2, z1col-c, -y2col/2, c-z1col],
              ['layer', 'straight', Steel, 4, As5, c-y1col, z1col-c, c-y1col, c-z1col]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(colC_35x35, matcolor=matcolor)
# plt.axis('equal')

#%% ============================== VIGAS ==============================

# VIGAS (VC-103 0.30X0.35)
# 30x35 --- 2#6 & 3#4 // 4#4  

BcolVig = 0.30
HcolVig = 0.35
c = 0.05  # recubrimiento 
# creación de la sección de fibra
y1col = HcolVig/2.0
z1col = BcolVig/2.0
nFibZ = 1
nFibZcore= 10
nFib = 20
nFibCover, nFibCore = 3, 16
As4 = 0.000127
As6 = 0.000286

sec30x35 = 3
vig30x35 = [['section', 'Fiber', sec30x35, '-GJ', 1.0e6],
              ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1col, c-z1col, y1col-c, z1col-c],
              ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col],
              ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1col, z1col-c, y1col, z1col],
              ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c],
              ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c],
              ['layer', 'straight', Steel, 2, As6, y1col-c, z1col-c, y1col-c, c-z1col],
              ['layer', 'straight', Steel, 3, As4, y1col-c, z1col-(c+2*np.sqrt(As6*4/3.141592)), y1col-c, (c+2*np.sqrt(As6*4/3.141592))-z1col],
              ['layer', 'straight', Steel, 4, As4, c-y1col, z1col-c, c-y1col, c-z1col]]

# opsv.plot_fiber_section(vig30x35, matcolor=matcolor)
# plt.axis('equal')
#%% =================== GENERAR LAS SECCIONES ========================
opsv.fib_sec_list_to_cmds(col35x35)
opsv.fib_sec_list_to_cmds(colC_35x35)
opsv.fib_sec_list_to_cmds(vig30x35)

npint = 5
beamIntegration('Lobatto', sec35x35, sec35x35, npint) 
beamIntegration('Lobatto', secC_35x35, secC_35x35, npint) 
beamIntegration('Lobatto', sec30x35, sec30x35, npint) 

