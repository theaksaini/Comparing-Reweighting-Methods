from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import argparse

import experimental_setup as experimental_setup



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--metrics', type=str)
    args = parser.parse_args()

    ml_models = [RandomForestClassifier, LogisticRegression, XGBClassifier]
    datasets_binary = ['heart_disease', 'student_math', 'student_por', 'creditg', 'titanic', 'us_crime', 'compas_violent', 'nlsy', 'compas', 'pmad_rus_phq', 'pmad_rus_epds']
    experiments1 = ['Equal Weights', 'Deterministic Weights', 'Evolved Weights']

    gp_params_remote = {'pop_size': 20, 'max_gens':50,  'mut_rate':0.1, 'cross_rate':0.8}

    data_dir = './Datasets'

    objective_functions_combinations = {'roc_dpd': ['auroc', 'demographic_parity_difference'],
                                'roc_sfn': ['auroc', 'subgroup_FNR_loss'],
                                'acc_dpd': ['accuracy', 'demographic_parity_difference'],
                                'acc_sfn': ['accuracy', 'subgroup_FNR_loss'],}
     

    experimental_setup.compare_reweighting_methods(ml_models= ml_models[0:1],
                                                   experiments=experiments1,
                                                   task_id_lists=datasets_binary,
                                                   base_save_folder='results',
                                                   data_dir = data_dir,
                                                   num_runs=20,
                                                   objective_functions=objective_functions_combinations[args.metrics],
                                                   objective_functions_weights=[1, -1],
                                                   ga_params=gp_params_remote)

    
if __name__ == '__main__':
    main()
