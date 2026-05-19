import ROOT

is_full = True
is_loose = True


# # get histograms from histmaker step
# inputDir       = f"../../outputs/higgs/zh_hww_4l/hists/{path_full if is_full else ''}/"

# get histograms from final step, selection to be defined
inputDir       = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if is_loose else ""}/final_selection/{"full" if is_full else ""}/'
selection      = "sel0"

intLumi        = 1.0 # assume histograms are scaled in previous step
outputDir      = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if is_loose else ""}/combine/{"full" if is_full else ""}/{selection}'
mc_stats       = True
rebin          = 10

sig_procs = {'sig':['wzp6_ee_eeH_HWW_ecm240', 'wzp6_ee_mumuH_HWW_ecm240']}
bkg_procs = {'bkg':['p8_ee_WW_ecm240', 'p8_ee_ZZ_ecm240']}
# bkg_procs = {'bkg':['p8_ee_WW_ecm240', 'p8_ee_ZZ_ecm240', 'wzp6_ee_ee_Mee_30_150_ecm240', 'wzp6_ee_mumu_ecm240']}


# categories = ["recoil"]
# hist_names = ["zll_recoil_m_final"]
categories = ["MVA"]
hist_names = ["mva_score"]


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
