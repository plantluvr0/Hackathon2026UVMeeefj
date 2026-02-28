import io
import os.path

import pandas as pd
import streamlit as st
import pymupdf
from streamlit import session_state as ss
from streamlit_pdf_viewer import pdf_viewer
#personal
import gemini
import secure_io

if __name__ == '__main__':
    #globals
    count = 0

    # PATHS TO LOCAL PDF TEMPLATES
    TEMPLATE_1 = "../../../pdfs/admission-form-pdf.pdf"
    TEMPLATE_2 = "../../../pdfs/test_form.pdf"

    # PATH TO PATIENT CSV
    PATIENTS_CSV = os.path.join(os.path.dirname(__file__), "patient_info.csv")

    #df = pd.read_csv(PATIENTS_CSV, dtype=str).fillna("")
    patients, labels = secure_io.inject_data()

    # session state
    if 'pdf_ref' not in ss:
        ss.pdf_ref = None
    if 'output_pdf' not in ss:
        ss.output_pdf = None

    form_fields = [
        "id_number", "name", "age", "gender", "date_of_birth",
        "phone_number", "admission_date", "diagnosis", "doctor",
        "room_number", "insurance", "primary_symptoms_summary"
    ]
    for field in form_fields:
        if field not in ss:
            ss[field] = ""

    #patient id lookup
    lookup_id = st.text_input("Patient ID")

    if st.button("Load Patient"):
        found_patient = None
        for patient in patients:
            if patient[0] == lookup_id.strip():
                found_patient = patient
                break

        if found_patient:
            # Populate fields
            for i, field in enumerate(form_fields):
                if i < len(found_patient):
                    ss[field] = found_patient[i]

            with st.spinner("Fetching data from Gemini..."):
                message = (
                    f"Patient information: {found_patient}. "
                    "Use this info to format an admissions form into a JSON style format."
                )
                if count == 0:
                    response = gemini.gemini_call(message)
                    ss.api_response = response

            st.success(f"Loaded patient {lookup_id} and processed via API.")
        else:
            st.error(f"No patient found with ID {lookup_id}")

    # template
    col1, col2 = st.columns(2)
    if col1.button("Template 1"):
        ss.pdf_ref = TEMPLATE_1
        ss.output_pdf = None
    if col2.button("Template 2"):
        ss.pdf_ref = TEMPLATE_2
        ss.output_pdf = None

    # form
    with st.form("patient_form"):
        ss.id_number = st.text_input("ID Number", value=ss.id_number)
        ss.name = st.text_input("Name", value=ss.name)
        ss.age = st.text_input("Age", value=ss.age)
        ss.gender = st.text_input("Gender", value=ss.gender)
        ss.date_of_birth = st.text_input("Date of Birth", value=ss.date_of_birth)
        ss.phone_number = st.text_input("Phone Number", value=ss.phone_number)
        ss.admission_date = st.text_input("Admission Date", value=ss.admission_date)
        ss.diagnosis = st.text_input("Diagnosis", value=ss.diagnosis)
        ss.doctor = st.text_input("Doctor", value=ss.doctor)
        ss.room_number = st.text_input("Room Number", value=ss.room_number)
        ss.insurance = st.text_input("Insurance", value=ss.insurance)
        ss.primary_symptoms_summary = st.text_area(
            "Primary Symptoms Summary", value=ss.primary_symptoms_summary
        )
        submitted = st.form_submit_button("Write to PDF")

    #submitted logic
    if submitted and ss.pdf_ref:
        data = {
            "id_number": ss.id_number,
            "name": ss.name,
            "age": ss.age,
            "gender": ss.gender,
            "date_of_birth": ss.date_of_birth,
            "phone_number": ss.phone_number,
            "admission_date": ss.admission_date,
            "diagnosis": ss.diagnosis,
            "doctor": ss.doctor,
            "room_number": ss.room_number,
            "insurance": ss.insurance,
            "primary_symptoms_summary": ss.primary_symptoms_summary,
        }
        doc = pymupdf.open(ss.pdf_ref)
        page = doc[0]
        widget_names = {w.field_name: w for w in page.widgets()} if page.widgets() else {}
        if widget_names:
            for key, value in data.items():
                if key in widget_names:
                    w = widget_names[key]
                    w.field_value = value
                    w.update()
        else:
            labels = [
                "ID Number", "Name", "Age", "Gender", "Date of Birth",
                "Phone Number", "Admission Date", "Diagnosis", "Doctor",
                "Room Number", "Insurance",
            ]
            keys = [
                "id_number", "name", "age", "gender", "date_of_birth",
                "phone_number", "admission_date", "diagnosis", "doctor",
                "room_number", "insurance",
            ]
            x, y, step = 50, 60, 20
            for label, key in zip(labels, keys):
                if data[key]:
                    page.insert_text((x, y), f"{label}: {data[key]}", fontsize=11)
                    y += step
            if data["primary_symptoms_summary"]:
                page.insert_text((x, y + 10), "Primary Symptoms Summary:", fontsize=11)
                rect = pymupdf.Rect(x, y + 25, page.rect.width - 50, y + 120)
                page.insert_textbox(rect, data["primary_symptoms_summary"], fontsize=11)
        buf = io.BytesIO()
        doc.save(buf)
        ss.output_pdf = buf.getvalue()
        doc.close()

    # viewer
    if ss.output_pdf:
        st.download_button("Download", data=ss.output_pdf, file_name="filled.pdf", mime="application/pdf")
        pdf_viewer(input=ss.output_pdf, width=700)
    elif ss.pdf_ref:
        with open(ss.pdf_ref, "rb") as f:
            pdf_viewer(input=f.read(), width=700)












