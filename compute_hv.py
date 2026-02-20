import utils
import os
import numpy as np
import pandas as pd
from deap.tools._hypervolume import pyhv

current_directory = os.getcwd()
print(f"Current working directory: {current_directory}")

# Hypervolume of pareto front for different datasets
def save_hv_results(base_result_folder, hv_folder, taskid, experiments, objectives, runs):
    if not os.path.isdir(hv_folder):
        print(f"Creating folder to save HV values: {hv_folder}")
        os.makedirs(hv_folder)
    hv_test_df = pd.DataFrame(columns = ['rep','hv', 'dataset', 'exp', 'num_pts', 'avg_pred_perf', 'avg_fair_perf']) # results on test data

    for exp in experiments:
        print("Processing experiment:", exp)
        for rep in range(runs):
            print("Processing run:", rep)
        
            save_folder = f"{base_result_folder}/{taskid}_{rep}_{exp}"
            # If hv_values file exist, take the values from there.
            if os.path.exists(f"{save_folder}/hv_values.pkl"):
                with open(f"{save_folder}/hv_values.pkl",'rb') as file:
                    hv_file = pd.read_pickle(file)
                hv_test_df.loc[len(hv_test_df.index)] = {'rep': rep, 'hv' : hv_file['test_hv']['hv'], 'dataset' : taskid, 'exp' : exp, 'num_pts':hv_file['test_hv']['num_pts'],'avg_pred_perf':hv_file['test_hv']['avg_pred_perf'], 'avg_fair_perf':hv_file['test_hv']['avg_fair_perf']}
                
            else:
                x_vals = [] # auroc, etc
                y_vals = [] # fnr, etc.

                results_file = f"{save_folder}/scores.pkl"
                with open(results_file,'rb') as file:
                    this_df = pd.read_pickle(file)
        
                test_pred_perf = this_df[objectives[0]].to_numpy()
                x_vals = 1-test_pred_perf
                y_vals = this_df[objectives[1]].to_numpy()

                PF = utils.front(x_vals,y_vals)
                pf_x = [x_vals[i] for i in PF]
                pf_y = [y_vals[i] for i in PF]
                hv = pyhv.hypervolume([(xi,yi) for xi,yi in zip(pf_x,pf_y)], ref=np.array([1,1]))
                avg_pred_perf = np.mean([1-x for x in pf_x])
                avg_fair_perf = np.mean(pf_y)
                hv_test_df.loc[len(hv_test_df.index)] = {'rep': rep, 'hv' : hv, 'dataset' : taskid, 'exp' : exp, 'num_pts':len(pf_x),'avg_pred_perf':avg_pred_perf, 'avg_fair_perf':avg_fair_perf}

    hv_test_file = f"{hv_folder}/hv_test_{taskid}.csv"
    hv_test_df.to_csv(hv_test_file)

    return hv_test_df


def analyze_hv(task_ids=None, experiments=None, results_folder=None, hv_folder=None, objective_functions=None):

    sample_file = None
    for dirpath, dirnames, filenames in os.walk(results_folder):
        if 'failed.pkl' in filenames:
            sample_file = os.path.join(dirpath, 'failed.pkl')
            with open(sample_file,'rb') as file:
                failed_df = pd.read_pickle(file)
            print(failed_df)
            print(failed_df["trace"])
            break

    files_dir = [
        f for f in os.listdir(results_folder) if os.path.isdir(os.path.join(results_folder, f))
    ]
    print(files_dir)

    for task_id in task_ids:
        print(f"Reading files related to {task_id}")
        num_completed = {}
        for exp in experiments:
            num_completed[exp] = 0
            for rep in range(20):
                save_folder = f"{results_folder}/RandomForestClassifier/{task_id}_{rep}_{exp}"
                if os.path.exists(f"{save_folder}/scores.pkl"):
                    num_completed[exp] += 1
        print(num_completed)

    for task_id in task_ids:
        print(f"Reading files related to {task_id}")
        csv_test = f"{hv_folder}/hv_test_{task_id}.csv"
        if os.path.exists(csv_test):
            df_test = pd.read_csv(f"{hv_folder}/hv_test_{task_id}.csv")
            if len(df_test) == 60:
                print(f"Already computed hv for {task_id}. Skipping.")
                continue
            else:
                print(f"Found incomplete hv for {task_id}. Recomputing.")
                save_hv_results(f'{results_folder}/{files_dir[0]}', hv_folder, task_id, experiments,objective_functions, 20)
        else:
            print('Processing task_id:', task_id)
            save_hv_results(f'{results_folder}/{files_dir[0]}', hv_folder, task_id, experiments,objective_functions, 20)

    
def generate_combined_file(hv_folder, task_ids):
    # List of CSV files to be merged
    csv_files = [f"{hv_folder}/hv_test_{task_id}.csv" for task_id in task_ids]

    # Read and concatenate all CSV files into one dataframe
    df_list= []
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"File {csv_file} does not exist. Skipping.")
            continue
        else:
            print(f"Reading file {csv_file}")
            df = pd.read_csv(csv_file)
            print("Length of dataframe:", len(df))
            df_list.append(df)

    merged_df = pd.concat(df_list, ignore_index=True)    # Concatenating DataFrames

    # Save the merged dataframe into a new CSV file
    output_file = f"{hv_folder}/hv_test.csv"
    merged_df.to_csv(output_file, index=False)

    print(f"Merged CSV file saved as {output_file}")


# from each of the folders hv_acc_dpd, hv_roc_dpd, hv_acc_sfn, hv_roc_sfn
def combine_all_hv(input_dirs, output_file):
    combined_df = pd.DataFrame()

    for input_dir in input_dirs:
        for filename in os.listdir(input_dir):
            if filename.endswith('hv_test.csv'):
                file_path = os.path.join(input_dir, filename)
                df = pd.read_csv(file_path)
                # add a column to for objective1 and objective2 
                # objective1 = 0 for acc, 1 for roc
                # objective2 = 0 for dpd, 1 for sfn
                if 'acc' in input_dir:
                    df['objective1'] = 0
                else:
                    df['objective1'] = 1
                if 'dpd' in input_dir:
                    df['objective2'] = 0
                else:
                    df['objective2'] = 1
                combined_df = pd.concat([combined_df, df], ignore_index=True)

    combined_df.to_csv(output_file, index=False)


def main():
    task_ids = ['heart_disease', 'student_math', 'student_por', 'creditg', 'titanic', 'us_crime', 'compas_violent', 'nlsy', 'compas', 'pmad_rus_phq', 'pmad_rus_epds']
    experiments = ['Equal Weights',
                'Deterministic Weights',
                'Evolved Weights']
    
    objective_functions_dict = {'Results/roc_dpd': ['auroc', 'demographic_parity_difference'],
                                'Results/roc_sfn': ['auroc', 'subgroup_FNR_loss'],
                                'Results/acc_dpd': ['accuracy', 'demographic_parity_difference'],
                                'Results/acc_sfn': ['accuracy', 'subgroup_FNR_loss'],}

    for results_folder in objective_functions_dict.keys():
        print(f"Processing results folder: {results_folder}")
        hv_folder = f"Results/hv_{results_folder.split('/')[1]}"
        analyze_hv(task_ids=task_ids, experiments=experiments, results_folder=results_folder, hv_folder=hv_folder, objective_functions=objective_functions_dict[results_folder])
    
        generate_combined_file(hv_folder, task_ids)

    input_dirs = [
        'Results/hv_acc_dpd',
        'Results/hv_roc_dpd',
        'Results/hv_acc_sfn',
        'Results/hv_roc_sfn'
    ]
    output_file = 'all_hv.csv'
    combine_all_hv(input_dirs, output_file)


if __name__ == '__main__':
    main()