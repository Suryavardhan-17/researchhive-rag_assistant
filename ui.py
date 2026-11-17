import streamlit as st
import requests
st.set_page_config(page_title='ResearchHive', layout='wide')
st.title('ResearchHive | Document Q&A')
st.caption('Evidence-first local demo. Answers show retrieved passages, not LLM-generated prose.')
api = st.sidebar.text_input('API URL', 'http://localhost:8000')
file = st.file_uploader('Upload a text-based PDF', type=['pdf'])
if file and st.button('Index PDF'):
    try:
        r = requests.post(f'{api}/documents', files={'file': (file.name, file.getvalue(), 'application/pdf')}, timeout=60)
        r.raise_for_status(); st.success(r.json())
    except requests.RequestException as exc: st.error(str(exc))
question = st.text_input('Ask a question about your documents')
if st.button('Search') and question:
    try:
        r = requests.post(f'{api}/ask', json={'question': question}, timeout=30)
        r.raise_for_status(); data = r.json()
        st.write(data['answer'])
        with st.expander('Retrieval scores and citations'): st.json(data['citations'])
    except requests.RequestException as exc: st.error(str(exc))
