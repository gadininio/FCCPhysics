
'''
Use a trained BDT model to compute MVA scores and add them to ROOT files.
'''

import uproot
import numpy as np
import pandas as pd
import pickle
import argparse
import ROOT


# Parse command line arguments
parser = argparse.ArgumentParser()
# parser.add_argument("-m", "--model", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/bdt_model_example.pkl", help="Input pkl file")
# parser.add_argument("-i", "--input", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/bdt_model_example.pkl", help="Input pkl file")
# parser.add_argument("-o", "--outDir", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/plots_training", help="Output directory")
parser.add_argument("-f", "--full", action='store_true', default=False, help="Process full dataset")
parser.add_argument("-l", "--loose", action='store_true', default=False, help="Process full dataset")
args = parser.parse_args()


# if args.loose:
#     parser.input.replace('mva', 'mva_loose')
#     parser.outDir.replace('mva', 'mva_loose')


model_path = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if args.loose else ""}/bdt_model_example.pkl'
input_path = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if args.loose else ""}/preselection/{"full/" if args.full else ""}'
output_path = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if args.loose else ""}/preselection_with_bdt/{"full/" if args.full else ""}'

# Create output directory if it doesn't exist
import os
if not os.path.exists(output_path):
    os.makedirs(output_path)


def apply_bdt(in_file, out_file):
    
    # --- Step 1: create tree with uproot ---
    # Load preselection ROOT TTree
    file = uproot.open(in_file)
    tree = file["events"]  # replace with your tree name

    # Load features you trained on
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

    # Load model
    with open(model_path, "rb") as f:
        clf = pickle.load(f)
        model = clf['model']

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
    
    
    print("MVA scores added to ", in_file, " and new ROOT file created ", out_file)


apply_bdt(f"{input_path}/wzp6_ee_eeH_HWW_ecm240.root", f"{output_path}/wzp6_ee_eeH_HWW_ecm240.root")
apply_bdt(f"{input_path}/wzp6_ee_mumuH_HWW_ecm240.root", f"{output_path}/wzp6_ee_mumuH_HWW_ecm240.root")
apply_bdt(f"{input_path}/p8_ee_WW_ecm240.root", f"{output_path}/p8_ee_WW_ecm240.root")
apply_bdt(f"{input_path}/p8_ee_ZZ_ecm240.root", f"{output_path}/p8_ee_ZZ_ecm240.root")

print("All done!")