import plotly.express as px
import streamlit as st


def get_olympics_charts(data):
    # Add a pie chart for the 'Sex' column in the 'Olympics data' dataset
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(data, names="Sex", title="Distribución de Sexo")
        st.plotly_chart(fig)

    with col2:
        medal_count = data.groupby("NOC")["Medal"].count().sort_values(ascending=False)
        fig = px.bar(
            medal_count,
            x=medal_count.index,
            y=medal_count.values,
            labels={"x": "País", "y": "Recuento de Medallas"},
            title="Recuento de Medallas por País",
        )
        st.plotly_chart(fig)

    with col1:
        medals_by_year_country = (
            data[data["Medal"].notna()]
            .groupby(["Year", "NOC"])["Medal"]
            .count()
            .reset_index()
        )
        fig = px.line(
            medals_by_year_country,
            x="Year",
            y="Medal",
            color="NOC",
            title="Medals by Year and Country",
        )
        st.plotly_chart(fig)

    with col2:
        athlete_count = data.groupby("Year")["ID"].nunique()
        fig = px.line(
            athlete_count,
            x=athlete_count.index,
            y=athlete_count.values,
            labels={"x": "Año", "y": "Número de Atletas"},
            title="Participación de Atletas a lo Largo del Tiempo",
        )
        st.plotly_chart(fig)

    with col1:
        gender_count = data.groupby(["Year", "Sex"])["ID"].nunique().unstack()
        fig = px.area(
            gender_count,
            labels={
                "value": "Número de Atletas",
                "variable": "Sexo",
                "Year": "Año",
            },
            title="Distribución de Género a lo Largo del Tiempo",
        )
        st.plotly_chart(fig)

    with col2:
        medals_by_sex = data[data["Medal"].notna()].groupby("Sex")["Medal"].count()
        fig = px.bar(
            medals_by_sex,
            x=medals_by_sex.index,
            y=medals_by_sex.values,
            labels={"x": "Sexo", "y": "Recuento de Medallas"},
            title="Recuento de Medallas por Sexo",
        )
        st.plotly_chart(fig)

    # Bar chart showing the top 10 countries with the most athletes
    with col1:
        athlete_country_count = data["NOC"].value_counts().head(10)
        fig = px.bar(
            athlete_country_count,
            x=athlete_country_count.index,
            y=athlete_country_count.values,
            labels={"x": "País", "y": "Número de Atletas"},
            title="Los 10 países con más atletas",
        )
        st.plotly_chart(fig)

    # Line chart showing the trend of the total number of medals won by year
    with col2:
        medals_by_year = data[data["Medal"].notna()].groupby("Year")["Medal"].count()
        fig = px.line(
            medals_by_year,
            x=medals_by_year.index,
            y=medals_by_year.values,
            labels={"x": "Año", "y": "Número de Medallas"},
            title="Tendencia de medallas totales ganadas por año",
        )
        st.plotly_chart(fig)

    # Pie chart showing the distribution of different types of medals
    with col1:
        medal_types = data["Medal"].value_counts()
        fig = px.pie(
            medal_types,
            names=medal_types.index,
            values=medal_types.values,
            title="Distribución de tipos de medallas",
        )
        st.plotly_chart(fig)

    # Scatter plot showing the relationship between the year and the number of medals won
    with col2:
        medals_by_year = (
            data[data["Medal"].notna()].groupby("Year")["Medal"].count().reset_index()
        )
        fig = px.scatter(
            medals_by_year,
            x="Year",
            y="Medal",
            labels={"x": "Año", "y": "Número de Medallas"},
            title="Relación entre el año y el número de medallas ganadas",
        )
        st.plotly_chart(fig)

    # Bar chart showing the top 10 athletes with the most medals
    with col1:
        athlete_medal_count = (
            data[data["Medal"].notna()]["Name"].value_counts().head(10)
        )
        fig = px.bar(
            athlete_medal_count,
            x=athlete_medal_count.index,
            y=athlete_medal_count.values,
            labels={"x": "Atleta", "y": "Número de Medallas"},
            title="Los 10 atletas con más medallas",
        )
        st.plotly_chart(fig)

    # Line chart showing the trend of the total number of athletes participating each year
    with col2:
        athletes_by_year = data.groupby("Year")["ID"].nunique()
        fig = px.line(
            athletes_by_year,
            x=athletes_by_year.index,
            y=athletes_by_year.values,
            labels={"x": "Año", "y": "Número de Atletas"},
            title="Tendencia del número total de atletas participantes cada año",
        )
        st.plotly_chart(fig)

    # Pie chart showing the distribution of athletes by sport
    with col1:
        sport_distribution = data["Sport"].value_counts().head(10)
        fig = px.pie(
            sport_distribution,
            names=sport_distribution.index,
            values=sport_distribution.values,
            title="Distribución de atletas por deporte (Top 10)",
        )
        st.plotly_chart(fig)

    # Scatter plot showing the relationship between the age of athletes and the number of medals they won
    with col2:
        athlete_age_medals = (
            data[data["Medal"].notna()].groupby("Age")["Medal"].count().reset_index()
        )
        fig = px.scatter(
            athlete_age_medals,
            x="Age",
            y="Medal",
            labels={"x": "Edad", "y": "Número de Medallas"},
            title="Relación entre la edad de los atletas y el número de medallas que ganaron",
        )
        st.plotly_chart(fig)

    # Bar chart showing the top 10 sports with the most medals
    with col1:
        sport_medal_count = data[data["Medal"].notna()]["Sport"].value_counts().head(10)
        fig = px.bar(
            sport_medal_count,
            x=sport_medal_count.index,
            y=sport_medal_count.values,
            labels={"x": "Deporte", "y": "Número de Medallas"},
            title="Los 10 deportes con más medallas",
        )
        st.plotly_chart(fig)

    # Line chart showing the trend of the total number of sports participated in each year
    with col2:
        sports_by_year = data.groupby("Year")["Sport"].nunique()
        fig = px.line(
            sports_by_year,
            x=sports_by_year.index,
            y=sports_by_year.values,
            labels={"x": "Año", "y": "Número de Deportes"},
            title="Tendencia del número total de deportes participados cada año",
        )
        st.plotly_chart(fig)

    # Pie chart showing the distribution of medals by sport
    with col1:
        medal_sport_distribution = (
            data[data["Medal"].notna()]["Sport"].value_counts().head(10)
        )
        fig = px.pie(
            medal_sport_distribution,
            names=medal_sport_distribution.index,
            values=medal_sport_distribution.values,
            title="Distribución de medallas por deporte (Top 10)",
        )
        st.plotly_chart(fig)

    # Scatter plot showing the relationship between the number of sports and the number of medals won
    with col2:
        sport_medal_relation = (
            data[data["Medal"].notna()].groupby("Sport")["Medal"].count().reset_index()
        )
        fig = px.scatter(
            sport_medal_relation,
            x="Sport",
            y="Medal",
            labels={"x": "Deporte", "y": "Número de Medallas"},
            title="Relación entre el número de deportes y el número de medallas ganadas",
        )
        st.plotly_chart(fig)

    # Bar chart showing the distribution of athletes by season
    with col1:
        season_distribution = data["Season"].value_counts()
        fig = px.bar(
            season_distribution,
            x=season_distribution.index,
            y=season_distribution.values,
            labels={"x": "Temporada", "y": "Número de Atletas"},
            title="Distribución de atletas por temporada",
        )
        st.plotly_chart(fig)

    # Scatter plot showing the relationship between the height and weight of athletes
    with col2:
        fig = px.scatter(
            data,
            x="Height",
            y="Weight",
            labels={"x": "Altura (cm)", "y": "Peso (kg)"},
            title="Relación entre la altura y el peso de los atletas",
        )
        st.plotly_chart(fig)

    # Line chart showing the trend of the average age of athletes over time
    with col1:
        average_age_by_year = data.groupby("Year")["Age"].mean().reset_index()
        fig = px.line(
            average_age_by_year,
            x="Year",
            y="Age",
            labels={"x": "Año", "y": "Edad Promedio de los Atletas"},
            title="Tendencia de la edad promedio de los atletas a lo largo del tiempo",
        )
        st.plotly_chart(fig)

    # Bar chart showing the top 10 teams with the most athletes
    with col2:
        team_athlete_count = data["Team"].value_counts().head(10)
        fig = px.bar(
            team_athlete_count,
            x=team_athlete_count.index,
            y=team_athlete_count.values,
            labels={"x": "Equipo", "y": "Número de Atletas"},
            title="Los 10 equipos con más atletas",
        )
        st.plotly_chart(fig)

    # Pie chart showing the distribution of events
    with col1:
        event_distribution = data["Event"].value_counts().head(10)
        fig = px.pie(
            event_distribution,
            names=event_distribution.index,
            values=event_distribution.values,
            title="Distribución de eventos (Top 10)",
        )
        st.plotly_chart(fig)

    # Scatter plot showing the relationship between the year and the number of events
    with col2:
        events_by_year = data.groupby("Year")["Event"].nunique().reset_index()
        fig = px.scatter(
            events_by_year,
            x="Year",
            y="Event",
            labels={"x": "Año", "y": "Número de Eventos"},
            title="Relación entre el año y el número de eventos",
        )
        st.plotly_chart(fig)
