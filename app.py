import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from statistics_calc import descriptors, qualitative_stats


def load_and_display_data(title, filename, qualitative_vars):
    st.markdown(f"## {title}")
    data = pd.read_csv(f"datasets/{filename}")
    st.dataframe(data, hide_index=True, use_container_width=True)

    st.markdown("### Variables cualitativas")
    qualitative = qualitative_stats(data, qualitative_vars)
    st.dataframe(qualitative, hide_index=True, use_container_width=True)

    st.markdown("### Variables cuantitativas")
    data_descriptors = descriptors(data)
    st.dataframe(data_descriptors, hide_index=False, use_container_width=True)

    # Add a selectbox for the user to select a quantitative variable
    quantitative_vars = [col for col in data.columns if col not in qualitative_vars]
    selected_var = st.selectbox(
        "Selecciona una variable para generar un histograma", quantitative_vars
    )

    # Plot a histogram of the selected variable
    fig, ax = plt.subplots()
    data[selected_var].hist(ax=ax, label="Frecuencia")  # Add a label for the legend
    ax.set_title(f"Histograma de {selected_var}")
    ax.set_xlabel(selected_var)  # Add x-label
    ax.set_ylabel("Frecuencia")  # Add y-label
    ax.legend()  # Display the legend
    st.pyplot(fig)


def main():
    st.set_page_config(page_title="Datamart data", page_icon="📊")

    # Define the datasets and their corresponding titles and qualitative variables
    datasets = {
        "🏅 Olympics data": (
            "olympics.csv",
            ["Team", "NOC", "Games", "Sport", "Event", "Medal"],
        ),
        "📚 Schooling data": ("expected-years-of-schooling.csv", ["Entity", "Code"]),
        "🪙 Income data": ("gross-national-income-per-capita.csv", ["Entity", "Code"]),
        "🌍 Human Development Index (HDI) data": (
            "human-development-index.csv",
            ["Entity", "Code"],
        ),
        "📈 Historical Index of Human Development (HIHD) data": (
            "hdi-vs-hihd.csv",
            ["Entity", "Code"],
        ),
    }

    with st.sidebar:
        st.markdown("# 📊 Datamart data")
        st.markdown(
            "Los siguientes datos no han sido modificados y se presentan tal como se encuentran en el archivo `csv`."
        )

        st.info(
            "📢 **Nota:** Considerar que se usa un punto en vez de una coma para valores decimales."
        )
        # Add a selectbox for the user to select a dataset
        selected_dataset = st.selectbox("Elige un dataset", list(datasets.keys()))

        # Load and display the selected dataset
        filename, qualitative_vars = datasets[selected_dataset]

    load_and_display_data(selected_dataset, filename, qualitative_vars)


if __name__ == "__main__":
    main()
