import os

import requests
from openai import OpenAI

OPENAI_API_KEY = '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'

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_bard(question):
    response = client.chat.completions.create(
        model="text-davinci-003",  # Specify "text-davinci-003" for the "bard" model
        messages=question,
        max_tokens=50
    )
    return response.choices[0].message.content


def get_nutritional_info(food_name):
    api_endpoint = "https://trackapi.nutritionix.com/v2/search/instant"
    app_id = "705ee908"
    app_key = "c6d88d8fef5107c7c69066f195056e73"
    params = {
        "query": food_name,
        "appId": app_id,
        "appKey": app_key
    }

    response = requests.get(api_endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        hits = data.get('hits', [])
        if hits:
            return hits[0]['fields']
        else:
            return None
    else:
        print("Failed to fetch nutritional information.")
        return None


def interact_with_chatbot():
    print("Welcome to the Fitness Chatbot!")
    print("You can ask me any questions related to workout routines, dietary advice, etc.")
    print("Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Exiting...")
            break

        response = ask_bard(user_input)
        print("Fitness Chatbot:", response)

        # Check if user is asking about nutritional information
        if "nutrition" in user_input.lower() or "calories" in user_input.lower():
            food_name = user_input.split("about")[-1].strip()
            nutritional_info = get_nutritional_info(food_name)
            if nutritional_info:
                print("Nutritional Information for", food_name + ":")
                print("Calories:", nutritional_info.get('calories'))
                print("Fat:", nutritional_info.get('fat'))
                print("Protein:", nutritional_info.get('protein'))
                print("Carbohydrates:", nutritional_info.get('carbohydrates'))
            else:
                print("Sorry, I couldn't find nutritional information for", food_name)


if __name__ == "__main__":
    interact_with_chatbot()
