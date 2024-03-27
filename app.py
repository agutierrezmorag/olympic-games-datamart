import pandas as pd
import streamlit as st

from statistics_calc import descriptors, qualitative_stats


def load_and_display_data(title, filename, qualitative_vars):
    st.markdown(f"## {title}")
    data = pd.read_csv(f"datasets/{filename}")
    st.dataframe(data, hide_index=True, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Variables cualitativas")
        qualitative = qualitative_stats(data, qualitative_vars)
        st.dataframe(qualitative, hide_index=True, use_container_width=True)
    with col2:
        st.markdown("### Variables cuantitativas")
        data_descriptors = descriptors(data)
        st.dataframe(data_descriptors, hide_index=False, use_container_width=True)


def main():
    st.set_page_config(page_title="Datamart data", page_icon="📊", layout="wide")
    st.title("📊 Datamart data")
    st.markdown(
        "Los siguientes datos no han sido modificados y se presentan tal como se encuentran en el archivo `csv`."
    )

    st.info(
        "📢 **Nota:** Considerar que se usa un punto en vez de una coma para valores decimales."
    )

    load_and_display_data(
        "🏅 Olympics data",
        "olympics.csv",
        ["Team", "NOC", "Games", "Sport", "Event", "Medal"],
    )
    load_and_display_data(
        "📚 Schooling data",
        "expected-years-of-schooling.csv",
        ["Entity", "Code"],
    )
    load_and_display_data(
        "🪙 Income data", "gross-national-income-per-capita.csv", ["Entity", "Code"]
    )
    load_and_display_data(
        "🌍 Human Development Index (HDI) data",
        "human-development-index.csv",
        ["Entity", "Code"],
    )
    load_and_display_data(
        "📈 Historical Index of Human Development (HIHD) data",
        "hdi-vs-hihd.csv",
        ["Entity", "Code"],
    )


if __name__ == "__main__":
    main()
