import pygame
import os
import random
import math 
import sys
import numpy as np
# from genetic import Genetic
pygame.init()
import matplotlib.pyplot as plt


# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1300
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONT = pygame.font.Font('freesansbold.ttf', 20)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False

        # Khung hình bao quanh khủng long
        self.image = self.run_img[0]
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, self.image.get_width(), self.image.get_height())
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0
        self.W = np.random.randn(16,5)
        self.W2 = np.random.randn(3,16)

        # Khởi tạo vị trí khủng long
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        # self.W = np.random.choice([-1.,0.,1.],size=(16,5))
        # self.W2 = np.random.choice([-1.,0.,1.],size=(3,16))
        
        # Điểm ban đầu bằng 0
        self.score = 0
        
    # Hàm cập nhật trạng thái khủng long
    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if self.step_index >= 10:
            self.step_index = 0

    # Trạng thái nhảy
    def jump(self):
        # Cập nhật hình ảnh khủng long nhảy
        self.image = self.jump_img
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    # Trạng thái chạy
    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    # Trạng thái cúi xuống
    def duck(self):
        self.image = DUCKING[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_DUCK
        self.step_index += 1
        # self.dino_run = True
        # self.dino_jump = False
        # self.dino_duck = False

    # Vẽ khủng long lên màn hình game tương ứng với trạng thái
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)

# Class chướng ngại vật
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = pygame.Rect(self.image[self.type].get_rect())
        self.rect.x = SCREEN_WIDTH + random.randint(0,200)*(1+game_speed*0.01)

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
        self.rect = self.rect

    # Vẽ hình ảnh  chướng ngại vật
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        pygame.draw.rect(SCREEN, (100,100,100), (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)

# Chướng ngại: Xương rồng nhỏ
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

# Chướng ngại: Xương rồng lớn
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

# Chướng ngại: Chim
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        # Độ cao của chim: 3 trạng thái độ cao
        self.rect.y = 250 + random.choice([50, -50])
        self.index = 0

    # Trạng thái của chim: Cài đặt trạng thái vỗ cánh
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1
        pygame.draw.rect(SCREEN, (100,100,100), (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)

def remove(index):
    dinosaurs.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

class Genetic:
    def __init__(self,num_gen=10,num_pop=100):
        self.num_gen = num_gen
        self.num_pop = num_pop
        self.gen_count = 0
        self.gen = []
        self.gen_best = []
        self.best_fitness = np.zeros(5)+0.2
        self.best_score = 0
        for _ in range(self.num_pop):
            self.gen.append(Dinosaur())

    def crossover(self,dino1,dino2):
        child = Dinosaur()
        choice1 = np.random.randint(2, size = dino1.W.shape).astype(bool)
        choice2 = np.random.randint(2, size = dino1.W2.shape).astype(bool)
        child.W = np.where(choice1,dino1.W,dino2.W)
        child.W2 = np.where(choice2,dino1.W2,dino2.W2)
        return child

    def mutation(self,dino):
        dummy = Dinosaur()
        choice1 = np.random.choice([1.,0.],p = [0.9,0.1], size = dino.W.shape).astype(bool)
        choice2 = np.random.choice([1.,0.],p = [0.9,0.1], size = dino.W2.shape).astype(bool)
        dino.W = np.where(choice1,dino.W,dummy.W)
        dino.W2 = np.where(choice2,dino.W2,dummy.W2)
        return dino

    def fitness(self,dino):
        return dino.score

    def reset(self):
        self.gen = []
    
    def next_gen(self):
        for dino in self.gen_best:
            dino.score = 0
            self.gen.append(dino)
        for i in range(10):
            self.gen.append(Dinosaur())
        while len(self.gen) < self.num_pop:
            if np.random.rand()>0.5:
                dino1,dino2 = np.random.choice(self.gen_best,size=2,p=self.best_fitness / np.sum(self.best_fitness),replace=False)
            else:
                dino1,dino2 = np.random.choice(self.gen[:10],size=2,replace=False)
            if np.random.rand() < 1:
                child = self.crossover(dino1,dino2)
            if np.random.rand()<0.5:
                self.gen.append(self.mutation(child))
            else:   
                self.gen.append(child)
    
    def evaluate(self):
        fitness = [self.fitness(dino) for dino in self.gen]
        self.gen_best = np.array(self.gen)[np.argsort(fitness)][-5:]
        self.best_fitness = np.array(fitness)[np.argsort(fitness)][-5:]
        if self.best_fitness[-1] > self.best_score:
            self.best_score = self.best_fitness[-1]
        self.reset()
        self.w = self.gen_best[-1].W
        self.w2 = self.gen_best[-1].W2
        # print(self.gen_best)
        print(f'Top Fitness:{self.best_fitness}')


def train(num_gen=10,num_dino=100,fps=30):
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, points
    clock = pygame.time.Clock()

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    genetic = Genetic(num_pop=num_dino)
    for num in range(num_gen):
        game_speed = 20
        genetic.gen_count+=1
        if num!=0:
            genetic.next_gen()
        else:
            pass
        points = 0
        obstacles = []
        dinosaurs = []
        for dino in genetic.gen:
            dinosaurs.append(dino)


        def score():
            global points, game_speed
            points += 1
            if points % 100 == 0:
                game_speed += 0.5
            text_1 = FONT.render(f'Score: {str(points)}', True, (0, 0, 0))
            text_2 = FONT.render(f'Hi Fitness:{genetic.best_score:.1f}',True,(0,0,0))
            text_3 = FONT.render(f'TRAINING MODE!',True,(0,0,0))
            # SCREEN.blit(text_1, (850, 50))
            SCREEN.blit(text_2, (800, 80))
            SCREEN.blit(text_3, (795, 50))
        def statistics():
            global dinosaurs, game_speed
            text_1 = FONT.render(f'Dinosaurs Alive:{str(len(dinosaurs))}', True, (0, 0, 0))
            text_2 = FONT.render(f'Generation:{genetic.gen_count}', True, (0, 0, 0))
            text_3 = FONT.render(f'Game Speed:{str(game_speed)}', True, (0, 0, 0))

            SCREEN.blit(text_1, (50, 450))
            SCREEN.blit(text_2, (50, 480))
            SCREEN.blit(text_3, (50, 510))

        def background():
            global x_pos_bg, y_pos_bg
            image_width = BG.get_width()
            SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            if x_pos_bg <= -image_width:
                x_pos_bg = 0
            x_pos_bg -= game_speed

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            SCREEN.fill((255, 255, 255))

            for dinosaur in dinosaurs:
                dinosaur.update()
                dinosaur.draw(SCREEN)
            if points>=100000:
                with open('Data\w.npy','wb') as f:
                        np.save(f,dinosaurs[0].W)
                with open('Data\w2.npy','wb') as f2:
                    np.save(f2,dinosaurs[0].W2)
                print('Saved!')
                genetic.best_score = 100000
                pygame.quit()
            if len(dinosaurs) == 0:
                break

            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))


            for obstacle in obstacles:
                obstacle.draw(SCREEN)       
                obstacle.update()
                for i, dinosaur in enumerate(dinosaurs):
                    if dinosaur.rect.colliderect(obstacle.rect):
                        # dinosaur.score = points
                        remove(i)
                    # print(len(dinosaurs))
                    else:
                        if dinosaur.dino_run==False:
                            dinosaur.score+=0.1
                        else:
                            dinosaur.score+=1
                        if dinosaur.rect.y == dinosaur.Y_POS  or dinosaur.rect.y == dinosaur.Y_POS+40:

                            output = dinosaur.W @ np.array([dinosaur.rect.y,obstacle.rect.x,obstacle.rect.y,\
                                    distance((dinosaur.rect.x, dinosaur.rect.y),obstacle.rect.midtop),game_speed]\
                                    ,dtype=float).reshape(-1,1)
                            output   = np.maximum(output,0)
                            output = dinosaur.W2 @ output
                            output = output.reshape(-1)

                            if np.argmax(output)==0 :
                                dinosaur.dino_jump = True
                                dinosaur.dino_run = False
                                dinosaur.dino_duck = False
                            elif np.argmax(output)==1 :
                                dinosaur.dino_jump = False
                                dinosaur.dino_run = False
                                dinosaur.dino_duck = True
                            else:
                                dinosaur.dino_jump = False
                                dinosaur.dino_run = True
                                dinosaur.dino_duck = False

            statistics()
            score()
            background()
            clock.tick(fps)
            pygame.display.update()
        
        genetic.evaluate()

def eval(fps=30):
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, points
    clock = pygame.time.Clock()
    

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    game_speed = 20
    points = 0
    obstacles = []
    dino_eval = Dinosaur()
    if sys.argv[1]=='eval_best':
        dino_eval.W = np.load('Data\w_best.npy')
        dino_eval.W2 = np.load('Data\w2_best.npy')
        print(f'W1: {dino_eval.W}')
        print(f'W2: {dino_eval.W2}')
    elif sys.argv[1]=='eval':
        # print(f'W1: {dino_eval.W}')
        # print(f'W2: {dino_eval.W2}')
        with open('Data/w.npy','rb') as f:
            dino_eval.W = np.load(f)
        with open('Data/w2.npy','rb') as f2:
            dino_eval.W2 = np.load(f2)
        print(f'W1: {dino_eval.W}')
        print(f'W2: {dino_eval.W2}')
    dinosaurs = [dino_eval]

    def score():
        global points, game_speed
        points += 1
        if points % 300 == 0:
            game_speed += 1
            game_speed = min(40,game_speed)
        text = FONT.render(f'Fitness:{dino_eval.score:.1f}', True, (0, 0, 0))
        text_2 = FONT.render(f'EVALUATE MODE!',True,(0,0,0))
        SCREEN.blit(text_2, (850, 20))
        SCREEN.blit(text, (850, 50))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    text1 = FONT.render(f'Jump!', True, (0, 0, 0))
    text2 = FONT.render(f'Duck!', True, (0, 0, 0))
    text3 = FONT.render(f'Run!', True, (0, 0, 0))
    mode = -1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((255, 255, 255))

        dino_eval.update()
        dino_eval.draw(SCREEN)

        if len(dinosaurs) == 0:
            print(f'Dino final score: {dino_eval.score}')
            break
        if dino_eval.dino_run==False:
            dino_eval.score+=0.1
        else:
            dino_eval.score+=1

        if len(obstacles) == 0:
            rand_int = random.randint(0, 2)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
            elif rand_int == 2:
                if np.random.rand()<0.5:
                        obstacles.append(Bird(BIRD, random.randint(0, 1)))
                else:
                    obstacles.append(HighBird(BIRD,2))
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if dino_eval.rect.colliderect(obstacle.rect):
                dino_eval.score = points
                dinosaurs = []
            else:
                if dino_eval.rect.y == dino_eval.Y_POS or dino_eval.rect.y == dino_eval.Y_POS+40:
                    # output = dino_eval.W @ np.array([dino_eval.rect.y,distance((dino_eval.rect.x, dino_eval.rect.y),obstacle.rect.midtop)],dtype=float).reshape(-1,1)
                    output = dino_eval.W @ np.array([dino_eval.rect.y,obstacle.rect.x,obstacle.rect.y,distance((dino_eval.rect.x, dino_eval.rect.y),obstacle.rect.midtop),game_speed],dtype=float).reshape(-1,1)
                    output   = np.maximum(output,0)
                    output = dino_eval.W2 @ output
                    output = output.reshape(-1)
                    if np.argmax(output)==0 :
                        dino_eval.dino_jump = True
                        dino_eval.dino_run = False
                        dino_eval.dino_duck = False
                    
                        mode = 1
                    elif np.argmax(output)==1 :
                        dino_eval.dino_jump = False
                        dino_eval.dino_run = False
                        dino_eval.dino_duck = True
                        mode = 2   
                    else:
                        dino_eval.dino_jump = False
                        dino_eval.dino_run = True
                        dino_eval.dino_duck = False
                        mode = 3
                # SCREEN.blit(text3, (400, 50))
        if mode==1:
            SCREEN.blit(text1, (400, 50))
        elif mode==2:
            SCREEN.blit(text2, (400, 50))
        elif mode==3:
            SCREEN.blit(text3, (400, 50))
        score()
        background()
        clock.tick(int(fps))
        pygame.display.update()

train(1500,200,1200)