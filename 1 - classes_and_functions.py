# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 20:06:02 2019

@author: Ray
"""

import random
import pandas as pd


class Patient:
    
    def __init__(self, drug_options=[], state_options=[]):
        
        self.drugs = drug_options 
        self.drugs_taken = []
        self.drugs_not_taken = drug_options[:] # create a shallow copy so self.drugs does not get modified
        self.current_drug = None # also includes states
        
        self.line_of_treatment = 1 # start at first line, augments upon failing to continue
        
        self.states = state_options
        
        # set up counter to track periods survived on each drug/state
        # survival count tracks total periods survived
        # continue count tracks total periods continued, reset for states not for drugs
        self.experience_counter = pd.DataFrame(data=0, index=self.states+self.drugs,
                                               columns=['survival count', 'continue count'])
        
    def roll_survival(self):
        # return 1 if patient survives, return 0 if dead/discontinue
        # uses survival rate for current drug for line and at relative period
        survival_period = self.experience_counter.loc[self.current_drug, 'survival count']
        
        # probability of surviving the period, according to line of treatment & relative period
        survival_prob = self.current_drug.survival_rates.loc[self.line_of_treatment, str(survival_period)]
        # probability of death or discontinuing this period
        death_prob = 1 - survival_prob
        
        outcome = random.choices(population=[1,0], weights=[survival_prob, death_prob])
        
        # augment experience counter if survival achived
        if outcome[0] == 1:
            self.experience_counter.loc[self.current_drug, 'survival count'] += 1
                
        # if patient dies/discontinues (outcome = 0), simulation should end
        return outcome[0]
    
    
    def roll_continue(self):
        # return 1 if patient continues on the drug after having survied
        # uses continuation rate for current drug for line and at relative period
        continue_period = self.experience_counter.loc[self.current_drug, 'continue count']
        
        # probability of continuing through current period
        continue_prob = self.current_drug.continuation_rates.loc[self.line_of_treatment, str(continue_period)]
        # probability of not continuing
        not_continue_prob = 1 - continue_prob
        
        outcome = random.choices(population=[1,0], weights=[continue_prob, not_continue_prob])
        
        # increase experience counter if patient continues on drug
        if outcome[0] == 1:
            self.experience_counter.loc[self.current_drug, 'continue count'] += 1        
        
        if outcome[0] == 0 and not self.current_drug.is_drug:
            self.experience_counter.loc[self.current_drug, 'continue count'] = 0

        return outcome[0]
    
    
    def select_drug(self, current_period):
        # roll from available drugs and states
        
        # select only those that have launched
        launched_drugs = [self.drugs[n] for n in range(len(self.drugs))
                          if self.drugs[n].launch_period <= current_period]

        launched_states = [self.states[n] for n in range(len(self.states))
                           if self.states[n].launch_period <= current_period]

        # select from an available drug or state        
        population = launched_drugs + launched_states
              
        # weights according to market shares     
        drug_weights = [drug.market_share.loc[self.line_of_treatment, str(current_period)] for drug in launched_drugs]
        state_weights = [state.market_share.loc[self.line_of_treatment, str(current_period)] for state in launched_states]
                       
        weights = drug_weights + state_weights
     
        outcome = random.choices(population=population, weights=weights)
        
        # if drug is already taken, roll another drug
        if outcome[0] in self.drugs_taken:
            
            # create list of remaining drugs
            remaining_drugs = [self.drugs_not_taken[n] for n in range(len(self.drugs_not_taken))
                               if self.drugs_not_taken[n].launch_period <= current_period]
            # get probabilities
            drug_weights = [drug.market_share.loc[self.line_of_treatment, str(current_period)] 
                            for drug in remaining_drugs]
            
            # if there are remaining drugs, pick one
            if remaining_drugs:
                outcome = random.choices(population=remaining_drugs, weights=drug_weights)
            
            # if there are no remaining drugs, pick a state
            else:
                outcome = random.choices(population=launched_states, weights = state_weights)
            
        # update lists to reflect taking new drug, don't do this for States
        # States (untreated) remain options throughout all periods
        # increase line of treatment 
        if outcome[0].is_drug:
            self.drugs_taken.append(outcome[0])
            self.drugs_not_taken.remove(outcome[0])
        
        self.current_drug = outcome[0] # includes states
        
        return outcome[0]
    
    
    def simulate(self, start_period, end_period):
        # simulates a single patient's journey 
        # calls .select_drug, .roll_survival and .roll_continue
        # returns results as two dataframes
        
        drugs = self.states + self.drugs
        lines = [x+1 for x in range(1+len(self.drugs))]
        
        drug_index = [drug for drug in drugs for n in range(len(lines))]
        line_index = [x+1 for line in lines for x in range(len(drugs))]
        
        # create results table, single index with each drug/state
        results = pd.DataFrame(data=0, index=drugs, columns=range(end_period))
        
        # create results table with double index for each drug/state and each line
        results_by_line = pd.DataFrame(index=[drug_index, line_index], columns=range(end_period))
        # initiate with each cell=0 (data=0 initiation does not work with double index)
        results_by_line.fillna(0, inplace=True)
        
        period = start_period
        
        # key simulation code
        while period < end_period:
            
            if self.current_drug == None:
                # if patient is not on a drug/state, pick one
                self.select_drug(period)
            
            else:
                # check survival
                if self.roll_survival() == 1:
                    
                    # check if patient continues on drug
                    if self.roll_continue() == 1:
                        # record result
                        results.loc[self.current_drug, period] += 1
                        results_by_line.loc[(self.current_drug, self.line_of_treatment), period] += 1
                        
                        # move forward one period
                        period += 1
                    
                    else:
                        # if patient fails to continue
                        
                        if self.current_drug.is_drug:
                            # increase line of treatment if failed a drug
                            self.line_of_treatment += 1
                        
                        # clear curent drug
                        self.current_drug = None
        
                else:
                    # if patient does not survive, end simulation
                    period = end_period
        
        # return the two results dataframes
        return results, results_by_line
    
    
    
class Drug:
    
    def __init__(self, name, market_share, continuation_rates, survival_rates, launch_period):
        # market_share, continuate_rates, survival_rates are dataframes
        self.name = name # text for drug name
        
        self.market_share = market_share # prob of talking drug if no competition, and bid versus others
        self.continuation_rates = continuation_rates # prob of continuing treatment in each period
        self.survival_rates = survival_rates # prob of dying/stopping treatment in each period

        self.launch_period = launch_period # period when drug becomes available
        
        self.is_drug = True # to differentiate from states
        
    def __repr__(self):
        # how the object is referenced in lists and other calls
        # should be unique. __str__ is another option
        return self.name



class State:
    
    def __init__(self, name, market_share, continuation_rates, survival_rates, launch_period=0):
        # identical to drug class, but used for states where no drug is consumed
        # expected state: 'untreated' for prior to drugs being available and waiting between lines for drug approvals
        # treated separately so that "line of treatment" and other parameters are not messed up by states
        # states always remain treatment options and patients can return to states
        self.name = name # text for state name
        
        self.market_share = market_share # prob of talking drug if no competition, and bid versus others
        self.continuation_rates = continuation_rates # prob of continuing in state for each period
        self.survival_rates = survival_rates # prob of dying/stopping treatment in each period

        self.launch_period = launch_period # period when state becomes available
        
        self.is_drug = False # to differentiate from Drug objects
        
    def __repr__(self):
        # how the object is referenced in lists and other calls
        # should be unique. __str__ is another option
        return self.name
