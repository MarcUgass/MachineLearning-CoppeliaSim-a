#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import vrep
from tkinter import messagebox

def Salir():
    global root
    root.destroy()
    
def ConectarCoppelia():
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
    
    etiqueta_desconectar = tkinter.Button(root, text= "Detener y desconectar CoopeliaSim", state = tkinter.DISABLED)
    etiqueta_desconectar.grid(row = 2, column = 0)
    
    etiqueta_estado = tkinter.Label(root, text= "Estado: No conectado a CoppeliaSim")
    etiqueta_estado.grid(row = 3, column = 0)
    
    etiqueta_capturar = tkinter.Button(root, text= "Capturar", state = tkinter.DISABLED)
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
    global caja_iteraciones,caja_cerca, caja_media, caja_lejos, caja_minpuntos, caja_maxpuntos, boton_conectar
    
    parametros = tkinter.Label(root, text= "Parámetros")
    parametros.grid(row = 1, column = 1)
    
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
    
    etiqueta_maxpuntos = tkinter.Label(root, text= "UmbralDistancia:",anchor = "e")
    etiqueta_maxpuntos.grid(row = 8, column = 1, sticky = "e")
    caja_maxpuntos = tkinter.Entry(root, width =5)
    caja_maxpuntos.grid(row=8, column = 2)
    
    boton_conectar = tkinter.Button(root, text= "Cambiar")
    boton_conectar.grid(row = 9, column = 1)

def Columna3():
    global lista
    etiqueta = tkinter.Label(root, text= "Fichero para la captura")
    etiqueta.grid(row = 1, column = 3)
    
    lista = tkinter.Listbox(root, width=35,height=12)
    lista.grid(row= 2, column = 3, rowspan = 10)

    boton_conectar = tkinter.Button(root, text="Cambiar", command=cambiar_valores)
    boton_conectar.grid(row=9, column=1)

def cargar_valores_desde_json(archivo):
    try:
        with open(archivo, 'r') as f:
            data = json.load(f)
            caja_iteraciones.delete(0, tkinter.END)
            caja_iteraciones.insert(0, data.get('iteraciones', ''))
            caja_cerca.delete(0, tkinter.END)
            caja_cerca.insert(0, data.get('cerca', ''))
            caja_media.delete(0, tkinter.END)
            caja_media.insert(0, data.get('media', ''))
            caja_lejos.delete(0, tkinter.END)
            caja_lejos.insert(0, data.get('lejos', ''))
            caja_minpuntos.delete(0, tkinter.END)
            caja_minpuntos.insert(0, data.get('minpuntos', ''))
            caja_maxpuntos.delete(0, tkinter.END)
            caja_maxpuntos.insert(0, data.get('maxpuntos', ''))
            caja_umbral.delete(0, tkinter.END)
            caja_umbral.insert(0, data.get('umbraldistancia', ''))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

def cambiar_valores():
    seleccion = lista.curselection()
    if seleccion:
        indice = seleccion[0]
        archivo_seleccionado = lista.get(indice)
        cargar_valores_desde_json(archivo_seleccionado)

# ... (código existente)

def seleccionar_archivo():
    directorio = "/ruta/del/directorio"  # Ruta del directorio donde se encuentran los archivos .json
    archivos_json = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.json')]
    lista.delete(0, tkinter.END)
    for archivo in archivos_json:
        lista.insert(tkinter.END, archivo)

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
