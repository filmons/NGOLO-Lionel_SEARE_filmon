# 🌲 Prédiction des incendies de forêt 🔥

## Dépendances

Ce script Python utilise les librairies suivantes :

- Fastapi.
- Numpy.
- Pandas.
- Pydantic.
- Requests.
- Scikit-learn.
- Streamlit.
- Tensorflow.
- Typing.

## Installation

1. Ouvrez un terminal et placez-vous dans le répertoire actuel du projet.

2. Installez les librairies requises.

```
pip install -r requirements.txt
```

N.B : Pour vérifier que l'installation fonctionne sans forcément installer les dépendances requises, vous pouvez également simuler l'installation :

```
pip install -r requirements.txt --dry-run
```

## Utilisation

1. Exécutez le script.

```
python -m uvicorn api:app --reload
```

```
streamlit run app_web.py
```

2. Une fois le script lancé, accédez à l'adresse suivante dans votre navigateur : http://localhost:8501

Si une adresse locale (LOCAL_URL) différente est indiquée par la console, utilisez la.

Groupe : Lionel,Filmon
