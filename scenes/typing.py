from collections import defaultdict

import pygame

from canvas_utils import setup_game_canvas, render_text_on_screen, create_text

from input_utils import map_romanji_to_katakana

TIMER_DEFAULT_VALUE = 31
# TIMER_DEFAULT_VALUE = 1

class TypingScene:

    @staticmethod
    def init_scene(game_session):
        # Update pass-by-ref game session
        game_session.update({
            # game data
            # 'TYPING_SCENE_TIMER': TIMER_DEFAULT_VALUE,
            # 'word_input': '',
            # 'current_word': None,
            'lives_remaining': 20,
            'keyboard_active': True,
            'recent_word_list': list(),
            "wrong_answers": defaultdict(int),
            # 'answered_wrong': False,
        })
        TypingScene.reset_for_next_word(game_session)
        return

    @staticmethod
    def reset_for_next_word(game_session):
        # Update pass-by-ref game session
        game_session.update({
            # game data
            'TYPING_SCENE_TIMER': TIMER_DEFAULT_VALUE,
            'word_input': '',
            'current_word': None,
            'answered_wrong': False,
        })
        return
    
    @staticmethod
    def mark_wrong_answer(game_session):
        # Mark wrong word for end-game stats
        wrong_answer = game_session['current_word']['kanji_form'] + " - " + game_session['current_word']['japanese_form']
        game_session['wrong_answers'][wrong_answer] += 1
        return
        

    @staticmethod
    def render_scene(canvas_surface, game_session, game_time_delta):
        canvas_surface_rect = canvas_surface.get_rect()

        # Boot the game back to title screen if dead
        if game_session['lives_remaining'] < 0:
            game_session['next_scene'] = 'GameOverScene'
            return

        if game_session['current_word'] is None:
            vocabs_df = game_session['word_list']
            # Draw a word from word list (that is not recently shown)
            is_non_recent_word_drawn = False
            while not is_non_recent_word_drawn:
                # vocabs_df = vocabs_df[vocabs_df['romanji'] == 'bonodori']
                random_vocab = vocabs_df.sample(1).iloc[0]
                japanese_form = random_vocab['japanese_form']
                kanji_form = random_vocab['kanji_form']
                romanji_form = str(random_vocab['romanji'])
                explanation = random_vocab['explanation']
                if romanji_form not in game_session['recent_word_list']:
                    is_non_recent_word_drawn = True
            game_session['current_word'] = {
                'japanese_form': japanese_form,
                'kanji_form': kanji_form,
                'romanji_form': romanji_form,
                'explanation': explanation,
            }
        else:
            japanese_form = game_session['current_word']['japanese_form']
            kanji_form = game_session['current_word']['kanji_form']
            romanji_form = game_session['current_word']['romanji_form']
            explanation = game_session['current_word']['explanation']

        katakana_word_input = map_romanji_to_katakana(game_session)

        # Put japanese and romanji word on screen
        if len(kanji_form) < 16:
            font_size = 60
        else:
            font_size = 30
        jp_word = create_text(kanji_form, font_size=font_size)
        render_text_on_screen(canvas_surface, canvas_surface_rect, jp_word, y_offset=-60)
        romanji_word = create_text(katakana_word_input, font_size=30)
        render_text_on_screen(canvas_surface, canvas_surface_rect, romanji_word, y_offset=60)

        if game_session['answered_wrong']:
            romanji_answer = create_text(romanji_form, font_size=30)
            render_text_on_screen(canvas_surface, canvas_surface_rect, romanji_answer, y_align='bottom', y_offset=60)

        explanation_answer = create_text(explanation, font_size=30, font_locale='zh-hk')
        render_text_on_screen(canvas_surface, canvas_surface_rect, explanation_answer, y_align='bottom', y_offset=120)

        # Update timer and format as 00:xx
        if game_session['keyboard_active']:
            game_session['TYPING_SCENE_TIMER'] -= game_time_delta / 1000
            # game_session['TYPING_SCENE_TIMER'] -= 1
            if game_session['TYPING_SCENE_TIMER'] < 1:
                game_session['TYPING_SCENE_TIMER'] = 0
                # Reduce a life and draw a new word
                TypingScene.mark_wrong_answer(game_session)
                TypingScene.reset_for_next_word(game_session)
                game_session['lives_remaining'] -= 1
        if int(game_session['TYPING_SCENE_TIMER']) < 10:
            typing_timer_str = f"00:0{int(game_session['TYPING_SCENE_TIMER'])}"
        else:
            typing_timer_str = f"00:{int(game_session['TYPING_SCENE_TIMER'])}"
        tick_word = create_text(typing_timer_str)
        render_text_on_screen(canvas_surface, canvas_surface_rect, tick_word, y_align='top', y_offset=20)

        # Number of lives
        lives_remaining = "Life: " + str(game_session['lives_remaining'])
        lives_remaining = create_text(lives_remaining, font_size=30)
        render_text_on_screen(canvas_surface, canvas_surface_rect, lives_remaining, x_align='top', y_align='top', x_offset=20, y_offset=20)

        return

    @staticmethod
    def handle_input_event(event, game_session):
        active = game_session['keyboard_active']
        if active and event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    # Check if input word is correct
                    romanji_form = game_session['current_word']['romanji_form']
                    word_input = game_session['word_input']
                    if word_input == romanji_form:
                        # Reset timer and allow drawing next word
                        if len(game_session['recent_word_list']) < 10:
                            game_session['recent_word_list'].append(game_session['current_word']['romanji_form'])
                        else:
                            game_session['recent_word_list'].append(game_session['current_word']['romanji_form'])
                            game_session['recent_word_list'] = game_session['recent_word_list'][1:]
                        TypingScene.reset_for_next_word(game_session)
                    else:
                        # game_session['keyboard_active'] = False
                        TypingScene.mark_wrong_answer(game_session)
                        game_session['lives_remaining'] -= 1
                        game_session['word_input'] = ''
                        game_session['answered_wrong'] = True
                elif event.key == pygame.K_BACKSPACE:
                    game_session['word_input'] = game_session['word_input'][:-1]
                else:
                    game_session['word_input'] += event.unicode