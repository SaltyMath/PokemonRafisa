from database import get_pokemon_by_name, get_attacks_for_pokemon, get_type_effectiveness


class Pokemon:
    def __init__(self, name, is_player=True):
        data = get_pokemon_by_name(name, is_player)
        if data:
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
            self.attacks = [Attack(*attack) for attack in get_attacks_for_pokemon(self.id)]
        else:
            raise ValueError(f"Pokemon with name {name} not found in database")

    def is_ko(self):
        return self.current_hp <= 0

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

    def heal(self, amount):
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp


class Attack:
    def __init__(self, id, name, power, accuracy, type_id):
        self.id = id
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.type_id = type_id

    def calculate_damage(self, attacker, defender):
        base_damage = ((2 * attacker.level / 5 + 2) * self.power * attacker.attack / defender.defense / 50) + 2
        effectiveness = get_type_effectiveness(self.type_id, defender.type1_id)
        if defender.type2_id:
            effectiveness *= get_type_effectiveness(self.type_id, defender.type2_id)
        return max(int(base_damage * effectiveness), 0)
