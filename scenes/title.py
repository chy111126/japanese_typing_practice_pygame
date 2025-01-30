import pygame

from canvas_utils import setup_game_canvas, render_text_on_screen, create_text

TYPING_SCENE_TIMER = 10

class TitleScene:

    @staticmethod
    def init_scene(game_session):
        return

    @staticmethod
    def render_scene(canvas_surface, game_session, game_time_delta):
        canvas_surface_rect = canvas_surface.get_rect()

        jp_word = create_text("Typing game!", font_size=60)
        render_text_on_screen(canvas_surface, canvas_surface_rect, jp_word, y_offset=-60)

        jp_word = create_text("Press Enter to start", font_size=30)
        render_text_on_screen(canvas_surface, canvas_surface_rect, jp_word, y_offset=60)
        return

    @staticmethod
    def handle_input_event(event, game_session):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_session['next_scene'] = 'TypingScene'