'''
Run with:
    ecm=240 scheme=loose_full fccanalysis plots plots.py
    ecm=365 scheme=loose_full fccanalysis plots plots.py
'''

import ROOT
import os

ecm = os.environ.get("ecm", "240")  # '240' or '365'
scheme = os.environ.get("scheme", "loose_full")


lumi = "10.8" if ecm == '240' else "3"

# global parameters
intLumi        = 1.
intLumiLabel   = f"L = {lumi} ab^{{-1}}"
ana_tex        = 'e^{+}e^{-} #rightarrow Z(ll)H, H #rightarrow WW* #rightarrow l#nul#nu'
delphesVersion = '3.4.2'
energy         = int(ecm)
collider       = 'FCC-ee'
inputDir       = f'../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{scheme}/final_selection/'
formats        = ['pdf']
outdir         = f'../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{scheme}/plots/'
yaxis          = ['lin','log']
stacksig       = ['nostack']
plotStatUnc    = True




variables = ['zll_recoil_m', 'zll_recoil_m_final', 'zll_m', 'zll_p', 'mva_score']
rebin = [10, 1, 1, 1, 5] # uniform rebin per variable (optional)

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ZH']   = ["sel0", "sel1"]

extralabel = {}
extralabel['sel0'] = "Basic selection"
extralabel['sel1'] = "MVA > 0.5"

colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2
if ecm == '365':
    colors['tt'] = ROOT.kMagenta+1


plots = {}

if ecm == '240':
    # plots['ZH'] = {
    #     'signal': {'ZH':['wzp6_ee_eeH_HWW_llnunu_ecm240', 'wzp6_ee_mumuH_HWW_llnunu_ecm240']},
    #     'backgrounds': {'WW':['p8_ee_WW_ee_ecm240', 'p8_ee_WW_mumu_ecm240'], 'ZZ':['p8_ee_ZZ_ecm240']}
    # }
    plots['ZH'] = {
        'signal': {'ZH':['wzp6_ee_eeH_HWW_llnunu_ecm240', 'wzp6_ee_mumuH_HWW_llnunu_ecm240']},
        'backgrounds': {'WW':['p8_ee_WW_ecm240'], 'ZZ':['p8_ee_ZZ_ecm240']}
    }

elif ecm == '365':
    # if 'inclWWInFit' in scheme:
    print('Using inclusive WW in fit.')
    WW_samples = ['p8_ee_WW_ecm365']
    # else:
    #     print('Using WW->ee + WW->mumu in fit.')
    #     WW_samples = ['p8_ee_WW_ee_ecm365', 'p8_ee_WW_mumu_ecm365']
    plots['ZH'] = {
        'signal': {'ZH':['wzp6_ee_eeH_HWW_ecm365', 'wzp6_ee_mumuH_HWW_ecm365']},
        'backgrounds': {'WW':WW_samples, 'ZZ':['p8_ee_ZZ_ecm365'], 'tt':['p8_ee_tt_ecm365']}
    }
    

legend = {}
legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'
if ecm == '365':
    legend['tt'] = 't#bar{t}'