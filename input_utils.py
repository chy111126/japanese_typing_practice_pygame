import pandas as pd
import json

def init_word_list(game_session):
    vocabs_df = pd.read_csv("word_lists/all_chapters_vocabs.csv")
    vocabs_df = vocabs_df[vocabs_df['kanji_form'].notna()]
    vocabs_df = vocabs_df[vocabs_df['kanji_form'] != '-']
    vocabs_df = vocabs_df[(vocabs_df['chapter'] >= 40) & (vocabs_df['chapter'] <= 45)]
    game_session['word_list'] = vocabs_df

    katakana_translate_df = pd.read_csv("word_lists/katakana_mapping_list.csv")
    katakana_translate_dict = {}
    for idx, row in katakana_translate_df.iterrows():
        katakana_translate_dict[row['romanji']] = row['katakana']
    game_session['katakana_translate_dict'] = katakana_translate_dict

    special_words_dict = json.load(open('word_lists/special_words.json', 'r', encoding='utf-8'))
    game_session['special_words_dict'] = special_words_dict

def map_romanji_to_katakana(game_session):
    # Compute word_input to display form (with katakana)
    # TODO: Better matching engine for cases like bonodori -> bon o do ri (but not bo no do ri)
    current_word_romanji = game_session['current_word']['romanji_form']
    katakana_translate_dict = game_session['katakana_translate_dict']
    special_words_dict = game_session['special_words_dict']
    word_input = game_session['word_input']
    katakana_word_input = ''
    while len(word_input) > 0:
        # Test from three characters, then two characters, then one character
        already_found_a_katakana = False
        matched_special_word = False
        for word_to_cut in [4,3,2,1]:
            # print(word_input, word_to_cut)
            # Special word rules always go over ordinary rules
            if current_word_romanji in special_words_dict:
                # Check with special rules first
                w = word_input[:word_to_cut]
                if w in special_words_dict[current_word_romanji]:
                    katakana_word_input += special_words_dict[current_word_romanji][w]
                    word_input = word_input[len(w):]
                    matched_special_word = True
                    # print("matched_special_word", katakana_word_input, word_input)
                    break
            if not matched_special_word:
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
                    # print("Testing for word:", w)
                    # Peek if the testing word after this is aeiou, if so, it should not be e.g. n
                    if len(word_input) > word_to_cut and word_input[word_to_cut-1] == 'n' and word_input[word_to_cut] in ['a', 'e', 'i', 'o', 'u']:
                        continue
                    # print(w, w in katakana_translate_dict)
                    if w in katakana_translate_dict:
                        # print("Found:", w)
                        katakana_word_input += katakana_translate_dict[w]
                        word_input = word_input[word_to_cut:]
                        already_found_a_katakana = True
        # If all characters not match, output romanji for that char
        if not already_found_a_katakana and not matched_special_word and len(word_input) > 0:
            katakana_word_input += word_input[0]
            word_input = word_input[1:]
    return katakana_word_input

if __name__ == '__main__':
    game_session = {
        'current_word': {
            'romanji_form': 'bonodori'
        },
        # 'word_input': 'bonodori'
        'word_input': 'kimono'
    }
    init_word_list(game_session)
    print(map_romanji_to_katakana(game_session))