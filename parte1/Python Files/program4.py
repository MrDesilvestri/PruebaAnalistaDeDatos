import pandas as pd

# Definición de variables
URL_ENTRADA = 'D:\\GITHUB\\PruebaAnalistaDeDatos\\parte1\\Uncorrected Data\\PROGRAMA_4.txt'
URL_SALIDA = 'D:\\GITHUB\\PruebaAnalistaDeDatos\\parte1\\Corrected Data\\PROGRAMA_4_corrected.txt'
verificacion_columnas = ["LOCALIDAD_FIC", "ESTADO_CIVIL_", "NOMBRE_EAPB_", "FECHA_DE_NACIMIENTO_", "ETNIA_", "SEXO_",
                         "FECHA_INTERVENCION"]

def limpiar_datos_programa4(ruta_entrada, ruta_salida, columnas_esperadas):
    """
    Realiza la limpieza del archivo de datos para programa 4.

    Esta función carga un archivo de datos en fragmentos, verifica que las columnas coincidan con las esperadas,
    elimina filas con datos faltantes o que contienen solo espacios en cualquier columna,
    formatea las fechas correctamente, elimina filas con datos mal formateados y guarda el archivo limpio en la ruta de salida especificada.

    Parámetros:
    ruta_entrada (str): La ruta completa del archivo de datos a limpiar.
    ruta_salida (str): La ruta completa donde se guardará el archivo limpio.
    columnas_esperadas (list): Lista de nombres de columnas que se esperan en el archivo para asegurar la consistencia.

    Retorna:
    None: Esta función no retorna ningún valor. Guarda el archivo limpio en la ubicación especificada.
    """
    try:
        # Cargar solo el encabezado para verificar las columnas
        encabezado = pd.read_csv(ruta_entrada, sep='|', nrows=0)

        # Verificar las columnas
        if not set(encabezado.columns) == set(columnas_esperadas):
            print("Las columnas del archivo no coinciden con las esperadas.")
            return
        else:
            print("Las columnas son correctas.")

        # Procesar el archivo en fragmentos
        chunks = pd.read_csv(ruta_entrada, sep='|', header=0, chunksize=10000)
        cleaned_data = []  # Lista para almacenar los fragmentos limpios

        for chunk in chunks:
            # Eliminar filas con datos faltantes o solo espacios en cualquier columna
            chunk = chunk.dropna(how='any')
            chunk = chunk[~chunk.apply(lambda row: row.astype(str).str.strip().eq('').any(), axis=1)]

            # Eliminar filas con comillas no deseadas o datos fuera del formato esperado
            chunk = chunk[~chunk.apply(lambda row: row.astype(str).str.contains(r'["|]| \d+-').any(), axis=1)]

            # Remover prefijos en las columnas categóricas
            for col in ['ESTADO_CIVIL_', 'ETNIA_', 'SEXO_']:
                chunk[col] = chunk[col].str.replace(r'^\d+-\s*', '', regex=True)

            # Formatear las fechas
            chunk['FECHA_DE_NACIMIENTO_'] = pd.to_datetime(chunk['FECHA_DE_NACIMIENTO_'], errors='coerce').dt.strftime('%Y-%m-%d')
            chunk['FECHA_INTERVENCION'] = pd.to_datetime(chunk['FECHA_INTERVENCION'], errors='coerce').dt.strftime('%Y-%m-%d')

            # Filtrar filas con fechas inválidas
            chunk = chunk.dropna(subset=['FECHA_DE_NACIMIENTO_', 'FECHA_INTERVENCION'])

            # Filtrar filas con más columnas de las esperadas
            chunk = chunk[chunk.apply(lambda x: len(x) == len(columnas_esperadas), axis=1)]

            # Agregar el fragmento limpio a la lista
            cleaned_data.append(chunk)

        # Concatenar todos los fragmentos limpios y guardar en archivo
        df_cleaned = pd.concat(cleaned_data, ignore_index=True)
        df_cleaned.to_csv(ruta_salida, sep='|', index=False)

        print("Archivo limpio guardado en la ruta especificada.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_entrada}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Implementación de la función
limpiar_datos_programa4(URL_ENTRADA, URL_SALIDA, verificacion_columnas)
