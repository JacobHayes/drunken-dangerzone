#!/usr/bin/env python3

import Life_Module

print("\t\tGame of Life!")

play_new_game = True
while play_new_game == True:
    game_type = input("Random or Still Life? [R]/S: ").lower()
    game_type = "Random" if game_type != 's' else "StillLife"

    game = None
    while game is None:
        try:
            horiz = input("\nHow wide a grid [5]: ")
            vert = input("How tall a grid [5]: ")
            live_cells = input("How many live cells [5]: ")
    
            game = Life_Module.Life(game_type, horiz, vert, live_cells)
        except (Life_Module.InputError, Life_Module.TooManyLiveCells):
            pass

    if game_type == "Random":
        print(game)

        msg = ""
        play_next_round = True
        while play_next_round == True:
            play_next_round = input("Next round [Y]/N: ").lower()
            play_next_round = True if play_next_round != 'n' else False

            if play_next_round == True:
                try:
                    play_next_round = game.next_round() # This may return false, meaning no more cells on the board
                    if play_next_round == False:
                        print(game)
                        msg = "The game ended"
                        break
                except Life_Module.LifeStill as ls:
                    msg = str(ls)
                    break
                finally:
                    print(game)
                    print(msg, end="")
            else:
                break
    else:
        num_still_lives = 0
        tot_combos = 0
        for still_life in game.still_life():
            if still_life == True:
                print("Still Life found!")
                print(game)
                num_still_lives += 1
            else:
                pass

            tot_combos += 1
        print("Done. Found {} Still Lives out of {} combinations.".format(num_still_lives, tot_combos), end="")

    play_new_game = input("\n\nNew game [Y]/N: ").lower()
    play_new_game = True if play_new_game != 'n' else False

print("\nAffirmative, Dave. I read you.")
