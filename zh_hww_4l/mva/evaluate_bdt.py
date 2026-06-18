
'''
Run evaluation plots for a trained BDT model, after using train_bdt.py to train it.
'''

import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/ecm240/bdt_model_example.pkl", help="Input pkl file")
parser.add_argument("-o", "--outDir", type=str, default="../../../outputs/higgs/zh_hww_4l/mva/ecm240/plots_training", help="Output directory")
parser.add_argument("-f", "--labelFontSize", type=int, default=14, help="xaxis and yaxis label font size")
# parser.add_argument("-l", "--loose", action='store_true', default=False, help="Process full dataset")
# parser.add_argument("-e", "--ecm", default='240', type=str, help="Center-of-mass energy (240 or 365)", choices=['240', '365'])
args = parser.parse_args()

# if args.loose:
#     if 'mva/' in args.input:
#         args.input = args.input.replace('mva', 'mva_loose')
#     if 'mva/' in args.outDir:
#         args.outDir = args.outDir.replace('mva', 'mva_loose')

# if args.ecm == '365':
#     if 'ecm240' in args.input:
#         args.input = args.input.replace('ecm240', 'ecm365')
#     if 'ecm240' in args.outDir:
#         args.outDir = args.outDir.replace('ecm240', 'ecm365')


def plot_roc():

    train_probs = bdt.predict_proba(train_data)
    train_preds = train_probs[:,1]
    train_fpr, train_tpr, threshold = sklearn.metrics.roc_curve(train_labels, train_preds)
    train_roc_auc = sklearn.metrics.auc(train_fpr, train_tpr)

    test_probs = bdt.predict_proba(test_data)
    test_preds = test_probs[:,1]
    test_fpr, test_tpr, threshold = sklearn.metrics.roc_curve(test_labels, test_preds)
    test_roc_auc = sklearn.metrics.auc(test_fpr, test_tpr)

    # Plot the ROC curve (bkg eff. vs sig eff.)
    plt.figure(figsize=(8, 6))
    plt.plot(train_fpr, train_tpr, color='blue', label=f"Training ROC (AUC = {train_roc_auc:.2%})")
    plt.plot(test_fpr, test_tpr, color='red', label=f"Testing ROC (AUC = {test_roc_auc:.2%})")
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random Guess')
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    plt.xlabel('Background efficiency (FPR)', fontsize=args.labelFontSize)
    plt.ylabel('Signal efficiency (TPR)', fontsize=args.labelFontSize)
    # set larger xlabel font size
    # plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.grid()
    # plt.savefig(f"{outDir}/roc.png")
    plt.savefig(f"{outDir}/roc.pdf")
    plt.close()
    
    # Plot the ROC curve (bkg rejection (1/bkg eff.) vs sig eff.)
    # Note: for bkg eff. = 0, we set bkg rej. to a large number (e.g. 1e6) to avoid infinite values in the plot
    # train_fpr_safe = np.where(train_fpr == 0, 1e-6, train_fpr)
    # test_fpr_safe = np.where(test_fpr == 0, 1e-6, test_fpr)
    train_bkg_rej = 1./train_fpr
    test_bkg_rej = 1./test_fpr
    train_bkg_rej[train_fpr == 0] = np.inf
    test_bkg_rej[test_fpr == 0] = np.inf
    
    plt.figure(figsize=(8, 6))
    plt.plot(train_tpr, train_bkg_rej, color='blue', label=f"Training ROC (AUC = {train_roc_auc:.2%})")
    plt.plot(test_tpr, test_bkg_rej, color='red', label=f"Testing ROC (AUC = {test_roc_auc:.2%})")
    plt.xlabel('Signal efficiency (TPR)', fontsize=args.labelFontSize)
    plt.ylabel('Background rejection (1/FPR)', fontsize=args.labelFontSize)
    plt.yscale('log')
    # plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.grid()
    # plt.savefig(f"{outDir}/roc.png")
    plt.savefig(f"{outDir}/roc_rej.pdf")
    plt.close()    
    
    print(f"Training AUC: {train_roc_auc:.6f}")
    print(f"Testing AUC: {test_roc_auc:.6f}")


def plot_score():

    train_predictions = bdt.predict_proba(train_data)[:,1]
    test_predictions = bdt.predict_proba(test_data)[:,1]

    # Separate the data into signal and background samples
    train_signal_scores = train_predictions[train_labels == 1]
    train_background_scores = train_predictions[train_labels == 0]
    test_signal_scores = test_predictions[test_labels == 1]
    test_background_scores = test_predictions[test_labels == 0]

    # Plot the BDT scores for signal and background events (linear scale)
    plt.figure(figsize=(8, 6))
    plt.hist(train_signal_scores, bins=50, range=(0, 1), histtype='step', label='Training Signal', color='blue', density=True)
    plt.hist(train_background_scores, bins=50, range=(0, 1), histtype='step', label='Training Background', color='red', density=True)
    plt.hist(test_signal_scores, bins=50, range=(0, 1), histtype='step', label='Testing Signal', color='blue', linestyle='dashed', density=True)
    plt.hist(test_background_scores, bins=50, range=(0, 1), histtype='step', label='Testing Background', color='red', linestyle='dashed', density=True)
    plt.xlabel('BDT score', fontsize=args.labelFontSize)
    plt.ylabel('Number of events (normalized)', fontsize=args.labelFontSize)
    # plt.title('BDT Score Distribution')
    plt.legend()
    plt.grid()
    # plt.savefig(f"{outDir}/score.png")
    plt.savefig(f"{outDir}/score.pdf")
    plt.close()
    
    # Plot the BDT scores for signal and background events (log scale)
    plt.figure(figsize=(8, 6))
    plt.hist(train_signal_scores, bins=50, range=(0, 1), histtype='step', label='Training Signal', color='blue', density=True)
    plt.hist(train_background_scores, bins=50, range=(0, 1), histtype='step', label='Training Background', color='red', density=True)
    plt.hist(test_signal_scores, bins=50, range=(0, 1), histtype='step', label='Testing Signal', color='blue', linestyle='dashed', density=True)
    plt.hist(test_background_scores, bins=50, range=(0, 1), histtype='step', label='Testing Background', color='red', linestyle='dashed', density=True)
    plt.xlabel('BDT score', fontsize=args.labelFontSize)
    plt.ylabel('Number of events (normalized)', fontsize=args.labelFontSize)
    plt.yscale('log')
    # plt.title('BDT Score Distribution')
    plt.legend()
    plt.grid()
    # plt.savefig(f"{outDir}/score.png")
    plt.savefig(f"{outDir}/score_log.pdf")
    plt.close()


def plot_importance():

    fig, ax = plt.subplots(figsize=(12, 6))

    importance = bdt.get_booster().get_score(importance_type='weight')
    sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=False)
    sorted_indices = [int(x[0][1:]) for x in sorted_importance] # sorted indices

    # Get the sorted variable names and their corresponding importances
    sorted_vars = [variables[i] for i in sorted_indices]
    sorted_values = [x[1] for x in sorted_importance]

    # Create a DataFrame and plot the feature importances
    importance_df = pd.DataFrame({'Variable': sorted_vars, 'Importance': sorted_values})
    importance_df.plot(kind='barh', x='Variable', y='Importance', legend=None, ax=ax)
    ax.set_xlabel('BDT score', fontsize=args.labelFontSize)
    ax.set_ylabel('Variable', fontsize=args.labelFontSize)
    # ax.set_title("BDT variable scores", fontsize=16)
    # plt.savefig(f"{outDir}/importance.png")
    plt.savefig(f"{outDir}/importance.pdf")
    plt.close()



if __name__ == "__main__":
    outDir = args.outDir

    # Create output directory if it doesn't exist
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    res = pickle.load(open(args.input, "rb"))
    bdt = res['model']
    train_data = res['train_data']
    val_data = res['val_data']
    test_data = res['test_data']
    train_labels = res['train_labels']
    val_labels = res['val_labels']
    test_labels = res['test_labels']
    variables = res['variables']

    plot_score()
    plot_roc()
    plot_importance()