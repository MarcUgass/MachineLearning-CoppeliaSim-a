#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import math

def agrupar_clusters():
    carpetas_positivas = ["positivo1", "positivo2", "positivo3", "positivo4", "positivo5", "positivo6"]
    carpetas_negativas = ["negativo1", "negativo2", "negativo3", "negativo4", "negativo5", "negativo6"]
    
    archivos_positivos = []
    archivos_negativos = []

    for carpeta in carpetas_positivas:
        archivos_positivos.extend([os.path.join(carpeta, archivo) for archivo in os.listdir(carpeta) if archivo.endswith(".json")])

    for carpeta in carpetas_negativas:
        archivos_negativos.extend([os.path.join(carpeta, archivo) for archivo in os.listdir(carpeta) if archivo.endswith(".json")])

    min_puntos = 5  # Ajusta según tus necesidades
    max_puntos = 30  # Ajusta según tus necesidades
    umbral_distancia = 0.1  # Ajusta según tus necesidades

    clusters_positivos = agrupar_puntos(archivos_positivos, min_puntos, max_puntos, umbral_distancia)
    clusters_negativos = agrupar_puntos(archivos_negativos, min_puntos, max_puntos, umbral_distancia)

    guardar_clusters_en_json(clusters_positivos, "clustersPiernas.json")
    guardar_clusters_en_json(clusters_negativos, "clustersNoPiernas.json")

def agrupar_puntos(archivos, min_puntos, max_puntos, umbral_distancia):
    clusters = []
    cluster_actual = []
    numero_cluster = 1
    
    for archivo in archivos:
        with open(archivo, 'r') as f:
            lineas = f.readlines()
        
        for linea in lineas:
            datos = json.loads(linea)
            puntos_x = datos["PuntosX"]
            puntos_y = datos["PuntosY"]
            
            for i in range(len(puntos_x)):
                punto_actual = {"x": puntos_x[i], "y": puntos_y[i]}
                
                if not cluster_actual:
                    cluster_actual.append(punto_actual)
                else:
                    distancia_anterior = math.sqrt((punto_actual["x"] - cluster_actual[-1]["x"])**2 + (punto_actual["y"] - cluster_actual[-1]["y"])**2)
                    
                    if distancia_anterior < umbral_distancia and len(cluster_actual) < max_puntos:
                        cluster_actual.append(punto_actual)
                    else:
                        if len(cluster_actual) >= min_puntos:
                            clusters.append({
                                "numero_cluster": numero_cluster,
                                "numero_puntos": len(cluster_actual),
                                "puntosX": [p["x"] for p in cluster_actual],
                                "puntosY": [p["y"] for p in cluster_actual]
                            })
                            numero_cluster += 1
                        
                        cluster_actual = [punto_actual]

        # Verificar si hay un último cluster por procesar
        if len(cluster_actual) >= min_puntos:
            clusters.append({
                "numero_cluster": numero_cluster,
                "numero_puntos": len(cluster_actual),
                "puntosX": [p["x"] for p in cluster_actual],
                "puntosY": [p["y"] for p in cluster_actual]
            })
            numero_cluster += 1
        
    return clusters

def guardar_clusters_en_json(clusters, nombre_archivo):
    with open(nombre_archivo, 'w') as f:
        for cluster in clusters:
            f.write(json.dumps(cluster) + '\n')
