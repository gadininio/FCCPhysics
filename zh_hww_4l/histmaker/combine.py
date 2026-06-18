'''
Run with:
    ecm=365 scheme=tight fccanalysis combine combine.py
'''

import ROOT
import os

ecm = os.environ.get("ecm", "365")  # '240' or '365'
scheme = os.environ.get("scheme", "tight_full")
# flavor = "mumu" # mumu, ee


## 240 GeV
# scheme = 'full_20251124_111307' # n_leptons=4
# scheme = 'full_20251124_112545' # n_leptons=4, with dR(Z,WW)>0.25 cut
# scheme = 'full_20251124_131704' # n_leptons>=4
# scheme = 'full_20251124_131805' # n_leptons>=4, with dR(Z,WW)>0.25 cut
# scheme = 'full_20251124_150648' # n_leptons=4, with dR(Z,WW)>0.25 cut
# scheme = 'full_20251125_134522' # n_leptons=4, with dR(Z,WW)>0.25 cut, bug in resonanceBuilder_mass_recoil_advanced fixed


intLumi        = 1.0 # assume histograms are scaled in previous step
outputDir      = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/combine/{scheme}/"
mc_stats       = True
rebin          = 10

# get histograms from histmaker step
inputDir       = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{scheme}/"

# # get histograms from final step, selection to be defined
# inputDir       = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/final_selection/{flavor}/"
# selection      = "sel3"


sig_procs = {'sig':[f"wzp6_ee_mumuH_HWW_{'llnunu_' if ecm=='240' else ''}ecm{ecm}",
                    f"wzp6_ee_eeH_HWW_{'llnunu_' if ecm=='240' else ''}ecm{ecm}",
                   ]}
bkg_procs = {'bkg':[f"p8_ee_ZZ_ecm{ecm}",
                    f"p8_ee_WW_ecm{ecm}",
                    # f"wzp6_ee_mumu_ecm{ecm}.root",
                    # f"wzp6_ee_tautau_ecm{ecm}.root",
                    # f"wzp6_ee_ee_Mee_30_150_ecm{ecm}.root",
                   ]}
if ecm == '365':
    bkg_procs['bkg'] += ["p8_ee_tt_ecm365"]


categories = ["recoil"]
hist_names = ["zll_recoil_m_final"]


systs = {}

# systs['bkg_norm'] = {
#     'type': 'lnN',
#     'value': 1.05,
#     'procs': ['bkg'],
# }

# systs['lumi'] = {
#     'type': 'lnN',
#     'value': 1.01,
#     'procs': '.*',
# }
