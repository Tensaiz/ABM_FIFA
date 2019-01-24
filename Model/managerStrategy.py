class ManagerStrategy(object):


    def __init__(self, model = None):
        self.model = model 

    def getAssemblyStrategy(self, currentManager):
        raise NotImplementedError()

    def executeTradeStrategy(self, currentManager):
        raise NotImplementedError()

    def executeRecoveryStrategy(self, currentManager):
        raise NotImplementedError()

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
                        if offer_accepted_by(potential_candidate):   # function not existent yet
                            break 
                        else:
                            candidates.remove(potential_candidate)
                            potential_candidate = random.choice(candidates)
 
                # if found a replacer in a team then exit this loop and move to next player

                # if that ^ fails, buy free player with available remaining money and stop firing 

                 


        


    def executeRecoveryStrategy(self, currentManager):
        pass
