import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, GridSearchCV
from warnings import simplefilter

# Ignorar futuras y advertencias de depreciación
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)

# Función para cargar los datos desde un archivo JSON
def cargar_datos(caracteristicas_file):
    caracteristicas_data = pd.read_json(caracteristicas_file, lines=True)

    # Obtener todos los atributos que no son 'numero_cluster'
    X = caracteristicas_data.drop(columns=['numero_cluster', 'numero_puntos', 'perímetro', 'profundidad', 'anchura'])

    # Usar 'numero_cluster' como etiqueta si existe
    if 'numero_cluster' in caracteristicas_data:
        y = caracteristicas_data['numero_cluster']
    else:
        y = None

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

# Función principal
def entrenar():
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
        _ = clasificar_y_evaluar(kernel, X_train_piernas, X_test_piernas, y_train_piernas, y_test_piernas)

        print("\n== Clasificación de No Piernas ==")
        _ = clasificar_y_evaluar(kernel, X_train_no_piernas, X_test_no_piernas, y_train_no_piernas, y_test_no_piernas)

    print("\n== Búsqueda de parámetros en un rango en el caso de RBF ==")
    _ = grid_search_rbf(X_train_piernas, y_train_piernas)
    
