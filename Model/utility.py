import math
import random

def match_outcome(manager_1, manager_2):
    """
    Determines the outcome of a match between the teams of two managers

    Use different weights and calculate outcome by using:
        - Market value of team
        - SPI of team
        - ELO (if it has been accumulated enough)
        - Average age

    Args:
        team_1 (:obj: manager): 
        team_2 (:obj: manager): 
    Returns:
        outcome (int): The outcome of the match, whether team_1 has won from team_2
            0 = team_1 won
            1 = team_2 won
            2 = tie
    """
    market_p = market_value_win_probability(manager_1, manager_2)
    draw = random.uniform(0, 1)
    if draw < market_p:
        result = 0
    elif draw > market_p:
        result = 1
    else:
        result = 2

    return result

def market_value_win_probability(manager_1, manager_2):
    '''
    Use sigmoid function to calculate probability of team 1 winning over team 2 based on average market value of the teams
    '''
    manager_1_market_val = get_manager_market_value(manager_1)
    manager_2_market_val = get_manager_market_value(manager_2)
    return 1 / (1 + math.exp(-math.log(manager_1_market_val / manager_2_market_val) / 1.3026))

def get_manager_market_value(manager):
    '''
    Calculate the average market value of the team
    '''
    market_value = 0
    positions = manager.team.keys()
    for position in positions:
        player = manager.team[position]
        market_value += player.stats['Value']
    return market_value / len(positions)