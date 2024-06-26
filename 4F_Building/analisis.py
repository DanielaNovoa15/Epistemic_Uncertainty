# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 17:59:44 2022

@author: Orlando
"""
from openseespy.opensees import *
import matplotlib.pyplot as plt
import numpy as np

# ANALISIS DE GRAVEDAD
# =============================
def gravedad():
    
# Create the system of equation, a sparse solver with partial pivoting
    system('BandGeneral')

# Create the constraint handler, the transformation method
    constraints('Plain')

# Create the DOF numberer, the reverse Cuthill-McKee algorithm
    numberer('RCM')

# Create the convergence test, the norm of the residual with a tolerance of
# 1e-12 and a max number of iterations of 10
    test('NormDispIncr', 1.0e-12, 10, 3)

# Create the solution algorithm, a Newton-Raphson algorithm
    algorithm('Newton')

# Create the integration scheme, the LoadControl scheme using steps of 0.1
    integrator('LoadControl', 0.1)

# Create the analysis object
    analysis('Static')

    ok = analyze(10)
    
    if ok != 0:
        print('Análisis de gravedad fallido')
        sys.exit()
    # else:
    #     print('       ----ANÁLISIS DE GRAVEDAD COMPLETADO----')
        


# ANALISIS PUSHOVER
# =============================

def pushover(Dmax,Dincr,IDctrlNode,IDctrlDOF):
    
    recorder('Node','-file','techo.out','-time','-node',IDctrlNode,'-dof',IDctrlDOF,'disp')
    maxNumIter = 6
    Tol = 1e-8
      
    
    wipeAnalysis()
    constraints('Transformation')
    numberer('Plain')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')
    
    integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
    analysis('Static')
    
    
    Nsteps =  int(Dmax/ Dincr)
    
    ok = analyze(Nsteps)
    print(ok)
    print('Pushover completado sin problemas')
    
    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}
    
    
    for i in tests:
        for j in algoritmo:
    
            if ok != 0:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
                    
                else:
                    algorithm(algoritmo[j])
                    
                test(tests[i], Tol, 1000)
                ok = analyze(Nsteps)                            
                print(tests[i], algoritmo[j], ok)             
                if ok == 0:
                    break
            else:
                continue
            
def pushover2(Dmax,Dincr,IDctrlNode,IDctrlDOF,norm=[-1,1],Tol=1e-8):
    
    # creación del recorder de techo y definición de la tolerancia
    recorder('Node','-file','techo.out','-time','-node',IDctrlNode,'-dof',IDctrlDOF,'disp')
    maxNumIter = 10
    
      
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
    analysis('Static')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    
    Nsteps =  int(Dmax/ Dincr) 
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    Vbasal = [getTime()]
    
    for k in range(Nsteps):
        ok = analyze(1)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en desplazamiento: ',nodeDisp(IDctrlNode,IDctrlDOF))
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*50)
                ok = analyze(1)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Pushover analisis fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
    
        
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        Vbasal.append(getTime())
        
    plt.figure()
    plt.plot(dtecho,Vbasal)
    plt.xlabel('desplazamiento de techo (m)')
    plt.ylabel('corte basal (kN)')
    
    techo = np.array(dtecho)
    V = np.array(Vbasal)
    
    
    if norm[0] != -1:
        deriva = techo/norm[0]*100
        VW = V/norm[1]
        plt.figure()
        plt.plot(deriva,VW)
        plt.xlabel('Deriva de techo (%)')
        plt.ylabel('V/W')
    
    return techo, V


def pushover2MP(Dmax,Dincr,IDctrlNode,IDctrlDOF,norm=[-1,1],Tol=1e-8):
    
    # creación del recorder de techo y definición de la tolerancia
    recorder('Node','-file','techo.out','-time','-node',IDctrlNode,'-dof',IDctrlDOF,'disp')
    maxNumIter = 20
    
      
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
    analysis('Static')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    
    Nsteps =  int(Dmax/ Dincr) 
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    Vbasal = [getTime()]
    
    for k in range(Nsteps):
        ok = analyze(1)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en desplazamiento: ',nodeDisp(IDctrlNode,IDctrlDOF))
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*25)
                ok = analyze(1)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Pushover analisis fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
    
        
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        Vbasal.append(getTime())
        

    techo = np.array(dtecho)
    V = np.array(Vbasal)
    
    
    if norm[0] != -1:
        deriva = techo/norm[0]*100
        VW = V/norm[1]
        plt.figure()
        plt.plot(deriva,VW)
        plt.xlabel('Deriva de techo (%)')
        plt.ylabel('V/W')
    
    return techo, V


def pushover2T(Dmax,Dincr,IDctrlNode,IDctrlDOF,norm=[-1,1],Tol=1e-8):
    
    # creación del recorder de techo y definición de la tolerancia
    recorder('Node','-file','techo.out','-time','-node',IDctrlNode,'-dof',IDctrlDOF,'disp')
    maxNumIter = 10
    
      
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
    analysis('Static')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    eig = eigen(1)
    TT = 2*3.1416/np.sqrt(eig[0])
    Nsteps =  int(Dmax/ Dincr) 
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    Vbasal = [getTime()]
    periods = [TT]
    fibras1 = [0]*8
    for k in range(Nsteps):
        ok = analyze(1)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en desplazamiento: ',nodeDisp(IDctrlNode,IDctrlDOF))
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*50)
                ok = analyze(1)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Pushover analisis fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
        
       
        eig = eigen(1)
        TT = 2*3.1416/np.sqrt(eig[0])
        periods.append(TT)
         
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        Vbasal.append(getTime())
        
    plt.figure()
    plt.plot(dtecho,Vbasal)
    plt.xlabel('desplazamiento de techo (m)')
    plt.ylabel('corte basal (kN)')
    
    techo = np.array(dtecho)
    V = np.array(Vbasal)
    PER = np.array(periods)
    
    
    if norm[0] != -1:
        deriva = techo/norm[0]*100
        VW = V/norm[1]
        plt.figure()
        plt.plot(deriva,VW)
        plt.xlabel('Deriva de techo (%)')
        plt.ylabel('V/W')
    
    plt.figure()
    plt.plot(dtecho,periods)
    plt.xlabel('desplazamiento de techo (m)')
    plt.ylabel('Periodo (s)')
    
    return techo, V, PER

def pushover3T(Dmax,Dincr,IDctrlNode,IDctrlDOF,elements,norm=[-1,1],Tol=1e-8):
    
    # creación del recorder de techo y definición de la tolerancia
    recorder('Node','-file','techo.out','-time','-node',IDctrlNode,'-dof',IDctrlDOF,'disp')
    maxNumIter = 10
    
      
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
    analysis('Static')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    eig = eigen(1)
    TT = 2*3.1416/np.sqrt(eig[0])
    Nsteps =  int(Dmax/ Dincr) 
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    Vbasal = [getTime()]
    periods = [TT]
    
    
    nels = len(elements)
    Eds = np.zeros((nels, Nsteps+1, 6)) # para grabar las fuerzas de los elementos
    Curv = np.zeros((nels,Nsteps+1)) # para grabar la curvatura de los elementos
    # Strains = np.zeros((Nsteps+1, 8, nels)) # # para grabar las deformaciones de los muros en las 8 fibras que tienen los elementos
    Strains = np.zeros((nels, Nsteps+1, 8))
    cStress = np.zeros((nels, Nsteps+1, 8)) # # para grabar los esfuerzos del concreto de los muros en las 8 fibras que tienen los elementos
    sStress = np.zeros((nels, Nsteps+1, 8)) # # para grabar los esfuerzos del acero de los muros en las 8 fibras que tienen los elementos
    
    for k in range(Nsteps):
        ok = analyze(1)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en desplazamiento: ',nodeDisp(IDctrlNode,IDctrlDOF))
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*50)
                ok = analyze(1)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Pushover analisis fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
        
        
        for el_i, ele_tag in enumerate(elements):
            
            # Curv[k+1, el_i] = [eleResponse(ele_tag,'Curvature')]
            Eds[el_i , k+1, :] = [eleResponse(ele_tag,'globalForce')[0],
                                 eleResponse(ele_tag,'globalForce')[1],
                                 eleResponse(ele_tag,'globalForce')[2],
                                 eleResponse(ele_tag,'globalForce')[3],
                                 eleResponse(ele_tag,'globalForce')[4],
                                 eleResponse(ele_tag,'globalForce')[5]]
            
            Strains[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Strain')[0],
                                 eleResponse(ele_tag,'Fiber_Strain')[1],
                                 eleResponse(ele_tag,'Fiber_Strain')[2],
                                 eleResponse(ele_tag,'Fiber_Strain')[3],
                                 eleResponse(ele_tag,'Fiber_Strain')[4],
                                 eleResponse(ele_tag,'Fiber_Strain')[5],
                                 eleResponse(ele_tag,'Fiber_Strain')[6],
                                 eleResponse(ele_tag,'Fiber_Strain')[7]]
            
            cStress[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Stress_Concrete')[0],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[1],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[2],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[3],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[4],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[5],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[6],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[7]]
            
            sStress[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Stress_Steel')[0],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[1],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[2],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[3],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[4],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[5],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[6],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[7]]
        
        eig = eigen(1)
        TT = 2*3.1416/np.sqrt(eig[0])
        periods.append(TT)
         
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        Vbasal.append(getTime())
        
    plt.figure()
    plt.plot(dtecho,Vbasal)
    plt.xlabel('desplazamiento de techo (m)')
    plt.ylabel('corte basal (kN)')
    
    techo = np.array(dtecho)
    V = np.array(Vbasal)
    PER = np.array(periods)
    
    
    if norm[0] != -1:
        deriva = techo/norm[0]*100
        VW = V/norm[1]
        plt.figure()
        plt.plot(deriva,VW)
        plt.xlabel('Deriva de techo (%)')
        plt.ylabel('V/W')
    
    plt.figure()
    plt.plot(dtecho,periods)
    plt.xlabel('desplazamiento de techo (m)')
    plt.ylabel('Periodo (s)')
    
    return techo, V, PER, Eds, Strains, cStress, sStress



def pushover3Tn(Dmax,Dincr,IDctrlNode,IDctrlDOF,elements,norm=[-1,1],Tol=1e-8):
    
    # creación del recorder de techo y definición de la tolerancia
    recorder('Node','-file','techo.out','-time','-node',IDctrlNode,'-dof',IDctrlDOF,'disp')
    maxNumIter = 10
    
      
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
    analysis('Static')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    eig = eigen(1)
    TT = 2*3.1416/np.sqrt(eig[0])
    Nsteps =  int(Dmax/ Dincr) 
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    Vbasal = [getTime()]
    periods = [TT]
    
    
    nels = len(elements)
    Eds = np.zeros((nels, Nsteps+1, 6)) # para grabar las fuerzas de los elementos
    Curv = np.zeros((nels,Nsteps+1)) # para grabar la curvatura de los elementos
    # Strains = np.zeros((Nsteps+1, 8, nels)) # # para grabar las deformaciones de los muros en las 8 fibras que tienen los elementos
    Strains = np.zeros((nels, Nsteps+1, 14))
    cStress = np.zeros((nels, Nsteps+1, 14)) # # para grabar los esfuerzos del concreto de los muros en las 8 fibras que tienen los elementos
    sStress = np.zeros((nels, Nsteps+1, 14)) # # para grabar los esfuerzos del acero de los muros en las 8 fibras que tienen los elementos
    
    for k in range(Nsteps):
        ok = analyze(1)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en desplazamiento: ',nodeDisp(IDctrlNode,IDctrlDOF))
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*50)
                ok = analyze(1)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Pushover analisis fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
        
        
        for el_i, ele_tag in enumerate(elements):
            
            # Curv[k+1, el_i] = [eleResponse(ele_tag,'Curvature')]
            Eds[el_i , k+1, :] = [eleResponse(ele_tag,'globalForce')[0],
                                 eleResponse(ele_tag,'globalForce')[1],
                                 eleResponse(ele_tag,'globalForce')[2],
                                 eleResponse(ele_tag,'globalForce')[3],
                                 eleResponse(ele_tag,'globalForce')[4],
                                 eleResponse(ele_tag,'globalForce')[5]]
            
            Strains[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Strain')[0],
                                 eleResponse(ele_tag,'Fiber_Strain')[1],
                                 eleResponse(ele_tag,'Fiber_Strain')[2],
                                 eleResponse(ele_tag,'Fiber_Strain')[3],
                                 eleResponse(ele_tag,'Fiber_Strain')[4],
                                 eleResponse(ele_tag,'Fiber_Strain')[5],
                                 eleResponse(ele_tag,'Fiber_Strain')[6],
                                 eleResponse(ele_tag,'Fiber_Strain')[7],
                                 eleResponse(ele_tag,'Fiber_Strain')[8],
                                 eleResponse(ele_tag,'Fiber_Strain')[9],
                                 eleResponse(ele_tag,'Fiber_Strain')[10],
                                 eleResponse(ele_tag,'Fiber_Strain')[11],
                                 eleResponse(ele_tag,'Fiber_Strain')[12],
                                 eleResponse(ele_tag,'Fiber_Strain')[13]]
                                 
            
            cStress[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Stress_Concrete')[0],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[1],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[2],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[3],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[4],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[5],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[6],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[7],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[8],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[9],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[10],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[11],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[12],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[13]]
                                 
            
            sStress[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Stress_Steel')[0],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[1],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[2],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[3],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[4],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[5],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[6],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[7],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[8],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[9],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[10],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[11],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[12],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[13]]


        eig = eigen(1)
        TT = 2*3.1416/np.sqrt(eig[0])
        periods.append(TT)
         
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        Vbasal.append(getTime())
        
    plt.figure()
    plt.plot(dtecho,Vbasal)
    plt.xlabel('desplazamiento de techo (m)')
    plt.ylabel('corte basal (kN)')
    
    techo = np.array(dtecho)
    V = np.array(Vbasal)
    PER = np.array(periods)
    
    
    if norm[0] != -1:
        deriva = techo/norm[0]*100
        VW = V/norm[1]
        plt.figure()
        plt.plot(deriva,VW)
        plt.xlabel('Deriva de techo (%)')
        plt.ylabel('V/W')
    
    plt.figure()
    plt.plot(dtecho,periods)
    plt.xlabel('desplazamiento de techo (m)')
    plt.ylabel('Periodo (s)')
    
    return techo, V, PER, Eds, Strains, cStress, sStress


# ANALISIS DINAMICO
# =============================   

# dinamico es el más sencillo de todos, corre un terremoto creando un recorder para el techo.
# dinamicoIDA crea el recorder en función del factor escalar.
# dinamicoAnim es dinamico pero guarda la información para animar el registro
# dinamicoIDA2 está modificado para ser utilizado cuando se desee correr en paralelo los cálculos. Devuelve solo el desplazamiento de techo
# dinamicoIDA3 PARA SER UTILIZADO PARA CORRER EN PARALELO LOS SISMOS Y EXTRAYENDO LAS FUERZAS DE LOS ELEMENTOS INDICADOS EN ELEMENTS. SOLO PUEDEN SER LOS MUROS DE MOMENTO. También extrae desplazamientos de los nodos
# dinamicoIDA4 PARA SER UTILIZADO PARA CORRER EN PARALELO LOS SISMOS Y EXTRAYENDO LAS FUERZAS DE LOS ELEMENTOS INDICADOS EN ELEMENTS. SOLO PUEDEN SER LOS MUROS DE MOMENTO. También extrae desplazamientos de los nodos, aceleraciones, derivas, velocidades, esfuerzos en concreto, acero y deformaciones unitarias de cada muro indicado en elements
# dinamicoIDA5 es lo mismo que IDA4, pero en lugar del nombre del registro, recibe una lista con las aceleraciones.

def dinamico(recordName,dtrec,nPts,dtan,fact,damp,IDctrlNode,IDctrlDOF,modes = [0,2],Kswitch = 1,Tol=1e-4):
    
    # record es el nombre del registro, incluyendo extensión. P.ej. GM01.txt
    # dtrec es el dt del registro
    # nPts es el número de puntos del análisis
    # dtan es el dt del análisis
    # fact es el factor escalar del registro
    # damp es el porcentaje de amortiguamiento (EN DECIMAL. p.ej: 0.03 para 3%)
    # Kswitch recibe: 1: matriz inicial, 2: matriz actual
    # IDctrlNode,IDctrlDOF son respectivamente el nodo y desplazamiento de control deseados
    
    # creación del recorder de techo y definición de la tolerancia
    recorder('Node','-file','techo.out','-time','-node',IDctrlNode,'-dof',IDctrlDOF,'disp')
    maxNumIter = 25
    
    # creación del pattern
    
    timeSeries('Path',1000,'-filePath',recordName,'-dt',dtrec,'-factor',fact)
    pattern('UniformExcitation',  1000,   1,  '-accel', 1000)
    
    # damping
    nmodes = max(modes)+1
    eigval = eigen(nmodes)
    
    eig1 = eigval[modes[0]]
    eig2 = eigval[modes[1]]
    
    w1 = eig1**0.5
    w2 = eig2**0.5
    
    beta = 2.0*damp/(w1 + w2)
    alfa = 2.0*damp*w1*w2/(w1 + w2)
    
    if Kswitch == 1:
        rayleigh(alfa, 0.0, beta, 0.0)
    else:
        rayleigh(alfa, beta, 0.0, 0.0)
    
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('NormDispIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('Newmark', 0.5, 0.25)
    analysis('Transient')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    
    Nsteps =  int(dtrec*nPts/dtan)
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    t = [getTime()]
    
    for k in range(Nsteps):
        ok = analyze(1,dtan)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en desplazamiento: ',nodeDisp(IDctrlNode,IDctrlDOF))
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('NormDispIncr', Tol, maxNumIter*50)
                ok = analyze(1,dtan)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('NormDispIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Análisis dinámico fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
    
        
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        t.append(getTime())
        
    # plt.figure()
    # plt.plot(t,dtecho)
    # plt.xlabel('tiempo (s)')
    # plt.ylabel('desplazamiento (m)')  
    
    techo = np.array(dtecho)
    tiempo = np.array(t)
    
    
    
    return tiempo,techo
     
def dinamicoIDA(recordName,dtrec,nPts,dtan,fact,damp,IDctrlNode,IDctrlDOF,modes = [0,2],Kswitch = 1,Tol=1e-4):
    
    # modelName
    # record es el nombre del registro, incluyendo extensión. P.ej. GM01.txt
    # dtrec es el dt del registro
    # nPts es el número de puntos del análisis
    # dtan es el dt del análisis
    # fact es el factor escalar del registro
    # damp es el porcentaje de amortiguamiento (EN DECIMAL. p.ej: 0.03 para 3%)
    # Kswitch recibe: 1: matriz inicial, 2: matriz actual
    # IDctrlNode,IDctrlDOF son respectivamente el nodo y desplazamiento de control deseados
     # creación del recorder de techo y definición de la tolerancia
    # nombre = str(int(fact/9.81*100))
    # recorder('Node','-file','techo'+nombre+'.out','-time','-node',IDctrlNode,'-dof',IDctrlDOF,'disp')
    maxNumIter = 25
    
    # creación del pattern
    
    timeSeries('Path',1000,'-filePath',recordName,'-dt',dtrec,'-factor',fact)
    pattern('UniformExcitation',  1000,   1,  '-accel', 1000)
    
    # damping
    nmodes = max(modes)+1
    eigval = eigen(nmodes)
    
    eig1 = eigval[modes[0]]
    eig2 = eigval[modes[1]]
    
    w1 = eig1**0.5
    w2 = eig2**0.5
    
    beta = 2.0*damp/(w1 + w2)
    alfa = 2.0*damp*w1*w2/(w1 + w2)
    
    if Kswitch == 1:
        rayleigh(alfa, 0.0, beta, 0.0)
    else:
        rayleigh(alfa, beta, 0.0, 0.0)
    
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('NormDispIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('Newmark', 0.5, 0.25)
    analysis('Transient')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    
    Nsteps =  int(dtrec*nPts/dtan)
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    t = [getTime()]
    
    for k in range(Nsteps):
        ok = analyze(1,dtan)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en tiempo: ',getTime())
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('NormDispIncr', Tol, maxNumIter*50)
                ok = analyze(1,dtan)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('NormDispIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Análisis dinámico fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
    
        
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        t.append(getTime())
        
    # plt.figure()
    # plt.plot(t,dtecho)
    # plt.xlabel('tiempo (s)')
    # plt.ylabel('desplazamiento (m)')
    
    # techo = np.array(dtecho)
    # tiempo = np.array(t)
    wipe()
   
def dinamicoAnim(recordName,dtrec,nPts,dtan,fact,damp,IDctrlNode,IDctrlDOF,modes = [0,2],Kswitch = 1,Tol=1e-8):
    
    # record es el nombre del registro, incluyendo extensión. P.ej. GM01.txt
    # dtrec es el dt del registro
    # nPts es el número de puntos del análisis
    # dtan es el dt del análisis
    # fact es el factor escalar del registro
    # damp es el porcentaje de amortiguamiento (EN DECIMAL. p.ej: 0.03 para 3%)
    # Kswitch recibe: 1: matriz inicial, 2: matriz actual
    # IDctrlNode,IDctrlDOF son respectivamente el nodo y desplazamiento de control deseados
    
    # creación del recorder de techo y definición de la tolerancia
    recorder('Node','-file','techo.out','-time','-node',IDctrlNode,'-dof',IDctrlDOF,'disp')
    maxNumIter = 10
    
    # creación del pattern
    
    timeSeries('Path',1000,'-filePath',recordName,'-dt',dtrec,'-factor',fact)
    pattern('UniformExcitation',  1000,   1,  '-accel', 1000)
    
    # damping
    nmodes = max(modes)+1
    eigval = eigen(nmodes)
    
    eig1 = eigval[modes[0]]
    eig2 = eigval[modes[1]]
    
    w1 = eig1**0.5
    w2 = eig2**0.5
    
    beta = 2.0*damp/(w1 + w2)
    alfa = 2.0*damp*w1*w2/(w1 + w2)
    
    if Kswitch == 1:
        rayleigh(alfa, 0.0, beta, 0.0)
    else:
        rayleigh(alfa, beta, 0.0, 0.0)
    
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('Newmark', 0.5, 0.25)
    analysis('Transient')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    
    Nsteps =  int(dtrec*nPts/dtan)
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    t = [getTime()]
    el_tags = getEleTags()
    nels = len(el_tags)
    Eds = np.zeros((Nsteps+1, nels, 6))
    
    
    for k in range(Nsteps):
        ok = analyze(1,dtan)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en desplazamiento: ',nodeDisp(IDctrlNode,IDctrlDOF))
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*50)
                ok = analyze(1,dtan)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Análisis dinámico fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
    
        for el_i, ele_tag in enumerate(el_tags):
            nd1, nd2 = eleNodes(ele_tag)
            Eds[k+1, el_i, :] = [nodeDisp(nd1)[0],
                                  nodeDisp(nd1)[1],
                                  nodeDisp(nd1)[2],
                                  nodeDisp(nd2)[0],
                                  nodeDisp(nd2)[1],
                                  nodeDisp(nd2)[2]]
        
        
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        t.append(getTime())
        
    plt.figure()
    plt.plot(t,dtecho)
    plt.xlabel('tiempo (s)')
    plt.ylabel('desplazamiento (m)')  
    
    techo = np.array(dtecho)
    tiempo = np.array(t)
    
    return tiempo,techo,Eds
    
def dinamicoIDA2(recordName,dtrec,nPts,dtan,fact,damp,IDctrlNode,IDctrlDOF,modes = [0,2],Kswitch = 1,Tol=1e-8):
    
    # PARA SER UTILIZADO PARA CORRER EN PARALELO LOS SISMOS
    
    # record es el nombre del registro, incluyendo extensión. P.ej. GM01.txt
    # dtrec es el dt del registro
    # nPts es el número de puntos del análisis
    # dtan es el dt del análisis
    # fact es el factor escalar del registro
    # damp es el porcentaje de amortiguamiento (EN DECIMAL. p.ej: 0.03 para 3%)
    # Kswitch recibe: 1: matriz inicial, 2: matriz actual
    
    maxNumIter = 10
    
    # creación del pattern
    
    timeSeries('Path',1000,'-filePath',recordName,'-dt',dtrec,'-factor',fact)
    pattern('UniformExcitation',  1000,   1,  '-accel', 1000)
    
    # damping
    nmodes = max(modes)+1
    eigval = eigen(nmodes)
    
    eig1 = eigval[modes[0]]
    eig2 = eigval[modes[1]]
    
    w1 = eig1**0.5
    w2 = eig2**0.5
    
    beta = 2.0*damp/(w1 + w2)
    alfa = 2.0*damp*w1*w2/(w1 + w2)
    
    if Kswitch == 1:
        rayleigh(alfa, 0.0, beta, 0.0)
    else:
        rayleigh(alfa, beta, 0.0, 0.0)
    
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('Newmark', 0.5, 0.25)
    analysis('Transient')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    
    Nsteps =  int(dtrec*nPts/dtan)
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    t = [getTime()]
    
    for k in range(Nsteps):
        ok = analyze(1,dtan)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en tiempo: ',getTime())
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*50)
                ok = analyze(1,dtan)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Análisis dinámico fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
    
        
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        t.append(getTime())
        
    # plt.figure()
    # plt.plot(t,dtecho)
    # plt.xlabel('tiempo (s)')
    # plt.ylabel('desplazamiento (m)')
    
    techo = np.array(dtecho)
    tiempo = np.array(t)
    wipe()
    return tiempo,techo


def dinamicoIDA3(recordName,dtrec,nPts,dtan,fact,damp,IDctrlNode,IDctrlDOF,elements,modes = [0,2],Kswitch = 1,Tol=1e-8):
    
    # PARA SER UTILIZADO PARA CORRER EN PARALELO LOS SISMOS Y EXTRAYENDO LAS FUERZAS DE LOS ELEMENTOS INDICADOS EN ELEMENTS
    
    # record es el nombre del registro, incluyendo extensión. P.ej. GM01.txt
    # dtrec es el dt del registro
    # nPts es el número de puntos del análisis
    # dtan es el dt del análisis
    # fact es el factor escalar del registro
    # damp es el porcentaje de amortiguamiento (EN DECIMAL. p.ej: 0.03 para 3%)
    # IDcrtlNode es el nodo de control para grabar desplazamientos
    # IDctrlDOF es el grado de libertad de control
    # elements son los elementos de los que se va a grabar información
    # nodes_control son los nodos donde se va a grabar las respuestas
    # Kswitch recibe: 1: matriz inicial, 2: matriz actual
    
    maxNumIter = 10
    
    # creación del pattern
    
    timeSeries('Path',1000,'-filePath',recordName,'-dt',dtrec,'-factor',fact)
    pattern('UniformExcitation',  1000,   1,  '-accel', 1000)
    
    # damping
    nmodes = max(modes)+1
    eigval = eigen(nmodes)
    
    eig1 = eigval[modes[0]]
    eig2 = eigval[modes[1]]
    
    w1 = eig1**0.5
    w2 = eig2**0.5
    
    beta = 2.0*damp/(w1 + w2)
    alfa = 2.0*damp*w1*w2/(w1 + w2)
    
    if Kswitch == 1:
        rayleigh(alfa, 0.0, beta, 0.0)
    else:
        rayleigh(alfa, beta, 0.0, 0.0)
    
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('Newmark', 0.5, 0.25)
    analysis('Transient')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    
    Nsteps =  int(dtrec*nPts/dtan)
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    t = [getTime()]
    nels = len(elements)
    # nnodos = len(nodes_control)
    Eds = np.zeros((nels, Nsteps+1, 6)) # para grabar las fuerzas de los elementos
    Curv = np.zeros((nels,Nsteps+1)) # para grabar la curvatura de los elementos
    # Strains = np.zeros((Nsteps+1, 8, nels)) # # para grabar las deformaciones de los muros en las 8 fibras que tienen los elementos
    Strains = np.zeros((nels, Nsteps+1, 8))
    cStress = np.zeros((nels, Nsteps+1, 8)) # # para grabar los esfuerzos del concreto de los muros en las 8 fibras que tienen los elementos
    sStress = np.zeros((nels, Nsteps+1, 8)) # # para grabar los esfuerzos del acero de los muros en las 8 fibras que tienen los elementos
    # node_disp = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    # node_vel = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    # node_acel = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    
    for k in range(Nsteps):
        ok = analyze(1,dtan)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en tiempo: ',getTime())
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*50)
                ok = analyze(1,dtan)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Análisis dinámico fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
        
        # for node_i, node_tag in enumerate(nodes_control):
            
        #     node_disp[k+1,node_i] = nodeDisp(node_tag,1)
        #     node_disp[k+1,node_i] = nodeDisp(node_tag,1)
                           
        
        
        
        for el_i, ele_tag in enumerate(elements):
            
            # Curv[k+1, el_i] = [eleResponse(ele_tag,'Curvature')]
            Eds[el_i , k+1, :] = [eleResponse(ele_tag,'globalForce')[0],
                                 eleResponse(ele_tag,'globalForce')[1],
                                 eleResponse(ele_tag,'globalForce')[2],
                                 eleResponse(ele_tag,'globalForce')[3],
                                 eleResponse(ele_tag,'globalForce')[4],
                                 eleResponse(ele_tag,'globalForce')[5]]
            
            Strains[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Strain')[0],
                                 eleResponse(ele_tag,'Fiber_Strain')[1],
                                 eleResponse(ele_tag,'Fiber_Strain')[2],
                                 eleResponse(ele_tag,'Fiber_Strain')[3],
                                 eleResponse(ele_tag,'Fiber_Strain')[4],
                                 eleResponse(ele_tag,'Fiber_Strain')[5],
                                 eleResponse(ele_tag,'Fiber_Strain')[6],
                                 eleResponse(ele_tag,'Fiber_Strain')[7]]
            
            cStress[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Stress_Concrete')[0],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[1],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[2],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[3],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[4],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[5],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[6],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[7]]
            
            sStress[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Stress_Steel')[0],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[1],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[2],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[3],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[4],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[5],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[6],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[7]]
            
            
            
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        t.append(getTime())
        
    # plt.figure()
    # plt.plot(t,dtecho)
    # plt.xlabel('tiempo (s)')
    # plt.ylabel('desplazamiento (m)')
    
    techo = np.array(dtecho)
    tiempo = np.array(t)
    wipe()
    return tiempo,techo,Eds,Strains,cStress,sStress


def dinamicoIDA4(recordName,dtrec,nPts,dtan,fact,damp,IDctrlNode,IDctrlDOF,elements,nodes_control,modes = [0,2],Kswitch = 1,Tol=1e-8):
    
    # PARA SER UTILIZADO PARA CORRER EN PARALELO LOS SISMOS Y EXTRAYENDO LAS FUERZAS DE LOS ELEMENTOS INDICADOS EN ELEMENTS
    
    # record es el nombre del registro, incluyendo extensión. P.ej. GM01.txt
    # dtrec es el dt del registro
    # nPts es el número de puntos del análisis
    # dtan es el dt del análisis
    # fact es el factor escalar del registro
    # damp es el porcentaje de amortiguamiento (EN DECIMAL. p.ej: 0.03 para 3%)
    # IDcrtlNode es el nodo de control para grabar desplazamientos
    # IDctrlDOF es el grado de libertad de control
    # elements son los elementos de los que se va a grabar información
    # nodes_control son los nodos donde se va a grabar las respuestas
    # Kswitch recibe: 1: matriz inicial, 2: matriz actual
    
    maxNumIter = 10
    
    # creación del pattern
    
    timeSeries('Path',1000,'-filePath',recordName,'-dt',dtrec,'-factor',fact)
    pattern('UniformExcitation',  1000,   1,  '-accel', 1000)
    
    # damping
    nmodes = max(modes)+1
    eigval = eigen(nmodes)
    
    eig1 = eigval[modes[0]]
    eig2 = eigval[modes[1]]
    
    w1 = eig1**0.5
    w2 = eig2**0.5
    
    beta = 2.0*damp/(w1 + w2)
    alfa = 2.0*damp*w1*w2/(w1 + w2)
    
    if Kswitch == 1:
        rayleigh(alfa, 0.0, beta, 0.0)
    else:
        rayleigh(alfa, beta, 0.0, 0.0)
    
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('Newmark', 0.5, 0.25)
    analysis('Transient')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    
    Nsteps =  int(dtrec*nPts/dtan)
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    t = [getTime()]
    nels = len(elements)
    nnodos = len(nodes_control)
    Eds = np.zeros((nels, Nsteps+1, 6)) # para grabar las fuerzas de los elementos
    Curv = np.zeros((nels,Nsteps+1)) # para grabar la curvatura de los elementos
    
    Strains = np.zeros((nels, Nsteps+1, 8))
    cStress = np.zeros((nels, Nsteps+1, 8)) # # para grabar los esfuerzos del concreto de los muros en las 8 fibras que tienen los elementos
    sStress = np.zeros((nels, Nsteps+1, 8)) # # para grabar los esfuerzos del acero de los muros en las 8 fibras que tienen los elementos
    node_disp = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    node_vel = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    node_acel = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    drift = np.zeros((Nsteps + 1, nnodos - 1)) # para grabar la deriva de entrepiso
    
    for k in range(Nsteps):
        ok = analyze(1,dtan)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en tiempo: ',getTime())
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*50)
                ok = analyze(1,dtan)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Análisis dinámico fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
        
        for node_i, node_tag in enumerate(nodes_control):
            
            node_disp[k+1,node_i] = nodeDisp(node_tag,1)
            node_vel[k+1,node_i] = nodeVel(node_tag,1)
            node_acel[k+1,node_i] = nodeAccel(node_tag,1)
            if node_i != 0:
                drift[k+1,node_i-1] = (nodeDisp(node_tag,1) - nodeDisp(nodes_control[node_i-1],1))/(nodeCoord(node_tag,2) - nodeCoord(nodes_control[node_i-1],2))
                       

        for el_i, ele_tag in enumerate(elements):
            
            # Curv[k+1, el_i] = [eleResponse(ele_tag,'Curvature')]
            Eds[el_i , k+1, :] = [eleResponse(ele_tag,'globalForce')[0],
                                 eleResponse(ele_tag,'globalForce')[1],
                                 eleResponse(ele_tag,'globalForce')[2],
                                 eleResponse(ele_tag,'globalForce')[3],
                                 eleResponse(ele_tag,'globalForce')[4],
                                 eleResponse(ele_tag,'globalForce')[5]]
            
            Strains[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Strain')[0],
                                 eleResponse(ele_tag,'Fiber_Strain')[1],
                                 eleResponse(ele_tag,'Fiber_Strain')[2],
                                 eleResponse(ele_tag,'Fiber_Strain')[3],
                                 eleResponse(ele_tag,'Fiber_Strain')[4],
                                 eleResponse(ele_tag,'Fiber_Strain')[5],
                                 eleResponse(ele_tag,'Fiber_Strain')[6],
                                 eleResponse(ele_tag,'Fiber_Strain')[7]]
            
            cStress[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Stress_Concrete')[0],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[1],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[2],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[3],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[4],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[5],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[6],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[7]]
            
            sStress[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Stress_Steel')[0],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[1],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[2],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[3],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[4],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[5],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[6],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[7]]
            
            
            
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        t.append(getTime())
        
    # plt.figure()
    # plt.plot(t,dtecho)
    # plt.xlabel('tiempo (s)')
    # plt.ylabel('desplazamiento (m)')
    
    techo = np.array(dtecho)
    tiempo = np.array(t)
    wipe()
    return tiempo,techo,Eds,Strains,cStress,sStress,node_disp,node_vel,node_acel,drift


def dinamicoIDA4P(recordName,dtrec,nPts,dtan,fact,damp,IDctrlNode,IDctrlDOF,elements,nodes_control,modes = [0,2],Kswitch = 1,Tol=1e-8):
    
    # PARA SER UTILIZADO PARA CORRER EN PARALELO LOS SISMOS Y EXTRAYENDO LAS FUERZAS DE LOS ELEMENTOS INDICADOS EN ELEMENTS
    
    # record es el nombre del registro, incluyendo extensión. P.ej. GM01.txt
    # dtrec es el dt del registro
    # nPts es el número de puntos del análisis
    # dtan es el dt del análisis
    # fact es el factor escalar del registro
    # damp es el porcentaje de amortiguamiento (EN DECIMAL. p.ej: 0.03 para 3%)
    # IDcrtlNode es el nodo de control para grabar desplazamientos
    # IDctrlDOF es el grado de libertad de control
    # elements son los elementos de los que se va a grabar información
    # nodes_control son los nodos donde se va a grabar las respuestas
    # Kswitch recibe: 1: matriz inicial, 2: matriz actual
    
    maxNumIter = 10
    
    # creación del pattern
    
    timeSeries('Path',1000,'-filePath',recordName,'-dt',dtrec,'-factor',fact)
    pattern('UniformExcitation',  1000,   1,  '-accel', 1000)
    
    # damping
    nmodes = max(modes)+1
    eigval = eigen(nmodes)
    
    eig1 = eigval[modes[0]]
    eig2 = eigval[modes[1]]
    
    w1 = eig1**0.5
    w2 = eig2**0.5
    
    beta = 2.0*damp/(w1 + w2)
    alfa = 2.0*damp*w1*w2/(w1 + w2)
    
    if Kswitch == 1:
        rayleigh(alfa, 0.0, beta, 0.0)
    else:
        rayleigh(alfa, beta, 0.0, 0.0)
    
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('Newmark', 0.5, 0.25)
    analysis('Transient')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    
    Nsteps =  int(dtrec*nPts/dtan)
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    t = [getTime()]
    nels = len(elements)
    nnodos = len(nodes_control)
    Eds = np.zeros((nels, Nsteps+1, 6)) # para grabar las fuerzas de los elementos
    
    
    
    node_disp = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    node_vel = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    node_acel = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    drift = np.zeros((Nsteps + 1, nnodos - 1)) # para grabar la deriva de entrepiso
    
    for k in range(Nsteps):
        ok = analyze(1,dtan)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            # print('configuración por defecto no converge en tiempo: ',getTime())
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*50)
                ok = analyze(1,dtan)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            # print('Análisis dinámico fallido')
            # print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
        
        for node_i, node_tag in enumerate(nodes_control):
            
            node_disp[k+1,node_i] = nodeDisp(node_tag,1)
            node_vel[k+1,node_i] = nodeVel(node_tag,1)
            node_acel[k+1,node_i] = nodeAccel(node_tag,1)
            if node_i != 0:
                drift[k+1,node_i-1] = (nodeDisp(node_tag,1) - nodeDisp(nodes_control[node_i-1],1))/(nodeCoord(node_tag,2) - nodeCoord(nodes_control[node_i-1],2))
                       

        for el_i, ele_tag in enumerate(elements):
                      
            Eds[el_i , k+1, :] = [eleResponse(ele_tag,'globalForce')[0],
                                 eleResponse(ele_tag,'globalForce')[1],
                                 eleResponse(ele_tag,'globalForce')[2],
                                 eleResponse(ele_tag,'globalForce')[3],
                                 eleResponse(ele_tag,'globalForce')[4],
                                 eleResponse(ele_tag,'globalForce')[5]]
            
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        t.append(getTime())
        
    # plt.figure()
    # plt.plot(t,dtecho)
    # plt.xlabel('tiempo (s)')
    # plt.ylabel('desplazamiento (m)')
    
    techo = np.array(dtecho)
    tiempo = np.array(t)
    wipe()
    return tiempo,techo,Eds,node_disp,node_vel,node_acel,drift

def dinamicoIDA5(acceleration,dtrec,nPts,dtan,fact,damp,IDctrlNode,IDctrlDOF,elements,nodes_control,modes = [0,2],Kswitch = 1,Tol=1e-8):
    
    # PARA SER UTILIZADO PARA CORRER EN PARALELO LOS SISMOS Y EXTRAYENDO LAS FUERZAS DE LOS ELEMENTOS INDICADOS EN ELEMENTS
    
    # acceleration es la lista de aceleraciones del registro. Se termina multiplicando por fact
    # dtrec es el dt del registro
    # nPts es el número de puntos del análisis
    # dtan es el dt del análisis
    # fact es el factor escalar del registro
    # damp es el porcentaje de amortiguamiento (EN DECIMAL. p.ej: 0.03 para 3%)
    # IDcrtlNode es el nodo de control para grabar desplazamientos
    # IDctrlDOF es el grado de libertad de control
    # elements son los elementos de los que se va a grabar información
    # nodes_control son los nodos donde se va a grabar las respuestas
    # Kswitch recibe: 1: matriz inicial, 2: matriz actual
    
    maxNumIter = 10
    
    # creación del pattern
    
    timeSeries('Path',1000,'-values',*acceleration,'-dt',dtrec,'-factor',fact)
    pattern('UniformExcitation',  1000,   1,  '-accel', 1000)
    
    # damping
    nmodes = max(modes)+1
    eigval = eigen(nmodes)
    
    eig1 = eigval[modes[0]]
    eig2 = eigval[modes[1]]
    
    w1 = eig1**0.5
    w2 = eig2**0.5
    
    beta = 2.0*damp/(w1 + w2)
    alfa = 2.0*damp*w1*w2/(w1 + w2)
    
    if Kswitch == 1:
        rayleigh(alfa, 0.0, beta, 0.0)
    else:
        rayleigh(alfa, beta, 0.0, 0.0)
    
    # configuración básica del análisis
    wipeAnalysis()
    constraints('Plain')
    numberer('RCM')
    system('BandGeneral')
    test('EnergyIncr', Tol, maxNumIter)
    algorithm('Newton')    
    integrator('Newmark', 0.5, 0.25)
    analysis('Transient')
    
    # Otras opciones de análisis    
    tests = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
    algoritmo = {1:'KrylovNewton', 2: 'SecantNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

    # rutina del análisis
    
    Nsteps =  int(dtrec*nPts/dtan)
    dtecho = [nodeDisp(IDctrlNode,IDctrlDOF)]
    t = [getTime()]
    nels = len(elements)
    nnodos = len(nodes_control)
    Eds = np.zeros((nels, Nsteps+1, 6)) # para grabar las fuerzas de los elementos
    Curv = np.zeros((nels,Nsteps+1)) # para grabar la curvatura de los elementos
    
    Strains = np.zeros((nels, Nsteps+1, 8))
    cStress = np.zeros((nels, Nsteps+1, 8)) # # para grabar los esfuerzos del concreto de los muros en las 8 fibras que tienen los elementos
    sStress = np.zeros((nels, Nsteps+1, 8)) # # para grabar los esfuerzos del acero de los muros en las 8 fibras que tienen los elementos
    node_disp = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    node_vel = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    node_acel = np.zeros((Nsteps + 1, nnodos)) # para grabar los desplazamientos de los nodos
    drift = np.zeros((Nsteps + 1, nnodos - 1)) # para grabar la deriva de entrepiso
    
    for k in range(Nsteps):
        ok = analyze(1,dtan)
        # ok2 = ok;
        # En caso de no converger en un paso entra al condicional que sigue
        if ok != 0:
            print('configuración por defecto no converge en tiempo: ',getTime())
            for j in algoritmo:
                if j < 4:
                    algorithm(algoritmo[j], '-initial')
    
                else:
                    algorithm(algoritmo[j])
                
                # el test se hace 50 veces más
                test('EnergyIncr', Tol, maxNumIter*50)
                ok = analyze(1,dtan)
                if ok == 0:
                    # si converge vuelve a las opciones iniciales de análisi
                    test('EnergyIncr', Tol, maxNumIter)
                    algorithm('Newton')
                    break
                    
        if ok != 0:
            print('Análisis dinámico fallido')
            print('Desplazamiento alcanzado: ',nodeDisp(IDctrlNode,IDctrlDOF),'m')
            break
        
        for node_i, node_tag in enumerate(nodes_control):
            
            node_disp[k+1,node_i] = nodeDisp(node_tag,1)
            node_vel[k+1,node_i] = nodeVel(node_tag,1)
            node_acel[k+1,node_i] = nodeAccel(node_tag,1)
            if node_i != 0:
                drift[k+1,node_i-1] = (nodeDisp(node_tag,1) - nodeDisp(nodes_control[node_i-1],1))/(nodeCoord(node_tag,2) - nodeCoord(nodes_control[node_i-1],2))
                       

        for el_i, ele_tag in enumerate(elements):
            
            # Curv[k+1, el_i] = [eleResponse(ele_tag,'Curvature')]
            Eds[el_i , k+1, :] = [eleResponse(ele_tag,'globalForce')[0],
                                 eleResponse(ele_tag,'globalForce')[1],
                                 eleResponse(ele_tag,'globalForce')[2],
                                 eleResponse(ele_tag,'globalForce')[3],
                                 eleResponse(ele_tag,'globalForce')[4],
                                 eleResponse(ele_tag,'globalForce')[5]]
            
            Strains[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Strain')[0],
                                 eleResponse(ele_tag,'Fiber_Strain')[1],
                                 eleResponse(ele_tag,'Fiber_Strain')[2],
                                 eleResponse(ele_tag,'Fiber_Strain')[3],
                                 eleResponse(ele_tag,'Fiber_Strain')[4],
                                 eleResponse(ele_tag,'Fiber_Strain')[5],
                                 eleResponse(ele_tag,'Fiber_Strain')[6],
                                 eleResponse(ele_tag,'Fiber_Strain')[7]]
            
            cStress[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Stress_Concrete')[0],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[1],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[2],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[3],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[4],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[5],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[6],
                                 eleResponse(ele_tag,'Fiber_Stress_Concrete')[7]]
            
            sStress[el_i , k+1, :] = [eleResponse(ele_tag,'Fiber_Stress_Steel')[0],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[1],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[2],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[3],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[4],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[5],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[6],
                                 eleResponse(ele_tag,'Fiber_Stress_Steel')[7]]
            
            
            
        dtecho.append(nodeDisp(IDctrlNode,IDctrlDOF))
        t.append(getTime())
        
    # plt.figure()
    # plt.plot(t,dtecho)
    # plt.xlabel('tiempo (s)')
    # plt.ylabel('desplazamiento (m)')
    
    techo = np.array(dtecho)
    tiempo = np.array(t)
    wipe()
    return tiempo,techo,Eds,Strains,cStress,sStress,node_disp,node_vel,node_acel,drift