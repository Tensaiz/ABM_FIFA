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
    age_p = average_age_win_probability(manager_1, manager_2)
    age_weight = 0.25
    market_p = market_value_win_probability(manager_1, manager_2)
    market_weight = 1
    victory_p = market_p * market_weight
    draw = get_draw(victory_p)

    chance = random.uniform(0, 1)

    if draw == chance:
        result = 2
    elif chance < victory_p:
        result = 0
    elif chance > victory_p:
        result = 1

    return result


def average_age_win_probability(manager_1, manager_2):
    team_1_average_age = get_average_age_team(manager_1)
    team_2_average_age = get_average_age_team(manager_2)
    difference_average_ages = team_1_average_age - team_2_average_age
    return 1/(1+math.exp(-(32*difference_average_ages-(difference_average_ages)**3)/131))

def get_average_age_team(manager):
    '''
    Calculate the average age of the team
    '''
    sum_ages = 0 
    current_team_size = 0     
    for pos, player in manager.team.items():  
        if player != None:
            current_team_size += 1
            sum_ages += player.stats['Age']        
    return sum_ages / current_team_size       
     
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
        if player != None:
            market_value += player.stats['Value']
    return market_value / len(positions)

def get_draw(p_victory):
    return (1/3) * math.exp(-( (p_victory-0.5)**2 / (2 * 0.28**2)))
