class ManagerStrategy(object):


    def __init__(self, model):
        self.model = model


    def getAssemblyStrategy(self, currentManager):
        raise NotImplementedError()


    def getTradeStrategy(self, currentManager):
        raise NotImplementedError()



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
