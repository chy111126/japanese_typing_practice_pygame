import pygame, sys
from canvas_utils import setup_game_canvas, render_text_on_screen, create_text

from scenes.title import TitleScene
from scenes.typing import TypingScene

pygame.init()
pygame.key.set_repeat(500, 100)

canvas_screen_size, canvas_fps, canvas_surface, canvas_surface_rect, game_clock = setup_game_canvas()

game_session = {

    # game data
    # 'TYPING_SCENE_TIMER': 11,
    # 'word_input': '',
    # 'current_word': None,
    # 'lives_remaining': 4,

    'next_scene': 'TitleScene',
}

import pandas as pd
vocabs_df = pd.read_csv("word_lists/all_chapters_vocabs.csv")
vocabs_df = vocabs_df[vocabs_df['kanji_form'].notna()]
vocabs_df = vocabs_df[vocabs_df['kanji_form'] != '-']
vocabs_df = vocabs_df[(vocabs_df['chapter'] >= 20) & (vocabs_df['chapter'] <= 30)]
game_session['word_list'] = vocabs_df

katakana_translate_df = pd.read_csv("katakana_mapping_list.csv")
katakana_translate_dict = {}
for idx, row in katakana_translate_df.iterrows():
    katakana_translate_dict[row['romanji']] = row['katakana']
game_session['katakana_translate_dict'] = katakana_translate_dict

current_scene = None
ended = False
game_time_delta = 0
while ended == False:
    # Setup background
    canvas_surface.fill('black')

    next_scene = game_session['next_scene']
    if next_scene is not None:
        # Load next scene if something is put on the queue
        if next_scene == 'TitleScene':
            current_scene = TitleScene
        elif next_scene == 'TypingScene':
            current_scene = TypingScene
        game_session['next_scene'] = None
        current_scene.init_scene(game_session)

    current_scene.render_scene(canvas_surface, game_session, game_time_delta)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        current_scene.handle_input_event(event, game_session)

    pygame.display.update()
    game_time_delta = game_clock.tick(canvas_fps)
