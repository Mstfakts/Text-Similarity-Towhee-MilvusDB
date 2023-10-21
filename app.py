import sys
sys.path.insert(0, './')
from src.utils.params import PARAMS
from pymilvus import utility
from database.create_collection import connect_milvusdb
from src.main import load_data_to_milvus, search
import streamlit as st
st.set_page_config(page_title="Job Search - Milvus")


# Connect to DB before doing any operation
try:
    connect_milvusdb()
except Exception as e:
    st.error("Could not connect to DB. Make sure that MilvusDB container is running..")
    st.error(str(e))
else:


    st.title('Job Posting')

    st.markdown('---')

    if 'button_pressed' not in st.session_state:
        st.session_state['button_pressed'] = False

    uploaded_file = None
    # 1. button
    uploaded_file = st.file_uploader(
        "Choose a CSV file to upload to MilvusDB or use the default file", type=['csv'])

    if st.button('Embed & Load Data to MilvusDB'):
        
        if uploaded_file is None:
            st.warning('Upload CSV file first.')

        else:
            try:
                st.session_state['button_pressed'] = True
                with st.spinner('Waiting...'):
                    load_data_to_milvus(path=uploaded_file)
                    st.success("Data has been embedded and loaded.")
            except Exception as e:
                st.error(f'An error occurred: {e}')

    st.markdown('---')

    # 2. button
    user_input = st.text_input("Please enter the text to search:",
                               placeholder='Enter any job description here...')

    if st.button('Predict the Given Text'):
        if not utility.has_collection(PARAMS.DATABASE.COLLECTION_NAME):
            st.write(
                "Please make sure that there exists data in which input will be searched among them.")

        if user_input:
            search_result = search(user_input)
            st.write("Prediction is being processed...")
            st.table(search_result)
        else:
            st.warning("Please enter text to search.")
    st.markdown('---')

    # 3. button
    if st.button('Load Ready-Data'):
        st.write('This feature will be developed.')
    st.markdown('---')
