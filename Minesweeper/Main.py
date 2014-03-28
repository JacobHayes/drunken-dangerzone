#!/usr/bin/env python3
# CS 101
#
# Jacob Hayes
# jacob.r.hayes@gmail.com

import Minesweeper

print("\t\tMinesweeper!")

run = True

while run == True:
    game_state = 'p'

    while True:
        try:
            horiz = abs(int(input("Board Width: ")))
            vert = abs(int(input("Board Height: ")))
            mines = abs(int(input("Number of Mines: ")))
            break
        except ValueError:
            print("Use '1' instead of 'one'")

    game = Minesweeper.Minesweeper(horiz, vert, mines)

    while game_state == 'p':
        print(game.display_Board("Player"))
        game_state = game.get_Input()

    play_again = input("Play again? [Y]/N:")

    if play_again.lower() in ('n', 'q', "no", "exit", "quit", "stop"):
        run = False
