import sqlite3
import os


def create_tables():
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    # Table des types
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Types (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')

    # Table des relations de type
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TypeRelations (
        attack_type_id INTEGER,
        target_type_id INTEGER,
        effectiveness REAL,
        PRIMARY KEY (attack_type_id, target_type_id),
        FOREIGN KEY (attack_type_id) REFERENCES Types(id),
        FOREIGN KEY (target_type_id) REFERENCES Types(id)
    )
    ''')

    # Table des Pokémon pour les dresseurs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TrainerPokemon (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type1_id INTEGER NOT NULL,
        type2_id INTEGER,
        level INTEGER NOT NULL,
        max_hp INTEGER NOT NULL,
        attack INTEGER NOT NULL,
        defense INTEGER NOT NULL,
        speed INTEGER NOT NULL,
        special_attack INTEGER NOT NULL,
        special_defense INTEGER NOT NULL,
        accuracy INTEGER NOT NULL,
        evasion INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        FOREIGN KEY (type1_id) REFERENCES Types(id),
        FOREIGN KEY (type2_id) REFERENCES Types(id)
    )
    ''')

    # Table des Pokémon pour le joueur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PlayerPokemon (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type1_id INTEGER NOT NULL,
        type2_id INTEGER,
        level INTEGER NOT NULL,
        max_hp INTEGER NOT NULL,
        attack INTEGER NOT NULL,
        defense INTEGER NOT NULL,
        speed INTEGER NOT NULL,
        special_attack INTEGER NOT NULL,
        special_defense INTEGER NOT NULL,
        accuracy INTEGER NOT NULL,
        evasion INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        FOREIGN KEY (type1_id) REFERENCES Types(id),
        FOREIGN KEY (type2_id) REFERENCES Types(id)
    )
    ''')

    # Table des attaques
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Attacks (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        power INTEGER NOT NULL,
        accuracy INTEGER NOT NULL,
        type_id INTEGER NOT NULL,
        FOREIGN KEY (type_id) REFERENCES Types(id)
    )
    ''')

    # Table des attaques données aux Pokémon
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PokemonAttacks (
        pokemon_id INTEGER,
        attack_id INTEGER,
        PRIMARY KEY (pokemon_id, attack_id),
        FOREIGN KEY (pokemon_id) REFERENCES TrainerPokemon(id),
        FOREIGN KEY (pokemon_id) REFERENCES PlayerPokemon(id),
        FOREIGN KEY (attack_id) REFERENCES Attacks(id)
    )
    ''')

    conn.commit()
    conn.close()


def insert_data():
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    # Insertion de types
    types = [
        ("Normal",), ("Feu",), ("Eau",), ("Électrik",), ("Plante",), ("Glace",),
        ("Combat",), ("Poison",), ("Sol",), ("Vol",), ("Psy",), ("Insecte",),
        ("Roche",), ("Spectre",), ("Dragon",), ("Ténèbres",), ("Acier",), ("Fée",)
    ]
    cursor.executemany('INSERT INTO Types (name) VALUES (?)', types)

    # Insertion de relations de type
    type_relations = [
        # normal
        (1, 17, 0.5),
        (1, 13, 0.5),
        (1, 14, 0.0),
        # feu
        (2, 5, 2.0),
        (2, 6, 2.0),
        (2, 17, 2.0),
        (2, 12, 2.0),
        (2, 15, 0.5),
        (2, 2, 0.5),
        (2, 13, 0.5),
        (2, 3, 0.5),
        # eau
        (3, 2, 2.0),
        (3, 13, 2.0),
        (3, 9, 2.0),
        (3, 15, 0.5),
        (3, 3, 0.5),
        (3, 5, 0.5),
        # Électrik
        (4, 3, 2.0),
        (4, 10, 2.0),
        (4, 15, 0.5),
        (4, 4, 0.5),
        (4, 5, 0.5),
        (4, 9, 0.0),
        # Plante
        (5, 2, 0.5),
        (5, 15, 0.5),
        (5, 12, 0.5),
        (5, 10, 0.5),
        (5, 5, 0.5),
        (5, 8, 0.5),
        (5, 3, 2.0),
        (5, 9, 2.0),
        (5, 13, 2.0),
        # Glace
        (6, 15, 2.0),
        (6, 5, 2.0),
        (6, 9, 2.0),
        (6, 10, 2.0),
        (6, 17, 0.5),
        (6, 3, 0.5),
        (6, 6, 0.5),
        (6, 2, 0.5),
        # Combat
        (7, 17, 2.0),
        (7, 6, 2.0),
        (7, 1, 2.0),
        (7, 13, 2.0),
        (7, 16, 2.0),
        (7, 18, 0.5),
        (7, 12, 0.5),
        (7, 9, 0.5),
        (7, 8, 0.5),
        (7, 11, 0.5),
        (7, 10, 0.0),
        # POISON
        (8, 18, 2.0),
        (8, 5, 2.0),
        (8, 8, 0.5),
        (8, 13, 0.5),
        (8, 9, 0.5),
        (8, 14, 0.5),
        (8, 17, 0.0),
        # sol
        (9, 4, 2.0),
        (9, 2, 2.0),
        (9, 8, 2.0),
        (9, 13, 2.0),
        (9, 12, 0.5),
        (9, 5, 0.5),
        (9, 10, 0.0),
        # vol
        (10, 7, 2.0),
        (10, 12, 2.0),
        (10, 5, 2.0),
        (10, 17, 0.5),
        (10, 4, 0.5),
        (10, 13, 0.5),
        # psy
        (11, 7, 2.0),
        (11, 8, 2.0),
        (11, 17, 0.5),
        (11, 11, 0.5),
        (11, 16, 0.0),
        # insecte
        (12, 5, 2.0),
        (12, 11, 2.0),
        (12, 16, 2.0),
        (12, 17, 0.5),
        (12, 7, 0.5),
        (12, 18, 0.5),
        (12, 2, 0.5),
        (12, 8, 0.5),
        (12, 14, 0.5),
        (12, 10, 0.5),
        # roche
        (13, 2, 2.0),
        (13, 6, 2.0),
        (13, 12, 2.0),
        (13, 10, 2.0),
        (13, 17, 0.5),
        (13, 7, 0.5),
        (13, 9, 0.5),
        # spectre
        (14, 11, 2.0),
        (14, 14, 2.0),
        (14, 16, 0.5),
        (14, 1, 0.0),
        # dragon
        (15, 15, 2.0),
        (15, 17, 0.5),
        (15, 18, 0.0),
        # ténèbres
        (16, 11, 2.0),
        (16, 14, 2.0),
        (16, 7, 0.5),
        (16, 18, 0.5),
        (16, 16, 0.5),
        # acier
        (17, 18, 2.0),
        (17, 6, 2.0),
        (17, 13, 2.0),
        (17, 17, 0.5),
        (17, 3, 0.5),
        (17, 4, 0.5),
        (17, 2, 0.5),
        # fée
        (18, 7, 2.0),
        (18, 15, 2.0),
        (18, 16, 2.0),
        (18, 17, 0.5),
        (18, 2, 0.5),
        (18, 8, 0.5),
    ]
    cursor.executemany('INSERT INTO TypeRelations (attack_type_id, target_type_id, effectiveness) VALUES (?, ?, ?)',
                       type_relations)

    # Insertion de Pokémon à donner aux dresseurs
    trainer_pokemons = [
        ("Vaultra", 7, None, 5, 35, 55, 40, 90, 40, 40, 100, 100, 'images_videos/nvll_t_pkmn/Vaultra-f.png'),
        ("Blatgel", 12, None, 5, 39, 52, 43, 65, 43, 43, 100, 100, 'images_videos/nvll_t_pkmn/Blatgel.png'),
        ("Londose", 1, None, 5, 44, 48, 46, 43, 48, 48, 100, 100, 'images_videos/nvll_t_pkmn/Londose.png'),
        ("Spectradoc", 14, None, 5, 45, 49, 49, 45, 49, 49, 100, 100, 'images_videos/nvll_t_pkmn/Spectradoc.png'),
        ("Dratinja", 16, None, 5, 70, 20, 40, 40, 20, 20, 100, 100, 'images_videos/nvll_t_pkmn/Dratinja.png')
    ]
    cursor.executemany('''
    INSERT INTO TrainerPokemon (name, type1_id, type2_id, level, max_hp, attack, defense, speed, special_attack, special_defense, accuracy, evasion, image_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', trainer_pokemons)

    # Insertion de Pokémon à donner au joueur (C'est les mêmes mais avec un sprite de dos)
    player_pokemons = [
        ("Vaultra", 7, None, 5, 35, 55, 40, 90, 40, 40, 100, 100, 'images_videos/nvll_t_pkmn/Vaultra-d.png'),
        ("Blatgel", 12, None, 5, 39, 52, 43, 65, 43, 43, 100, 100, 'images_videos/nvll_t_pkmn/Blatgel_dos.png'),
        ("Londose", 1, None, 5, 44, 48, 46, 43, 48, 48, 100, 100, 'images_videos/nvll_t_pkmn/Londose_dos.png'),
        ("Spectradoc", 14, None, 5, 45, 49, 49, 45, 49, 49, 100, 100, 'images_videos/nvll_t_pkmn/Spectradoc_dos.png'),
        ("Dratinja", 16, None, 5, 70, 20, 40, 40, 20, 20, 100, 100, 'images_videos/nvll_t_pkmn/Dratinja_dos.png')
    ]
    cursor.executemany('''
    INSERT INTO PlayerPokemon (name, type1_id, type2_id, level, max_hp, attack, defense, speed, special_attack, special_defense, accuracy, evasion, image_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', player_pokemons)

    # Insertion d'attaques
    attacks = [
        ("Ball'ombre", 40, 100, 14),
        ("Molotov", 40, 100, 2),
        ("Lance-dagues", 40, 100, 17),
        ("Vampirisme", 40, 100, 5),
        ("BONK", 60, 80, 7),
        ("Cri de guerre", 5, 100, 1),
        ("Drapochoc", 100, 50, 15),
        ("Invasion", 40, 85, 12),
        ("Piqûre", 10, 100, 12),
        ("Vol", 30, 80, 10),
        ("Koud'kouto", 50, 90, 17),
        ("Kayou", 5, 80, 13)
    ]
    cursor.executemany('''
    INSERT INTO Attacks (name, power, accuracy, type_id)
    VALUES (?, ?, ?, ?)
    ''', attacks)

    # Insertion de relations Pokémon-Attaques
    pokemon_attacks = [
        (1, 2),
        (1, 5),
        (1, 6),
        (1, 7),
        (2, 4),
        (2, 8),
        (2, 9),
        (2, 10),
        (3, 2),
        (3, 3),
        (3, 6),
        (3, 11),
        (4, 1),
        (4, 4),
        (4, 6),
        (4, 10),
        (5, 3),
        (5, 5),
        (5, 11),
        (5, 12)
    ]
    cursor.executemany('''
    INSERT INTO PokemonAttacks (pokemon_id, attack_id)
    VALUES (?, ?)
    ''', pokemon_attacks)

    conn.commit()
    conn.close()


def reset_database():
    # Supprimer le fichier de base de données s'il existe
    if os.path.exists('pokemon.db'):
        os.remove('pokemon.db')

    # Recréer les tables et insérer les données
    create_tables()
    insert_data()


if __name__ == "__main__":
    reset_database()
