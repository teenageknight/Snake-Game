import pygame
import time

from random import randint

# Global variables
# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,128,0)
RED = (255,0,0)
# from random import randint
class Player:
    """docstring for the player."""

    def __init__(self, gameWindow, screen_width, screen_height):
        self.gameWindow = gameWindow
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 20
        self.head = pygame.Rect(self.screen_width/2, self.screen_height/2, 20, 20)
        # self.head = pygame.draw.rect()
        self.direction = 'up'
        # Location is a list of list where the first one is the location of the head. Also, starts in the center
        self.body = []

    def drawPlayer(self):
        pygame.draw.rect(self.gameWindow, GREEN, self.head)

        for body_part in self.body:
            pygame.draw.rect(self.gameWindow, GREEN, body_part)

    def updateBody(self):
        new_list = []
        temporary_list = []
        for i, body_part in list(enumerate(self.body)):

            if i == 0:
                temporary_list.append(body_part)
                body_part = self.head.copy()
                new_list.append(body_part)
            else:
                temporary_list.append(body_part)
                body_part = temporary_list[i-1].copy()
                new_list.append(body_part)

        # update the body with the new values from the for loop
        self.body = new_list

    def eatingSelf(self):
        for body_part in self.body:
            if self.head.colliderect(body_part):
                return True
            else:
                pass
        return False

    def outOfBounds(self):
        if self.head.x < 0 or self.head.x > self.screen_width:
            return True
        if self.head.y < 0 or self.head.y > self.screen_height:
            return True

    def movePlayer(self):
        self.updateBody()

        if self.direction == 'up':
            self.head = self.head.move(0, -self.speed)
        elif self.direction == 'down':
            self.head = self.head.move(0, self.speed)
        elif self.direction == 'left':
            self.head = self.head.move(-self.speed, 0)
        elif self.direction == 'right':
            self.head = self.head.move(self.speed, 0)

    def eatingFood(self, center):
        # Returns a boolean wether or not the center of the food is in the head of the snake
        # center type is a tuple
        return self.head.collidepoint(center)

    def addBody(self):
        if len(self.body) == 0:
            new_body_part = self.head.copy()
        else:
            # If this is not the first body part it copys the last item in the body list
            new_body_part = self.body[-1].copy()


        if self.direction == 'up':
            new_body_part = new_body_part.move(0, self.head.height + 20)
        elif self.direction == 'down':
            new_body_part = new_body_part.move(0, - self.head.height - 20)
        elif self.direction == 'left':
            new_body_part = new_body_part.move(self.head.height + 20, 0)
        elif self.direction == 'right':
            new_body_part = new_body_part.move(- self.head.height - 20, 0)
        self.body.append(new_body_part)

class Food:
    """Stores the information about the food and where it spawns."""

    def __init__(self, gameWindow, screen_width, screen_height):
        self.gameWindow = gameWindow
        self.screen_width = screen_width
        self.screen_height = screen_height

    def newFood(self):
        self.x = randint(10, self.screen_width-10)
        self.y = randint(10, self.screen_height-10)

    def drawFood(self):
        self.FOOD = pygame.draw.circle(self.gameWindow, RED, [self.x, self.y], 5)

class Application:
    """Stores the information for the game."""

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Initialize pygame display function
        pygame.display.init()

        # Initialize pygame.Font
        pygame.font.init()

        # Open the game window
        self.screen_width = 800
        self.screen_height = 600
        self.gameWindow = pygame.display.set_mode([self.screen_width, self.screen_height])

        # Set name and icon of gameWindow
        pygame.display.set_caption('Snake Game')


    def displayMessage(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', 30)
        textSurface = largeText.render(text, True, WHITE)
        textRect = textSurface.get_rect()
        textRect.center = ((self.screen_width/2, self.screen_height/2))
        self.gameWindow.blit(textSurface, textRect)

    def endGame(self, score):
        # Makes screen white
        pygame.Surface.fill(self.gameWindow, BLACK)

        message = "Game Over! Your final score was " + str(score)
        self.displayMessage(message)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitGame()

            # if any key is pressed, end the game
            keys = pygame.key.get_pressed()
            if keys:
                pass


    def exitGame(self):
        # Quits the Font module
        pygame.font.quit()

        # Quits the display module
        pygame.display.quit()

        # Quits pygame
        pygame.quit()

    def startGame(self):
        # Makes screen white
        pygame.Surface.fill(self.gameWindow, BLACK)

        self.displayMessage("Press (W, A, S, D) to Start")

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitGame()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                return 'up'
            if keys[pygame.K_s]:
                return 'down'
            if keys[pygame.K_a]:
                return 'left'
            if keys[pygame.K_d]:
                return 'right'

    def gameLoop(self, player, food):
        gameOver = False

        # Sets up the variables that will be affected by the while loop
        score = 0

        clock = pygame.time.Clock()

        pygame.Surface.fill(self.gameWindow, WHITE)

        player.drawPlayer()

        food.newFood()
        food.drawFood()

        pygame.display.update()

        while not gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitGame()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                player.direction = 'up'
            if keys[pygame.K_s]:
                player.direction = 'down'
            if keys[pygame.K_a]:
                player.direction = 'left'
            if keys[pygame.K_d]:
                player.direction = 'right'

            if player.eatingSelf() or player.outOfBounds():
                self.endGame(score)

            if player.eatingFood(food.FOOD.center):
                print("Food eaten. Generating new food...")
                score += 10
                food.newFood()
                player.addBody()

            player.movePlayer()

            # All functions dealing with drawing go after here
            pygame.Surface.fill(self.gameWindow, WHITE)
            food.drawFood()
            # Draw the player after the food so the food looks like it is under the player (eaten)
            player.drawPlayer()
            pygame.display.update()

            # Slows the speed of the movement
            clock.tick(player.speed)

        return score

    def runGame(self):
        player = Player(self.gameWindow, self.screen_width, self.screen_height)

        food = Food(self.gameWindow, self.screen_width, self.screen_height)

        # After everything is initalizied, run the game
        player.direction = self.startGame()

        score = self.gameLoop(player, food)

        self.endGame(score)

        self.exitGame()

def main():
    app = Application()

    app.runGame()


if __name__ == '__main__':
    main()
