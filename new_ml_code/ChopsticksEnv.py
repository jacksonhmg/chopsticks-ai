import gym
from gym import spaces
import pygame

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