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
        ("Vaultra", 7, None, 5, 35, 55, 40, 90, 40, 40, 100, 100, 'images_videos/nvll_t_pkmn/Vaultra-f.png'),  # combat
        ("Blatgel", 12, None, 5, 39, 52, 43, 65, 43, 43, 100, 100, 'images_videos/nvll_t_pkmn/Blatgel.png'),  # Insecte
        ("Londose", 8, None, 5, 44, 48, 46, 43, 48, 48, 100, 100, 'images_videos/nvll_t_pkmn/Londose.png'),  # poison
        ("Spectradoc", 14, None, 5, 45, 49, 49, 45, 49, 49, 100, 100, 'images_videos/nvll_t_pkmn/Spectradoc.png'),  # spectre
        ("Dratinja", 16, None, 5, 70, 20, 40, 40, 20, 20, 100, 100, 'images_videos/nvll_t_pkmn/Dratinja.png'),  # Tenebres
        ("Un Sprite", 1, None, 5, 500, 10, 30, 10, 10, 30, 100, 100, 'images_videos/nvll_t_pkmn/ADesign.png'),  # normal
        ("Pikachu", 4, None, 5, 40, 40, 40, 70, 50, 45, 100, 100, 'images_videos/nvll_t_pkmn/25.png'),  # elektrik
        ("Pokipo", 17, None, 5, 50, 30, 35, 20, 30, 35, 100, 100, 'images_videos/nvll_t_pkmn/Pokipo.png'),  # acier
        ("Féepalfou", 18, None, 5, 35, 35, 30, 40, 35, 30, 100, 100, 'images_videos/nvll_t_pkmn/Féepalfou.png'),  # fée
        ("Pivroum", 10, None, 5, 33, 33, 38, 40, 33, 38, 100, 100, 'images_videos/nvll_t_pkmn/Pivroum.png'),  # vol
        ("Feudkan", 2, None, 5, 50, 37, 42, 33, 42, 47, 100, 100, 'images_videos/nvll_t_pkmn/Feudkan.png'),  # feu
        ("Rainglock", 3, None, 5, 23, 27, 35, 42, 46, 49, 100, 100, 'images_videos/nvll_t_pkmn/Rainglock.png'),  # eau
        ("Somegrass", 5, None, 5, 33, 37, 42, 45, 48, 39, 100, 100, 'images_videos/nvll_t_pkmn/Somegrass.png'),  # plante
        ("Gelus", 6, None, 5, 37, 34, 32, 45, 46, 46, 100, 100, 'images_videos/nvll_t_pkmn/Gelus.png'),  # glace
        ("Sofanalyse", 11, None, 5, 35, 42, 31, 32, 38, 44, 100, 100, 'images_videos/nvll_t_pkmn/Sofanalyse.png'),  # psy
        ("Plancher", 9, None, 5, 41, 40, 37, 33, 47, 47, 100, 100, 'images_videos/nvll_t_pkmn/Plancher.png'),  # sol
        ("Alderiate", 13, None, 5, 45, 40, 50, 20, 45, 40, 100, 100, 'images_videos/nvll_t_pkmn/ALDERIATE.png'),  # roche
        ("Lorneax", 15, None, 5, 50, 46, 38, 49, 43, 48, 100, 100, 'images_videos/nvll_t_pkmn/Lorneax.png')  # dragon

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
        ("Dratinja", 16, None, 5, 70, 20, 40, 40, 20, 20, 100, 100, 'images_videos/nvll_t_pkmn/Dratinja_dos.png'),
        ("Un Sprite", 1, None, 5, 500, 10, 30, 10, 10, 30, 100, 100, 'images_videos/nvll_t_pkmn/ADesign_dos.png'),
        ("Pikachu", 4, None, 5, 40, 40, 40, 70, 50, 45, 100, 100, 'images_videos/nvll_t_pkmn/25_dos.png'),
        ("Pokipo", 17, None, 5, 50, 30, 35, 20, 30, 35, 100, 100, 'images_videos/nvll_t_pkmn/Pokipo_dos.png'),
        ("Féepalfou", 18, None, 5, 35, 35, 30, 40, 35, 30, 100, 100, 'images_videos/nvll_t_pkmn/Féepalfou.png'),
        ("Pivroum", 10, None, 5, 33, 33, 38, 40, 33, 38, 100, 100, 'images_videos/nvll_t_pkmn/Pivroum_dos.png'),
        ("Feudkan", 2, None, 5, 50, 37, 42, 33, 42, 47, 100, 100, 'images_videos/nvll_t_pkmn/Feudkan_dos.png'),
        ("Rainglock", 3, None, 5, 23, 27, 35, 42, 46, 49, 100, 100, 'images_videos/nvll_t_pkmn/Rainglock_dos.png'),
        ("Somegrass", 5, None, 5, 33, 37, 42, 45, 48, 39, 100, 100, 'images_videos/nvll_t_pkmn/Somegrass_dos.png'),
        ("Gelus", 6, None, 5, 37, 34, 32, 45, 46, 46, 100, 100, 'images_videos/nvll_t_pkmn/Gelus_dos.png'),
        ("Sofanalyse", 11, None, 5, 35, 42, 31, 32, 38, 44, 100, 100, 'images_videos/nvll_t_pkmn/Sofanalyse_dos.png'),
        ("Plancher", 9, None, 5, 41, 40, 37, 33, 47, 47, 100, 100, 'images_videos/nvll_t_pkmn/Plancher_dos.png'),
        ("Alderiate", 13, None, 5, 45, 40, 50, 20, 45, 40, 100, 100, 'images_videos/nvll_t_pkmn/ALDERIATE_dos.png'),
        ("Lorneax", 15, None, 5, 50, 46, 38, 49, 43, 48, 100, 100, 'images_videos/nvll_t_pkmn/Lorneax_dos.png')

    ]
    cursor.executemany('''
    INSERT INTO PlayerPokemon (name, type1_id, type2_id, level, max_hp, attack, defense, speed, special_attack, special_defense, accuracy, evasion, image_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', player_pokemons)

    # Insertion d'attaques
    attacks = [
        ("Ball'ombre (spectre)", 40, 100, 14),  # 1
        ("Molotov (feu)", 40, 100, 2),  # 2
        ("Lance-dagues (acier)", 40, 100, 17),  # 3
        ("Vampirisme (plante)", 40, 100, 5),  # 4
        ("BONK (combat)", 60, 80, 7),  # 5
        ("Cri de guerre (normal)", 5, 100, 1),  # 6
        ("Drapochoc (dragon)", 100, 50, 15),  # 7
        ("Invasion (insecte)", 40, 85, 12),  # 8
        ("Piqûre (insecte)", 10, 100, 12),  # 9
        ("Vol (vol)", 30, 80, 10),  # 10
        ("Koud'kouto (acier)", 50, 90, 17),  # 11
        ("Kayou (roche)", 5, 80, 13),  # 12
        ("Une attaque eau (eau)", 10, 100, 3),  # 13
        ("Une attaque dragon (dragon)", 10, 100, 15),  # 14
        ("Une attaque spectre (spectre)", 10, 100, 14),  # 15
        ("Une attaque feu (feu)", 10, 100, 2),  # 16
        ("Éclair (élektrik)", 30, 90, 4),  # 17
        ("Queue de fer (acier)", 20, 100, 17),  # 18
        ("Aéropique (vol)", 25, 80, 10),  # 19
        ("Coup d'aile (vol)", 30, 100, 10),  # 20
        ("Embrasement (feu)", 30, 100, 2),  # 21
        ("Lance-flammes (feu)", 25, 80, 2),  # 22
        ("Ball'eau (eau)", 20, 100, 3),  # 23
        ("Tacle herbeux (plante)", 40, 70, 5),  # 24
        ("Lance-soleil (plante)", 35, 50, 5),  # 25
        ("Neige (glace)", 5, 100, 6),  # 26
        ("Grêle (glace)", 30, 100, 6),  # 27
        ("Boule de neige (glace)", 20, 50, 6),  # 28
        ("Vent d'hiver (glace)", 10, 100, 6),  # 29
        ("Cauchemar (psy)", 20, 80, 11),  # 30
        ("Psychanalyse (psy)", 20, 100, 11),  # 31
        ("Facture (vol)", 40, 100, 10),  # 32
        ("Meme (normal)", 20, 80, 1),  # 33
        ("Rage (roche)", 30, 90, 13),
        ("Planche moisie (sol)", 20, 80, 9),
        ("Sol glissant (sol)", 40, 50, 9),
        ("Marche invisible (sol)", 10, 100, 9),
        ("Détritus piquants (poison)", 15, 100, 8)
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
        (5, 12),
        (6, 13),
        (6, 14),
        (6, 15),
        (6, 16),
        (7, 17),
        (7, 18),
        (7, 6),
        (7, 12),
        (8, 18),
        (8, 5),
        (8, 2),
        (8, 6),
        (9, 4),
        (9, 9),
        (9, 10),
        (9, 12),
        (10, 10),
        (10, 5),
        (10, 19),
        (10, 20),
        (11, 2),
        (11, 21),
        (11, 22),
        (11, 6),
        (12, 1),
        (12, 3),
        (12, 6),
        (12, 23),
        (13, 8),
        (13, 9),
        (13, 24),
        (13, 25),
        (14, 26),
        (14, 27),
        (14, 28),
        (14, 29),
        (15, 6),
        (15, 30),
        (15, 31),
        (15, 32),
        (16, 35),
        (16, 36),
        (16, 37),
        (16, 38),
        (17, 12),
        (17, 18),
        (17, 33),
        (17, 34),
        (18, 22),
        (18, 7),
        (18, 21),
        (18, 17)
    ]
    cursor.executemany('''
    INSERT INTO PokemonAttacks (pokemon_id, attack_id)
    VALUES (?, ?)
    ''', pokemon_attacks)

    conn.commit()
    conn.close()


def reset_database():
    # Supprime le fichier de base de données s'il existe
    if os.path.exists('pokemon.db'):
        os.remove('pokemon.db')

    # Recrée les tables et insére les données
    create_tables()
    insert_data()


if __name__ == "__main__":
    reset_database()
