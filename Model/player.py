from mesa import Agent

class Player(Agent):
    """
    The (soccer) player class for the FIFA agent based model simulation.

    This class inherits the Agent class from the mesa library.
    The players receive identical stats to the ones attributed to their name in the FIFA dataset
    They initially receive offers and accept the one that fits them best
    After that they progress through matches and may receive offers at the end of a season, which they can reject or accept
    (Optional?) They age as years pass, and when they pass 35 they retire

    Args:
        name (str): Actual name of the soccer player
        model (:obj: model): The top-level ABM model
        stats (:list: str or int): the different stats of the player

    TODO:
        Needs a step function to determine what the player does every action,
        for the first few steps it should be considering between open invitations to teams (when teams are assembled)
        Afterwards it should choose between new teams if he is invited by a manager
    """
    def __init__(self, name, model, stats):
        super().__init__(name, model)
        self.name = name
        self.stats = stats
        self.offers = []
        self.manager = None
        # In the field or a substitute player
        self.active = None
        # Which position player is currently playing
        self.position = None

    def step(self):
        """
        Takes offers into account after season finishes. The (first) manager with the highest reputation is
        chosen by the player.
        """
        highest_offer = None

        if self.manager is None:
            highest_rep = 0

        else:
            highest_rep = self.manager.reputation

        for offer in self.offers:
            if offer.manager.reputation > highest_rep:
                highest_offer = offer

        if highest_offer is not None:
            highest_offer.accept()
