import pandas as pd
import managerStrategy
from model import FIFA_Simulation

def run_FIFA_model():
    FIFA_data = pd.read_csv('.../data.csv')

    assemble_rounds = 1
    seasons = 15
    # Amount of managers is 18 * n_pools
    n_pools = 1
    n_players = 0
    player_stats = FIFA_data
    money_distribution_type = 0
    mu = 10^6
    sigma = 10^6
    earnings_ratio = (1/2)
    strategies = [managerStrategy.SimpleStrategy(), managerStrategy.EvenStrategy()]

    verbose = True

    model = FIFA_Simulation(assemble_rounds, seasons, n_pools, n_players, player_stats, money_distribution_type, mu, sigma, earnings_ratio, strategies, verbose)
    model.run()

if __name__ == "__main__":
    run_FIFA_model()