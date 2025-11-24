import ROOT

# flavor = "mumu" # mumu, ee
is_full = True

intLumi        = 1.0 # assume histograms are scaled in previous step
outputDir      = f"../../outputs/higgs/zh_hww_4l/combine/{'full/' if is_full else ''}/"
mc_stats       = True
rebin          = 10

# get histograms from histmaker step
inputDir       = f"../../outputs/higgs/zh_hww_4l/hists/{'full/' if is_full else ''}/"

# # get histograms from final step, selection to be defined
# inputDir       = f"../../../outputs/higgs/zh_hww_4l/final_selection/{flavor}/"
# selection      = "sel3"


sig_procs = {'sig':['wzp6_ee_eeH_HWW_ecm240', 'wzp6_ee_mumuH_HWW_ecm240']}
# bkg_procs = {'bkg':['p8_ee_WW_ecm240', 'p8_ee_ZZ_ecm240']}
bkg_procs = {'bkg':['p8_ee_WW_ecm240', 'p8_ee_ZZ_ecm240', 'wzp6_ee_ee_Mee_30_150_ecm240', 'wzp6_ee_mumu_ecm240']}


categories = ["recoil"]
hist_names = ["zll_recoil_m_final"]


systs = {}

systs['bkg_norm'] = {
    'type': 'lnN',
    'value': 1.05,
    'procs': ['bkg'],
}

systs['lumi'] = {
    'type': 'lnN',
    'value': 1.01,
    'procs': '.*',
}
