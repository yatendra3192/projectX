import streamlit as st
import requests
import json

st.title('Text Input & OpenAI Response')

text_input = st.text_input("Enter your text here, e.g., Describe a product")
attributes_input = st.text_input("Enter comma-separated attributes")

if st.button('Analyze and Display'):
    attributes = [attr.strip() for attr in attributes_input.split(',') if attr]
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_SECRET_KEY'
        }

        data = {
            'model': 'gpt-4',
            'messages': [
                { 
                    "role": "system",
                    "content": "You are a helpful assistant. User is trying to convert unstructure text data in to table format.Extract data in Json format for table insert as per given attributes : " + ', '.join(attributes) 
                },
                { 
                    "role": "user", 
                    "content": text_input 
                }
            ]
        }

        response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, data=json.dumps(data))
        api_response = response.json()

        st.write('Full API Response:', api_response)

        formatted_data = [api_response[attr] if attr in api_response else '[Not Found]' for attr in attributes]

        st.table([formatted_data])

    except Exception as e:
        st.error(f'Error: {e}')
