import pygame

from canvas_utils import setup_game_canvas, render_text_on_screen, create_text

class GameOverScene:

    @staticmethod
    def init_scene(game_session):
        return

    @staticmethod
    def render_scene(canvas_surface, game_session, game_time_delta):
        canvas_surface_rect = canvas_surface.get_rect()

        jp_word = create_text("Game over!", font_size=60)
        render_text_on_screen(canvas_surface, canvas_surface_rect, jp_word, y_align='top', y_offset=20)

        top_ten_wrong_words = create_text("Top ten wrong answers:", font_size=20)
        render_text_on_screen(canvas_surface, canvas_surface_rect, top_ten_wrong_words, y_align='top', y_offset=120)
        for idx, (k, v) in enumerate(list(sorted(game_session['wrong_answers'].items(), key=lambda item: -item[1]))[:10]):
            top_ten_wrong_words = create_text(f"{k}:   {v}", font_size=20)
            render_text_on_screen(canvas_surface, canvas_surface_rect, top_ten_wrong_words, y_align='top', y_offset=160 + 30 * idx)

        jp_word = create_text("Press Enter to restart", font_size=20)
        render_text_on_screen(canvas_surface, canvas_surface_rect, jp_word, y_align='bottom', y_offset=20)
        return

    @staticmethod
    def handle_input_event(event, game_session):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_session['next_scene'] = 'TypingScene'