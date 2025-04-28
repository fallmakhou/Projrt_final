import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Exemple de données extraites des CV (Nom, Email, Compétences, Expérience, etc.)
data = {
    'Nom': ['Alice Dupont', 'Bob Martin', 'Charlie Lemoine'],
    'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
    'Compétences': ['Python, Machine Learning', 'Java, SQL', 'Python, Data Science'],
    'Expérience': ['5 ans', '3 ans', '7 ans'],
    'Diplôme': ['Master en Informatique', 'Licence en Mathématiques', 'Doctorat en Data Science'],
    'Candidat retenu': [1, 0, 1]  # 1 signifie que le candidat a été retenu, 0 non retenu
}

# 1. Stocker les données extraites dans une base de données SQLite
def save_data_to_db(data):
    # Convertir les données en DataFrame
    df = pd.DataFrame(data)
    
    # Connexion à la base de données SQLite (elle sera créée si elle n'existe pas)
    conn = sqlite3.connect('cvs_database.db')
    
    # Sauvegarder le DataFrame dans une table appelée 'candidats'
    df.to_sql('candidats', conn, if_exists='replace', index=False)
    conn.close()
    print("Données sauvegardées dans la base de données.")

# 2. Charger les données depuis la base de données
def load_data_from_db():
    conn = sqlite3.connect('cvs_database.db')
    df = pd.read_sql('SELECT * FROM candidats', conn)
    conn.close()
    return df

# 3. Construire un modèle de machine learning pour prédire si un candidat est retenu
def build_model(df):
    # Préparer les données pour l'entraînement
    X = df[['Compétences', 'Expérience', 'Diplôme']]  # Variables indépendantes
    y = df['Candidat retenu']  # Variable dépendante
    
    # Convertir les données textuelles en variables numériques (vectorisation)
    X = pd.get_dummies(X)
    
    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Entraîner un modèle de Random Forest
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    # Faire des prédictions
    y_pred = model.predict(X_test)
    
    # Évaluer le modèle
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Précision du modèle: {accuracy * 100:.2f}%")
    
    return model

# 4. Exemple d'utilisation
if __name__ == "__main__":
    # Sauvegarder les données dans une base de données
    save_data_to_db(data)

    # Charger les données depuis la base de données
    df = load_data_from_db()
    print(df)

    # Construire et évaluer un modèle de machine learning
    model = build_model(df)
