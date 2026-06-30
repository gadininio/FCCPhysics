'''
Run with:
    ecm=240 scheme=loose_full fccanalysis combine combine.py
    ecm=365 scheme=loose_full fccanalysis combine combine.py
'''


import ROOT
import os


ecm = os.environ.get("ecm", "240")  # '240' or '365'
scheme = os.environ.get("scheme", "loose_full")


# # get histograms from histmaker step
# inputDir       = f"../../outputs/higgs/zh_hww_4l/hists/{path_full if is_full else ''}/"

# get histograms from final step, selection to be defined
inputDir       = f'../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{scheme}/final_selection/'
selection      = "sel0"

intLumi        = 1.0 # assume histograms are scaled in previous step
outputDir      = f'../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{scheme}/combine/{selection}'
mc_stats       = True
rebin          = 10


if ecm == '240':
    sig_procs = {'sig':['wzp6_ee_eeH_HWW_llnunu_ecm240', 'wzp6_ee_mumuH_HWW_llnunu_ecm240']}
    bkg_procs = {'bkg':['p8_ee_WW_ee_ecm240', 'p8_ee_WW_mumu_ecm240', 'p8_ee_ZZ_ecm240']}
    
elif ecm == '365':
    # if 'inclWWInFit' in scheme:
    print('Using inclusive WW in fit.')
    WW_samples = ['p8_ee_WW_ecm365']
    # else:
    #     print('Using WW->ee + WW->mumu in fit.')
    #     WW_samples = ['p8_ee_WW_ee_ecm365', 'p8_ee_WW_mumu_ecm365']
        
    sig_procs = {'sig':['wzp6_ee_eeH_HWW_ecm365', 'wzp6_ee_mumuH_HWW_ecm365']}
    # bkg_procs = {'bkg':['p8_ee_WW_ee_ecm365', 'p8_ee_WW_mumu_ecm365', 'p8_ee_ZZ_ecm365', 'p8_ee_tt_ecm365']}
    bkg_procs = {'bkg':['p8_ee_ZZ_ecm365', 'p8_ee_tt_ecm365']+WW_samples}


# categories = ["recoil"]
# hist_names = ["zll_recoil_m_final"]
categories = ["MVA"]
hist_names = ["mva_score"]


systs = {}

systs['bkg_norm'] = {
    'type': 'lnN',
    'value': 1.01,
    'procs': ['bkg'],
}

# systs['lumi'] = {
#     'type': 'lnN',
#     'value': 1.01,
#     'procs': '.*',
# }
