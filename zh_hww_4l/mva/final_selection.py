'''
This script produces histograms of the MVA scores and other relevant variables for further analysis from the ROOT files produced at the preselection level (after the BDT training and applying the BDT score to the analysis events).

It generates two sets of histograms for the variables defined in histoList according to the cuts defined in cutList:
    1. before applying any cut on the MVA score (sel0).
    2. after applying a cut on the MVA score (sel1).

Run with:
    ecm=240 scheme=loose_full fccanalysis final final_selection.py
    ecm=365 scheme=loose_full fccanalysis final final_selection.py
'''


import os
ecm = os.environ.get("ecm", "240")  # '240' or '365'
scheme = os.environ.get("scheme", "loose_full")


# Input directory where the files produced at the pre-selection level are
inputDir = f'../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{scheme}/preselection_with_bdt/'

# Input directory where the files produced at the pre-selection level are
# Optional: output directory, default is local running directory
outputDir = f'../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{scheme}/final_selection/'

# if no processList or empty dictionary provided, run over all ROOT files in the input directory
processList = {}

# Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

# If a training sample is used for the fit (the rest being the  analysis samples), provide here the meta information of this training sample (number of events, sum of weights, cross-section, k-factor, matching efficiency). This is needed to properly scale the training sample in the final fit.
# procDictAdd={"MySample_p8_ee_ZH_ecm240":{"numberOfEvents": 10000000, "sumOfWeights": 10000000, "crossSection": 0.201868, "kfactor": 1.0, "matchingEfficiency": 1.0}}


# Number of CPUs to use
nCPUS = -1

# produces ROOT TTrees, default is False
doTree = False


# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 10.8e6 if ecm == '240' else 3e6  # 10.8 /ab for 240 GeV, 3 /ab for 365 GeV

saveTabular = True

# Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    "sel0": "1==1",
    "sel1": "mva_score > 0.5",
}


# Dictionary for the ouput variable/hitograms.
# - The key is the name of the variable in the output files.
# - "cols" is the name of the variable in the input file
# - "title" is the x-axis label of the histogram
# - "bin" is (nbins,xmin,xmax)

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.


histoList = {
    "mva_score":{"cols": ["mva_score"], "title": "MVA score", "bins": [(100,0,1)]},
    "zll_m":{"cols": ["zll_m"], "title": "m_{Z} (GeV)", "bins": [(250,0,250)]},
    "zll_p":{"cols": ["zll_p"], "title": "p_{Z} (GeV)", "bins": [(250,0,250)]},
    "zll_recoil_m":{"cols": ["zll_recoil_m"], "title": "Recoil (GeV)", "bins": [(250,0,250)]},
    "zll_recoil_m_final":{"cols": ["zll_recoil_m"], "title": "Recoil (GeV)", "bins": [(200,120,140)]},
}

# add all variables to plot here!