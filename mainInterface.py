#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import vrep
from tkinter import messagebox
import os
from parametros import instancia
from Capturar import capturar

def DesconectarCoppelia():
    global clientID
    
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)
    vrep.simxFinish(clientID)
    
    messagebox.showinfo("Práctica PTC Tkinter Robótica","Se ha desconectado de CoppeliaSim")    
    etiqueta_estado.config(text = "Estado: No conectado a CoppeliaSim")
    etiqueta_desconectar.config(state = tkinter.DISABLED)
    etiqueta_capturar.config(state = tkinter.DISABLED)

def Salir():
    global root, etiqueta_estado
    
    if etiqueta_estado.cget("text") == "Estado: Conectado a CoppeliaSim":
        messagebox.showwarning("Práctica PTC Tkinter Robótica","Antes de salir debe desconectar")
        return
    
    confirmacion = messagebox.askyesno("Práctica PTC Tkinter Robótica",f"¿Está seguro de que desea salir?") 
    
    if not confirmacion:
        return
    root.destroy()
    
def ConectarCoppelia():
    global clientID
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
    #Para que funcione, abrir una escena en el coppeliaSim, alli darle al run, y ya podra funcionar 
    
    if clientID!=-1:
        messagebox.showinfo("Práctica PTC Tkinter Robótica","Conexión con Coppelia establecida")    
        etiqueta_estado.config(text = "Estado: Conectado a CoppeliaSim")
        etiqueta_desconectar.config(state = tkinter.ACTIVE)
        etiqueta_capturar.config(state = tkinter.ACTIVE)
    else:
        messagebox.showerror("Práctica PTC Tkinter Robótica","Debe iniciar el simulador")

def Columna1():
    global root , etiqueta_conectar, etiqueta_desconectar, etiqueta_estado, etiqueta_capturar, etiqueta_agrupar ,etiqueta_extraer, etiqueta_entrenar, etiqueta_predecir, etiqueta_salir
    etiqueta = tkinter.Label(root, text= "Es necesario ejecutar el simulador CoppeliaSim")
    etiqueta.grid(row = 0, column = 0)
    
    etiqueta_conectar = tkinter.Button(root, text= "Conectar con CoopeliaSim", command = ConectarCoppelia)
    etiqueta_conectar.grid(row = 1, column = 0)
    
    etiqueta_desconectar = tkinter.Button(root, text= "Detener y desconectar CoopeliaSim", state = tkinter.DISABLED, command = DesconectarCoppelia)
    etiqueta_desconectar.grid(row = 2, column = 0)
    
    etiqueta_estado = tkinter.Label(root, text= "Estado: No conectado a CoppeliaSim")
    etiqueta_estado.grid(row = 3, column = 0)
    
    etiqueta_capturar = tkinter.Button(root, text= "Capturar", state = tkinter.DISABLED, command = capturar_boton)
    etiqueta_capturar.grid(row = 4, column = 0)
    
    etiqueta_agrupar = tkinter.Button(root, text= "Agrupar", state = tkinter.DISABLED)
    etiqueta_agrupar.grid(row = 5, column = 0)
    
    etiqueta_extraer = tkinter.Button(root, text= "Extraer características", state = tkinter.DISABLED)
    etiqueta_extraer.grid(row = 6, column = 0)
    
    etiqueta_entrenar = tkinter.Button(root, text= "Entrenar clasificador", state = tkinter.DISABLED)
    etiqueta_entrenar.grid(row = 7, column = 0)
    
    etiqueta_predecir = tkinter.Button(root, text= "Predecir", state = tkinter.DISABLED)
    etiqueta_predecir.grid(row = 8, column = 0)
    
    etiqueta_salir = tkinter.Button(root, text= "Salir", command = Salir)
    etiqueta_salir.grid(row = 9, column = 0)

def Columna2():
    global caja_iteraciones, caja_cerca, caja_media, caja_lejos, caja_minpuntos, caja_maxpuntos, caja_umbral, boton_conectar

    etq_parametros = tkinter.Label(root, text= "Parámetros")
    etq_parametros.grid(row = 1, column = 1)

    etiqueta_iteraciones = tkinter.Label(root, text= "Iteraciones:", anchor = "e")
    etiqueta_iteraciones.grid(row = 2, column = 1, sticky = "e")
    caja_iteraciones = tkinter.Entry(root, width =5)
    caja_iteraciones.grid(row=2, column = 2)

    etiqueta_cerca = tkinter.Label(root, text= "Cerca:",anchor = "e")
    etiqueta_cerca.grid(row = 3, column = 1, sticky = "e")
    caja_cerca = tkinter.Entry(root, width =5)
    caja_cerca.grid(row=3, column = 2)

    etiqueta_media = tkinter.Label(root, text= "Media:",anchor = "e")
    etiqueta_media.grid(row = 4, column = 1, sticky = "e")
    caja_media = tkinter.Entry(root, width =5)
    caja_media.grid(row=4, column = 2)

    etiqueta_lejos = tkinter.Label(root, text= "Lejos:",anchor = "e")
    etiqueta_lejos.grid(row = 5, column = 1, sticky = "e")
    caja_lejos = tkinter.Entry(root, width =5)
    caja_lejos.grid(row=5, column = 2)

    etiqueta_minpuntos = tkinter.Label(root, text= "MinPuntos:",anchor = "e")
    etiqueta_minpuntos.grid(row = 6, column = 1, sticky = "e")
    caja_minpuntos = tkinter.Entry(root, width =5)
    caja_minpuntos.grid(row=6, column = 2)

    etiqueta_maxpuntos = tkinter.Label(root, text= "MaxPuntos:",anchor = "e")
    etiqueta_maxpuntos.grid(row = 7, column = 1, sticky = "e")
    caja_maxpuntos = tkinter.Entry(root, width =5)
    caja_maxpuntos.grid(row=7, column = 2)

    etiqueta_umbral = tkinter.Label(root, text= "UmbralDistancia:",anchor = "e")
    etiqueta_umbral.grid(row = 8, column = 1, sticky = "e")
    caja_umbral = tkinter.Entry(root, width =5)
    caja_umbral.grid(row=8, column = 2)

    boton_conectar = tkinter.Button(root, text= "Cambiar", command = cambiar_valores)
    boton_conectar.grid(row = 9, column = 1)

def Columna3():
    global lista
    etiqueta = tkinter.Label(root, text= "Fichero para la captura")
    etiqueta.grid(row = 1, column = 3)

    
    lista = tkinter.Listbox(root, width=35,height=12)
    lista.grid(row= 2, column = 3, rowspan = 10)
    archivos = [
        ]
    #positivo
    lista.insert(tkinter.END, f"positivo1/enPieCerca.json") 
    lista.insert(tkinter.END, f"positivo2/enPieMedia.json")
    lista.insert(tkinter.END, f"positivo3/enPieLejos.json")
    lista.insert(tkinter.END, f"positivo4/sentadoCerca.json")
    lista.insert(tkinter.END, f"positivo5/sentadoMedia.json")
    lista.insert(tkinter.END, f"positivo6/sentadoLejos.json")
    
    #negativo
    lista.insert(tkinter.END, f"negativo1/cilindroMenorCerca.json")  
    lista.insert(tkinter.END, f"negativo2/cilindroMenorMedia.json")
    lista.insert(tkinter.END, f"negativo3/cilindroLejosLejosa.json")
    lista.insert(tkinter.END, f"negativo4/cilindroMayorCerca.json")
    lista.insert(tkinter.END, f"negativo5/cilindroMayorMedia.json")
    lista.insert(tkinter.END, f"negativo6/cilindroMayorLejos.json")

def capturar_boton():
    global lista, clientID
    item = lista.curselection()
    if not item:
        messagebox.showwarning("Práctica PTC Tkinter Robótica","Debe elegir un fichero de la lista")
        return
    name = lista.get(item)
    path = os.path.join(".", name) 
    
    if os.path.exists(path):
        confirmacion = messagebox.askyesno("Práctica PTC Tkinter Robótica",f"Se va a crear el fichero: {name} ¿Está seguro?") 
    else:
        confirmacion = messagebox.askyesno("Práctica PTC Tkinter Robótica",f"El fichero: {name} Ya exste. Se creará de nuevo. ¿Está seguro?")
    
    if not confirmacion: #no acepta
        return
    
    capturar(path, clientID)
    
def cambiar_valores():
    global caja_iteraciones,caja_cerca, caja_media, caja_lejos, caja_minpuntos, caja_maxpuntos, caja_umbral, boton_conectar
    try:
        # Actualiza las variables globales con los valores de las entradas
        iteraciones = float(caja_iteraciones.get())
        cerca = float(caja_cerca.get())
        media = float(caja_media.get())
        lejos = float(caja_lejos.get())
        min_puntos = float(caja_minpuntos.get())
        max_puntos = float(caja_maxpuntos.get())
        umbral = float(caja_umbral.get())
        
        instancia.set_valores(iteraciones, cerca, media, lejos, min_puntos, max_puntos, umbral)
    except:
        instancia.set_valores(0, 0, 0, 0, 0, 0, 0)
    
def agrupar_boton():
    return

def main():    
    global root
    root = tkinter.Tk()
    root.title("Práctica PTC Tkinter Robótica")
    root.geometry("750x300") #En toeria es 700, pero si no, no cabe
    Columna1()
    Columna2()
    Columna3()
    
    root.mainloop()
    
main()