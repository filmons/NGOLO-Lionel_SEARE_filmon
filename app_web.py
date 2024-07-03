import streamlit as st
import requests

# Titre de l'application
st.title('Prédiction des incendies de forêt')

# Sous-titre pour les paramètres
st.subheader('Paramètres')

# Formulaire pour saisir les caractéristiques nécessaires à la prédiction
month = st.selectbox('Mois', ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
day = st.selectbox('Jour', ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'])
FFMC = st.number_input('FFMC', min_value=0.0)
DMC = st.number_input('DMC', min_value=0.0)
DC = st.number_input('DC', min_value=0.0)
ISI = st.number_input('ISI', min_value=0.0)
temp = st.number_input('Température', min_value=0.0)
RH = st.number_input('Humidité relative', min_value=0)
wind = st.number_input('Vitesse du vent', min_value=0.0)
rain = st.number_input('Pluie', min_value=0.0)
X = st.number_input('X', min_value=0.0)
Y = st.number_input('Y', min_value=0.0)

# Bouton pour réaliser la prédiction
if st.button('Prédire'):
    data = {
        'month': month,
        'day': day,
        'FFMC': FFMC,
        'DMC': DMC,
        'DC': DC,
        'ISI': ISI,
        'temp': temp,
        'RH': RH,
        'wind': wind,
        'rain': rain,
        'X': X,
        'Y': Y
    }

    # Faire la requête POST à l'API FastAPI
    response = requests.post('http://127.0.0.1:8000/predict', json=data)

    # Afficher la réponse de l'API
    if response.status_code == 200:
        prediction = response.json()['Prediction']
        st.success(f'Prédiction : {prediction}')
    else:
        st.error('Erreur lors de la prédiction')

# Informations supplémentaires
st.markdown("""
    *FFMC: Fine Fuel Moisture Code (indice de l'humidité des combustibles fins)
    *DMC: Duff Moisture Code (indice de l'humidité de la matière organique)
    *DC: Drought Code (indice de la sécheresse)
    *ISI: Initial Spread Index (indice d'initiation de propagation)
    *Température: Température en degrés Celsius
    *Humidité relative: En pourcentage
    *Vitesse du vent: En km/h
    *Pluie: En mm/m2
    *X: Description de la nouvelle caractéristique X
    *Y: Description de la nouvelle caractéristique Y
""")
