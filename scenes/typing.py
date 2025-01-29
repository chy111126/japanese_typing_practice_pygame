import pygame

from canvas_utils import setup_game_canvas, render_text_on_screen, create_text

class TypingScene:

    @staticmethod
    def init_scene(game_session):
        # Update pass-by-ref game session
        game_session.update({
            # game data
            'TYPING_SCENE_TIMER': 11,
            'word_input': '',
            'current_word': None,
            'lives_remaining': 4,
        })
        return

    @staticmethod
    def render_scene(canvas_surface, game_session, game_time_delta):
        canvas_surface_rect = canvas_surface.get_rect()

        # Boot the game back to title screen if dead
        if game_session['lives_remaining'] < 0:
            game_session['next_scene'] = 'TitleScene'
            return

        # Draw a word from word list
        if game_session['current_word'] is None:
            vocabs_df = game_session['word_list']
            random_vocab = vocabs_df.sample(1).iloc[0]
            japanese_form = random_vocab['japanese_form']
            kanji_form = random_vocab['kanji_form']
            romanji_form = str(random_vocab['romanji'])
            explanation = random_vocab['explanation']
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

        # Compute word_input to display form (with katakana)
        katakana_translate_dict = game_session['katakana_translate_dict']
        word_input = game_session['word_input']
        katakana_word_input = ''
        while len(word_input) > 0:
            # Test from three characters, then two characters, then one character
            already_found_a_katakana = False
            for word_to_cut in [4,3,2,1]:
                if len(word_input) > 2 and word_input[0] == word_input[1] and word_input[0] not in ['a', 'e', 'i', 'o', 'u', 'n','0','1','2','3','4','5','6','7','8','9']:
                    # Possible double consonants (small っ)
                    # It should only happen for non-vowels (aeiou) and n
                    katakana_word_input += 'っ'
                    word_input = word_input[1:]
                    continue
                else:
                    if word_to_cut == 4:
                        # If no double consonants check is needed, skip the outermost loop
                        continue
                    w = word_input[:word_to_cut]
                    # Peek if the testing word after this is aeiou, if so, it should not be e.g. n
                    # if len(word_input) > word_to_cut:
                    #     print(w, len(word_input) > word_to_cut+1 , word_input[word_to_cut-1] == 'n' , word_input[word_to_cut] in ['a', 'e', 'i', 'o', 'u'])
                    if len(word_input) > word_to_cut and word_input[word_to_cut-1] == 'n' and word_input[word_to_cut] in ['a', 'e', 'i', 'o', 'u']:
                        continue
                    # print("Testing for word:", w)
                    # print(w, w in katakana_translate_dict)
                    if w in katakana_translate_dict:
                        # print("Found:", w)
                        katakana_word_input += katakana_translate_dict[w]
                        word_input = word_input[word_to_cut:]
                        already_found_a_katakana = True
            # If all characters not match, output romanji for that char
            if not already_found_a_katakana and len(word_input) > 0:
                katakana_word_input += word_input[0]
                word_input = word_input[1:]

        # Put japanese and romanji word on screen
        if len(kanji_form) < 16:
            font_size = 60
        else:
            font_size = 30
        jp_word, jp_word_rec = create_text(kanji_form, font_size=font_size)
        render_text_on_screen(canvas_surface, canvas_surface_rect, jp_word, y_offset=-60)
        romanji_word, romanji_word_rect = create_text(katakana_word_input, font_size=30)
        render_text_on_screen(canvas_surface, canvas_surface_rect, romanji_word, y_offset=60)
        romanji_answer, romanji_answer_rect = create_text(romanji_form, font_size=30)
        render_text_on_screen(canvas_surface, canvas_surface_rect, romanji_answer, y_align='bottom', y_offset=60)
        explanation_answer, explanation_answer_rect = create_text(explanation, font_size=30)
        render_text_on_screen(canvas_surface, canvas_surface_rect, explanation_answer, y_align='bottom', y_offset=120)

        # Update timer and format as 00:xx
        game_session['TYPING_SCENE_TIMER'] -= game_time_delta / 1000
        if game_session['TYPING_SCENE_TIMER'] < 1:
            game_session['TYPING_SCENE_TIMER'] = 0
            # Reduce a life and draw a new word
            game_session.update({
                # game data
                'TYPING_SCENE_TIMER': 11,
                'word_input': '',
                'current_word': None,
            })
            game_session['lives_remaining'] -= 1
        if int(game_session['TYPING_SCENE_TIMER']) < 10:
            typing_timer_str = f"00:0{int(game_session['TYPING_SCENE_TIMER'])}"
        else:
            typing_timer_str = f"00:{int(game_session['TYPING_SCENE_TIMER'])}"
        tick_word, tick_word_rec = create_text(typing_timer_str)
        render_text_on_screen(canvas_surface, canvas_surface_rect, tick_word, y_align='top', y_offset=20)

        # Number of lives
        lives_remaining = "Life: " + str(game_session['lives_remaining'])
        lives_remaining, lives_remaining_rec = create_text(lives_remaining, font_size=30)
        render_text_on_screen(canvas_surface, canvas_surface_rect, lives_remaining, x_align='top', y_align='top', x_offset=20, y_offset=20)

        return

    @staticmethod
    def handle_input_event(event, game_session):
        active = True
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    # Check if input word is correct
                    romanji_form = game_session['current_word']['romanji_form']
                    word_input = game_session['word_input']
                    if word_input == romanji_form:
                        pass
                    else:
                        game_session['lives_remaining'] -= 1

                    # Reset timer and allow drawing next word
                    game_session.update({
                        # game data
                        'TYPING_SCENE_TIMER': 11,
                        'word_input': '',
                        'current_word': None,
                    })
                elif event.key == pygame.K_BACKSPACE:
                    game_session['word_input'] = game_session['word_input'][:-1]
                else:
                    game_session['word_input'] += event.unicode