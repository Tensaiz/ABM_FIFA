import pandas as pd
import managerStrategy
from model import FIFA_Simulation
<<<<<<< HEAD

def run_FIFA_model():

    assemble_rounds = 1
    seasons = 15
    # Amount of managers is 18 * n_pools
    n_pools = 1
    n_players = 0
    player_stats = FIFA_data
    money_distribution_type = 0
    money_distribution_params = {'mu': 25000000, 'sigma':2500000}
    earnings_ratio = (1/2)
    strategies = [managerStrategy.UnforgivingStrategy(), managerStrategy.SimpleStrategy()] #, managerStrategy.EvenStrategy()

    verbose = True

    model = FIFA_Simulation(assemble_rounds, seasons, n_pools, n_players, player_stats, money_distribution_type, money_distribution_params, earnings_ratio, strategies, verbose)
    model = FIFA_Simulation()
    model.run()
=======
import utility
import matplotlib.pyplot as plt

def run_FIFA_model():

    player_stats = utility.transform_fifa(pd.read_csv('../data.csv'))

    evenstrat = []
    unforgiving = []
    simple = []
>>>>>>> 6bef7d0711bb8940e9683a8c05f5033a9bfefab0

    evenstrat_money = []
    unforgiving_money = []
    simple_money = []

    for i in range(10):
        model = FIFA_Simulation(player_stats=player_stats, verbose=False)
        model.run_model()

        even = 0
        unforg = 0
        sim = 0

        even_money = 0
        unforg_money = 0
        sim_money = 0

        for manager in model.managers:
            strat = type(manager.strategy).__name__
            if strat == 'EvenStrategy':
                even += manager.reputation
                even_money += manager.assets
            elif strat == 'UnforgivingStrategy':
                unforg += manager.reputation
                unforg_money += manager.assets
            elif strat == 'SimpleStrategy':
                sim += manager.reputation
                sim_money += manager.assets
        evenstrat.append(even)
        unforgiving.append(unforg)
        simple.append(sim)

        evenstrat_money.append(even_money)
        unforgiving_money.append(unforg_money)
        simple_money.append(sim_money)

    plot(evenstrat, unforgiving, simple, evenstrat_money, unforgiving_money, simple_money)
    data = model.datacollector.get_model_vars_dataframe()
<<<<<<< HEAD
    print(data)
=======
    # print(data)

def plot(tactic1, tactic2, tactic3, money1, money2, money3):
    x = list(range(1, 11))
    plt.figure(0)
    plt.scatter(x, tactic1, label='Even strategy')
    plt.scatter(x, tactic2, label='Unforgiving strategy')
    plt.scatter(x, tactic3, label='Simple strategy')
    plt.ylabel('Cummulative manager reputation after 15 seasons')
    plt.xlabel('Iteration')
    plt.xticks(x)
    plt.legend()
    plt.show()

    plt.figure(1)
    plt.scatter(x, money1, label='Even strategy')
    plt.scatter(x, money2, label='Unforgiving strategy')
    plt.scatter(x, money3, label='Simple strategy')
    plt.ylabel('Cummulative manager assets after 15 seasons')
    plt.xlabel('Iteration')
    plt.xticks(x)
    plt.legend()
    plt.show()
>>>>>>> 6bef7d0711bb8940e9683a8c05f5033a9bfefab0

if __name__ == "__main__":
    run_FIFA_model()