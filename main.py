import gym
from DeepQNetwork import Agent
import numpy as np
from gym import wrappers
import pickle

# configuration zone
SESSION_NAME = ""
MODEL_SAVE_LOCATION = "models/"

if __name__ == "__main__":
    # test implementation using OpenAI GYM.

    env = gym.make("SpaceInvaders-v0")

    # Start Learning
    # '''
    agent = Agent(
        discountRate=0.99,
        epsilon=0.00,
        epsilonFinal=0.00,
        batchSize=64,
        actions=4,
        inputDimension=[8],
        learningRate=0.003
    )
    # '''

    # Continue Learning or Transferred Learning
    #agent = Agent.load(MODEL_SAVE_LOCATION+"latest.model")

    scores = []
    epsilonHistory = []
    gamePlays = 500
    currentScore = 0

    for i in range(gamePlays):
        if i % 10 == 0 and i > 0:
            averageScore = np.mean(scores[max(0, i-10):(i+1)])
            print("GamePlay: ", i, " / Score:", currentScore,
                  "Average Score: ", averageScore, "epsilon: ", agent.epsilon)
            agent.save(MODEL_SAVE_LOCATION+"latest.model")
        else:
            print("GamePlay: ", i, " / Score:", currentScore)

        currentScore = 0
        epsilonHistory.append(agent.epsilon)
        observation = env.reset()

        isGameover = False

        while not isGameover:
            env.render()
            action = agent.decideAction(observation)
            newObservation, reward, isGameover, info = env.step(action)
            currentScore += reward
            agent.storeTransition(observation, action,
                                  reward, newObservation, isGameover)
            agent.learn()

            observation = newObservation

        scores.append(currentScore)

env.close()
