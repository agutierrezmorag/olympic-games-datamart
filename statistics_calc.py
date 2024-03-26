import numpy as np
import pandas as pd


def qualitative_stats(data, cols_cualitativas):
    # Crear un DataFrame vacío para almacenar las estadísticas
    estadisticas = pd.DataFrame(
        columns=[
            "Columna",
            "Moda",
            "Moda (#)",
            "Moda (%)",
            "Valores unicos (#)",
            "Valores unicos (%)",
            "Valores nulos (%)",
        ]
    )

    for col in cols_cualitativas:
        # Moda
        moda = data[col].mode()[0]

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
                "Valores unicos (#)": [valores_unicos],
                "Valores unicos (%)": [valor_porcentajes],
                "Valores nulos (%)": [porcentaje_nulos],
            }
        )
        estadisticas = pd.concat([estadisticas, nueva_fila], ignore_index=True)

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

    # Append skewness and kurtosis to the description
    desc = pd.concat([desc, skewness, kurtosis, iqr])

    return desc
