import pygame, sys, codecs

def setup_game_canvas():
    canvas_screen_size = (960, 544)
    canvas_fps = 60
    canvas_surface = pygame.display.set_mode(canvas_screen_size)
    canvas_surface_rect = canvas_surface.get_rect()
    game_clock = pygame.time.Clock()

    return canvas_screen_size, canvas_fps, canvas_surface, canvas_surface_rect, game_clock

def create_text(text_str, font_size=60):
    text = text_str
    newtext = text.encode("utf-8").decode("utf-8")
    gamefont = pygame.font.Font("fonts/ipaexg.ttf", font_size)
    gametext = gamefont.render(newtext, True, (225, 225, 225))
    gametext_rect = gametext.get_rect()
    return gametext, gametext_rect
    # canvas_surface.blit(gametext, (0, 0))

def render_text_on_screen(canvas_surface, canvas_surface_rect, gametext, 
                          x_align = 'center', x_offset=0, 
                          y_align = 'center', y_offset=0):
    gametext_rect = gametext.get_rect()
    # Calculate x and y using _align setting
    if x_align == 'center':
        text_x = canvas_surface_rect.centerx - gametext_rect.width / 2
    elif x_align == 'top':
        text_x = x_offset
    elif x_align == 'bottom':
        text_x = canvas_surface_rect.width - gametext_rect.width - x_offset

    if y_align == 'center':
        text_y = canvas_surface_rect.centery - gametext_rect.height / 2 + y_offset
    elif y_align == 'top':
        text_y = y_offset
    elif y_align == 'bottom':
        text_y = canvas_surface_rect.height - gametext_rect.height - y_offset
    canvas_surface.blit(gametext, (text_x, text_y))
    # Setup text
    if False:
        if i_dir:
            i += 1
            canvas_surface.blit(gametext, (i, canvas_surface_rect.centery - gametext_rect.height / 2))
        else:
            i -= 1
            canvas_surface.blit(gametext, (i, canvas_surface_rect.centery - gametext_rect.height / 2))
        if i == 0:
            i_dir = True
        elif i == 100:
            i_dir = False
        pass
    return