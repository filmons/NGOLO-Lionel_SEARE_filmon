import streamlit as st
import requests
from fastapi import FastAPI, Query
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
from pydantic import BaseModel
import numpy as np
from functions import get_answer_from_openai
from typing import Optional
from pydantic import BaseModel
import os

tags_metadata = [
    {
        "name": "Text",
        "description": "Operations with text.",
    },
    {
        "name": "Numbers",
        "description": "Operations with numbers.",
    },
]


app = FastAPI(
    title="FastAPI for Forest Fires",
    openapi_tags=tags_metadata,
    description="""
#
This is a very fancy project, with auto docs for the API and everything"
""",
)

# Mapping pour les mois
month_mapping = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
}

# Mapping pour les jours
day_mapping = {
    'sun': 1, 'mon': 2, 'tue': 3, 'wed': 4, 'thu': 5, 'fri': 6, 'sat': 7
}


class ForestData(BaseModel):
    month: str
    day: str
    FFMC: float
    DMC: float
    DC: float
    ISI: float
    temp: float
    RH: float
    wind: float
    rain: float
    X: float
    Y: float

@app.get("/", tags=["Text"])
def hello_world():
    return {"message": "Hello World"}

@app.get("/hello_you", tags=["Text"])
def hello_you(name='John Doe'):
    return {"message": f"Hello {name}"}

@app.post("/training")
def train_model(file: str):
    # Charger le dataset
    data = pd.read_csv(file)

    #Conversion des données
    data['month'] = data['month'].map(month_mapping)
    data['day'] = data['day'].map(day_mapping)


    # Sélectionner les caractéristiques et la cible
    X = data.drop(columns=['area'])
    y = data['area']

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normaliser les données
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Créer le modèle
    model = Sequential([
    Dense(64, input_shape=(12,), activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='linear')
])

    # Compiler le modèle
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Entraîner le modèle
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

    # Sauvegarder le modèle
    model.save('forest_fire_model.h5')

    return {"message": "Modèle entraîné et sauvegardé avec succès"}


# --------------------------
# Fonction pour faire une prédiction en utilisant l'API

@app.post("/predict")
def predict(data: ForestData):
    # Convertir les mois en numérique
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    data.month = months.index(data.month) + 1

    # Convertir les jours en numérique
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    data.day = days.index(data.day) + 1

    # Préparation des données pour la prédiction
    data_dict = data.dict()
    data_list = list(data_dict.values())

    # Convertir la liste en un tableau NumPy
    data_array = np.array([data_list], dtype=np.float32)

    # Charger le modèle et effectuer la prédiction
    model = load_model('forest_fire_model.h5')
    prediction = model.predict(data_array)

    return {"Prediction": float(prediction[0])}

@app.get("/model")
async def get_answer_endpoint(question: str = Query(..., description="La question pour laquelle vous souhaitez obtenir une réponse")):
    api_key = os.getenv("OPENAI_API_KEY") 
    # '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'
    return get_answer_from_openai(question, api_key)


# Interface utilisateur avec Streamlit
def main():
    st.title("Prédiction des incendies de forêt")

    # Chargement des données
    data = load_data()

    # Sélection des fonctionnalités pour la prédiction
    selected_features = st.multiselect("Sélectionnez les fonctionnalités", data.columns)

    if len(selected_features) == 0:
        st.warning("Veuillez sélectionner au moins une fonctionnalité.")
        return

    # Affichage des fonctionnalités sélectionnées
    st.write("Vous avez sélectionné les fonctionnalités suivantes:")
    st.write(selected_features)

    # Affichage des statistiques des fonctionnalités sélectionnées
    st.write("Statistiques des fonctionnalités sélectionnées:")
    st.write(data[selected_features].describe())

    # Saisie des valeurs des fonctionnalités pour la prédiction
    feature_data = {}
    for feature in selected_features:
        feature_value = st.number_input(f"Valeur de {feature}", min_value=0.0)
        feature_data[feature] = feature_value

    # Prédiction lorsque l'utilisateur appuie sur le bouton
    if st.button("Prédire"):
        prediction = predict(feature_data)
        st.write(f"Prédiction : {prediction}")

if __name__ == "__main__":
    main()
