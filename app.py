from flask import Flask, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
import openai

load_dotenv()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

openai.api_key = os.environ.get("OPENAI_KEY")


@app.route("/recipe", methods=["POST"])
@cross_origin()
def recepie():
    ingredients = request.get_json()
    list_ingredients = "Ingredientes a utilizar: "
    for ingredient in ingredients:
        if ingredient != ingredients[-1]:
            list_ingredients += ingredient + ", "
        else:
            list_ingredients += ingredient + "."

    prompt = """Eres un chef profesional. Necesito que completes la receta usando solo los ingredientes listados 
                al principio. Usa la siguiente estructura: 
                Nombre:
                Tiempo de cocción:
                Porciones:
                Ingredientes:
                Pasos:
                Aporte calórico:
                """
    output = openai.Completion.create(
        engine="text-davinci-003",
        prompt=list_ingredients + prompt,
        temperature=0,
        max_tokens=700,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
    )

    json_response = {
        "recipe": output["choices"][0]["text"]
    }

    return json_response
