# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, GridSearchCV
import pickle
from warnings import simplefilter

# Ignorar futuras y advertencias de depreciación
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)

# Función para cargar los datos desde un archivo json
def cargar_datos(caracteristicas_file):
    caracteristicas_data = pd.read_json(caracteristicas_file, lines=True)
    X = caracteristicas_data[['perímetro', 'profundidad', 'anchura']]
    y = caracteristicas_data['esPierna']
    return X, y

# Función para dividir los datos en conjuntos de entrenamiento y prueba
def dividir_datos(X, y):
    return train_test_split(X, y, test_size=0.20, random_state=25)

# Función para clasificar y evaluar un kernel específico
def clasificar_y_evaluar(kernel, X_train, X_test, y_train, y_test):
    svc = SVC(kernel=kernel)
    svc.fit(X_train, y_train)
    y_pred = svc.predict(X_test)
    acc_test = accuracy_score(y_test, y_pred)

    print(f"Clasificación con kernel {kernel}")
    print(f"Acc_test {kernel}: (TP+TN)/(T+P)  {acc_test:.4f}")

    print("Matriz de confusión Filas: verdad Columnas: predicción")
    print(confusion_matrix(y_test, y_pred))

    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred))

    svc_cv = SVC(kernel=kernel)
    scores = cross_val_score(svc_cv, X, y, cv=5)
    print(f"Accuracy 5-cross validation ({kernel}): {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

    return svc

# Función para realizar una búsqueda de parámetros en el caso de kernel RBF
def grid_search_rbf(X_train, y_train):
    param_grid = {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.005, 0.01, 0.1]}
    clf = GridSearchCV(SVC(kernel='rbf', class_weight="balanced"), param_grid)
    clf = clf.fit(X_train, y_train)
    print("Mejor estimador encontrado")
    print(clf.best_estimator_)
    return clf.best_estimator_

# Función para guardar el clasificador en un archivo
def guardar_clasificador(clasificador, filename="clasificador.pkl"):
    with open(filename, "wb") as archivo:
        pickle.dump(clasificador, archivo)
    print(f"Clasificador guardado en {filename}")

# Función para cargar el clasificador desde un archivo
def cargar_clasificador(filename="clasificador.pkl"):
    with open(filename, "rb") as archivo:
        clasificador = pickle.load(archivo)
    return clasificador

# Función principal
def main():
    # Archivos de datos
    caracteristicas_file_piernas = "caracteristicasPiernas.dat"
    caracteristicas_file_no_piernas = "caracteristicasNoPiernas.dat"

    # Cargar datos de piernas y no piernas
    X_piernas, y_piernas = cargar_datos(caracteristicas_file_piernas)
    X_no_piernas, y_no_piernas = cargar_datos(caracteristicas_file_no_piernas)

    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train_piernas, X_test_piernas, y_train_piernas, y_test_piernas = dividir_datos(X_piernas, y_piernas)
    X_train_no_piernas, X_test_no_piernas, y_train_no_piernas, y_test_no_piernas = dividir_datos(X_no_piernas, y_no_piernas)

    # Kernels a probar
    kernels = ['linear', 'poly', 'rbf']

    for kernel in kernels:
        print("\n== Clasificación de Piernas ==")
        svc_piernas = clasificar_y_evaluar(kernel, X_train_piernas, X_test_piernas, y_train_piernas, y_test_piernas)

        print("\n== Clasificación de No Piernas ==")
        svc_no_piernas = clasificar_y_evaluar(kernel, X_train_no_piernas, X_test_no_piernas, y_train_no_piernas, y_test_no_piernas)

    print("\n== Búsqueda de parámetros en un rango en el caso de RBF ==")
    mejor_svc_rbf_piernas = grid_search_rbf(X_train_piernas, y_train_piernas)
    mejor_svc_rbf_no_piernas = grid_search_rbf(X_train_no_piernas, y_train_no_piernas)

    # Guardar clasificadores
    guardar_clasificador(svc_piernas, "clasificador_piernas.pkl")
    guardar_clasificador(svc_no_piernas, "clasificador_no_piernas.pkl")
    guardar_clasificador(mejor_svc_rbf_piernas, "clasificador_mejor_rbf_piernas.pkl")
    guardar_clasificador(mejor_svc_rbf_no_piernas, "clasificador_mejor_rbf_no_piernas.pkl")

    # Cargar clasificadores
    clasificador_piernas = cargar_clasificador("clasificador_piernas.pkl")
    clasificador_no_piernas = cargar_clasificador("clasificador_no_piernas.pkl")
    clasificador_mejor_rbf_piernas = cargar_clasificador("clasificador_mejor_rbf_piernas.pkl")
    clasificador_mejor_rbf_no_piernas = cargar_clasificador("clasificador_mejor_rbf_no_piernas.pkl")

    # Ejemplo de predicción
    print("\n== Ejemplo de Predicción con Clasificador de Piernas ==")
    ejemplo_piernas = np.array([[0.23, 0.12, 0.15]])
    prediccion_piernas = clasificador_piernas.predict(ejemplo_piernas)
    print(f"Predicción: {prediccion_piernas}")

    # Ejemplo de predicción
    print("\n== Ejemplo de Predicción con Clasificador de No Piernas ==")
    ejemplo_no_piernas = np.array([[0.45, 0.25, 0.30]])
    prediccion_no_piernas = clasificador_no_piernas.predict(ejemplo_no_piernas)
    print(f"Predicción: {prediccion_no_piernas}")

    # Ejemplo de predicción
    print("\n== Ejemplo de Predicción con Clasificador RBF de Piernas ==")
    ejemplo_rbf_piernas = np.array([[0.35, 0.20, 0.25]])
    prediccion_rbf_piernas = clasificador_mejor_rbf_piernas.predict(ejemplo_rbf_piernas)
    print(f"Predicción: {prediccion_rbf_piernas}")

    # Ejemplo de predicción
    print("\n== Ejemplo de Predicción con Clasificador RBF de No Piernas ==")
    ejemplo_rbf_no_piernas = np.array([[0.55, 0.30, 0.35]])
    prediccion_rbf_no_piernas = clasificador_mejor_rbf_no_piernas.predict(ejemplo_rbf_no_piernas)
    print(f"Predicción: {prediccion_rbf_no_piernas}")


if __name__ == "__main__":
    main()

