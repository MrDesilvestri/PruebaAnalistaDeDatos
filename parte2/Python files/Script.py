import pandas as pd
from datetime import datetime
import warnings

# Deshabilitar advertencias de openpyxl
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Rutas a los archivos Excel
ruta_capital = 'D:\\GITHUB\\PruebaAnalistaDeDatos\\parte2\\Uncorrected data\\Capital.xlsx'
ruta_sur = 'D:\\GITHUB\\PruebaAnalistaDeDatos\\parte2\\Uncorrected data\\SUR.xlsx'

# Cargar datos
df_capital = pd.read_excel(ruta_capital)
df_sur = pd.read_excel(ruta_sur)

# Función para validar el formato de fecha
def validar_fecha(fecha_texto):
    try:
        datetime.strptime(fecha_texto, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Función para validar los datos de cada archivo
def validar_datos(df, nombre_archivo):
    errores = []

    # Verificaciones generales
    columnas_obligatorias = ['Sexo', 'Edad', 'Fecha de Caracterización', 'Programa', 'EAPB']
    for columna in columnas_obligatorias:
        if columna in df.columns:
            vacios = df[columna].isnull() | df[columna].astype(str).str.strip().eq('')
            if vacios.any():
                errores.append(f"{nombre_archivo}: Hay valores vacíos en la columna '{columna}'.")

    if 'Sexo' in df.columns:
        sexo_invalido = df[~df['Sexo'].isin(['HOMBRE', 'MUJER', 'INTERSEXUAL', 'OTROS', 'NO REGISTRA'])]
        if not sexo_invalido.empty:
            errores.append(f"{nombre_archivo}: Valores inválidos en la columna 'Sexo'.")

    if 'Edad' in df.columns:
        edad_invalida = df[~df['Edad'].apply(lambda x: isinstance(x, (int, float)) and x >= 0)]
        if not edad_invalida.empty:
            errores.append(f"{nombre_archivo}: Valores inválidos en la columna 'Edad'.")

    if 'Fecha de Caracterización' in df.columns:
        fechas_invalidas = df[~df['Fecha de Caracterización'].apply(lambda x: validar_fecha(str(x)))]
        if not fechas_invalidas.empty:
            errores.append(f"{nombre_archivo}: Formato de fecha inválido en la columna 'Fecha de Caracterización'.")

    if 'Programa' in df.columns:
        programa_invalido = df[~df['Programa'].isin(['PROGRAMA 1', 'PROGRAMA 2', 'PROGRAMA 3'])]
        if not programa_invalido.empty:
            errores.append(f"{nombre_archivo}: Valores inválidos en la columna 'Programa'.")

    if 'EAPB' in df.columns:
        eapb_faltante = df['EAPB'].isnull()
        if eapb_faltante.any():
            errores.append(f"{nombre_archivo}: Valores faltantes en la columna 'EAPB'.")

    return errores

# Ejecutar validación para cada archivo
errores_capital = validar_datos(df_capital, 'Capital.xlsx')
errores_sur = validar_datos(df_sur, 'SUR.xlsx')

# Imprimir resultados
if errores_capital:
    print("Errores en Capital.xlsx:")
    for error in errores_capital:
        print(error)
else:
    print("Capital.xlsx: Todos los datos son válidos.")

if errores_sur:
    print("\nErrores en SUR.xlsx:")
    for error in errores_sur:
        print(error)
else:
    print("SUR.xlsx: Todos los datos son válidos.")
