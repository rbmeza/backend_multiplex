from flask import Flask, request
from flask_cors import CORS, cross_origin
from markupsafe import escape
import openai

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

openai.api_key = "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"

@app.route("/<name>")
def hello_world(name):
    return f"<p>Hello, {escape(name)}!</p>"

@app.route("/recipe", methods=["POST"])
@cross_origin()
def recepie():
    ingredients = request.get_json()
    list_ingredients = ""
    
    for ingredient in ingredients:
        list_ingredients += ingredient + ", "

    prompt = """Eres un chef profesional. Tengo una página web donde un usuario escoge los ingredientes que quiere incluir en una receta. Necesito que escribas una receta con los ingredientes listados al final, usando la siguiente estructura: 
                [Nombre de la receta]
                [Tiempo de cocción]
                [Porciones]
                [Lista de ingredientes con sus respectivas cantidades]
                [Pasos a seguir]
                [Aporte calórico]
                Entrega el título de la receta entre tags de html <h2>, la lista de ingredientes entre tags <ul>, cada uno de los ingredientes y sus cantidades entre tags <li>, la lista de pasos a seguir entre tags <ol>, cada paso entre tags <li> y las porciones y el aporte calórico entre tags <p>
                Ingredientes:"""
    output = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.3,
        max_tokens=60,
    )

    json_response = {
        "recipe": output["choices"][0]["text"],
    }

    return json_response