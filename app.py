import pandas as pd
import plotly.express as px
import streamlit as st

from charts.hdi import get_hdi_charts
from charts.income import get_income_charts
from charts.olympics import get_olympics_charts
from charts.schooling import get_schooling_charts
from statistics_calc import descriptors, qualitative_stats


def load_and_display_data(title, filename):
    st.markdown(f"## :red[{title}]")
    data = pd.read_csv(f"datasets/{filename}")
    st.dataframe(data, hide_index=True, use_container_width=True)
    st.caption(
        f"Total de filas: **{data.shape[0]}** | Total de columnas: **{data.shape[1]}**"
    )

    col1, col2 = st.columns(2)

    st.markdown("### Variables cualitativas")
    qualitative_vars = data.select_dtypes(include=["object"]).columns.tolist()
    qualitative = qualitative_stats(data, qualitative_vars)
    st.dataframe(qualitative, hide_index=True, use_container_width=True)

    st.markdown("### Variables cuantitativas")
    data_descriptors = descriptors(data)
    st.dataframe(data_descriptors, hide_index=False, use_container_width=True)

    st.markdown("## :green[Valores únicos]")
    # Add a selectbox for the user to select a column
    selected_column = st.selectbox(
        "Selecciona una columna para ver sus valores únicos", data.columns
    )

    # Display all unique values of the selected column
    st.write(f"Valores únicos para {selected_column}:")

    # Get all unique values of the selected column
    unique_values = data[selected_column].unique()

    # Convert the unique values to a DataFrame
    unique_values_df = pd.DataFrame(unique_values, columns=[selected_column])

    # Display the DataFrame
    st.dataframe(unique_values_df, use_container_width=True)
    st.write(f"Total de valores únicos: **{len(unique_values)}**")

    st.markdown("## :violet[Graficar]")
    # Add a selectbox for the user to select a plot type
    plot_types = ["Histograma", "Box Plot", "Scatter Plot"]
    selected_plot = st.selectbox("Selecciona un tipo de gráfico", plot_types)

    # Add a selectbox for the user to select a quantitative variable
    quantitative_vars = [col for col in data.columns if col not in qualitative_vars]
    selected_var = st.selectbox(
        "Selecciona una variable para generar un gráfico", quantitative_vars
    )

    # Plot the selected plot type
    if selected_plot == "Histograma":
        fig = px.histogram(
            data,
            x=selected_var,
            nbins=50,
            labels={"x": selected_var, "y": "Frecuencia"},
            text_auto=True,
        )
        fig.update_xaxes(title_text=selected_var)
        fig.update_yaxes(title_text="Frecuencia")
    elif selected_plot == "Box Plot":
        fig = px.box(data, x=selected_var)
        fig.update_xaxes(title_text=selected_var)
        fig.update_yaxes(title_text="Value")
    elif selected_plot == "Scatter Plot":
        selected_var2 = st.selectbox(
            "Selecciona una segunda variable para el gráfico de dispersión",
            quantitative_vars,
        )
        fig = px.scatter(data, x=selected_var, y=selected_var2)
        fig.update_xaxes(title_text=selected_var)
        fig.update_yaxes(title_text=selected_var2)

    fig.update_layout(title_text=f"{selected_plot} de {selected_var}", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    if title == "🏅 Olympics":
        get_olympics_charts(data)
    elif title == "🎓 Schooling":
        get_schooling_charts(data)
    elif title == "💰 Income":
        get_income_charts(data)
    elif title == "🌍 Human Development Index (HDI)":
        get_hdi_charts(data)


def main():
    st.set_page_config(page_title="Datamart data", page_icon="📊", layout="wide")

    with st.sidebar:
        # Define the datasets and their corresponding titles and qualitative variables
        chosen_datasets = {
            "🏅 Olympics": "olympics_spanish.csv",
            "🎓 Schooling": "expected-years-of-schooling.csv",
            "💰 Income": "gross-national-income-per-capita.csv",
            "🌍 Human Development Index (HDI)": "human-development-index.csv",
            "📊 Historical Index of Human Development (HIHD)": "hdi-vs-hihd.csv",
        }

        other_datasets = {
            "🔄 HDI Comparison": "human-development-index-comparison.csv",
            "💹 HDI vs. GDP per capita": "hdi-vs-gdp-per-capita.csv",
            "🌐 HDI Without GDP vs GDP per capita": "hdi-without-gdp-vs-gdp-per-capita.csv",
            "📈 HDI - Escosura": "human-development-index-escosura.csv",
            "📚 Mean Years of Schooling Long Run": "mean-years-of-schooling-long-run.csv",
        }

        st.markdown("# 📊 Datamart data")
        st.markdown(
            "Los siguientes datos no han sido modificados y se presentan tal como se encuentran en los archivos `csv`."
        )

        st.warning(
            "⚠️ **IMPORTANTE:** Considerar que se usa un punto para valores decimales y una coma para separar miles."
        )

        st.info("📢 **Nota:** La carga de un `scatter plot` puede tomar tiempo.")

        only_chosen_datasets = st.toggle(
            "Mostrar solo los datasets seleccionados",
            value=True,
            help="Mostrar solo los datasets que hayan sido seleccionados para el análisis o incluir todos los datasets disponibles.",
        )

        # Add a selectbox for the user to select a dataset
        datasets = (
            chosen_datasets
            if only_chosen_datasets
            else {**chosen_datasets, **other_datasets}
        )
        selected_dataset = st.selectbox("Elige un dataset", list(datasets.keys()))

        st.divider()

        st.button(
            "Limpiar cache",
            on_click=st.cache_data.clear(),
            type="primary",
            use_container_width=True,
        )
        st.caption(
            "_Limpiar el cache de los graficos de interes. Solo utilizar en caso de ser necesario._"
        )

    # Load and display the selected dataset
    filename = datasets[selected_dataset]

    load_and_display_data(selected_dataset, filename)


if __name__ == "__main__":
    main()
