import random
from mesa.time import RandomActivation

from manager import Manager

class RandomActivationFIFA(RandomActivation):
    '''
    The scheduler for the FIFA simulation ABM
    It schedules the activation of the manager and the players

    It starts with a few assembly rounds for the managers and players where managers form teams
    Afterwards the match scheduling should start where managers in pools play matches with each other
    Every season the managers get the chance to trade and buy players, whereas players can accept or reject these offers

    TODO:
        - Incorporate aging
    '''
    def __init__(self, model):
        super().__init__(model)
        self.managers = []
        self.players = []

    def add_agent(self, agent):
        if isinstance(agent, Manager):
            self.managers.append(agent)
        else:
            self.players.append(agent)




    def assemble_step(self):
        self.shuffle_agents()
        for manager in self.managers:
            manager.assemble_step()
        
        for player in self.players:
            player.assemble_step()

        self.increment_time()

    def step(self):
        self.shuffle_agents()

        # Play one season of matches
        self.play_matches()

        for manager in self.managers:
            manager.step()
        
        for player in self.players:
            player.step()

        self.increment_time()


    def play_matches(self):
        pass

    def shuffle_agents(self):
        random.shuffle(self.managers)
        random.shuffle(self.players)

    def increment_time(self):
        self.steps += 1
        self.time += 1