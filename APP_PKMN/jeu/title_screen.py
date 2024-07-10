import pygame
import os

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.start_game = False
        self.show_help = False

        # Chemin d'accès à l'image
        current_path = os.path.dirname(__file__)  # Chemin d'accès du dossier actuel
        image_path = os.path.join(current_path, 'images_videos', 'titre.png')

        # Charger l'image de fond
        self.background = pygame.image.load(image_path).convert()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.start_game = True
        if keys[pygame.K_h]:
            self.show_help = not self.show_help  # Afficher ou masquer l'écran d'aide

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if self.show_help:
            self.draw_help()
        else:
            self.draw_title()

    def draw_title(self):
        # Rendu du texte principal
        start_text = self.font_large.render('Appuyez sur Entrée', True, (0, 0, 0))

        # Calcul pour centrer le texte
        text_rect = start_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 100))

        # Créer un rectangle derrière le texte
        rect_padding = 10
        background_rect = pygame.Rect(
            text_rect.left - rect_padding,
            text_rect.top - rect_padding,
            text_rect.width + 2 * rect_padding,
            text_rect.height + 2 * rect_padding
        )

        pygame.draw.rect(self.screen, (255, 255, 255), background_rect)

        # Dessiner le texte à l'écran
        self.screen.blit(start_text, text_rect)

        # Texte d'aide et ses paramètres
        help_text = self.font_small.render('Appuyez sur H pour l\'aide', True, (0, 0, 0))
        help_text_rect = help_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
        self.screen.blit(help_text, help_text_rect)

    def draw_help(self):
        # Créer un fond blanc pour l'aide
        help_background = pygame.Surface(self.screen.get_size())
        help_background.fill((255, 255, 255))
        self.screen.blit(help_background, (0, 0))

        # Rendu et affichage des contrôles
        controls_title = self.font_large.render('Contrôles', True, (0, 0, 0))
        controls_text = self.font_small.render('Déplacement: flèches directionnelles', True, (0, 0, 0))
        interact_text = self.font_small.render('Interagir: E', True, (0, 0, 0))
        start_text = self.font_small.render('Commencer: Entrée', True, (0, 0, 0))
        back_text = self.font_small.render('Retour: H', True, (0, 0, 0))

        # Rendu et affichage de l'histoire
        story_title = self.font_large.render('Histoire', True, (0, 0, 0))
        story_text = ("Un homme étrange s'est introduit dans le bureau de Tania et s'y est enfermé, "
                      "battez vos collègues et frayez-vous un passage dans le bureau pour l'en déloger!!")

        # Position et affichage des textes pour les contrôles
        self.screen.blit(controls_title, (50, 50))
        self.screen.blit(controls_text, (50, 150))
        self.screen.blit(interact_text, (50, 200))
        self.screen.blit(start_text, (50, 250))
        self.screen.blit(back_text, (50, 300))

        # Position et affichage des textes pour l'histoire
        self.screen.blit(story_title, (50, 400))

        # Wrapping et rendu du texte de l'histoire
        wrapped_story_lines = self.wrap_text(story_text, self.font_small, self.screen.get_width() - 100)
        y_offset = 500
        for line in wrapped_story_lines:
            rendered_line = self.font_small.render(line, True, (0, 0, 0))
            self.screen.blit(rendered_line, (50, y_offset))
            y_offset += rendered_line.get_height()

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word, True, (0, 0, 0))
            word_width = word_surface.get_width()
            if current_width + word_width >= max_width:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width + font.render(' ', True, (0, 0, 0)).get_width()
            else:
                current_line.append(word)
                current_width += word_width + font.render(' ', True, (0, 0, 0)).get_width()

        lines.append(' '.join(current_line))  # Ajouter la dernière ligne
        return lines
