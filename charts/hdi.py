import plotly.express as px
import streamlit as st


def get_hdi_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    # Choropleth map of HDI in early times
    with col1:
        # Find the earliest year in the data
        earliest_year = data["Año"].min()

        # Filter the data to only include the earliest year
        data_earliest_year = data[data["Año"] == earliest_year]

        # Add a choropleth map showing the expected years of schooling
        fig = px.choropleth(
            data_earliest_year,
            title=f"Índice de Desarrollo Humano en {earliest_year}",
            locations="Entidad",
            locationmode="country names",
            color="Índice de Desarrollo Humano (PNUD)",
            hover_name="Entidad",
            color_continuous_scale="Viridis",
            range_color=(0, 1),
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
            projection_type="natural earth",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Add a bar chart showing the top countries with the highest hdi
        fig = px.bar(
            data_earliest_year.nlargest(10, "Índice de Desarrollo Humano (PNUD)"),
            x="Índice de Desarrollo Humano (PNUD)",
            y="Entidad",
            title=f"Top 10 países con mayor indice de desarrollo humano en {earliest_year}",
            orientation="h",
            text="Índice de Desarrollo Humano (PNUD)",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Choropleth map of HDI in modern times
    with col2:
        # Find the latest year in the data
        latest_year = data["Año"].max()

        # Filter the data to only include the latest year
        data_latest_year = data[data["Año"] == latest_year]

        # Add a choropleth map showing the expected years of schooling
        fig = px.choropleth(
            data_latest_year,
            title=f"Índice de Desarrollo Humano en {latest_year}",
            locations="Entidad",
            locationmode="country names",
            color="Índice de Desarrollo Humano (PNUD)",
            hover_name="Entidad",
            color_continuous_scale="Viridis",
            range_color=(0, 1),
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
            projection_type="natural earth",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Add a bar chart showing the top countries with the highest hdi
        fig = px.bar(
            data_latest_year.nlargest(10, "Índice de Desarrollo Humano (PNUD)"),
            x="Índice de Desarrollo Humano (PNUD)",
            y="Entidad",
            title=f"Top 10 países con mayor indice de desarrollo humano en {latest_year}",
            orientation="h",
            text="Índice de Desarrollo Humano (PNUD)",
        )
        st.plotly_chart(fig, use_container_width=True)
