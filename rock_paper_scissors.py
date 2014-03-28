# CS 101
# rock_paper_scissors.py
# Jacob Hayes
#
# PROBLEM: Play Rock-Paper-Scissors with a player, progressevly
#          playing smarter based on the player's previous hands
# ALGORITHM:
# - At all prompts, allow 'h' or 'help' for help info
#     - Show game types and map what hand beats others
# - Map out inputs: Rock = r, Paper = p, Scissors = s
# - Get user choice
# - Choose calculated choice based on previous player's choices
# - Store player and computed choice in choice history
# - Display winner or tie and choices
#
# -When quitting, show game summary
#     - Games total, won, lost, favorite hand, and number of each hand's use

def is_int(input_val):
    try:
        input_val = int(input_val)
        return True

    except ValueError:
        return False
#def is_int

def is_valid(input_val):
    if is_int(input_val) == True:
        print("\nNumbers are invalid...")

        return is_valid('h')
    elif input_val in valid_input:
        return True
    elif input_val == 'h' or input_val == 'help':
        print("\n\tChoice: Rock -> 'r' Paper -> 'p' Scissors -> 's'")
        print("\tHelp -> 'h' or Quit -> 'q'")
        print("\t\tRock beats Scissors, but loses to Paper")
        print("\t\tScissors beats Paper, but loses to Rock")
        print("\t\tPaper beats Rock, but loses to Scissors\n")

        return False
    else:
        print("\nUnknown input:", player_hand)

        return False
#def is_valid

rounds = 0
ties = 0
player_wins = 0
player_losses = 0

valid_input = ('r', 'p', 's', 'q', "rock", "paper", "scissors", "quit")
player_hand_hist = {'r' : 0,
                    'p' : 0,
                    's' : 0}

print("Rock - Paper - Scissors")

play = True
while play == True:
    print("\n\tChoices: Rock -> 'r' Paper -> 'p' Scissors -> 's'")
    print("\tHelp -> 'h' or Quit -> 'q'")
    player_hand = input("Enter your desired hand: ").lower()

    while is_valid(player_hand) == False:
        player_hand = input("Enter a valid hand: ").lower()

    if player_hand == 'q' or player_hand == "quit":
        play = False

        print("Quitting...")
        continue
    else:
        max_played_hand = max(player_hand_hist, key=player_hand_hist.get)

        # Calculate computer hand
        if max_played_hand == 'r':
            computer_hand = 'p'
        elif max_played_hand == 'p':
            computer_hand = 's'
        elif max_played_hand == 's':
            computer_hand = 'r'

        # Add to our player hand counts
        if player_hand == 'r' or player_hand == "rock":
            player_hand_hist['r'] += 1

        elif player_hand == 'p' or player_hand == "paper":
            player_hand_hist['p'] += 1

        elif player_hand == 's' or player_hand == "scissors":
            player_hand_hist['s'] += 1

        print("You played:", player_hand + "... I played:", computer_hand)

        if player_hand == computer_hand:
            print("We tied...")
            ties += 1
        elif (player_hand == 'r' and computer_hand != 'p') or (player_hand == 'p' and computer_hand != 's') or (player_hand == 's' and computer_hand != 'r'):
            print("You won!")
            player_wins += 1
        else:
            print("Yeah, I won!")
            player_losses += 1

    rounds += 1

for key, value in player_hand_hist.items():
    print(key, ":", value)
print("Number of rounds:", rounds)
print("Wins:", player_wins, "| Losses:", player_losses, "| Ties:", ties)
input("\nPress enter to exit...")
