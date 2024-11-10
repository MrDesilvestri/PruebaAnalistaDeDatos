import pandas as pd
import re

# Definición de variables
URL_ENTRADA = 'D:\\GITHUB\\PruebaAnalistaDeDatos\\parte1\\Uncorrected Data\\PROGRAMA_3.txt'
URL_SALIDA = 'D:\\GITHUB\\PruebaAnalistaDeDatos\\parte1\\Corrected Data\\PROGRAMA_3_corrected.txt'
verificacion_columnas = ["LOCALIDADFIC_3", "NACIONALIDAD_10", "NOMBREEAPB_27", "FECHADENACIMIENTO_14", "ETNIA_18", "SEXO_11", "GENERO_12", "FECHAINTERVENCION_2"]

def limpiar_datos_programa3(ruta_entrada, ruta_salida, columnas_esperadas):
    """
    Realiza la limpieza del archivo de datos para programa 3.
    """
    try:
        # Cargar el archivo con 'on_bad_lines=skip' para ignorar filas problemáticas
        df = pd.read_csv(ruta_entrada, sep='|', header=0, names=columnas_esperadas, on_bad_lines='skip')

        # Verificar las columnas
        if not set(df.columns) == set(columnas_esperadas):
            print("Las columnas del archivo no coinciden con las esperadas.")
            return
        else:
            print("Las columnas son correctas.")

        # Eliminar filas con datos faltantes en FECHADENACIMIENTO_14
        df = df.dropna(subset=['FECHADENACIMIENTO_14'])

        # Formatear la columna FECHADENACIMIENTO_14 como fecha en formato 'YYYY-MM-DD'
        df['FECHADENACIMIENTO_14'] = pd.to_datetime(df['FECHADENACIMIENTO_14'], errors='coerce').dt.strftime('%Y-%m-%d')

        # Eliminar filas que no se pudieron convertir a fecha (NaT)
        df = df.dropna(subset=['FECHADENACIMIENTO_14'])

        # Formatear la columna FECHAINTERVENCION_2 como fecha en formato 'YYYY-MM-DD'
        df['FECHAINTERVENCION_2'] = pd.to_datetime(df['FECHAINTERVENCION_2'].str[:8], errors='coerce', format='%Y%m%d').dt.strftime('%Y-%m-%d')

        # Limpiar las columnas ETNIA_18, SEXO_11 y GENERO_12 para quitar prefijos numéricos y guiones
        df['ETNIA_18'] = df['ETNIA_18'].str.replace(r'^\d+-\s*', '', regex=True)
        df['SEXO_11'] = df['SEXO_11'].str.replace(r'^\d+-\s*', '', regex=True)
        df['GENERO_12'] = df['GENERO_12'].str.replace(r'^\d+-\s*', '', regex=True)

        # Eliminar caracteres no deseados de todas las columnas (excepto las fechas, que ya están en formato adecuado)
        for col in ['LOCALIDADFIC_3', 'NACIONALIDAD_10', 'NOMBREEAPB_27', 'ETNIA_18', 'SEXO_11', 'GENERO_12']:
            df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[^A-Za-z0-9\s,-]', '', x).strip())

        # Guardar el archivo limpio en la ruta de salida
        df.to_csv(ruta_salida, sep='|', index=False)

        print("Archivo limpio guardado como PROGRAMA_3_corrected.txt en la ruta especificada.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_entrada}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Implementación de la función
limpiar_datos_programa3(URL_ENTRADA, URL_SALIDA, verificacion_columnas)
