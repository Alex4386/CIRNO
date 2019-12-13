import gym
from DeepQNetwork import Agent
from utils import plotLearning
import numpy as np
from gym import wrappers

if __name__ == "__main__":
    # test implementation using OpenAI GYM.

    env = gym.make("LunarLander-v2")
    agent = Agent(
        discountRate=0.99,
        epsilon=1.00,
        batchSize=64,
        actions=4,
        inputDimension=[8],
        learningRate=0.003
    )

    scores = []
    epsilonHistory = []
    gamePlays = 500
    currentScore = 0

    for i in range(gamePlays):
        if i % 10 == 0 and i > 0:
            averageScore = np.mean(scores[max(0, i-10):(i+1)])
            print("GamePlay: ", i, " / Score:", currentScore,
                  "Average Score: ", averageScore, "epsilon: ", agent.epsilon)
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

    x = [1 for i in range(gamePlays)]
    fileName = "lunar-lander.png"

    plotLearning(x, scores, epsilonHistory, fileName)

env.close()
