import pandas as pd
import managerStrategy
from model import FIFA_Simulation

def run_FIFA_model():

    model = FIFA_Simulation()
    model.run()

    data = model.datacollector.get_model_vars_dataframe()
    print(data)
if __name__ == "__main__":
    run_FIFA_model()