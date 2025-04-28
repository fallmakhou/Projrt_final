import spacy
from spacy.matcher import Matcher
import re

# Charger le modèle de langue spaCy
nlp = spacy.load("fr_core_news_sm")

# Exemple de texte extrait d'un CV
cv_text = """
Riyad Haymad a travaillé chez Google en tant que Data Scientist de 2018 à 2022. 
Il a également étudié à l'Université de Paris où il a obtenu un Master en Informatique en 2017. 
Il maîtrise les compétences en Python, Machine Learning et Data Science.
Jean a participé à plusieurs projets incluant des analyses de données pour des entreprises comme Facebook et Apple.
"""

# Traitement du texte avec spaCy
doc = nlp(cv_text)

# Fonction pour extraire les relations entre les entités
def extract_relations(doc):
    relations = []
    
    # Relation entre le nom de la personne et son expérience professionnelle
    name = None
    experience = []
    for ent in doc.ents:
        if ent.label_ == "PER":  # Entités de type Personne
            name = ent.text
        elif ent.label_ == "ORG":  # Entités de type Organisation (entreprise)
            experience.append(ent.text)
        elif ent.label_ == "DATE":  # Entités de type Date
            experience.append(ent.text)
    
    # Lier le nom aux expériences professionnelles
    if name and experience:
        relations.append({"Nom": name, "Expérience professionnelle": experience})
    
    # Relation entre le nom et la formation académique
    education = []
    for ent in doc.ents:
        if ent.label_ == "ORG":  # Université ou école
            education.append(ent.text)
        elif ent.label_ == "DATE":  # Année d'obtention du diplôme
            education.append(ent.text)
    
    if name and education:
        relations.append({"Nom": name, "Formation académique": education})
    
    # Relation entre les compétences et les entreprises/éducation
    skills = []
    for token in doc:
        if token.text.lower() in ["python", "machine learning", "data science"]:
            skills.append(token.text)
    
    if skills:
        for ent in doc.ents:
            if ent.label_ == "ORG" or ent.label_ == "GPE":  # Organisation ou Lieu
                relations.append({"Compétences": skills, "Entreprise/Éducation": ent.text})
    
    # Relation entre les projets et les technologies (exemple simple)
    projects = []
    for sent in doc.sents:
        if "projet" in sent.text.lower() or "analyse de données" in sent.text.lower():
            projects.append(sent.text)
    
    if projects:
        relations.append({"Projets": projects, "Technologies": skills})
    
    return relations

# Extraire les relations
relations = extract_relations(doc)

# Afficher les relations extraites
for relation in relations:
    print(relation)
