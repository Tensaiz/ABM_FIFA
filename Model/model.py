import numpy as np
import time

# mesa
from mesa import Model
from mesa.datacollection import DataCollector

# Custom classes
from fifa_schedule import RandomActivationFIFA
from player import Player
from manager import Manager

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

    def __init__(self, assemble_rounds, seasons, n_pools, n_players, player_stats, money_distribution_type, money_distribution_params, strategies, verbose=True):
        self.verbose = verbose
        # Properties
        self.assemble_rounds = assemble_rounds
        self.seasons = seasons
        self.n_pools = n_pools
        self.n_managers = 18 * n_pools
        self.n_players = n_players
        self.player_stats = self.transform_fifa(player_stats)
        self.money_distrubtion_type = money_distribution_type
        self.money_distribution_params = money_distribution_params
        self.strategies = strategies

        self.managers = []
        self.pools = []
        self.players = []

        self.player_lookup = {}

        self.schedule = RandomActivationFIFA(self)

        # Initialization functions
        self.init_agents()

    def transform_fifa(self, player_stats):
        start_time = time.time()
        player_stats['Release Clause'] = player_stats['Release Clause'].apply(self.transform_to_number)
        player_stats['Value'] = player_stats['Value'].apply(self.transform_to_number)
        print("Transforming fifa data took --- %s seconds ---" % (time.time() - start_time))
        return player_stats

    def transform_to_number(self, release_clause):
        if isinstance(release_clause, float):
            return 0
        elif release_clause == '€0':
            return 0
        elif release_clause[-1] == 'K':
            multiplier = 1000
        elif release_clause[-1] == 'M':
            multiplier = 1000000
        return float(release_clause[1:-1]) * multiplier

    def init_agents(self):
        start_time = time.time()
        self.init_players()
        self.init_managers()
        print("Initializing agents took --- %s seconds ---" % (time.time() - start_time))

    def init_players(self):
        if self.n_players == 0:
            self.n_players = len(self.player_stats)

        # Randomly select n_players amount of players
        self.chosen_player_stats = self.player_stats.sample(self.n_players)

        for i in range(self.n_players):
            p = Player(self.chosen_player_stats.iloc[i]['Name'], self, self.chosen_player_stats.iloc[i])
            # Associate player objects by their name in a map to find them efficiently
            self.player_lookup[p.name] = p
            self.players.append(p)
            self.schedule.add_agent(p)

    def init_managers(self):
        assets = self.get_assets()
        for i in range(self.n_managers):
            m = Manager(i, self, assets[i], 0, 0, 0)
            self.managers.append(m)
            self.schedule.add_agent(m)

    def get_assets(self):
        '''
        Return a list of n_managers length containing different assets for the managers depending on money_distribution_type
        '''
        if self.money_distrubtion_type == 0:
            assets = self.normal_asset_distribution(self.money_distribution_params['mu'], self.money_distribution_params['sigma'])
        elif self.money_distrubtion_type == 1:
            assets = self.uniform_asset_distribution(self.money_distribution_params['low'], self.money_distribution_params['high'])
        elif self.money_distrubtion_type == 2:
            assets = self.expo_asset_distribution(self.money_distribution_params['scale'])
        elif self.money_distrubtion_type == 3:
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
            print('Manager ' + str(manager.name) + ' started with: €' + str(manager.starting_assets) + ' and has ' + str(manager.game_history.count(1)) + ' wins and ' + str(manager.game_history.count(0)) + ' losses.')

    def run(self):
        """
        Runs the model after initialization by first assembling the teams and then playing the matches
        """
        start_time = time.time()
        for _ in range(self.assemble_rounds):
            self.schedule.assemble_step()
        print("Assembling teams took --- %s seconds ---" % (time.time() - start_time))

        self.create_pools()

        start_time = time.time()
        for _ in range(self.seasons):
            self.schedule.step()
        print("Simulating seasons took --- %s seconds ---" % (time.time() - start_time))

        self.print_results()