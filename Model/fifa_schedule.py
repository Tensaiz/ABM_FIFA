import random
from mesa.time import RandomActivation

from manager import Manager
from utility import match_outcome

class RandomActivationFIFA(RandomActivation):
    """"
    The scheduler for the FIFA simulation ABM
    It schedules the activation of the manager and the players

    It starts with a few assembly rounds for the managers and players where managers form teams
    Afterwards the match scheduling should start where managers in pools play matches with each other
    Every season the managers get the chance to trade and buy players, whereas players can accept or reject these offers

    TODO:
        - Incorporate aging
    """
    def __init__(self, model):
        super().__init__(model)
        self.managers = []
        self.incomplete_teams = []
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

        self.increment_time()

    def step(self):
        self.shuffle_agents()

        # Play one season of matches
        self.play_matches()

        for manager in self.managers:
            manager.step()
        
        for player in self.players:
            player.step()

        self.get_incomplete_teams()
        self.shuffle_agents()

        for manager in set(self.incomplete_teams):
            manager.recovery_step()
            manager.assets += manager.earnings

        self.incomplete_teams = []

        self.increment_time()


    def play_matches(self):
        '''
        Let every manager in each pool play against the other managers in that pool twice
        '''
        for pool in self.model.pools:
            for manager in pool:
                for manager_2 in pool:
                    if manager == manager_2:
                        continue
                    self.play_match(manager, manager_2)

    def play_match(self, manager_1, manager_2):
        outcome = match_outcome(manager_1, manager_2)
        if outcome == 0:
            # Manager one won
            manager_1.game_history.append(0)
            manager_1.reputation += 1
            manager_2.game_history.append(1)
            manager_2.reputation -= 1
        elif outcome == 1:
            # Manager two won
            manager_1.game_history.append(1)
            manager_1.reputation -= 1
            manager_2.game_history.append(0)
            manager_2.reputation += 1
        elif outcome == 2:
            # Tie
            manager_1.game_history.append(2)
            manager_2.game_history.append(2)

    def get_incomplete_teams(self):
        for manager in self.managers:
            incomplete = False
            for _, player in manager.team.items():
                if player == None:
                    incomplete = True
            if incomplete:
                self.incomplete_teams.append(manager)

    def shuffle_agents(self):
        random.shuffle(self.managers)
        random.shuffle(self.players)

    def increment_time(self):
        self.steps += 1
        self.time += 1