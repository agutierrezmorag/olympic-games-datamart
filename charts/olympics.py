import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


@st.cache_data
def get_olympics_charts(data):
    og_data = data.copy()

    # Assuming 'ID' is the unique identifier for each athlete
    data = data.drop_duplicates(subset="ID")

    st.markdown("## :yellow[Diferencias de género en los Juegos Olímpicos]")
    gender_charts(data, og_data)

    st.markdown("## :green[Rendimiento por país]")
    country_charts(data, og_data)

    st.markdown("## :red[Segunda Guerra Mundial]")
    st.markdown(
        "El periodo de la Segunda Guerra Mundial se considera de 1939 a 1945 y se encuentra resaltado en los gráficos a continuación."
    )
    ww2_charts(data, og_data)

    st.markdown("## :blue[Guerra Fría]")
    st.markdown(
        "El periodo de la Guerra Fría se considera de 1947 a 1991 y se encuentra resaltado en los gráficos a continuación."
    )
    cold_war_charts(data, og_data)

    st.markdown("## :blue[Otros gráficos de interés]")
    extra_charts(data, og_data)

    st.markdown("## :green[Información adicional]")
    st.markdown("""
        - La Aeronáutica solo recibió Medals de Gold en los Juegos Olímpicos de 1936 en Berlín, Alemania. \
        Hubieron preparativos para expandir esta disciplina como Sport pero el inicio de la Segunda Guerra Mundial \
        detuvo el proceso.
        
        - Lacrosse solo fue jugado en 1904 en St. Louis, 1908 en Londres, 1928 en Ámsterdam y 1932 en Los Ángeles. \
        En 1904, solo hubieron 3 Teams participantes. En 1908 y 1928 solo participaron Teams de Canadá y en 1932 \
        solo participaron Teams de Estados Unidos y Canadá. Posteriormente, dejó de ser un Sport olímpico debido a \
        la falta de Teams internacionales. Se espera que regrese a los Juegos Olímpicos en 2028.
        """)


def gender_charts(data, og_data):
    male_color = "steelblue"
    female_color = "orchid"

    gcol1, gcol2 = st.columns(2)

    with gcol1:
        gender_distribution = data["Sex"].value_counts()
        fig = px.pie(
            names=gender_distribution.index,
            values=gender_distribution.values,
            title="Distribución de género",
            labels={"names": "Sex", "values": "Total"},
            color=gender_distribution.index,
            color_discrete_map={"F": female_color, "M": male_color},
        )
        fig.update_traces(textinfo="value+percent")
        st.plotly_chart(fig)

    with gcol2:
        # Group by season and gender
        season_gender_distribution = (
            data.groupby(["Season", "Sex"])["Sex"].count().unstack().reset_index()
        )
        season_gender_distribution.columns = ["Season", "F", "M"]

        # Create a stacked bar chart to show gender distribution by season
        fig = px.bar(
            season_gender_distribution,
            x="Season",
            y=["F", "M"],
            title="Distribución de género por Season",
            labels={"value": "Total", "variable": "Sex", "Season": "Season"},
            barmode="stack",
            color_discrete_map={"F": female_color, "M": male_color},
            text_auto=True,
        )

        st.plotly_chart(fig)

    with gcol1:
        medal_distribution = (
            data[data["Medal"].isin(["Bronze", "Silver", "Gold"])]
            .groupby(["Sport", "Sex", "Medal"])["Medal"]
            .count()
            .unstack()
            .reset_index()
        )
        medal_distribution.columns = ["Sport", "Sex", "Bronze", "Silver", "Gold"]
        medal_distribution["Total"] = medal_distribution[
            ["Bronze", "Silver", "Gold"]
        ].sum(axis=1)
        medal_distribution = medal_distribution.sort_values("Total", ascending=False)

        fig = px.bar(
            medal_distribution,
            x="Sport",
            y=["Bronze", "Silver", "Gold"],
            color="Sex",
            title="Distribución de tipos de Medals dentro de cada Sport por género",
            labels={
                "value": "Número de Medals",
                "variable": "Tipo de Medal",
                "Sport": "Sport",
                "Sex": "Género",
            },
            barmode="group",
            color_discrete_map={"F": female_color, "M": male_color},
        )

        st.plotly_chart(fig)

    # Group by sport and gender
    gender_distribution = (
        data.groupby(["Sport", "Sex"])["Sex"].count().unstack().reset_index()
    )
    gender_distribution.columns = ["Sport", "F", "M"]

    # Find sports played only by females
    female_only_sports = gender_distribution[gender_distribution["M"].isna()][
        "Sport"
    ].tolist()

    # Find sports played only by males
    male_only_sports = gender_distribution[gender_distribution["F"].isna()][
        "Sport"
    ].tolist()

    # Display sports played only by each gender
    st.write(
        "Sports jugados solo por atletas :red[femeninas]: ", str(female_only_sports)
    )
    st.write(
        "Sports jugados solo por atletas :blue[masculinos]: ", str(male_only_sports)
    )


def country_charts(data, og_data):
    ccol1, ccol2 = st.columns(2)

    # Create a chGoldpleth map to show the distribution of medals by country
    with ccol1:
        # Filter out rows where Medal is NaN
        medal_data = og_data.dropna(subset=["Medal"])

        # Drop duplicates for team events
        medal_data = medal_data.drop_duplicates(
            subset=["Team", "Event", "Year", "Season", "Sport"]
        )

        # Count the number of medals for each NOC
        medal_distribution = medal_data["Region"].value_counts().reset_index()
        medal_distribution.columns = ["Region", "Count"]

        fig = px.chGoldpleth(
            medal_distribution,
            locations="Region",
            locationmode="country names",
            color="Count",
            title="Distribución de Medals por país",
            labels={"Region": "País", "Count": "Número de Medallas"},
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
        )
        st.plotly_chart(fig)

        # Create a bar chart to show the distribution of medals by country
        fig = px.bar(
            medal_distribution.head(25),
            x="Region",
            y="Count",
            title="Top 25 países con más Medals",
            labels={"Region": "País", "Count": "Número de Medallas"},
            text_auto=True,
        )
        st.plotly_chart(fig)

    # Create a chGoldpleth map to show the distribution of athletes by country
    with ccol2:
        country_distribution = data["Region"].value_counts().reset_index()
        country_distribution.columns = ["Region", "Count"]
        fig = px.chGoldpleth(
            country_distribution,
            locations="Region",
            locationmode="country names",
            color="Count",
            title="Distribución de atletas por país",
            labels={"Region": "Pais", "Count": "Número de atletas"},
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
        )
        st.plotly_chart(fig)

        # Create a bar chart for the top 25 countries with the most athletes
        fig = px.bar(
            country_distribution.head(25),
            x="Region",
            y="Count",
            title="Top 25 países con más atletas",
            labels={"Region": "País", "Count": "Número de atletas"},
            text_auto=True,
        )

        st.plotly_chart(fig)

    # Count the number of unique years each country has hosted the Olympics
    with ccol1:
        city_distribution = (
            data.drop_duplicates(subset=["Host country", "Year"])["Host country"]
            .value_counts()
            .reset_index()
        )
        city_distribution.columns = ["Host country", "Count"]

        fig = px.chGoldpleth(
            city_distribution,
            locations="Host country",
            locationmode="country names",
            color="Count",
            title="Países anfitriones de los Juegos Olímpicos",
            labels={"Host country": "Pais", "Count": "Número de olímpiadas"},
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Create a bar chart to show the average number of medals won per Olympics by each country
    with ccol2:
        # Calculate the total number of medals won by each country
        total_medals = data.groupby("Region")["Medal"].count().reset_index()
        total_medals.columns = ["Region", "Total Medals"]

        # Calculate the total number of Olympics each country has participated in
        total_olympics = data["Region"].value_counts().reset_index()
        total_olympics.columns = ["Region", "Total Olympics"]

        # Merge the two DataFrames
        avg_medals = pd.merge(total_medals, total_olympics, on="Region")

        # Calculate the average number of medals won per Olympics
        avg_medals["Promedio"] = (
            avg_medals["Total Medals"] / avg_medals["Total Olympics"]
        )

        # Create the Plotly Express bar chart
        fig = px.chGoldpleth(
            avg_medals.sort_values("Promedio", ascending=False),
            locations="Region",
            locationmode="country names",
            color="Promedio",
            title="Promedio de Medals ganadas por país por Olimpiada",
            color_continuous_scale=px.colors.sequential.Viridis,
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


def ww2_charts(data, og_data):
    xcol1, xcol2, xcol3 = st.columns(3)
    # Create a list of the countries that were involved in WWII as Axis powers
    axis_countries = ["GER", "ITA", "JPN"]

    # Create a list of the countries that were involved in WWII as Allies
    allies_countries = ["USA", "GBR", "URS"]

    # Create a list of the countries that were neutral during WWII
    neutral_countries = ["SWE", "SUI", "ESP"]

    # Group the data by country and Olympic year
    grouped_data = (
        data.groupby(["NOC", "Year"])
        .agg({"Medal": "count", "ID": pd.Series.nunique})
        .reset_index()
    )
    grouped_data.columns = ["NOC", "Year", "Medals", "Atletas"]

    # Filter the data to consider only up to 1994
    grouped_data = grouped_data[grouped_data["Year"] <= 1993]

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
                    x=country_data["Year"],
                    y=country_data["Medals"],
                    mode="lines",
                    name=f"{country} Medals",
                    line=dict(dash="solid", color=colors.get(country, "blue")),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=country_data["Year"],
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
                    x=country_data["Year"],
                    y=country_data["Medals"],
                    mode="lines",
                    name=f"{country} Medals",
                    line=dict(dash="solid", color=colors.get(country, "blue")),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=country_data["Year"],
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
                    x=country_data["Year"],
                    y=country_data["Medals"],
                    mode="lines",
                    name=f"{country} Medals",
                    line=dict(dash="solid", color=colors.get(country, "blue")),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=country_data["Year"],
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


def cold_war_charts(data, og_data):
    xcol1, xcol2 = st.columns(2)
    # Create a list of the countries that were involved in the Cold War as Western Bloc
    western_bloc_countries = ["USA", "GBR", "FRA", "CAN", "AUS"]

    # Create a list of the countries that were involved in the Cold War as Eastern Bloc
    eastern_bloc_countries = ["URS", "GDR", "HUN", "POL", "CUB"]

    # Group the data by country and Olympic year
    grouped_data = (
        data.groupby(["NOC", "Year"])
        .agg({"Medal": "count", "ID": pd.Series.nunique})
        .reset_index()
    )
    grouped_data.columns = ["NOC", "Year", "Medals", "Atletas"]

    # Filter the data to consider only up to 1991
    grouped_data = grouped_data[grouped_data["Year"] <= 1993]

    # Create separate dataframes for Western Bloc and Eastern Bloc countries
    western_bloc_data = grouped_data[grouped_data["NOC"].isin(western_bloc_countries)]
    eastern_bloc_data = grouped_data[grouped_data["NOC"].isin(eastern_bloc_countries)]

    # Define a list of shapes to represent the Cold War period
    shapes = [
        dict(
            type="rect",
            xref="x",
            yref="paper",
            x0=1947,
            x1=1991,
            y0=0,
            y1=1,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
    ]

    # Define a list of annotations to emphasize the dip in the year 1980 and the year 1984
    annotations = [
        dict(
            x=1980,
            y=1,
            xref="x",
            yref="paper",
            text="Boicot estadounidense de los Juegos Olímpicos de 1980",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-35,
        ),
        dict(
            x=1984,
            y=1,
            xref="x",
            yref="paper",
            text="Boicot soviético de los Juegos Olímpicos de 1984",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-75,
        ),
    ]

    # Define a color for each country
    colors = {
        "USA": "darkblue",  # USA
        "GBR": "darkgreen",  # Great Britain
        "FRA": "darkred",  # France
        "CAN": "darkorange",  # Canada
        "AUS": "darkviolet",  # Australia
        "URS": "deepskyblue",  # USSR
        "GDR": "gold",  # East Germany
        "HUN": "lightseagreen",  # Hungary
        "POL": "saddlebrown",  # Poland
        "CUB": "darkred",  # Cuba
    }

    # Create line plots to visualize the performance metrics of the Cold War-involved countries over time
    with xcol1:
        fig = go.Figure()
        for country in western_bloc_countries:
            country_data = western_bloc_data[western_bloc_data["NOC"] == country]
            fig.add_trace(
                go.Scatter(
                    x=country_data["Year"],
                    y=country_data["Medals"],
                    mode="lines",
                    name=f"{country} Medals",
                    line=dict(dash="solid", color=colors.get(country, "blue")),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=country_data["Year"],
                    y=country_data["Atletas"],
                    mode="lines",
                    name=f"{country} Atletas",
                    line=dict(dash="dash", color=colors.get(country, "blue")),
                )
            )
        fig.update_layout(
            shapes=shapes,
            annotations=annotations,
            title="Rendimiento de los países del Bloque Occidental a lo largo del tiempo",
        )
        st.plotly_chart(fig)

        st.markdown("### Boicot estadounidense de los Juegos Olímpicos de 1980")
        st.markdown("""
    Las Olimpiadas de 1980 se celebraron en Moscú, Unión Soviética (actual Rusia) del 19 de julio al 3 de agosto de 1980. \
    Fue la primera vez que los Juegos Olímpicos se llevaron a cabo en un país comunista.

    Estas Olimpiadas fueron muy polémicas debido a un boicot liderado por los Estados Unidos. \
    En enero de 1980, el presidente estadounidense Jimmy Carter anunció que EEUU boicotearía los Juegos si \
    la Unión Soviética no retiraba sus tropas de Afganistán en un plazo de un mes. \
    Cuando la URSS no retiró sus tropas, EEUU, junto con más de 60 países, finalmente se negaron a participar en las Olimpiadas de Moscú.

    La ausencia de EEUU y sus aliados, incluyendo potencias deportivas como Alemania Occidental, Canadá y Japón, \
    fue un duro golpe para estos Juegos. \
    La Unión Soviética y sus países del bloque comunista dominaron las competencias, ganando la mayor parte de las Medals de Gold. \
    Sin embargo, los Juegos de Moscú se vieron opacados por la controversia y la baja participación.
        """)

    with xcol2:
        fig = go.Figure()
        for country in eastern_bloc_countries:
            country_data = eastern_bloc_data[eastern_bloc_data["NOC"] == country]
            fig.add_trace(
                go.Scatter(
                    x=country_data["Year"],
                    y=country_data["Medals"],
                    mode="lines",
                    name=f"{country} Medals",
                    line=dict(dash="solid", color=colors.get(country, "blue")),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=country_data["Year"],
                    y=country_data["Atletas"],
                    mode="lines",
                    name=f"{country} Atletas",
                    line=dict(dash="dash", color=colors.get(country, "blue")),
                )
            )
        fig.update_layout(
            shapes=shapes,
            annotations=annotations,
            title="Rendimiento de los países del Bloque Oriental a lo largo del tiempo",
        )
        st.plotly_chart(fig)

        st.markdown("### Boicot soviético de los Juegos Olímpicos de 1984")
        st.markdown("""
Las Olimpiadas de 1984 se llevaron a cabo del 28 de julio al 12 de agosto de 1984 en Los Ángeles, Estados Unidos. \
A diferencia de 1980, en esta ocasión fue la Unión Soviética y sus países aliados los que boicotearon los Juegos, \
en respuesta al boicot de 1980 liderado por EEUU.

A pesar de la ausencia de la URSS y sus países del bloque comunista, los Juegos de Los Ángeles 1984 fueron un gran éxito, \
con la participación de 140 países y la asistencia de más de 5 millones de espectadores. La competencia fue intensa y \
Estados Unidos dominó el medallero.    
        """)


def extra_charts(data, og_data):
    col1, col2 = st.columns(2)

    # Create a pie chart to show the distribution of athletes across different Olympic seasons
    with col1:
        season_distribution = data["Season"].value_counts().reset_index()
        season_distribution.columns = ["Season", "Count"]

        fig = px.pie(
            season_distribution,
            names="Season",
            values="Count",
            title="Distribución de atletas por Season olímpica",
            labels={"Season": "Season", "Count": "Número de atletas"},
            color=season_distribution["Season"],
            color_discrete_map={"Summer": "khaki", "Winter": "lightblue"},
        )

        fig.update_traces(textinfo="value+percent")
        st.plotly_chart(fig)

    # Create a dot chart showing the distribution of medals and athletes by age
    with col2:
        # Calculate the distribution of medals by age
        medal_distribution = (
            data[data["Medal"].notna()].groupby("Age")["Medal"].count().reset_index()
        )

        # Calculate the distribution of athletes by age
        athlete_distribution = data.groupby("Age")["ID"].nunique().reset_index()

        # Create a figure
        fig = go.Figure()

        # Add a scatter trace for the distribution of medals by age
        fig.add_trace(
            go.Scatter(
                x=medal_distribution["Age"],
                y=medal_distribution["Medal"],
                mode="markers",
                name="Medals",
            )
        )

        # Add a scatter trace for the distribution of athletes by age
        fig.add_trace(
            go.Scatter(
                x=athlete_distribution["Age"],
                y=athlete_distribution["ID"],
                mode="markers",
                name="Atletas",
            )
        )

        # Add annotations for each marker
        for i in range(len(medal_distribution)):
            fig.add_annotation(
                x=medal_distribution.loc[i, "Age"],
                y=medal_distribution.loc[i, "Medal"],
                text=str(int(medal_distribution.loc[i, "Age"])),
                showarrow=False,
                font=dict(size=11),
                yshift=10,
            )
        for i in range(len(athlete_distribution)):
            fig.add_annotation(
                x=athlete_distribution.loc[i, "Age"],
                y=athlete_distribution.loc[i, "ID"],
                text=str(int(athlete_distribution.loc[i, "Age"])),
                showarrow=False,
                font=dict(size=11),
                yshift=10,
            )

        # Set the title and labels
        fig.update_layout(
            title="Distribución de Medals y atletas por edad",
            xaxis_title="Age",
            yaxis_title="Número",
            legend_title="Distribución",
        )

        st.plotly_chart(fig)

    # Create a bar chart to show the distribution of medal types within each sport
    with col1:
        medal_distribution = (
            og_data[og_data["Medal"].isin(["Bronze", "Silver", "Gold"])]
            .groupby(["Sport", "Medal"])["Medal"]
            .count()
            .unstack()
            .reset_index()
        )
        medal_distribution.columns = ["Sport", "Bronze", "Silver", "Gold"]
        medal_distribution["Total"] = medal_distribution[
            ["Bronze", "Silver", "Gold"]
        ].sum(axis=1)
        medal_distribution = medal_distribution.sort_values("Total", ascending=False)

        fig = px.bar(
            medal_distribution,
            x="Sport",
            y=["Bronze", "Silver", "Gold"],
            title="Distribución de tipos de Medals dentro de cada deporte",
            labels={
                "value": "Número de Medals",
                "variable": "Tipo de Medal",
                "Sport": "Sport",
            },
            barmode="stack",
            text_auto=True,
            color_discrete_sequence=[
                "darkgoldenrod",
                "aliceblue",
                "gold",
            ],
        )

        st.plotly_chart(fig)

    # Display the oldest sports that are still played today in a line chart
    with col2:
        oldest_sports = og_data.groupby("Sport")["Year"].min().reset_index()
        latest_sports = og_data.groupby("Sport")["Year"].max().reset_index()

        # Merge the two dataframes
        sports = pd.merge(oldest_sports, latest_sports, on="Sport")

        # Filter sports that are still played today
        sports = sports[sports["Year_y"] == og_data["Year"].max()]

        # Sort by the oldest year
        sports = sports.sort_values("Year_x", ascending=True)

        fig = px.line(
            sports,
            x="Year_x",
            y="Sport",
            title="Deportes más antiguos que todavía se juegan hoy en día",
            labels={"Sport": "Sport", "Year_x": "Primer año de competencia"},
        )

        st.plotly_chart(fig)

    # Create a line plot to show the number of participants in each sport over time
    with col1:
        sport_participation = (
            og_data.groupby(["Year", "Sport"])["Sport"]
            .count()
            .reset_index(name="Count")
        )
        fig = px.line(
            sport_participation,
            x="Year",
            y="Count",
            color="Sport",
            title="Participación en cada deporte a lo largo del tiempo",
            labels={"Count": "Número de atletas", "Year": "Year", "Sport": "Sport"},
        )
        st.plotly_chart(fig)

    # Create a bar chart to show the number of participants in the top 25 events in the most recent year
    with col2:
        recent_year = data["Year"].max()
        event_participation = (
            data[data["Year"] == recent_year]["Event"]
            .value_counts()
            .nlargest(25)  # Select only the top 25 events
            .reset_index(name="Atletas")
        )
        event_participation.columns = ["Event", "Atletas"]
        fig = px.bar(
            event_participation,
            x="Event",
            y="Atletas",
            text_auto=True,
            title=f"Participación en los 25 Events principales en {recent_year}",
        )
        st.plotly_chart(fig)

    # Create a chart to show the athletes with the most participation in the Olympics
    with col1:
        # Group by athlete name and NOC, and count the number of participations for each
        athlete_participation = (
            og_data.groupby(["Name", "NOC"])
            .size()
            .nlargest(10)
            .reset_index(name="Participaciones")
        )

        # Create a new column that combines the athlete name and NOC
        athlete_participation["Name (NOC)"] = (
            athlete_participation["Name"] + " (" + athlete_participation["NOC"] + ")"
        )

        fig = px.bar(
            athlete_participation,
            x="Name (NOC)",
            y="Participaciones",
            title="Atletas con más participaciones en los Juegos Olímpicos",
            text_auto=True,
        )
        st.plotly_chart(fig)

    # Find sports that are no longer played in the Olympics
    with col2:
        # Find the most recent year for each sport and whether it's a Summer or Winter Olympics
        latest_year = data.groupby(["Sport", "Season"])["Year"].max().reset_index()

        # Find the most recent year for Summer and Winter Olympics
        latest_summer_year = data[data["Season"] == "Summer"]["Year"].max()
        latest_winter_year = data[data["Season"] == "Winter"]["Year"].max()

        # Filter sports that are no longer played in Summer Olympics
        discontinued_summer_sports = latest_year[
            (latest_year["Year"] < latest_summer_year)
            & (latest_year["Season"] == "Summer")
        ]

        # Filter sports that are no longer played in Winter Olympics
        discontinued_winter_sports = latest_year[
            (latest_year["Year"] < latest_winter_year)
            & (latest_year["Season"] == "Winter")
        ]

        # Calculate years since each sport was last played
        discontinued_summer_sports.loc[:, "Years desde la última vez que se jugó"] = (
            latest_summer_year - discontinued_summer_sports["Year"]
        )
        discontinued_winter_sports.loc[:, "Years desde la última vez que se jugó"] = (
            latest_winter_year - discontinued_winter_sports["Year"]
        )

        # Concatenate the two dataframes and create a new column for the type of sport
        discontinued_sports = pd.concat(
            [
                discontinued_summer_sports.assign(Tipo="Summer"),
                discontinued_winter_sports.assign(Tipo="Winter"),
            ]
        )

        # Sort the dataframe by the "Years desde la última vez que se jugó" column
        discontinued_sports = discontinued_sports.sort_values(
            "Years desde la última vez que se jugó"
        )

        # Create a bar plot
        fig = px.bar(
            discontinued_sports,
            x="Years desde la última vez que se jugó",
            y="Sport",
            color="Tipo",
            color_discrete_map={"Summer": "khaki", "Winter": "lightblue"},
            orientation="h",
            title="Sports que ya no se juegan en los Juegos Olímpicos",
            text="Year",
            text_auto=True,
        )

        st.plotly_chart(fig)
