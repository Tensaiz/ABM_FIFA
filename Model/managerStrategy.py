from offer import Offer
import random

class ManagerStrategy(object):

    def __init__(self, model = None):   
        self.model = model 

    def getAssemblyStrategy(self, currentManager):
        raise NotImplementedError()

    def executeTradeStrategy(self, currentManager):
        raise NotImplementedError()

    def executeRecoveryStrategy(self, currentManager):
        raise NotImplementedError()
        print('Executing recovery strategy...')

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

    def buy_free_player(self, manager, pos, money):
        attempt = 0
        possible_players = self.pick_player(pos, money)
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
        manager.team[pos] = player_agent
        manager.assets -= chosen_player['Release Clause']
        if pos[0:3] == 'sub':
            player_agent.active = False
        else:
            player_agent.active = True
        player_agent.manager = manager
        player_agent.position = pos

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

    def executeRecoveryStrategy(self, currentManager):
        pass


class UnforgivingStrategy(ManagerStrategy):

    '''
    Spread money evenly for team assembly,
    Trade step: After a decent season, don't trade. After a mediocre or bad season,  replace the current team with n players from teams that did better last season, when 
    this doesn't fully work, buy free players with this budget: 1.25 (or other nr if we want) * assets/team.SIZE)
    Recovery step: if necessary bBuy the best player you can for empty positions and if not a single person has been 
    replaced, still buy a free player

    '''
    def getAssemblyStrategy(self, currentManager):
        # (For now) copied from EvenStrategy 

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
        teams_ranking_last_season = sorted(self.model.managers, key=lambda manager: manager.game_history[-34:].count(1), reverse=True)
        own_ranking_place = teams_ranking_last_season.index(currentManager) # this and above line maybe funct/attr in model
        n_traitors_recruiting = 0
        lower_boundary_wins = 0.4
        middle_boundary_wins = 0.7
        proportion_won_last_season = currentManager.game_history[-34:].count(1)/34    
        if proportion_won_last_season < lower_boundary_wins: 
	        n_traitors_recruiting = 5
        if lower_boundary_wins <=  proportion_won_last_season  <= middle_boundary_wins:
	        n_traitors_recruiting = 3
        a = 1.25       # or something else
        budget_for_replacing_player = a*(currentManager.assets/currentManager.TEAM_SIZE)

        candidates_recruitment = []  
        for better_team in teams_ranking_last_season[:own_ranking_place-1]:
            for pos, player in better_team.team.items():  
                if player != None:
                    if player.stats['Release Clause'] <= budget_for_replacing_player:
                        candidates_recruitment.append(player)

        narrowed_down_candidate_list = []
        if len(candidates_recruitment) >= n_traitors_recruiting:
            for i in range(n_traitors_recruiting):
                candidate = random.choice(candidates_recruitment)
                narrowed_down_candidate_list.append(candidate)
                candidates_recruitment.remove(candidate) 
                ''' later: add a function to check that no more than 3 or 4 of a type of player is recruited,
                because if there's more and they all accept you'd have wasted money on this 'extra' player you have to reject'''
        elif len(candidates_recruitment) < n_traitors_recruiting:
            if len(candidates_recruitment) != 0:
                for i in range(len(candidates_recruitment)):
                    candidate = random.choice(candidates_recruitment)
                    narrowed_down_candidate_list.append(candidate)
                    candidates_recruitment.remove(candidate) 
                    '''idem'''
                     
        for final_candidate in narrowed_down_candidate_list:
            Offer(currentManager, final_candidate, final_candidate.position) 
            
    def executeRecoveryStrategy(self, currentManager):
        # mostly copied from SimpleStrategy, but different budget for free players 
        a = 1.25       # or something else
        budget_for_replacing_player = a*(currentManager.assets/currentManager.TEAM_SIZE)

        # Get empty positions
        empty_postions = []
        for pos, player in currentManager.team.items():
            if player == None:
                empty_postions.append(pos)
        n_players_who_quit = len(empty_postions)

        for pos in empty_postions:
            # Check if you can fill an empty position with a player that accepted your offer
            filled = False
            for player in currentManager.accepted:
                if player.position == pos:
                    # Assign player to empty position
                    currentManager.team[pos] = player
                    if pos[0:3] == 'sub':
                        player.active = False
                    else:
                        player.active = True
                    filled = True
                    currentManager.accepted.remove(player)
                    break
            if filled:
                empty_postions.remove(pos)
                continue

            # Otherwise buy a new player to fill the position that will accept your offer
            self.buy_free_player(currentManager, pos, (currentManager.assets / len(empty_postions)))


            # Allow any remaining players that accepted the offer to join
        if len(currentManager.accepted) != 0:
            for player in currentManager.accepted:
                position = player.position
                replaceable_player = currentManager.team[position]
                self.kick_player(currentManager, replaceable_player, position)
                currentManager.team[position] = player

        currentManager.accepted = []
 
        ''' If 1) nobody resigned AND 2a) couldn't find any affordable players from better teams to send offer to OR 
        # 2b) none of the players from better teams accepted the offer, then replace the worst player in the current team 
        by buying a new player (to still improve the team somwhat) '''
        if n_players_who_quit == 0 and len(currentManager.accepted) == 0:
            
            # Get worst player
            worst_player = None
            overall = 100
            for pos, player in currentManager.team.items():
                if player.stats['Overall'] < overall:
                    worst_player = player
                    overall = worst_player.stats['Overall']
            position = worst_player.position

            # Buy or send offer to best player you can buy
            possible_players = self.pick_player(position, budget_for_replacing_player)
            if len(possible_players > 0):
                chosen_player = possible_players.iloc[0]
                if (chosen_player['Overall'] > worst_player.stats['Overall']):
                    # Might have to catch a key error if the player isn't in the dictionary here
                    player_agent = self.model.player_lookup[chosen_player['Name']]
                    # Send offer to the player
                    Offer(currentManager, player_agent, position)

class SimpleStrategy(ManagerStrategy):
    '''
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
            if player.stats['Overall'] < overall: # during one run got AttributeError: 'NoneType' object has no attribute 'stats'
                worst_player = player
                overall = worst_player.stats['Overall']
        position = worst_player.position

        # Buy or send offer to best player you can buy
        possible_players = self.pick_player(position, currentManager.assets)
        if len(possible_players > 0):
            chosen_player = possible_players.iloc[0]
            if (chosen_player['Overall'] > worst_player.stats['Overall']):
                # Might have to catch a key error if the player isn't in the dictionary here
                player_agent = self.model.player_lookup[chosen_player['Name']]
                # Send offer to the player
                Offer(currentManager, player_agent, position)

    def executeRecoveryStrategy(self, currentManager):
        # Get empty positions
        empty_postions = []
        for pos, player in currentManager.team.items():
            if player == None:
                empty_postions.append(pos)

        for pos in empty_postions:
            # Check if you can fill an empty position with a player that accepted your offer
            filled = False
            for player in currentManager.accepted:
                if player.position == pos:
                    # Assign player to empty position
                    currentManager.team[pos] = player
                    if pos[0:3] == 'sub':
                        player.active = False
                    else:
                        player.active = True
                    filled = True
                    currentManager.accepted.remove(player)
                    break
            if filled:
                empty_postions.remove(pos)
                continue

            # Otherwise buy a new player to fill the position that will accept your offer
            money = currentManager.assets / len(empty_postions)
            self.buy_free_player(currentManager, pos, money)

        # Now choose between left over players that accepted your offer
        for player in currentManager.accepted:
            position = player.position
            replaceable_player = currentManager.team[position]
            self.kick_player(currentManager, replaceable_player, position)
            currentManager.team[position] = player

        currentManager.accepted = []



class BestPlayerStrategy(ManagerStrategy):

    def getAssemblyStrategy(self, currentManager):
        pass

    def executeTradeStrategy(self, currentManager):
        pass

    def executeRecoveryStrategy(self, currentManager):
        pass
