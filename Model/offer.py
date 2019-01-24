class Offer(object):

    def __init__(self, manager, player, position):
        self.manager = manager
        self.player = player
        self.position = position

        self.player.offers.apeend(self)

    def accept(self):
        # Update Players Manager, remove him
        self.player.manager.team[self.player.position] = None
        self.player.manager.assets += self.player.stats['Release Clause']

        # Update player and new manager
        self.player.position = self.position
        self.player.manager = self.manager

        self.manager.assets -= self.player.stats['Release Clause']

        self.manager.accepted.append(self.player)

    def decline(self):
        pass





