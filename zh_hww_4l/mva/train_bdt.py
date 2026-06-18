
"""
Train a Boosted Decision Tree (BDT) model using XGBoost for the ZH->llWW->4l analysis.

Run:
    python3 train_bdt.py --ecm 240 --scheme loose_full
    python3 train_bdt.py --ecm 365 --scheme loose_full
"""

import uproot
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import ROOT
import pickle
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument("-i", "--input", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/ecm240/bdt_model_example.pkl", help="Input pkl file")
# parser.add_argument("-o", "--outDir", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/ecm240/plots_training", help="Output directory")
# parser.add_argument("-l", "--loose", action='store_true', default=False, help="Process full dataset")
# parser.add_argument("-f", "--labelFontSize", type=int, default=14, help="xaxis and yaxis label font size")
parser.add_argument("-e", "--ecm", default='240', help="Center-of-mass energy (240 or 365)", choices=['240', '365'])
parser.add_argument("-s", "--scheme", default='loose_full', help="Scheme")
args = parser.parse_args()


use_training = True  # should be True for training on the dedicated training samples
ecm = args.ecm
scheme = args.scheme


ROOT.gROOT.SetBatch(True)
# e.g. https://root.cern/doc/master/tmva101__Training_8py.html

def load_process(fIn, variables, target=0, weight_sf=1.):

    f = uproot.open(fIn)
    tree = f["events"]
    #meta = f["meta"]
    #weight = meta.values()[2]/meta.values()[1]*weight_sf
    weight = 1.0/tree.num_entries*weight_sf
    print("Load {} with {} events and weight {}".format(fIn.replace(".root", ""), tree.num_entries, weight))

    df = tree.arrays(variables, library="pd") # convert the signal and background data to pandas DataFrames
    df['target'] = target # add a target column to indicate signal (1) and background (0)
    df['weight'] = weight
    return df


print("Parse inputs")

# Configuration of signal, background, variables, files, ...
variables = [
    "lep0_p", "lep1_p", "lep2_p", "lep3_p", "muons_no", "electrons_no",  # leptons
    "zll_m", "zll_p", "zll_theta", "zll_phi", "zll_recoil_m",  # Z->ll system
    "zll_lep0_p", "zll_lep0_theta", "zll_lep0_phi", "zll_lep1_p", "zll_lep1_theta", "zll_lep1_phi", "zll_leps_dR",  # Z->ll leptons 
    "WW_lep0_p", "WW_lep0_theta", "WW_lep0_phi", "WW_lep1_p", "WW_lep1_theta", "WW_lep1_phi", "WW_leps_dR", # WW leptons
    "WW_mass", "WW_p", "WW_theta", "WW_phi",  # WW system
    "zll_WW_dR",  # Z->ll, WW
    "miss_cosTheta", "miss_energy"  # missing energy
]
weight_sf = 1e9
# weight_sf = 1.0
outputs_path = f'../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{scheme}/'

# Define samples to be used for training/testing
if use_training:
    print("Using training samples")
    
    if ecm == '240':
        sample_list = [
            {'name': 'wzp6_ee_eeH_HWW_llnunu_ecm240', 'target': 1},
            {'name': 'wzp6_ee_mumuH_HWW_llnunu_ecm240', 'target': 1},
            {'name': 'p8_ee_ZZ_llX_ecm240', 'target': 0},
            {'name': 'p8_ee_ZZ_tautauX_ecm240', 'target': 0},
        ]
    elif ecm == '365':
        sample_list = [
            {'name': 'wzp6_ee_eeH_HWW_ecm365', 'target': 1},
            {'name': 'wzp6_ee_mumuH_HWW_ecm365', 'target': 1},
            {'name': 'p8_ee_ZZ_llX_ecm365', 'target': 0},
            {'name': 'p8_ee_ZZ_tautauX_ecm365', 'target': 0},
            {'name': 'p8_ee_WW_ee_ecm365', 'target': 0},
            {'name': 'p8_ee_WW_mumu_ecm365', 'target': 0},
        ]
        
else:
    print("Using full samples")
    
    if ecm == '240':
        sample_list = [
            {'name': 'wzp6_ee_eeH_HWW_llnunu_ecm240', 'target': 1},
            {'name': 'wzp6_ee_mumuH_HWW_llnunu_ecm240', 'target': 1},
            {'name': 'p8_ee_WW_ee_ecm240', 'target': 0},
            {'name': 'p8_ee_WW_mumu_ecm240', 'target': 0},
            {'name': 'p8_ee_ZZ_ecm240', 'target': 0},
        ]
    elif ecm == '365':
        sample_list = [
            {'name': 'wzp6_ee_eeH_HWW_ecm365', 'target': 1},
            {'name': 'wzp6_ee_mumuH_HWW_ecm365', 'target': 1},
            {'name': 'p8_ee_WW_ee_ecm365', 'target': 0},
            {'name': 'p8_ee_WW_mumu_ecm365', 'target': 0},
            {'name': 'p8_ee_ZZ_ecm365', 'target': 0},
            {'name': 'p8_ee_tt_ee_ecm365', 'target': 0},
        ]


# Load signal and background dataframes
df_list = []
for sample in sample_list:
    print(f"Loading sample: {sample['name']}")
    fIn = f"{outputs_path}/preselection/{'training/' if use_training else ''}{sample['name']}.root"
    df = load_process(fIn, variables, weight_sf=weight_sf, target=sample['target'])
    df_list.append(df)
    
# Concatenate the dataframes into a single dataframe
data = pd.concat(df_list, ignore_index=True)

# # Split data in train/test events
# train_data, test_data, train_labels, test_labels, train_weights, test_weights  = train_test_split(
#     data[variables], data['target'], data['weight'], test_size=0.2, random_state=42
# )

# 1. First split: Separate out the dedicated Test set (10% of total)
train_val_data, test_data, train_val_labels, test_labels, train_val_weights, test_weights = train_test_split(
    data[variables], data['target'], data['weight'], test_size=0.1, random_state=42
)

# 2. Second split: Divide the remaining 90% into Train (72% of total) and Val (18% of total)
train_data, val_data, train_labels, val_labels, train_weights, val_weights = train_test_split(
    train_val_data, train_val_labels, train_val_weights, test_size=0.2, random_state=42
)

# conversion to numpy needed to have default feature_names (fN), needed for conversion to TMVA
train_data = train_data.to_numpy()
val_data = val_data.to_numpy()
test_data = test_data.to_numpy()
train_labels = train_labels.to_numpy()
val_labels = val_labels.to_numpy()
test_labels = test_labels.to_numpy()
train_weights = train_weights.to_numpy()
val_weights = val_weights.to_numpy()
test_weights = test_weights.to_numpy()

# Set hyperparameters for the XGBoost model
params = {
    'objective': 'binary:logistic',
    'eval_metric': 'logloss',
    'eta': 0.1,
    'max_depth': 5,
    'subsample': 0.5,
    'colsample_bytree': 0.5,
    'seed': 42,
    'n_estimators': 350, # low number for testing purposes (default 350)
    'early_stopping_rounds': 25,
    'num_rounds': 20,
    'learning_rate': 0.20,
    'gamma': 3,
    'min_child_weight': 10,
    'max_delta_step': 0,
}


# Train the XGBoost model
print("Start training")
# eval_set = [(train_data, train_labels), (test_data, test_labels)]
eval_set = [(train_data, train_labels), (val_data, val_labels)]
bdt = xgb.XGBClassifier(**params)
bdt.fit(train_data, train_labels, verbose=True, eval_set=eval_set, sample_weight=train_weights)


# Export model (to ROOT and pkl)
print("Export model")
fOutName = f"{outputs_path}/bdt_model.root"
ROOT.TMVA.Experimental.SaveXGBoost(bdt, "bdt_model", fOutName, num_inputs=len(variables))

# Append the input variable names to the same ROOT file
variables_ = ROOT.TList()
for var in variables:
     variables_.Add(ROOT.TObjString(var))
fOut = ROOT.TFile(fOutName, "UPDATE")
fOut.WriteObject(variables_, "variables")
print(f"Saved model to {fOutName}")

# Save everything (mode, data, variable names) as pickle for evaluation and plotting (see evaluate_bdt.py)
print("Export pickle")
pkl_output_name = fOutName.replace(".root", ".pkl")
save = {}
save['model'] = bdt
save['train_data'] = train_data
save['val_data'] = val_data
save['test_data'] = test_data
save['train_labels'] = train_labels
save['val_labels'] = val_labels
save['test_labels'] = test_labels
save['variables'] = variables
pickle.dump(save, open(pkl_output_name, "wb"))
print(f"Saved model and data to {pkl_output_name}")

# Evaluate the model and make plots
print("Evaluating model and making plots...")
import subprocess
subprocess.run(["python3", "evaluate_bdt.py", "--input", pkl_output_name, "--outDir", f"{outputs_path}/plots_training"])
