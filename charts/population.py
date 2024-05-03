import plotly.express as px
import streamlit as st


def get_population_charts(data):
    st.markdown("## :blue[Otros gráficos de interés]")
    col1, col2 = st.columns(2)

    # Calculate the global minimum and maximum population
    global_min = data["Count"].min()
    global_max = data["Count"].max()

    # Create a choropleth map for the oldest year
    with col1:
        oldest_year = data["Year"].min()
        data_oldest_year = data[data["Year"] == oldest_year]
        fig = px.choropleth(
            data_oldest_year,
            locations="Code",
            color="Count",
            labels={"Count": "Población"},
            title=f"Población del mundo en {oldest_year}",
            hover_name="Country Name",
            color_continuous_scale="Mint",
            range_color=[global_min, global_max],
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
        )
        st.plotly_chart(fig)

        # Show the top 10 countries with the most population in the oldest year as a bar chart
        top_10_oldest_year = data_oldest_year.sort_values(
            "Count", ascending=False
        ).head(10)
        fig = px.bar(
            top_10_oldest_year,
            x="Count",
            y="Country Name",
            orientation="h",
            labels={"Count": "Población", "Country Name": "País"},
            text_auto=True,
            title=f"Top 10 países con mayor población en {oldest_year}",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Create a choropleth map for the latest year
    with col2:
        latest_year = data["Year"].max()
        data_latest_year = data[data["Year"] == latest_year]
        fig = px.choropleth(
            data_latest_year,
            locations="Code",
            color="Count",
            labels={"Count": "Población"},
            title=f"Población del mundo en {latest_year}",
            hover_name="Country Name",
            color_continuous_scale="Mint",
            range_color=[global_min, global_max],
        )
        fig.update_geos(
            showcountries=True,
            countrycolor="Black",
            showcoastlines=False,
        )
        st.plotly_chart(fig)

        # Show the top 10 countries with the most population in the latest year as a bar chart
        top_10_latest_year = data_latest_year.sort_values(
            "Count", ascending=False
        ).head(10)
        fig = px.bar(
            top_10_latest_year,
            x="Count",
            y="Country Name",
            orientation="h",
            labels={"Count": "Población", "Country Name": "País"},
            text_auto=True,
            title=f"Top 10 países con mayor población en {latest_year}",
        )
        st.plotly_chart(fig, use_container_width=True)
