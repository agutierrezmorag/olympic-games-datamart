import numpy as np
import pandas as pd


def qualitative_stats(data, cols_cualitativas):
    # Create a DataFrame with a single row of dummy data
    estadisticas = pd.DataFrame(
        {
            "Columna": ["dummy"],
            "Moda": ["dummy"],
            "Moda (#)": [0],
            "Moda (%)": [0.0],
            "Total de valores": [0],
            "Valores unicos (#)": [0],
            "Valores unicos (%)": [0.0],
            "Valores nulos (%)": [0.0],
        }
    )

    for col in cols_cualitativas:
        # Moda
        moda = data[col].mode()[0]
        # Total non-null values
        total_values = data[col].count()
        # Cantidad de veces que se repite la moda
        moda_count = data[col].value_counts().iloc[0]
        # Porcentaje de la moda
        moda_porcentaje = moda_count / len(data) * 100
        # Cantidad de valores diferentes
        valores_unicos = data[col].nunique()
        # Porcentaje de cada tipo de valor
        valor_porcentajes = data[col].nunique() / len(data) * 100
        # Porcentaje de datos faltantes
        porcentaje_nulos = data[col].isna().mean() * 100

        # Agregar una fila al DataFrame de estadísticas
        nueva_fila = pd.DataFrame(
            {
                "Columna": [col],
                "Moda": [moda],
                "Moda (#)": [moda_count],
                "Moda (%)": [moda_porcentaje],
                "Total de valores": [total_values],
                "Valores unicos (#)": [valores_unicos],
                "Valores unicos (%)": [valor_porcentajes],
                "Valores nulos (%)": [porcentaje_nulos],
            }
        )
        estadisticas = pd.concat([estadisticas, nueva_fila], ignore_index=True)

    # Drop the dummy row
    estadisticas = estadisticas.drop(estadisticas.index[0])

    return estadisticas


def descriptors(data):
    # Calculate skewness for numeric columns only
    numeric_cols = data.select_dtypes(include=[np.number])
    skewness = pd.DataFrame(numeric_cols.skew(), columns=["skewness"]).T

    # Calculate kurtosis for numeric columns only
    kurtosis = pd.DataFrame(numeric_cols.kurt(), columns=["kurtosis"]).T

    # Calculate IQR for numeric columns only
    iqr = numeric_cols.apply(lambda x: x.quantile(0.75) - x.quantile(0.25))
    iqr = pd.DataFrame(iqr, columns=["IQR"]).T

    # Get the description for all columns
    desc = data.describe()

    # Append skewness, kurtosis, IQR, and total values to the description
    desc = pd.concat([desc, skewness, kurtosis, iqr])

    return desc


def translate_descriptors(df):
    # Create a dictionary mapping English descriptors to Spanish
    spanish_descriptors = {
        "count": "Total de valores",
        "mean": "Media",
        "std": "Desviación estándar",
        "min": "Valor mínimo",
        "25%": "Q1",
        "50%": "Q2",
        "75%": "Q3",
        "max": "Q4",
        "skewness": "Asimetría",
        "kurtosis": "Curtosis",
        "IQR": "RIC",
    }

    # Rename the rows of the DataFrame
    df.rename(index=spanish_descriptors, inplace=True)
    return df


def generate_domain_df(df):
    # Crear listas vacías para almacenar los nombres de las columnas y los dominios
    column_names = []
    domains = []

    # Iterar sobre cada columna en el DataFrame
    for column in df.columns:
        # Agregar el nombre de la columna a la lista de nombres de columnas
        column_names.append(column)

        # Calcular el dominio de la columna y agregarlo a la lista de dominios
        domain = len(df[column].unique())
        domains.append(domain)

    # Crear un nuevo DataFrame con las listas de nombres de columnas y dominios
    domain_df = pd.DataFrame({"Columna": column_names, "Dominio": domains})

    return domain_df
