import plotly.express as px
import streamlit as st


def get_schooling_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    # Add a line chart for Expected years of schooling over the years
    with col1:
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
    with col2:
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
    with col1:
        fig = px.histogram(
            data,
            x="Expected Years of Schooling (years)",
            title="Histograma de años de escolaridad esperados",
            labels={
                "Expected Years of Schooling (years)": "Años de escolaridad esperados",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    # Add a scatter plot for Expected years of schooling by Year for each Entity
    with col2:
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
