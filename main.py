import pygame
import time
import random
import os
import threading
import sys

false = False
true = True

pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Chopsticks AI")


def get_input(prompt, result_list):
    result_list[0] = input(prompt).strip().lower()


def draw(hands, current_player, prompt):
    WIN.fill((255, 255, 255))

    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render(f"{current_player}'s turn", True, (0, 0, 0))
    textRect = text.get_rect()

    textRect.center = (WIDTH // 2, HEIGHT // 2 - 100)



    font2 = pygame.font.Font('freesansbold.ttf', 12)
    text = font2.render(prompt, True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2 + 100)
    WIN.blit(text, textRect)



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

    clock = pygame.time.Clock()


    while run and not game_over(hands):
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        os.system('clear')

        display_hands("Player 1", hands["Player 1"]['left'], hands["Player 1"]['right'])
        display_hands("Player 2", hands["Player 2"]['left'], hands["Player 2"]['right'])

        cant_split = False

        if hands[current_player]['left'] == hands[current_player]['right']:
            cant_split = True
        
        buttons = [None]

        if cant_split:
            prompt = f"{current_player}, choose an action (strike) (you can't split because you have equal values on both hands): "
            buttons[0] = Button('strike', WIDTH // 2 - 100, HEIGHT // 2 - 50, (255, 0, 0))
        else:
            prompt = f"{current_player}, choose an action (strike/split): "
            buttons[0] = Button('strike', WIDTH // 2 - 200, HEIGHT // 2 - 50, (255, 0, 0))
            buttons.append(Button('split', WIDTH // 2 , HEIGHT // 2 - 50, (0, 255, 0)))


        draw(hands, current_player, prompt)
        

        for btn in buttons:
            btn.draw(WIN)

        pygame.display.update()

        selectedChoice = false
        action = None
    

        while not selectedChoice:
            # print("bhere", selectedChoice)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in buttons:
                        if btn.click(pos):
                            action = btn.text
                            selectedChoice = true


        


        # result_list = [None]
        # input_thread = threading.Thread(target=get_input, args=(prompt,result_list))
        # input_thread.start()

        # while input_thread.is_alive():
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             run = False
        #             input_thread.join(timeout=0.1)
        #             if input_thread.is_alive():
        #                 os._exit(0)
        #             break
        #     time.sleep(0.1)


        



        # action = result_list[0]

        if action == 'strike':
            if current_player == 'Player 1':
                strike('Player 1', 'Player 2', hands)
            else:
                strike('Player 2', 'Player 1', hands)
        elif action == 'split' and not cant_split:
            split(current_player, hands)
        # else:
        #     print("Invalid action. Please choose 'strike' or 'split'.")
        #     continue

        # Switch to the other player
        current_player = 'Player 1' if current_player == 'Player 2' else 'Player 2'

    print(f"{current_player} loses! Game over.")
    

        
    pygame.quit()


def display_hands(player, left_hand, right_hand):
    print(f"{player}'s hands: Left: {left_hand} | Right: {right_hand}\n")

def strike(attacker, defender, hands):


    btns = [None]
    btns[0] = (Button('left', WIDTH // 2 - 200, HEIGHT // 2 - 50, (255, 0, 0)))
    btns.append(Button('right', WIDTH // 2, HEIGHT // 2 - 50, (0, 0, 255)))
        


    draw(hands, attacker, "Choose a hand to attack with: ")

    for btn in btns:
        btn.draw(WIN)

    pygame.display.update()

    # Ensure the strike is valid
    validAttacker = False
    while not validAttacker:

        chosen = false

        while not chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in btns:
                        if btn.click(pos):
                            attack_hand = btn.text
                            chosen = true

        # attack_hand = input(f"{attacker}, choose a hand to attack with (left/right): ").strip().lower()
        if hands[attacker][attack_hand] == 0:
            print("Invalid strike. Please try again.")
        else:
            validAttacker = True



    draw(hands, attacker, "Choose a hand to attack: ")

    for btn in btns:
        btn.draw(WIN)

    pygame.display.update()

    validAttacked = False
    while not validAttacked:

        chosen = false

        while not chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in btns:
                        if btn.click(pos):
                            attacked_hand = btn.text
                            chosen = true

        # attacked_hand = input(f"{attacker}, choose a hand to attack (left/right): ").strip().lower()
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



    user_text = ''

    input_rect = pygame.Rect(200,200,140,32)

    color_active = pygame.Color('lightskyblue3')
    
    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    
    active = False


    # Ensure the split is valid
    total = hands[player]['left'] + hands[player]['right']
    while True:
        notEntered = True
        while notEntered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = true
                    else:
                        active = false

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        notEntered = False
                    else:
                        user_text += event.unicode
            
            if active:
                color = color_active
            else:
                color = color_passive

            draw(hands, player, "Enter the number of fingers for the left hand (total fingers = " + str(total) + "): ")
            pygame.draw.rect(WIN, color, input_rect)

            text_surface = pygame.font.Font(None, 32).render(user_text, True, (0,0,0))

            WIN.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

            input_rect.w = max(100, text_surface.get_width() + 10)

            pygame.display.flip()

        # left = int(input(f"Enter the number of fingers for the left hand (total fingers = {total}): "))
        left = int(user_text)
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

if __name__ == "__main__":
    main()
