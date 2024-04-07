import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LogisticRegression


@st.cache_data
def get_olympics_charts(data):
    # Assuming 'ID' is the unique identifier for each athlete
    data = data.drop_duplicates(subset="ID")

    logistic_regression(data)

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
        fig.update_traces(textinfo="value+percent")
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

        fig.update_traces(textinfo="value+percent")
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
        )

        st.plotly_chart(fig)

    # Create a dot chart showing the distribution of medals and athletes by age
    with col2:
        # Calculate the distribution of medals by age
        medal_distribution = (
            data[data["Medalla"].notna()]
            .groupby("Edad")["Medalla"]
            .count()
            .reset_index()
        )

        # Calculate the distribution of athletes by age
        athlete_distribution = data.groupby("Edad")["ID"].nunique().reset_index()

        # Create a figure
        fig = go.Figure()

        # Add a scatter trace for the distribution of medals by age
        fig.add_trace(
            go.Scatter(
                x=medal_distribution["Edad"],
                y=medal_distribution["Medalla"],
                mode="markers",
                name="Medallas",
            )
        )

        # Add a scatter trace for the distribution of athletes by age
        fig.add_trace(
            go.Scatter(
                x=athlete_distribution["Edad"],
                y=athlete_distribution["ID"],
                mode="markers",
                name="Atletas",
            )
        )

        # Add annotations for each marker
        for i in range(len(medal_distribution)):
            fig.add_annotation(
                x=medal_distribution.loc[i, "Edad"],
                y=medal_distribution.loc[i, "Medalla"],
                text=str(int(medal_distribution.loc[i, "Edad"])),
                showarrow=False,
                font=dict(size=11),
                yshift=10,
            )
        for i in range(len(athlete_distribution)):
            fig.add_annotation(
                x=athlete_distribution.loc[i, "Edad"],
                y=athlete_distribution.loc[i, "ID"],
                text=str(int(athlete_distribution.loc[i, "Edad"])),
                showarrow=False,
                font=dict(size=11),
                yshift=10,
            )

        # Set the title and labels
        fig.update_layout(
            title="Distribución de medallas y atletas por edad",
            xaxis_title="Edad",
            yaxis_title="Número",
            legend_title="Distribución",
        )

        st.plotly_chart(fig)

    # Create a choropleth map to show the distribution of medals by country
    with col1:
        # Filter out rows where Medal is NaN
        medal_data = data.dropna(subset=["Medalla"])

        # Count the number of medals for each NOC
        medal_distribution = medal_data["NOC"].value_counts().reset_index()
        medal_distribution.columns = ["NOC", "Count"]

        fig = px.choropleth(
            medal_distribution,
            locations="NOC",
            color="Count",
            title="Distribución de medallas por país",
            labels={"NOC": "País", "Count": "Número de medallas"},
            color_continuous_scale=px.colors.sequential.Greens,
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

    # Display the oldest sports that are still played today in a line chart
    with col2:
        oldest_sports = data.groupby("Deporte")["Año"].min().reset_index()
        latest_sports = data.groupby("Deporte")["Año"].max().reset_index()

        # Merge the two dataframes
        sports = pd.merge(oldest_sports, latest_sports, on="Deporte")

        # Filter sports that are still played today
        sports = sports[sports["Año_y"] == data["Año"].max()]

        # Sort by the oldest year
        sports = sports.sort_values("Año_x", ascending=True)

        fig = px.line(
            sports,
            x="Año_x",
            y="Deporte",
            title="Deportes más antiguos que todavía se juegan hoy en día",
            labels={"Deporte": "Deporte", "Año_x": "Primer año de competencia"},
        )

        st.plotly_chart(fig)

    # Create a bar chart to show the distribution of medal types within each country
    with col2:
        medal_distribution = (
            data[data["Medalla"].isin(["Bronce", "Plata", "Oro"])]
            .groupby(["NOC", "Medalla"])["Medalla"]
            .count()
            .unstack()
            .reset_index()
        )
        medal_distribution.columns = ["NOC", "Bronce", "Plata", "Oro"]
        medal_distribution["Total"] = medal_distribution[
            ["Bronce", "Plata", "Oro"]
        ].sum(axis=1)
        medal_distribution = medal_distribution.sort_values("Total", ascending=False)

        # Select only the top 25 countries
        medal_distribution = medal_distribution.head(25)

        fig = px.bar(
            medal_distribution,
            x="NOC",
            y=["Bronce", "Plata", "Oro"],
            title="Distribución de tipos de medallas por país (Top 25)",
            labels={
                "value": "Número de medallas",
                "variable": "Tipo de medalla",
                "NOC": "País",
            },
            barmode="stack",
            text_auto=True,
        )

        st.plotly_chart(fig)

    # Create a grouped bar chart to show the distribution of medal types within each sport for male and female athletes
    with col1:
        medal_distribution = (
            data[data["Medalla"].isin(["Bronce", "Plata", "Oro"])]
            .groupby(["Deporte", "Sexo", "Medalla"])["Medalla"]
            .count()
            .unstack()
            .reset_index()
        )
        medal_distribution.columns = ["Deporte", "Sexo", "Bronce", "Plata", "Oro"]
        medal_distribution["Total"] = medal_distribution[
            ["Bronce", "Plata", "Oro"]
        ].sum(axis=1)
        medal_distribution = medal_distribution.sort_values("Total", ascending=False)

        fig = px.bar(
            medal_distribution,
            x="Deporte",
            y=["Bronce", "Plata", "Oro"],
            color="Sexo",
            title="Distribución de tipos de medallas dentro de cada deporte por género",
            labels={
                "value": "Número de medallas",
                "variable": "Tipo de medalla",
                "Deporte": "Deporte",
                "Sexo": "Género",
            },
            barmode="group",
            color_discrete_map={"M": "sky blue", "F": "pink"},
        )

        st.plotly_chart(fig)

    # Create a line plot to show the number of participants in each sport over time
    with col2:
        sport_participation = (
            data.groupby(["Año", "Deporte"])["Deporte"]
            .count()
            .reset_index(name="Count")
        )
        fig = px.line(
            sport_participation,
            x="Año",
            y="Count",
            color="Deporte",
            title="Participación en cada deporte a lo largo del tiempo",
        )
        st.plotly_chart(fig)

    # Create a bar chart to show the number of participants in the top 25 events in the most recent year
    with col1:
        recent_year = data["Año"].max()
        event_participation = (
            data[data["Año"] == recent_year]["Evento"]
            .value_counts()
            .nlargest(25)  # Select only the top 25 events
            .reset_index(name="Atletas")
        )
        event_participation.columns = ["Evento", "Atletas"]
        fig = px.bar(
            event_participation,
            x="Evento",
            y="Atletas",
            text_auto=True,
            title=f"Participación en los 25 eventos principales en {recent_year}",
        )
        st.plotly_chart(fig)

    ww2_charts(data)


def logistic_regression(data):
    # Create 'Medal_Won' column
    data["Medal_Won"] = data["Medalla"].notnull().astype(int)

    # Clean data
    cleaned_data = data.dropna(subset=["Altura", "Peso"])

    # Perform logistic regression with BMI
    X = cleaned_data[["Altura", "Peso", "IMC"]]
    y = cleaned_data["Medal_Won"]

    log_reg = LogisticRegression().fit(X, y)

    # Print coefficients
    height_coef = log_reg.coef_[0][0]
    weight_coef = log_reg.coef_[0][1]
    imc_coef = log_reg.coef_[0][2]

    st.markdown(f"""
        ## Coeficientes de la Regresión Logística
        
        - **Coeficiente de Altura:** {height_coef:.4f}
            - Por cada unidad que aumenta la altura, las log-odds de ganar una medalla {'aumentan' if height_coef > 0 else 'disminuyen'} en {abs(height_coef):.4f}, asumiendo que todas las demás características permanecen constantes.
        
        - **Coeficiente de Peso:** {weight_coef:.4f}
            - Por cada unidad que aumenta el peso, las log-odds de ganar una medalla {'aumentan' if weight_coef > 0 else 'disminuyen'} en {abs(weight_coef):.4f}, asumiendo que todas las demás características permanecen constantes.
    
        - **Coeficiente de IMC:** {imc_coef:.4f}
            - Por cada unidad que aumenta el IMC, las log-odds de ganar una medalla {'aumentan' if imc_coef > 0 else 'disminuyen'} en {abs(imc_coef):.4f}, asumiendo que todas las demás características permanecen constantes.
        """)

    st.markdown("""
        ### ¿Qué son los Log-Odds?

        Los log-odds, también conocidos como logits, son una forma de expresar probabilidades.

        - Si tienes una probabilidad, la "odds" (o posibilidad) es la probabilidad de que ocurra un evento dividida por la probabilidad de que no ocurra.
        - El "log-odds" es simplemente el logaritmo natural de las odds.

        En el contexto de la regresión logística, usamos log-odds porque nos permiten modelar una variable de respuesta binaria con una combinación lineal de predictores. Esto significa que aunque estamos modelando una probabilidad (que está limitada entre 0 y 1), los log-odds pueden variar de -infinito a +infinito.

        En resumen, los coeficientes de la regresión logística representan el cambio en los log-odds causado por una unidad de cambio en los predictores. En nuestro caso, los coeficientes de altura y peso representan cuánto cambian las log-odds de ganar una medalla cuando la altura o el peso cambian en una unidad.
    """)


def ww2_charts(data):
    st.markdown("## :red[Segunda Guerra Mundial]")
    st.markdown(
        "Analisis de los países involucrados en la Segunda Guerra Mundial. El periodo de la Segunda Guerra Mundial se considera de 1939 a 1945 y se encuentra resaltado en los gráficos a continuación."
    )
    xcol1, xcol2, xcol3 = st.columns(3)
    # Create a list of the countries that were involved in WWII as Axis powers
    axis_countries = ["GER", "ITA", "JPN"]

    # Create a list of the countries that were involved in WWII as Allies
    allies_countries = ["USA", "GBR", "URS"]

    # Create a list of the countries that were neutral during WWII
    neutral_countries = ["SWE", "SUI", "ESP"]

    # Group the data by country and Olympic year
    grouped_data = (
        data.groupby(["NOC", "Año"])
        .agg({"Medalla": "count", "ID": pd.Series.nunique})
        .reset_index()
    )
    grouped_data.columns = ["NOC", "Año", "Medallas", "Atletas"]

    # Filter the data to consider only up to 1994
    grouped_data = grouped_data[grouped_data["Año"] <= 1993]

    # Create separate dataframes for Axis, Allies, and Neutral countries
    axis_data = grouped_data[grouped_data["NOC"].isin(axis_countries)]
    allies_data = grouped_data[grouped_data["NOC"].isin(allies_countries)]
    neutral_data = grouped_data[grouped_data["NOC"].isin(neutral_countries)]

    # Define a list of shapes to represent the WWII period
    shapes = [
        dict(
            type="rect",
            xref="x",
            yref="paper",
            x0=1939,
            x1=1945,
            y0=0,
            y1=1,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
    ]

    # Define a color for each country
    colors = {
        "GER": "darkred",  # Germany
        "ITA": "deepskyblue",  # Italy
        "JPN": "gold",  # Japan
        "USA": "darkgreen",  # USA
        "GBR": "darkblue",  # Great Britain
        "URS": "darkviolet",  # USSR
        "SWE": "lightseagreen",  # Sweden
        "SUI": "saddlebrown",  # Switzerland
        "ESP": "darkorange",  # Spain
    }

    # Create line plots to visualize the performance metrics of the WWII-involved countries over time
    with xcol1:
        fig = go.Figure()
        for country in axis_countries:
            country_data = axis_data[axis_data["NOC"] == country]
            fig.add_trace(
                go.Scatter(
                    x=country_data["Año"],
                    y=country_data["Medallas"],
                    mode="lines",
                    name=f"{country} Medallas",
                    line=dict(dash="solid", color=colors.get(country, "blue")),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=country_data["Año"],
                    y=country_data["Atletas"],
                    mode="lines",
                    name=f"{country} Atletas",
                    line=dict(dash="dash", color=colors.get(country, "blue")),
                )
            )
        fig.update_layout(
            shapes=shapes,
            title="Rendimiento de los países del Eje a lo largo del tiempo",
        )
        st.plotly_chart(fig)

    with xcol2:
        fig = go.Figure()
        for country in allies_countries:
            country_data = allies_data[allies_data["NOC"] == country]
            fig.add_trace(
                go.Scatter(
                    x=country_data["Año"],
                    y=country_data["Medallas"],
                    mode="lines",
                    name=f"{country} Medallas",
                    line=dict(dash="solid", color=colors.get(country, "blue")),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=country_data["Año"],
                    y=country_data["Atletas"],
                    mode="lines",
                    name=f"{country} Atletas",
                    line=dict(dash="dash", color=colors.get(country, "blue")),
                )
            )
        fig.update_layout(
            shapes=shapes,
            title="Rendimiento de los países aliados a lo largo del tiempo",
        )
        st.plotly_chart(fig)

    with xcol3:
        fig = go.Figure()
        for country in neutral_countries:
            country_data = neutral_data[neutral_data["NOC"] == country]
            fig.add_trace(
                go.Scatter(
                    x=country_data["Año"],
                    y=country_data["Medallas"],
                    mode="lines",
                    name=f"{country} Medallas",
                    line=dict(dash="solid", color=colors.get(country, "blue")),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=country_data["Año"],
                    y=country_data["Atletas"],
                    mode="lines",
                    name=f"{country} Atletas",
                    line=dict(dash="dash", color=colors.get(country, "blue")),
                )
            )
        fig.update_layout(
            shapes=shapes,
            title="Rendimiento de los países neutrales a lo largo del tiempo",
        )
        st.plotly_chart(fig)
