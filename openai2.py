import streamlit as st
import openai
import json

# Define the text boxes and button.
api_key = st.text_input("Please provide your API Key:")
user_prompt = st.text_input("Enter your text:")
attribute_headers = st.text_input("Enter comma-separated attributes:")
submit = st.button('Analyze and Display')

if submit:
    # Set the OpenAI API key.
    openai.api_key = api_key

    # Convert the comma-separated attribute headers into a list.
    attributes = [attr.strip() for attr in attribute_headers.split(',') if attr.strip()]

    # Initialize the OpenAI completion.
    response = openai.Completion.create(
        engine="gpt-4",
        prompt="User is trying to convert unstructured text data into table format. Extract data in Json format for table insert as per given attributes : " + ', '.join(attributes) + " " + user_prompt,
        temperature=0.5,
        max_tokens=100
    )
    
    # Parse the OpenAI API response.
    response_data = json.loads(response.choices[0].text.strip())

    # Filter the response data based on the attribute headers and format as a list of dictionaries for the Streamlit table.
    tabular_data = [{attr: response_data.get(attr, '[Not Found]') for attr in attributes}]

    # Display the API response.
    st.write("Full API Response:-")
    st.json(response_data)

    # Display the formatted data.
    st.write("Formatted Data:-")
    st.table(tabular_data)
