import pygame
from database import get_pokemon_by_name, get_attacks_for_pokemon
from pokemon import Pokemon


class Trainer(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, name, dialogue, defeated_dialogue, post_defeat_dialogue, map_name, pokemon_names):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.name = name
        self.dialogue = dialogue  # Dialogue pré défaite
        self.defeated_dialogue = defeated_dialogue  # Dialogue post défaite
        self.post_defeat_dialogue = post_defeat_dialogue  # Nouveau dialogue après la défaite de Trainer11
        self.map_name = map_name
        self.pokemon_team = self.create_pokemon_team(pokemon_names)
        self.defeated = False
        self.post_defeat_condition_met = False  # Condition pour débloquer le troisième dialogue

    def talk(self, post_defeat=False):
        if self.post_defeat_condition_met:
            return self.post_defeat_dialogue
        elif post_defeat and isinstance(self, (Trainer1, Trainer2, Trainer3, Trainer4, Trainer5, Trainer6, Trainer7, Trainer8, Trainer9, Trainer10, Trainer11, Trainer12, Trainer13)):
            return self.post_defeat_dialogue
        elif self.defeated:
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
        pokemon_names = ["Spectradoc", "Sofanalyse"]
        super().__init__(x, y, 'images_videos/blaine.png', "Miguel",
                         "Au secours on m'a implanté dans un arbre, que quelqu'un licencie le Game Designer pitié!",
                         "Tu as fais ça?? Ce sera noté sur ton rapport...",
                         "En vrai cet arbre est pas si inconfortable que ça...", map_name, pokemon_names)


class Trainer2(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/triathletecyclistm.png', "Jérôme",
                         "Eh t'as oublié de m'AirDrop ta Pokéball!",
                         "Ah, apparemment j'ai oublié de m'AirDrop la victoire...",
                         "Merci pour notre combat.", map_name, pokemon_names)


class Trainer3(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Vaultra"]
        super().__init__(x, y, 'images_videos/collector.png', "Nathan", "Copyright © 2024 <copyright holders>"
                         "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:"
                         "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."
                         "THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.",
                         "Check it out ! 127.0.0.1",
                         "[dialogue.txt]", map_name, pokemon_names)


class Trainer4(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Gelus"]
        super().__init__(x, y, 'images_videos/erika.png', "Kamilla", "Appuie sur E pour nous reparler après un combat, on aura peut-être des conseils vu que le dev a eu la flemme de mettre des indices sur l'histoire sur la carte.",
                         "N'oublie pas d'appuyer sur E devant certains objets! Maintenant, va parler à Tania à l'intérieur.",
                         "(Écoute de la musique)", map_name, pokemon_names)


class Trainer5(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/biker.png', "Cédric",
                         "Je veux savoir qui a eu l'idée géniale de me donner ce sprite alors qu'on est dans des"
                         " locaux situés au premier étage... Oh c'est toi? Alors en garde!!", "T'es viré.",
                         "Merci pour le stagiaire. Le bus pour l'EPSIC part bientôt, tu devrais te dépêcher de le prendre !!", map_name, pokemon_names)


class Trainer6(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Pivroum"]
        super().__init__(x, y, 'images_videos/brock.png', "Karim", "Je comprends pas pourquoi les sprites de Baldy ont été retirés de la version finale... ils étaient trop drôles.", "Tu peux passer derrière les caisses à l'entrée pour accéder à l'open space.",
                         "Et du coup pour Baldy ??", map_name, pokemon_names)


class Trainer7(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Féepalfou", "Rainglock"]
        super().__init__(x, y, 'images_videos/triathleterunnerf.png', "Mario",
                         "Bonjour [Dresseur], je suis un prince ruiné de/du [insérer pays] et j'ai besoin de tes"
                         " coordonnées bancaires pour pouvoir prendre l'avion et récupérer mes "
                         "richesses! ", "EUh... ma demande tiens toujours alors dans le doute, envoie moi ça sur ce site pas suspect du tout stp : http://pas_une_arnaque.virus",
                         "Tu sais où est Miguel ?", map_name, pokemon_names)


class Trainer8(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Vaultra", "Londose", "Spectradoc", "Alderiate"]
        super().__init__(x, y, 'images_videos/swimmerm.png', "Guillaume",
                         "Je ne te céderais jamais mes jantes OZ gold 18 pouces de ma Subaru Impreza WRX 2007 "
                         "2.5T (169KW quand même)", "C'est sad en vrai...",
                         "Petite pause clope et je m'y remet.", map_name, pokemon_names)


class Trainer9(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Londose", "Vaultra"]
        super().__init__(x, y, 'images_videos/greta.png', "Tania",
                         "Le stagiaire a pété les plombs et s'est enfermé dans mon bureau ! Il veut combattre le plus fort d'entre nous alors on a pas vraiment le choix, À L'ASSAUT !!", "J'ai perdu mon bureau et le combat, sale journée.",
                         "Merci d'avoir récupéré mon bureau, ça fait du bien d'être de retour.", map_name, pokemon_names)


class Trainer10(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Londose"]
        super().__init__(x, y, 'images_videos/richboy.png', "Dylan",
                         "Dépêchons-nous, il faut absolument que je me prépare à manger, ça fera du bien à mes Pokémon.", "J'irai bien manger mais je ne peux pas bouger de cet endroit parce que le dev à pas codé de déplacements...",
                         "Bon appétit !!", map_name, pokemon_names)


class Trainer11(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Feudkan", "Lorneax", "Vaultra"]
        super().__init__(x, y, 'images_videos/supernerd.png', "Stagiaire",
                         "Tu n'arrêteras pas ma révolution! Alors c'est parti pour le combat!", "OK! J'abandonne... tu peux aller dire à Cédric que je me rends...",
                         "OK! J'abandonne... tu peux aller dire à Cédric que je me rends...", map_name, pokemon_names)


class Trainer12(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Blatgel", "Blatgel", "Blatgel"]
        super().__init__(x, y, 'images_videos/ninjaboy.png', "Angel", "Fais gaffe, mon pseudo sur Splatoon c'est android 10 !", "The",
                         "Nvidia Quadro K2000 c'est un super nom d'équipe, tu trouves pas?", map_name, pokemon_names)


class Trainer13(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Plancher", "Gelus"]
        super().__init__(x, y, 'images_videos/aquagruntm.png', "Zhi", "C'est l'heure de la bagarre !!", "J'ai perdu la bagarre...",
                         "J'attends Guillaume pour qu'il m'aide avec mon CSS.", map_name, pokemon_names)


class Eleve1(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Pokipo", "Somegrass"]
        super().__init__(x, y, 'images_videos/worker.png', "Ahmed", "Je peux copier sur toi ?", "L'infirmière est à l'étage mais Mr. Mocca bloque le passage, mange un truc avant d'y aller !",
                         "Tu pense que j'aurais pu demander de l'aide à ChatGPT pour gagner notre combat ?", map_name, pokemon_names)


class Eleve2(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Pivroum", "Vaultra"]
        super().__init__(x, y, 'images_videos/skinhead.png', "Tomy", "J'étais carrossier autrefois...",
                         "...et puis j'ai pris un sacré mal de dos.",
                         "Bon il est où Mocca ?!", map_name,
                         pokemon_names)


class Eleve3(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Plancher", "Pokipo"]
        super().__init__(x, y, 'images_videos/sailor.png', "Kira", "Tu veux de la crypto?",
                         "J'ai un projet NFT à te montrer, il est dans un de mes 148 onglets Google.",
                         "Mon PC est hyper lent, je sais pas pourquoi...", map_name,
                         pokemon_names)


class Eleve4(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Londose", "Féepalfou"]
        super().__init__(x, y, 'images_videos/archie.png', "Elmo", "Viens te battre.",
                         "Je m'ennuie...",
                         "ZZz...", map_name,
                         pokemon_names)


class Eleve5(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Somegrass", "Somegrass"]
        super().__init__(x, y, 'images_videos/matt.png', "Dave", "Regarde j'ai fais un script qui dessine la lettre G avec la lettre G.",
                         "Faut que je me remette à l'apprentissage de ce langage hyper sombre là... j'ai plus le nom.",
                         "J'ai demandé 13 fois à Mr. Mocca si je pouvais faire l'exact opposé de ce qu'il a demandé et il m'a dit d'aller me faire cuire un oeuf, j'ai pas compris.", map_name,
                         pokemon_names)


class Eleve6(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Gelus", "Plancher"]
        super().__init__(x, y, 'images_videos/officelady.png', "Laura", "Les trajets en train c'est fatigant, je vais me détendre avec un combat",
                         "C'est vraiment la galère ces trains...",
                         "Je pensais faire une sieste pendant le cours de math mais le cours est super intéressant.", map_name,
                         pokemon_names)


class Eleve7(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Feudkan", "Rainglock"]
        super().__init__(x, y, 'images_videos/aquagruntmbeta.png', "Dario", "Tu peux m'aider pour la base de données ?",
                         "Tu peux m'aider pour la base de données ?",
                         "Tu peux m'aider pour la base de données ?", map_name,
                         pokemon_names)


class Eleve8(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Plancher", "Pokipo"]
        super().__init__(x, y, 'images_videos/businessman2.png', "Maurice", "J'ai un des examens qu'un pote à fait l'année passée, tu veux?",
                         "J'te le fais à 30 balles, c'est donné !",
                         "Oublie le paiement, j'avais oublié qu'on était dans le même groupe.", map_name,
                         pokemon_names)


class Eleve9(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Vaultra"]
        super().__init__(x, y, 'images_videos/palmer2.png', "Gary", "Un combat, super......",
                         "J'ai perdu.... super......",
                         "Je joue à Clash Royale là, viens plus tard", map_name,
                         pokemon_names)


class Eleve10(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Spectradoc"]
        super().__init__(x, y, 'images_videos/daycarestudentm.png', "Michel", "EH EH EH J'EXISTE REGARDEZ HAHAHAHAHAH!!!!!!!!!!!!!",
                         "EH EH EH REGARDEZ JE SUIS INTÉRESSANT JE FAIS N'IMPORTE QUOI!!!!!!!!",
                         "Mon patron vient de me virer.", map_name,
                         pokemon_names)


class Prof1(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Rainglock", "Feudkan", "Alderiate"]
        super().__init__(x, y, 'images_videos/gentleman.png', "O. Mocca", "Je suis Oliver Mocca et vous? Comment ça vous avez un deuxième prénom ? Vous allez payer au nom des bases de données !!", "Vous m'avez mis une belle raclée... Bon je devrais peut-être retourner vers mes élèves ça va bientôt faire 30 minutes que je fais une courte pause de 2 minutes.",
                         "Vous devriez aller parler au Doyen, ou faire une pause café avec moi ça me va aussi.", map_name, pokemon_names)


class Prof2(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Un Sprite"]
        super().__init__(x, y, 'images_videos/gentleman.png', "O. Mocca", "Vous avez vaincu le Doyen... dans ce cas je serais votre dernier challenge ! FINISSONS-EN!!", "Bravo, me voilà vaincu... votre aventure s'arrête ici. Enfin elle le sera quand vous sortirez du bâtiment. Merci d'avoir joué!",
                         "Votre victoire face à moi est ce qui conclu votre aventure, bravo à vous. ", map_name, pokemon_names)


class Prof3(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Blatgel", "Pokipo"]
        super().__init__(x, y, 'images_videos/hiker.png', "Mr. Lagoon", "Bienvenue à l'École Pokémon de Stratégie Innovante et de Combats (EPSIC)! Vous voulez une démo ?", "Pas mal, je suppose que vous savez déjà quoi faire, vous balader -> battre tout le monde au passage -> refuser d'élaborer -> partir.",
                         "Le théorème de Pythagore c'est : Si la somme des carrés des deux petits côtés d'un triangle est égale à celui de l'hypothénuse, ce triangle est rectangle.", map_name, pokemon_names)


class Prof4(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Dratinja", "Dratinja"]
        super().__init__(x, y,'images_videos/wallace.png', "Mr. Can't", "T'es un yes life ou un no life toi ?", "Je taggerais ta victoire sur un mur !",
                         "Trouvez la page du code civil où se situe l'article qui parle de succession avec plusieurs héritiers.", map_name, pokemon_names)


class Prof5(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Féepalfou"]
        super().__init__(x, y, 'images_videos/hexmaniac.png', "Mme. Egg", "Open your book on page : 'I will destroy your team' please", "Bon au moins j'aurais essayé...",
                         "Repeat after me : Dragon type is weak against ice, fairy and... dragon.", map_name, pokemon_names)


class Prof6(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Vaultra", "Blatgel","Blatgel"]
        super().__init__(x, y, 'images_videos/cyclistm.png', "Mr. Pleinlac",
                         "Vous avez vu mes Crocs? Elles sont belles hein?",
                         "Vive les Crocs !",
                         "Un élève m'a rendu un script de roulette russe qui delete System32 si je perds, ingénieux... ", map_name,
                         pokemon_names)


class Prof7(Trainer):
    def __init__(self, x, y, map_name):
        pokemon_names = ["Spectradoc", "Sofanalyse"]
        super().__init__(x, y, 'images_videos/wattson.png', "Mr. Bubulle",
                         "Je fais l'appel via ma liste des futurs perdants. Oh on dirait que vous y êtes.",
                         "Pourtant j'étais pas sur la liste...",
                         "Attention à vos mots de passe, mettre 1234 c'est vraiment une mauvaise idée.",
                         map_name,
                         pokemon_names)


class Doyen(Trainer):
    def __init__(self, x, y, map_name, game_instance):
        pokemon_names = ["Pikachu", "Pikachu", "Pikachu", "Gelus"]
        super().__init__(x, y, 'images_videos/gentleman2.png', "Doyen",
                         "Je suis le Doyen je suis trop puissant pour être vaincu! En garde!",
                         "Bien joué. Mais ce n'est pas fini! Je vois un dernier challenger qui vous empêchera de sortir d'ici victorieux! Soignez-vous avant tout de même.",
                         "Sortez du bâtiment pour mettre fin à votre aventure, vous avez bien mérité votre victoire et du repos.",
                         map_name, pokemon_names)
        self.game_instance = game_instance

    def talk(self, post_defeat=False):
        if self.post_defeat_condition_met and self.game_instance.trainers_defeated[Prof2]:
            return self.post_defeat_dialogue
        elif self.defeated:
            return self.defeated_dialogue
        else:
            return self.dialogue
