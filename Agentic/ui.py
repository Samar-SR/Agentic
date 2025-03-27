import streamlit as st
import requests


title = st.text_input("Enter Query", "")

if title:
    response = requests.post(url=f"http://127.0.0.1:8000/result?query={title}")

    output = response.json()

    st.write(output)





