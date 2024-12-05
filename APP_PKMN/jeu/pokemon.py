from database import get_pokemon_by_name, get_attacks_for_pokemon, get_type_effectiveness


class Pokemon:
    def __init__(self, name, is_player=True):
        # Récupère les données du Pokémon à partir de la base de données
        data = get_pokemon_by_name(name, is_player)
        if data:
            # Initialisation des attributs du Pokémon
            self.id = data[0]
            self.name = data[1]
            self.type1_id = data[2]
            self.type2_id = data[3]
            self.level = data[4]
            self.max_hp = data[5]
            self.current_hp = self.max_hp
            self.attack = data[6]
            self.defense = data[7]
            self.speed = data[8]
            self.special_attack = data[9]
            self.special_defense = data[10]
            self.accuracy = data[11]
            self.evasion = data[12]
            self.image_path = data[13]
            # Récupère les attaques du Pokémon et les initialise en tant qu'objets Attack
            self.attacks = [Attack(*attack) for attack in get_attacks_for_pokemon(self.id)]
        else:
            raise ValueError(f"Le Pokémon {name} n'est pas dans la base de données")

    def is_ko(self):
        # Vérifie si le Pokémon est KO (points de vie à zéro ou moins)
        return self.current_hp <= 0

    def take_damage(self, damage):
        # Réduit les points de vie actuels du Pokémon en fonction des dégâts reçus
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0  # Les points de vie ne peuvent pas être inférieurs à zéro

    def heal(self, amount):
        # Augmente les points de vie actuels du Pokémon en fonction de la quantité de soin reçue
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp  # Les points de vie ne peuvent pas dépasser le maximum


class Attack:
    def __init__(self, id, name, power, accuracy, type_id):
        # Initialisation des attributs de l'attaque
        self.id = id
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.type_id = type_id

    def calculate_damage(self, attacker, defender):
        # Calcule les dégâts de base de l'attaque
        base_damage = ((2 * attacker.level / 5 + 2) * self.power * attacker.attack / defender.defense / 50) + 2
        # Calcule l'efficacité du type de l'attaque contre les types du défenseur
        effectiveness = get_type_effectiveness(self.type_id, defender.type1_id)
        if defender.type2_id:
            effectiveness *= get_type_effectiveness(self.type_id, defender.type2_id)
        # Retourne les dégâts finaux, arrondis à l'entier inférieur, avec un minimum de 0
        return max(int(base_damage * effectiveness), 0)
