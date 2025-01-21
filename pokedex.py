import requests
import json
import os

def get_pokemon_data(pokemon_name):
    """Obtiene los datos de un Pokémon desde la API."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:   
            return response.json() #Devuelve los datos como un diccionario 
        elif response.status_code == 404:
            print("Pokémon no encontrado. Por favor, verifica el nombre.")
        else:
            print(f"Error al obtener los datos. Código de estado : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    return None

def display_pokemon_info(data):
    """Muestra informacion del Pokémon."""
    print(f"\n Nombre: {data['name'].capitalize()}")
    print("Tipos:",",".join([t['type']['name']for t in data['types']]))
    print("Habilidades:",",".join([a['ability']['name'] for a in data ['abilities']]))
    print(f"Peso: {data['weight']} hectogramos")
    print(f"Altura: {data['height']} decímetros")

def save_to_file(pokemon_name, data, file="pokemon_history.json"):
    """Guarda los datos del Pokémon en un archivo JSON."""
    pokemon_info = {
        "name": data['name'],
        "types": [t['type']['name'] for t in data['types']],
        "abilities": [a['ability']['name'] for a in data['abilities']],
        "weight": data['weight'],
        "height": data['height']
    }

    try:
        # Verificar si el archivo existe y no está vacío
        if os.path.exists(file) and os.path.getsize(file) > 0:
            with open(file, "r") as f:
                history = json.load(f)
        else:
            history = []  # Inicializar como lista vacía si el archivo no existe o está vacío

        # Añadir el nuevo Pokémon al historial
        history.append(pokemon_info)

        # Guardar el historial actualizado
        with open(file, "w") as f:
            json.dump(history, f, indent=4)

        print(f"Datos de {pokemon_name.capitalize()} guardados en '{file}'.")
    except Exception as e:
        print(f"Error al guardar en JSON: {e}")
def load_from_json(file="pokemon_history.json"):
    """Carga y muestra el historial de busquedas desde un archivo JSON."""
    try:
        with open(file, "r") as f:
            history = json.load(f)
            print("\nHistorial de búsquedas:")
            for pokemon in history:
                print(f"- {pokemon['name'].capitalize()} (Tipos: {','.join(pokemon['types'])})")
    except FileNotFoundError:
        print("\nNo se encontró un historial. Busca un Pokémon primero.")
    except Exception as e:
        print(f"Error al leer el historial: {e}")

def compare_pokemon(pokemon1, pokemon2):
    """ Compara el peso y la altura de dos Pokémon."""
    data1 = get_pokemon_data(pokemon1)
    data2 = get_pokemon_data(pokemon2)

    if data1 and data2:
        print("\nComparación:")
        print(f"{pokemon1.capitalize()} - Peso: {data1['weight']} hectogramos, Altura: {data1['height']} decímetros")
        print(f"{pokemon2.capitalize()} - Peso: {data2['weight']} hectogramos, Altura: {data2['height']} decímetros")

        heavier = pokemon1 if data['weight'] > data2['weight'] else pokemon2
        taller = pokemon1 if data1['height'] > data2['height'] else pokemon2

        print(f"Más pesado: {heavier.capitalize()}")
        print(f"Más alto: {taller.capitalize()}")
    else:
        print("No se pudieron obtener datos para uno o ambos Pokémon.")

if __name__=="__main__":
    print("Bienvenido a la pokédex CLI!")
    while True:
        print("\nOpciones:")
        print("1. Buscar un Pokémon")
        print("2. Comparar dos Pokémon")
        print("3. Ver historial de búsquedas")
        print("4. Salir")
        option = input("Selecciona una opción: ").strip()

        if option == "1":
            pokemon_name = input("\nIngresa el nombre de un Pokémon: ").strip()
            data = get_pokemon_data(pokemon_name)
            if data:
                display_pokemon_info(data)
                save_to_file(pokemon_name, data)
        elif option == "2":
            pokemon1 = input("\nIngresa el nombre del primer pokémon: ").strip()
            pokemon2 = input("\nIngresa el nombre del segundo Pokémon: ").strip()
            compare_pokemon(pokemon1, pokemon2)
        elif option == "3":
            load_from_json()
        elif option == "4":
            print("¡Adiós!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")




        