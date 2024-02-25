from flask import Flask, render_template, request
import requests as req
from transformers import pipeline
from nltk.corpus import wordnet as wn
import spacy

FOOD_API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/nutrients"
APP_ID = "705ee908"
APP_KEY = "c6d88d8fef5107c7c69066f195056e73"

nlp = spacy.load("en_core_web_sm")

food = wn.synset('food.n.02')
foods = list(set([w for s in food.closure(lambda s: s.hyponyms()) for w in s.lemma_names()]))


def extract_food_name(text):
    doc = nlp(text)
    food_names = []
    for token in doc:
        if token.text in foods:
            food_names.append(token.text)
    return food_names


def ask_bard(question):
    qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

    context = "Fitness is the state of being physically active and healthy. It involves regular exercise, " \
              "proper nutrition,  adequate rest, and overall well-being. Common fitness activities include strength " \
              "training, cardiovascular exercises, flexibility training, and endurance activities. It's important to " \
              "consult with healthcare professionals before starting any new fitness program, especially if you have " \
              "underlying health conditions or concerns. "

    result = qa_pipeline(question=question, context=context)

    return result['answer']


def get_nutritional_info(food_name):
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "Content-Type": 'application/json'
    }
    params = {
        "query": food_name
    }

    try:
        response = req.request("POST", FOOD_API_ENDPOINT, json=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            data = data.get('foods', [])

            return data[0]
    except req.exceptions.RequestException as e:
        print("Error fetching nutritional information:", e)
        return None


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    response = ask_bard(user_input)
    food_names = extract_food_name(user_input)
    food_info = []
    for food_name in food_names:
        nutritional_info = get_nutritional_info(food_name)
        if nutritional_info:
            food_info.append({
                'name': food_name,
                'calories': nutritional_info.get('nf_calories'),
                'fat': nutritional_info.get('nf_total_fat'),
                'protein': nutritional_info.get('nf_protein'),
                'carbohydrates': nutritional_info.get('nf_total_carbohydrate')
            })
    return render_template('index.html', response=response, food_info=food_info)


if __name__ == '__main__':
    app.run(port=5000)
