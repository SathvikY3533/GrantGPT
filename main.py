import openai
import streamlit as st
import time
import os

from openai.error import AuthenticationError

st.set_page_config(initial_sidebar_state='expanded')

st.title("GrantGPT - :book: :chart_with_upwards_trend:")
st.text(
    "A bot which allows you to generate a grant, as well as analyze how good \nyour own writing is based on the given context!")

st.subheader(":star2: Available features: ")
generate = st.checkbox('Generate Grants', value=True)
analyze = st.checkbox('Analyze Grants')
st.divider()

st.sidebar.title(":key: Instructions:")
st.sidebar.text("1. Choose the feature you want to\n"
                "   use above!\n"
                "2. Input values into the text-areas\n"
                "   - Generating:\n"
                "      1. OpenAI API Key\n"
                "      2. Context\n"
                "   - Analyzing:\n"
                "      1. Piece of writing\n"
                "      2. Desired purpose\n"
                "3. Voila, you have your outcome!")
st.sidebar.title(":sunglasses: About:")
st.sidebar.text(f"""
    Hello! This is one of my first 
    projects realted to NLP and AI! 
    From my experience in the FRC 
    robotics team, Radicubs (#7503), 
    writing grants has been on my 
    weaker sides- mainly I had a 
    hard time brainstorming effective 
    ideas. So, I came up with GrantGPT! 
    Feel free to use this to help you 
    brainstorm or analyze your work. 
    (Caution: responses might not be 
    100% accurate and could contain 
    invalid statements).
""")

# ----------------------------------------------------------------------------------------------------------------------------------------

if (generate):
    st.subheader("Generating Grants :robot_face:")
    openai.api_key = st.text_input(
        label="For the generation process to work, since this bot uses gpt3, it requires an Open API Key to continue.",
        placeholder="Your key here...", type="password")
    # openai.api_key = os.environ["OPENAI_API_KEY"]


    def askGPT(text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text}
            ],
            max_tokens = 400,
            temperature=0.6
        )
        return response.choices[0].message.content


    if (openai.api_key):
        with st.form("my_form"):
            st.write("Grant Information")

            c1, c2 = st.columns([2, 2])
            with c1:
                recipient_name = st.text_input("Recipient Name (non-profit organization, etc.)", placeholder="...")
            with c2:
                sender_name = st.text_input("Sender (you/organization) Name", placeholder="...")

            overview = st.text_area("Provide context for the grant (overview, purpose, question, etc.)",
                                    placeholder="More context can often give you more accurate results...")

            submitted = st.form_submit_button("Submit")
        if submitted:
            prompt = f"""
                Can you write a grant for me? It is to the {recipient_name} organization from me (the {sender_name}). 
                Don't talk about the price given by the grant but talk about how it can benefit the {recipient_name} organization in
                 the future. Here is some more context for this grant, make sure to use valid points so that 
                this grant is straight forward and concise: \n\n {overview} \n Please provide a brief answer in 200 words or less.
                """
            try:
                with st.spinner("Generating..."):
                    generated_text = askGPT(prompt)
                st.success('Your draft is ready!')
                st.write(generated_text)

            except AuthenticationError as e:
                st.error("Please provide a valid OpenAI Api key!")

if (analyze):
    st.subheader('Analyzing Grants  :face_with_monocle:')

st.divider()
st.markdown("<h6 style='text-align: center; padding: none;margin: none; '>Made with ❤ by</h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; padding: none; margin: none;'>Sathvik Yechuri | 2023</h6>",
            unsafe_allow_html=True)
