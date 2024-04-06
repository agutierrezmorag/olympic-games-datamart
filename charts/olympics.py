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
        fig.update_traces(textinfo="label+percent")
        st.plotly_chart(fig)

    # Create a pie chart to show the distribution of athletes across different Olympic seasons
    with col2:
        season_distribution = data["Temporada"].value_counts().reset_index()
        season_distribution.columns = ["Temporada", "Count"]

        fig = px.pie(
            season_distribution,
            names="Temporada",
            values="Count",
            title="Distribución de atletas por temporada olímpica",
            labels={"Season": "Temporada", "Count": "Número de atletas"},
        )

        fig.update_traces(textinfo="label+percent")
        st.plotly_chart(fig)

    # Create a bar chart to show the total number of medals won by each country
    with col1:
        medal_distribution = (
            data[data["Medalla"].notna()]["NOC"].value_counts().reset_index()
        )
        medal_distribution.columns = ["NOC", "Count"]

        fig = px.bar(
            medal_distribution,
            x="NOC",
            y="Count",
            title="Medallas ganadas por país",
            labels={"NOC": "País", "Count": "Número de medallas"},
            text_auto=True,
            color="Count",
            color_continuous_scale=px.colors.sequential.Viridis,
        )

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

    # Create a bar chart to show the distribution of medal types within each sport
    with col1:
        medal_distribution = (
            data[data["Medalla"].isin(["Bronce", "Plata", "Oro"])]
            .groupby(["Deporte", "Medalla"])["Medalla"]
            .count()
            .unstack()
            .reset_index()
        )
        medal_distribution.columns = ["Deporte", "Bronce", "Plata", "Oro"]
        medal_distribution["Total"] = medal_distribution[
            ["Bronce", "Plata", "Oro"]
        ].sum(axis=1)
        medal_distribution = medal_distribution.sort_values("Total", ascending=False)

        fig = px.bar(
            medal_distribution,
            x="Deporte",
            y=["Bronce", "Plata", "Oro"],
            title="Distribución de tipos de medallas dentro de cada deporte",
            labels={
                "value": "Número de medallas",
                "variable": "Tipo de medalla",
                "Deporte": "Deporte",
            },
            barmode="stack",
            text_auto=True,
        )

        st.plotly_chart(fig)
