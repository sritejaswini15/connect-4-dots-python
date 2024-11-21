import cv2
import pygame
import sys
import numpy as np
import math
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer

# Set up the screen dimensions
SCREEN_WIDTH = 525
SCREEN_HEIGHT = 525

# Load music files
pygame.mixer.music.load('background.mp3')
start_sound = pygame.mixer.Sound('startsound.mp3')
win_sound = pygame.mixer.Sound('win.mp3')
game_sound = pygame.mixer.Sound('game.mp3')

# Button class to handle button creation and scaling
class Button:
    def __init__(self, x, y, image_path, scale):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

#Functions to play and stop background music and various sound effects.
def play_background_music():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)  # Loop the background music indefinitely

def stop_background_music():
    pygame.mixer.music.stop()

def play_start_sound():
    start_sound.play()

def play_win_sound():
    stop_background_music()
    win_sound.play(-1)  # Loop the win sound indefinitely

def stop_win_sound():
    win_sound.stop()

def play_game_sound():
    game_sound.play()

def loading():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #This opens the video file player12.mp4 for reading frames.
    player12_video_path = 'player12.mp4'
    cap = cv2.VideoCapture(player12_video_path)

    # A clock object is created to control the frame rate, set to 30 frames per second.
    clock = pygame.time.Clock()
    frame_rate = 30
    #This loop continues running until the video ends or the user quits.
    running = True
    while running:
        ret, frame = cap.read() #reads a frame from the video.
        if not ret:
            running = False
            continue
        #Checks for Pygame events such as quitting the window or pressing the Escape key to exit.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        #converts the frame from BGR (OpenCV's default) to RGB (Pygame's format)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #resizes the frame to fit the screen dimensions.
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        #Convert the resized and color-corrected frame into a format that Pygame can display
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        #draws the frame on the screen.
        screen.blit(frame_surface, (0, 0))
        #updates the display to show the new frame.
        pygame.display.flip()

        #Ensures the loop runs at the specified frame rate.
        clock.tick(frame_rate)

    cap.release() # Releases the video capture object.
    main_game()  # Start the main game after the video
    sys.exit() # Exits the program.

def instructions():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    instructions_video_path = 'instructions.mp4'
    cap = cv2.VideoCapture(instructions_video_path)

    continue_button = Button(285, 420, "continue.jpg", 0.15)

    # Set up the clock for controlling the frame rate
    clock = pygame.time.Clock()
    frame_rate = 30  # Frames per second
    
    # Reads the next frame from the video. If no frame is returned,
    # it sets the video's position to the beginning to loop the video.
    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video
            continue
# Checks for Pygame events such as quitting the window,
# clicking the continue button, or pressing the Escape key to exit.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and continue_button.rect.collidepoint(event.pos):
                play_start_sound()
                cap.release()
                loading()  # Call the loading function
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        screen.blit(frame_surface, (0, 0))
        continue_button.draw(screen)
        pygame.display.flip()

        # Control the frame rate
        clock.tick(frame_rate)

    cap.release()
    pygame.quit()
    sys.exit()

def homepage():
    pygame.display.set_caption('Connect4dots')  # Set the window title
    #Creates a screen with the specified width and height.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    play_background_music() #Plays the background music in a loop

    video_path = 'video1.mp4'
    cap = cv2.VideoCapture(video_path) # Opens the video file video1.mp4 for playback.
    #Creates the button objects
    start_button = Button(275, 290, "start.jpg", 0.1)
    guide_button = Button(275, 330, "guide.jpeg", 0.1) 

    # Set up the clock for controlling the frame rate
    clock = pygame.time.Clock()
    frame_rate = 20  # Frames per second

    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and start_button.rect.collidepoint(event.pos):
                play_start_sound()
                cap.release()
                instructions()  # Call the instructions function
            elif event.type == pygame.MOUSEBUTTONDOWN and guide_button.rect.collidepoint(event.pos):
                play_start_sound()
                cap.release()
                guidewindow()  # Call the guidewindow function
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        screen.blit(frame_surface, (0, 0))
        start_button.draw(screen)
        guide_button.draw(screen)  # Draw the guide button
        pygame.display.flip()

        # Control the frame rate
        clock.tick(frame_rate)

    cap.release()
    pygame.quit()
    sys.exit()

# Function to handle the win/tie scenario with video playback and buttons
def winner(video_path, replay_action, exit_action):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    play_win_sound()

    cap = cv2.VideoCapture(video_path) #initializes the video capture object using OpenCV.
    replay_button = Button(190, 310, "replay.jpg", 0.1)
    exit_button = Button(330, 310, "exit.jpg", 0.1)

    clock = pygame.time.Clock() #Initializes a clock object from Pygame.
    frame_rate = 30  # Frames per second

    running = True
    while running:
        ret, frame = cap.read() #Reads each frame from the victory video.
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video
            continue

        for event in pygame.event.get(): #This loop processes all events in the Pygame event queue
            if event.type == pygame.QUIT:
                running = False #stop the main loop.
                stop_win_sound()
                exit_action()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.rect.collidepoint(event.pos):
                    play_start_sound()
                    running = False
                    stop_win_sound()
                    replay_action()
                elif exit_button.rect.collidepoint(event.pos):
                    play_start_sound()
                    running = False
                    stop_win_sound()
                    exit_action()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                stop_win_sound()
                exit_action()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Converts the frame from BGR to RGB color space, as OpenCV uses BGR by default and Pygame expects RGB.
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT)) #Resizes the frame to fit the screen dimensions
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1)) # Convert the video frame (originally in OpenCV's format) into a format that Pygame can work with.

        screen.blit(frame_surface, (0, 0)) #Draw the current video frame (frame_surface) onto the main display surface (screen).
        replay_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.flip()

        clock.tick(frame_rate)

    cap.release() #Releases the video capture object and frees associated resources.
    pygame.quit()
    sys.exit()

# color scheme
BLUE = (0, 37, 149)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
WINNING_COLOR = (135, 206, 235)

ROW_COUNT = 6
COLUMN_COUNT = 7

#Initializes the game board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

#Places a piece on the board.
def drop_piece(board, row, col, piece):
    board[row][col] = piece
    
#Checks if a column can accept a new piece.
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

#Finds the next open row in a column.
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Prints the board.
def print_board(board):
    print(np.flip(board, 0))
    
#Checks for a winning move
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return [(r, c), (r, c + 1), (r, c + 2), (r, c + 3)]

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return [(r, c), (r + 1, c), (r + 2, c), (r + 3, c)]

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return [(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)]

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return [(r, c), (r - 1, c + 1), (r - 2, c + 2), (r - 3, c + 3)]

    return None

#Draws the game board on the screen.
def draw_board(screen, board, winning_pieces=None, winning=False):
    SQUARESIZE = SCREEN_WIDTH // COLUMN_COUNT
    RADIUS = int(SQUARESIZE / 2 - 5)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2 + SQUARESIZE)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                color = WINNING_COLOR if winning and winning_pieces and (r, c) in winning_pieces else RED
                pygame.draw.circle(screen, color, (int(c * SQUARESIZE + SQUARESIZE / 2), SCREEN_HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                color = WINNING_COLOR if winning and winning_pieces and (r, c) in winning_pieces else YELLOW
                pygame.draw.circle(screen, color, (int(c * SQUARESIZE + SQUARESIZE / 2), SCREEN_HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

#The main game loop, handling player turns and checking for a win.
def main_game():
    def replay_game():
        homepage()

    def exit_game():
        pygame.quit()
        sys.exit()

    board = create_board()
    print_board(board)
    game_over = False 
    turn = 0 #to keep track of player turns.

    SQUARESIZE = SCREEN_WIDTH // COLUMN_COUNT #Calculates the size of each square on the game board based on the screen width and the number of columns.
    size = (SCREEN_WIDTH, SCREEN_HEIGHT) #Specifies the size of the game window.
    RADIUS = int(SQUARESIZE / 2 - 5) #Specifies the radius of the pieces to be drawn.

    screen = pygame.display.set_mode(size)
    draw_board(screen, board)
    pygame.display.update() # Updates the display to show the initial state of the game board.

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION: 
                pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SQUARESIZE))
                posx = event.pos[0] #Retrieves the x-coordinate of the mouse position from the event.pos tuple.
                if turn == 0: # 
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SQUARESIZE))
                play_game_sound()
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        winning_pieces = winning_move(board, 1)
                        if winning_pieces:
                            draw_board(screen, board, winning_pieces, winning=True)
                            pygame.display.update()
                            pygame.time.wait(500)  # Wait for 0.5 seconds
                            draw_board(screen, board, winning_pieces, winning=False)
                            pygame.display.update()
                            winner('player11.mp4', replay_game, exit_game)
                            game_over = True

                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        winning_pieces = winning_move(board, 2)
                        if winning_pieces:
                            draw_board(screen, board, winning_pieces, winning=True)
                            pygame.display.update()
                            pygame.time.wait(1300)  # Wait for 1.3 second
                            draw_board(screen, board, winning_pieces, winning=False)
                            pygame.display.update()
                            winner('player22.mp4', replay_game, exit_game)
                            game_over = True

                print_board(board)
                draw_board(screen, board)

                turn += 1
                turn = turn % 2

def guidewindow():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    video_paths = ['111.mp4', '222.mp4', '333.mp4', '444.mp4', '555.mp4', '666.mp4'] #list of paths to the video files to be played.
    videos = [cv2.VideoCapture(path) for path in video_paths] 

    # Set up the clock for controlling the frame rate
    clock = pygame.time.Clock()
    frame_rate = 30  # Frames per second

    running = True #to keep the main loop running.
    index = 0 #Initializes an index to keep track of the current video.
    while running:
        ret, frame = videos[index].read() #Reads the next frame from the current video.
        if not ret: #If not, increments the index to move to the next video.
            index += 1
            if index >= len(videos):
                break
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False #to exit 
            elif event.type == pygame.MOUSEBUTTONDOWN:# If the user clicks the mouse, increments the index to move to the next video
                index += 1
                if index >= len(videos):
                    running = False

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Converts the frame from BGR to RGB color space.
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1)) #Converts the frame to a Pygame Surface.

        screen.blit(frame_surface, (0, 0))
        pygame.display.flip() # Updates the display with the new frame.

        # Control the frame rate
        clock.tick(frame_rate)

    for video in videos:
        video.release()

    # Go back to the homepage
    homepage()
    
homepage()