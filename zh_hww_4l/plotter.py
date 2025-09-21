import ROOT

# flavor = "ee"
flavor = "mumu"

leptons = '#mu^{+}#mu^{-}' if flavor=='mumu' else 'e^{+}e^{-}'

# global parameters
intLumi        = 1.
intLumiLabel   = "L = 10.8 ab^{-1}"
ana_tex        = 'e^{+}e^{-}#rightarrow Z('+leptons+')H,  H#rightarrow WW*#rightarrow l^{+}#nu l^{-}#nu  (4l)'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = f"outputs/hists/{flavor}/"
formats        = ['pdf']
outdir         = f"outputs/plots/{flavor}/"
plotStatUnc    = True

colors = {}
colors['ZH'] = ROOT.kRed
# colors['WW'] = ROOT.kBlue+1
# colors['ZZ'] = ROOT.kGreen+2

procs = {}
procs['signal'] = {'ZH':[f'wzp6_ee_{flavor}H_HWW_ecm240']}
# procs['backgrounds'] =  {'WW':['p8_ee_WW_ecm240'], 'ZZ':['p8_ee_ZZ_ecm240']}
procs['backgrounds'] =  {}


legend = {}
legend['ZH'] = 'ZH'
# legend['WW'] = 'WW'
# legend['ZZ'] = 'ZZ'



hists = {}

hists["zll_recoil_m_final"] = {
    "output":   "zll_recoil_m",
    "logy":     False,
    "stack":    True,
    "rebin":    10,
    "xmin":     120,
    "xmax":     140,
    "ymin":     0,
    # "ymax":     2500,
    "xtitle":   "Recoil (GeV)",
    "ytitle":   "Events / 100 MeV",
}

hists["zll_p_final"] = {
    "output":   "zll_p",
    "logy":     False,
    "stack":    True,
    # "rebin":    2,
    "xmin":     0,
    "xmax":     80,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p(#mu^{#plus}#mu^{#minus}) (GeV)",
    "ytitle":   "Events ",
}

hists["zll_m_final"] = {
    "output":   "zll_m",
    "logy":     False,
    "stack":    True,
    # "rebin":    2,
    "xmin":     86,
    "xmax":     96,
    "ymin":     0,
    # "ymax":     3000,
    "xtitle":   "m(#mu^{#plus}#mu^{#minus}) (GeV)",
    "ytitle":   "Events ",
}

hists["cosThetaMiss_cut5"] = {
    "output":   "cosThetaMiss_cut5",
    "logy":     False,
    "stack":    True,
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
    "stack":    True,
    "rebin":    200,
    "xmin":     0,
    "xmax":     1,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "cos(#theta_{miss})",
    "ytitle":   "Events ",
    # "extralab": "After cos(#theta_{miss}) cut",
}

hists["missingEnergy_cut5"] = {
    "output":   "missingEnergy_cut5",
    "logy":     False,
    "stack":    True,
    "rebin":    10,
    "xmin":     0,
    "xmax":     250,
    # "ymin":     10,
    "ymax":     45,
    "xtitle":   "MissingEnergy (GeV)",
    "ytitle":   "Events ",
    "extralab": "Before cos(#theta_{miss}) cut",
}

hists["missingEnergy_final"] = {
    "output":   "missingEnergy",
    "logy":     False,
    "stack":    True,
    "rebin":    10,
    "xmin":     0,
    "xmax":     250,
    # "ymin":     10,
    "ymax":     45,
    "xtitle":   "MissingEnergy (GeV)",
    "ytitle":   "Events ",
    # "extralab": "After cos(#theta_{miss}) cut",
}

hists["cutFlow"] = {
    "output":   "cutFlow",
    "logy":     False,
    "stack":    False,
    "xmin":     0,
    "xmax":     10,
    # "ymin":     1e4,
    # "ymax":     1e11,
    "ymin":     0,
    # "ymax":     3e5,    
    "xtitle":   ["All events", "#geq 1 #mu^{#pm} + ISO", "#geq 2 #mu^{#pm} + OS", "86 < m_{#mu^{+}#mu^{#minus}} < 96", "20 < p_{#mu^{+}#mu^{#minus}} < 70", "|cos#theta_{miss}| < 0.98", "120 < m_{rec} < 140", "#geq 4 l^{#pm}", "#geq 4 ISO l^{#pm}", "2 OS l^{#pm} pairs"],
    "ytitle":   "Events ",
    "scaleSig": 10,
    "dumpTable": True,
}

# hists["leptons_no"] = {
#     "output":   "leptons_no",
#     "logy":     False,
#     "stack":    True,
#     # "rebin":    10,
#     "xmin":     0,
#     "xmax":     10,
#     "ymin":     10,
#     "ymax":     100000,
#     "xtitle":   "N_{l^{#pm}}",
#     "ytitle":   "Events ",
#     # "extralab": "Before cos(#theta_{miss}) cut",
# }


hists["muon0_p_cut2"] = {
    "output":   "muon0_p_cut2",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{#mu_{0}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["muon1_p_cut2"] = {
    "output":   "muon1_p_cut2",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{#mu_{1}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["muon2_p_cut2"] = {
    "output":   "muon2_p_cut2",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{#mu_{2}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["muon3_p_cut2"] = {
    "output":   "muon3_p_cut2",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{#mu_{3}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}


hists["muon0_p_cut3"] = {
    "output":   "muon0_p_cut3",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{#mu_{0}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["muon1_p_cut3"] = {
    "output":   "muon1_p_cut3",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{#mu_{1}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["muon2_p_cut3"] = {
    "output":   "muon2_p_cut3",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{#mu_{2}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["muon3_p_cut3"] = {
    "output":   "muon3_p_cut3",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{#mu_{3}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}


hists["leps_WW_p0"] = {
    "output":   "leps_WW_p0",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{l_{WW}^{0}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["leps_WW_p1"] = {
    "output":   "leps_WW_p1",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{l_{WW}^{1}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["leps_WW_dR"] = {
    "output":   "leps_WW_dR",
    "logy":     False,
    "stack":    True,
    "rebin":    10,
    "xmin":     -5,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR_{l_{WW}^{0},l_{WW}^{1}}",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["zll_leps_p0"] = {
    "output":   "zll_leps_p0",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{l_{Z}^{0}} (GeV)",
    "ytitle":   "Events ",
    # "extralab": "Before cos(#theta_{miss}) cut",
}

hists["zll_leps_p1"] = {
    "output":   "zll_leps_p1",
    "logy":     False,
    "stack":    True,
    "rebin":    5,
    "xmin":     0,
    "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "P_{l_{Z}^{1}} (GeV)",
}
    


# debug
hists["zll_leps_p0_index"] = {
    "output":   "zll_leps_p0_index",
    "logy":     False,
    "stack":    True,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    "ymax":     180,
    # "xtitle":   "Muon index for zll_leps[0]",
    "xtitle":   ["Not found", "muons[0]", "muons[1]", "muons[2]", "muons[3]"],
    "extralab":   "Muon index for zll_leps[0]",
}

hists["zll_leps_p1_index"] = {
    "output":   "zll_leps_p1_index",
    "logy":     False,
    "stack":    True,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     180,
    # "xtitle":   "Muon index for zll_leps[1]",
    "xtitle":   ["Not found", "muons[0]", "muons[1]", "muons[2]", "muons[3]"],
    "extralab":   "Muon index for zll_leps[1]",
}
    