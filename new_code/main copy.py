import pygame
import time
import random
import os
import threading
import sys

import gym
from gym import spaces
import pygame
import numpy as np
import time
import io
import sys

from ChopsticksEnv import ChopsticksEnv

from QLearningAgent import QLearningAgent
from QLearningAgent import RandomAgent

false = False
true = True

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
            player = 'Human'
            height = 1.2
            increment = 0.1
            pWidth = 1.3
        else:
            player = 'AI'
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
        if self.x < WIDTH // 2:
            text = font.render("(A)", 1, (0, 0, 255))
            win.blit(text, (self.x + (self.width // 2 - text.get_width() // 2),
                        self.y + (self.height // 2 - text.get_height() // 2) - 100))
            
        elif self.x >=  WIDTH // 2:
            text = font.render("(L)", 1, (0, 0, 255))
            win.blit(text, (self.x + (self.width // 2 - text.get_width() // 2),
                        self.y + (self.height // 2 - text.get_height() // 2) - 100))

    def click(self,pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        attack_hand = "left"
                        chosen = true
                    if event.key == pygame.K_l:
                        attack_hand = "right"
                        chosen = true


        # attack_hand = input(f"{attacker}, choose a hand to attack with (left/right): ").strip().lower()
        if hands[attacker][attack_hand] == 0:
            print("Invalid strike. Please try again.")

            font2 = pygame.font.Font('freesansbold.ttf', 12)
            text = font2.render("Invalid strike. Please try again", True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2 - 75)
            WIN.blit(text, textRect)
            pygame.display.update()

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        attacked_hand = "left"
                        chosen = true
                    if event.key == pygame.K_l:
                        attacked_hand = "right"
                        chosen = true

        # attacked_hand = input(f"{attacker}, choose a hand to attack (left/right): ").strip().lower()
        if hands[defender][attacked_hand] == 0:
            print("Invalid strike. Please try again.")

            font2 = pygame.font.Font('freesansbold.ttf', 12)
            text = font2.render("Invalid strike. Please try again", True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2 - 100)
            WIN.blit(text, textRect)
            pygame.display.update()

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

    clock = pygame.time.Clock()


    user_text = ''

    input_rect = pygame.Rect(WIDTH // 2 - 50,HEIGHT // 2,140,32)

    color_active = pygame.Color('lightskyblue3')
    
    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    
    active = False

    invalidInput = False

    preLeft = hands[player]['left']
    preRight = hands[player]['right']

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

            if invalidInput:
                font2 = pygame.font.Font('freesansbold.ttf', 12)
                text = font2.render("Invalid split. Please try again", True, (255, 0, 0))
                textRect = text.get_rect()
                textRect.center = (WIDTH // 2, HEIGHT // 2 - 100)
                WIN.blit(text, textRect)
                pygame.display.update()

            pygame.display.flip()

            clock.tick(10)

        # left = int(input(f"Enter the number of fingers for the left hand (total fingers = {total}): "))
        left = int(user_text)
        right = total - left
        if preLeft == left and preRight == right:
            print("Invalid split. Please try again.")
            invalidInput = True
            continue
        if preLeft == 0 or preRight == 0:
            if left == preRight and right == preLeft:
                print("Invalid split. Please try again.")
                invalidInput = True
                continue
        if 0 <= left <= 4 and 0 <= right <= 4:
            invalidInput = False
            break
        print("Invalid split. Please try again.")
        invalidInput = True
        


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

def old_train_two_agents(env, player_agent, opponent_agent, num_episodes=1000):
    initial_epsilon = 1.0
    epsilon_decay = 0.9995
    min_epsilon = 0.2

    for episode in range(num_episodes):
        # Adjust exploration rate
        player_agent.epsilon = max(min_epsilon, initial_epsilon * (epsilon_decay ** episode))
        opponent_agent.epsilon = max(min_epsilon, initial_epsilon * (epsilon_decay ** episode))
       

        state = env.reset()
        done = False
        current_agent = player_agent  # Start with the player agent

        while not done:
            action = current_agent.choose_action(state, env) 

            old_state = state.copy()
            next_state, reward, done, _ = env.step(action)


            #print("the state is ", old_state)
            if reward == 1:
                other_player = opponent_agent if current_agent == player_agent else player_agent

            current_agent.learn(old_state, action, reward, next_state)
            state = next_state

            if reward == 1:
                other_player.learn(env.logs[-3]['state'], env.logs[-2]['action'], -reward, old_state)

            # Switch agents
            current_agent = opponent_agent if current_agent == player_agent else player_agent


def train_two_agents(env, player_agent, opponent_agent, num_episodes=1000):
    initial_epsilon = 1.0
    epsilon_decay = 0.9995
    min_epsilon = 0.2

    for episode in range(num_episodes):
        # Adjust exploration rate
        player_agent.epsilon = max(min_epsilon, initial_epsilon * (epsilon_decay ** episode))
        opponent_agent.epsilon = max(min_epsilon, initial_epsilon * (epsilon_decay ** episode))
       
        print("--------------Start of new episode------------------")

        state = env.reset()
        print("state is reset here ", state)
        done = False
        current_agent = player_agent  # Start with the player agent

        hands = {
        'Human': {'left': 1, 'right': 1},
        'AI': {'left': 1, 'right': 1}
        }

        current_player = 'Human'
        
        clock = pygame.time.Clock()

        while not done and not game_over(hands):
            clock.tick(60)

            if current_player == 'Human':
                hands['Human']['left'] = state[0]
                hands['Human']['right'] = state[1]
                hands['AI']['left'] = state[2]
                hands['AI']['right'] = state[3]


            else:
                state[0] = hands['Human']['left']
                state[1] = hands['Human']['right']
                state[2] = hands['AI']['left']
                state[3] = hands['AI']['right']

                env.logs.append({
                    'state': state.copy(),
                })

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #os.system('clear')

            display_hands("Human", hands["Human"]['left'], hands["Human"]['right'])
            display_hands("AI", hands["AI"]['left'], hands["AI"]['right'])

            if current_player == 'Human':
                cant_split = False
                
                if (hands[current_player]['left'] == 0 or hands[current_player]['right'] == 0) and (hands[current_player]['left'] == 1 or hands[current_player]['right'] == 1):
                    cant_split = True
                
                buttons = [None]

                if cant_split:
                    prompt = f"{current_player}, choose an action (strike) (you can't split): "
                    buttons[0] = Button('strike', WIDTH // 2 - 100, HEIGHT // 2 - 50, (255, 0, 0))
                else:
                    prompt = f"{current_player}, choose an action (strike/split): "
                    buttons[0] = Button('strike', WIDTH // 2 - 200, HEIGHT // 2 - 50, (255, 0, 0))
                    buttons.append(Button('split', WIDTH // 2 , HEIGHT // 2 - 50, (0, 255, 0)))

            if current_player == 'AI':
                prompt = "The AI is deciding"


            draw(hands, current_player, prompt)

            if current_player == 'Human':
                for btn in buttons:
                    btn.draw(WIN)

            pygame.display.update()

            if current_player == 'Human':

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

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_a:
                                action = 'strike'
                                selectedChoice = true
                            if event.key == pygame.K_l:
                                action = 'split'
                                selectedChoice = true

                if action == 'strike':
                    strike('Human', 'AI', hands)
                elif action == 'split' and not cant_split:
                    split(current_player, hands)





            # HOW CAN THE AI PREDICT SPLITS FOR FUTURE MOVES TO PREPARE FOR???

            if current_player == 'AI':
                print("now the current player is ", env.current_player)
                action = player_agent.choose_action(state, env) 
                print("action chosen ", action)

                old_state = state.copy()
                next_state, reward, done, _ = env.step(action)
                print("old state ", old_state)
                print("new state ", next_state)
                print("reward ", reward)

                print("abt to get fed into learn")
                player_agent.learn(old_state, action, reward, next_state)
                opponent_agent.learn(old_state, action, reward, next_state)
                state = next_state

            current_player = 'AI' if current_player == 'Human' else 'Human'

        if game_over(hands) and not done:
            player_agent.learn(env.logs[-2]['state'], env.logs[-1]['action'], -1, env.logs[-1]['state'])
            opponent_agent.learn(env.logs[-2]['state'], env.logs[-1]['action'], -1, env.logs[-1]['state'])

        print("Game finished!")

    pygame.quit()


def test_two_agents(env, player_agent, opponent_agent, num_episodes=100):
    total_wins = 0

    # Disable exploration
    player_agent.epsilon = 0
    opponent_agent.epsilon = 0

    for episode in range(num_episodes):
        state = env.reset()
        done = False
        starting_player = player_agent  # Track the starting player for each episode
        current_agent = starting_player

        while not done:
            env.render()  # Visualize the game state
            # time.sleep(2)
            print("choosing a new action")
            action = current_agent.choose_action(state, env)
            next_state, reward, done, _ = env.step(action)
            state = next_state

            if done:
                print(f"Episode {episode + 1}")
                for log in env.logs:
                    print(f"State: {log['state']}, Action: {log['action']}, Player: {'Player' if log['current_player'] == 0 else 'Opponent'}")
                print("--------------------------")

                env.logs.clear()  # Clear logs for the next game
                    
                # Check which agent made the last move
                last_moving_agent = current_agent
                
                if (reward == 1 and last_moving_agent == player_agent):
                    total_wins += 1



            # Switch agents
            current_agent = opponent_agent if current_agent == player_agent else player_agent

    win_rate = total_wins / num_episodes
    return win_rate


file_name = 'q_table_player.npy'

if os.path.exists(file_name):
    Q = np.load(file_name, allow_pickle=True).item()

else:
    Q = {}

env = ChopsticksEnv()



random_agent = RandomAgent(env.action_space)





player_agent = QLearningAgent(env.action_space, learning_rate=0.7, q_table=Q)
opponent_agent = QLearningAgent(env.action_space, learning_rate=0.7, q_table=Q)

print("player q_table", player_agent.q_table)
print("opponent q_table", opponent_agent.q_table)

print("-------------------")
print("training main agents on random agents...")
print("-------------------")

old_stdout = sys.stdout
sys.stdout = io.StringIO()

try:
    old_train_two_agents(env, player_agent, random_agent, num_episodes=1000)
    old_train_two_agents(env, opponent_agent, random_agent, num_episodes=1000)

    old_train_two_agents(env, player_agent, opponent_agent, num_episodes=50000)
finally:
    sys.stdout = old_stdout
print("player q_table", player_agent.q_table)
print("opponent q_table", opponent_agent.q_table)

#random_agent = RandomAgent(env.action_space)
#train_two_agents(env, player_agent, random_agent, num_episodes=5000)

#train_two_agents(env, player_agent, opponent_agent, num_episodes=50000)

pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Chopsticks AI")
print("getting started")
train_two_agents(env, player_agent, opponent_agent, num_episodes=10)


#win_rate = test_two_agents(env, player_agent, opponent_agent, num_episodes=1000)
#print(f"Player agent's win rate against opponent agent: {win_rate * 100:.2f}%")

#print("Sample of player's Q-values:")
count = 0
max_keys = 100
for key in list(player_agent.q_table.keys()):
    if player_agent.q_table[key] > 0:
        print(key, player_agent.q_table[key])
        count += 1
    if count == max_keys:
        break
print('done')

count = 0
for key in list(opponent_agent.q_table.keys()):
    if opponent_agent.q_table[key] > 0:
        print(key, opponent_agent.q_table[key])
        count += 1
        if count == max_keys:
            break
print('done')
#print(f"Players q table {player_agent.q_table} and opponent q table {opponent_agent.q_table}")

print("player q_table", player_agent.q_table)
print("opponent q_table", opponent_agent.q_table)

np.save('q_table_player.npy', player_agent.q_table)