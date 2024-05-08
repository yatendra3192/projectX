import streamlit as st
import openai

st.title("OpenAI Attribute Extraction")

# API Key Input
api_key = st.text_input("OpenAI API Key", type="password")

# Text Input
user_text = st.text_area("Enter Your Text Here:")

# Attribute Headers Input
attributes = st.text_input("Enter Attribute Headers (comma-separated):")
attribute_list = [attr.strip() for attr in attributes.split(",")] if attributes else []

# Submit Button
if st.button("Extract Attributes"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not user_text:
        st.error("Please enter some text.")
    elif not attribute_list:
        st.error("Please enter at least one attribute header.")
    else:
        try:
            openai.api_key = api_key

            response = openai.Completion.create(
                engine="text-davinci-003",  # You might need to adjust the engine based on your needs
                prompt=(
                    "You are a helpful assistant. User is trying to convert unstructured text data into table format. "
                    "Extract data in JSON format for table insert as per given attributes: " + ", ".join(attribute_list) +
                    "\n\nText: " + user_text
                ),
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )

            response_json = response.choices[0].text.strip()
            # ... (rest of the code remains the same)

        except Exception as e:
            st.error(f"Error: {e}")
