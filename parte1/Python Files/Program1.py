import pandas as pd

"""
Autor: Carlos D silvestri
Fecha de creación: 10/11/2024

Descripción:
Este script realiza un proceso de limpieza de datos para el archivo 'PROGRAMA_1.txt'. 
Verifica que las columnas sean correctas, elimina filas con datos faltantes o con un número 
incorrecto de columnas, y remueve comillas dobles de los datos. Finalmente, guarda el archivo limpio en formato .txt.

Entradas:
- Archivo de texto con datos sin procesar, ubicado en la ruta especificada.

Salidas:
- Archivo de texto con datos limpios, guardado en la misma ruta especificada.

Uso:
Ejecuta este script en un entorno que tenga la biblioteca pandas instalada para 
procesar los datos, el archivo requirements.txt cumple con los criterios esperados 
para poder instalar las bibliotecas solicitadas en venv.
"""

# Definición de todas las variables a utilizar
URL_ENTRADA = 'D:\\GITHUB\\PruebaAnalistaDeDatos\\parte1\\Uncorrected Data\\PROGRAMA_1.txt'
URL_SALIDA = 'D:\\GITHUB\\PruebaAnalistaDeDatos\\parte1\\Corrected Data\\PROGRAMA_1_corrected.txt'
verificacion_columnas = ["REGIMEN_DE_AFILIACION", "LOCALIDAD_CALCULADA", "ASEGURADOR",
                         "FECHA_DE_NACIMIENTO_USUARIO", "SEXO", "FECHA_DE_LA_CONSULTA", "NACIONALIDAD"]

# Definición de funciones a utilizar
def limpiar_datos(ruta_entrada, ruta_salida, columnas_esperadas):
    """
    Realiza la limpieza de un archivo de datos.

    Esta función lee un archivo de datos, verifica que las columnas coincidan con las esperadas,
    elimina filas con datos faltantes, verifica que todas las filas tengan el número correcto de columnas
    y remueve comillas dobles de los datos. Finalmente, guarda el archivo limpio en la ruta de salida especificada.

    Parámetros:
    ruta_entrada (str): La ruta completa del archivo de datos a limpiar.
    ruta_salida (str): La ruta completa donde se guardará el archivo limpio.
    columnas_esperadas (list): Lista de nombres de columnas esperadas en el archivo para garantizar que los datos
                               cumplan con el formato adecuado antes de ser ingresados en la base de datos.

    Retorna:
    None: Esta función no retorna ningún valor. Guarda el archivo limpio en la ubicación especificada.

    Ejemplo de uso:
    limpiar_datos('ruta/al/archivo_entrada.txt', 'ruta/al/archivo_salida.txt', ["col1", "col2", "col3"])
    El archivo ha sido limpiado y guardado en la ruta de salida.
    """

    try:
        # Lectura del archivo
        data = pd.read_csv(ruta_entrada, delimiter=',', header=0, quotechar='"')

        # Verificación de columnas
        if set(data.columns) != set(columnas_esperadas):
            print("Las columnas no coinciden con las esperadas.")
            return
        else:
            print("Las columnas son correctas.")

        # Convertir las columnas de fecha al formato de tipo date
        data['FECHA_DE_NACIMIENTO_USUARIO'] = pd.to_datetime(data['FECHA_DE_NACIMIENTO_USUARIO'], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
        data['FECHA_DE_LA_CONSULTA'] = pd.to_datetime(data['FECHA_DE_LA_CONSULTA'], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')

        # Eliminar filas con datos faltantes
        data = data.dropna(how='any')

        # Eliminar filas que no tienen el número correcto de columnas
        data = data[data.apply(lambda row: len(row) == len(columnas_esperadas), axis=1)]

        # Remover comillas dobles de los datos
        data.replace('"', '', regex=True, inplace=True)

        # Guardar el archivo limpio
        data.to_csv(ruta_salida, sep=',', index=False, quoting=3, escapechar='\\')

        print("Datos limpios y guardados en formato TXT sin comillas en la ruta especificada.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_entrada}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Implementación de la función
limpiar_datos(URL_ENTRADA, URL_SALIDA, verificacion_columnas)
