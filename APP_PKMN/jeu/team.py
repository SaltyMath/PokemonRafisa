from pokemon import Pokemon


class Team:
    def __init__(self, pokemon_names):
        self.pokemons = [Pokemon(name) for name in pokemon_names]

    def has_available_pokemon(self):
        return any(not pokemon.is_ko() for pokemon in self.pokemons)
