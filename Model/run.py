import pandas as pd
import managerStrategy
from model import FIFA_Simulation

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

    data = model.datacollector.get_model_vars_dataframe()
    print(data)

if __name__ == "__main__":
    run_FIFA_model()