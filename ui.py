import streamlit as st
import requests


def clear_text():
    st.session_state.my_text = st.session_state.query
    st.session_state.query = ""


st.text_input('Enter text here:', key='query', on_change=clear_text)
query = st.session_state.get('my_text', '')

question = query

if query:
    response = requests.post(url=f"http://127.0.0.1:8000/result?query={query}")

    output = response.json()

    if output.get('result'):
        st.write(f'**Your Question** : {question} ')
        st.header(f'**Result**')
        st.write(output.get('result'))

    else:
        st.write('Some exception occurs')
