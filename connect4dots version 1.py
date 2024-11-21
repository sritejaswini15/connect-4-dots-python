import cv2
import pygame
import numpy as np
import sys
import math

class Button:
    def __init__(self, x, y, image_path, scale):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

def run_background_video(video_path, start_button, replay_button, exit_button):
    pygame.init()
    pygame.mixer.init()

    # Load sounds
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play(-1)  # Loop indefinitely
    button_click_sound = pygame.mixer.Sound('startsound.mp3')

    cap = cv2.VideoCapture(video_path)
    screen_width, screen_height = 525, 525

    # Control video frame rate
    frame_delay = 0.05  # seconds

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Connect4Dots")

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)  # Rotate the frame
        frame = np.flipud(frame)  # Flip vertically to correct orientation
        frame = cv2.resize(frame, (screen_width, screen_height), interpolation=cv2.INTER_LINEAR)  # Use linear interpolation for better quality
        frame = pygame.surfarray.make_surface(frame)
        
        screen.blit(frame, (0, 0))

        # Draw the buttons on top of the video
        start_button.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cap.release()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.clicked(event.pos):
                    button_click_sound.play()
                    pygame.time.wait(500)  # Wait for 500 milliseconds (adjust as needed)
                    pygame.mixer.music.load('background.mp3')
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    # Draw the blue grid
                    board = create_board()
                    draw_board(board, screen)
                    # Start the game loop
                    button_clicked_function(screen, replay_button, exit_button)
                    # Pass replay and exit buttons to the play_video function
                    play_video("player1.mp4", screen, replay_button, exit_button, win=True)

        pygame.time.delay(int(frame_delay * 1000))

def play_video(video_path, screen, replay_button, exit_button, win=False):
    cap = cv2.VideoCapture(video_path)
    frame_delay = 33  # milliseconds (approximately 30 frames per second)
    replay_clicked = False  # Flag to track if replay button is clicked

    if win:
        pygame.mixer.music.load('win.mp3')
        pygame.mixer.music.play(-1)  # Loop indefinitely

    button_click_sound = pygame.mixer.Sound('startsound.mp3')

    # Load video frames into memory
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        frame = np.rot90(frame)  # Rotate the frame
        frame = np.flipud(frame)  # Flip vertically to correct orientation
        frame = cv2.resize(frame, (screen.get_width(), screen.get_height()), interpolation=cv2.INTER_LINEAR)  # Resize to match screen resolution
        frames.append(frame)
    
    # Play the preloaded video frames
    for frame in frames:
        screen.blit(pygame.surfarray.make_surface(frame), (0, 0))
        # Draw the buttons on top of the video
        replay_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.clicked(event.pos):
                    button_click_sound.play()
                    pygame.time.wait(500)  # Wait for 500 milliseconds
                    replay_clicked = True
                    break  # Break out of the event loop to stop processing further events
                elif exit_button.clicked(event.pos):
                    button_click_sound.play()
                    pygame.quit()
                    sys.exit()

        if replay_clicked:
            break  # Break out of the frame loop if replay button is clicked

        pygame.time.delay(frame_delay)

    if replay_clicked:
        # Reset and restart the game
        run_background_video("video.mp4", start_button, replay_button, exit_button)

def button_clicked_function(screen, replay_button, exit_button):
    board = create_board()
    game_over = False
    turn = 0

    SQUARESIZE = 75
    RADIUS = int(SQUARESIZE/2 - 5)
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE

    drop_sound = pygame.mixer.Sound('game.mp3')

    while not game_over:
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1 if turn == 0 else 2)
                    drop_sound.play()

                    if winning_move(board, 1 if turn == 0 else 2):
                        draw_board(board, screen)
                        pygame.display.update()
                        
                        if turn == 0:
                            play_video("player1.mp4", screen, replay_button, exit_button, win=True)
                        else:
                            play_video("player2.mp4", screen, replay_button, exit_button, win=True)
                        game_over = True
                    elif np.count_nonzero(board) == ROW_COUNT * COLUMN_COUNT:
                        draw_board(board, screen)
                        pygame.display.update()
                        
                        play_video("tie.mp4", screen, replay_button, exit_button)
                        game_over = True
                    else:
                        turn += 1
                        turn = turn % 2

                        draw_board(board, screen)
        pygame.display.update()

        if game_over:
            pygame.time.wait(3000)
            screen.fill(BLACK)
            pygame.display.update()

# Connect 4 game functions
#color scheme
BLUE = (0, 0, 204)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board, screen):
    SQUARESIZE = 75
    RADIUS = int(SQUARESIZE/2 - 5)
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

if __name__ == "__main__":
    # Load the start, replay, and exit buttons
    start_button = Button(205, 312, "start.jpg", 0.1)
    replay_button = Button(25, 343, "replay.jpg", 0.17)
    exit_button = Button(292, 343, "exit.jpg", 0.17)

    # Run background video with start button
    run_background_video("video.mp4", start_button, replay_button, exit_button)