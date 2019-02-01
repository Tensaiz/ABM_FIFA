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
    'names': ['sheep_reproduce', 'wolf_reproduce', 'wolf_gain_from_food'],
    'bounds': [[0.01, 0.1], [0.01, 0.1], [10, 40]]
                }
        
        # Set the repetitions, the amount of steps, and the amount of distinct values per variable
    replicates = 10
    max_steps = 100
    distinct_samples = 10

    # We get all our samples here
    param_values = saltelli.sample(problem, distinct_samples)

    # READ NOTE BELOW CODE
    batch = BatchRunner(FIFA_Simulation, 
                        max_steps=max_steps,
                        variable_parameters={name:[] for name in problem['names']},
                        model_reporters=model_reporters)

    count = 0
    for i in range(replicates):
        for vals in param_values: 
            # Change parameters that should be integers
            vals = list(vals)
            vals[2] = int(vals[2])

            # Transform to dict with parameter names and their values
            variable_parameters = {}
            for name, val in zip(problem['names'], vals):
                variable_parameters[name] = val

            batch.run_iteration(variable_parameters, tuple(vals), count)
            count += 1

            clear_output()
            print(f'{count / (len(param_values) * (replicates)) * 100:.2f}% done')
        
    data = batch.get_model_vars_dataframe()

    print(data)