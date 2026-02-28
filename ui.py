import streamlit as st
from streamlit import session_state as ss
from streamlit_pdf_viewer import pdf_viewer


# declare variable.
if 'pdf_ref' not in ss:
    ss.pdf_ref = None

# access the uploaded ref via a key.
st.file_uploader("Upload PDF file", type=('pdf'), key='pdf')

if ss.pdf:
    ss.pdf_ref = ss.pdf  # backup

# "pdf_ref" should be accessible anywhere in your app.
if ss.pdf_ref:
    binary_data = ss.pdf_ref.getvalue()
    pdf_viewer(input=binary_data, width=700)