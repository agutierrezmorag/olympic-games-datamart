import plotly.express as px
import streamlit as st


@st.cache_data
def get_olympics_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    # add a pie chart to show gender distribution
    with col1:
        gender_distribution = data["Sexo"].value_counts()
        fig = px.pie(
            names=gender_distribution.index,
            values=gender_distribution.values,
            title="Distribución de género",
            labels={"names": "Sexo", "values": "Total"},
        )
        fig.update_traces(textinfo="label+value")
        st.plotly_chart(fig)

    # Create a choropleth map to show the distribution of athletes by country
    with col2:
        country_distribution = data["NOC"].value_counts().reset_index()
        country_distribution.columns = ["NOC", "Count"]
        fig = px.choropleth(
            country_distribution,
            locations="NOC",
            color="Count",
            title="Distribución de atletas por país",
            labels={"NOC": "Pais", "Count": "Número de atletas"},
            color_continuous_scale=px.colors.sequential.Greens,
        )
        st.plotly_chart(fig)
