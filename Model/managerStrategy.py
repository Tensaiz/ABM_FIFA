class ManagerStrategy(object):

    def __init__(self, model = None):
        self.model = model 

    def getAssemblyStrategy(self, currentManager):
        raise NotImplementedError()

    def executeTradeStrategy(self, currentManager):
        raise NotImplementedError()

    def executeRecoveryStrategy(self, currentManager):
        raise NotImplementedError()

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

    def pick_player(self, pos, money):
        '''
        Return a list with possible players for a position and a certain amount of money
        '''
        print(pos)
        # List of players that have the same release clause as the money the manager wants to spend for the position
        suitable_players = self.model.chosen_player_stats[self.model.chosen_player_stats['Release Clause'] == money]
        if pos.split('_')[0] != 'sub':
            pos = pos.split('_')[0]
            suitable_players = suitable_players[suitable_players['Position'].isin(self.GENERAL_POSITION_DICT[pos])]
        if len(suitable_players) > 0:
            # Pick the player with the highest overall rating
            return suitable_players[suitable_players['Overall'].argsort()[::-1]]
        else:
            # If there are none, find the closest release clause that is smaller than the money available
            possibilities = self.model.chosen_player_stats[self.model.chosen_player_stats['Release Clause'] - money <= 0]
            if pos.split('_')[0] != 'sub':
                possibilities = possibilities[possibilities['Position'].isin(self.GENERAL_POSITION_DICT[pos])]
            return possibilities.iloc[(possibilities['Release Clause'] - money).abs().argsort()]

    def kick_player(self, manager, player, position):
        manager.team[position] = None
        player.position = None
        player.manager = None

class ExampleStrategy(ManagerStrategy):

    def getAssemblyStrategy(self, currentManager):
        #expenentialy distributed assets over players
        total = currentManager.assets
        strategy = {'keeper': total // 2}
        total = total // 2 # rest
        for i in range(4):
            strategy['defender_' + str(i + 1)] = total // 2
            total = total // 2
        for i in range(3):
            strategy['midfielder_' + str(i + 1)] = total // 2
            total = total // 2
        for i in range(3):
            strategy['attacker_' + str(i + 1)] = total // 2
            total = total // 2

        for i in range(6):
            strategy['sub_player_' + str(i + 1)] = total // 2
            total = total // 2


        strategy['sub_keeper'] = total
        return strategy

    def executeTradeStrategy(self, currentManager):
        # use the same strategy as in Assembly
        return self.getAssemblyStrategy(currentManager)

    def executeRecoveryStrategy(self, currentManager):
        # use the same strategy as in Assembly
        return self.getAssemblyStrategy(currentManager)


class EvenStrategy(ManagerStrategy):

    def getAssemblyStrategy(self, currentManager):
        # pass just current manager :D
        if currentManager.team_type == 0:
            # Spend an even amount of money on each player
            money = currentManager.assets / currentManager.TEAM_SIZE
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

    def executeTradeStrategy(self, currentManager):
        pass

class StrategyA(ManagerStrategy):

    def getAssemblyStrategy(self, currentManager):
        pass

    def executeTradeStrategy(self, currentManager):
        n_players_to_fire = 0
	    lower_boundary_wins = 0.3
        middle_boundary_wins = 0.6
        proportion_won_last_season = currentManager.game_history[-34:].count(1)/34      # 34 is always n_matches played last season?
        if proportion_won_last_season < lower_boundary_wins: 
	        n_players_to_fire = 9
        if lower_boundary_wins <_  proportion_won_last_season  <_ middle_boundary_wins:
	        n_players_to_fire = 5
            #wait make sure that you don't randomly fire sb you just hired. \
            # so just get the full list of ppl to replace
        current_team_members = currentManager.team.keys()
        positions_to_fire = []
        for i in range(n_players_to_fire):
            positions_to_fire.append(random.choice(current_team_members))  # are these 'position type' + str(i)?
        for pos in positions_to_fire:  
            player_to_fire = team[pos]
            player_to_fire.manager = None           
            currentManager.team[pos] = None 
            teams_ranking_last_season = sorted(model.managers, key=lambda manager: manager.game_history[-34:]count(1), reverse=True)
            own_ranking_place = teams_ranking_last_season.index(currentManager)
            for team in teams_ranking_last_season[:own_ranking_place-1]: 
                positions = team.keys()
                candidates = []
                for position in positions:
                    if pos == position:
                        candidates.append(position)
                        potential_candidate = random.choice(candidates)
                        if offer_accepted_by(team[potential_candidate]):   # function not existent yet
                            team[potential_candidate].manager = currentManager
                            currentManager.team[pos] = team[potential_candidate]
                            break 
                        else:
                            candidates.remove(potential_candidate)
                            potential_candidate = random.choice(candidates)
                            if offer_accepted_by(potential_candidate):
                                team[potential_candidate].manager = currentManager
                                currentManager.team[pos] = team[potential_candidate]
                                break
            for backup_candidates in free_players:
                
            # if that ^ fails, buy free player with available remaining money and stop firing 

                 


        


    def executeRecoveryStrategy(self, currentManager):
        # Get open positions
        to_buy = []
        for pos, player in currentManager.team.items():
            if player == None:
                to_buy.append(pos)
        for pos in to_buy:
            attempt = 0
            # Buy best player you can buy that will accept your offer
            possible_players = self.pick_player(pos, currentManager.assets / len(to_buy))
            chosen_player = possible_players.iloc[attempt]
            # Might have to catch a key error if the player isn't in the dictionary here
            player_agent = self.model.player_lookup[chosen_player['Name']]
            if player_agent.manager != None:
                attempt += 1
                continue
            else:
                # Buy player
                currentManager.team[pos] = player_agent
                player_agent.pos = pos
                currentManager.assets -= chosen_player['Release Clause']
                if pos[0:3] == 'sub':
                    player_agent.active = False
                else:
                    player_agent.active = True
                player_agent.manager = currentManager
                player_agent.position = pos












































class SimpleStrategy(ManagerStrategy):
    '''
    HAS TO BE REWRITTEN TO TAKE INTO ACCOUNT NEW OFFER CLASS

    Spread money evenly for team assembly,
    Trade step: Every season swap your worst player for the best possible player you can buy
    Recovery step: Buy the best player you can for the missing positions
    '''
    def getAssemblyStrategy(self, currentManager):
        # pass just current manager :D
        if currentManager.team_type == 0:
            # Spend an even amount of money on each player
            money = currentManager.assets / currentManager.TEAM_SIZE
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

    def executeTradeStrategy(self, currentManager):
        '''
        Every season swap your worst player for the best possible player you can buy
        '''
        # Get worst player
        worst_player = None
        overall = 100
        for pos, player in currentManager.team.items():
            if player.stats['Overall'] < overall:
                worst_player = player
        print(worst_player)
        print(worst_player.position)
        # Let him go
        position = worst_player.position
        self.kick_player(currentManager, worst_player, position)
        print('Buy / send: ' + position)
        # Buy or send offer to best player you can buy that will accept your offer
        possible_players = self.pick_player(position, currentManager.assets)
        chosen_player = possible_players.iloc[0]
        # Might have to catch a key error if the player isn't in the dictionary here
        player_agent = self.model.player_lookup[chosen_player['Name']]
        if player_agent.manager != None:
            # Send offer to player
            player_agent.offers.append((currentManager, position))
        else:
            # Buy player
            currentManager.team[pos] = player_agent
            player_agent.position = pos
            currentManager.assets -= chosen_player['Release Clause']
            if pos[0:3] == 'sub':
                player_agent.active = False
            else:
                player_agent.active = True
            player_agent.manager = currentManager
            player_agent.position = pos

    def executeRecoveryStrategy(self, currentManager):
        # Get open positions
        to_buy = []
        for pos, player in currentManager.team.items():
            if player == None:
                to_buy.append(pos)
        print('Recovery for manager: ' + str(currentManager.name))
        print('positions: ' + str(to_buy))
        for pos in to_buy:
            attempt = 0
            # Buy best player you can buy that will accept your offer
            print(pos)
            possible_players = self.pick_player(pos, currentManager.assets / len(to_buy))
            chosen_player = possible_players.iloc[attempt]
            # Might have to catch a key error if the player isn't in the dictionary here
            player_agent = self.model.player_lookup[chosen_player['Name']]
            if player_agent.manager != None:
                player_agent = None
            while (player_agent == None):
                chosen_player = possible_players.iloc[attempt]
                # Might have to catch a key error if the player isn't in the dictionary here
                player_agent = self.model.player_lookup[chosen_player['Name']]
                if player_agent.manager != None:
                    player_agent = None
                attempt += 1
            # Buy player
            currentManager.team[pos] = player_agent
            currentManager.assets -= chosen_player['Release Clause']
            if pos[0:3] == 'sub':
                player_agent.active = False
            else:
                player_agent.active = True
            player_agent.manager = currentManager
            player_agent.position = pos


class BestPlayerStrategy(ManagerStrategy):

    def getAssemblyStrategy(self, currentManager):
        pass

    def executeTradeStrategy(self, currentManager):
        pass

    def executeRecoveryStrategy(self, currentManager):
        pass
