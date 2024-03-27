import plotly.express as px
import streamlit as st


def get_income_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    # Get the latest year data
    latest_year_data = data[data["Year"] == data["Year"].max()]

    # Plot GNI per capita for each entity in the latest year
    with col1:
        fig = px.bar(
            latest_year_data,
            x="Entity",
            y="GNI per capita, PPP (constant 2017 international $)",
            title="GNI per cápita por entidad en el último año",
            labels={
                "Entity": "Entity",
                "GNI per capita, PPP (constant 2017 international $)": "GNI per capita, PPP (constant 2017 international $)",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    # Plot GNI per capita for the entities with the lowest GNI per capita
    with col2:
        lowest_gni = latest_year_data.nsmallest(
            10, "GNI per capita, PPP (constant 2017 international $)"
        )
        fig = px.bar(
            lowest_gni,
            x="Entity",
            y="GNI per capita, PPP (constant 2017 international $)",
            title="10 entidades con el GNI per cápita más bajo en el último año",
            labels={
                "Entity": "Entity",
                "GNI per capita, PPP (constant 2017 international $)": "GNI per capita, PPP (constant 2017 international $)",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    # Plot GNI per capita for the entities with the highest GNI per capita
    with col1:
        highest_gni = latest_year_data.nlargest(
            10, "GNI per capita, PPP (constant 2017 international $)"
        )
        fig = px.bar(
            highest_gni,
            x="Entity",
            y="GNI per capita, PPP (constant 2017 international $)",
            title="10 entidades con el GNI per cápita más alto en el último año",
            labels={
                "Entity": "Entity",
                "GNI per capita, PPP (constant 2017 international $)": "GNI per capita, PPP (constant 2017 international $)",
            },
        )
        st.plotly_chart(fig, use_container_width=True)
