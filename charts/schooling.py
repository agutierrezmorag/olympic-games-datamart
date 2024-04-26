import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def get_schooling_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    with col1:
        # Find the earliest year in the data
        earliest_year = data["Year"].min()

        # Filter the data to only include the earliest year
        data_earliest_year = data[data["Year"] == earliest_year]

        # Add a choropleth map showing the expected years of schooling
        fig = px.choropleth(
            data_earliest_year,
            title="Expected Years of Schooling (years) (1990)",
            locations="Entity",
            locationmode="country names",
            color="Expected Years of Schooling (years)",
            hover_name="Entity",
            color_continuous_scale="Viridis",
            range_color=(5, 20),
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Add a bar chart showing the top countries with the highest expected years of schooling in 1990
        fig = px.bar(
            data_earliest_year.nlargest(10, "Expected Years of Schooling (years)"),
            x="Expected Years of Schooling (years)",
            y="Entity",
            title="Top 10 países con mayor Expected Years of Schooling (years) (1990)",
            orientation="h",
            text="Expected Years of Schooling (years)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Find the latest year in the data
        latest_year = data["Year"].max()

        # Filter the data to only include the latest year
        data_latest_year = data[data["Year"] == latest_year]

        # Add a choropleth map showing the expected years of schooling
        fig = px.choropleth(
            data_latest_year,
            title="Expected Years of Schooling (years) (2017)",
            locations="Entity",
            locationmode="country names",
            color="Expected Years of Schooling (years)",
            hover_name="Entity",
            color_continuous_scale="Viridis",
            range_color=(5, 20),
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Add a bar chart showing the top countries with the highest expected years of schooling in 2017
        fig = px.bar(
            data_latest_year.nlargest(10, "Expected Years of Schooling (years)"),
            x="Expected Years of Schooling (years)",
            y="Entity",
            title="Top 10 países con mayor Expected Years of Schooling (years) (2017)",
            orientation="h",
            text="Expected Years of Schooling (years)",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Identify the top 10 countries in 1990 and 2017
    top_countries_1990 = data_earliest_year.nlargest(
        10, "Expected Years of Schooling (years)"
    )["Entity"]
    top_countries_2017 = data_latest_year.nlargest(
        10, "Expected Years of Schooling (years)"
    )["Entity"]

    # Combine the two sets of countries
    top_countries = pd.concat([top_countries_1990, top_countries_2017]).unique()

    # Filter the original data to only include these countries
    data_top_countries = data[data["Entity"].isin(top_countries)]

    # Create a line chart
    fig = px.line(
        data_top_countries,
        x="Year",
        y="Expected Years of Schooling (years)",
        color="Entity",
        title="Diferencia en Expected Years of Schooling (years) entre 1990 y 2017",
        labels={
            "Year": "Year",
            "Expected Years of Schooling (years)": "Expected Years of Schooling (years)",
            "Entity": "Entity",
        },
    )
    st.plotly_chart(fig, use_container_width=True)
