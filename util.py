import pygame

def get_font(font_path, size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(font_path, size)

def draw_text(text, font, color, x, y, alignment, screen):
    text_surface = font.render(text, True, color)
    
    match alignment:
        case 'center':
            text_rect = text_surface.get_rect(center = (x, y))
        case 'left':
            text_rect = text_surface.get_rect(left = x, centery = y)
        case 'right':
            text_rect = text_surface.get_rect(right = x, centery = y)
        case _:
            text_rect = text_surface.get_rect(center = (x, y))

    screen.blit(text_surface, text_rect)

def is_point_inside_rect(point, rect):
    return rect[0] < point[0] < rect[0] + rect[2] and rect[1] < point[1] < rect[1] + rect[3]