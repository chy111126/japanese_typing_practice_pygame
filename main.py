import pygame, sys
from canvas_utils import setup_game_canvas, render_text_on_screen, create_text
from scenes.typing import TypingScene

pygame.init()
pygame.key.set_repeat(500, 100)

canvas_screen_size, canvas_fps, canvas_surface, canvas_surface_rect, game_clock = setup_game_canvas()

i = 0
i_dir = True

active = True
ended = False
game_time_delta = 0

game_session = {
    'TYPING_SCENE_TIMER': 11,
    'word_input': '',
    'current_word': None,
}

import pandas as pd
vocabs_df = pd.read_csv("word_lists/all_chapters_vocabs.csv")
vocabs_df = vocabs_df[vocabs_df['kanji_form'].notna()]
vocabs_df = vocabs_df[vocabs_df['kanji_form'] != '-']
vocabs_df = vocabs_df[(vocabs_df['chapter'] >= 40) & (vocabs_df['chapter'] <= 45)]
game_session['word_list'] = vocabs_df

katakana_translate_df = pd.read_csv("katakana_mapping_list.csv")
katakana_translate_dict = {}
for idx, row in katakana_translate_df.iterrows():
    katakana_translate_dict[row['romanji']] = row['katakana']
game_session['katakana_translate_dict'] = katakana_translate_dict

while ended == False:
    # Setup background
    canvas_surface.fill('black')

    TypingScene.render_scene(canvas_surface, game_session, game_time_delta)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        TypingScene.handle_input_event(event, game_session)

    pygame.display.update()
    game_time_delta = game_clock.tick(canvas_fps)
