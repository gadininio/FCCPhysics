
'''
Use a trained BDT model to compute MVA scores and add them to ROOT files of the analysis samples.

Run with:
    python3 apply_mva.py -e 240 -s loose_full
    python3 apply_mva.py -e 365 -s medium_full

or use a trained model from a different scheme:
    python3 apply_mva.py -e 365 -s medium_full -m loose_full
'''

import uproot
import numpy as np
import pandas as pd
import pickle
import argparse
import ROOT




# Parse command line arguments
parser = argparse.ArgumentParser()
# parser.add_argument("-m", "--model", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/ecm240/bdt_model_example.pkl", help="Input pkl file")
# parser.add_argument("-i", "--input", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/ecm240/bdt_model_example.pkl", help="Input pkl file")
# parser.add_argument("-o", "--outDir", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/ecm240/plots_training", help="Output directory")
# parser.add_argument("-f", "--full", action='store_true', default=False, help="Process full dataset")
# parser.add_argument("-l", "--loose", action='store_true', default=False, help="Process full dataset")
parser.add_argument("-e", "--ecm", default='240', type=str, help="Center-of-mass energy (240 or 365)", choices=['240', '365'])
parser.add_argument("-s", "--scheme", default='loose_ful', type=str, help="Scheme")
parser.add_argument("-m", "--model_scheme", default='', type=str, help="Use trained model from a different scheme.")
args = parser.parse_args()

ecm = args.ecm
scheme = args.scheme


if ecm == '240':
    print("Processing ecm240 samples...")
    sampleList = [
        "wzp6_ee_eeH_HWW_llnunu_ecm240",
        "wzp6_ee_mumuH_HWW_llnunu_ecm240",
        "p8_ee_WW_ecm240",
        # "p8_ee_WW_ee_ecm240",
        # "p8_ee_WW_mumu_ecm240",
        "p8_ee_ZZ_ecm240",
    ]
elif ecm == '365':
    print("Processing ecm365 samples...")
    sampleList = [
        "wzp6_ee_eeH_HWW_ecm365",
        "wzp6_ee_mumuH_HWW_ecm365",
        "p8_ee_WW_ecm365",
        "p8_ee_WW_ee_ecm365",
        "p8_ee_WW_mumu_ecm365",
        "p8_ee_ZZ_ecm365",
        "p8_ee_tt_ecm365"
    ]


model_scheme = scheme if args.model_scheme == "" else args.model_scheme
print(f"Using trained model from scheme: {model_scheme}")

model_path = f'../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{model_scheme}/bdt_model.pkl'
input_path = f'../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{scheme}/preselection/'
output_path = f'../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{scheme}/preselection_with_bdt/'


def apply_bdt(in_file, out_file):
    
    print(f"Applying BDT to {in_file}...")
    
    # --- Step 1: create tree with uproot ---
    # Load preselection ROOT TTree
    file = uproot.open(in_file)
    tree = file["events"]  # replace with your tree name

    # Load BDT input features
    features = [
        "lep0_p", "lep1_p", "lep2_p", "lep3_p", "muons_no", "electrons_no",  # leptons
        "zll_m", "zll_p", "zll_theta", "zll_phi", "zll_recoil_m",  # Z->ll system
        "zll_lep0_p", "zll_lep0_theta", "zll_lep0_phi", "zll_lep1_p", "zll_lep1_theta", "zll_lep1_phi", "zll_leps_dR",  # Z->ll leptons 
        "WW_lep0_p", "WW_lep0_theta", "WW_lep0_phi", "WW_lep1_p", "WW_lep1_theta", "WW_lep1_phi", "WW_leps_dR", # WW leptons
        "WW_mass", "WW_p", "WW_theta", "WW_phi",  # WW system
        "zll_WW_dR",  # Z->ll, WW
        "miss_cosTheta", "miss_energy"  # missing energy
    ]
    df = tree.arrays(features, library="pd")

    # Compute MVA score
    scores = model.predict_proba(df[features])[:, 1]  # for binary classifier

    # Add MVA score as a new branch to dataframe
    df["mva_score"] = scores

    # Write new ROOT file with mva_score
    with uproot.recreate(out_file) as fout:
        fout["events"] = df
    
    
    # --- Step 2: copy TParameters using ROOT ---
    fin = ROOT.TFile.Open(in_file)
    fout_root = ROOT.TFile.Open(out_file, "UPDATE")

    for key in fin.GetListOfKeys():
        obj = fin.Get(key.GetName())
        classname = obj.ClassName()
        if "TTree" not in classname:
            fout_root.cd()
            obj.Write()  # copy TParameter into output file

    fout_root.Close()
    fin.Close()
    
    print(f"MVA scores added to {in_file} and new ROOT file created {out_file}")


if "__main__" == __name__:
    
    # Create output directory if it doesn't exist
    import os
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Load model
    print('Loading BDT model from', model_path)
    with open(model_path, "rb") as f:
        clf = pickle.load(f)
        model = clf['model']
    
    # Apply BDT to each sample
    for sample in sampleList:
        in_file = f"{input_path}/{sample}.root"
        out_file = f"{output_path}/{sample}.root"
        apply_bdt(in_file, out_file)
    
    print("All done!")