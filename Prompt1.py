import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Your goal is to answer questions as a funny British person. Use humor and joke in every response.
    
    Below is the question:
    PARAGRAPHS: {text}
    
    YOUR RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["text"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Chat with a Funny British Bot", page_icon=":robot:")
st.header("Funny Bot")

st.markdown("## What do you want to ask Funny Bot")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

def get_text():
    input_text = st.text_area(label="Question", label_visibility='collapsed', placeholder="...", key="text_input")
    return input_text

text_input = get_text()


def update_text_with_example():
    print ("in updated")
    st.session_state.text_input = text_input

st.button("*See An Example Response*", type='secondary', help="Click to see an example of the text you will be converting.", on_click=update_text_with_example)

if text_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_text = prompt.format(text=text_input)

    formatted_text = llm(prompt_with_text)

    st.write(formatted_text)
