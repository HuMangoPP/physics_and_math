from select import select
import pygame, sys, math

WIDTH = 1200
HEIGHT = 800
FPS = 60
ORIGX, ORIGY = WIDTH/2, 50
DOT_SIZE = 4
INIT_A1 = math.pi/2
INIT_A2 = math.pi/2

class Run:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Double Pendulum")
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.get_surface()
        self.trail = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)

        self.m1 = 20
        self.m2 = 50
        self.r1 = 200
        self.r2 = 300
        self.a1 = INIT_A1
        self.a2 = INIT_A2
        self.a1v = 0
        self.a2v = 0
        self.g = 0.5
        self.rect1 = pygame.Rect(0, 0, self.m1, self.m1)
        self.rect2 = pygame.Rect(0, 0, self.m2, self.m2)
        self.px, self.py = math.inf, math.inf

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.surface.fill('white')
            self.simulate()
            self.window.blit(self.trail, (0, 0))
            self.trail.fill('white', None, pygame.BLEND_RGBA_MULT)
            pygame.display.update()
            self.clock.tick(FPS)
    
    def simulate(self):
        self.a1a = (-self.g*(2*self.m1+self.m2)*math.sin(self.a1) - self.m2*self.g*math.sin(self.a1-2*self.a2) - 2*math.sin(self.a1-self.a2)*self.m2*(self.a2v*self.a2v*self.r2+self.a1v*self.a1v*self.r1*math.cos(self.a1-self.a2))) / (self.r1*(2*self.m1+self.m2-self.m2*math.cos(2*self.a1-2*self.a2)))

        self.a2a = (2*math.sin(self.a1-self.a2)*(self.a1v*self.a1v*self.r1*(self.m1+self.m2)+self.g*(self.m1+self.m2)*math.cos(self.a1)+self.a2v*self.a2v*self.r2*self.m2*math.cos(self.a1-self.a2))) / (self.r2*(2*self.m1+self.m2-self.m2*math.cos(2*self.a1-2*self.a2)))

        self.a1+=self.a1v
        self.a2+=self.a2v
        self.a1v+=self.a1a
        self.a2v+=self.a2a

        self.a1v*=0.999
        self.a2v*=0.999

        self.rect1.centerx = ORIGX+self.r1*math.sin(self.a1)
        self.rect1.centery = ORIGY+self.r1*math.cos(self.a1)
        self.rect2.centerx = self.rect1.centerx+self.r2*math.sin(self.a2)
        self.rect2.centery = self.rect1.centery+self.r2*math.cos(self.a2)
        self.draw()
        self.px, self.py = self.rect2.centerx, self.rect2.centery

    def draw(self):
        pygame.draw.line(self.surface, 'black', (ORIGX, ORIGY), (self.rect1.centerx, self.rect1.centery), DOT_SIZE)
        pygame.draw.line(self.surface, 'black', (self.rect1.centerx, self.rect1.centery), (self.rect2.centerx, self.rect2.centery), DOT_SIZE)
        pygame.draw.ellipse(self.surface, 'black', self.rect1)
        pygame.draw.ellipse(self.surface, 'black', self.rect2)
        if self.px!=math.inf:
            pygame.draw.line(self.trail, 'blue', (self.rect2.centerx, self.rect2.centery), (self.px, self.py), DOT_SIZE//2)

if __name__ == '__main__':
    pendulum = Run()
    pendulum.run()