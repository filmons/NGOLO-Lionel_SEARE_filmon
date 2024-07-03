import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="App des Incendies de Forêt", page_icon="🔥", layout="wide")

# Charger et préparer les données
@st.cache
def load_data():
    data = pd.read_csv("data_forest_fires.csv")
    # Convertir les mois en numérique
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    data['month'] = data['month'].apply(lambda x: months.index(x) + 1)
    # Convertir les jours en numérique
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    data['day'] = data['day'].apply(lambda x: days.index(x) + 1)
    return data

df = load_data()

# Header principal de l'application
st.title("Projet de Prédiction des Incendies de Forêt")
st.header("Utiliser l'IA pour comprendre et prédire les incendies de forêt")

# Sidebar pour la navigation
st.sidebar.header("Navigation")
sidebar_options = ["Introduction", "À propos des Données", "Visualisations", "Documentation"]
selection = st.sidebar.radio("Aller à", options=sidebar_options)

# Gestion de la navigation
if selection == "Introduction":
    st.subheader("Introduction")
    st.write("""
    ## Étapes du Projet jusqu'à la Prédiction des Incendies de Forêt
    
    Ce projet a pour objectif de prédire les incendies de forêt en utilisant des techniques d'intelligence artificielle. Les étapes principales du projet sont les suivantes :
    
    ### 1. Collecte des Données
    - **Source des Données** : Les données sont collectées à partir de diverses sources telles que des capteurs météorologiques, des rapports d'incendies, et des bases de données publiques.
    - **Variables** : Les données comprennent des variables comme la température, l'humidité, la vitesse du vent, la pluie, et la superficie brûlée.

    ### 2. Préparation des Données
    - **Nettoyage des Données** : Les données brutes sont nettoyées pour supprimer les valeurs manquantes et les anomalies.
    - **Transformation des Données** : Les variables catégorielles telles que les mois et les jours sont converties en valeurs numériques pour faciliter l'analyse et la modélisation.

    ### 3. Analyse Exploratoire des Données (EDA)
    - **Visualisation des Données** : Utilisation de graphiques pour comprendre les distributions et les relations entre les variables.
    - **Statistiques Descriptives** : Calcul des mesures de tendance centrale et de dispersion pour résumer les données.

    ### 4. Développement du Modèle d'IA
    - **Outils Utilisés** : 
        - **Langage de Programmation** : Python
        - **Bibliothèques** : Scikit-learn pour le machine learning, Pandas pour la manipulation des données, Matplotlib et Seaborn pour les visualisations.
    - **Sélection du Modèle** : Choix des algorithmes appropriés (par exemple, régression linéaire, forêts aléatoires, réseaux de neurones) en fonction des données et des objectifs du projet.
    - **Entraînement du Modèle** : Utilisation des données préparées pour entraîner le modèle d'IA. Par exemple, un modèle de régression linéaire pour prédire la superficie brûlée en fonction des variables météorologiques.
    - **Évaluation du Modèle** : Mesure des performances du modèle à l'aide de métriques telles que l'exactitude, la précision, et le rappel. Validation croisée pour évaluer la robustesse du modèle.

    ### 5. Déploiement et Visualisation
    - **Déploiement** : Mise en œuvre du modèle dans une application web en utilisant FastAPI pour le backend et Streamlit pour l'interface utilisateur, permettant de prédire les incendies de forêt en temps réel.
    - **Visualisations** : Création de graphiques interactifs avec Plotly pour permettre aux utilisateurs de visualiser les prédictions et d'explorer les données.
""")

elif selection == "À propos des Données":
    st.subheader("À Propos des Données")
    st.write("Ci-dessous, les données originales sans transformation :")
    original_data = pd.read_csv("data_forest_fires.csv")
    st.dataframe(original_data)
    st.write("Ci-dessous, les données transformées avec les mois et jours convertis en valeurs numériques :")
    st.dataframe(df)
    st.write("Statistiques descriptives des données transformées :")
    st.write(df.describe())
    st.download_button("Télécharger les Données", data=open("data_forest_fires.csv", "rb"), file_name="data_forest_fires.csv")

elif selection == "Visualisations":
    st.subheader("Visualisations")
    
    # Histogramme des Températures
    st.write("### Distribution des Températures")
    st.write("Cette visualisation montre comment les valeurs de température sont réparties dans l'ensemble des données. "
             "Cela permet d'identifier les plages de température les plus fréquentes et de détecter les valeurs extrêmes.")
    fig_temp = px.histogram(df, x='temp', nbins=30, title="Distribution des Températures")
    st.plotly_chart(fig_temp)

    # Scatter Plot Vitesse du Vent vs. Area
    st.write("### Relation entre Vitesse du Vent et Superficie Brûlée")
    st.write("Ce graphique en nuage de points explore la relation entre la vitesse du vent (exprimée en km/h) et la superficie brûlée. "
             "Les couleurs représentent les différents mois de l'année, permettant d'observer les tendances saisonnières.")
    fig_wind_area = px.scatter(df, x='wind', y='area', color='month', title="Relation entre Vitesse du Vent et Superficie Brûlée")
    st.plotly_chart(fig_wind_area)

    # Moyenne des Aires brûlées par Mois
    st.write("### Moyenne des Aires Brûlées par Mois")
    st.write("Ce diagramme à barres montre la moyenne de la superficie brûlée pour chaque mois. "
             "Cela aide à identifier les mois où les incendies sont les plus fréquents et les plus dévastateurs.")
    df_month_area = df.groupby('month')['area'].mean().reset_index()
    fig_area_month = px.bar(df_month_area, x='month', y='area', title="Moyenne des Aires Brûlées par Mois")
    st.plotly_chart(fig_area_month)

    # Heatmap des Corrélations
    st.write("### Heatmap des Corrélations")
    st.write("La heatmap des corrélations montre les relations linéaires entre les différentes variables du dataset. "
             "Les coefficients de corrélation varient entre -1 et 1 :\n"
             "- **1** : Corrélation positive parfaite\n"
             "- **0** : Aucune corrélation\n"
             "- **-1** : Corrélation négative parfaite\n"
             "Cette visualisation aide à identifier les variables qui sont fortement corrélées entre elles, "
             "ce qui peut être utile pour comprendre les facteurs influençant les incendies de forêt.")
    corr = df.corr()
    fig_heatmap = go.Figure(data=go.Heatmap(z=corr.values,
                                            x=corr.index.values,
                                            y=corr.columns.values,
                                            colorscale='Viridis'))
    fig_heatmap.update_layout(title="Heatmap des Corrélations",
                              xaxis_title="Variables",
                              yaxis_title="Variables")
    st.plotly_chart(fig_heatmap)

elif selection == "Documentation":
    st.subheader("Documentation")
    st.components.v1.iframe("http://127.0.0.1:8000/docs", height=1000, width=1000, scrolling=True)

# Footer/contact
st.sidebar.header("Contact")
st.sidebar.write("Pour plus d'informations, veuillez contacter l'administrateur du projet à admin@example.com.")
