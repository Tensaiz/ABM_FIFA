from mesa.time import RandomActivation

class RandomActivationFIFA(RandomActivation):
    '''
    The scheduler for the FIFA simulation ABM
    It schedules the activation of the manager and the players

    It starts with a few assembly rounds for the managers and players where managers form teams
    Afterwards the match scheduling should start where managers in pools play matches with each other
    Every season the managers get the chance to trade and buy players, whereas players can accept or reject these offers

    TODO:
        - Actual schedule
            - Different schedule stages (initial offers -> matches)
            - Incorporate years and seasons
        - Incorporate aging
    '''
    def __init__(self, model):
        super().__init__(model)

    def step(self):
        pass
