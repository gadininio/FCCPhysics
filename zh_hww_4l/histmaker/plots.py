import ROOT

flavor = 'll'  # 'mumu', 'ee', 'll'
ecm = '240'  # '240' or '365'

# scheme = 'full_20251124_111307' # n_leptons=4
# scheme = 'full_20251124_112545' # n_leptons=4, with dR(Z,WW)>0.25 cut
# scheme = 'full_20251124_131704' # n_leptons>=4
# scheme = 'full_20251124_131805' # n_leptons>=4, with dR(Z,WW)>0.25 cut
# scheme = 'full_20251124_150648' # n_leptons=4, with dR(Z,WW)>0.25 cut
# scheme = 'full_20251125_134522' # n_leptons=4, with dR(Z,WW)>0.25 cut, bug in resonanceBuilder_mass_recoil_advanced fixed
scheme = 'full_loose_20260126_112336' # loose cuts used as preselections for mva analysis
# scheme = 'loose' # loose cuts used as preselections for mva analysis
scheme = 'loose_20260806_155312'

if flavor=='mumu':
    Z_leptons = '#mu^{+}#mu^{-}'
if flavor=='ee':
    Z_leptons = 'e^{+}e^{-}'
if flavor=='ll':
    Z_leptons = 'l^{+}l^{-}'

lumi = "10.8" if ecm == '240' else "3"

# global parameters
intLumi        = 1.
intLumiLabel   = f"L = {lumi} ab^{{-1}}"
ana_tex        = 'e^{+}e^{-} #rightarrow Z(ll)H, H #rightarrow WW* #rightarrow l#nul#nu'
# ana_tex        = 'e^{+}e^{-}#rightarrow Z(' + Z_leptons + ') H[W(l#nu)W(l#nu)]'
# ana_tex        = 'e^{+}e^{-}#rightarrow Z(' + Z_leptons + ') H#left[W(l#nu)W(l#nu)#right]'
delphesVersion = '3.4.2'
energy         = int(ecm)
collider       = 'FCC-ee'
inputDir       = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{scheme}"
formats        = ['pdf']
outdir         = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{scheme}/{flavor}/"
plotStatUnc    = True


colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['WW_ll'] = ROOT.kBlue-2
colors['ZZ'] = ROOT.kGreen+2
colors['Z'] = ROOT.kOrange+1


procs = {}

if flavor=='ll':
    procs['signal'] = {'ZH':['wzp6_ee_mumuH_HWW_llnunu_ecm240', 'wzp6_ee_eeH_HWW_llnunu_ecm240']}
else:
    procs['signal'] = {'ZH':[f'wzp6_ee_{flavor}H_HWW_llnunu_ecm240']}
# procs['backgrounds'] =  {'WW':['p8_ee_WW_ee_ecm240', 'p8_ee_WW_mumu_ecm240'], 'ZZ':['p8_ee_ZZ_ecm240'], 'Z':['wzp6_ee_ee_Mee_30_150_ecm240', 'wzp6_ee_mumu_ecm240']}
# procs['backgrounds'] =  {'WW':['p8_ee_WW_ecm240'], 'ZZ':['p8_ee_ZZ_ecm240'], 'Z':['wzp6_ee_ee_Mee_30_150_ecm240', 'wzp6_ee_mumu_ecm240']}
procs['backgrounds'] =  {'WW':['p8_ee_WW_ecm240'], 'ZZ':['p8_ee_ZZ_ecm240']}


legend = {}
legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
legend['WW_ll'] = 'WW#rightarrow ee,#mu#mu'
legend['ZZ'] = 'ZZ'
legend['Z'] = 'Z#rightarrowll'


if 'loose' in scheme:
    # cutflow_xaxis = ["All events", "4 leptons", "2 OS pairs", "#geq1 SF pair", "p_{l_{1}},p_{l_{2}},p_{l_{3}},p_{l_{4}}", "76 < m_{l^{+}l^{-}} < 106", "20 < p_{l^{+}l^{-}} < 70", "120 < m_{rec} < 145", "|cos#theta_{miss}| < 0.98", "20 < E_{miss} < 120", "60 < m_{WW*} < 135", "#DeltaR(l_{WW*,1}, l_{WW*,2})>0.25"]
    cutflow_xaxis = ["All events", "4 leptons", "2 OS pairs", "#geq1 SF pair", "Leptons p", "76 < m_{l^{+}l^{-}} < 106", "20 < p_{l^{+}l^{-}} < 70", "120 < m_{rec} < 145", "|cos#theta_{miss}| < 0.98", "20 < E_{miss} < 120", "60 < m_{WW*} < 135", "#DeltaR(l_{WW*}, l_{WW*}) > 0.25"]

else:
    cutflow_xaxis = ["All events", "4 leptons", "2 OS pairs", "#geq1 SF pair", "p_{l_{1}},p_{l_{2}},p_{l_{3}},p_{l_{4}}", "76 < m_{l^{+}l^{-}} < 106", "20 < p_{l^{+}l^{-}} < 70", "120 < m_{rec} < 140", "|cos#theta_{miss}| < 0.98", "30 < E_{miss} < 110", "80 < m_{WW*} < 135", "#DeltaR(l_{WW*,1}, l_{WW*,2})>0.25"]


hists = {}

hists["cutFlow"] = {
    "output":   "cutFlow",
    "logy":     True,
    "stack":    False,
    "xmin":     0,
    "xmax":     len(cutflow_xaxis),
    "ymin":     0.1,
    "ymax":     1e12,
    "xtitle":   cutflow_xaxis,
    "ytitle":   "Events ",
    "scaleSig": 1,
    "dumpTable": True,
}

hists["n_leptons_cut0"] = {
    "output":   "n_leptons_cut0",
    "logy":     True,
    "stack":    False,
    # "rebin":    10,
    "xmin":     0,
    "xmax":     10,
    # "ymin":     10,
    "ymax":     1e13,
    "xtitle":   "N_{l^{#pm}}",
    "ytitle":   "Events ",
    "extralab": "Number of leptons with p > 5 GeV; before preselections",
}

hists["n_leptons_final"] = {
    "output":   "n_leptons",
    "logy":     True,
    "stack":    False,
    # "rebin":    10,
    "xmin":     0,
    "xmax":     10,
    # "ymin":     10,
    "ymax":     1e4,
    "xtitle":   "N_{l^{#pm}}",
    "ytitle":   "Events ",
    # "extralab": "Before preselections",
}

hists["lep0_p_cut2"] = {
    "output":   "lep0_p_cut2",
    "logy":     True,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}} [GeV]",
    "ytitle":   "Events ",
    "extralab": "Before lepton p_{l} cuts",
}

hists["lep1_p_cut2"] = {
    "output":   "lep1_p_cut2",
    "logy":     True,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}} [GeV]",
    "ytitle":   "Events ",
    "extralab": "Before lepton p_{l} cuts",
}

hists["lep2_p_cut2"] = {
    "output":   "lep2_p_cut2",
    "logy":     True,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{3}} [GeV]",
    "ytitle":   "Events ",
    "extralab": "Before lepton p_{l} cuts",
}

hists["lep3_p_cut2"] = {
    "output":   "lep3_p_cut2",
    "logy":     True,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{4}} [GeV]",
    "ytitle":   "Events ",
    "extralab": "Before lepton p_{l} cuts",
}

hists["lep0_p_final"] = {
    "output":   "lep0_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}} [GeV]",
    "ytitle":   "Events ",
    # "extralab": "After lepton p_{l} cuts",
}

hists["lep1_p_final"] = {
    "output":   "lep1_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}} [GeV]",
    "ytitle":   "Events ",
    # "extralab": "After lepton p_{l} cuts",
}

hists["lep2_p_final"] = {
    "output":   "lep2_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{3}} [GeV]",
    "ytitle":   "Events ",
    # "extralab": "After lepton p_{l} cuts",
}

hists["lep3_p_final"] = {
    "output":   "lep3_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{4}} [GeV]",
    "ytitle":   "Events ",
    # "extralab": "After lepton p_{l} cuts",
}

hists["zll_m_cut4"] = {
    "output":   "zll_m_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0,
    "xmax":     140,
    "ymin":     0,
    # "ymax":     3000,
    "xtitle":   "m_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["zll_m_final"] = {
    "output":   "zll_m",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     76,
    "xmax":     106,
    "ymin":     0,
    # "ymax":     3000,
    "xtitle":   "m_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
}

hists["zll_p_cut4"] = {
    "output":   "zll_p_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0,
    "xmax":     120,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 5,
    "extralab": "Before selections",
}

hists["zll_p_cut5"] = {
    "output":   "zll_p_cut5",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0,
    "xmax":     110,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 5,
    "extralab": "Before p_{l^{#plus}l^{#minus}} cut",
}

hists["zll_p_final"] = {
    "output":   "zll_p",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     15,
    "xmax":     75,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
}

hists["zll_theta_cut4"] = {
    "output":   "zll_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     3700,
    "xtitle":   "#theta_{l^{#plus}l^{#minus}}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["zll_theta_final"] = {
    "output":   "zll_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{l^{#plus}l^{#minus}}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["zll_phi_cut4"] = {
    "output":   "zll_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     1700,
    "xtitle":   "#phi_{l^{#plus}l^{#minus}}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["zll_phi_final"] = {
    "output":   "zll_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    20,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{l^{#plus}l^{#minus}}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["zll_recoil_m_cut4"] = {
    "output":   "zll_recoil_m_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    1,
    "xmin":     110,
    "xmax":     220,
    "ymin":     0,
    "ymax":     1200,
    "xtitle":   "m_{rec} [GeV]",
    "ytitle":   "Events",
    # "scaleSig": 2,
    "extralab": "Before selections",
}

hists["zll_recoil_m_final"] = {
    "output":   "zll_recoil_m",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     115,
    "xmax":     150,
    "ymin":     0,
    # "ymax":     2500,
    "xtitle":   "m_{rec} [GeV]",
    "ytitle":   "Events",
}

hists["zll_lep0_p_cut4"] = {
    "output":   "zll_lep0_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     90,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}^{Z}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["zll_lep0_p_final"] = {
    "output":   "zll_lep0_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     90,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}^{Z}} [GeV]",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["zll_lep0_theta_cut4"] = {
    "output":   "zll_lep0_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     5500,
    "xtitle":   "#theta_{l_{1}^{Z}}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["zll_lep0_theta_final"] = {
    "output":   "zll_lep0_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{l_{1}^{Z}}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["zll_lep0_phi_cut4"] = {
    "output":   "zll_lep0_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     1700,
    "xtitle":   "#phi_{l_{1}^{Z}}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["zll_lep0_phi_final"] = {
    "output":   "zll_lep0_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    20,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{l_{1}^{Z}}",
    "ytitle":   "Events ",
    # "extralab": "Before selections",
}

hists["zll_lep1_p_cut4"] = {
    "output":   "zll_lep1_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     90,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}^{Z}} [GeV]",
    "scaleSig": 20,
    "extralab": "Before selections",
}
    
hists["zll_lep1_p_final"] = {
    "output":   "zll_lep1_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     90,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}^{Z}} [GeV]",
}

hists["zll_lep1_theta_cut4"] = {
    "output":   "zll_lep1_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     4500,
    "xtitle":   "#theta_{l_{2}^{Z}}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["zll_lep1_theta_final"] = {
    "output":   "zll_lep1_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{l_{2}^{Z}}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["zll_lep1_phi_cut4"] = {
    "output":   "zll_lep1_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     1800,
    "xtitle":   "#phi_{l_{2}^{Z}}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["zll_lep1_phi_final"] = {
    "output":   "zll_lep1_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    20,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{l_{2}^{Z}}",
    "ytitle":   "Events ",
    # "extralab": "Before selections",
}

hists["zll_leps_dR_cut4"] = {
    "output":   "zll_leps_dR_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR(l_{1}^{Z}, l_{2}^{Z})",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["zll_leps_dR_final"] = {
    "output":   "zll_leps_dR",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR(l_{1}^{Z}, l_{2}^{Z})",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["zll_leps_category_cut4"] = {
    "output":   "zll_leps_category_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     -1,
    # "xmax":     3,
    # "ymin":     10,
    "ymax":     37000,
    # "xtitle":   "WW* leptons category",
    "xtitle":   ["Not leptonic", "e^{+}e^{-}", "#mu^{+}#mu^{-}", "e-#mu / #mu-e"],
    "scaleSig": 20,
    "extralab":   "Z-lepton candidates category, before selections",
}

hists["zll_leps_category_final"] = {
    "output":   "zll_leps_category",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     -1,
    # "xmax":     3,
    # "ymin":     10,
    "ymax":     770,
    # "xtitle":   "WW* leptons category",
    "xtitle":   ["Not leptonic", "e^{+}e^{-}", "#mu^{+}#mu^{-}", "e-#mu / #mu-e"],
    "extralab":   "Z-lepton candidates category",
}

hists["zll_lep0_p_index_cut4"] = {
    "output":   "zll_lep0_p_index_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     28e3,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
    "scaleSig": 20,
    "extralab":   "Lepton index for l_{1}^{Z}, before selections",
}

hists["zll_lep0_p_index_final"] = {
    "output":   "zll_lep0_p_index",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    "ymax":     1300,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
    "extralab":   "Lepton index for l_{1}^{Z}",
}

hists["zll_lep1_p_index_cut4"] = {
    "output":   "zll_lep1_p_index_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     24e3,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
    "scaleSig": 20,
    "extralab":   "Lepton index for l_{2}^{Z}, before selections",
}

hists["zll_lep1_p_index_final"] = {
    "output":   "zll_lep1_p_index",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    "ymax":     720,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
    "extralab":   "Lepton index for l_{2}^{Z}",
}

# WW
hists["WW_lep0_p_cut4"] = {
    "output":   "WW_lep0_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}^{WW*}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["WW_lep0_p_final"] = {
    "output":   "WW_lep0_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}^{WW*}} [GeV]",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["WW_lep0_theta_cut4"] = {
    "output":   "WW_lep0_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     5300,
    "xtitle":   "#theta_{l_{1}^{WW*}}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["WW_lep0_theta_final"] = {
    "output":   "WW_lep0_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{l_{1}^{WW*}}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["WW_lep0_phi_cut4"] = {
    "output":   "WW_lep0_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     1700,
    "xtitle":   "#phi_{l_{1}^{WW*}}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["WW_lep0_phi_final"] = {
    "output":   "WW_lep0_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    20,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{l_{1}^{WW*}}",
    "ytitle":   "Events ",
    # "extralab": "Before selections",
}

hists["WW_lep1_p_cut4"] = {
    "output":   "WW_lep1_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     6100,
    "xtitle":   "p_{l_{2}^{WW*}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["WW_lep1_p_final"] = {
    "output":   "WW_lep1_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}^{WW*}} [GeV]",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["WW_lep1_theta_cut4"] = {
    "output":   "WW_lep1_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     4300,
    "xtitle":   "#theta_{l_{2}^{WW*}}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["WW_lep1_theta_final"] = {
    "output":   "WW_lep1_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{l_{2}^{WW*}}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["WW_lep1_phi_cut4"] = {
    "output":   "WW_lep1_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     1700,
    "xtitle":   "#phi_{l_{2}^{WW*}}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["WW_lep1_phi_final"] = {
    "output":   "WW_lep1_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    20,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{l_{2}^{WW*}}",
    "ytitle":   "Events ",
    # "extralab": "Before selections",
}

hists["WW_leps_dR_cut4"] = {
    "output":   "WW_leps_dR_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR(l_{1}^{WW*},l_{2}^{WW*})",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["WW_leps_dR_cut9"] = {
    "output":   "WW_leps_dR_cut9",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR(l_{1}^{WW*},l_{2}^{WW*})",
    "ytitle":   "Events ",
    "extralab": "Before #DeltaR(l_{1}^{WW*},l_{2}^{WW*}) cut",
}

hists["WW_leps_dR_final"] = {
    "output":   "WW_leps_dR",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR(l_{1}^{WW*}, l_{2}^{WW*})",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["WW_leps_category_cut4"] = {
    "output":   "WW_leps_category_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     -1,
    # "xmax":     3,
    # "ymin":     10,
    "ymax":     27000,
    # "xtitle":   "WW* leptons category",
    "xtitle":   ["Not leptonic", "e^{+}e^{-}", "#mu^{+}#mu^{-}", "e-#mu / #mu-e"],
    "scaleSig": 20,
    "extralab":   "WW*-lepton candidates category, before selections",
}

hists["WW_leps_category_final"] = {
    "output":   "WW_leps_category",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     -1,
    # "xmax":     3,
    # "ymin":     10,
    # "ymax":     180,
    # "xtitle":   "WW* leptons category",
    "xtitle":   ["Not leptonic", "e^{+}e^{-}", "#mu^{+}#mu^{-}", "e-#mu / #mu-e"],
    "extralab":   "WW*-lepton candidates category",
}

hists["WW_lep0_p_index_cut4"] = {
    "output":   "WW_lep0_p_index_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     23000,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
    "scaleSig": 20,
    "extralab":   "Lepton index for l_{1}^{WW*}, before selections",
}

hists["WW_lep0_p_index_final"] = {
    "output":   "WW_lep0_p_index",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     1100,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
    "extralab":   "Lepton index for l_{1}^{WW*}",
}

hists["WW_lep1_p_index_cut4"] = {
    "output":   "WW_lep1_p_index_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     1100,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
    "scaleSig": 20,
    "extralab":   "Lepton index for l_{2}^{WW*}, before selections",
}

hists["WW_lep1_p_index_final"] = {
    "output":   "WW_lep1_p_index",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     1100,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
    "extralab":   "Lepton index for l_{2}^{WW*}",
}

hists["WW_mass_cut4"] = {
    "output":   "WW_mass_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     180,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "m_{WW*} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

# GADI: could be WW_mass_cut8
hists["WW_mass_cut8"] = {
    "output":   "WW_mass_cut8",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     150,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "m_{WW*} [GeV]",
    "ytitle":   "Events ",
    "extralab": "Before m_{WW*} cut",
}

hists["WW_mass_final"] = {
    "output":   "WW_mass",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     50,
    "xmax":     150,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "m_{WW*} [GeV]",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["WW_p_cut4"] = {
    "output":   "WW_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     130,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{WW*} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["WW_p_final"] = {
    "output":   "WW_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     90,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{WW*} [GeV]",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["WW_theta_cut4"] = {
    "output":   "WW_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     3700,
    "xtitle":   "#theta_{WW*}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["WW_theta_final"] = {
    "output":   "WW_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{WW*}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["WW_phi_cut4"] = {
    "output":   "WW_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     1700,
    "xtitle":   "#phi_{WW*}",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before selections",
}

hists["WW_phi_final"] = {
    "output":   "WW_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    20,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{WW*}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

# zll, WW
hists["zll_WW_dR_cut4"] = {
    "output":   "zll_WW_dR_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     8,
    # "ymin":     10,
    # "ymax":     100000,
    # "xtitle":   "#DeltaR(l^{#plus}l^{#minus}, l_{1}^{WW*}l_{2}^{WW*})",
    "xtitle":   "#DeltaR(l^{#plus}l^{#minus}, WW*)",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["zll_WW_dR_final"] = {
    "output":   "zll_WW_dR",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     8,
    # "ymin":     10,
    # "ymax":     100000,
    # "xtitle":   "#DeltaR(l^{#plus}l^{#minus}, l_{1}^{WW*}l_{2}^{WW*})",
    "xtitle":   "#DeltaR(l^{#plus}l^{#minus}, WW*)",
    "ytitle":   "Events ",
    # "extralab": "Before selections",
}

# Missing energy
# cosThetaMiss_cut7 or cosThetaMiss_cut6 (GADI))
hists["cosThetaMiss_cut6"] = {
    "output":   "cosThetaMiss_cut6",
    "logy":     False,
    "stack":    False,
    "rebin":    200,
    "xmin":     0,
    "xmax":     1,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "cos(#theta_{miss})",
    "ytitle":   "Events ",
    "scaleSig": 20,
    "extralab": "Before cos(#theta_{miss}) cut",
}

hists["cosThetaMiss_final"] = {
    "output":   "cosThetaMiss",
    "logy":     False,
    "stack":    False,
    "rebin":    200,
    "xmin":     0,
    "xmax":     1,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "cos(#theta_{miss})",
    "ytitle":   "Events ",
    # "extralab": "After cos(#theta_{miss}) cut",
}

# missingEnergy_cut8 or missingEnergy_cut7 (GADI)
hists["missingEnergy_cut7"] = {
    "output":   "missingEnergy_cut7",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     150,
    # "ymin":     10,
    # "ymax":     45,
    "xtitle":   "E_{miss} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before E_{miss} cut",
}

hists["missingEnergy_final"] = {
    "output":   "missingEnergy",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     150,
    # "ymin":     10,
    # "ymax":     45,
    "xtitle":   "E_{miss} [GeV]",
    "ytitle":   "Events ",
    # "extralab": "After cos(#theta_{miss}) cut",
}
