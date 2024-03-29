import os

import pandas as pd
import streamlit as st
from langchain.agents.agent_types import AgentType
from langchain_anthropic import ChatAnthropic
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

os.environ["LANGCHAIN_TRACING_V2"] = st.secrets.langsmith.tracing
os.environ["LANGCHAIN_PROJECT"] = st.secrets.langsmith.project
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets.langsmith.endpoint
os.environ["LANGCHAIN_API_KEY"] = st.secrets.langsmith.api_key


@st.cache_data
def load_csvs():
    olympics = pd.read_csv("datasets/olympics.csv")
    income = pd.read_csv("datasets/gross-national-income-per-capita.csv")
    schooling = pd.read_csv("datasets/expected-years-of-schooling.csv")
    hdi = pd.read_csv("datasets/human-development-index.csv")
    hihd = pd.read_csv("datasets/hdi-vs-hihd.csv")
    return olympics, income, schooling, hdi, hihd


def choose_dataset():
    upload_instead = st.toggle("Upload my own csv file")
    if upload_instead:
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(df)
            return df
    else:
        olympics, income, schooling, hdi, hihd = load_csvs()
        dataset_dict = {
            "Olympics": olympics,
            "Income": income,
            "Schooling": schooling,
            "HDI": hdi,
            "HDI vs. HIHD": hihd,
        }

        selected_dataset = st.selectbox(
            "Select a dataset to view",
            list(dataset_dict.keys()),
        )
        st.write(dataset_dict[selected_dataset])
        return dataset_dict[selected_dataset]


def choose_llm():
    col1, col2 = st.columns(2)
    with col1:
        model = st.selectbox(
            "Select a language model",
            [
                "claude-3-haiku-20240307",
                "claude-3-sonnet-20240229",
                "claude-3-opus-20240229",
                "gpt-3.5-turbo",
            ],
        )

    with col2:
        api_key = st.text_input(
            "Enter your LLM API key",
            help="Get one from https://anthropic.com/. This value will not be validated, stored nor shared.",
        )

    temperature = st.slider("Temperature", 0.0, 10.0, 0.0)
    if api_key:
        if model == "gpt-3.5-turbo":
            llm = ChatOpenAI(
                model=model,
                temperature=temperature,
                openai_api_key=api_key,
            )
        else:
            llm = ChatAnthropic(
                model=model,
                temperature=temperature,
                anthropic_api_key=api_key,
            )
        return llm


def main():
    st.set_page_config(page_title="DataQuery AI", page_icon="🤖")
    st.title("DataQuery AI")
    st.write(
        "This is a chatbot that can answer questions about various datasets. Select a dataset from the sidebar (or upload your own) \
        and ask a question!"
    )

    with st.sidebar:
        st.header("LLM")
        llm = choose_llm()
        iterations = st.number_input(
            "Max iterations",
            1,
            10,
            3,
            help="Max iterations of operations for the agent to run",
        )

        st.header("Dataset")
        df = choose_dataset()

    if not llm:
        st.stop()

    try:
        agent_executor = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            max_iterations=iterations,
            return_intermediate_steps=True,
            agent_type=AgentType.OPENAI_FUNCTIONS
            if isinstance(llm, ChatOpenAI)
            else AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
    except ValueError:
        st.error("No valid dataset selected.")
        st.stop()

    if query := st.chat_input("Ask me a question!"):
        st.chat_message("user", avatar="🤓").write(query)
        with st.chat_message("assistant"):
            response = agent_executor.invoke(query)
            st.write(response["output"])
            st.expander("Show intermediate steps").write(response["intermediate_steps"])


if __name__ == "__main__":
    main()
