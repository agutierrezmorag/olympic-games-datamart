import plotly.express as px
import streamlit as st


def get_income_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    # Choropleth map of income in early times
    with col1:
        # Find the earliest year in the data
        earliest_year = data["Año"].min()

        # Filter the data to only include the earliest year
        data_earliest_year = data[data["Año"] == earliest_year]

        # Add a choropleth map showing the gross national income per capita
        fig = px.choropleth(
            data_earliest_year,
            title=f"Ingreso Nacional Bruto per cápita en {earliest_year}",
            locations="Entidad",
            locationmode="country names",
            color="Ingreso Nacional Bruto per cápita",
            hover_name="Entidad",
            color_continuous_scale="Viridis",
            range_color=(10_000, 100_000),
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
            projection_type="natural earth",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Add a bar chart showing the top countries with the highest income
        fig = px.bar(
            data_earliest_year.nlargest(10, "Ingreso Nacional Bruto per cápita"),
            x="Ingreso Nacional Bruto per cápita",
            y="Entidad",
            title=f"Top 10 países con mayor ingreso nacional bruto per cápita en {earliest_year}",
            orientation="h",
            text=data_earliest_year.nlargest(10, "Ingreso Nacional Bruto per cápita")[
                "Ingreso Nacional Bruto per cápita"
            ].round(2),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Choropleth map of income in modern times
    with col2:
        st.caption(
            "Si bien el ultimo año del dataset es 2020, se muestra el año 2017, ya que este es el último año con datos de todos los países."
        )
        # Find the latest year in the data
        latest_year = 2017

        # Filter the data to only include the latest year
        data_latest_year = data[data["Año"] == latest_year]

        # Add a choropleth map showing the gross national income per capita
        fig = px.choropleth(
            data_latest_year,
            title=f"Ingreso Nacional Bruto per cápita en {latest_year}",
            locations="Entidad",
            locationmode="country names",
            color="Ingreso Nacional Bruto per cápita",
            hover_name="Entidad",
            color_continuous_scale="Viridis",
            range_color=(10_000, 100_000),
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
            projection_type="natural earth",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Add a bar chart showing the top countries with the highest income
        fig = px.bar(
            data_latest_year.nlargest(10, "Ingreso Nacional Bruto per cápita"),
            x="Ingreso Nacional Bruto per cápita",
            y="Entidad",
            title=f"Top 10 países con mayor ingreso nacional bruto per cápita en {latest_year}",
            orientation="h",
            text=data_latest_year.nlargest(10, "Ingreso Nacional Bruto per cápita")[
                "Ingreso Nacional Bruto per cápita"
            ].round(2),
        )
        st.plotly_chart(fig, use_container_width=True)
