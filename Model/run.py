import pandas as pd
import managerStrategy
from model import FIFA_Simulation
import utility
import matplotlib.pyplot as plt

def run_FIFA_model():

    player_stats = utility.transform_fifa(pd.read_csv('../data.csv'))

    evenstrat = []
    unforgiving = []
    simple = []

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

if __name__ == "__main__":
    run_FIFA_model()