
import pandas as pd
import numpy as np

def standardize_column_names(df):
    """
    Convierte todos los nombres de columnas a minúsculas,
    quita espacios al inicio y final, y reemplaza espacios intermedios con guiones bajos.
    """
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    return df

def replace_percent_sign(df, column):
    """
    Elimina el símbolo de porcentaje de una columna si existe.
    Solo se aplica si la columna está presente en el DataFrame.
    """
    if column in df.columns:
        df[column] = df[column].astype(str).str.replace('%', '', regex=False)
    return df

def convert_column_to_numeric(df, column):
    """
    Convierte una columna a tipo numérico si está presente en el DataFrame.
    Los valores no convertibles se reemplazan con NaN.
    """
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

def extract_middle_from_date_string(df, column):
    """
    Extrae el número del medio de cadenas con formato tipo "1/5/00".
    Convierte el resultado a número.
    """
    if column in df.columns:
        df[column] = df[column].astype(str).str.split('/').str[1]
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

def fill_null_with_median(df, column):
    """
    Rellena los valores nulos en una columna con la mediana,
    siempre que la columna exista.
    """
    if column in df.columns:
        median = df[column].median()
        df[column] = df[column].fillna(median)
    return df

def drop_duplicates_and_reset_index(df):
    """
    Elimina duplicados del DataFrame y reinicia el índice.
    """
    df = df.drop_duplicates().reset_index(drop=True)
    return df

def convert_floats_to_ints(df):
    """
    Convierte columnas de tipo float a int (si no hay NaN).
    """
    for col in df.select_dtypes(include='float'):
        if df[col].isna().sum() == 0:
            df[col] = df[col].astype(int)
    return df

def clean_open_complaints(df, column="number_of_open_complaints"):
    # Extrae el primer número antes del "/" y lo convierte a numérico
    df[column] = df[column].astype(str).str.extract(r'^(\d+)')
    df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).astype(int)
    return df

def clean_data(df):
    """
    Función principal que limpia un DataFrame usando varios pasos estándar.
    Robustez integrada para evitar errores si las columnas no existen.
    """
    df = standardize_column_names(df)
    df = clean_open_complaints(df, "number_of_open_complaints")

    df = replace_percent_sign(df, "monthly_premium_auto")
    df = convert_column_to_numeric(df, "customer_lifetime_value")
    df = fill_null_with_median(df, "income")

    df = drop_duplicates_and_reset_index(df)
    df = convert_floats_to_ints(df)

    return df
