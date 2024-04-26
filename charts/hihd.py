import plotly.express as px
import streamlit as st


def get_hihd_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    # Choropleth map of HIHD in early times
    with col1:
        # Find the earliest year in the data
        earliest_year = data["Year"].max()

        # Filter the data to only include the earliest year
        data_earliest_year = data[data["Year"] == earliest_year]

        st.dataframe(data_earliest_year)

        # Add a choropleth map showing the historical index of human development
        fig = px.choropleth(
            data_earliest_year,
            title=f"Índice Histórico de Desarrollo Humano en {earliest_year}",
            locations="Entity",
            locationmode="country names",
            color="Population (historical estimates)",
            hover_name="Entity",
            color_continuous_scale="Viridis",
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
        )
        st.plotly_chart(fig, use_container_width=True)
