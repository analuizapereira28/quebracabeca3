import pygame
import sys
import random

# Configurações iniciais
pygame.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
CARD_WIDTH, CARD_HEIGHT = 100, 150
FPS = 30
GRID_SIZE = (4, 4)  # 4 colunas e 4 linhas

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (135, 206, 235)  # Azul Claro para o fundo
CARD_BACK_COLOR = (220, 220, 220)  # Cor de fundo das cartas (cinza claro)

# Definindo cores para as cartas
COLORS = [
    (255, 0, 0),    # Vermelho
    (0, 255, 0),    # Verde
    (0, 0, 255),    # Azul
    (255, 255, 0),  # Amarelo
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Ciano
    (255, 128, 0),  # Laranja
    (128, 0, 255)   # Roxo
]

# Configurações de fonte
FONT_NAME = pygame.font.match_font('arial')
FONT_SIZE = 48  # Tamanho da fonte aumentado para o título
FONT_COLOR = (255, 255, 255)  # Cor do texto
TITLE_SHADOW_COLOR = (0, 0, 0)  # Cor da sombra do título


# Classe da carta
class Card:
    def __init__(self, color):
        self.color = color
        self.flipped = False

    def draw(self, surface, x, y):
        if self.flipped:
            pygame.draw.rect(surface, self.color, (x, y, CARD_WIDTH, CARD_HEIGHT))  # Usar a cor da carta
        else:
            pygame.draw.rect(surface, CARD_BACK_COLOR, (x, y, CARD_WIDTH, CARD_HEIGHT))  # Cor de fundo
            pygame.draw.rect(surface, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2)


# Classe do jogo da memória
class MemoryGame:
    def __init__(self):
        self.board = self.create_board()
        self.flipped_cards = []
        self.pairs_found = 0

    def create_board(self):
        # Criar uma lista de cores duplicadas para pares
        colors = COLORS * 2  # Duplicamos cada cor para ter pares
        random.shuffle(colors)  # Embaralha as cores
        return [[Card(colors.pop()) for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]

    def flip_card(self, row, col):
        card = self.board[row][col]
        if not card.flipped and len(self.flipped_cards) < 2:
            card.flipped = True
            self.flipped_cards.append((row, col))

            if len(self.flipped_cards) == 2:
                self.check_match()

    def check_match(self):
        row1, col1 = self.flipped_cards[0]
        row2, col2 = self.flipped_cards[1]
        if self.board[row1][col1].color != self.board[row2][col2].color:
            pygame.time.delay(1000)  # Aguarde 1 segundo antes de virar as cartas de volta
            self.board[row1][col1].flipped = False
            self.board[row2][col2].flipped = False
        else:
            self.pairs_found += 1
        self.flipped_cards = []

    def all_pairs_found(self):
        return self.pairs_found == (GRID_SIZE[0] * GRID_SIZE[1]) // 2


# Classe do botão
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text.upper()  # Mudar texto para maiúsculas
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 0, 0)
        self.hover_color = (50, 50, 50)
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)

    def draw(self, surface):
        # Muda a cor do botão se o mouse estiver sobre ele
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]


# Classe de exibição do jogo
class GameDisplay:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('Jogo da Memória - Tela Cheia')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)

        # Botões
        self.restart_button = Button("Reiniciar", WIDTH // 4, HEIGHT - 100, 200, 50)
        self.exit_button = Button("Sair", WIDTH // 2 + 20, HEIGHT - 100, 200, 50)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)  # Preenche o fundo com a cor de fundo
        self.draw_title()
        for row in range(GRID_SIZE[1]):
            for col in range(GRID_SIZE[0]):
                x = col * CARD_WIDTH + (WIDTH - CARD_WIDTH * GRID_SIZE[0]) // 2
                y = row * CARD_HEIGHT + 70
                self.game.board[row][col].draw(self.screen, x, y)

        self.display_message()

        # Desenha os botões
        self.restart_button.draw(self.screen)
        self.exit_button.draw(self.screen)

        pygame.display.flip()

    def draw_title(self):
        # Desenha a sombra do título
        title_shadow = self.font.render("JOGO DA MEMÓRIA", True, TITLE_SHADOW_COLOR)  # Título em maiúsculas
        title_rect_shadow = title_shadow.get_rect(center=(WIDTH // 2 + 2, 40 + 2))
        self.screen.blit(title_shadow, title_rect_shadow)

        # Desenha o título
        title = self.font.render("JOGO DA MEMÓRIA", True, FONT_COLOR)  # Título em maiúsculas
        title_rect = title.get_rect(center=(WIDTH // 2, 40))
        self.screen.blit(title, title_rect)

    def display_message(self):
        if self.game.all_pairs_found():
            text = self.font.render("VOCÊ ENCONTROU TODOS OS PARES!", True, BLACK)  # Texto em maiúsculas
            self.screen.blit(text, (WIDTH // 4, HEIGHT // 2 - 20))


# Função principal
def main():
    game = MemoryGame()
    display = GameDisplay(game)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Permite sair do jogo ao pressionar ESC
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                clicked_row = (mouse_y - 70) // CARD_HEIGHT
                clicked_col = (mouse_x - (WIDTH - CARD_WIDTH * GRID_SIZE[0]) // 2) // CARD_WIDTH

                if clicked_row < GRID_SIZE[1] and clicked_col < GRID_SIZE[0]:
                    game.flip_card(clicked_row, clicked_col)

                # Verifica se os botões foram clicados
                if display.restart_button.is_clicked():
                    game = MemoryGame()  # Reinicia o jogo
                if display.exit_button.is_clicked():
                    pygame.quit()
                    sys.exit()

        display.draw()
        display.clock.tick(FPS)


if __name__ == "__main__":
    main()

