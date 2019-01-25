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

    self.candidates_recruitment = []

    def getAssemblyStrategy(self, currentManager):
        pass

    def executeTradeStrategy(self, currentManager):
        teams_ranking_last_season = sorted(model.managers, key=lambda manager: manager.game_history[-34:]count(1), reverse=True)
        own_ranking_place = teams_ranking_last_season.index(currentManager) # this and above line maybe funct/attr in model
        n_players_to_replace = 0
        n_teams_to_recruit_from = 4
	    lower_boundary_wins = 0.4
        middle_boundary_wins = 0.7
        proportion_won_last_season = currentManager.game_history[-34:].count(1)/34      # 34 is always n_matches played last season?
        if proportion_won_last_season < lower_boundary_wins: 
	        n_players_to_replace = 2
        if lower_boundary_wins <=  proportion_won_last_season  <= middle_boundary_wins:
	        n_players_to_replace = 1
        x = 1.25       # or something else
        global budget_for_reorganization = x*currentManager.assets*(n_players_to_replace/currentManager.TEAM_SIZE)
        
        current_team_members = currentManager.team.keys()
        global positions_to_replace
        positions_to_replace = []
        for i in range(n_players_to_replace):
            positions_to_replace.append(random.choice(current_team_members))  # but are these 'position type' + str(i)?
            # write sth to check that that you don't append a duplicate of sb you appended already
        for pos in positions_to_replace:  
            # candidates_recruitment = [], or self.?
            for better_team in teams_ranking_last_season[:own_ranking_place-1]:
                positions = better_team.keys() 
                for position in positions:
                    if pos == position and release clause of better_team[position] <= budget_for_reorganization/n_players_to_replace:
                        self.candidates_recruitment.append(better_team[position])
                        among candidates_recruitment pick 3 candidates randomly and then for these 3 candidates:
                        offer_to_candidate = Offer(currentManager, candidate, pos) 
                    else:
                        send offer to the best (= most expensive) free player with relevant position within budget ^
# when to fire own player?

    def executeRecoveryStrategy(self, currentManager):
        pass

        

        Assume there could be 1+ types of positions in currentManager.accepted: make use of keys in positions_to_replace 
        and create a list for each position type and for each list get the best (most expensive) player 
        to join the team like this:
        




class BestPlayerStrategy(ManagerStrategy):

    def getAssemblyStrategy(self, currentManager):
        pass

    def executeTradeStrategy(self, currentManager):
        pass

    def executeRecoveryStrategy(self, currentManager):
        pass
