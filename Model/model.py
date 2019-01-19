import numpy as np

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
        years (int): Amount of years to simulate
        n_managers (int): The amount of managers to use.
        n_players (int): The amount of players to use from the FIFA dataset. 0 can be used to select all players.
        player_stats (pandas dataframe): A FIFA dataset of players with all their corresponding stats
        money_distribution_type (int): The type of money distribution to use for the managers
            0 = normally distributed
            1 = uniformly distributed
            2 = exponentially distributed
            3 = constant
        money_distrbution_params (:obj: any): Required parameters for the money distribution used 
        strategies (:list:`int`): A list with the different strategies

    TODO:
        - Add agents to scheduler
        - Run the scheduler
        - Create pools for manager teams after team assembly
    """

    def __init__(self, assemble_rounds, years, n_managers, n_players, player_stats, money_distribution_type, money_distribution_params, strategies):
        # Properties
        self.assemble_rounds = assemble_rounds
        self.years = years
        self.n_managers = n_managers
        self.n_players = n_players
        self.player_stats = player_stats
        self.money_distrubtion_type = money_distribution_type
        self.money_distribution_params = money_distribution_params
        self.strategies = strategies

        self.managers = []
        self.players = []

        self.schedule = RandomActivationFIFA(self)

        # Initialization functions
        self.init_agents()

    def init_agents(self):
        self.init_players()
        self.init_managers()

    def init_players(self):
        if self.n_players == 0:
            self.n_players = len(self.player_stats)

        # Randomly select n_players amount of players
        self.chosen_player_stats = self.player_stats.sample(self.n_players)

        for i in range(self.n_players):
            p = Player(self.chosen_player_stats['Name'][i], self, self.chosen_player_stats.iloc[i])
            self.players.append(p)

    def init_managers(self):
        assets = self.get_assets()
        for i in range(self.n_managers):
            m = Manager(i, self, assets[i], 0, 0, 0)
            self.managers.append(m)


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


    def run(self):
        """
        Should run the model after initialization
        """
        pass