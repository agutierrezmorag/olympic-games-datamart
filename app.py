import pandas as pd
import plotly.express as px
import streamlit as st

from statistics_calc import descriptors, qualitative_stats


def load_and_display_data(title, filename, qualitative_vars):
    st.markdown(f"## :red[{title}]")
    data = pd.read_csv(f"datasets/{filename}")
    st.dataframe(data, hide_index=True, use_container_width=True)
    col1, col2 = st.columns(2)

    st.markdown("### Variables cualitativas")
    qualitative = qualitative_stats(data, qualitative_vars)
    st.dataframe(qualitative, hide_index=True, use_container_width=True)

    st.markdown("### Variables cuantitativas")
    data_descriptors = descriptors(data)
    st.dataframe(data_descriptors, hide_index=False, use_container_width=True)

    # Add a selectbox for the user to select a plot type
    plot_types = ["Histogram", "Box Plot", "Scatter Plot"]
    selected_plot = st.selectbox("Selecciona un tipo de gráfico", plot_types)

    # Add a selectbox for the user to select a quantitative variable
    quantitative_vars = [col for col in data.columns if col not in qualitative_vars]
    selected_var = st.selectbox(
        "Selecciona una variable para generar un gráfico", quantitative_vars
    )

    # Plot the selected plot type
    if selected_plot == "Histogram":
        fig = px.histogram(
            data,
            x=selected_var,
            nbins=50,
            labels={"x": selected_var, "y": "Frecuencia"},
        )
        fig.update_xaxes(title_text=selected_var)
        fig.update_yaxes(title_text="Frecuencia")
    elif selected_plot == "Box Plot":
        fig = px.box(data, x=selected_var)
        fig.update_xaxes(title_text=selected_var)
        fig.update_yaxes(title_text="Value")
    elif selected_plot == "Scatter Plot":
        selected_var2 = st.selectbox(
            "Selecciona una segunda variable para el gráfico de dispersión",
            quantitative_vars,
        )
        fig = px.scatter(data, x=selected_var, y=selected_var2)
        fig.update_xaxes(title_text=selected_var)
        fig.update_yaxes(title_text=selected_var2)

    fig.update_layout(title_text=f"{selected_plot} de {selected_var}", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Add a pie chart for the 'Sex' column in the 'Olympics data' dataset
    st.markdown("## :blue[Otros gráficos de interés]")
    if title == "🏅 Olympics data":
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(data, names="Sex", title="Distribución de Sexo")
            st.plotly_chart(fig)

        with col2:
            medal_count = (
                data.groupby("NOC")["Medal"].count().sort_values(ascending=False)
            )
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
            medals_by_year = (
                data[data["Medal"].notna()].groupby("Year")["Medal"].count()
            )
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
                data[data["Medal"].notna()]
                .groupby("Year")["Medal"]
                .count()
                .reset_index()
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
                data[data["Medal"].notna()]
                .groupby("Age")["Medal"]
                .count()
                .reset_index()
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
            sport_medal_count = (
                data[data["Medal"].notna()]["Sport"].value_counts().head(10)
            )
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
                data[data["Medal"].notna()]
                .groupby("Sport")["Medal"]
                .count()
                .reset_index()
            )
            fig = px.scatter(
                sport_medal_relation,
                x="Sport",
                y="Medal",
                labels={"x": "Deporte", "y": "Número de Medallas"},
                title="Relación entre el número de deportes y el número de medallas ganadas",
            )
            st.plotly_chart(fig)


def main():
    st.set_page_config(page_title="Datamart data", page_icon="📊", layout="wide")

    # Define the datasets and their corresponding titles and qualitative variables
    datasets = {
        "🏅 Olympics data": (
            "olympics.csv",
            ["Team", "NOC", "Games", "Sport", "Event", "Medal"],
        ),
        "📚 Schooling data": ("expected-years-of-schooling.csv", ["Entity", "Code"]),
        "🪙 Income data": ("gross-national-income-per-capita.csv", ["Entity", "Code"]),
        "🌍 Human Development Index (HDI) data": (
            "human-development-index.csv",
            ["Entity", "Code"],
        ),
        "📈 Historical Index of Human Development (HIHD) data": (
            "hdi-vs-hihd.csv",
            ["Entity", "Code"],
        ),
    }

    with st.sidebar:
        st.markdown("# 📊 Datamart data")
        st.markdown(
            "Los siguientes datos no han sido modificados y se presentan tal como se encuentran en el archivo `csv`."
        )

        st.warning(
            "⚠️ **IMPORTANTE:** Considerar que se usa un punto en vez de una coma para valores decimales."
        )

        st.info("📢 **Nota:** La carga de un `scatter plot` puede tomar tiempo.")

        # Add a selectbox for the user to select a dataset
        selected_dataset = st.selectbox("Elige un dataset", list(datasets.keys()))

    # Load and display the selected dataset
    filename, qualitative_vars = datasets[selected_dataset]

    load_and_display_data(selected_dataset, filename, qualitative_vars)


if __name__ == "__main__":
    main()
