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

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. User is trying to convert unstructured text data into table format. Extract data in JSON format for table insert as per given attributes: " + ", ".join(attribute_list)},
                    {"role": "user", "content": user_text},
                ],
            )

            response_json = response.choices[0].message.content
            extracted_data = [response_json.get(attr, "[Not Found]") for attr in attribute_list]

            # Display Results in Table
            st.table(dict(zip(attribute_list, extracted_data)))

            # Optional: Show Full API Response
            # st.write("Full API Response:", response)

        except Exception as e:
            st.error(f"Error: {e}")
