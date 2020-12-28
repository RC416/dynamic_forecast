# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 22:18:40 2020

@author: Ray
"""

from classes_and_functions import Patient
from drug_and_state_data import untreated, drug_1, drug_2, drug_3


'''
# single patient simulation

patient_1 = Patient(drug_options=[drug_1, drug_2, drug_3], state_options=[untreated])

result, result_by_line = patient_1.simulate(start_period=0, end_period=20)
'''

'''
# multiple patient simulation for one period

# create dummy patient to get empty results tables
dummy = Patient(drug_options=[drug_1, drug_2, drug_3], state_options=[untreated])
results, results_by_line = dummy.simulate(start_period=20, end_period=20) # use start_period equal to end period

# choose number of patients, start period and end period
n_patients = 100
start_period = 0
end_period = 20

for n in range(n_patients):
    
    # initialize patient and run simulation
    patient = Patient(drug_options=[drug_1, drug_2, drug_3], state_options=[untreated])
    result, result_by_line = patient.simulate(start_period=start_period, end_period=end_period)
    
    # add single patient result to results tables
    # surprising that this syntax works - you can simply can add two dfs: df1 + df2
    results += result 
    results_by_line += result_by_line
'''
  


# multiple patient simulation for multiple periods

# create dummy patient to get empty results tables
dummy = Patient(drug_options=[drug_1, drug_2, drug_3], state_options=[untreated])
results, results_by_line = dummy.simulate(start_period=20, end_period=20) # use start_period equal to end period

incident_patients = [1000 for x in range(20)] # incident patients in each period
start_period = 0
end_period = 20

for period in range(end_period):
    
    for n in range(incident_patients[period]):
        
        # initialize patient and run simulation
        patient = Patient(drug_options=[drug_1, drug_2, drug_3], state_options=[untreated])
        result, result_by_line = patient.simulate(start_period=period,
                                                  end_period=end_period) # use start_period=current_period

    
        # add single patient result to results tables
        results += result 
        results_by_line += result_by_line











