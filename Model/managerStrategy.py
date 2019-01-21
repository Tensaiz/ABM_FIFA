class ManagerStrategy(object):


    def __init__(self):
        pass


    def getAssemblyStrategy(self, team_type, assets, TEAM_SIZE):
        raise NotImplementedError()


    def getStepStrategy(self):
        raise NotImplementedError()



class EvenStrategy(ManagerStrategy):


    def getAssemblyStrategy(self, team_type, assets, TEAM_SIZE):
        if team_type == 0:
            # Spend an even amount of money on each player
            money = assets / TEAM_SIZE
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
