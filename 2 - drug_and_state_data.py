# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 22:35:56 2020

Initalize drugs/states here 

@author: Ray
"""

from classes_and_functions import Drug, State
import pandas as pd

# set up drugs

# read market share, survival rates and continuation rates for each drug/state
path = r'C:\Users\Ray\OneDrive\Mini projects\Patient flow forecast\forecast inputs csv' # can't end in \ character

untreated_ms = pd.read_csv(path + r'\ms untreated.csv', index_col=0)
untreated_sr = pd.read_csv(path + r'\sr untreated.csv', index_col=0)
untreated_cr = pd.read_csv(path + r'\cr untreated.csv', index_col=0)

drug_1_ms = pd.read_csv(path + r'\ms drug 1.csv', index_col=0)
drug_1_sr = pd.read_csv(path + r'\sr drug 1.csv', index_col=0)
drug_1_cr = pd.read_csv(path + r'\cr drug 1.csv', index_col=0)

drug_2_ms = pd.read_csv(path + r'\ms drug 2.csv', index_col=0)
drug_2_sr = pd.read_csv(path + r'\sr drug 2.csv', index_col=0)
drug_2_cr = pd.read_csv(path + r'\cr drug 2.csv', index_col=0)

drug_3_ms = pd.read_csv(path + r'\ms drug 3.csv', index_col=0)
drug_3_sr = pd.read_csv(path + r'\sr drug 3.csv', index_col=0)
drug_3_cr = pd.read_csv(path + r'\cr drug 3.csv', index_col=0)


# initialize drugs and states

untreated = State('untreated', market_share=untreated_ms, continuation_rates=untreated_cr,
                  survival_rates=untreated_sr, launch_period=0)

drug_1 = Drug('drug 1', market_share=drug_1_ms, continuation_rates=drug_1_cr,
              survival_rates=drug_1_sr, launch_period=2)

drug_2 = Drug('drug 2', market_share=drug_2_ms, continuation_rates=drug_2_cr,
              survival_rates=drug_2_sr, launch_period=7)

drug_3 = Drug('drug 3', market_share=drug_3_ms, continuation_rates=drug_3_cr,
              survival_rates=drug_3_sr, launch_period=15)