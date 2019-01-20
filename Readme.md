# Agent based FIFA simulation modelling

### Description

This agent based model simulates the behavior of manager and player agents in a FIFA environment.
The player agents are soccer players that have inherited stats from the FIFA2019 videogame.
The manager agents try to assemble teams and use different strategies to create a winning team by trading players with other managers, or buying players who are still available.
The players themselves try to find an optimal team for their own worth and earn as much money as they can, while playing for more reputable managers.

### Overview

This project contains multiple files belonging to the model and top-level running and visualization thereof.
- FIFA_ABM_Visualisation.ipynb: Ipython notebook exploring the FIFA2019 dataset
- data.csv: comma seperated values file containing all the FIFA2019 data for the players
- requirements.txt: containing the pip dependencies
- Model
    - run.py: wrapper file to run the model and set all the parameters from
    - model.py: the main model file that initializes the agents and scheduler and then progresses through time
    - player.py: the file containing the player agent class
    - manager.py: the file containing the manager agent class
    - fifa_schedule.py: the file that schedules the managers and players accordingly
    - utility.py: a utility file that calculates the probability of winning for one team versus another


### TODO:

#### Model

- Implement match system where pools are created that have 18 managers and each (manager) team plays each other 2 times

#### Player

- Needs a step function to determine what the player does every action,
- Afterwards it should choose between new teams if he is invited by a manager

#### Manager

- Create trading mechanism between manager agents
- Create team trading mechanics
- Create different optimisation strategies to assemble a team
- Fix negative assets for a manager when assembling team

#### Scheduler

- Incorporate aging


### Literature and sources

#### Dataset
https://www.kaggle.com/karangadiya/fifa19/home

#### Literature

http://www.worldcup-simulator.de/static/data/Dormagen_2014_World_Cup_Simulator_2014-05-29.pdf



### Authors:
- Mathijs Maijer
- Esra Solak
- Whitney Mok
- Kasper Nicholas
- Lukáš Kiss