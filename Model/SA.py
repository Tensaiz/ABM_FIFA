from IPython.display import clear_output
from SALib.sample import saltelli
from manager import Manager
from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from IPython.display import clear_output
from model import FIFA_Simulation
import utility

def run_FIFA_model():
    # We define our variables and bounds
    problem = {
        'num_vars': 3,
        'names': ['mu', 'sigma', 'earnings_ratio'],
        'bounds': [[25000000, 50000000], [2500000, 5000000], [(1 / 20), (1 / 5)]]
    }

    # Set the repetitions, the amount of steps, and the amount of distinct values per variable
    replicates = 1
    max_steps = 15
    distinct_samples = 1





    # Set the outputs (STILL NEED TO IMPLEMENT THIS IN ACTUAL MODEL)
    model_reporters = {"Manager assets": lambda m: m.schedule.get_manager_assets(),
                       "Manager reputation": lambda m: m.schedule.get_manager_reputation()}

    data = {}

    for i, var in enumerate(problem['names']):
        # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples)

        batch = BatchRunner(FIFA_Simulation,
                            max_steps=max_steps,
                            iterations=replicates,
                            variable_parameters={var: samples},
                            model_reporters=model_reporters,
                            display_progress=True)

        batch.run_all()

        data[var] = batch.get_model_vars_dataframe()
        print(data)

if __name__ == "__main__":
    run_FIFA_model()