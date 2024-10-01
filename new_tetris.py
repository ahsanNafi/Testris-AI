import pygame
import random
import new_ai
import trainer

colors = [
    (0, 0, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (128, 0, 128),
    (255, 255, 0),
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def fig(self):
        return self.figures[self.type]

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    level = 0
    score = 0
    cleared_lines = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None
    max_score = 0
    max_lines = 0
    weights = [0.25, 0.25, 0.25, 0.25]

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.level = 0
        self.score = 0
        self.cleared_lines = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    # reset the pos of the falling pieces
    def new_figure(self):
        self.figure = Figure(3, 0)

        # find the best place for the figure
        ai_place = new_ai.find_best_place(self.field, self.figure.fig(), weights=self.weights)
        self.ai_rotate = ai_place[0]
        self.ai_x = ai_place[1][0]
        self.ai_y = ai_place[1][1]
        # print(f"The figure will be place at [{self.ai_x}, {self.ai_y}] with rotation number {self.ai_rotate}")
        # Get the set of inputs to move piece

    # Collision detection
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    # clear lines if they are full
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        
        self.score += 4 * (self.level + 1) * lines
        self.cleared_lines += lines
        if (self.level + 2) * 5 <= self.cleared_lines // (self.level + 1):
            self.level += 1
        if (self.score > self.max_score):
            self.max_score = self.score
        if (self.cleared_lines > self.max_lines):
            self.max_lines = self.cleared_lines

    # hard drop piece on space press
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    # Move the piece down 1 space
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    # freeze the piece in place
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
            if player == "ai":
                self.state = "roundover"

    # move the falling piece by dx
    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    # rotate the piece
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


# Initalize the trainer
class Trainer:
    epoch_size = 20  # Number of indiviuals per epoche
    max_mutation = 0.1  # The max amount that mutation will change a value

    def __init__(self):
        seed = random.randrange(1000, 9999)  # If we want to controll randomness
        self.trainer = trainer.Trainer()
        self.trainer.size = self.epoch_size
        self.trainer.max_mute = self.max_mutation
        self.trainer.set_seed(seed)

        # Keep track of what number this is in the order
        self.child_num = 1


game = Tetris(20, 10)
player = "ai"

# Initialize the trainer
train = Trainer()

# Start up info
start_up = False
replay = False
classic_move = True
replaying = False
if start_up:
    player_choice = False
    custom_ai = True

    if player_choice:
        player_ai = input("Would you like to play yourself? [Y/N]")
        if player_ai == "Y":
            player = "user"
        else:
            player = "ai"

    if custom_ai:
        train.trainer.set_seed(int(input("Enter the seed")))
        new_weights = []
        for i in range(4):
            new_weights.append(float(input(f"enter wieght {i}")))
        game.weights = new_weights
        replay = True

        if input("would like classic movement? [Y/N]") == "Y":
            classic_move = True

        print("Ready to begin? Press space to begin")
        replaying = True
        

# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DRED = (255, 0, 0)

# Size of the screen
size = (600, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25

counter = 0

pressing_down = False

while replaying:
    for event in list(pygame.event.get()):
        if event.type == pygame.QUIT:
            done = True
            replaying = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                replaying = False

while not done:
    # Create figure if there is none
    if game.figure is None:
        game.new_figure()

    # region user input
    if player == "user":

        # Counter to limit the speed of the game
        counter += 1
        if counter > 100000:
            counter = 0
        # Go down consistently or when pushing down
        # Can remove the fps to allow AI time
        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        # Listen for input from user
        for event in list(pygame.event.get()):
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)

            # Stop going down if the key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False
    # endregion

    # region ai input
    if player == "ai" and not classic_move:
        
        for event in list(pygame.event.get()):
            if event.type == pygame.QUIT:
                done = True
        
        # Put the piece where it should go
        game.figure.rotation = game.ai_rotate
        game.figure.x = game.ai_x
        game.figure.y = game.ai_y

        game.freeze()
    elif player == "ai" and classic_move:
        if not game.figure.rotation == game.ai_rotate:
            game.rotate()
        elif game.figure.x > game.ai_x:
            game.go_side(-1)
        elif game.figure.x < game.ai_x:
            game.go_side(1)
        else:
            game.go_space()
        for event in list(pygame.event.get()):
            if event.type == pygame.QUIT:
                done = True

    # endregion

    # If the round ends (can move to after the drawing of the screen maybe)
    if game.state == "roundover":

        # Only play the one round
        if replay:
            done = True
            break

        # Log info about the game and do the post game analysis
        # commented out for simpler output for longer tests
        # print(f"score: {game.score} saving child {train.child_num}: mod{game.weights}")
        train.trainer.calc_fitness(game.score)

        if train.child_num == 20:
            # Save the data for the best of each generation.
            save_data = train.trainer.get_best()

            # Save data is a dictonary formated as such:
            # {
            # "seed":self.seed,
            # "modifiers":best_mod,
            # "score":best_fit,
            # "child number":best_index,
            # "generation":self.generation
            # }

            save_data["lines"] = game.cleared_lines
    
            # Saving code Here
            print(f"generation: {train.trainer.generation} \n{save_data}")
            # Then Generate a new set of weights to use
            train.trainer.gen_epoch()

        # Update the modifers
        game.weights = train.trainer.get_mod(train.child_num - 1)
        train.child_num = train.child_num % 20 + 1

        # Fix the seed so the piece order should not change
        random.seed(train.trainer.get_seed())

        # When done with everthing that restart the game and continue again
        game.__init__(20, 10)
        game.figure = None

    # Drawing the screen:
    screen.fill(BLACK)

    
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text_score = font.render("Score: " + str(game.score), True, WHITE)
    text_level = font.render("Level: " + str(game.level), True, WHITE)
    text_lines = font.render("Lines: " + str(game.cleared_lines), True, WHITE)
    text_max_score = font.render("MAX Score: " + str(game.max_score), True, DRED)
    text_max_lines = font.render("MAX Lines: " + str(game.max_lines), True, DRED)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    # Add custom text that includes:
    # generation number                 = train.trainer.generation
    # Child number within generation    = train.child_num and train.epoch_size
    # The current modifers              = game.weights

    screen.blit(text_level, [325, 70])
    screen.blit(text_lines, [325, 120])
    screen.blit(text_score, [325, 170])
    screen.blit(text_max_lines, [325, 370])
    screen.blit(text_max_score, [325, 420])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
