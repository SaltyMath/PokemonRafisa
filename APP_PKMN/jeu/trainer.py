import pygame
from database import get_pokemon_by_name, get_attacks_for_pokemon
from pokemon import Pokemon

class Trainer(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, name, dialogue, defeated_dialogue, map_name, pokemon_names):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.name = name
        self.dialogue = dialogue
        self.defeated_dialogue = defeated_dialogue
        self.map_name = map_name
        self.pokemon_team = self.create_pokemon_team(pokemon_names)
        self.defeated = False

    def talk(self):
        if self.defeated:
            return self.defeated_dialogue
        else:
            return self.dialogue

    def create_pokemon_team(self, pokemon_names):
        return [Pokemon(name, is_player=False) for name in pokemon_names]

    def is_defeated(self):
        return self.defeated

    def set_defeated(self):
        self.defeated = True


class Trainer1(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/blaine.png', "Miguel",
                         "Au secours on m'a implanté dans un arbre, que quelqu'un licencie le Game Designer pitié!",
                         "Tu as fais ça?? Ce sera noté sur ton rapport...", map_name, pokemon_names)


class Trainer2(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/triathletecyclistm.png', "Jérôme",
                         "Eh t'as oublié de m'AirDrop ta Pokéball!",
                         "Ah, apparemment j'ai oublié de m'AirDrop la victoire...", map_name, pokemon_names)


class Trainer3(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/collector.png', "Nathan", "Copyright © 2024 <copyright holders>"

"Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:"

"The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."

"THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.",
                         "Check it out ! 127.0.0.1", map_name, pokemon_names)


class Trainer4(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/erika.png', "Kamilla", "Appuie sur E pour nous reparler après un combat, on aura peut-être des conseils vu que le dev a eu la flemme de mettre des indices sur quoi faire dans ce jeu", "Oui je brise le quatrième mur, et alors?! N'oublie pas d'appuyer sur E devant certains objets! Maintenant, va parler à Tania à l'intérieur.", map_name, pokemon_names)


class Trainer5(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/biker.png', "Cédric",
                         "Je veux savoir qui a eu l'idée géniale de me donner ce sprite alors qu'on est dans des"
                         " locaux situés au premier étage... Oh c'est toi? Alors en garde!!", "T'es viré.", map_name, pokemon_names)


class Trainer6(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/brock.png', "Karim", "Amogus!", "Je comprends pas pourquoi les sprites de Baldy ont été retirés de la version finale... ils étaient trop drôles.", map_name, pokemon_names)


class Trainer7(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/triathleterunnerf.png', "Mario",
                         "Bonjour [Dresseur], je suis un prince ruiné de/du [insérer pays] et j'ai besoin de tes"
                         " coordonnées bancaires pour pouvoir prendre l'avion et récupérer mes "
                         "richesses! ", "EUh... ma demande tiens toujours alors dans le doute, envoie moi ça sur ce site pas suspect du tout stp : http://pas_une_arnaque.virus", map_name, pokemon_names)


class Trainer8(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Vaultra", "Londose", "Spectradoc", "Vaultra"]
        super().__init__(x, y, 'images_videos/swimmerm.png', "Guillaume",
                         "Je ne te céderais jamais mes jantes OZ gold 18 pouces de ma Subaru Impreza WRX 2007 "
                         "2.5T (169KW quand même)", "C'est sad en vrai...", map_name, pokemon_names)


class Trainer9(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/greta.png', "Tania",
                         "Le stagiaire a pété les plombs et s'est enfermé dans mon bureau ! Il veut combattre le plus fort d'entre nous alors on a pas vraiment le choix, À L'ASSAUT !!", "J'ai perdu mon bureau et le combat, sale journée.", map_name, pokemon_names)


class Trainer10(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/richboy.png', "Dylan",
                         "Dépêchons-nous, il faut absolument que je me prépare à manger, ça fera du bien à mes Pokémon.", "J'irai bien manger mais je ne peux pas bouger de cet endroit parce que le dev à pas instauré de déplacements...", map_name, pokemon_names)


class Trainer11(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/wattson.png', "Stagiaire",
                         "Tu n'arrêteras pas ma révolution! Alors c'est parti pour le combat!", "Oh oh... je crois que je vais me faire virer. À plus dans LE BUS!", map_name, pokemon_names)


class Trainer12(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Blatgel", "Blatgel", "Blatgel"]
        super().__init__(x, y, 'images_videos/ninjaboy.png', "Angel", "Fais gaffe, mon pseudo sur Splatoon c'est android 10 !", "The", map_name, pokemon_names)


class Trainer13(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/aquagruntm.png', "Zhi", "C'est l'heure de la bagarre !!", "J'ai perdu la bagarre...", map_name, pokemon_names)
