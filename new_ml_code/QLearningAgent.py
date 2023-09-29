import numpy as np

class QLearningAgent:
    def __init__(self, action_space, learning_rate=0.9, discount_factor=0.9, exploration_rate=0.1, q_table={}):
        self.q_table = q_table
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

class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def choose_action(self, state, env):
        return self.action_space.sample()

    def learn(self, *args):
        pass  # Random agent doesn't learn


