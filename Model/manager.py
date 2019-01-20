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
        Create team trading mechanics
        Create different optimisation strategies to assemble a team
    """

    TEAM_SIZE = 18
    SPECIFIC_POSITION_DICT = {
        'RF': 'attacker',
        'ST': 'attacker',
        'LW': 'midfielder',
        'GK': 'keeper',
        'RCM': 'midfielder',
        'LF': 'attacker',
        'RS': 'attacker',
        'RCB': 'defender',
        'LCM': 'midfielder',
        'CB': 'defender',
        'LDM': 'midfielder',
        'CAM': 'midfielder',
        'CDM': 'midfielder',
        'LS': 'attacker',
        'LCB': 'defender',
        'RM': 'midfielder',
        'LAM': 'midfielder',
        'LM': 'midfielder',
        'LB': 'defender',
        'RDM': 'midfielder',
        'RW': 'midfielder',
        'CM': 'midfielder',
        'RB': 'defender',
        'RAM': 'midfielder',
        'CF': 'attacker',
        'RWB': 'defender',
        'LWB': 'defender'
    }

    GENERAL_POSITION_DICT = {
        'keeper': [
            'GK'
        ],
        'attacker': [
            'RF',
            'ST',
            'LF',
            'RS',
            'LS',
            'CF'
        ],
        'midfielder': [
            'LW',
            'RCM',
            'LCM',
            'LDM',
            'CAM',
            'CDM',
            'RM',
            'LAM',
            'LM',
            'RDM',
            'RW',
            'CM',
            'RAM'
        ],
        'defender': [
            'RCB',
            'CB',
            'LCB',
            'LB',
            'RB',
            'RWB',
            'LWB'
        ]
    }

    def __init__(self, name, model, assets, reputation, assemble_strategy, trade_strategy, team_type=0):
        super().__init__(name, model)
        self.name = name
        self.assets = assets
        self.reputation = reputation

        # 1 keeper, 4 defenders, 3 midfielders, 3 attackers
        # + 1 keeper sub and 6 sub players
        self.team_type = team_type
        self.init_empty_team()

        self.assemble_strategy = self.get_assemble_strategy(assemble_strategy)
        self.trade_strategy = self.get_trade_strategy(trade_strategy)

        # Keep track of past match results
        self.game_history = []

    def assemble_step(self):
        if self.model.verbose:
            print('Manager ' + str(self.name) + ' has ' + str(self.assets) + ' funds available to pick players')
        for pos, player in self.team.items():
            if player == None:
                attempt = 0
                # Keep picking players until you find one that is in the model and doesn't have a manager yet
                chosen_players = self.pick_player(pos)
                chosen_player = chosen_players.iloc[0]
                # Might have to catch a key error if the player isn't in the dictionary here
                player_agent = self.model.player_lookup[chosen_player['Name']]
                if player_agent.manager != None:
                    player_agent = None
                while (player_agent == None):
                    chosen_player = chosen_players.iloc[attempt]
                    # Get the player agent to assign to the team
                    # Might have to catch a key error if the player isn't in the dictionary here
                    player_agent = self.model.player_lookup[chosen_player['Name']]
                    if player_agent.manager != None:
                        player_agent = None
                    attempt += 1
                self.team[pos] = player_agent
                self.assets -= chosen_player['Release Clause']
                if pos[0:3] == 'sub':
                    player_agent.active = False
                else:
                    player_agent.active = True
                player_agent.manager = self

    def pick_player(self, pos):
        money_available_for_pos = self.assemble_strategy[pos]
 
        # List of players that have the same release clause as the money the manager wants to spend for the position
        suitable_players = self.model.chosen_player_stats[self.model.chosen_player_stats['Release Clause'] == money_available_for_pos]
        if pos.split('_')[0] != 'sub':
            pos = pos.split('_')[0]
            suitable_players = suitable_players[suitable_players['Position'].isin(self.GENERAL_POSITION_DICT[pos])]
        if len(suitable_players) > 0:
            # Pick the player with the highest overall rating
            return suitable_players[suitable_players['Overall'].argsort()[::-1]]
        else:
            # If there are none, find the closest release clause that is smaller than the money available
            possibilities = self.model.chosen_player_stats[self.model.chosen_player_stats['Release Clause'] - money_available_for_pos <= 0]
            if pos.split('_')[0] != 'sub':
                possibilities = possibilities[possibilities['Position'].isin(self.GENERAL_POSITION_DICT[pos])]
            return possibilities.iloc[(possibilities['Release Clause'] - money_available_for_pos).abs().argsort()]

    def step(self):
        pass


    def get_assemble_strategy(self, strategy):
        '''
        This function should return a dictionary with the amount of money the manager should spend per player to assemble his team
        '''
        if strategy == 0:
            if self.team_type == 0:
                # Spend an even amount of money on each player
                money = self.assets / self.TEAM_SIZE
                strategy = {'keeper': money}
                # 4 defenders, 3 midfielders, 3 attackers
                for i in range(4):
                    strategy['defender_' + str(i + 1)] = money
                for i in range(3):
                    strategy['midfielder_' + str(i + 1)] = money
                for i in range(3):
                    strategy['attacker_' + str(i + 1)] = money
            strategy['sub_keeper'] = money
            for i in range(6):
                strategy['sub_player_' + str(i + 1)] = money
            return strategy

    def get_trade_strategy(self, strategy):
        pass

    def init_empty_team(self):
        self.team = {
            'keeper': None,
        }
        if self.team_type == 0:
            # 4 defenders, 3 midfielders, 3 attackers
            for i in range(4):
                self.team['defender_' + str(i + 1)] = None
            for i in range(3):
                self.team['midfielder_' + str(i + 1)] = None
            for i in range(3):
                self.team['attacker_' + str(i + 1)] = None
        self.team['sub_keeper'] = None
        for i in range(6):
            self.team['sub_player_' + str(i + 1)] = None
