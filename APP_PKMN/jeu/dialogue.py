import pygame

class DialogueBox:
    def __init__(self, screen):
        self.screen = screen
        # Initialisation de la police utilisée pour le texte
        self.font = pygame.font.Font(None, 36)
        # Définition du rectangle représentant la boîte de dialogue
        self.box_rect = pygame.Rect(50, 450, 700, 100)
        # Couleur de fond de la boîte de dialogue
        self.box_color = (255, 255, 255)
        # Couleur du texte et des bordures de la boîte de dialogue
        self.text_color = (0, 0, 0)
        # Texte et nom à afficher dans la boîte de dialogue
        self.dialogue = ""
        self.name = ""

    def set_dialogue(self, text, name=""):
        # Définit le texte et le nom à afficher dans la boîte de dialogue
        self.dialogue = text
        self.name = name
        # Messages de debug
        print(f"{name} : {text}")
        if name:
            print(f"{name} :")

    def draw(self):
        # Dessine la boîte de dialogue sur l'écran
        pygame.draw.rect(self.screen, self.box_color, self.box_rect)
        # Dessine les bordures de la boîte de dialogue
        pygame.draw.rect(self.screen, self.text_color, self.box_rect, 2)

        if self.name:
            # Si un nom est défini, dessine une boîte pour le nom au-dessus de la boîte de dialogue
            name_rect = pygame.Rect(self.box_rect.x, self.box_rect.y - 30, 150, 30)
            pygame.draw.rect(self.screen, self.box_color, name_rect)
            pygame.draw.rect(self.screen, self.text_color, name_rect, 2)
            # Rend le nom et le dessine à l'écran
            name_surface = self.font.render(self.name, True, self.text_color)
            self.screen.blit(name_surface, (self.box_rect.x + 5, self.box_rect.y - 25))

        # Enveloppe le texte de dialogue pour qu'il tienne dans la boîte de dialogue
        lines = self.wrap_text(self.dialogue, self.font, self.box_rect.width - 20)
        for i, line in enumerate(lines):
            # Rend chaque ligne de texte et la dessine dans la boîte de dialogue
            text_surface = self.font.render(line, True, self.text_color)
            self.screen.blit(text_surface, (self.box_rect.x + 10, self.box_rect.y + 10 + i * 30))

    def wrap_text(self, text, font, max_width):
        # Divise le texte en mots
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            # Rend la ligne actuelle de texte
            text_surface = font.render(' '.join(current_line), True, self.text_color)
            # Vérifie si la largeur de la ligne dépasse la largeur maximale
            if text_surface.get_width() > max_width:
                # Si oui, enlève le dernier mot ajouté et ajoute la ligne aux lignes finales
                current_line.pop()
                lines.append(' '.join(current_line))
                # Commence une nouvelle ligne avec le mot en cours
                current_line = [word]

        # Ajoute la dernière ligne
        lines.append(' '.join(current_line))
        return lines
