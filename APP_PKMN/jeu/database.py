import sqlite3

# Là où sont récupérées les données
def get_pokemon_by_name(name, is_player=True):
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    table = 'PlayerPokemon' if is_player else 'TrainerPokemon'
    cursor.execute(f'''
        SELECT id, name, type1_id, type2_id, level, max_hp, attack, defense, speed, special_attack, special_defense, accuracy, evasion, image_path
        FROM {table} 
        WHERE name=?
    ''', (name,))
    result = cursor.fetchone()

    conn.close()
    return result


def get_attacks_for_pokemon(pokemon_id):
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT a.id, a.name, a.power, a.accuracy, a.type_id
    FROM Attacks a
    JOIN PokemonAttacks pa ON a.id = pa.attack_id
    WHERE pa.pokemon_id=?
    ''', (pokemon_id,))

    result = cursor.fetchall()

    conn.close()
    return result


def get_type_effectiveness(attack_type_id, target_type_id):
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    cursor.execute('SELECT effectiveness FROM TypeRelations WHERE attack_type_id=? AND target_type_id=?',
                   (attack_type_id, target_type_id))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else 1.0
