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
import random
import math


def capturar(path, clientID):
    
    #Guardar la referencia del robot
    _, robothandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
    
    #Guardar la referencia de la camara
    _, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
    
    #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)
    
    partes = path.split("/")
    parte1 = partes[1]
    parte2 = partes[2].split(".")[0]
    
    if parte1.startswith("positivo"):
        
        if parte2.startswith("enPie"):
        # obtenermos la referencia a la persona Bill para moverla    
            _, personhandle = vrep.simxGetObjectHandle(clientID, 'Bill#0', vrep.simx_opmode_oneshot_wait)
        else:
            _, personhandle = vrep.simxGetObjectHandle(clientID, 'Bill', vrep.simx_opmode_oneshot_wait)
           
        #Iniciar la camara y esperar un segundo para llenar el buffer
        _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
        time.sleep(1)
        plt.axis('equal')
        plt.axis([0, 4, -2, 2])
        
        #print("Cambiando el directorio de trabajo: ", os.getcwd())
        os.chdir(parte1)

        cabecera={"TiempoSleep":time.sleep(0.5),
                  "MaxIteraciones":instancia.iteraciones}
        
        ficheroLaser=open(f"{parte2}.json", "w")
    
        ficheroLaser.write(json.dumps(cabecera)+'\n')
        
        i = 0
        
        seguir=True
        xmin = 0
        xmax = 0
        
        if parte2 == "enPieCerca" or parte2 == "sentadoCerca":
            xmin = instancia.cerca #0.5
            xmax = instancia.media #1.5
        if parte2 == "enPieMedia" or parte2 == "sentadoMedia":
            xmin = instancia.media #1.5
            xmax = instancia.lejos #2.5
        if parte2 == "enPieLejos" or parte2 == "sentadoLejos":
            xmin = instancia.lejos #2.5
            xmax = instancia.lejos + 1 #3.5   
            
        while(i<instancia.iteraciones and seguir):
            
            x_pos = random.uniform(xmin,xmax)
            angulo = random.uniform(0, 360)
            radianes = math.radians(angulo)
            
            #Situamos donde queremos a la persona sentada, unidades en metros
            returnCode = vrep.simxSetObjectPosition(clientID,personhandle,-1,[x_pos,0.0,0.0],vrep.simx_opmode_oneshot)
            
            #Cambiamos la orientacion, ojo está en radianes: Para pasar de grados a radianes hay que multiplicar por PI y dividir por 180
            returnCode = vrep.simxSetObjectOrientation(clientID, personhandle, -1, [0.0,0.0,radianes], vrep.simx_opmode_oneshot)
            
            time.sleep(0.5)
            
            puntosx=[] #listas para recibir las coordenadas x, y z de los puntos detectados por el laser
            puntosy=[]
            puntosz=[]
            returnCode, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer) 
           
            datosLaser=vrep.simxUnpackFloats(signalValue)
            for indice in range(0,len(datosLaser),3):
                puntosx.append(datosLaser[indice+1])
                puntosy.append(datosLaser[indice+2])
                puntosz.append(datosLaser[indice])
                
            """
            print("Iteración: ", i)         
            plt.clf()    
            plt.plot(puntosx, puntosy, 'r.')
            plt.savefig('Plot'+str(i)+'.jpg')
            plt.show()
            """
            
            #Guardamos los puntosx, puntosy en el fichero JSON
            lectura={"Iteracion":i, "PuntosX":puntosx, "PuntosY":puntosy}
            #ficheroLaser.write('{}\n'.format(json.dumps(lectura)))
            ficheroLaser.write(json.dumps(lectura)+'\n')
            
            #Guardar frame de la camara, rotarlo y convertirlo a BGR
            _, resolution, image=vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_buffer)
            img = np.array(image, dtype = np.uint8)
            img.resize([resolution[0], resolution[1], 3])
            img = np.rot90(img,2)
            img = np.fliplr(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            #salvo a disco la imagen
            cv2.imwrite('Iteracion'+str(i)+'.jpg', img)
         
            #Mostrar frame y salir con "ESC"
            cv2.imshow('Image', img)
              
            
            tecla = cv2.waitKey(5) & 0xFF
            if tecla == 27:
                seguir=False
            
            i=i+1
        #detenemos la simulacion
        vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)

        #cerramos la conexion
        vrep.simxFinish(clientID)

        #cerramos las ventanas
        cv2.destroyAllWindows()

        finFichero={"Iteraciones totales":i}
        ficheroLaser.write(json.dumps(finFichero)+'\n')
        ficheroLaser.close()
    else:
        if parte2 == "cilindroMenorCerca" or parte2 == "cilindroMenorMedia" or parte2 == "cilindroMenorLejos":

            _, cilindro1 = vrep.simxGetObjectHandle(clientID, 'Cylinder1', vrep.simx_opmode_oneshot_wait)
        
            _, cilindro2 = vrep.simxGetObjectHandle(clientID, 'Cylinder2', vrep.simx_opmode_oneshot_wait)
        else:
            _, cilindro1 = vrep.simxGetObjectHandle(clientID, 'Cylinder', vrep.simx_opmode_oneshot_wait)

        #Iniciar la camara y esperar un segundo para llenar el buffer
        _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
        time.sleep(1)
        plt.axis('equal')
        plt.axis([0, 4, -2, 2])
        
        #print("Cambiando el directorio de trabajo: ", os.getcwd())
        os.chdir(parte1)

        cabecera={"TiempoSleep":time.sleep(0.5),
                  "MaxIteraciones":instancia.iteraciones}
        
        ficheroLaser=open(f"{parte2}.json", "w")
    
        ficheroLaser.write(json.dumps(cabecera)+'\n')
        
        i = 0
        
        seguir=True
        xmin = 0
        xmax = 0
        
        if parte2 == "cilindroMenorCerca" or parte2 == "cilindroMayorCerca":
            xmin = instancia.cerca #0.5
            xmax = instancia.media #1.5
        if parte2 == "cilindroMenorMedia" or parte2 == "cilindroMayorMedia":
            xmin = instancia.media #1.5
            xmax = instancia.lejos #2.5
        if parte2 == "cilindroMenorLejos" or parte2 == "cilindroMayorLejos":
            xmin = instancia.lejos #2.5
            xmax = instancia.lejos + 1 #3.5   
            
        while(i<instancia.iteraciones and seguir):
            
            x_pos = random.uniform(xmin,xmax)
            if parte2 == "cilindroMenorCerca" or parte2 == "cilindroMenorMedia" or parte2 == "cilindroMenorLejos":
                #Situamos donde queremos a la persona sentada, unidades en metros
                returnCode = vrep.simxSetObjectPosition(clientID,cilindro1,-1,[x_pos,0.05,0.6],vrep.simx_opmode_oneshot)
                returnCode = vrep.simxSetObjectPosition(clientID,cilindro2,-1,[x_pos,-0.05,0.6],vrep.simx_opmode_oneshot)

                
                time.sleep(0.5)
                
                puntosx=[] #listas para recibir las coordenadas x, y z de los puntos detectados por el laser
                puntosy=[]
                puntosz=[]
                returnCode, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer) 
               
                datosLaser=vrep.simxUnpackFloats(signalValue)
                for indice in range(0,len(datosLaser),3):
                    puntosx.append(datosLaser[indice+1])
                    puntosy.append(datosLaser[indice+2])
                    puntosz.append(datosLaser[indice])
                    
                """
                print("Iteración: ", i)         
                plt.clf()    
                plt.plot(puntosx, puntosy, 'r.')
                plt.savefig('Plot'+str(i)+'.jpg')
                plt.show()
                """
                
                #Guardamos los puntosx, puntosy en el fichero JSON
                lectura={"Iteracion":i, "PuntosX":puntosx, "PuntosY":puntosy}
                #ficheroLaser.write('{}\n'.format(json.dumps(lectura)))
                ficheroLaser.write(json.dumps(lectura)+'\n')
            else:
                #Situamos donde queremos a la persona sentada, unidades en metros
                returnCode = vrep.simxSetObjectPosition(clientID,cilindro1,-1,[x_pos,0.05,0.25],vrep.simx_opmode_oneshot)
                
                time.sleep(0.5)
                
                puntosx=[] #listas para recibir las coordenadas x, y z de los puntos detectados por el laser
                puntosy=[]
                puntosz=[]
                returnCode, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer) 
               
                datosLaser=vrep.simxUnpackFloats(signalValue)
                for indice in range(0,len(datosLaser),3):
                    puntosx.append(datosLaser[indice+1])
                    puntosy.append(datosLaser[indice+2])
                    puntosz.append(datosLaser[indice])
                    
                
                #Guardamos los puntosx, puntosy en el fichero JSON
                lectura={"Iteracion":i, "PuntosX":puntosx, "PuntosY":puntosy}
                #ficheroLaser.write('{}\n'.format(json.dumps(lectura)))
                ficheroLaser.write(json.dumps(lectura)+'\n')
            #Guardar frame de la camara, rotarlo y convertirlo a BGR
            _, resolution, image=vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_buffer)
            img = np.array(image, dtype = np.uint8)
            img.resize([resolution[0], resolution[1], 3])
            img = np.rot90(img,2)
            img = np.fliplr(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            #salvo a disco la imagen
            cv2.imwrite('Iteracion'+str(i)+'.jpg', img)
         
            #Mostrar frame y salir con "ESC"
            cv2.imshow('Image', img)
              
            
            tecla = cv2.waitKey(5) & 0xFF
            if tecla == 27:
                seguir=False
            
            i=i+1
        #detenemos la simulacion
        vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)

        #cerramos la conexion
        vrep.simxFinish(clientID)

        #cerramos las ventanas
        cv2.destroyAllWindows()

        finFichero={"Iteraciones totales":i}
        ficheroLaser.write(json.dumps(finFichero)+'\n')
        ficheroLaser.close()
    
    direct_padre = os.path.dirname(os.getcwd())   
    os.chdir(direct_padre)
        