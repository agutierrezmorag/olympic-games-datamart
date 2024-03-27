import plotly.express as px
import streamlit as st


def get_income_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    with col1:
        # Get the latest year data
        latest_year_data = data[data["Year"] == data["Year"].max()]

        # Plot GNI per capita for each entity in the latest year
        fig = px.bar(
            latest_year_data,
            x="Entity",
            y="GNI per capita, PPP (constant 2017 international $)",
            title="GNI per Capita in the Latest Year for Each Entity",
            labels={
                "Entity": "Entity",
                "GNI per capita, PPP (constant 2017 international $)": "GNI per capita, PPP (constant 2017 international $)",
            },
        )
        st.plotly_chart(fig, use_container_width=True)
