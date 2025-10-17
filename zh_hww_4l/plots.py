import ROOT

flavor = 'ee'  # 'mumu', 'ee', 'll'
if flavor=='mumu':
    Z_leptons = '#mu^{+}#mu^{-}'
if flavor=='ee':
    Z_leptons = 'e^{+}e^{-}'
if flavor=='ll':
    Z_leptons = 'l^{+}l^{-}'
    
# global parameters
intLumi        = 1.
intLumiLabel   = "L = 10.8 ab^{-1}"
ana_tex        = 'e^{+}e^{-}#rightarrow Z(' + Z_leptons + ')H, H#rightarrow WW*#rightarrow l^{+}#nu l^{-}#nu'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = f"outputs/hists/"
formats        = ['pdf']
outdir         = f"outputs/plots/{flavor}/"
plotStatUnc    = True

colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2

procs = {}
if flavor=='ll':
    procs['signal'] = {'ZH':['wzp6_ee_eeH_HWW_ecm240', 'wzp6_ee_mumuH_HWW_ecm240']}
else:
    procs['signal'] = {'ZH':[f'wzp6_ee_{flavor}H_HWW_ecm240']}
procs['backgrounds'] =  {'WW':['p8_ee_WW_ecm240'], 'ZZ':['p8_ee_ZZ_ecm240']}
# procs['backgrounds'] =  {}


legend = {}
legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'



hists = {}

hists["zll_recoil_m_cut5"] = {
    "output":   "zll_recoil_m_cut5",
    "logy":     False,
    "stack":    False,
    "rebin":    1,
    "xmin":     110,
    "xmax":     150,
    "ymin":     0,
    # "ymax":     2500,
    "xtitle":   "m_{rec} (GeV)",
    "ytitle":   "Events / 100 MeV",
    "extralab": "Before m_{rec} cut",
}

hists["zll_recoil_m_final"] = {
    "output":   "zll_recoil_m",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     110,
    "xmax":     150,
    "ymin":     0,
    # "ymax":     2500,
    "xtitle":   "m_{rec} (GeV)",
    "ytitle":   "Events / 100 MeV",
}

hists["zll_p_cut4"] = {
    "output":   "zll_p_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0,
    "xmax":     80,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} (GeV)",
    "ytitle":   "Events ",
    "extralab": "Before _{l^{#plus}l^{#minus}} cut",

}

hists["zll_p_final"] = {
    "output":   "zll_p",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0,
    "xmax":     80,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} (GeV)",
    "ytitle":   "Events ",
}

hists["zll_m_cut3"] = {
    "output":   "zll_m_cut3",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     86,
    "xmax":     96,
    "ymin":     0,
    # "ymax":     3000,
    "xtitle":   "m_{l^{#plus}l^{#minus}} (GeV)",
    "ytitle":   "Events ",
    "extralab": "Before m_{l^{#plus}l^{#minus}} cut",
}

hists["zll_m_final"] = {
    "output":   "zll_m",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     86,
    "xmax":     96,
    "ymin":     0,
    # "ymax":     3000,
    "xtitle":   "m_{l^{#plus}l^{#minus}} (GeV)",
    "ytitle":   "Events ",
}

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

hists["missingEnergy_cut7"] = {
    "output":   "missingEnergy_cut7",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     250,
    # "ymin":     10,
    # "ymax":     45,
    "xtitle":   "E_{miss} (GeV)",
    "ytitle":   "Events ",
    "extralab": "Before E_{miss} cut",
}

hists["missingEnergy_final"] = {
    "output":   "missingEnergy",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     250,
    # "ymin":     10,
    # "ymax":     45,
    "xtitle":   "E_{miss} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "After cos(#theta_{miss}) cut",
}

hists["cutFlow"] = {
    "output":   "cutFlow",
    "logy":     True,
    "stack":    False,
    "xmin":     0,
    "xmax":     11,
    "ymin":     0.1,
    # "ymax":     1e3,
    # "xtitle":   ["All events", "#geq 1 #mu^{#pm} + ISO", "#geq 2 #mu^{#pm} + OS", "86 < m_{#mu^{+}#mu^{#minus}} < 96", "20 < p_{#mu^{+}#mu^{#minus}} < 70", "|cos#theta_{miss}| < 0.98", "120 < m_{rec} < 140", "#geq 4 l^{#pm}", "#geq 4 ISO l^{#pm}", "2 OS l^{#pm} pairs"],
    "xtitle":   ["All events", "4 leptons", "2 OS pairs", "Leptons p_{T}", "86 < m_{l^{+}l^{-}} < 96", "20 < p_{l^{+}l^{-}} < 70", "120 < m_{rec} < 140", "|cos#theta_{miss}| < 0.98", "30 < E_{miss} < 110", "80 < m_{WW*} < 135", "25 < p_{WW*} < 55"],
    # , "#theta_{WW*} < 2.5", "#phi_{WW*} < 2.5"],
    "ytitle":   "Events ",
    "scaleSig": 1,
    "dumpTable": True,
}

# hists["leptons_no"] = {
#     "output":   "leptons_no",
#     "logy":     False,
#     "stack":    False,
#     # "rebin":    10,
#     "xmin":     0,
#     "xmax":     10,
#     "ymin":     10,
#     "ymax":     100000,
#     "xtitle":   "N_{l^{#pm}}",
#     "ytitle":   "Events ",
#     # "extralab": "Before cos(#theta_{miss}) cut",
# }


hists["lep0_p_cut2"] = {
    "output":   "lep0_p_cut2",
    "logy":     True,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{#mu_{0}} (GeV)",
    "ytitle":   "Events ",
    "extralab": "Before lepton p_{T} cuts",
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
    "xtitle":   "P_{#mu_{1}} (GeV)",
    "ytitle":   "Events ",
    "extralab": "Before lepton p_{T} cuts",
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
    "xtitle":   "P_{#mu_{2}} (GeV)",
    "ytitle":   "Events ",
    "extralab": "Before lepton p_{T} cuts",
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
    "xtitle":   "P_{#mu_{3}} (GeV)",
    "ytitle":   "Events ",
    "extralab": "Before lepton p_{T} cuts",
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
    "xtitle":   "P_{#mu_{0}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "After lepton p_{T} cuts",
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
    "xtitle":   "P_{#mu_{1}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "After lepton p_{T} cuts",
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
    "xtitle":   "P_{#mu_{2}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "After lepton p_{T} cuts",
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
    "xtitle":   "P_{#mu_{3}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "After lepton p_{T} cuts",
}


# hists["WW_leps_p0_cut8"] = {
#     "output":   "WW_leps_p0_cut8",
#     "logy":     False,
#     "stack":    False,
#     "rebin":    5,
#     "xmin":     0,
#     "xmax":     100,
#     # "ymin":     10,
#     # "ymax":     100000,
#     "xtitle":   "P_{l_{WW}^{0}} (GeV)",
#     "ytitle":   "Events ",
#     "extralab": "Before P_{l_{WW}^{0}} cut",
# }

hists["WW_leps_p0_final"] = {
    "output":   "WW_leps_p0",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{l_{WW}^{0}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

# hists["WW_leps_p1_cut8"] = {
#     "output":   "WW_leps_p1_cut8",
#     "logy":     False,
#     "stack":    False,
#     "rebin":    5,
#     "xmin":     0,
#     "xmax":     100,
#     # "ymin":     10,
#     # "ymax":     100000,
#     "xtitle":   "P_{l_{WW}^{1}} (GeV)",
#     "ytitle":   "Events ",
#     "extralab": "Before P_{l_{WW}^{1}} cut",
# }

hists["WW_leps_p1_final"] = {
    "output":   "WW_leps_p1",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{l_{WW}^{1}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

# hists["WW_leps_dR_cut8"] = {
#     "output":   "WW_leps_dR_cut8",
#     "logy":     False,
#     "stack":    False,
#     "rebin":    10,
#     "xmin":     -5,
#     "xmax":     5,
#     # "ymin":     10,
#     # "ymax":     100000,
#     "xtitle":   "#DeltaR_{l_{WW}^{0},l_{WW}^{1}}",
#     "ytitle":   "Events ",
#     "extralab": "Before #DeltaR_{l_{WW}^{0},l_{WW}^{1}} cut",
# }

hists["WW_leps_dR_final"] = {
    "output":   "WW_leps_dR",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -5,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR_{l_{WW}^{0},l_{WW}^{1}}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["zll_leps_p0_cut8"] = {
    "output":   "zll_leps_p0_cut8",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{l_{Z}^{0}} (GeV)",
    "ytitle":   "Events ",
    "extralab": "Before P_{l_{Z}^{0}} cut",
}

hists["zll_leps_p0_final"] = {
    "output":   "zll_leps_p0",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{l_{Z}^{0}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["zll_leps_p1_cut8"] = {
    "output":   "zll_leps_p1_cut8",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{l_{Z}^{1}} (GeV)",
    "extralab": "Before P_{l_{Z}^{1}} cut",
}
    
hists["zll_leps_p1_final"] = {
    "output":   "zll_leps_p1",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{l_{Z}^{1}} (GeV)",
}

hists["WW_mass_cut8"] = {
    "output":   "WW_mass_cut8",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     170,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "m_{WW*} (GeV)",
    "ytitle":   "Events ",
    "extralab": "Before m_{WW*} cut",
}

hists["WW_mass_final"] = {
    "output":   "WW_mass",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     170,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "m_{WW*} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["WW_p_cut9"] = {
    "output":   "WW_p_cut9",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{WW*}",
    "ytitle":   "Events ",
    "extralab": "Before p_{WW*} cut",
}

hists["WW_p_final"] = {
    "output":   "WW_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{WW*}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

# hists["WW_theta_cut8"] = {
#     "output":   "WW_theta_cut8",
#     "logy":     False,
#     "stack":    False,
#     "rebin":    10,
#     "xmin":     0,
#     "xmax":     5,
#     # "ymin":     10,
#     # "ymax":     100000,
#     "xtitle":   "#theta_{WW*}",
#     "ytitle":   "Events ",
#     "extralab": "Before #theta_{WW*} cut",
# }

hists["WW_theta_final"] = {
    "output":   "WW_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{WW*}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

# hists["WW_phi_cut8"] = {
#     "output":   "WW_phi_cut8",
#     "logy":     False,
#     "stack":    False,
#     "rebin":    10,
#     "xmin":     -3.5,
#     "xmax":     3.5,
#     # "ymin":     10,
#     # "ymax":     100000,
#     "xtitle":   "#phi_{WW*}",
#     "ytitle":   "Events ",
#     "extralab": "Before #phi_{WW*} cut",
# }

hists["WW_phi_final"] = {
    "output":   "WW_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{WW*}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

################
### debug plots
################
hists["zll_leps_p0_index_final"] = {
    "output":   "zll_leps_p0_index",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     180,
    # "xtitle":   "Lepton index for leading Z->ll lepton (zll_leps[0])",
    "xtitle":   ["Not found", "leptons[0]", "leptons[1]", "leptons[2]", "leptons[3]"],
    "extralab":   "Lepton index for leading Z->ll lepton (zll_leps[0])",
}

hists["zll_leps_p1_index_final"] = {
    "output":   "zll_leps_p1_index",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     180,
    # "xtitle":   "Lepton index for subleading Z->ll lepton (zll_leps[1])",
    "xtitle":   ["Not found", "leptons[0]", "leptons[1]", "leptons[2]", "leptons[3]"],
    "extralab":   "Lepton index for subleading Z->ll lepton (zll_leps[1])",
}

hists["WW_leps_category_cut8"] = {
    "output":   "WW_leps_category_cut8",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     -1,
    # "xmax":     3,
    # "ymin":     10,
    # "ymax":     180,
    # "xtitle":   "WW leptons category",
    "xtitle":   ["Not leptonic", "e^{+}e^{-}", "#mu^{+}#mu^{-}", "e-#mu / #mu-e"],
    "extralab":   "WW leptons category, before WW lepton cuts",
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
    # "xtitle":   "WW leptons category",
    "xtitle":   ["Not leptonic", "e^{+}e^{-}", "#mu^{+}#mu^{-}", "e-#mu / #mu-e"],
    "extralab":   "WW leptons category",
}