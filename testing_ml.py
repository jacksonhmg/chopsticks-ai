import gym
from gym import spaces
import pygame
import numpy as np
import time


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
        active_hand = self.state[:2] if self.current_player == 0 else self.state[2:]
        print("active_hand ", active_hand)
        passive_hand = self.state[2:] if self.current_player == 0 else self.state[:2]
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
        if self.current_player == 0:
            self.state[:2] = active_hand
            self.state[2:] = passive_hand
        else:
            self.state[:2] = passive_hand
            self.state[2:] = active_hand

        # Check for game end
        done = all(f == 0 for f in self.state[:2]) or all(f == 0 for f in self.state[2:])
        #print("done ", done)
        if self.current_player == 0:
            #print("self.current_player == 0 so returning reward = 1 if all(f == 0 for f in self.state[2:]) else -1 if all(f == 0 for f in self.state[:2]) else 0")
            reward = 1 if all(f == 0 for f in self.state[2:]) else -1 if all(f == 0 for f in self.state[:2]) else 0 
        else:
            #print("self.current_player == 1 so returning reward = 1 if all(f == 0 for f in self.state[:2]) else -1 if all(f == 0 for f in self.state[2:]) else 0")
            reward = 1 if all(f == 0 for f in self.state[:2]) else -1 if all(f == 0 for f in self.state[2:]) else 0

        #if not done:
        #    reward = -0.01
        print("reward ", reward)

        print("state ", self.state)
        #print("action ", action)

        self.logs.append({
            'state': self.state.copy(),
            'action': action,
            'current_player': self.current_player
        })

        self.current_player = 1 - self.current_player

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
        if env.current_player == 0:
            active_hand = state[:2]
            passive_hand = state[2:]
        else:
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
        #print("state in learn ", state)
        #print("action in learn ", action)
        #print("reward in learn ", reward)
        #print("next state in learn ", next_state)
        old_value = self.get_q_value(state, action)
        #print("old value ", old_value)
        future_max_value = max([self.get_q_value(next_state, a) for a in range(self.action_space.n)])
        #print("future max value ", future_max_value)
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * future_max_value)
        #print("new value ", new_value)

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

        while not done:
            print("now the current player is ", env.current_player)
            action = current_agent.choose_action(state, env) 
            print("action chosen ", action)

            old_state = state.copy()
            next_state, reward, done, _ = env.step(action)
            print("old state ", old_state)
            print("new state ", next_state)
            print("reward ", reward)


            #print("the state is ", old_state)
            if reward == 1:
                other_player = opponent_agent if current_agent == player_agent else player_agent

            print("abt to get fed into learn")
            current_agent.learn(old_state, action, reward, next_state)
            state = next_state

            if reward == 1:
                print("the start state is ", env.logs[-3]['state'])
                print("the action is ", env.logs[-3]['action'])
                print("the reward is ", -reward)
                print("the end state is ", old_state)
                print("abt to learn for the other player")
                print("other player ", env.current_player)
                other_player.learn(env.logs[-3]['state'], env.logs[-2]['action'], -reward, old_state)

            # Switch agents
            current_agent = opponent_agent if current_agent == player_agent else player_agent




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