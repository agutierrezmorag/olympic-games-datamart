import plotly.express as px
import streamlit as st


def get_income_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    # Choropleth map of income in early times
    with col1:
        # Find the earliest year in the data
        earliest_year = data["Year"].min()

        # Filter the data to only include the earliest year
        data_earliest_year = data[data["Year"] == earliest_year]

        # Add a choropleth map showing the gross national income per capita
        fig = px.choropleth(
            data_earliest_year,
            title=f"GNI per capita, PPP (constant 2017 international $) en {earliest_year}",
            locations="Entity",
            locationmode="country names",
            color="GNI per capita, PPP (constant 2017 international $)",
            hover_name="Entity",
            color_continuous_scale="Viridis",
            range_color=(10_000, 100_000),
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Add a bar chart showing the top countries with the highest income
        fig = px.bar(
            data_earliest_year.nlargest(
                10, "GNI per capita, PPP (constant 2017 international $)"
            ),
            x="GNI per capita, PPP (constant 2017 international $)",
            y="Entity",
            title=f"Top 10 países con mayor GNI per capita, PPP (constant 2017 international $) en {earliest_year}",
            orientation="h",
            text=data_earliest_year.nlargest(
                10, "GNI per capita, PPP (constant 2017 international $)"
            )["GNI per capita, PPP (constant 2017 international $)"].round(2),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Choropleth map of income in modern times
    with col2:
        st.caption(
            "Si bien el ultimo Year del dataset es 2020, se muestra el Year 2017, ya que este es el último Year con datos de todos los países."
        )
        # Find the latest year in the data
        latest_year = 2017

        # Filter the data to only include the latest year
        data_latest_year = data[data["Year"] == latest_year]

        # Add a choropleth map showing the gross national income per capita
        fig = px.choropleth(
            data_latest_year,
            title=f"GNI per capita, PPP (constant 2017 international $) en {latest_year}",
            locations="Entity",
            locationmode="country names",
            color="GNI per capita, PPP (constant 2017 international $)",
            hover_name="Entity",
            color_continuous_scale="Viridis",
            range_color=(10_000, 100_000),
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Add a bar chart showing the top countries with the highest income
        fig = px.bar(
            data_latest_year.nlargest(
                10, "GNI per capita, PPP (constant 2017 international $)"
            ),
            x="GNI per capita, PPP (constant 2017 international $)",
            y="Entity",
            title=f"Top 10 países con mayor GNI per capita, PPP (constant 2017 international $) en {latest_year}",
            orientation="h",
            text=data_latest_year.nlargest(
                10, "GNI per capita, PPP (constant 2017 international $)"
            )["GNI per capita, PPP (constant 2017 international $)"].round(2),
        )
        st.plotly_chart(fig, use_container_width=True)
