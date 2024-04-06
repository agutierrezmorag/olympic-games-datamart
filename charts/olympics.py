import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from sklearn.linear_model import LogisticRegression


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

    # Clean data
    cleaned_data = data.dropna(subset=["Altura", "Peso", "Medalla"])

    # Create 'Medal_Won' column
    cleaned_data["Medal_Won"] = cleaned_data["Medalla"].notnull().astype(int)

    # Create scatter plots
    sns.scatterplot(x="Altura", y="Medal_Won", data=cleaned_data)
    plt.show()

    sns.scatterplot(x="Peso", y="Medal_Won", data=cleaned_data)
    plt.show()

    # Perform logistic regression
    X = cleaned_data[["Altura", "Peso"]]
    y = cleaned_data["Medal_Won"]

    log_reg = LogisticRegression().fit(X, y)

    # Print coefficients
    st.write("Height coefficient:", log_reg.coef_[0][0])
    st.write("Weight coefficient:", log_reg.coef_[0][1])


def ww2_charts(data):
    st.markdown("## :red[Segunda Guerra Mundial]")
    st.markdown(
        "Analisis de los países involucrados en la Segunda Guerra Mundial. El periodo de la Segunda Guerra Mundial se considera de 1939 a 1945 y se encuentra resaltado en los gráficos a continuación."
    )
    xcol1, xcol2, xcol3 = st.columns(3)
    # Create a list of the countries that were involved in WWII as Axis powers
    axis_countries = ["GER", "ITA", "JPN", "HUN", "ROM", "BUL", "FIN"]

    # Create a list of the countries that were involved in WWII as Allies
    allies_countries = [
        "USA",
        "GBR",
        "FRA",
        "USSR",
        "CHN",
        "CAN",
        "AUS",
        "NZL",
        "IND",
        "RSA",
        "EGY",
        "BRA",
        "MEX",
        "ARG",
        "BEL",
        "NED",
        "NOR",
        "POL",
        "GRE",
        "YUG",
    ]

    # Create a list of the countries that were neutral during WWII
    neutral_countries = ["SWE", "SWI", "SPA", "POR", "IRE", "TUR"]

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
    with xcol1:
        # Create line plots to visualize the performance metrics of the WWII-involved countries over time
        fig = px.line(
            axis_data,
            x="Año",
            y="Medallas",
            color="NOC",
            title="Rendimiento de los países del Eje a lo largo del tiempo",
        )

        # Add the shapes to the layout of each figure
        fig.update_layout(shapes=shapes)
        st.plotly_chart(fig)

    with xcol2:
        fig = px.line(
            allies_data,
            x="Año",
            y="Medallas",
            color="NOC",
            title="Rendimiento de los países aliados a lo largo del tiempo",
        )
        # Add the shapes to the layout of each figure
        fig.update_layout(shapes=shapes)
        st.plotly_chart(fig)

    with xcol3:
        fig = px.line(
            neutral_data,
            x="Año",
            y="Medallas",
            color="NOC",
            title="Rendimiento de los países neutrales a lo largo del tiempo",
        )
        # Add the shapes to the layout of each figure
        fig.update_layout(shapes=shapes)
        st.plotly_chart(fig)

    with xcol1:
        # Create line plots to visualize the performance metrics of the WWII-involved countries over time
        fig = px.line(
            axis_data,
            x="Año",
            y="Atletas",
            color="NOC",
            title="Número de atletas de los países del Eje a lo largo del tiempo",
        )

        # Add the shapes to the layout of each figure
        fig.update_layout(shapes=shapes)
        st.plotly_chart(fig)

    with xcol2:
        fig = px.line(
            allies_data,
            x="Año",
            y="Atletas",
            color="NOC",
            title="Número de atletas de los países aliados a lo largo del tiempo",
        )

        # Add the shapes to the layout of each figure
        fig.update_layout(shapes=shapes)
        st.plotly_chart(fig)

    with xcol3:
        fig = px.line(
            neutral_data,
            x="Año",
            y="Atletas",
            color="NOC",
            title="Número de atletas de los países neutrales a lo largo del tiempo",
        )

        # Add the shapes to the layout of each figure
        fig.update_layout(shapes=shapes)
        st.plotly_chart(fig)
