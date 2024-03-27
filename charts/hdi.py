import plotly.express as px
import streamlit as st


def get_hdi_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    # Line chart of HDI over the years for the selected entity
    with col1:
        # Get a list of unique entities in the HDI data
        entities_hdi = sorted(data["Entity"].unique())

        # Create a select box for the entities in the HDI data
        selected_entity_hdi = st.selectbox(
            "Selecciona una entidad para el Índice de Desarrollo Humano", entities_hdi
        )

        # Filter HDI data for the selected entity
        entity_data_hdi = data[data["Entity"] == selected_entity_hdi]

        fig_hdi_line = px.line(
            entity_data_hdi,
            x="Year",
            y="Human Development Index (UNDP)",
            title=f"Índice de Desarrollo Humano en {selected_entity_hdi}",
            labels={
                "Year": "Año",
                "Human Development Index (UNDP)": "Indice de Desarrollo Humano (IDH)",
            },
        )
        st.plotly_chart(fig_hdi_line, use_container_width=True)

    with col2:
        # Get the latest year in the data
        latest_year_hdi = data["Year"].max()

        # Filter data for the latest year
        latest_year_data_hdi = data[data["Year"] == latest_year_hdi]

        # Histogram of HDI in the latest year
        fig_hdi_hist = px.histogram(
            latest_year_data_hdi,
            x="Human Development Index (UNDP)",
            title=f"Distribución del Índice de Desarrollo Humano en {latest_year_hdi}",
            labels={
                "Human Development Index (UNDP)": "Indice de Desarrollo Humano (IDH)",
            },
        )
        st.plotly_chart(fig_hdi_hist, use_container_width=True)

    with col1:
        # Histogram of HDI through the years
        fig_hdi_hist_years = px.histogram(
            data,
            x="Year",
            y="Human Development Index (UNDP)",
            histfunc="avg",
            title="Promedio del Índice de Desarrollo Humano a lo largo de los años",
            labels={
                "Year": "Año",
                "Human Development Index (UNDP)": "Indice de Desarrollo Humano (IDH)",
            },
            text_auto=True,
        )
        st.plotly_chart(fig_hdi_hist_years, use_container_width=True)
