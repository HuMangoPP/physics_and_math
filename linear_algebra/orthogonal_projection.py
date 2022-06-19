import pygame,sys
import numpy as np
from math import *

FPS = 60

points = []
for x in (-1, 1):
    for y in (-1, 1):
        for z in (-1, 1):
            points.append(np.matrix([x, y, z]))

for x in (-2,2):
    for y in (-2,2):
        for z in (-2,2):
            points.append(np.matrix([x,y,z]))

projection_matrix = [
    [1,0,0],
    [0,1,0],
    [0,0,0]
]

projected_points = [
    [n,n] for n in range(len(points))
]

pygame.init()
clock = pygame.time.Clock()

WIDTH,HEIGHT = 1000,800
SCALE = 100;
CENTER = [WIDTH/2,HEIGHT/2]
angle = 0

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("tesseract")

def connect_points(i,j,points):
    pygame.draw.line(display,WHITE,(points[i][0],points[i][1]), (points[j][0],points[j][1]))

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    rotate_x = np.matrix([
        [1,0,0],
        [0,cos(angle),-sin(angle)],
        [0,sin(angle),cos(angle)]
    ])

    rotate_y = np.matrix([
        [cos(angle),0,sin(angle)],
        [0,1,0],
        [-sin(angle),0,cos(angle)]
    ])

    rotate_z = np.matrix([
        [cos(angle),-sin(angle),0],
        [sin(angle),cos(angle),0],
        [0,0,1]
    ])

    angle+=0.01

    display.fill(BLACK)

    for index,point in enumerate(points):
        rotated2d = np.dot(rotate_y,point.reshape((3,1)))
        rotated2d = np.dot(rotate_y,rotated2d)
        rotated2d = np.dot(rotate_z,rotated2d)
        projected2d = np.dot(projection_matrix,rotated2d)

        x = int(projected2d[0][0]*SCALE) + CENTER[0]
        y = int(projected2d[1][0]*SCALE) + CENTER[1]
        projected_points[index] = [x,y]
        pygame.draw.circle(display,RED,(x,y),5)

    for i in (0,2,4,6,8,10,12,14):
        connect_points(i,i+1,projected_points)
    for i in (0,1,4,5,8,9,12,13):
        connect_points(i,i+2,projected_points)
    for i in (0,1,2,3,8,9,10,11):
        connect_points(i,i+4,projected_points)
    for i in range(0,8):
        connect_points(i,i+8,projected_points)
    pygame.display.update()