import pandas as pd

from model import FIFA_Simulation

def run_FIFA_model():
    FIFA_data = pd.read_csv('../data.csv')

    assemble_rounds = 1
    seasons = 10
    # Amount of managers is 18 * n_pools
    n_pools = 1
    n_players = 0
    player_stats = FIFA_data
    money_distribution_type = 0
    money_distribution_params = {'mu': 25000000, 'sigma':2500000}
    strategies = []

    verbose = True

    model = FIFA_Simulation(assemble_rounds, seasons, n_pools, n_players, player_stats, money_distribution_type, money_distribution_params, strategies, verbose)
    model.run()

if __name__ == "__main__":
    run_FIFA_model()