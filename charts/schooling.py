import plotly.express as px
import streamlit as st


@st.cache_data
def get_schooling_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    # Add a line chart for Expected years of schooling over the years
    fig = px.line(
        data,
        x="Year",
        y="Expected Years of Schooling (years)",
        title="Años de escolaridad esperados a lo largo de los años",
        labels={
            "Year": "Año",
            "Expected Years of Schooling (years)": "Años de escolaridad esperados",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

    # Add a bar chart for Expected years of schooling by Entity
    fig = px.bar(
        data,
        x="Entity",
        y="Expected Years of Schooling (years)",
        title="Años de escolaridad esperados por entidad",
        labels={
            "Entity": "Entidad",
            "Expected Years of Schooling (years)": "Años de escolaridad esperados",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

    # Add a histogram for Expected years of schooling
    fig = px.histogram(
        data,
        x="Expected Years of Schooling (years)",
        title="Histograma de años de escolaridad esperados",
        labels={
            "Expected Years of Schooling (years)": "Años de escolaridad esperados",
        },
        text_auto=True,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Add a scatter plot for Expected years of schooling by Year for each Entity
    fig = px.scatter(
        data,
        x="Year",
        y="Expected Years of Schooling (years)",
        color="Entity",
        title="Años de escolaridad esperados por año para cada entidad",
        labels={
            "Year": "Año",
            "Expected Years of Schooling (years)": "Años de escolaridad esperados",
            "Entity": "Entidad",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

    # Get the latest year data
    latest_year_data = data[data["Year"] == data["Year"].max()]

    # Sort by "Expected Years of Schooling (years)" and get the top 10 entities
    top_entities = latest_year_data.sort_values(
        by="Expected Years of Schooling (years)", ascending=False
    ).head(10)

    # Add a bar chart for Expected years of schooling for the latest year for top 10 entities
    fig = px.bar(
        top_entities,
        x="Entity",
        y="Expected Years of Schooling (years)",
        title="Top 10 entidades con mayor años de escolaridad esperados en el último año",
        labels={
            "Entity": "Entidad",
            "Expected Years of Schooling (years)": "Años de escolaridad esperados",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

    # Add a box plot for Expected years of schooling for each Entity
    fig = px.box(
        data,
        x="Entity",
        y="Expected Years of Schooling (years)",
        title="Diagrama de caja de años de escolaridad esperados por entidad",
        labels={
            "Entity": "Entidad",
            "Expected Years of Schooling (years)": "Años de escolaridad esperados",
        },
    )
    st.plotly_chart(fig, use_container_width=True)
