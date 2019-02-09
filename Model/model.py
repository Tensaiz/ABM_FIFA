import numpy as np
import pandas as pd
import time

# mesa
from mesa import Model
from mesa.datacollection import DataCollector

# Custom classes
from fifa_schedule import RandomActivationFIFA
from player import Player
from manager import Manager
import managerStrategy
import utility

class FIFA_Simulation(Model):
    """
    The main model class for the FIFA agent based model simulation.

    This class inherits the model class from the mesa library.
    It creates manager agents and player agents, who both try to maximise their utility.
    The agents try to create optimal teams with the amount of money they have using different strategies.
    The players try to receive the most money and play for the most reputable managers.

    Args:
        assemble_rounds (int): Amount of rounds it should take for all teams to form
        seasons (int): Amount of seasons to simulate
        n_pools (int): The amount of pools to use. Amount of managers is 18 times this number.
        n_players (int): The amount of players to use from the FIFA dataset. 0 can be used to select all players.
        player_stats (pandas dataframe): A FIFA dataset of players with all their corresponding stats
        money_distribution_type (int): The type of money distribution to use for the managers
            0 = normally distributed
            1 = uniformly distributed
            2 = exponentially distributed
            3 = constant
        money_distrbution_params (:obj: any): Required parameters for the money distribution used
        strategies (:list:`int`): A list with the different strategies
    """

    player_stats = None

    def __init__(self, assemble_rounds = 1, seasons = 15, n_pools = 1, n_players = 0, 
                 player_stats_ = pd.read_csv('../data.csv'), money_distribution_type = 0,
                 mu = 25000000, sigma = 2500000, earnings_ratio = (1/2), verbose=False, player_stats = None,
                 # market value, age, spi
                 match_weights = [0.25, 0.1, 1],
                 strategies = [managerStrategy.SimpleStrategy(), managerStrategy.EvenStrategy(), managerStrategy.UnforgivingStrategy()]):


        self.verbose = verbose
        # Set parameters
        self.money_distribution_params = {'mu': mu, 'sigma': sigma}
        self.earnings_ratio = earnings_ratio

        self.assemble_rounds = assemble_rounds
        self.seasons = seasons
        self.n_pools = n_pools
        self.n_managers = 18 * n_pools
        self.n_players = n_players

        self.match_weights = match_weights

        if FIFA_Simulation.player_stats is None:
            FIFA_Simulation.player_stats = utility.transform_fifa(player_stats_)

        self.money_distribution_type = money_distribution_type
        self.strategies = strategies

        self.managers = []
        self.pools = []
        self.players = []

        self.player_lookup = {}

        self.schedule = RandomActivationFIFA(self)
        self.datacollector = DataCollector(
            {"Manager assets": lambda m: m.schedule.get_manager_assets(),
             "Manager reputation": lambda m: m.schedule.get_manager_reputation()})
        self.running = True

        # Initialization functions
        self.init_agents()
        self.step_n = 0
        # Collect first time
        self.datacollector.collect(self)




    def init_agents(self):
        start_time = time.time()
        self.init_players()
        self.init_managers()
        if self.verbose:
            print("Initializing agents took --- %s seconds ---" % (time.time() - start_time))

    def init_players(self):
        if self.n_players == 0:
            self.n_players = len(FIFA_Simulation.player_stats)

        # Randomly select n_players amount of players
        self.chosen_player_stats = FIFA_Simulation.player_stats.sample(self.n_players)

        for i in range(self.n_players):
            p = Player(self.chosen_player_stats.iloc[i]['Name'], self, self.chosen_player_stats.iloc[i])
            # Associate player objects by their name in a map to find them efficiently
            self.player_lookup[p.name] = p
            self.players.append(p)
            self.schedule.add_agent(p)

    def init_managers(self):
        assets = self.get_assets()
        for i in range(self.n_managers):

            strategy = self.strategies[i % len(self.strategies)]
            strategy.model = self # Some strategies need access to model
            # Then they are able to make better decisions

            m = Manager(i, self, max(5000000, assets[i]), self.earnings_ratio, 0, strategy, 0)
            self.managers.append(m)
            self.schedule.add_agent(m)

    def get_assets(self):
        '''
        Return a list of n_managers length containing different assets for the managers depending on money_distribution_type
        '''
        if self.money_distribution_type == 0:
            assets = self.normal_asset_distribution(self.money_distribution_params['mu'], self.money_distribution_params['sigma'])
        elif self.money_distribution_type == 1:
            assets = self.uniform_asset_distribution(self.money_distribution_params['low'], self.money_distribution_params['high'])
        elif self.money_distribution_type == 2:
            assets = self.expo_asset_distribution(self.money_distribution_params['scale'])
        elif self.money_distribution_type == 3:
            assets = [self.money_distribution_params['constant']] * self.n_managers
        return assets


    def normal_asset_distribution(self, mu, sigma):
        '''
        Returns n_manager samples from a normal distribution

        Args:
            mu (float): The mean of the normal distribution
            sigma (float): The standard deviation
        '''
        return np.random.normal(mu, sigma, self.n_managers)

    def uniform_asset_distribution(self, low, high):
        '''
        Returns n_manager samples from a uniform distribution

        Args:
            low (float): The lower bound of the uniform distribution
            high (float): The upper bound of the uniform distribution
        '''
        return np.random.uniform(low, high, self.n_managers)

    def expo_asset_distribution(self, scale):
        '''
        Returns n_manager samples from a exponential distribution

        Args:
            scale (float): Scale parameter: 1/lambda
        '''
        return np.random.exponential(scale, self.n_managers)


    def create_pools(self):
        for i in range(self.n_pools):
            start = i * 18
            end = i * 18 + 18
            self.pools.append(self.managers[start : end])

    def print_results(self):
        print('Win / loss overview per manager after ' + str(self.seasons) +' seasons:')
        for manager in self.managers:
            print('Manager ' + str(manager.name) + ' started with: €' + str(manager.starting_assets) + '\nHas ' + str(manager.game_history.count(0)) + ' wins and ' + str(manager.game_history.count(1)) + ' losses. Has ' + str(manager.reputation) + ' reputation.') 
            print('Has ' + str(manager.assets) + ' funds remaining and used ' + type(manager.strategy).__name__ + '\n')

        results = sorted(self.managers, key=lambda manager: manager.game_history.count(0), reverse=True)
        for i, manager in enumerate(results):
            print('Manager ' + str(manager.name) + ' finished ' + str(i + 1) + 'th place and used strategy: ' + type(manager.strategy).__name__ + '\n')

    def run_model(self):
        """
        Runs the model after initialization by first assembling the teams and then playing the matches
        """
        self.running = True
        start_time = time.time()

        for _ in range(self.assemble_rounds):
            self.schedule.assemble_step()
        if self.verbose:
            print("Assembling teams took --- %s seconds ---" % (time.time() - start_time))

        self.create_pools()

        start_time = time.time()
        for _ in range(self.seasons):
            self.schedule.step()
            self.datacollector.collect(self)
        if self.verbose:
            print("Simulating seasons took --- %s seconds ---" % (time.time() - start_time))
            self.print_results()
        self.running = False

    # Mesa required step function
    def step(self):
        if self.step_n < self.assemble_rounds:
            self.schedule.assemble_step()
            self.step_n += 1
            return
        if self.step_n == self.assemble_rounds:
            self.create_pools()
        if self.step_n >= self.assemble_rounds:
            if self.step_n - self.assemble_rounds < self.seasons:
                self.schedule.step()
                self.datacollector.collect(self)
                self.step_n += 1
        if self.step_n == (self.assemble_rounds + self.seasons) - 1 and self.verbose:
            self.print_results()