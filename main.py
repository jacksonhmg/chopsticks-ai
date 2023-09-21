import pygame
import time
import random
import os
import threading

pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Invaders")


def get_input(prompt, result_list):
    result_list[0] = input(prompt).strip().lower()


def draw(hands):
    WIN.fill((255, 255, 255))

    font = pygame.font.Font('freesansbold.ttf', 32)

    for index, (player, hand) in enumerate(hands.items()):
        if index == 0:
            player = 'Player 1'
            height = 1.2
            increment = 0.1
            pWidth = 1.3
        else:
            player = 'Player 2'
            height = 6
            increment = 2
            pWidth = 10

        text = font.render(player, True, (0, 0, 0))

        textRect = text.get_rect()

        textRect.center = (WIDTH // 2, HEIGHT // pWidth)
        
        WIN.blit(text, textRect)

        for ind, (side, value) in enumerate(hand.items()):
            if ind == 0:
                width = WIDTH // 3
            else:
                width = WIDTH // 1.525
            text = font.render(side, True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (width, HEIGHT // height)
            WIN.blit(text, textRect)

            text = font.render(str(value), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (width, HEIGHT // (height-increment))
            WIN.blit(text, textRect)


    pygame.display.update()


class Button:
    def __init__(self, text, x, y, colour):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = 200
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self.text, 1, (0, 0, 0))
        win.blit(text, (self.x + (self.width // 2 - text.get_width() // 2),
                        self.y + (self.height // 2 - text.get_height() // 2)))

    def click(self,pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def main():
    hands = {
        'Player 1': {'left': 1, 'right': 1},
        'Player 2': {'left': 1, 'right': 1}
    }

    current_player = 'Player 1'

    run = True

    while run and not game_over(hands):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(hands)

        os.system('clear')

        display_hands("Player 1", hands["Player 1"]['left'], hands["Player 1"]['right'])
        display_hands("Player 2", hands["Player 2"]['left'], hands["Player 2"]['right'])

        cant_split = False

        if hands[current_player]['left'] == hands[current_player]['right']:
            cant_split = True
        
        buttons = [None]

        if cant_split:
            prompt = f"{current_player}, choose an action (strike) (you can't split because you have equal values on both hands): "
            buttons[0] = Button('Strike', WIDTH // 2 - 100, HEIGHT // 2 - 50, (255, 0, 0))
        else:
            prompt = f"{current_player}, choose an action (strike/split): "
            buttons[0] = Button('Strike', WIDTH // 2 - 100, HEIGHT // 2 - 50, (255, 0, 0))
            buttons.append(Button('Split', WIDTH // 2 + 100, HEIGHT // 2 - 50, (0, 255, 0)))

        for btn in buttons:
            btn.draw(WIN)

        pygame.display.update()

        result_list = [None]
        input_thread = threading.Thread(target=get_input, args=(prompt,result_list))
        input_thread.start()

        while input_thread.is_alive():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    input_thread.join(timeout=0.1)
                    if input_thread.is_alive():
                        os._exit(0)
                    break
            time.sleep(0.1)

        action = result_list[0]

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
    

        
    pygame.quit()


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

# def main():
#     hands = {
#         'Player 1': {'left': 1, 'right': 1},
#         'Player 2': {'left': 1, 'right': 1}
#     }

#     current_player = 'Player 1'
#     while not game_over(hands):
#         os.system('clear')

#         display_hands("Player 1", hands["Player 1"]['left'], hands["Player 1"]['right'])
#         display_hands("Player 2", hands["Player 2"]['left'], hands["Player 2"]['right'])

#         cant_split = False

#         if hands[current_player]['left'] == hands[current_player]['right']:
#             cant_split = True
        
#         if cant_split:
#             action = input(f"{current_player}, choose an action (strike) (you can't split because you have equal values on both hands): ").strip().lower()
#         else:
#             action = input(f"{current_player}, choose an action (strike/split): ").strip().lower()

#         if action == 'strike':
#             if current_player == 'Player 1':
#                 strike('Player 1', 'Player 2', hands)
#             else:
#                 strike('Player 2', 'Player 1', hands)
#         elif action == 'split' and not cant_split:
#             split(current_player, hands)
#         else:
#             print("Invalid action. Please choose 'strike' or 'split'.")
#             continue

#         # Switch to the other player
#         current_player = 'Player 1' if current_player == 'Player 2' else 'Player 2'

#     print(f"{current_player} loses! Game over.")

if __name__ == "__main__":
    main()
