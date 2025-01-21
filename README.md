
# Pokédex CLI

Un proyecto en Python que permite buscar información sobre cualquier Pokémon utilizando la API de PokeAPI. La aplicación se ejecuta desde la línea de comandos.

## Características

- **Buscar Pokémon:** Consulta datos como tipos, habilidades, peso y altura de un Pokémon.
- **Historial de búsqueda:** Guarda cada búsqueda en un archivo `pokemon_history.json`.
- **Comparación:** Compara dos Pokémon por su peso y altura.
- **Menú interactivo:** Permite elegir entre diferentes opciones de forma sencilla.

## Requisitos

- Python 3.8 o superior.
- Librerías listadas en `requirements.txt`.

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/jorgef17/pokedex-cli.git
   cd pokedex-cli
   ```

2. Crea un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el programa:

   ```bash
   python main.py
   ```

2. Sigue las instrucciones en pantalla para buscar un Pokémon o comparar dos.

## Estructura del Proyecto

```plaintext
pokedex-cli/
├── pokedex.py                # Archivo principal
├── requirements.txt       # Dependencias
├── pokemon_history.json   # Historial de búsquedas (ignorado en Git)
└── README.md              # Documentación
```

## Ejemplo de Uso

### Buscar un Pokémon:

```plaintext
Ingresa el nombre de un Pokémon (o 'salir' para terminar): pikachu

Nombre: Pikachu
Tipos: electric
Habilidades: static, lightning-rod
Peso: 60 hectogramos
Altura: 4 decímetros
Datos de Pikachu guardados en 'pokemon_history.json'.
```

### Comparar dos Pokémon:

```plaintext
Ingresa el nombre del primer Pokémon: pikachu
Ingresa el nombre del segundo Pokémon: bulbasaur

Comparación:
Pikachu - Peso: 60 hectogramos, Altura: 4 decímetros
Bulbasaur - Peso: 69 hectogramos, Altura: 7 decímetros
Más pesado: Bulbasaur
Más alto: Bulbasaur
```

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras un error o tienes una sugerencia, abre un issue o envía un pull request.


## Recursos

- [PokeAPI](https://pokeapi.co/): API utilizada para obtener los datos de los Pokémon.
- [Python](https://www.python.org/): Lenguaje de programación utilizado.
