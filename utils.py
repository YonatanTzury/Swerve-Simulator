import pygame

def draw_circle(screen, pos, r, color, direction, d_color):
    pygame.draw.circle(screen, color, pos, r)

    end_pos = pos + (direction * r * 1.2)
    pygame.draw.line(screen, d_color, pos, end_pos)
