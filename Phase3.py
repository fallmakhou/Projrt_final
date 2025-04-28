import streamlit as st
import spacy
from spacy import displacy

"""
Phase 3 - Reconnaissance d'entités nommées (NER)

Dans cette phase, nous utilisons le modèle NER de spaCy pour extraire des entités nommées telles que des noms de personnes, des dates, des lieux, des organisations, des compétences, etc.
Nous utilisons le modèle linguistique de spaCy pour analyser le texte et identifier ces entités.
L'utilisateur peut voir un affichage graphique des entités extraites grâce à la visualisation intégrée dans Streamlit.
"""

# Charger le modèle spaCy pour la langue française
nlp = spacy.load('fr_core_news_sm')

# Fonction pour effectuer la reconnaissance d'entités
def recognize_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities

# Fonction pour visualiser les entités extraites
def visualize_entities(text):
    doc = nlp(text)
    html = displacy.render(doc, style='ent', page=True)
    return html

# Interface Streamlit
def main():
    st.title("Phase 3 - Reconnaissance d'entités depuis le CV")

    uploaded_text = st.text_area("Coller ici le texte extrait du CV :", height=300)

    if uploaded_text:
        if st.button("Reconnaître les entités"):
            # Reconnaissance des entités
            entities = recognize_entities(uploaded_text)
            st.success("Entités extraites avec succès 🎉")

            # Affichage des entités extraites
            st.subheader("Entités Extraites :")
            st.json(entities)

            # Visualisation graphique des entités
            st.subheader("Visualisation des entités :")
            html = visualize_entities(uploaded_text)
            st.components.v1.html(html, height=400)

if __name__ == "__main__":
    main()
