import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below are paragraphs that contain incorrect grammar.
    Your goal is to:
    - Correct the grammar of the paragraphs
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: It was great to meet you. 
    - Warm: It was wonderful to meet you!  
    - Casual: Great to meet you!

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Below is the text, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    PARAGRAPHS: {text}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "text"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Grammar Genie", page_icon=":robot:")
st.header("Grammar Genie")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Beautify your writing")

with col2:
    pass

st.markdown("## Enter Your Paragraphs To Beautify")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your paragraphs to have?',
        ('Formal', 'Warm', 'Casual'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

def get_text():
    input_text = st.text_area(label="Text Input", label_visibility='collapsed', placeholder="Your Email...", key="text_input")
    return input_text

text_input = get_text()

# if len(text_input.split(" ")) > 700:
#     st.write("Please enter a shorter email. The maximum length is 700 words.")
#     st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.text_input = text_input

st.button("*See An Example*", type='secondary', help="Click to see an example of the text you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Beautified Text:")

if text_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_text = prompt.format(tone=option_tone, dialect=option_dialect, email=text_input)

    formatted_text = llm(prompt_with_text)

    st.write(formatted_text)
