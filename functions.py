import requests

def get_answer_from_openai(question: str, api_key: str):
    openai_url = "https://api.openai.com/v1/completions"

    headers_openai = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data_openai = {
        "model": "text-davinci-002",
        "prompt": f"Question: {question}\nRéponse:",
        "max_tokens": 100
    }

    response_openai = requests.post(openai_url, headers=headers_openai, json=data_openai)

    if response_openai.status_code != 200:
        print(response_openai.status_code)
        print(response_openai)
        return {"error": "Erreur lors de l'appel à l'API OpenAI"}

    answer = response_openai.json()['choices'][0]['text'].strip()

    return {"answer": answer}


def load_data():
    df = pd.read_csv("data_forest_fires.csv")  # Mettez le chemin vers votre fichier CSV
    return df