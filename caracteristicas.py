import json
import csv

# Función para cargar clusters desde un archivo JSON
def cargar_clusters_desde_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        clusters = [json.loads(line) for line in archivo]
    return clusters

# Función para calcular la distancia euclidiana entre dos puntos
def distancia_euclidiana(punto1, punto2):
    return ((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)**0.5

# Función para calcular la distancia de un punto a una recta
def distancia_punto_recta(punto, punto_recta1, punto_recta2):
    x1, y1 = punto_recta1
    x2, y2 = punto_recta2
    numerador = abs((y2 - y1)*punto[0] - (x2 - x1)*punto[1] + x2*y1 - y2*x1)
    denominador = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
    return numerador / denominador

# Función para calcular las características de los clusters
def calcular_caracteristicas_clusters(clusters):
    caracteristicas = []
    for cluster in clusters:
        numero_puntos = len(cluster['puntosX'])
        perimetro = 0
        profundidad = 0
        anchura = distancia_euclidiana((cluster['puntosX'][0], cluster['puntosY'][0]),
                                        (cluster['puntosX'][-1], cluster['puntosY'][-1]))
        for i in range(numero_puntos - 1):
            distancia = distancia_euclidiana((cluster['puntosX'][i], cluster['puntosY'][i]),
                                             (cluster['puntosX'][i+1], cluster['puntosY'][i+1]))
            perimetro += distancia
            profundidad = max(profundidad, distancia_punto_recta((cluster['puntosX'][i], cluster['puntosY'][i]),
                                                                 (cluster['puntosX'][0], cluster['puntosY'][0]),
                                                                 (cluster['puntosX'][-1], cluster['puntosY'][-1])))
        caracteristicas.append({
            "numero_cluster": cluster["numero_cluster"],
            "numero_puntos": numero_puntos,
            "perímetro": perimetro,
            "profundidad": profundidad,
            "anchura": anchura
        })
    return caracteristicas

# Función para guardar las características en un archivo JSON
def guardar_caracteristicas_en_archivo(caracteristicas, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for caracteristica in caracteristicas:
            archivo.write(json.dumps(caracteristica) + '\n')

# Función principal que realiza todo el proceso
def calcular_caracteristicas_y_generar_dataset():
    # Cargar clusters de piernas y no piernas desde archivos JSON
    clusters_piernas = cargar_clusters_desde_archivo("clustersPiernas.json")
    clusters_no_piernas = cargar_clusters_desde_archivo("clustersNoPiernas.json")

    # Calcular características de los clusters
    caracteristicas_piernas = calcular_caracteristicas_clusters(clusters_piernas)
    caracteristicas_no_piernas = calcular_caracteristicas_clusters(clusters_no_piernas)

    # Guardar características en archivos JSON
    guardar_caracteristicas_en_archivo(caracteristicas_piernas, "caracteristicasPiernas.dat")
    guardar_caracteristicas_en_archivo(caracteristicas_no_piernas, "caracteristicasNoPiernas.dat")

    # Crear archivo CSV "piernasDataset.csv"
    with open("piernasDataset.csv", 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Escribir ejemplos de clase 0 (no pierna)
        for caracteristica in caracteristicas_no_piernas:
            csv_writer.writerow([caracteristica["perímetro"], caracteristica["profundidad"],
                                 caracteristica["anchura"], 0])
        # Escribir ejemplos de clase 1 (pierna)
        for caracteristica in caracteristicas_piernas:
            csv_writer.writerow([caracteristica["perímetro"], caracteristica["profundidad"],
                                 caracteristica["anchura"], 1])
