import pygame

from canvas_utils import setup_game_canvas, render_text_on_screen, create_text

TYPING_SCENE_TIMER = 10

class TypingScene:

    @staticmethod
    def render_scene(canvas_surface, game_session, game_time_delta):
        canvas_surface_rect = canvas_surface.get_rect()

        # Put japanese and romanji word on screen
        jp_word, jp_word_rec = create_text("こんにちは！")
        render_text_on_screen(canvas_surface, canvas_surface_rect, jp_word, jp_word_rec, y_offset=-60)
        romanji_word, romanji_word_rect = create_text(game_session['word_input'])
        render_text_on_screen(canvas_surface, canvas_surface_rect, romanji_word, romanji_word_rect, y_offset=60)

        # Update timer and format as 00:xx
        game_session['TYPING_SCENE_TIMER'] -= game_time_delta / 1000
        if game_session['TYPING_SCENE_TIMER'] < 0:
            game_session['TYPING_SCENE_TIMER'] = 0
        if int(game_session['TYPING_SCENE_TIMER']) < 10:
            typing_timer_str = f"00:0{int(game_session['TYPING_SCENE_TIMER'])}"
        else:
            typing_timer_str = f"00:{int(game_session['TYPING_SCENE_TIMER'])}"
        tick_word, tick_word_rec = create_text(typing_timer_str)
        render_text_on_screen(canvas_surface, canvas_surface_rect, tick_word, tick_word_rec, y_align='top', y_offset=20)
        return

    @staticmethod
    def handle_input_event(event, game_session):
        active = True
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    game_session['word_input'] = ''
                elif event.key == pygame.K_BACKSPACE:
                    game_session['word_input'] = game_session['word_input'][:-1]
                else:
                    game_session['word_input'] += event.unicode