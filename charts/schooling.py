import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def get_schooling_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    with col1:
        # Find the latest year in the data
        latest_year = data["Año"].max()

        # Filter the data to only include the latest year
        data_latest_year = data[data["Año"] == latest_year]

        # Add a choropleth map showing the expected years of schooling
        fig = px.choropleth(
            data_latest_year,
            title="Años de escolaridad esperados (1990)",
            locations="Entidad",
            locationmode="country names",
            color="Años de escolaridad esperados",
            hover_name="Entidad",
            color_continuous_scale="Viridis",
            range_color=(5, 20),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Find the earliest year in the data
        earliest_year = data["Año"].min()

        # Filter the data to only include the earliest year
        data_earliest_year = data[data["Año"] == earliest_year]

        # Add a choropleth map showing the expected years of schooling
        fig = px.choropleth(
            data_earliest_year,
            title="Años de escolaridad esperados (2017)",
            locations="Entidad",
            locationmode="country names",
            color="Años de escolaridad esperados",
            hover_name="Entidad",
            color_continuous_scale="Viridis",
            range_color=(5, 20),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Add a bar chart showing the top countries with the highest expected years of schooling in 1990
    with col1:
        fig = px.bar(
            data_earliest_year.nlargest(10, "Años de escolaridad esperados"),
            x="Años de escolaridad esperados",
            y="Entidad",
            title="Top 10 países con mayor años de escolaridad esperados (1990)",
            orientation="h",
            text="Años de escolaridad esperados",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Add a bar chart showing the top countries with the highest expected years of schooling in 2017
    with col2:
        fig = px.bar(
            data_latest_year.nlargest(10, "Años de escolaridad esperados"),
            x="Años de escolaridad esperados",
            y="Entidad",
            title="Top 10 países con mayor años de escolaridad esperados (2017)",
            orientation="h",
            text="Años de escolaridad esperados",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Identify the top 10 countries in 1990 and 2017
    top_countries_1990 = data_earliest_year.nlargest(
        10, "Años de escolaridad esperados"
    )["Entidad"]
    top_countries_2017 = data_latest_year.nlargest(10, "Años de escolaridad esperados")[
        "Entidad"
    ]

    # Combine the two sets of countries
    top_countries = pd.concat([top_countries_1990, top_countries_2017]).unique()

    # Filter the original data to only include these countries
    data_top_countries = data[data["Entidad"].isin(top_countries)]

    # Create a line chart
    fig = px.line(
        data_top_countries,
        x="Año",
        y="Años de escolaridad esperados",
        color="Entidad",
        title="Differences in Expected Years of Schooling Over Time",
        labels={
            "Año": "Year",
            "Años de escolaridad esperados": "Expected Years of Schooling",
            "Entidad": "Country",
        },
    )
    st.plotly_chart(fig, use_container_width=True)
