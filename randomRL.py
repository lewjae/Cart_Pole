# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 21:24:19 2016

@author: Jae
Main alogrithm comes from:
http://kvfrans.com/simple-algoritms-for-solving-cartpole/

Just add "chekckng 100 conseccutive runs with reward >= 195" to ensure the problem solved 

It is a linear state feedback control with discrete output, 0 or 1.
Feedback gains are selected randomly, but it works surprisingly well.
It is used as a benchmark for Reforcement Learning future developemnt.

"""
import gym
import numpy as np

# One eposide up to 200 steps. It stops if the pole passes beyond +- degrees.
def run_episode(env, parameters, render=False):
    observation = env.reset()
    totalreward = 0
    
    # run 200 steps for one episode
    for _ in range(200):
        
        # if True, animate Cart-Pole
        if render == True:     
            env.render()
       
       # Define action as 0 or 1 upon u where u  = k1 x1 + k2 x2 + k3 x3 + k4 x4 
        action = 0 if np.matmul(parameters,observation) < 0 else 1   
        # Get state, reward, etc
        observation, reward, done, info = env.step(action)
        # compute total reward for one episode
        totalreward += reward
        
        # Stop if the pole passes beyond +- degrees
        if done:
            break
    return totalreward

# Start main program

#Start CartPole-v0    
env = gym.make('CartPole-v0') 

# Initialize a few parametes
counter = 0
env.monitor.start('exp1/') 

#  Find the best parameters by linear state feedback  randomly  upto 1000 episodes 
while counter < 1000 :
    counter += 1
    # Randomly select feedback gains:k1,k2,k3,k4
    parameters = np.random.rand(4) * 2 - 1     
    
    # Run one episode and compute reward for the episode
    reward = run_episode(env,parameters)        
    
    print "counter: ", counter, reward
    
    #  Pick the bestparams when rewards = 200
    if reward == 200:      
        bestparams = parameters
        print counter, reward, bestparams
        sum = 0
        myreward = 0
        mycount = 0
        
        #  Check if the problem is solved by running 100 consesctive 100 episodes.
        for episode in range(100): 
            myreward = run_episode(env,bestparams)
            sum += myreward
            
            # Count how times it scores more than 195
            if myreward >= 195:
                mycount += 1
        print "average reward for 100 episode: ", sum/100
        print "# of times reward >= 195: ", mycount
        
        # Check if it was 100 consecutive runs with reward >=195
        if mycount == 100:
    
            run_episode(env,bestparams,True)
            print "Problem solved!!!"
            print bestparams
            break
        # Continue to try  different parameters
        else:
            print "Try again with different best parameters"
            bestreward = 0
 
env.monitor.close()

     
    


