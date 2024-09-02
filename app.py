from flask import Flask, render_template
import urllib.request, json

app = Flask(__name__)

@app.route("/")
def get_list_characters_page():
    url = "https://rickandmortyapi.com/api/character/"
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    
    return render_template("characters.html", characters=dict["results"])

@app.route('/episodios')
def get_episodes():
    url = 'https://rickandmortyapi.com/api/episode'
    response = urllib.request.urlopen(url)
    data = response.read()  
    dict = json.loads(data)

    return render_template('episodes.html', episodes=dict['results'])    


@app.route("/profile/<id>")
def get_profile(id):
    url = "https://rickandmortyapi.com/api/character/" + id
    response = urllib.request.urlopen(url)
    data = response.read()
    character = json.loads(data)


    #Criação do dicionário de episódio, bem como a iteraçaõ sobre episódio.
    #É exatamente a mesma lógica que a demonstração de perfil.

    episodes = []
    for episode_url in character['episode']:
        episode_response = urllib.request.urlopen(episode_url)
        episode_data = episode_response.read()
        episode = json.loads(episode_data)
        episodes.append({
            "id": episode["id"],
            "name": episode["name"],
        })

    # Criação do dicionário para receber todas as informações de perfil.
    profile = {
        "image": character["image"],
        "name": character["name"],
        "status": character["status"],
        "species": character["species"],
        "gender": character["gender"],
        "origin": {
            "name": character["origin"]["name"],
            "url": "/locations/" + str(character["origin"]["url"].split('/')[-1])  
        },
        "location": {
            "name": character["location"]["name"],
            "url": "/locations/" + str(character["location"]["url"].split('/')[-1])
        }, 
        "episodes": episodes
    }    
    
    return render_template("profile.html", profile=profile)

# Rota para o perfil da localização
@app.route('/location/<int:id>')
def location_profile(id):
    try:
        with urllib.request.urlopen(f'https://rickandmortyapi.com/api/location/{id}') as response:
            location_data = json.loads(response.read().decode())
        characters = []
        for character_url in location_data['residents']:
            with urllib.request.urlopen(character_url) as character_response:
                characters.append(json.loads(character_response.read().decode()))
        return render_template('location.html', location=location_data, characters=characters)
    
    except urllib.error.URLError as e:
        print(f'Erro ao buscar dados da API: {e}')
        return render_template('404.html'), 404
    except json.JSONDecodeError as e:
        print(f'Erro ao decodificar a resposta JSON: {e}')
        return render_template('404.html'), 404
    except Exception as e:
        print(f'Erro inesperado: {e}')
        return render_template('404.html'), 404