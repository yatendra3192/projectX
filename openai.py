import streamlit as st
import openai
import json
import pandas as pd

st.title('Text Input & OpenAI Response')

api_key = st.text_input('Please provide your API Key:', type='password')

user_input = st.text_input('Enter your text here, e.g., Describe a product')
attributes_input = st.text_input('Enter comma-separated attributes')

if st.button('Analyze and Display'):
    if api_key and user_input and attributes_input:
        attributes = [attr.strip() for attr in attributes_input.split(',') if attr]
        
        openai.api_key = api_key

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. User is trying to convert unstructured text data into table format. Extract data in Json format for table insert as per given attributes : " + ', '.join(attributes),
                    },
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
            )
            response_json = json.loads(response['choices'][0]['message']['content'])
            
            st.text('Full API Response:')
            st.write(response)

            formatted_data = {}
            
            for attr in attributes:
                formatted_data[attr] = response_json.get(attr, '[Not Found]')
                
            df = pd.DataFrame(formatted_data, index=[0])
            st.dataframe(df)

        except Exception as e:
            st.error(f'Error fetching data: {e}')
    else:
        st.error('Please fill all inputs.')
