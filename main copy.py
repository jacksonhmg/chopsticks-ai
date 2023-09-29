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

false = False
true = True

pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Chopsticks AI")


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
            text = font.render("(L)", 1, (0, 0, 255))
            win.blit(text, (self.x + (self.width // 2 - text.get_width() // 2),
                        self.y + (self.height // 2 - text.get_height() // 2) - 100))
            
        elif self.x >=  WIDTH // 2:
            text = font.render("(R)", 1, (0, 0, 255))
            win.blit(text, (self.x + (self.width // 2 - text.get_width() // 2),
                        self.y + (self.height // 2 - text.get_height() // 2) - 100))

    def click(self,pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def main():
    hands = {
        'Human': {'left': 1, 'right': 1},
        'AI': {'left': 1, 'right': 1}
    }

    current_player = 'Human'

    run = True

    clock = pygame.time.Clock()


    while run and not game_over(hands):
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        os.system('clear')

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

            if action == 'strike':
                if current_player == 'Human':
                    strike('Human', 'AI', hands)
                else:
                    strike('AI', 'Human', hands)
            elif action == 'split' and not cant_split:
                split(current_player, hands)

        current_player = 'Human' if current_player == 'AI' else 'AI'

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        attack_hand = "left"
                        chosen = true
                    if event.key == pygame.K_r:
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
                    if event.key == pygame.K_l:
                        attacked_hand = "left"
                        chosen = true
                    if event.key == pygame.K_r:
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









class ChopsticksEnv(gym.Env):
    def __init__(self):
        super(ChopsticksEnv, self).__init__()

        # Define action and observation spaces
        # We'll handle the dynamic nature of the split actions in the step function
        self.action_space = spaces.Discrete(14)  # 4 striking actions + 10 potential split actions

        # Observation space remains the same
        self.observation_space = spaces.Tuple([spaces.Discrete(5) for _ in range(4)])

        # Initialize state
        self.reset()

        self.current_player = 0

    def reset(self):
        self.state = [1, 1, 1, 1]
        self.current_player = 0
        self.logs = []
        return self.state

    def valid_splits(self, total, original_hand):
        # Generate all valid splits for a given total
        splits = [[i, total-i] for i in range(total + 1)]  # This will include [x, 0] combinations        

        # Filter out splits with a number greater than 4
        splits = [s for s in splits if all(val <= 4 for val in s)]

        invalid_splits = [[0, 1], [1, 0], [4, 4], original_hand]
        return [s for s in splits if s not in invalid_splits]

    def step(self, action):
        print("action in step is ", action)
        # Extract active and passive hands based on current player
        active_hand = self.state[2:]
        print("active_hand ", active_hand)
        passive_hand = self.state[:2]
        print("passive_hand ", passive_hand)

        # Handle striking actions
        if 0 <= action <= 3:
            if active_hand[action // 2] == 0 or passive_hand[action % 2] == 0:
                print("invalid strike, returning -1 for reward")
                return self.state, -1, True, {'reason': 'Invalid strike'}  # Invalid action
            passive_hand[action % 2] += active_hand[action // 2]
            if passive_hand[action % 2] >= 5:
                passive_hand[action % 2] = 0

        # Handle splitting actions
        else:
            total_fingers = sum(active_hand)
            splits = self.valid_splits(total_fingers, active_hand)
            print("splits ", splits)
            split_action_index = action - 4
            print("split action index ", split_action_index)
            if split_action_index < len(splits): # uhhhhh
                active_hand[:] = splits[split_action_index]
                print("active hand is now ", active_hand)
            else:
                print("invalid split, returning -1 for reward")
                return self.state, -1, True, {'reason': 'Invalid split'}  # Invalid action

        # Update the state based on current player

        self.state[:2] = passive_hand
        self.state[2:] = active_hand

        # Check for game end
        done = all(f == 0 for f in self.state[:2]) or all(f == 0 for f in self.state[2:])
        #print("done ", done)
        
        #print("self.current_player == 1 so returning reward = 1 if all(f == 0 for f in self.state[:2]) else -1 if all(f == 0 for f in self.state[2:]) else 0")
        reward = 1 if all(f == 0 for f in self.state[:2]) else -1 if all(f == 0 for f in self.state[2:]) else 0

        #if not done:
        #    reward = -0.01
        print("reward ", reward)

        print("state ", self.state)
        #print("action ", action)

        print("im boutta append")
        self.logs.append({
            'state': self.state.copy(),
            'action': action,
            'current_player': self.current_player
        })

        #print("leaving step")

        return self.state, reward, done, {}


    def render(self, mode='human'):
        # Initialize pygame if not done already
        if not pygame.get_init():
            pygame.init()
            self.screen = pygame.display.set_mode((400, 400))
            self.font = pygame.font.SysFont(None, 36)

        # Clear the screen
        self.screen.fill((255, 255, 255))

        # Draw the game state
        player_text = f"Player: {self.state[0]} | {self.state[1]}"
        opponent_text = f"Opponent: {self.state[2]} | {self.state[3]}"
        
        player_surface = self.font.render(player_text, True, (0, 0, 0))
        opponent_surface = self.font.render(opponent_text, True, (0, 0, 0))
        
        self.screen.blit(player_surface, (50, 150))
        self.screen.blit(opponent_surface, (50, 100))

        pygame.display.flip()

    def close(self):
        pygame.quit()


class QLearningAgent:
    def __init__(self, action_space, learning_rate=0.9, discount_factor=0.9, exploration_rate=0.1):
        self.q_table = {}
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.action_space = action_space

    def get_q_value(self, state, action):
        return self.q_table.get((tuple(state), action), 0.0)


    def choose_action(self, state, env):
        
        active_hand = state[2:]
        passive_hand = state[:2]

        validChoice = False
        idx = 0
        while not validChoice:
            if np.random.uniform(0, 1) < self.epsilon: #ADD A THING SO THAT IF THEY CHOOSE q_values in first iteration, then they find the next best q_value action instead of potentially random
                print("we're exploring")
                choice = self.action_space.sample()  # Exploration
            else: #ADD A THING SO THAT IF THEY CHOOSE q_values in first iteration, then they find the next best q_value action instead of potentially random
                # Exploitation
                print("we're getting a q value")
                q_values = [self.get_q_value(state, action) for action in range(self.action_space.n)]
                #print("q values ", q_values)
                sorted_indices = np.argsort(q_values)[::-1]
                choice = sorted_indices[idx]
                idx += 1
            
            #print("choice ", choice)

            # Check if the action is valid
            if choice <= 3:
                if active_hand[choice // 2] == 0 or passive_hand[choice % 2] == 0:
                    continue
            else:
                total_fingers = sum(active_hand)
                splits = env.valid_splits(total_fingers, active_hand)
                if choice - 4 >= len(splits):
                    continue

            #print("valid choice")
            validChoice = True

        return choice

            



    def learn(self, state, action, reward, next_state):
        print("state in learn ", state)
        print("action in learn ", action)
        print("reward in learn ", reward)
        print("next state in learn ", next_state)
        old_value = self.get_q_value(state, action)
        print("old value ", old_value)
        future_max_value = max([self.get_q_value(next_state, a) for a in range(self.action_space.n)])
        print("future max value ", future_max_value)
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * future_max_value)
        print("new value ", new_value)

        self.q_table[(tuple(state), action)] = new_value



        
    # def choose_action2(self, state):
    #     action = self.action_space.sample() if np.random.uniform(0, 1) < self.epsilon else np.argmax([self.get_q_value(state, a) for a in range(self.action_space.n)])
    #     # Introduce noise
    #     if np.random.uniform(0, 1) < 0.05:
    #         action = self.action_space.sample()
    #     return action


class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def choose_action(self, state):
        return self.action_space.sample()

    def learn(self, *args):
        pass  # Random agent doesn't learn


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
                            if event.key == pygame.K_l:
                                action = 'strike'
                                selectedChoice = true
                            if event.key == pygame.K_r:
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





env = ChopsticksEnv()

player_agent = QLearningAgent(env.action_space, learning_rate=0.7)
opponent_agent = QLearningAgent(env.action_space, learning_rate=0.7)

#random_agent = RandomAgent(env.action_space)
#train_two_agents(env, player_agent, random_agent, num_episodes=5000)

#train_two_agents(env, player_agent, opponent_agent, num_episodes=50000)
train_two_agents(env, player_agent, opponent_agent, num_episodes=50)


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