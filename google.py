import streamlit as st
import openai
import json
from streamlit_handsontable import st_handsontable

# Set page configuration
st.set_page_config(page_title="OpenAI Integration with Handsontable", layout="wide")

# Input fields for API key, text input, and attributes
st.title("Text Input & OpenAI Response")
api_key = st.text_input("Please provide your API Key:")
user_input = st.text_area("Enter your text here, e.g., Describe a product")
attributes_input = st.text_input("Enter comma-separated attributes")

# Process attributes
attributes = [attr.strip() for attr in attributes_input.split(",")]

# Submit button
if st.button("Analyze and Display"):
    try:
        # Set API key
        openai.api_key = api_key

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. User is trying to convert unstructured text data into table format. Extract data in Json format for table insert as per given attributes : " + ", ".join(attributes)},
                {"role": "user", "content": user_input},
            ],
        )

        # Parse response and extract data
        response_json = json.loads(response.choices[0].message.content)
        formatted_data = [response_json.get(attr, "[Not Found]") for attr in attributes]

        # Display full API response
        st.subheader("Full API Response:")
        st.json(response)

        # Display table with Handsontable
        st.subheader("Extracted Data:")
        st_handsontable(pd.DataFrame([formatted_data], columns=attributes), height=300, width=700)

    except Exception as e:
        st.error(f"Error: {e}")
