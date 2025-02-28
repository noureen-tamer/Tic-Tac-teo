import pygame, sys
import pygame.locals
import random
from collections import deque


pygame.init()


WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")


board = [['' for _ in range(COLS)] for _ in range(ROWS)]
player_turn = 'X'


def draw_board():
    WINDOW.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(WINDOW, BLACK, (col * SQUARE_SIZE, row *
                             SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), LINE_WIDTH)
            if board[row][col] == 'X':
                pygame.draw.line(WINDOW, BLUE, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20),
                                 ((col + 1) * SQUARE_SIZE - 20, (row + 1) * SQUARE_SIZE - 20), LINE_WIDTH - 5)
                pygame.draw.line(WINDOW, BLUE, ((col + 1) * SQUARE_SIZE - 20, row * SQUARE_SIZE + 20),
                                 (col * SQUARE_SIZE + 20, (row + 1) * SQUARE_SIZE - 20), LINE_WIDTH - 5)
            elif board[row][col] == 'O':
                pygame.draw.circle(WINDOW, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 20, LINE_WIDTH - 5)


def check_winner(board):
    for i in range(ROWS):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None


def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == '':
                return False
    return True


def get_empty_cells(board):
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                empty_cells.append((i, j))
    return empty_cells


def bfs(board):
    queue = deque([(board, [])])
    visited = set()
    visited.add(tuple(map(tuple, board)))

    while queue:
        current_board, path = queue.popleft()
        winner = check_winner(current_board)
        if winner == 'O':
            return path
        elif winner == 'X':
            continue

        for row, col in get_empty_cells(current_board):
            new_board = copy.deepcopy(current_board)
            new_board[row][col] = 'O'
            if tuple(map(tuple, new_board)) not in visited:
                queue.append((new_board, path + [new_board]))
                visited.add(tuple(map(tuple, new_board)))


def make_move(row, col):
    global player_turn, board
    if board[row][col] == '':
        board[row][col] = player_turn
        player_turn = 'O' if player_turn == 'X' else 'X'
        draw_board()
        winner = check_winner(board)
        if winner:
            display_winner_message(winner)
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
        elif is_board_full(board):
            display_draw_message()
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()


def find_best_move(board):
    # Check for a winning move
    for row, col in get_empty_cells(board):
        board[row][col] = 'O'
        if check_winner(board) == 'O':
            board[row][col] = ''
            return row, col
        board[row][col] = ''

    for row, col in get_empty_cells(board):
        board[row][col] = 'X'
        if check_winner(board) == 'X':
            board[row][col] = ''
            return row, col
        board[row][col] = ''

    empty_cells = get_empty_cells(board)
    if empty_cells:
        return random.choice(empty_cells)
    return None


def play_ai():
    global player_turn
    if player_turn == 'O':
        best_move = find_best_move(board)
        if best_move:
            make_move(*best_move)


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def display_draw_message():
    font = pygame.font.Font(None, 36)
    text = "It's a draw!"
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WINDOW.blit(text_surface, text_rect)


def display_winner_message(winner):
    font = pygame.font.Font(None, 36)
    text = f"Player {winner} wins!"
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WINDOW.blit(text_surface, text_rect)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(mouse_pos)
                make_move(row, col)
                play_ai()
        draw_board()
        pygame.display.update()


if __name__ == "__main__":
    main()