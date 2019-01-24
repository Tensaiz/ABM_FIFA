class Offer(object):

    def __init__(self, manager, player):
        self.manager = manager
        self.player = player

    def execute(self):
        self.player.offers.append(self.manager)

