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
        r = requests.post(f'{api}/ask', json={'question': question}, timeout=120)
        r.raise_for_status(); data = r.json()

        st.subheader("AI-Generated Answer")
        st.write(data["answer"])

        st.subheader("Retrieved Evidence")
        for citation in data.get("citations", []):
            st.markdown(
                f"**Source: {citation['source']} | Page {citation['page']}**"
            )
            st.write(citation["text"])
            st.divider()
        with st.expander('Retrieval scores and citations'):
            st.json(data['citations'])
    except requests.RequestException as exc:
        st.error(str(exc))
