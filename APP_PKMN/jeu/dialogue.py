import pygame

class DialogueBox:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.box_rect = pygame.Rect(50, 450, 700, 100)
        self.box_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.dialogue = ""
        self.name = ""

    def set_dialogue(self, text, name=""):
        self.dialogue = text
        self.name = name
        print(f"{name} : {text}")  # Debug message
        if name:
            print(f"Dresseur {name} veut se battre")  # Debug message

    def draw(self):
        pygame.draw.rect(self.screen, self.box_color, self.box_rect)
        pygame.draw.rect(self.screen, self.text_color, self.box_rect, 2)

        if self.name:
            name_rect = pygame.Rect(self.box_rect.x, self.box_rect.y - 30, 150, 30)
            pygame.draw.rect(self.screen, self.box_color, name_rect)
            pygame.draw.rect(self.screen, self.text_color, name_rect, 2)
            name_surface = self.font.render(self.name, True, self.text_color)
            self.screen.blit(name_surface, (self.box_rect.x + 5, self.box_rect.y - 25))

        lines = self.wrap_text(self.dialogue, self.font, self.box_rect.width - 20)
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, self.text_color)
            self.screen.blit(text_surface, (self.box_rect.x + 10, self.box_rect.y + 10 + i * 30))

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            text_surface = font.render(' '.join(current_line), True, self.text_color)
            if text_surface.get_width() > max_width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]

        lines.append(' '.join(current_line))
        return lines
