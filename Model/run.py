import pandas as pd
import managerStrategy
from model import FIFA_Simulation

def run_FIFA_model():

    model = FIFA_Simulation()
    model.run()

if __name__ == "__main__":
    run_FIFA_model()