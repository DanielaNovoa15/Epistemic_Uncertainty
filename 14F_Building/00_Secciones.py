"""
------------------------- Secciones del Arquetipo ------------------------
------------------------- @author: Daniela Novoa -------------------------
"""
#%% ======================= IMPORTAR LIBRERIAS ===========================
from openseespy.opensees import *
import numpy as np
import opsvis as opsv
import matplotlib.pyplot as plt
import analisis as an
import utilidades as ut
import pickle
#%% ======================= A TENER EN CUENTA ============================
# --- Columna confinada ---
# Col_Conf = 1 Columna confinada
# ---- Viga connfinada ----
# Vig_Conf = 2
# --Columna no confinada---
# Col_Unconf = 3
# --- Viga no confinada ---
# Vig_Unconf = 4
# --------- Acero ---------
# Steel = 5
#%% ========================= ÁREA DE ACERO ==============================
As3 = 0.0000712
As4 = 0.000127
As5 = 0.000198
As6 = 0.000286
As7 = 0.000387
As8 = 0.000506
#%% =========================== COLUMNAS =================================

# ---------------------------------------------------------------------
# ---------------------------- CLA_T1_(40X70) -------------------------
# ---------------------------------------------------------------------

BCol = 0.40                            # Base de la columna en metros
HCol = 0.70                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1col = HCol/2.0                       # Coordenada y                  
z1col = BCol/2.0                       # Coordenada z
y0col = 0.0
y2col = (y1col-c)/3
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec1ClA_40x70 = 17
Cl1A_40x70 = [['section', 'Fiber', sec1ClA_40x70, '-GJ', 1.0e6],
              ['patch', 'rect', Col_Conf, nFibCore, nFibZcore, c-y1col, c-z1col, y1col-c, z1col-c],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, z1col-c, y1col, z1col],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c],
              ['layer', 'straight', Steel, 5, As7, y1col-c, z1col-c, y1col-c, c-z1col],
              ['layer', 'straight', Steel, 2, As7, y2col, z1col-c, y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As7, y2col*2, z1col-c, y2col*2, c-z1col],
              ['layer', 'straight', Steel, 2, As7, y0col, z1col-c, y0col, c-z1col],
              ['layer', 'straight', Steel, 2, As7, -y2col, z1col-c, -y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As7, -y2col*2, z1col-c, -y2col*2, c-z1col],
              ['layer', 'straight', Steel, 5, As7, c-y1col, z1col-c, c-y1col, c-z1col]]

# matcolor = ['#4F7DA3', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(Cl1A_40x70, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# ---------------------------- CLA_T2_(40X70) -------------------------
# ---------------------------------------------------------------------

BCol = 0.40                            # Base de la columna en metros
HCol = 0.70                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1col = HCol/2.0                       # Coordenada y                  
z1col = BCol/2.0                       # Coordenada z
y0col = 0.0
y2col = (y1col-c)/2
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec2ClA_40x70 = 18
Cl2A_40x70 = [['section', 'Fiber', sec2ClA_40x70, '-GJ', 1.0e6],
              ['patch', 'rect', Col_Conf, nFibCore, nFibZcore, c-y1col, c-z1col, y1col-c, z1col-c],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, z1col-c, y1col, z1col],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c],
              ['layer', 'straight', Steel, 3, As6, y1col-c, z1col-c, y1col-c, c-z1col],
              ['layer', 'straight', Steel, 2, As5, y2col, z1col-c, y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As5, y0col, z1col-c, y0col, c-z1col],
              ['layer', 'straight', Steel, 2, As5, -y2col, z1col-c, -y2col, c-z1col],
              ['layer', 'straight', Steel, 3, As6, c-y1col, z1col-c, c-y1col, c-z1col]]

# matcolor = ['#6B4375', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(Cl2A_40x70, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# ----------------------------- CLD_(40X70) ---------------------------
# ---------------------------------------------------------------------

BCol = 0.40                            # Base de la columna en metros
HCol = 0.70                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1col = HCol/2.0                       # Coordenada y                  
z1col = BCol/2.0                       # Coordenada z
y0col = 0.0
y2col = (y1col-c)/3
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

secClD_40x70 = 19
ClD_40x70 = [['section', 'Fiber', secClD_40x70, '-GJ', 1.0e6],
              ['patch', 'rect', Col_Conf, nFibCore, nFibZcore, c-y1col, c-z1col, y1col-c, z1col-c],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, z1col-c, y1col, z1col],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c],
              ['layer', 'straight', Steel, 5, As8, y1col-c, z1col-c, y1col-c, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y2col, z1col-c, y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y2col*2, z1col-c, y2col*2, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y0col, z1col-c, y0col, c-z1col],
              ['layer', 'straight', Steel, 2, As8, -y2col, z1col-c, -y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As8, -y2col*2, z1col-c, -y2col*2, c-z1col],
              ['layer', 'straight', Steel, 5, As8, c-y1col, z1col-c, c-y1col, c-z1col]]

# matcolor = ['#6B4375', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(ClD_40x70, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# --------------------------- CLB_T1_(40X100) -------------------------
# ---------------------------------------------------------------------

BCol = 0.40                            # Base de la columna en metros
HCol = 1.00                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1col = HCol/2.0                       # Coordenada y                  
z1col = BCol/2.0                       # Coordenada z
y0col = 0.0
y2col = (y1col-c)/5
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec1ClB_40x100 = 20
Cl1B_40x100 = [['section', 'Fiber', sec1ClB_40x100, '-GJ', 1.0e6],
              ['patch', 'rect', Col_Conf, nFibCore, nFibZcore, c-y1col, c-z1col, y1col-c, z1col-c],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, z1col-c, y1col, z1col],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c],
              ['layer', 'straight', Steel, 5, As8, y1col-c, z1col-c, y1col-c, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y2col, z1col-c, y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y2col*2, z1col-c, y2col*2, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y2col*3, z1col-c, y2col*3, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y2col*4, z1col-c, y2col*4, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y0col, z1col-c, y0col, c-z1col],
              ['layer', 'straight', Steel, 2, As8, -y2col, z1col-c, -y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As8, -y2col*2, z1col-c, -y2col*2, c-z1col],
              ['layer', 'straight', Steel, 2, As8, -y2col*3, z1col-c, -y2col*3, c-z1col],
              ['layer', 'straight', Steel, 2, As8, -y2col*4, z1col-c, -y2col*4, c-z1col],
              ['layer', 'straight', Steel, 5, As8, c-y1col, z1col-c, c-y1col, c-z1col]]

# matcolor = ['#784F40', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(Cl1B_40x100, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# --------------------------- CLB_T2_(40X80) --------------------------
# ---------------------------------------------------------------------

BCol = 0.40                            # Base de la columna en metros
HCol = 0.80                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1col = HCol/2.0                       # Coordenada y                  
z1col = BCol/2.0                       # Coordenada z
y0col = 0.0
y2col = (y1col-c)/4
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec2ClB_40x80 = 21
Cl2B_40x80 = [['section', 'Fiber', sec2ClB_40x80, '-GJ', 1.0e6],
              ['patch', 'rect', Col_Conf, nFibCore, nFibZcore, c-y1col, c-z1col, y1col-c, z1col-c],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, z1col-c, y1col, z1col],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c],
              ['layer', 'straight', Steel, 5, As8, y1col-c, z1col-c, y1col-c, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y2col, z1col-c, y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y2col*2, z1col-c, y2col*2, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y2col*3, z1col-c, y2col*3, c-z1col],
              ['layer', 'straight', Steel, 2, As8, y0col, z1col-c, y0col, c-z1col],
              ['layer', 'straight', Steel, 2, As8, -y2col, z1col-c, -y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As8, -y2col*2, z1col-c, -y2col*2, c-z1col],
              ['layer', 'straight', Steel, 2, As8, -y2col*3, z1col-c, -y2col*3, c-z1col],
              ['layer', 'straight', Steel, 5, As8, c-y1col, z1col-c, c-y1col, c-z1col]]

# matcolor = ['#784F40', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(Cl2B_40x80, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# --------------------------- CLB_T3_(40X70) --------------------------
# ---------------------------------------------------------------------

BCol = 0.40                            # Base de la columna en metros
HCol = 0.70                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1col = HCol/2.0                       # Coordenada y                  
z1col = BCol/2.0                       # Coordenada z
y0col = 0.0
z0col = 0.0
y2col = (HCol-2*c)/7
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec3ClB_40x70 = 22
Cl3B_40x70 = [['section', 'Fiber', sec3ClB_40x70, '-GJ', 1.0e6],
              ['patch', 'rect', Col_Conf, nFibCore, nFibZcore, c-y1col, c-z1col, y1col-c, z1col-c],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, z1col-c, y1col, z1col],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c],
              ['layer', 'straight', Steel, 4, As8, y1col-c, z1col-c, y1col-c, c-z1col],
              ['layer', 'straight', Steel, 2, As8, (y1col-c)-y2col, z1col-c, (y1col-c)-y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As8, (y1col-c)-y2col*2, z1col-c, (y1col-c)-y2col*2, c-z1col],
              ['layer', 'straight', Steel, 2, As8, (y1col-c)-y2col*3, z1col-c, (y1col-c)-y2col*3, c-z1col],
              ['layer', 'straight', Steel, 2, As8, (y1col-c)-y2col*4, z1col-c, (y1col-c)-y2col*4, c-z1col],
              ['layer', 'straight', Steel, 2, As8, (y1col-c)-y2col*5, z1col-c, (y1col-c)-y2col*5, c-z1col],
              ['layer', 'straight', Steel, 2, As8, (y1col-c)-y2col*6, z1col-c, (y1col-c)-y2col*6, c-z1col],
              ['layer', 'straight', Steel, 4, As8, c-y1col, z1col-c, c-y1col, c-z1col]]

# matcolor = ['#784F40', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(Cl3B_40x70, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# --------------------------- CLB_T4_(40X70) --------------------------
# ---------------------------------------------------------------------

BCol = 0.40                            # Base de la columna en metros
HCol = 0.70                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1col = HCol/2.0                       # Coordenada y                  
z1col = BCol/2.0                       # Coordenada z
y0col = 0.0
z0col = 0.0
y2col = (y1col-c)/2
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec4ClB_40x70 = 23
Cl4B_40x70 = [['section', 'Fiber', sec4ClB_40x70, '-GJ', 1.0e6],
              ['patch', 'rect', Col_Conf, nFibCore, nFibZcore, c-y1col, c-z1col, y1col-c, z1col-c],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col],
              ['patch', 'rect', Col_Unconf, nFib, nFibZ, -y1col, z1col-c, y1col, z1col],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c],
              ['patch', 'rect', Col_Unconf, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c],
              ['layer', 'straight', Steel, 2, As5, y1col-c, z1col-c, y1col-c, c-z1col],
              ['layer', 'straight', Steel, 1, As6, y1col-c, z0col, y1col-c, z0col],
              ['layer', 'straight', Steel, 2, As5, y2col, z1col-c, y2col, c-z1col],
              ['layer', 'straight', Steel, 2, As5, y0col, z1col-c, y0col, c-z1col],
              ['layer', 'straight', Steel, 2, As6, -y2col, z1col-c, -y2col, c-z1col],
              ['layer', 'straight', Steel, 1, As6, c-y1col, z0col, c-y1col, z0col],
              ['layer', 'straight', Steel, 2, As6, c-y1col, z1col-c, c-y1col, c-z1col]]

# matcolor = ['#784F40', 'lightgrey', 'gray', 'w', 'w', 'w']
# opsv.plot_fiber_section(Cl4B_40x70, matcolor=matcolor)
# plt.axis('equal')
#%% ============================ VIGAS ===================================

# ---------------------------------------------------------------------
# -------------------------- VGA_N-1.2_(60X50) ------------------------
# ------------------------ 2#6 & 2#5 / 2#6 & 2#5 ----------------------
# ---------------------------------------------------------------------
 
BVig = 0.60                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z
z2vig = (BVig-2*c)/3                   
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

secVgA_60x50 = 1
VgA_60x50 = [['section', 'Fiber', secVgA_60x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-c, y1vig-c, c-z1vig], 
               ['layer', 'straight', Steel, 2, As5, y1vig-c, z1vig-(c+z2vig), y1vig-c, (c+z2vig)-z1vig],
               ['layer', 'straight', Steel, 2, As5, c-y1vig, z1vig-(c+z2vig), c-y1vig, (c+z2vig)-z1vig],              
               ['layer', 'straight', Steel, 2, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(VgA_60x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGB_N-1.2_(95X50) ------------------------
# ------------------------ 2#6 & 4#5 / 2#6 & 4#5 ----------------------
# ---------------------------------------------------------------------
 
BVig = 0.95                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z
z2vig = (BVig-2*c)/5                   
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

secVgB_95x50 = 2
VgB_95x50 = [['section', 'Fiber', secVgB_95x50, '-GJ', 1.0e6],
                ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
                ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
                ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
                ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
                ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
                ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-c, y1vig-c, c-z1vig], 
                ['layer', 'straight', Steel, 4, As5, y1vig-c, z1vig-(c+z2vig), y1vig-c, (c+z2vig)-z1vig],
                ['layer', 'straight', Steel, 4, As5, c-y1vig, z1vig-(c+z2vig), c-y1vig, (c+z2vig)-z1vig],              
                ['layer', 'straight', Steel, 2, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(VgB_95x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGC_N-1.2_(60X50) ------------------------
# --------------------- 2#7 & 4#6 & 3#5 / 5#6 & 2#5 -------------------
# ---------------------------------------------------------------------
 
BVig = 0.60                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z
z2vig = (BVig-2*c)/6 
z3vig = (BVig-2*c)/8              
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

secVgC_60x50 = 3
VgC_60x50 = [['section', 'Fiber', secVgC_60x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 2, As7, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-(c+z3vig), y1vig-c, (c+z3vig)-z1vig],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-(c+z3vig*2), y1vig-c, (c+z3vig*2)-z1vig],
               ['layer', 'straight', Steel, 3, As5, y1vig-c, z1vig-(c+z3vig*3), y1vig-c, (c+z3vig*3)-z1vig],
               ['layer', 'straight', Steel, 2, As5, c-y1vig, z1vig-(c+z2vig*2), c-y1vig, (c+z2vig*2)-z1vig],
               ['layer', 'straight', Steel, 3, As6, c-y1vig, z1vig-(c+z2vig), c-y1vig, (c+z2vig)-z1vig], 
               ['layer', 'straight', Steel, 2, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(VgC_60x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGA_N+1.9_(60X50) ------------------------
# --------------------------- 4#6 & 2#5 / 5#6 -------------------------
# ---------------------------------------------------------------------
 
BVig = 0.60                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z
z2vig = (BVig-2*c)/5              
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec2VgA_60x50 = 4
Vg2A_60x50 = [['section', 'Fiber', sec2VgA_60x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-(c+z2vig), y1vig-c, (c+z2vig)-z1vig],
               ['layer', 'straight', Steel, 2, As5, y1vig-c, z1vig-(c+z2vig*2), y1vig-c, (c+z2vig*2)-z1vig],
               ['layer', 'straight', Steel, 5, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg2A_60x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGC_N+1.9_(60X50) ------------------------
# --------------------------- 8#7 / 5#7 & 1#6 -------------------------
# ---------------------------------------------------------------------
 
BVig = 0.60                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z     
z2vig = (BVig-2*c)/5         
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec2VgC_60x50 = 5
Vg2C_60x50 = [['section', 'Fiber', sec2VgC_60x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 8, As7, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 1, As6, c-y1vig, z1vig-(c+z2vig*3), c-y1vig, (c+z2vig*3)-z1vig],
               ['layer', 'straight', Steel, 1, As7, c-y1vig, z1vig-(c+z2vig*2), c-y1vig, (c+z2vig*2)-z1vig],
               ['layer', 'straight', Steel, 2, As7, c-y1vig, z1vig-(c+z2vig), c-y1vig, (c+z2vig)-z1vig],
               ['layer', 'straight', Steel, 2, As7, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg2C_60x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGA_N+4.9_(60X50) ------------------------
# ------------------------ 2#7 & 2#6 & 3#5 / 5#6 ----------------------
# ---------------------------------------------------------------------
 
BVig = 0.60                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z    
z2vig = (BVig-2*c)/6       
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec3VgA_60x50 = 6
Vg3A_60x50 = [['section', 'Fiber', sec3VgA_60x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 2, As7, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-(c+z2vig), y1vig-c, (c+z2vig)-z1vig],
               ['layer', 'straight', Steel, 3, As5, y1vig-c, z1vig-(c+z2vig*2), y1vig-c, (c+z2vig*2)-z1vig],
               ['layer', 'straight', Steel, 5, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg3A_60x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGC_N+4.9_(60X50) ------------------------
# ------------------------------ 8#7 / 5#7 ----------------------------
# ---------------------------------------------------------------------
 
BVig = 0.60                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z             
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec3VgC_60x50 = 7
Vg3C_60x50 = [['section', 'Fiber', sec3VgC_60x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 8, As7, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 5, As7, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg3C_60x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGA_N+7.9_(80X50) ------------------------
# --------------------------- 9#7 / 5#7 & 2#6 -------------------------
# ---------------------------------------------------------------------
 
BVig = 0.80                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z
z2vig = (BVig-2*c)/6              
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec4VgA_80x50 = 8
Vg4A_80x50 = [['section', 'Fiber', sec4VgA_80x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 9, As7, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 2, As6, c-y1vig, z1vig-(c+z2vig*2), c-y1vig, (c+z2vig*2)-z1vig],
               ['layer', 'straight', Steel, 1, As7, c-y1vig, z1vig-(c+z2vig*3), c-y1vig, (c+z2vig*3)-z1vig],
               ['layer', 'straight', Steel, 2, As7, c-y1vig, z1vig-(c+z2vig), c-y1vig, (c+z2vig)-z1vig],
               ['layer', 'straight', Steel, 2, As7, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg4A_80x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGC_N+7.9_(80X50) ------------------------
# ------------------------ 6#7 & 4#6 / 2#7 & 5#6 ----------------------
# ---------------------------------------------------------------------
 
BVig = 0.80                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z   
z2vig = (BVig-2*c)/9
z3vig = (BVig-2*c)/6       
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec4VgC_80x50 = 9
Vg4C_80x50 = [['section', 'Fiber', sec4VgC_80x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 2, As7, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 2, As7, y1vig-c, z1vig-(c+z2vig), y1vig-c, (c+z2vig)-z1vig],
               ['layer', 'straight', Steel, 2, As7, y1vig-c, z1vig-(c+z2vig*2), y1vig-c, (c+z2vig*2)-z1vig],
               ['layer', 'straight', Steel, 4, As6, y1vig-c, z1vig-(c+z2vig*3), y1vig-c, (c+z2vig*3)-z1vig],
               ['layer', 'straight', Steel, 3, As6, c-y1vig, z1vig-(c+z3vig*2), c-y1vig, (c+z3vig*2)-z1vig],
               ['layer', 'straight', Steel, 2, As6, c-y1vig, z1vig-(c+z3vig), c-y1vig, (c+z3vig)-z1vig],
               ['layer', 'straight', Steel, 2, As7, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg4C_80x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGC_N+28.9_(80X50) -----------------------
# ------------------------ 7#7 & 4#6 / 3#7 & 5#6 ----------------------
# ---------------------------------------------------------------------
 
BVig = 0.80                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z   
z2vig = (BVig-2*c)/10
z3vig = (BVig-2*c)/7       
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec5VgC_80x50 = 10
Vg5C_80x50 = [['section', 'Fiber', sec5VgC_80x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 2, As7, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 2, As7, y1vig-c, z1vig-(c+z2vig), y1vig-c, (c+z2vig)-z1vig],
               ['layer', 'straight', Steel, 2, As7, y1vig-c, z1vig-(c+z2vig*2), y1vig-c, (c+z2vig*2)-z1vig],
               ['layer', 'straight', Steel, 1, As7, y1vig-c, z1vig-(c+z2vig*5), y1vig-c, (c+z2vig*5)-z1vig],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-(c+z2vig*3), y1vig-c, (c+z2vig*3)-z1vig],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-(c+z2vig*4), y1vig-c, (c+z2vig*4)-z1vig],
               ['layer', 'straight', Steel, 1, As6, c-y1vig, z1vig-(c+z3vig*4), c-y1vig, (c+z3vig*4)-z1vig],
               ['layer', 'straight', Steel, 2, As6, c-y1vig, z1vig-(c+z3vig*2), c-y1vig, (c+z3vig*2)-z1vig],
               ['layer', 'straight', Steel, 2, As6, c-y1vig, z1vig-(c+z3vig), c-y1vig, (c+z3vig)-z1vig],
               ['layer', 'straight', Steel, 1, As7, c-y1vig, z1vig-(c+z3vig*3), c-y1vig, (c+z3vig*3)-z1vig],
               ['layer', 'straight', Steel, 2, As7, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg5C_80x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGA_N+34.9_(60X50) -----------------------
# ------------------------------ 6#6 / 4#6 ----------------------------
# ---------------------------------------------------------------------
 
BVig = 0.60                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z         
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec6VgA_60x50 = 11
Vg6A_60x50 = [['section', 'Fiber', sec6VgA_60x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 6, As6, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 4, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg6A_60x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGB_N+34.9_(60X50) -----------------------
# ------------------------------ 8#6 / 4#6 ----------------------------
# ---------------------------------------------------------------------
 
BVig = 0.95                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z         
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec6VgB_95x50 = 12
Vg6B_95x50 = [['section', 'Fiber', sec6VgB_95x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 8, As6, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 4, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg6B_95x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGC_N+34.9_(60X50) -----------------------
# ------------------------------ 9#6 / 5#6 ----------------------------
# ---------------------------------------------------------------------
 
BVig = 0.60                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z         
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec6VgC_60x50 = 13
Vg6C_60x50 = [['section', 'Fiber', sec6VgC_60x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 9, As6, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 5, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg6C_60x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGA_N+37.9_(50X50) -----------------------
# --------------------------- 6#7 & 2#5 / 4#6 -------------------------
# ---------------------------------------------------------------------
 
BVig = 0.50                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z   
z2vig = (BVig-2*c)/7
z3vig = (BVig-2*c)/5       
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec7VgA_50x50 = 14
Vg7A_50x50 = [['section', 'Fiber', sec7VgA_50x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-(c+z2vig), y1vig-c, (c+z2vig)-z1vig],
               ['layer', 'straight', Steel, 2, As6, y1vig-c, z1vig-(c+z2vig*2), y1vig-c, (c+z2vig*2)-z1vig],
               ['layer', 'straight', Steel, 2, As5, y1vig-c, z1vig-(c+z2vig*3), y1vig-c, (c+z2vig*3)-z1vig],
               ['layer', 'straight', Steel, 4, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg7A_50x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGB_N+37.9_(50X50) -----------------------
# ------------------------------ 8#6 / 4#6 ----------------------------
# ---------------------------------------------------------------------
 
BVig = 0.50                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z         
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec7VgB_50x50 = 15
Vg7B_50x50 = [['section', 'Fiber', sec7VgB_50x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 8, As6, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 4, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg7B_50x50, matcolor=matcolor)
# plt.axis('equal')

# ---------------------------------------------------------------------
# -------------------------- VGC_N+37.9_(50X50) -----------------------
# ------------------------------ 8#6 / 4#6 ----------------------------
# ---------------------------------------------------------------------
 
BVig = 0.50                            # Base de la columna en metros
HVig = 0.50                            # Altura de la columna en metros
c = 0.04                               # Recubrimiento en metros
# ------------------------- Coordenadas y & z -------------------------
y1vig = HVig/2.0                       # Coordenada y                  
z1vig = BVig/2.0                       # Coordenada z         
# ------------------ Creación de la sección de fibra ------------------
nFibZ = 1                              # Número fibras z no confinado 
nFib = 20                              # Número fibras y no confinado (T)
nFibCover = 3                          # Número fibras y no confinado (L)
nFibZcore= 10                          # Número fibras z confinado
nFibCore = 16                          # Número fibras y confinado 

sec7VgC_50x50 = 16
Vg7C_50x50 = [['section', 'Fiber', sec7VgC_50x50, '-GJ', 1.0e6],
               ['patch', 'rect', Vig_Conf, nFibCore, nFibZcore, c-y1vig, c-z1vig, y1vig-c, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, -z1vig, y1vig, c-z1vig],
               ['patch', 'rect', Vig_Unconf, nFib, nFibZ, -y1vig, z1vig-c, y1vig, z1vig],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, -y1vig, c-z1vig, c-y1vig, z1vig-c],
               ['patch', 'rect', Vig_Unconf, nFibCover, nFibZ, y1vig-c, c-z1vig, y1vig, z1vig-c],
               ['layer', 'straight', Steel, 9, As6, y1vig-c, z1vig-c, y1vig-c, c-z1vig],
               ['layer', 'straight', Steel, 5, As6, c-y1vig, z1vig-c, c-y1vig, c-z1vig]]

# matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
# opsv.plot_fiber_section(Vg7C_50x50, matcolor=matcolor)
# plt.axis('equal')
#%% ===================== GENERAR LAS SECCIONES ==========================
# =============================== VIGAS ===============================
opsv.fib_sec_list_to_cmds(VgA_60x50)
opsv.fib_sec_list_to_cmds(VgB_95x50)
opsv.fib_sec_list_to_cmds(VgC_60x50)
opsv.fib_sec_list_to_cmds(Vg2A_60x50)
opsv.fib_sec_list_to_cmds(Vg2C_60x50)
opsv.fib_sec_list_to_cmds(Vg3A_60x50)
opsv.fib_sec_list_to_cmds(Vg3C_60x50)
opsv.fib_sec_list_to_cmds(Vg4A_80x50)
opsv.fib_sec_list_to_cmds(Vg4C_80x50)
opsv.fib_sec_list_to_cmds(Vg5C_80x50)
opsv.fib_sec_list_to_cmds(Vg6A_60x50)
opsv.fib_sec_list_to_cmds(Vg6B_95x50)
opsv.fib_sec_list_to_cmds(Vg6C_60x50)
opsv.fib_sec_list_to_cmds(Vg7A_50x50)
opsv.fib_sec_list_to_cmds(Vg7B_50x50)
opsv.fib_sec_list_to_cmds(Vg7C_50x50)
# ============================= COLUMNAS =============================
opsv.fib_sec_list_to_cmds(Cl1A_40x70)
opsv.fib_sec_list_to_cmds(Cl2A_40x70)
opsv.fib_sec_list_to_cmds(ClD_40x70)
opsv.fib_sec_list_to_cmds(Cl1B_40x100)
opsv.fib_sec_list_to_cmds(Cl2B_40x80)
opsv.fib_sec_list_to_cmds(Cl3B_40x70)
opsv.fib_sec_list_to_cmds(Cl4B_40x70)
npint = 5
# =============================== VIGAS ===============================
beamIntegration('Lobatto', secVgA_60x50, secVgA_60x50, npint) 
beamIntegration('Lobatto', secVgB_95x50, secVgB_95x50, npint) 
beamIntegration('Lobatto', secVgC_60x50, secVgC_60x50, npint) 
beamIntegration('Lobatto', sec2VgA_60x50, sec2VgA_60x50, npint) 
beamIntegration('Lobatto', sec2VgC_60x50, sec2VgC_60x50, npint) 
beamIntegration('Lobatto', sec3VgA_60x50, sec3VgA_60x50, npint)
beamIntegration('Lobatto', sec3VgC_60x50, sec3VgC_60x50, npint) 
beamIntegration('Lobatto', sec4VgA_80x50, sec4VgA_80x50, npint)  
beamIntegration('Lobatto', sec4VgC_80x50, sec4VgC_80x50, npint) 
beamIntegration('Lobatto', sec5VgC_80x50, sec5VgC_80x50, npint) 
beamIntegration('Lobatto', sec6VgA_60x50, sec6VgA_60x50, npint) 
beamIntegration('Lobatto', sec6VgB_95x50, sec6VgB_95x50, npint) 
beamIntegration('Lobatto', sec6VgC_60x50, sec6VgC_60x50, npint) 
beamIntegration('Lobatto', sec7VgA_50x50, sec7VgA_50x50, npint) 
beamIntegration('Lobatto', sec7VgB_50x50, sec7VgB_50x50, npint) 
beamIntegration('Lobatto', sec7VgC_50x50, sec7VgC_50x50, npint) 
# ============================= COLUMNAS =============================
beamIntegration('Lobatto', sec1ClA_40x70, sec1ClA_40x70, npint)  
beamIntegration('Lobatto', sec2ClA_40x70, sec2ClA_40x70, npint)
beamIntegration('Lobatto', secClD_40x70, secClD_40x70, npint)
beamIntegration('Lobatto', sec1ClB_40x100, sec1ClB_40x100, npint)
beamIntegration('Lobatto', sec2ClB_40x80, sec2ClB_40x80, npint)
beamIntegration('Lobatto', sec3ClB_40x70, sec3ClB_40x70, npint)
beamIntegration('Lobatto', sec4ClB_40x70, sec4ClB_40x70, npint)
