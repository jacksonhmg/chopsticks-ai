import os
import numpy as np
from ChopsticksEnv import ChopsticksEnv
from QLearningAgent import QLearningAgent
import sqlite3
import pickle

conn = sqlite3.connect('agents.db', check_same_thread=False)
cursor = conn.cursor()

# Create a table to store agents
cursor.execute('''
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY,
    agent BLOB,
    env BLOB
)
''')
conn.commit()

false = False
true = True

def game_over(state):
    result = False

    if (state[0] and state[1]) == 0 or (state[2] and state[3]) == 0:
        result = True
    else:
        return True

    return result


def return_move(state, id):
    cursor.execute("SELECT agent, env FROM agents WHERE id=?", (id,))
    row = cursor.fetchone()
    if row:
        retrieved_serialized_agent, retrieved_serialized_env = row

        # Deserialize the agent object
        agent = pickle.loads(retrieved_serialized_agent)

        # Deserialize the environment object
        env = pickle.loads(retrieved_serialized_env)

    env.logs.append({
        'state': state.copy(),
    })

    if game_over(state) and not done:
        agent.learn(env.logs[-3]['state'], env.logs[-2]['action'], -1, env.logs[-2]['state'])
        env.logs.clear()
        return [1,1,1,1]

    action = agent.choose_action(state, env)
    old_state = state.copy()
    next_state, reward, done, _ = env.step(action)
    agent.learn(old_state, action, reward, next_state)
    state = next_state

    if done:
        env.logs.clear()

    return state


def create_agent_and_env():
    if os.path.exists('q_table_player.npy'):
        Q = np.load('q_table_player.npy', allow_pickle=True).item()

    else:
        Q = {}

    env = ChopsticksEnv()

    player_agent = QLearningAgent(env.action_space, learning_rate=0.7, q_table=Q)

    serialized_agent = pickle.dumps(player_agent)

    serialized_env = pickle.dumps(env)

    cursor.execute("INSERT INTO agents (agent, env) VALUES (?, ?)", (serialized_agent, serialized_env))
    conn.commit()

    last_id = cursor.lastrowid

    return last_id



# Close the database connection
conn.close()