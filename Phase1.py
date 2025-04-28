import streamlit as st
import pytesseract
from PIL import Image
from docx import Document
from pdfminer.high_level import extract_text as pdfminer_extract_text
import re

# --------- Fonctions Utilitaires ---------

def extract_text(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        text = pdfminer_extract_text(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif uploaded_file.name.endswith(('.png', '.jpg', '.jpeg')):
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image, lang='fra')
    else:
        text = ""
    return text


def clean_text(text):
    return " ".join(text.split())


def extract_basic_info(text):
    email = re.findall(r"\S+@\S+", text)
    phone = re.findall(r"\b\d{10}\b", text)
    return {
        "Emails": email,
        "Téléphones": phone
    }

# --------- Interface Streamlit ---------

def main():
    st.title("Phase 1 - Extraction de données depuis CV")

    uploaded_file = st.file_uploader("Uploader un CV", type=["pdf", "docx", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        st.success("Fichier reçu avec succès ✅")

        with st.spinner('Extraction du texte en cours...'):
            text = extract_text(uploaded_file)
            cleaned_text = clean_text(text)
            info = extract_basic_info(cleaned_text)

        st.subheader("Texte Extrait :")
        st.text_area("Contenu du CV", cleaned_text, height=300)

        st.subheader("Informations Clés :")
        st.json(info)


if __name__ == "__main__":
    main()
