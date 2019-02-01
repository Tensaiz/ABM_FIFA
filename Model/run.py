import pandas as pd
import managerStrategy
from model import FIFA_Simulation
import utility

def run_FIFA_model():

    player_stats = utility.transform_fifa(pd.read_csv('../data.csv'))
    model = FIFA_Simulation(player_stats=player_stats)

    model.run_model()

    data = model.datacollector.get_model_vars_dataframe()
    print(data)
if __name__ == "__main__":
    run_FIFA_model()