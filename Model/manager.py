from mesa import Agent

class Manager(Agent):
    """
    The (soccer) manager class for the FIFA agent based model simulation

    This class inherits the Agent class from the mesa library
    The managers try to assemble a team initially based on different strategies
    They try to optimise their teams by trying to maximise their reputation (ELO) which can be gained by winning
    They have different strategies for dealing with wins / losses

    Args:
        name (int): Name of the manager
        model (:obj: model): The top-level ABM model
        assets (float): The assets that the manager can use to buy or trade for players
        reputation (int): The starting reputation / ELO of the manager
        assemble_strategy (int): The strategy used to assemble the initial team
        trade_strategy (int): The strategy used to progress by buying and trading players


    TODO:
        Create trading mechanism between manager agents
        Create team assembly and team trading mechanics
        Create different optimisation strategies to assemble a team
    """
    def __init__(self, name, model, assets, reputation, assemble_strategy, trade_strategy):
        super().__init__(name, model)
        self.assets = assets
        self.reputation = reputation
        self.assemble_strategy = assemble_strategy
        self.trade_strategy = trade_strategy
        self.team = {}

    def step(self):
        pass
