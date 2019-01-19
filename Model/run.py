import pandas as pd

from model import FIFA_Simulation

def run_FIFA_model():
    FIFA_data = pd.read_csv('../data.csv')

    assemble_rounds = 10
    years = 1
    n_managers = 5
    n_players = 0
    player_stats = FIFA_data
    money_distribution_type = 0
    money_distribution_params = {'mu': 1000000, 'sigma':250000}
    strategies = []

    model = FIFA_Simulation(assemble_rounds, years, n_managers, n_players, player_stats, money_distribution_type, money_distribution_params, strategies)
    model.run()

if __name__ == "__main__":
    run_FIFA_model()