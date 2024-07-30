import streamlit as st
import openai
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

def humanize_text_openai(input_text, prompt, model):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Humanize this text: {input_text}"}
        ]
    )
    return response.choices[0].message['content']

import streamlit as st
import openai
import anthropic
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

def humanize_text_openai(input_text, prompt, model):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Humanize this text: {input_text}"}
        ]
    )
    return response.choices[0].message['content']


def humanize_text_anthropic(input_text, prompt):
    client = anthropic.Anthropic(api_key=anthropic_api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Humanize this text: {input_text}"}
        ],
        model="claude-3-5-sonnet-20240620",
    )
    return chat_completion.choices[0].message.content

# ... (rest of the code remains the same)

def humanize_text_groq(input_text, prompt):
    client = Groq(api_key=groq_api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Humanize this text: {input_text}"}
        ],
        model="mixtral-8x7b-32768",
    )
    return chat_completion.choices[0].message.content

st.title("AI-powered Text Humanizer")

# Model selection
model_option = st.selectbox(
    "Choose an LLM model:",
    ("mixtral-8x7b-32768", "GPT-4o", "claude-3-5-sonnet-20240620")
)

# Input text area
input_text = st.text_area("Enter the text you want to humanize:", height=150)

# Prompt input
prompt = st.text_area("Enter the prompt for humanizing the text:", 
                      value='''
                      # IDENTITY and PURPOSE

You are a writing expert. You refine the input text to enhance clarity, coherence, grammar, and style. You also specialize in making AI-generated text sound more natural and human-like.

# Steps

- Identify patterns typical of AI-generated text, such as overly formal language, repetitive structures, or unnatural phrasing.
- Apply corrections and improvements directly to the text.
- Rephrase sections that sound artificial or pretentious to make them more conversational and authentic.
- Maintain the original meaning and intent of the user's text, ensuring that the improvements are made within the context of the input language's grammatical norms and stylistic conventions.
- Introduce natural language variations and imperfections where appropriate to enhance human-like quality.

# GUIDELINES FOR HUMAN-LIKE WRITING

- Use contractions where appropriate (e.g., "it's" instead of "it is").
- Vary sentence structure and length to create a more natural rhythm.
- Include occasional colloquialisms or idiomatic expressions, if suitable for the context.
- Avoid overly complex vocabulary when simpler words would suffice.
- Incorporate personal pronouns (I, we, you) to create a more engaging tone.
- Add subtle transitions between ideas to improve flow.
- Include mild imperfections or hesitations that are common in human writing (e.g., starting a sentence with "And" or "But" occasionally).

# OUTPUT INSTRUCTIONS

- Refined and improved text that has no grammar mistakes and sounds naturally human-written.
- Return in the same language as the input.
- Ensure the tone is appropriate for the content and intended audience.
- Include NO additional commentary or explanation in the response.

''',
                      height=100)

if st.button("Humanize Text"):
    if input_text and prompt:
        if model_option in ["GPT-4o"] and openai.api_key:
            with st.spinner("Humanizing your text..."):
                humanized_text = humanize_text_openai(input_text, prompt, model_option.lower())
        elif model_option == "mixtral-8x7b-32768" and groq_api_key:
            with st.spinner("Humanizing your text..."):
                humanized_text = humanize_text_groq(input_text, prompt)
        elif model_option == "claude-3-5-sonnet-20240620" and anthropic_api_key:
            with st.spinner("Humanizing your text..."):
                humanized_text = humanize_text_groq(input_text, prompt)
        else:
            st.error(f"API key for {model_option} is missing. Please check your .env file.")
            st.stop()
        
        st.subheader("Humanized Text:")
        st.write(humanized_text)
    else:
        st.warning("Please enter both input text and prompt.")

st.sidebar.header("About")
st.sidebar.info("This app uses various LLM models to make text sound more human-like based on the provided prompt.")
