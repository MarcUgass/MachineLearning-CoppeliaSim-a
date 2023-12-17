#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import vrep
from parametros import instancia
import matplotlib.pyplot as plt
import json
import os
import glob
import sys
import cv2
import numpy as np


def capturar(path, clientID):
    
    #Guardar la referencia del robot
    _, robothandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
    
    #Guardar la referencia de la camara
    _, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
    
    #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)
       
    # obtenermos la referencia a la persona Bill para moverla    
    _, personhandle = vrep.simxGetObjectHandle(clientID, 'Bill#0', vrep.simx_opmode_oneshot_wait)
        
       
    #Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
    plt.axis('equal')
    plt.axis([0, 4, -2, 2])
    
    print("Directorio de trabajo es: ", os.getcwd())
    
    partes = path.split("/")
    parte1 = partes[0]
    parte2 = partes[1].split(".")[0]
    
    listaDir=sorted(glob.glob(parte1))

    nuevoDir=parte1+str(len(listaDir))

    if (os.path.isdir(nuevoDir)):
        sys.exit("Error: ya existe el directorio "+ nuevoDir)
    else:
        os.mkdir(nuevoDir)
        os.chdir(nuevoDir)
        print("Cambiando el directorio de trabajo: ", os.getcwd())
    
    cabecera={"TiempoSleep":time.sleep(0.5),
              "MaxIteraciones":instancia.iteraciones}
    
    ficheroLaser=open("enPieCerca.json", "w")

    ficheroLaser.write(json.dumps(cabecera)+'\n')
    
    i = 0
    
    seguir=True
     
    while(i<=instancia.iteraciones and seguir):
        
        #Situamos donde queremos a la persona sentada, unidades en metros
        returnCode = vrep.simxSetObjectPosition(clientID,personhandle,-1,[1+2.0*i/10,-0.4,0.0],vrep.simx_opmode_oneshot)
        
        #Cambiamos la orientacion, ojo está en radianes: Para pasar de grados a radianes hay que multiplicar por PI y dividir por 180
        returnCode = vrep.simxSetObjectOrientation(clientID, personhandle, -1, [0.0,0.0,3.05-(0.20)*i], vrep.simx_opmode_oneshot)
