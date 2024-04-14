import pygame
import random

# Tamanho da janela
WIDTH, HEIGHT = 640, 480

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Tamanho do labirinto
ROWS, COLS = 20, 20

# Tamanho das células
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Inicializar Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Classe para representar uma célula do labirinto
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

# Função auxiliar para obter os vizinhos de uma célula
def get_neighbors(cell, cells):
    neighbors = []
    if cell.row > 0: # vizinho de cima
        neighbors.append(cells[cell.row - 1][cell.col])
    if cell.row < ROWS - 1: # vizinho de baixo
        neighbors.append(cells[cell.row + 1][cell.col])
    if cell.col > 0: # vizinho da esquerda
        neighbors.append(cells[cell.row][cell.col - 1])
    if cell.col < COLS - 1: # vizinho da direita
        neighbors.append(cells[cell.row][cell.col + 1])
    return neighbors

# Função auxiliar para remover a parede entre duas células
def remove_wall(cell1, cell2):
    if cell1.row == cell2.row:
        if cell1.col > cell2.col: # cell2 está à esquerda de cell1
            cell1.walls["left"] = False
            cell2.walls["right"] = False
        else: # cell2 está à direita de cell1
            cell1.walls["right"] = False
            cell2.walls["left"] = False
    else:
        if cell1.row > cell2.row: # cell2 está acima de cell1
            cell1.walls["top"] = False
            cell2.walls["bottom"] = False
        else: # cell2 está abaixo de cell1
            cell1.walls["bottom"] = False
            cell2.walls["top"] = False

# Função para gerar o labirinto usando o algoritmo de busca em profundidade
def generate_maze(cells):
    # Escolher uma célula aleatória para começar
    start = cells[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]
    start.visited = True

    # Iniciar a pilha com a célula inicial
    stack = [start]

    while len(stack) > 0:
        current = stack[-1]

        # Obter os vizinhos não visitados da célula atual
        neighbors = [cell for cell in get_neighbors(current, cells) if not cell.visited]

        if len(neighbors) > 0:
            # Escolher um vizinho aleatório
            neighbor = random.choice(neighbors)

            # Remover a parede entre a célula atual e o vizinho escolhido
            remove_wall(current, neighbor)

            # Marcar o vizinho como visitado e adicioná-lo à pilha
            neighbor.visited = True
            stack.append(neighbor)
        else:
            # Se a célula atual não tem vizinhos não visitados, removê-la da pilha
            stack.pop()

# Função para desenhar o labirinto
def draw_maze(cells):
    for row in cells:
        for cell in row:
            x = cell.col * CELL_WIDTH
            y = cell.row * CELL_HEIGHT
            if cell.walls["top"]:
                pygame.draw.line(WIN, WHITE, (x, y), (x + CELL_WIDTH, y))
            if cell.walls["right"]:
                pygame.draw.line(WIN, WHITE, (x + CELL_WIDTH, y), (x + CELL_WIDTH, y + CELL_HEIGHT))
            if cell.walls["bottom"]:
                pygame.draw.line(WIN, WHITE, (x, y + CELL_HEIGHT), (x + CELL_WIDTH, y + CELL_HEIGHT))
            if cell.walls["left"]:
                pygame.draw.line(WIN, WHITE, (x, y), (x, y + CELL_HEIGHT))

# Função para desenhar a bolinha vermelha
def draw_ball(x, y):
    pygame.draw.circle(WIN, RED, (x * CELL_WIDTH + CELL_WIDTH // 2, y * CELL_HEIGHT + CELL_HEIGHT // 2), min(CELL_WIDTH, CELL_HEIGHT) // 4)

# Função para desenhar a bolinha branca no final do labirinto
def draw_finish():
    pygame.draw.circle(WIN, WHITE, ((COLS - 1) * CELL_WIDTH + CELL_WIDTH // 2, (ROWS - 1) * CELL_HEIGHT + CELL_HEIGHT // 2), min(CELL_WIDTH, CELL_HEIGHT) // 4)

# Função principal
def main():
    clock = pygame.time.Clock()
    cells = [[Cell(i, j) for j in range(COLS)] for i in range(ROWS)]
    generate_maze(cells)

    # Posição inicial da bolinha
    ball_x, ball_y = 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if ball_y > 0 and not cells[ball_y][ball_x].walls["top"]:
                        ball_y -= 1
                elif event.key == pygame.K_DOWN:
                    if ball_y < ROWS - 1 and not cells[ball_y][ball_x].walls["bottom"]:
                        ball_y += 1
                elif event.key == pygame.K_LEFT:
                    if ball_x > 0 and not cells[ball_y][ball_x].walls["left"]:
                        ball_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if ball_x < COLS - 1 and not cells[ball_y][ball_x].walls["right"]:
                        ball_x += 1
        
        # Verificar se a bolinha vermelha chegou à bolinha branca
        if ball_x == COLS - 1 and ball_y == ROWS - 1:
            print("Parabéns por concluir o labirinto")
            running = False

        WIN.fill((0, 0, 0))
        draw_maze(cells)
        # Desenhar a bolinha vermelha na posição atual
        draw_ball(ball_x, ball_y)
        # Desenhar a bolinha branca no final do labirinto
        draw_finish()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
