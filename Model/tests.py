import unittest
import pandas as pd
import sys
import inspect
from model import FIFA_Simulation


class TestUtility(unittest.TestCase):

    def test_utility(self):
        pass





    def test_moneySumInStrategies(self):
        # money sum instrategy should <= totalAssets

        #Create model
        FIFA_data = pd.read_csv('../data.csv')

        assemble_rounds = 1
        seasons = 10
        # Amount of managers is 18 * n_pools
        n_pools = 1
        n_players = 0
        player_stats = FIFA_data
        money_distribution_type = 0
        money_distribution_params = {'mu': 25000000, 'sigma': 2500000}
        for name, obj in inspect.getmembers(sys.modules["managerStrategy"]):
            if inspect.isclass(obj) and name != "ManagerStrategy":
                strategies = [obj()]

        verbose = True

        model = FIFA_Simulation(assemble_rounds, seasons, n_pools, n_players, player_stats, money_distribution_type,
                                money_distribution_params, strategies, verbose)

        # now, the strategies should be initialized, so we can test them
        for man in model.managers:
            stra = man.strategy.getAssemblyStrategy(man)
            #print("[*] Checking Strategy and manager assets:", stra.__name__)
            #print("[*] Assets: ", man.assets)
            self.assertGreaterEqual(man.assets, sum(stra.values()))




    

if __name__ == '__main__':
    unittest.main()