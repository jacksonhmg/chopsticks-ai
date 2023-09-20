# import pygame
# import time
# import random
import os

# WIDTH, HEIGHT = 800, 600
# WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# pygame.display.set_caption("Space Invaders")

# WIN.fill((255, 255, 255))
# pygame.display.update()

# def draw():
#     WIN.blit(BG, (0, 0))

# def main():
#     run = True

#     while run:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 break

#     pygame.quit()


def display_hands(player, left_hand, right_hand):
    print(f"{player}'s hands: Left: {left_hand} | Right: {right_hand}\n")

def strike(attacker, defender, hands):

    # Ensure the strike is valid
    validAttacker = False
    while not validAttacker:
        attack_hand = input(f"{attacker}, choose a hand to attack with (left/right): ").strip().lower()
        if hands[attacker][attack_hand] == 0:
            print("Invalid strike. Please try again.")
        else:
            validAttacker = True

    validAttacked = False
    while not validAttacked:
        attacked_hand = input(f"{attacker}, choose a hand to attack (left/right): ").strip().lower()
        if hands[defender][attacked_hand] == 0:
            print("Invalid strike. Please try again.")
        else:
            validAttacked = True

    # Calculate the result of the strike
    hands[defender][attacked_hand] += hands[attacker][attack_hand]
    if hands[defender][attacked_hand] >= 5:
        hands[defender][attacked_hand] = 0

    # Display the result
    display_hands(defender, hands[defender]['left'], hands[defender]['right'])

def split(player, hands):
    print(f"{player} is splitting.")
    # Ensure the split is valid
    total = hands[player]['left'] + hands[player]['right']
    while True:
        left = int(input(f"Enter the number of fingers for the left hand (total fingers = {total}): "))
        right = total - left
        if 0 <= left <= 4 and 0 <= right <= 4:
            break
        print("Invalid split. Please try again.")
    
    hands[player]['left'] = left
    hands[player]['right'] = right
    display_hands(player, hands[player]['left'], hands[player]['right'])

def game_over(hands):
    result = False
    for player in hands:
        if hands[player]['left'] != 0 or hands[player]['right'] != 0:
            result = False
        else:
            return True

    return result

def main():
    hands = {
        'Player 1': {'left': 1, 'right': 1},
        'Player 2': {'left': 1, 'right': 1}
    }

    current_player = 'Player 1'
    while not game_over(hands):
        os.system('clear')

        display_hands("Player 1", hands["Player 1"]['left'], hands["Player 1"]['right'])
        display_hands("Player 2", hands["Player 2"]['left'], hands["Player 2"]['right'])

        cant_split = False

        if hands[current_player]['left'] == hands[current_player]['right']:
            cant_split = True
        
        if cant_split:
            action = input(f"{current_player}, choose an action (strike) (you can't split because you have equal values on both hands): ").strip().lower()
        else:
            action = input(f"{current_player}, choose an action (strike/split): ").strip().lower()

        if action == 'strike':
            if current_player == 'Player 1':
                strike('Player 1', 'Player 2', hands)
            else:
                strike('Player 2', 'Player 1', hands)
        elif action == 'split' and not cant_split:
            split(current_player, hands)
        else:
            print("Invalid action. Please choose 'strike' or 'split'.")
            continue

        # Switch to the other player
        current_player = 'Player 1' if current_player == 'Player 2' else 'Player 2'

    print(f"{current_player} loses! Game over.")

if __name__ == "__main__":
    main()
