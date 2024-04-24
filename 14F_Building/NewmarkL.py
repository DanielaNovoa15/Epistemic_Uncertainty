# -*- coding: utf-8 -*-
"""
Método de Newmark
@author: Daniela Novoa
"""

from openseespy.opensees import *
import opsvis as opsv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

#%% Newmark
def newmarkL(T,xi,GM,delta_t,betha = 1/6, gamma = 1/2 ,u0 = 0,v0 = 0,P0 = 0):
    #T: periodo de la estrutura
    #xi: porcentaje de amortiguamiento crítico
    #GM: registro en unidades consistentes
    #delta_t: delta de tiempo del registro
    #betha, gamma: parámetros del Newmark. Por defecto utiliza método lineal de interpolación
    #u0,v0,a0: condiciones iniciales de desplazamiento velocidad y aceleración
    
    w = 2*np.pi/T
    m = 1.0
    k = m*w**2
    c = 2*xi*m*w
    # Calculos iniciales
    a0 = (P0-c*v0-k*u0)/m                     # Aceleración inicial
    a1 = m/(betha*(delta_t**2))+(gamma*c)/(betha*delta_t)
    a2 = m/(betha*delta_t)+(gamma/betha-1)*c
    a3 = (1/(2*betha)-1)*m+delta_t*(gamma/(2*betha)-1)*c
    k_g = k+a1
    
    # INICIAR VARIABLES
    
    Npts = len(GM)+1
    Desplz = np.zeros((Npts,1))
    Vel = np.zeros((Npts,1))
    Acel = np.zeros((Npts,1))
    Tiempo = np.linspace(0,delta_t*(Npts-1),Npts)
    P_1 = GM*m
    P_2 = np.zeros((Npts,1))
    
    for i in range(Npts-1):
        P_2[i+1] = P_1[i] + a1*Desplz[i] + a2*Vel[i] + a3*Acel[i]
        Desplz[i+1] = P_2[i+1]/k_g
        Vel[i+1] = gamma/(betha*delta_t)*(Desplz[i+1]-Desplz[i])+(1-(gamma/betha))*Vel[i]+delta_t*(1-(gamma/(2*betha)))*Acel[i]
        Acel[i+1] = (Desplz[i+1]-Desplz[i])/(betha*(delta_t**2))-Vel[i]/(betha*delta_t)-(1/(2*betha)-1)*Acel[i]
        
    return Tiempo,Desplz,Vel,Acel
        
#%% Newmark 2
def newmarkLA(T,xi,GM,delta_t,flag = 'all',betha = 1/6, gamma = 1/2 ,u0 = 0,v0 = 0,P0 = 0):
    #T: periodo de la estrutura
    #xi: porcentaje de amortiguamiento crítico
    #GM: registro en unidades consistentes
    #delta_t: delta de tiempo del registro
    #flag: recibe 'max' cuando solo se deseen los valores máximos de tiempo, desplazamiento, velocidad y aceleracion absolutas.
    #betha, gamma: parámetros del Newmark. Por defecto utiliza método lineal de interpolación
    #u0,v0,a0: condiciones iniciales de desplazamiento velocidad y aceleración
    
    
    w = 2*np.pi/T
    m = 1.0
    k = m*w**2
    c = 2*xi*m*w
    # Calculos iniciales
    a0 = (P0-c*v0-k*u0)/m                     # Aceleración inicial
    a1 = m/(betha*(delta_t**2))+(gamma*c)/(betha*delta_t)
    a2 = m/(betha*delta_t)+(gamma/betha-1)*c
    a3 = (1/(2*betha)-1)*m+delta_t*(gamma/(2*betha)-1)*c
    k_g = k+a1
    
    # INICIAR VARIABLES
    
    Npts = len(GM)
    Desplz = np.zeros((Npts))
    Vel = np.zeros((Npts))
    Acel = np.zeros((Npts))
    Tiempo = np.linspace(0,delta_t*(Npts-1),Npts)
    P_1 = GM*m
    P_2 = np.zeros((Npts))
    
    for i in range(Npts-2):
        P_2[i+1] = P_1[i] + a1*Desplz[i] + a2*Vel[i] + a3*Acel[i]
        Desplz[i+1] = P_2[i+1]/k_g
        Vel[i+1] = gamma/(betha*delta_t)*(Desplz[i+1]-Desplz[i])+(1-(gamma/betha))*Vel[i]+delta_t*(1-(gamma/(2*betha)))*Acel[i]
        Acel[i+1] = (Desplz[i+1]-Desplz[i])/(betha*(delta_t**2))-Vel[i]/(betha*delta_t)-(1/(2*betha)-1)*Acel[i]
    
    AcelAbs = Acel + GM # Aquí se calcula la aceleración absoluta
    
    if flag == 'max':
        TT = np.max(np.abs(Tiempo))
        DD = np.max(np.abs(Desplz))
        VV = np.max(np.abs(Vel))
        AA = np.max(np.abs(AcelAbs))
    else:
        TT = Tiempo
        DD = Desplz
        VV = Vel
        AA = Acel
    
    return TT,DD,VV,AA


def newmarkLA2(T,xi,GM,delta_t,flag = 'all',betha = 1/6, gamma = 1/2 ,u0 = 0,v0 = 0,P0 = 0):
    #T: periodo de la estrutura
    #xi: porcentaje de amortiguamiento crítico
    #GM: registro en unidades consistentes
    #delta_t: delta de tiempo del registro
    #flag: recibe 'max' cuando solo se deseen los valores máximos de tiempo, desplazamiento, velocidad y aceleracion absolutas.
    #betha, gamma: parámetros del Newmark. Por defecto utiliza método lineal de interpolación
    #u0,v0,a0: condiciones iniciales de desplazamiento velocidad y aceleración
    
    
    w = 2*np.pi/T
    m = 1.0
    k = m*w**2
    c = 2*xi*m*w
    # Calculos iniciales
    a0 = (P0-c*v0-k*u0)/m                     # Aceleración inicial
    a1 = m/(betha*(delta_t**2))+(gamma*c)/(betha*delta_t)
    a2 = m/(betha*delta_t)+(gamma/betha-1)*c
    a3 = (1/(2*betha)-1)*m+delta_t*(gamma/(2*betha)-1)*c
    k_g = k+a1
    
    # INICIAR VARIABLES
    
    Npts = len(GM)
    Desplz = np.zeros((Npts))
    Vel = np.zeros((Npts))
    Acel = np.zeros((Npts))
    Tiempo = np.linspace(0,delta_t*(Npts-1),Npts)
    P_1 = GM*m
    P_2 = np.zeros((Npts))
    
    for i in range(Npts-2):
        P_2[i+1] = P_1[i] + a1*Desplz[i] + a2*Vel[i] + a3*Acel[i]
        Desplz[i+1] = P_2[i+1]/k_g
        Vel[i+1] = gamma/(betha*delta_t)*(Desplz[i+1]-Desplz[i])+(1-(gamma/betha))*Vel[i]+delta_t*(1-(gamma/(2*betha)))*Acel[i]
        Acel[i+1] = (Desplz[i+1]-Desplz[i])/(betha*(delta_t**2))-Vel[i]/(betha*delta_t)-(1/(2*betha)-1)*Acel[i]
    
    AcelAbs = Acel + GM # Aquí se calcula la aceleración absoluta
    
    if flag == 'max':
        TT = np.max(np.abs(Tiempo))
        DD = np.max(np.abs(Desplz))
        VV = np.max(np.abs(Vel))
        AA = np.max(np.abs(AcelAbs))
    else:
        TT = Tiempo
        DD = Desplz
        VV = Vel
        AA = Acel
    
    return TT,DD,VV,AA,Acel,AcelAbs

def newmarkLM(T,xi,GM,delta_t,betha = 1/6, gamma = 1/2 ,u0 = 0,v0 = 0,P0 = 0):
    #T: periodo de la estrutura
    #xi: porcentaje de amortiguamiento crítico
    #GM: registro en unidades consistentes
    #delta_t: delta de tiempo del registro
    #flag: recibe 'max' cuando solo se deseen los valores máximos de tiempo, desplazamiento, velocidad y aceleracion absolutas.
    #betha, gamma: parámetros del Newmark. Por defecto utiliza método lineal de interpolación
    #u0,v0,a0: condiciones iniciales de desplazamiento velocidad y aceleración
    
    
    w = 2*np.pi/T
    m = 1.0
    k = m*w**2
    c = 2*xi*m*w
    # Calculos iniciales
    a0 = (P0-c*v0-k*u0)/m                     # Aceleración inicial
    a1 = m/(betha*(delta_t**2))+(gamma*c)/(betha*delta_t)
    a2 = m/(betha*delta_t)+(gamma/betha-1)*c
    a3 = (1/(2*betha)-1)*m+delta_t*(gamma/(2*betha)-1)*c
    k_g = k+a1
    
    # INICIAR VARIABLES
    
    Npts = len(GM)
    des1, des2, maxdes = 0,0,-1000000 # Desplz = np.zeros((Npts,1))
    vel1, vel2, maxvel = 0,0,-1000000 # Vel = np.zeros((Npts,1))
    acc1, acc2, maxacc = 0,0,0 # Acel = np.zeros((Npts,1))
    # Tiempo = np.linspace(0,delta_t*(Npts-1),Npts)
    P_1 = GM*m
    P21, P22 = 0,0 # P_2 = np.zeros((Npts,1))
    Acel = []
    Acel = np.zeros(Npts)
    print(Npts)
    for i in range(Npts-2):
        P22 = P_1[i] + a1*des1 + a2*vel1 + a3*acc1 # P_2[i+1] = P_1[i] + a1*Desplz[i] + a2*Vel[i] + a3*Acel[i]
        des2 = P22/k_g # Desplz[i+1] = P_2[i+1]/k_g
        vel2 = gamma/(betha*delta_t)*(des2-des1)+(1-(gamma/betha))*vel1+delta_t*(1-(gamma/(2*betha)))*acc1 # Vel[i+1] = gamma/(betha*delta_t)*(Desplz[i+1]-Desplz[i])+(1-(gamma/betha))*Vel[i]+delta_t*(1-(gamma/(2*betha)))*Acel[i]
        acc2 = (des2-des1)/(betha*(delta_t**2))-vel1/(betha*delta_t)-(1/(2*betha)-1)*acc1 # Acel[i+1] = (Desplz[i+1]-Desplz[i])/(betha*(delta_t**2))-Vel[i]/(betha*delta_t)-(1/(2*betha)-1)*Acel[i]
        # Acel.append(acc2+GM[i])
        des1 = des2+0
        vel1 = vel2+0
        acc1 = acc2+0
        Acel[i+1] = acc2 + GM[i]
        maxacc = max(maxacc,np.abs(acc2+GM[i+1]))
        maxdes = max(maxdes,np.abs(des2))
        # print(i)

    
    return maxdes, maxacc, Acel

def newmarkLA3(T,xi,GM,TH,delta_t,flag = 'all',betha = 1/6, gamma = 1/2 ,u0 = 0,v0 = 0,P0 = 0):
    #T: periodo de la estrutura
    #xi: porcentaje de amortiguamiento crítico
    #GM: registro en unidades consistentes
    #delta_t: delta de tiempo del registro
    #flag: recibe 'max' cuando solo se deseen los valores máximos de tiempo, desplazamiento, velocidad y aceleracion absolutas.
    #betha, gamma: parámetros del Newmark. Por defecto utiliza método lineal de interpolación
    #u0,v0,a0: condiciones iniciales de desplazamiento velocidad y aceleración
    
    
    w = 2*np.pi/T
    m = 1.0
    k = m*w**2
    c = 2*xi*m*w
    # Calculos iniciales
    a0 = (P0-c*v0-k*u0)/m                     # Aceleración inicial
    a1 = m/(betha*(delta_t**2))+(gamma*c)/(betha*delta_t)
    a2 = m/(betha*delta_t)+(gamma/betha-1)*c
    a3 = (1/(2*betha)-1)*m+delta_t*(gamma/(2*betha)-1)*c
    k_g = k+a1
    
    # INICIAR VARIABLES
    
    Npts = len(GM)
    Desplz = np.zeros((Npts))
    Vel = np.zeros((Npts))
    Acel = np.zeros((Npts))
    Tiempo = TH
    P_1 = GM*m
    P_2 = np.zeros((Npts))
    
    for i in range(Npts-2):
        P_2[i+1] = P_1[i] + a1*Desplz[i] + a2*Vel[i] + a3*Acel[i]
        Desplz[i+1] = P_2[i+1]/k_g
        Vel[i+1] = gamma/(betha*delta_t)*(Desplz[i+1]-Desplz[i])+(1-(gamma/betha))*Vel[i]+delta_t*(1-(gamma/(2*betha)))*Acel[i]
        Acel[i+1] = (Desplz[i+1]-Desplz[i])/(betha*(delta_t**2))-Vel[i]/(betha*delta_t)-(1/(2*betha)-1)*Acel[i]
    
    AcelAbs = Acel + GM # Aquí se calcula la aceleración absoluta
    
    if flag == 'max':
        TT = np.max(np.abs(Tiempo))
        DD = np.max(np.abs(Desplz))
        VV = np.max(np.abs(Vel))
        AA = np.max(np.abs(AcelAbs))
    else:
        TT = Tiempo
        DD = Desplz
        VV = Vel
        AA = Acel
    
    return TT,DD,VV,AA



#%% Espectro elástico

def spectrum(GM,delta_t,xi):
    N = 400
    T = np.linspace(0.02,3,N)
    Sa = np.zeros(N)
    U = np.zeros(N)
    V = np.zeros(N)
    
    for i,per in enumerate(T):
        w = 2*np.pi/per
        Tiempo,Desplz,Vel,Acel = newmarkL(per,xi,GM,delta_t)
        umax = np.max(np.abs(Desplz))
        vmax = np.max(np.abs(Vel))
        U[i] = umax
        V[i] = vmax
        Sa[i] = umax*w**2
    return T,Sa
    

def spectrum2(GM,delta_t,xi):
    N = 400
    T = np.linspace(0.02,3,N)
    Sa = np.zeros(N)
    U = np.zeros(N)
    V = np.zeros(N)
    
    for i,per in enumerate(T):
        w = 2*np.pi/per
        Tiempo,Desplz,Vel,Acel = newmarkLA(per,xi,GM,delta_t,'max')
        U[i] = Desplz
        V[i] = Vel
        Sa[i] = Desplz*w**2
    return T,Sa


def spectrum3(GM,TH,delta_t,xi):
    N = 400
    T = np.linspace(0.02,3,N)
    Sa = np.zeros(N)
    U = np.zeros(N)
    V = np.zeros(N)
    
    for i,per in enumerate(T):
        w = 2*np.pi/per
        Tiempo,Desplz,Vel,Acel = newmarkLA3(per,xi,GM,TH,delta_t,'max')
        U[i] = Desplz
        V[i] = Vel
        Sa[i] = Desplz*w**2
    return T,Sa


def spectrum4(GM,dt,xi=0.05,rango=[0.02,3.0],N=100):
    ''' spectrum4(GM,dt,xi=0.05,rango=[0.02,3.0],N=100):
        está basado en la rutina de OpenSees
        GM: el registro en .txt. Por ejemplo 'GM01.txt'
        dt: dt del registro
        xi: porcentaje del amortiguamiento crítico
        rango: rango de periodos en un vector
        N: número de puntos
           
    '''
    m = 1
    T = np.linspace(rango[0],rango[1],N)
    w = 2*np.pi/T
    k = m*w**2
    Sa = np.zeros(N)
    U = np.zeros(N)
    A = np.zeros(N)
    for indx, frec in enumerate(w):
        umax,ufin,uperm,amax,tamax = sdfResponse(m,xi,k[indx],1e16,0.05,dt,GM,dt)
        U[indx] = umax
        Sa[indx] = umax*frec**2
        A[indx] = amax
    return T,Sa,U,A
    
# %% Prueba
# record = np.loadtxt('GM07.txt')
# s1 = time.time()
# T,U,V,A= newmarkLA(0.15,0.02,record,0.01)

# T2,U2,V2,A2 = newmarkLA(0.15,0.05,record,0.01)


# T3,U3,V3,A3 = newmarkLA(0.15,0.10,record,0.01)


# plt.plot(T,U,T2,U2,T3,U3)

# s2 = time.time()
# plt.plot(T,U)
# plt.show()
# print(np.max(A))
# print(np.min(A))
# s3 = time.time()
# md,ma,acc = newmarkLM(0.15,0.05,record,0.01)
# s4 = time.time()
# print(ma)
# print(s2-s1,'s')
# print(s4-s3,'s')

# #%% 
# s5 = time.time()
# PER,Sa = spectrum(record,0.01,0.05)
# s6 = time.time()
# print(s6-s5,'s')
# plt.plot(PER,Sa)
# # plt.show()

# s5 = time.time()
# PER,Sa = spectrum(record,0.01,0.02)
# s6 = time.time()
# print(s6-s5,'s')
# plt.plot(PER,Sa)
# plt.show()

# s7 = time.time()
# PER2,Sa2 = spectrum2(record,0.01,0.05)
# s8 = time.time()
# print(s8-s7,'s')
# plt.figure()
# plt.plot(PER,Sa,PER2,Sa2)
# plt.show()

#%%  Prueba espectro
import time
gg = np.loadtxt('GM23.txt')
tt = np.linspace(0,len(gg)*0.005,len(gg))
stime = time.time()
T,Sa = spectrum3(gg,tt,0.005,0.05)
etime = time.time() # tiempo final
ttotal = etime - stime # para calcular el tiempo de ejecución
plt.plot(T,Sa)
plt.show()

stime2 = time.time()
T2,Sa2,U2,A2 = spectrum4('GM23.txt',0.005,0.05,[0.02,3.0],400)
etime2 = time.time() # tiempo final
ttotal2 = etime2 - stime2 # para calcular el tiempo de ejecución
plt.plot(T,Sa,T2,Sa2)
plt.show()

