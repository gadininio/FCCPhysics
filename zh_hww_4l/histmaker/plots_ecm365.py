'''
Run with:
    path=nosel_ fccanalysis plots plots_ecm365.py
'''


import ROOT
import os

ecm = os.environ.get("ecm", "365")  # '240' or '365'
flavor = os.environ.get("flavor", "ll")
path_full = os.environ.get("path", "nosel_")  # 'nosel'_, 'loose_', 'tight_', 'full_tight_'

print(f"ecm: {ecm} GeV, flavor: {flavor}, path: {path_full}")

# flavor = 'll'  # 'mumu', 'ee', 'll'
# ecm = '365'  
# path_full = 'nosel_'  # no selections, 20% of events.
# path_full = 'loose_'  # loose selections, 20% of events.
# path_full = 'tight_'  # tight selections, 20% of events.
# path_full = 'full_tight_'  # tight selections, 100% of events.

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
# ana_tex        = 'e^{+}e^{-}#rightarrow Z(' + Z_leptons + ')H, H#rightarrow WW*#rightarrow l^{+}#nu l^{-}#nu'
# ana_tex        = 'e^{+}e^{-}#rightarrow Z(' + Z_leptons + ') H[W(l#nu)W(l#nu)]'
ana_tex        = 'e^{+}e^{-} #rightarrow Z(' + Z_leptons + ') H#left[W(l#nu)W(l#nu)#right]'
delphesVersion = '3.4.2'
energy         = int(ecm)
collider       = 'FCC-ee'
inputDir       = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{path_full}"
formats        = ['pdf']
outdir         = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{path_full}/{flavor}/"
plotStatUnc    = True


colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['WW_ll'] = ROOT.kBlue-2
colors['ZZ'] = ROOT.kGreen+2
colors['tt'] = ROOT.kOrange+3


procs = {}
procs['signal'] = {'ZH':['wzp6_ee_mumuH_HWW_ecm365', 'wzp6_ee_eeH_HWW_ecm365']}
# procs['backgrounds'] =  {'WW':['p8_ee_WW_ecm365'], 'WW_ll':['p8_ee_WW_ee_ecm365', 'p8_ee_WW_mumu_ecm365'], 'ZZ':['p8_ee_ZZ_ecm365'], 'Z':['wzp6_ee_ee_Mee_30_150_ecm365', 'wzp6_ee_mumu_ecm365']}
# procs['backgrounds'] =  {'WW':['p8_ee_WW_ecm365'], 'ZZ':['p8_ee_ZZ_ecm365'], 'Z':['wzp6_ee_ee_Mee_30_150_ecm365', 'wzp6_ee_mumu_ecm365']}
procs['backgrounds'] =  {'WW':['p8_ee_WW_ecm365'], 'ZZ':['p8_ee_ZZ_ecm365'], 'tt':['p8_ee_tt_ecm365']}

# procs['signal'] = {'ZH':['wzp6_ee_eeH_HWW_ecm365']}
# procs['backgrounds'] = {}
# outdir         = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{path_full}/{flavor}_eeH/"

# procs['signal'] = {'ZH':['wzp6_ee_mumuH_HWW_ecm365']}
# procs['backgrounds'] = {}
# outdir         = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{path_full}/{flavor}_mumuH/"

legend = {}
legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
legend['WW_ll'] = 'WW#rightarrow ee,#mu#mu'
legend['ZZ'] = 'ZZ'
legend['tt'] = 't#bar{t}'


if 'nosel' in path_full:
    cutflow_xaxis = ["All events",
                     "4 leptons",
                     "2 OS pairs",
                     "#geq1 SF pair",
                    #  "p_{l_{1}},p_{l_{2}},p_{l_{3}},p_{l_{4}}",
                    #  "76 < m_{l^{+}l^{-}} < 106",
                    #  "35 < p_{l^{+}l^{-}} < 155",
                    #  "120 < m_{rec} < 145",
                    #  "|cos#theta_{miss}| < 0.98",
                    #  "E_{miss} < 60",
                    #  "35 < m_{WW*} < 130",
                    #  "100 < p_{WW*} < 150",
                    #  "0.2<#DeltaR(l_{WW*,1},l_{WW*,2})<3.5",
                    #  "3.0<#DeltaR(WW*,ZZ*)<4.0"
    ]
    extralab = "Preselections"
elif 'loose' in path_full:
    cutflow_xaxis = ["All events",
                     "4 leptons",
                     "2 OS pairs",
                     "#geq1 SF pair",
                     "p_{l_{1}},p_{l_{2}},p_{l_{3}},p_{l_{4}}",
                     "76 < m_{l^{+}l^{-}} < 106",
                     "35 < p_{l^{+}l^{-}} < 155",
                     "120 < m_{rec} < 145",
                     "|cos#theta_{miss}| < 0.98",
                     "E_{miss} < 60",
                     "35 < m_{WW*} < 130",
                     "100 < p_{WW*} < 150",
                    #  "0.2<#DeltaR(l_{WW*,1},l_{WW*,2})<3.5",
                    #  "3.0<#DeltaR(WW*,ZZ*)<4.0"
    ]
    extralab = "Loose selections"
elif 'tight' in path_full:
    cutflow_xaxis = ["All events",
                     "4 leptons",
                     "2 OS pairs",
                     "#geq1 SF pair",
                     "p_{l_{1}},p_{l_{2}},p_{l_{3}},p_{l_{4}}",
                     "76 < m_{l^{+}l^{-}} < 106",
                     "140 < p_{l^{+}l^{-}} < 150",
                     "", # "120 < m_{rec} < 140",
                     "|cos#theta_{miss}| < 0.98",
                     "E_{miss} < 50",
                     "95 < m_{WW*} > 125",
                     "130 < p_{WW*} < 150",
                    #  "0.1<#DeltaR(l_{WW*,1},l_{WW*,2})<1.3",
                    #  "3.0<#DeltaR(WW*,ZZ*)<4.0"
    ]
    extralab = "Tight selections"
else:
    cutflow_xaxis = ["All events", "4 leptons", "2 OS pairs", "#geq1 SF pair", "p_{l_{1}},p_{l_{2}},p_{l_{3}},p_{l_{4}}", "m_{l^{+}l^{-}}", "p_{l^{+}l^{-}}", "m_{rec} ", "|cos#theta_{miss}|", "E_{miss}", "m_{WW*}", "#DeltaR(l_{WW*,1}, l_{WW*,2})"]


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
    # "scaleSig": 100,
    "dumpTable": True,
    "extralab": extralab,
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
    # "scaleSig": 100,
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
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["lep0_p_cut2"] = {
    "output":   "lep0_p_cut2",
    "logy":     True,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before lepton p_{l} cuts",
}

if not 'nosel' in path_full:
    hists["lep0_p_cut2a"] = {
        "output":   "lep0_p_cut2a",
        "logy":     True,
        "stack":    False,
        "rebin":    5,
        "xmin":     0,
        # "xmax":     100,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "p_{l_{1}} [GeV]",
        "ytitle":   "Events ",
        # "scaleSig": 100,
        "extralab": "Before lepton p_{1} cuts",
    }


hists["lep1_p_cut2"] = {
    "output":   "lep1_p_cut2",
    "logy":     True,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before lepton p_{l} cuts",
}

if not 'nosel' in path_full:
    hists["lep1_p_cut2b"] = {
        "output":   "lep1_p_cut2b",
        "logy":     True,
        "stack":    False,
        "rebin":    5,
        "xmin":     0,
        # "xmax":     100,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "p_{l_{2}} [GeV]",
        "ytitle":   "Events ",
        # "scaleSig": 100,
        "extralab": "Before lepton p_{2} cuts",
    }


hists["lep2_p_cut2"] = {
    "output":   "lep2_p_cut2",
    "logy":     True,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{3}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before lepton p_{l} cuts",
}

if not 'nosel' in path_full:
    hists["lep2_p_cut2c"] = {
        "output":   "lep2_p_cut2c",
        "logy":     True,
        "stack":    False,
        "rebin":    5,
        "xmin":     0,
        # "xmax":     100,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "p_{l_{3}} [GeV]",
        "ytitle":   "Events ",
        # "scaleSig": 100,
        "extralab": "Before lepton p_{3} cuts",
    }

hists["lep3_p_cut2"] = {
    "output":   "lep3_p_cut2",
    "logy":     True,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{4}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before lepton p_{l} cuts",
}

if not 'nosel' in path_full:
    hists["lep3_p_cut2d"] = {
        "output":   "lep3_p_cut2d",
        "logy":     True,
        "stack":    False,
        "rebin":    5,
        "xmin":     0,
        # "xmax":     100,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "p_{l_{4}} [GeV]",
        "ytitle":   "Events ",
        # "scaleSig": 100,
        "extralab": "Before lepton p_{4} cuts",
    }

hists["lep0_p_final"] = {
    "output":   "lep0_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["lep1_p_final"] = {
    "output":   "lep1_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["lep2_p_final"] = {
    "output":   "lep2_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{3}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["lep3_p_final"] = {
    "output":   "lep3_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{4}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["zll_m_cut4"] = {
    "output":   "zll_m_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0, # 76,
    "xmax":     375, # 106,
    "ymin":     0,
    # "ymax":     3000,
    "xtitle":   "m_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100,
    "extralab": "Before selections",
}

hists["zll_m_final"] = {
    "output":   "zll_m",
    "logy":     False,
    "stack":    False,
    "rebin":    1 if 'nosel' in path_full else 2,
    "xmin":     0, # 76,
    "xmax":     375 if 'nosel' in path_full else 120, # 106,
    "ymin":     0,
    # "ymax":     3000,
    "xtitle":   "m_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in path_full else 1,
    "extralab": extralab,
}

hists["zll_p_cut4"] = {
    "output":   "zll_p_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0,
    # "xmax":     80,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["zll_p_cut5"] = {
    "output":   "zll_p_cut5",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0,
    # "xmax":     80,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before p_{l^{#plus}l^{#minus}} cut",
}

hists["zll_p_final"] = {
    "output":   "zll_p",
    "logy":     False,
    "stack":    False,
    # "rebin":    1 if 'nosel' in path_full else 4,
    "xmin":     0 if 'nosel' in path_full else 100,
    "xmax":     375 if 'nosel' in path_full else 200,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["zll_theta_cut4"] = {
    "output":   "zll_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    "ymax":     3700,
    "xtitle":   "#theta_{l^{#plus}l^{#minus}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["zll_theta_final"] = {
    "output":   "zll_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{l^{#plus}l^{#minus}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["zll_phi_cut4"] = {
    "output":   "zll_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    "ymax":     1700,
    "xtitle":   "#phi_{l^{#plus}l^{#minus}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["zll_phi_final"] = {
    "output":   "zll_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{l^{#plus}l^{#minus}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["zll_recoil_m_cut4"] = {
    "output":   "zll_recoil_m_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    1,
    # "xmin":     110,
    # "xmax":     150,
    "ymin":     0,
    "ymax":     200,
    "xtitle":   "m_{rec} [GeV]",
    "ytitle":   "Events / 100 MeV",
    "extralab": "Before selections",
}

hists["zll_recoil_m_cut6"] = {
    "output":   "zll_recoil_m_cut6",
    "logy":     False,
    "stack":    False,
    "rebin":    1,
    # "xmin":     110,
    # "xmax":     150,
    "ymin":     0,
    # "ymax":     200,
    "xtitle":   "m_{rec} [GeV]",
    "ytitle":   "Events / 100 MeV",
    "extralab": "Before m_{rec} cut",
}

hists["zll_recoil_m_final"] = {
    "output":   "zll_recoil_m",
    "logy":     False,
    "stack":    False,
    "rebin":    5 if 'nosel' in path_full else 15,
    "xmin":     0 if 'nosel' in path_full else 110,
    "xmax":     375 if 'nosel' in path_full else 150,
    "ymin":     0,
    # "ymax":     2500,
    "xtitle":   "m_{rec} [GeV]",
    "ytitle":   "Events / 100 MeV",
    "scaleSig": 10 if 'nosel' in path_full else 1,
    "extralab": extralab,
}

hists["zll_lep0_p_cut4"] = {
    "output":   "zll_lep0_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}^{Z}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["zll_lep0_p_final"] = {
    "output":   "zll_lep0_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}^{Z}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["zll_lep0_theta_cut4"] = {
    "output":   "zll_lep0_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    "ymax":     5500,
    "xtitle":   "#theta_{l_{1}^{Z}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["zll_lep0_theta_final"] = {
    "output":   "zll_lep0_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{l_{1}^{Z}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["zll_lep0_phi_cut4"] = {
    "output":   "zll_lep0_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    "ymax":     1700,
    "xtitle":   "#phi_{l_{1}^{Z}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["zll_lep0_phi_final"] = {
    "output":   "zll_lep0_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{l_{1}^{Z}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["zll_lep1_p_cut4"] = {
    "output":   "zll_lep1_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}^{Z}} [GeV]",
    "extralab": "Before selections",
}
    
hists["zll_lep1_p_final"] = {
    "output":   "zll_lep1_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}^{Z}} [GeV]",
    "extralab": extralab,
}

hists["zll_lep1_theta_cut4"] = {
    "output":   "zll_lep1_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    "ymax":     4500,
    "xtitle":   "#theta_{l_{2}^{Z}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["zll_lep1_theta_final"] = {
    "output":   "zll_lep1_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{l_{2}^{Z}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["zll_lep1_phi_cut4"] = {
    "output":   "zll_lep1_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    "ymax":     1800,
    "xtitle":   "#phi_{l_{2}^{Z}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["zll_lep1_phi_final"] = {
    "output":   "zll_lep1_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{l_{2}^{Z}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
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
    # "scaleSig": 100,
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
    # "scaleSig": 100,
    "extralab": extralab,
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
    "extralab":   extralab + ", Z-lepton candidates category",
}

hists["zll_lep0_p_index_cut4"] = {
    "output":   "zll_lep0_p_index_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    "ymax":     28e3,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
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
    "extralab":  extralab + ", Lepton index for l_{1}^{Z}",
}

hists["zll_lep1_p_index_cut4"] = {
    "output":   "zll_lep1_p_index_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    "ymax":     24e3,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
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
    "extralab":  extralab +  ", Lepton index for l_{2}^{Z}",
}

# WW
hists["WW_lep0_p_cut4"] = {
    "output":   "WW_lep0_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}^{WW*}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["WW_lep0_p_final"] = {
    "output":   "WW_lep0_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}^{WW*}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["WW_lep0_theta_cut4"] = {
    "output":   "WW_lep0_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    "ymax":     5300,
    "xtitle":   "#theta_{l_{1}^{WW*}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
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
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["WW_lep0_phi_cut4"] = {
    "output":   "WW_lep0_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    "ymax":     1700,
    "xtitle":   "#phi_{l_{1}^{WW*}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["WW_lep0_phi_final"] = {
    "output":   "WW_lep0_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{l_{1}^{WW*}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["WW_lep1_p_cut4"] = {
    "output":   "WW_lep1_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    "ymax":     6100,
    "xtitle":   "p_{l_{2}^{WW*}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["WW_lep1_p_final"] = {
    "output":   "WW_lep1_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}^{WW*}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["WW_lep1_theta_cut4"] = {
    "output":   "WW_lep1_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    "ymax":     4300,
    "xtitle":   "#theta_{l_{2}^{WW*}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["WW_lep1_theta_final"] = {
    "output":   "WW_lep1_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#theta_{l_{2}^{WW*}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["WW_lep1_phi_cut4"] = {
    "output":   "WW_lep1_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    "ymax":     1700,
    "xtitle":   "#phi_{l_{2}^{WW*}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["WW_lep1_phi_final"] = {
    "output":   "WW_lep1_phi",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#phi_{l_{2}^{WW*}}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
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
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["WW_leps_dR_cut9"] = {
    "output":   "WW_leps_dR_cut9",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR(l_{1}^{WW*},l_{2}^{WW*})",
    "ytitle":   "Events ",
    "scaleSig": 10,
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
    "scaleSig": 100 if 'nosel' in path_full else 1,
    "extralab": extralab,
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
    "extralab":  extralab +  ", WW*-lepton candidates category",
}

hists["WW_lep0_p_index_cut4"] = {
    "output":   "WW_lep0_p_index_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    "ymax":     23000,
    # "xtitle":   ["Not found", "l_{1}", "l_{2}", "l_{3}", "l_{4}"],
    "xtitle":   ["Not found", "1", "2", "3", "4"],
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
    "extralab":  extralab +  ", Lepton index for l_{1}^{WW*}",
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
    "extralab":  extralab + ", Lepton index for l_{2}^{WW*}",
}

hists["WW_mass_cut4"] = {
    "output":   "WW_mass_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     170,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "m_{WW*} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["WW_mass_cut9"] = {
    "output":   "WW_mass_cut9",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     170,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "m_{WW*} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before m_{WW*} cut",
}

hists["WW_mass_final"] = {
    "output":   "WW_mass",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0 if 'nosel' in path_full else 50,
    "xmax":     300 if 'nosel' in path_full else 300,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "m_{WW*} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in path_full else 1,
    "extralab": extralab,
}

hists["WW_p_cut4"] = {
    "output":   "WW_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{WW*} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["WW_p_cut10"] = {
    "output":   "WW_p_cut10",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{WW*} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

hists["WW_p_final"] = {
    "output":   "WW_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    # "xmax":     100,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{WW*} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in path_full else 1,
    "extralab": extralab,
}

hists["WW_theta_cut4"] = {
    "output":   "WW_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     5,
    # "ymin":     10,
    "ymax":     3700,
    "xtitle":   "#theta_{WW*}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

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
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["WW_phi_cut4"] = {
    "output":   "WW_phi_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     -3.5,
    "xmax":     3.5,
    # "ymin":     10,
    "ymax":     1700,
    "xtitle":   "#phi_{WW*}",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

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
    # "scaleSig": 100,
    "extralab": extralab,
}

# zll, WW
hists["zll_WW_dR_cut4"] = {
    "output":   "zll_WW_dR_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     10,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR(l^{#plus}l^{#minus}, l_{1}^{WW*}l_{2}^{WW*})",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before selections",
}

# hists["zll_WW_dR_cut10"] = {
#     "output":   "zll_WW_dR_cut10",
#     "logy":     False,
#     "stack":    False,
#     "rebin":    10,
#     "xmin":     0,
#     "xmax":     10,
#     # "ymin":     10,
#     # "ymax":     100000,
#     "xtitle":   "#DeltaR(l^{#plus}l^{#minus}, l_{1}^{WW*}l_{2}^{WW*})",
#     "ytitle":   "Events ",
#     # "scaleSig": 100,
#     "extralab": "Before #DeltaR(l^{#plus}l^{#minus}, l_{1}^{WW*}l_{2}^{WW*}) selection",
# }

hists["zll_WW_dR_final"] = {
    "output":   "zll_WW_dR",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     10,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR(l^{#plus}l^{#minus}, l_{1}^{WW*}l_{2}^{WW*})",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

# Missing energy
hists["cosThetaMiss_cut7"] = {
    "output":   "cosThetaMiss_cut7",
    "logy":     False,
    "stack":    False,
    "rebin":    200,
    "xmin":     0,
    "xmax":     1,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "cos(#theta_{miss})",
    "ytitle":   "Events ",
    # "scaleSig": 100,
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
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["missingEnergy_cut8"] = {
    "output":   "missingEnergy_cut8",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     200,
    # "ymin":     10,
    # "ymax":     300,
    "xtitle":   "E_{miss} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 1,
    "extralab": "Before E_{miss} cut",
}

hists["missingEnergy_final"] = {
    "output":   "missingEnergy",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     375 if 'nosel' in path_full else 200,
    # "ymin":     10,
    # "ymax":     1000,
    "xtitle":   "E_{miss} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in path_full else 1,
    "extralab": extralab,
}
