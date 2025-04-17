from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_pokemon_list():
    url = "https://pokeapi.co/api/v2/pokemon?limit=1302"
    response = requests.get(url)
    data = response.json()
    return [pokemon['name'] for pokemon in data['results']]

def get_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return {
        'name': data['name'].title(),
        'image': data['sprites']['front_default'],
        'height': data['height'],
        'weight': data['weight'],
        'abilities': [a['ability']['name'] for a in data['abilities']]
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    pokemon_list = get_pokemon_list()
    selected_pokemon = None

    if request.method == 'POST':
        name = request.form.get('pokemon')
        selected_pokemon = get_pokemon_data(name)

    return render_template('index.html', pokemon_list=pokemon_list, pokemon=selected_pokemon)

if __name__ == "__main__":
    app.run(debug=True)
