import asyncio

import pandas as pd
import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


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
    model = st.selectbox(
        "Select a language model",
        [
            "claude-3-haiku-20240307",
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229",
        ],
    )

    api_key = st.text_input(
        "Enter your LLM API key", help="Get one from https://anthropic.com/"
    )
    st.caption("This value will not be validated, stored nor shared.")

    temperature = st.slider("Temperature", 0.0, 10.0, 0.0)
    if api_key:
        llm = ChatAnthropic(
            model=model,
            temperature=temperature,
            anthropic_api_key=api_key,
            streaming=True,
        )
        return llm


async def answer_question(
    query, agent, response_placeholder, agent_thoughts_placeholder
):
    full_response = ""

    async for chunk in agent.astream(query):
        # Agent Action
        if "actions" in chunk:
            for action in chunk["actions"]:
                agent_thoughts_placeholder.markdown(f"- Using Tool: `{action.tool}`")
                agent_thoughts_placeholder.markdown(
                    f"- Tool Input: `{action.tool_input}`"
                )
        # Observation
        elif "steps" in chunk:
            for step in chunk["steps"]:
                agent_thoughts_placeholder.markdown(
                    f"- Tool Result: `{step.observation}`"
                )
        # Final result
        elif "output" in chunk:
            full_response += chunk["output"]
            response_placeholder.markdown(full_response)
        else:
            raise ValueError()

    agent_thoughts_placeholder.update(
        label="Answered! 🎉",
        expanded=False,
        state="complete",
    )


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

        st.header("Dataset")
        df = choose_dataset()

    if not llm:
        st.stop()

    try:
        agent_executor = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate",
            return_intermediate_steps=True,
        )
    except ValueError:
        st.error("No valid dataset selected.")
        st.stop()

    if query := st.chat_input("Ask me a question!"):
        st.chat_message("user", avatar="🤓").write(query)
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            agent_thoughts_placeholder = st.status("🤔 Pensando...", expanded=True)
            try:
                asyncio.run(
                    answer_question(
                        query,
                        agent_executor,
                        response_placeholder,
                        agent_thoughts_placeholder,
                    )
                )
            except Exception as e:
                print(
                    f"An error occurred: {e}. Try again or reload the page by pressing `R`."
                )


if __name__ == "__main__":
    main()
