import pandas as pd
import os

# Definición de Variables
URL_ENTRADA = 'D:\\GITHUB\\PruebaAnalistaDeDatos\\parte1\\Uncorrected Data\\PROGRAMA_2.txt'
URL_SALIDA = 'D:\\GITHUB\\PruebaAnalistaDeDatos\\parte1\\Corrected Data\\PROGRAMA_2_corrected.txt'
verificacion_columnas = ["SEXO_BIOLOGICO", "LOCALIDAD", "EAPB", "FECHA_DE_NACIMIENTO",
                         "PERTENENCIA_ETNICA", "SEXO_BIOLOGICO_1", "RIESGO_PSICOSOCIAL",
                         "FECHA_DE_LA_CONSULTA", "TALLA"]

def verificar_columnas(data, columnas_esperadas):
    """
    Verifica que las columnas en el DataFrame coincidan con las columnas esperadas.

    Parámetros:
    data (DataFrame): El DataFrame con los datos cargados.
    columnas_esperadas (list): Lista de nombres de columnas que se esperan en el archivo.

    Retorna:
    bool: True si las columnas coinciden, False de lo contrario.
    """
    return set(data.columns) == set(columnas_esperadas)

def limpiar_datos(ruta_entrada, ruta_salida, columnas_esperadas):
    """
    Realiza la limpieza del archivo de datos para programa 2.

    Esta función carga un archivo de datos, verifica que las columnas coincidan con las esperadas,
    elimina filas con datos faltantes, asegura que la columna 'TALLA' contenga solo números, convierte
    las fechas al formato YYYY-MM-DD y guarda el archivo limpio en la ruta de salida especificada.

    Parámetros:
    ruta_entrada (str): La ruta completa del archivo de datos a limpiar.
    ruta_salida (str): La ruta completa donde se guardará el archivo limpio.
    columnas_esperadas (list): Lista de nombres de columnas que se esperan en el archivo para asegurar la consistencia.

    Retorna:
    None: Esta función no retorna ningún valor. Guarda el archivo limpio en la ubicación especificada.

    Ejemplo de uso:
    limpiar_datos('ruta/al/archivo_entrada.txt', 'ruta/al/archivo_salida.txt', columnas_esperadas)
    """
    try:
        # Cargar el archivo
        df = pd.read_csv(ruta_entrada, sep='|', header=0)

        # Verificar las columnas
        if not verificar_columnas(df, columnas_esperadas):
            print("Las columnas no coinciden con las esperadas.")
            return
        else:
            print("Las columnas son correctas.")

        # Eliminar filas con datos faltantes
        df = df.dropna(how='any')

        # Limpiar la columna 'TALLA' para que contenga solo números y convertir a enteros
        df['TALLA'] = df['TALLA'].astype(str).str.replace(r'[^0-9]', '', regex=True).astype(float).astype('Int64')

        # Convertir las fechas al formato YYYY-MM-DD
        df['FECHA_DE_NACIMIENTO'] = pd.to_datetime(df['FECHA_DE_NACIMIENTO'], errors='coerce').dt.strftime('%Y-%m-%d')
        df['FECHA_DE_LA_CONSULTA'] = pd.to_datetime(df['FECHA_DE_LA_CONSULTA'], errors='coerce').dt.strftime('%Y-%m-%d')

        # Eliminar filas con valores faltantes después de la conversión de fechas
        df = df.dropna(how='any')

        # Verificar que cada fila tenga el número correcto de columnas
        df = df[df.apply(lambda row: len(row) == len(columnas_esperadas), axis=1)]

        # Guardar el archivo limpio en la ruta de salida
        df.to_csv(ruta_salida, sep='|', index=False, quoting=3)

        print("Datos limpios y guardados en formato TXT en la ruta especificada.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_entrada}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Implementación de la función
limpiar_datos(URL_ENTRADA, URL_SALIDA, verificacion_columnas)
