import uproot
import numpy as np
import pandas as pd
import pickle
import uproot
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/bdt_model_example.pkl", help="Input pkl file")
# parser.add_argument("-i", "--input", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/bdt_model_example.pkl", help="Input pkl file")
# parser.add_argument("-o", "--outDir", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/plots_training", help="Output directory")
parser.add_argument("-f", "--full", action='store_true', default=False, help="Process full dataset")
parser.add_argument("-l", "--loose", action='store_true', default=False, help="Process full dataset")
args = parser.parse_args()


if args.loose:
    parser.input.replace('mva', 'mva_loose')
    parser.outDir.replace('mva', 'mva_loose')


def apply_bdt(in_file, out_file):
    
    # Load preselection ROOT TTree
    file = uproot.open(in_file)
    tree = file["events"]  # replace with your tree name

    # Load features you trained on
    features = [
        "zll_m", "zll_p", "zll_recoil_m",  # Z->ll system
        "zll_lep1_p", "zll_lep2_p", "zll_lep1_theta", "zll_lep2_theta", "Zll_leps_dR",  # Z->ll leptons 
        "WW_lep1_p", "WW_lep2_p", "WW_lep1_theta", "WW_lep2_theta", "WW_leps_dR",  # WW leptons
        "WW_mass", "WW_p", "WW_theta", "WW_phi",  # WW system
        "miss_cosTheta", "miss_energy"  # missing energy
    ]
    df = tree.arrays(features, library="pd")

    # Load model
    with open(args.model, "rb") as f:
        clf = pickle.load(f)
        model = clf['model']

    # Compute MVA score
    scores = model.predict_proba(df[features])[:, 1]  # for binary classifier

    # Add MVA score as a new branch to dataframe
    df["mva_score"] = scores

    # Write new ROOT file with mva_score
    with uproot.recreate(out_file) as fout:
        fout["events"] = df
    
    print("MVA scores added to ", in_file, " and new ROOT file created ", out_file)


input_path = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if args.loose else ""}/preselection/{"full/" if args.full else ""}'
output_path = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if args.loose else ""}/preselection_with_bdt/{"full/" if args.full else ""}'

# Create output directory if it doesn't exist
import os
if not os.path.exists(output_path):
    os.makedirs(output_path)

apply_bdt(f"{input_path}/wzp6_ee_eeH_HWW_ecm240.root", f"{output_path}/wzp6_ee_eeH_HWW_ecm240.root")
apply_bdt(f"{input_path}/wzp6_ee_mumuH_HWW_ecm240.root", f"{output_path}/wzp6_ee_mumuH_HWW_ecm240.root")
apply_bdt(f"{input_path}/p8_ee_WW_ecm240.root", f"{output_path}/p8_ee_WW_ecm240.root")
apply_bdt(f"{input_path}/p8_ee_ZZ_ecm240.root", f"{output_path}/p8_ee_ZZ_ecm240.root")

print("All done!")