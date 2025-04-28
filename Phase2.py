import streamlit as st
import re
import unidecode

"""
Phase 2 - Nettoyage des données

Après l'extraction brute du texte, cette phase consiste à nettoyer et normaliser les données.
Le nettoyage comprend la suppression des caractères spéciaux inutiles, des espaces multiples,
et la correction des incohérences de formatage (majuscules/minuscules, accents, etc.).
L'objectif est d'obtenir un texte propre, cohérent et structuré, prêt à être utilisé
pour des étapes d'analyse avancée comme l'extraction d'entités ou la classification.
"""

# --------- Fonctions Utilitaires ---------

def advanced_clean_text(text):
    # Suppression des caractères non ASCII
    text = unidecode.unidecode(text)
    # Suppression des caractères spéciaux
    text = re.sub(r'[^\w\s]', ' ', text)
    # Suppression des espaces multiples
    text = re.sub(r'\s+', ' ', text)
    # Passage en minuscules
    text = text.lower()
    return text.strip()

# --------- Interface Streamlit ---------

def main():
    st.title("Phase 2 - Nettoyage avancé des données")

    uploaded_text = st.text_area("Coller ici le texte extrait du CV :", height=300)

    if uploaded_text:
        if st.button("Nettoyer le texte"):
            cleaned_text = advanced_clean_text(uploaded_text)
            st.success("Texte nettoyé avec succès 🎉")

            st.subheader("Texte Nettoyé :")
            st.text_area("Contenu Nettoyé", cleaned_text, height=300)

if __name__ == "__main__":
    main()
