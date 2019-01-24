class ManagerStrategy(object):


    def __init__(self, model = None):
        self.model = model 

    def getAssemblyStrategy(self, currentManager):
        raise NotImplementedError()

    def getTradeStrategy(self, currentManager):
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

    def getTradeStrategy(self, currentManager):
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

    def getTradeStrategy(self, currentManager):

        pass

class StrategyA(ManagerStrategy):

    def getAssemblyStrategy(self, currentManager):
        pass

    def getTradeStrategy(self, currentManager):
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
        players_to_fire = []
        for i in range(n_players_to_fire):
            players_to_fire.append(random.choice(current_team_members))# did I really access player objects by position keys?
        for pos in players_to_fire:
            pos.manager = None          
            currentManager.team[pos] = None 
            team_ranking_last_season = sorted(model.managers, key=lambda manager: manager.game_history[-34:]count(1), reverse=True)
            for i-th in team_ranking_last_season:
                i-th.managers..........

                 


        


