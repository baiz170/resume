import pygame
import random
import psycopg2


pygame.init()
pygame.font.init() 


WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
SPEED_INCREMENT = 2
FOOD_LIFETIME = 5000  
WALL_COLOR = (100, 100, 100)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()


font = pygame.font.Font(None, 24)


def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="snake_game",  
        user="madikbaizakov",  
        password="Madik1722" 
    )


def save_score(username, score, level):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_scores (username, score, level) VALUES (%s, %s, %s)", (username, score, level))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Score saved for {username}: {score} at level {level}")
    except Exception as e:
        print(f"Error saving score: {e}")


def get_user_level(username):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT level FROM user_scores WHERE username = %s ORDER BY date DESC LIMIT 1", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else 1  
    except Exception as e:
        print(f"Error retrieving user level: {e}")
        return 1  

# Snake class
class Snake:
    def __init__(self, level):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)
        self.growing = False
        self.speed = 10 + level * SPEED_INCREMENT  
        self.level = level
        self.score = 0

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            return False

       
        if new_head in self.body:
            return False

        self.body.insert(0, new_head)

        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

        return True

    def grow(self, value):
        self.growing = True
        self.score += value

       
        if self.score % 3 == 0:
            self.level += 1
            self.speed += SPEED_INCREMENT

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))


class Food:
    def __init__(self, snake):
        self.position = self.generate_position(snake)
        self.value = random.choice([1, 2, 3])  
        self.spawn_time = pygame.time.get_ticks()  

    def generate_position(self, snake):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in snake.body:
                return (x, y)

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > FOOD_LIFETIME

    def draw(self):
        pygame.draw.rect(screen, RED, (*self.position, CELL_SIZE, CELL_SIZE))
        
        time_left = max(0, (FOOD_LIFETIME - (pygame.time.get_ticks() - self.spawn_time)) // 1000)
        timer_text = font.render(str(time_left), True, WHITE)
        screen.blit(timer_text, (self.position[0] + 5, self.position[1] - 20))

# Game loop
username = input("Enter your username: ")
current_level = get_user_level(username)  
print(f"Welcome back! Your current level is {current_level}.")

snake = Snake(current_level)
food = Food(snake)
running = True
paused = False  

while running:
    screen.fill(BLACK)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:  
        paused = not paused

    if not paused:
        
        if keys[pygame.K_UP] and snake.direction != (0, CELL_SIZE):
            snake.direction = (0, -CELL_SIZE)
        if keys[pygame.K_DOWN] and snake.direction != (0, -CELL_SIZE):
            snake.direction = (0, CELL_SIZE)
        if keys[pygame.K_LEFT] and snake.direction != (CELL_SIZE, 0):
            snake.direction = (-CELL_SIZE, 0)
        if keys[pygame.K_RIGHT] and snake.direction != (-CELL_SIZE, 0):
            snake.direction = (CELL_SIZE, 0)

        if not snake.move():
            print("Game Over!")
            save_score(username, snake.score, snake.level)  
            running = False

       
        if snake.body[0] == food.position:
            snake.grow(food.value)
            food = Food(snake)  

        
        if food.is_expired():
            food = Food(snake)  

        
        snake.draw()
        food.draw()

       
        score_text = font.render(f"Score: {snake.score}", True, BLUE)
        level_text = font.render(f"Level: {snake.level}", True, BLUE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

    else:
      
        pause_text = font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - 50, HEIGHT // 2))

    pygame.display.update()
    clock.tick(snake.speed)

    

pygame.quit()
