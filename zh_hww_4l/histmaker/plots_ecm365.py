'''
Run with:
    scheme=loose_full fccanalysis plots plots_ecm365.py
    scheme=medium_full_inclWWInFit fccanalysis plots plots_ecm365.py
    scheme=medium fccanalysis plots plots_ecm365.py

Use inclusive WW:
    scheme=medium3 inclWW=true fccanalysis plots plots_ecm365.py
    scheme=medium3_chi2-1.0_iso-3.0 inclWW=true fccanalysis plots plots_ecm365.py

Plot lepton isolation:
    scheme=presel_chi2-1.0 inclWW=true iso=true no_new=true fccanalysis plots plots_ecm365.py
    scheme=medium3 inclWW=true iso=true fccanalysis plots plots_ecm365.py
    scheme=medium3_full_chi2-1.0_iso-3.0 inclWW=true iso=true fccanalysis plots plots_ecm365.py
    
Compare signal Z(ee)H(WW) vs Z(mumu)H(WW):
    scheme=medium3 comp_sig=true fccanalysis plots plots_ecm365.py
    scheme=medium3_chi2-1.0 comp_sig=true fccanalysis plots plots_ecm365.py
'''


import ROOT
import os

ecm = os.environ.get("ecm", "365")  # '240' or '365'
flavor = os.environ.get("flavor", "ll")
scheme = os.environ.get("scheme", "presel")
use_incl_WW = os.environ.get("inclWW", "False").lower() in ("true", "1")
compare_signal = os.environ.get("comp_sig", "False").lower() in ("true", "1")
plot_lepton_iso = os.environ.get("iso", "False").lower() in ("true", "1")
is_plot_new = not os.environ.get("no_new", "False").lower() in ("true", "1")

print(f"ecm: {ecm} GeV, flavor: {flavor}, scheme: {scheme}")

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
ana_tex        = 'e^{+}e^{-} #rightarrow Z(ll)H, H #rightarrow WW* #rightarrow l#nul#nu'
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
colors['tt'] = ROOT.kMagenta+1


procs = {}
procs['signal'] = {'ZH':['wzp6_ee_mumuH_HWW_ecm365', 'wzp6_ee_eeH_HWW_ecm365']}

if 'inclWWInFit' in scheme or use_incl_WW:
    print('Using inclusive WW in fit.')
    WW_samples = ['p8_ee_WW_ecm365']
    WW_legend = 'WW'
else:
    print('Using WW->ee + WW->mumu in fit.')
    WW_samples = ['p8_ee_WW_ee_ecm365', 'p8_ee_WW_mumu_ecm365']
    WW_legend = 'WW#rightarrow ee,#mu#mu'
# procs['backgrounds'] =  {'WW':['p8_ee_WW_ecm365'], 'WW_ll':['p8_ee_WW_ee_ecm365', 'p8_ee_WW_mumu_ecm365'], 'ZZ':['p8_ee_ZZ_ecm365'], 'Z':['wzp6_ee_ee_Mee_30_150_ecm365', 'wzp6_ee_mumu_ecm365']}
procs['backgrounds'] =  {'WW':WW_samples, 'ZZ':['p8_ee_ZZ_ecm365'], 'tt':['p8_ee_tt_ecm365']}


# procs['signal'] = {'ZH':['wzp6_ee_eeH_HWW_ecm365']}
# procs['backgrounds'] = {}
# outdir         = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{scheme}/{flavor}_eeH/"

# procs['signal'] = {'ZH':['wzp6_ee_mumuH_HWW_ecm365']}
# procs['backgrounds'] = {}
# outdir         = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{scheme}/{flavor}_mumuH/"


legend = {}
legend['ZH'] = 'ZH'
legend['WW'] = WW_legend
# legend['WW_ll'] = 'WW#rightarrow ee,#mu#mu'
legend['ZZ'] = 'ZZ'
legend['tt'] = 't#bar{t}'




#########################################################################
if compare_signal:
    # compare Z(ee)H(WW) with Z(mumu)H(WW)
    procs = {}
    procs['signal'] = {'Zmumu':['wzp6_ee_mumuH_HWW_ecm365']}
    procs['backgrounds'] = {'Zee':['wzp6_ee_eeH_HWW_ecm365']}
    outdir = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{scheme}/{flavor}_sig/"

    colors = {}
    colors['Zmumu'] = ROOT.kRed
    colors['Zee'] = ROOT.kBlue+1

    legend = {}
    legend['Zmumu'] = 'Z(#mu#mu)H(WW) (ZH only)'
    legend['Zee'] = 'Z(ee)H(WW) (inclusive)'
#########################################################################




extralab = ""
if 'nosel' in scheme:
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
elif 'loose' in scheme:
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
elif 'medium' in scheme:
    cutflow_xaxis = ["All events",
                     "4 leptons",
                     "Lepton isolation",
                     "2 OS pairs",
                     "#geq1 SF pair",
                     "Leptons p",
                     "71 < m_{l^{+}l^{-}} < 111",
                     "35 < p_{l^{+}l^{-}} < 155",
                     "115 < m_{rec} < 230",
                     "|cos#theta_{miss}| < 0.98",
                     "20 < E_{miss} < 180",
                     "m_{WW*} > 50",
                     "0.1<#DeltaR(l_{WW*},l_{WW*})<4",
                     "#DeltaR(Z#rightarrowll,WW*)>3",
                     "#DeltaR(l^{+},l^{-}) < 3"
    ]
    # extralab = "Medium selections (loose + #DeltaR(Z#rightarrow ll, WW*) > 3.0 cut)"
    extralab = "Medium selections"
elif 'firm' in scheme:
    cutflow_xaxis = ["All events",
                     "4 leptons",
                     "Lepton Isolation",
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
                     "0.2<#DeltaR(l_{WW*,1},l_{WW*,2})<3.5",
                     "#DeltaR(Z#rightarrow ll, WW*) > 3.0"
    ]
    extralab = "Firm selections (medium + lepton isolation)"
elif 'tight' in scheme:
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
    "xmax":     200,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before lepton p_{l} cuts",
}

if 'nosel' not in scheme and 'presel' not in scheme:
    hists["lep0_p_cut2a"] = {
        "output":   "lep0_p_cut2a",
        "logy":     True,
        "stack":    False,
        "rebin":    5,
        "xmin":     0,
        "xmax":     200,
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
    "xmax":     200,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before lepton p_{l} cuts",
}

if 'nosel' not in scheme and 'presel' not in scheme:
    hists["lep1_p_cut2b"] = {
        "output":   "lep1_p_cut2b",
        "logy":     True,
        "stack":    False,
        "rebin":    5,
        "xmin":     0,
        "xmax":     200,
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
    "xmax":     200,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{3}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before lepton p_{l} cuts",
}

if 'nosel' not in scheme and 'presel' not in scheme:
    hists["lep2_p_cut2c"] = {
        "output":   "lep2_p_cut2c",
        "logy":     True,
        "stack":    False,
        "rebin":    5,
        "xmin":     0,
        "xmax":     200,
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
    "xmax":     200,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{4}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": "Before lepton p_{l} cuts",
}

if 'nosel' not in scheme and 'presel' not in scheme:
    hists["lep3_p_cut2d"] = {
        "output":   "lep3_p_cut2d",
        "logy":     True,
        "stack":    False,
        "rebin":    5,
        "xmin":     0,
        "xmax":     200,
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
    "rebin":    10,
    "xmin":     0,
    "xmax":     180,
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
    "rebin":   105,
    "xmin":     0,
    "xmax":     180,
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
    "rebin":    10,
    "xmin":     0,
    "xmax":     150,
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
    "rebin":    10,
    "xmin":     0,
    "xmax":     150,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{4}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}






if '_iso' in scheme or plot_lepton_iso:
    
    # # Before cuts
    # hists["lep0_iso_cut2"] = {
    #     "output":   "lep0_iso_cut2",
    #     "logy":     False,
    #     "stack":    False,
    #     "rebin":    500,
    #     "xmin":     -11,
    #     "xmax":     3,
    #     # "ymin":     10,
    #     # "ymax":     100000,
    #     "xtitle":   "l_{1} isolation",
    #     "ytitle":   "Events ",
    #     # "scaleSig": 100,
    #     "extralab": "Before lepton p_{l} cuts",
    # }

    # hists["lep1_iso_cut2"] = {
    #     "output":   "lep1_iso_cut2",
    #     "logy":     False,
    #     "stack":    False,
    #     "rebin":    500,
    #     "xmin":     -11,
    #     "xmax":     3,
    #     # "ymin":     10,
    #     # "ymax":     100000,
    #     "xtitle":   "l_{2} isolation",
    #     "ytitle":   "Events ",
    #     # "scaleSig": 100,
    #     "extralab": "Before lepton p_{l} cuts",
    # }

    # hists["lep2_iso_cut2"] = {
    #     "output":   "lep2_iso_cut2",
    #     "logy":     False,
    #     "stack":    False,
    #     "rebin":    500,
    #     "xmin":     -11,
    #     "xmax":     3,
    #     # "ymin":     10,
    #     # "ymax":     100000,
    #     "xtitle":   "l_{3} isolation",
    #     "ytitle":   "Events ",
    #     # "scaleSig": 100,
    #     "extralab": "Before lepton p_{l} cuts",
    # }

    # hists["lep3_iso_cut2"] = {
    #     "output":   "lep3_iso_cut2",
    #     "logy":     False,
    #     "stack":    False,
    #     "rebin":    500,
    #     "xmin":     -11,
    #     "xmax":     3,
    #     # "ymin":     10,
    #     # "ymax":     100000,
    #     "xtitle":   "l_{4} isolation",
    #     "ytitle":   "Events ",
    #     # "scaleSig": 100,
    #     "extralab": "Before lepton p_{l} cuts",
    # }


    # After all cuts, log scale
    hists["lep0_iso_log_final"] = {
        "output":   "lep0_iso_log",
        "logy":     True,
        "stack":    False,
        "rebin":    500,
        "xmin":     -11,
        "xmax":     3,
        # "ymin":     10,
        # "ymax":     1e5,
        "xtitle":   "log_{10}(l_{1} isolation)",
        "ytitle":   "Events ",
        "scaleSig": 1,
        "extralab": extralab,
    }

    hists["lep1_iso_log_final"] = {
        "output":   "lep1_iso_log",
        "logy":     True,
        "stack":    False,
        "rebin":    500,
        "xmin":     -11,
        "xmax":     3,
        # "ymin":     10,
        # "ymax":     1e5,
        "xtitle":   "log_{10}(l_{2} isolation)",
        "ytitle":   "Events ",
        "scaleSig": 1,
        "extralab": extralab,
    }

    hists["lep2_iso_log_final"] = {
        "output":   "lep2_iso_log",
        "logy":     True,
        "stack":    False,
        "rebin":    500,
        "xmin":     -11,
        "xmax":     3,
        # "ymin":     10,
        # "ymax":     250,
        "xtitle":   "log_{10}(l_{3} isolation)",
        "ytitle":   "Events ",
        "scaleSig": 1,
        "extralab": extralab,
    }

    hists["lep3_iso_log_final"] = {
        "output":   "lep3_iso_log",
        "logy":     True,
        "stack":    False,
        "rebin":    500,
        "xmin":     -11,
        "xmax":     3,
        # "ymin":     10,
        # "ymax":     300,
        "xtitle":   "log_{10}(l_{4} isolation)",
        "ytitle":   "Events ",
        "scaleSig": 1,
        "extralab": extralab,
    }








hists["zll_m_cut4"] = {
    "output":   "zll_m_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0, # 76,
    "xmax":     250, # 106,
    "ymin":     0,
    # "ymax":     3000,
    "xtitle":   "m_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 1 if compare_signal else 10,
    "extralab": "Before selections",
}

# hists["zll_m_cut4"] = { # GADI
#     "output":   "zll_m_cut4",
#     "logy":     True,
#     "stack":    False,
#     # "rebin":    2,
#     "xmin":     0, # 76,
#     "xmax":     375, # 106,
#     # "ymin":     0,
#     # "ymax":     3000,
#     "xtitle":   "m_{l^{#plus}l^{#minus}} [GeV]",
#     "ytitle":   "Events ",
#     "scaleSig": 1,
#     "extralab": "Before selections",
# }

hists["zll_m_final"] = {
    "output":   "zll_m",
    "logy":     False,
    "stack":    False,
    "rebin":    1 if 'nosel' in scheme else 2,
    "xmin":     71,
    "xmax":     375 if 'nosel' in scheme else 111,
    "ymin":     0,
    # "ymax":     3000,
    "xtitle":   "m_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in scheme else 1,
    "extralab": extralab,
}

hists["zll_p_cut4"] = {
    "output":   "zll_p_cut4",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0,
    "xmax":     200,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["zll_p_cut5"] = {
    "output":   "zll_p_cut5",
    "logy":     False,
    "stack":    False,
    # "rebin":    2,
    "xmin":     0,
    "xmax":     200,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before p_{l^{#plus}l^{#minus}} cut",
}

hists["zll_p_final"] = {
    "output":   "zll_p",
    "logy":     False,
    "stack":    False,
    "rebin":    1 if 'nosel' in scheme else 2,
    "xmin":     0 if 'nosel' in scheme else 60,
    "xmax":     375 if 'nosel' in scheme else 160,
    "ymin":     0,
    # "ymax":     2000,
    "xtitle":   "p_{l^{#plus}l^{#minus}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

if is_plot_new:
    hists["zll_pt_cut4"] = {
        "output":   "zll_pt_cut4",
        "logy":     False,
        "stack":    False,
        # "rebin":    2,
        "xmin":     0,
        "xmax":     200,
        "ymin":     0,
        # "ymax":     2000,
        "xtitle":   "p_{T}^{l^{#plus}l^{#minus}} [GeV]",
        "ytitle":   "Events ",
        "scaleSig": 5,
        "extralab": "Before selections",
    }

    hists["zll_pt_final"] = {
        "output":   "zll_pt",
        "logy":     False,
        "stack":    False,
        "rebin":    1 if 'nosel' in scheme else 5,
        "xmin":     0 if 'nosel' in scheme else 0,
        "xmax":     375 if 'nosel' in scheme else 160,
        "ymin":     0,
        # "ymax":     2000,
        "xtitle":   "p_{T}^{l^{#plus}l^{#minus}} [GeV]",
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
    "xmax":     3.5,
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
    "xmax":     3.5,
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
    # "ymax":     1700,
    "xtitle":   "#phi_{l^{#plus}l^{#minus}}",
    "ytitle":   "Events ",
    "scaleSig": 10,
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
    # "ymin":     0,
    # "ymax":     200,
    "xtitle":   "Recoil [GeV]",
    "ytitle":   "Events",
    "scaleSig": 3,
    "extralab": "Before selections",
}

hists["zll_recoil_m_cut6"] = {
    "output":   "zll_recoil_m_cut6",
    "logy":     False,
    "stack":    False,
    "rebin":    2,
    "xmin":     50,
    "xmax":     300,
    "ymin":     0,
    # "ymax":     200,
    "xtitle":   "Recoil [GeV]",
    "ytitle":   "Events",
    "scaleSig": 2,
    "extralab": "Before Recoil cut",
}

hists["zll_recoil_m_final"] = {
    "output":   "zll_recoil_m",
    "logy":     False,
    "stack":    False,
    "rebin":    5 if 'nosel' in scheme else 50,
    "xmin":     0 if 'nosel' in scheme else 105,
    "xmax":     375 if 'nosel' in scheme else 235,
    "ymin":     0,
    # "ymax":     2500,
    "xtitle":   "Recoil [GeV]",
    "ytitle":   "Events",
    "scaleSig": 10 if 'nosel' in scheme else 1,
    "extralab": extralab,
}

hists["zll_lep0_p_cut4"] = {
    "output":   "zll_lep0_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     180,
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
    "rebin":    10,
    "xmin":     0,
    "xmax":     180,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}^{Z}} [GeV]",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

if is_plot_new:
    hists["zll_lep0_pt_cut4"] = {
        "output":   "zll_lep0_pt_cut4",
        "logy":     False,
        "stack":    False,
        "rebin":    5,
        "xmin":     0,
        "xmax":     180,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "p_{T}^{l_{1}^{Z}} [GeV]",
        "ytitle":   "Events ",
        "scaleSig": 10,
        "extralab": extralab,
    }

    hists["zll_lep0_pt_final"] = {
        "output":   "zll_lep0_pt",
        "logy":     False,
        "stack":    False,
        "rebin":    10,
        "xmin":     0,
        "xmax":     180,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "p_{T}^{l_{1}^{Z}} [GeV]",
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
    "xmax":     3.5,
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
    "xmax":     3.5,
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
    # "ymax":     1700,
    "xtitle":   "#phi_{l_{1}^{Z}}",
    "ytitle":   "Events ",
    "scaleSig": 10,
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
    "xmax":     170,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}^{Z}} [GeV]",
    "extralab": "Before selections",
}
    
hists["zll_lep1_p_final"] = {
    "output":   "zll_lep1_p",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     150,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{2}^{Z}} [GeV]",
    "extralab": extralab,
}

if is_plot_new:
    hists["zll_lep1_pt_cut4"] = {
        "output":   "zll_lep1_pt_cut4",
        "logy":     False,
        "stack":    False,
        "rebin":    5,
        "xmin":     0,
        "xmax":     150,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "p_{T}^{l_{2}^{Z}} [GeV]",
        "scaleSig": 10,
        "extralab": extralab,
    }

    hists["zll_lep1_pt_final"] = {
        "output":   "zll_lep1_pt",
        "logy":     False,
        "stack":    False,
        "rebin":    10,
        "xmin":     0,
        "xmax":     100,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "p_{T}^{l_{2}^{Z}} [GeV]",
        "extralab": extralab,
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
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["zll_lep1_theta_final"] = {
    "output":   "zll_lep1_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    20,
    "xmin":     0,
    "xmax":     3.5,
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
    # "ymax":     1800,
    "xtitle":   "#phi_{l_{2}^{Z}}",
    "ytitle":   "Events ",
    "scaleSig": 10,
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
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["zll_leps_dR_cut4"] = {
    "output":   "zll_leps_dR_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     8,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR(l_{1}^{Z}, l_{2}^{Z})",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["zll_leps_dR_cut12"] = {
    "output":   "zll_leps_dR_cut12",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0.5,
    "xmax":     7,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "#DeltaR(l_{1}^{Z}, l_{2}^{Z})",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["zll_leps_dR_final"] = {
    "output":   "zll_leps_dR",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0.5,
    "xmax":     3.5,
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
    # "ymax":     37000,
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
    # "ymax":     770,
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
    # "ymax":     28e3,
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
    # "ymax":     1300,
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
    # "ymax":     24e3,
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
    # "ymax":     720,
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
    "xmax":     180,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{l_{1}^{WW*}} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["WW_lep0_p_final"] = {
    "output":   "WW_lep0_p",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     170,
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
    "xmax":     3.5,
    # "ymin":     10,
    "ymax":     5300,
    "xtitle":   "#theta_{l_{1}^{WW*}}",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["WW_lep0_theta_final"] = {
    "output":   "WW_lep0_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    20,
    "xmin":     0,
    "xmax":     3.5,
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
    # "ymax":     1700,
    "xtitle":   "#phi_{l_{1}^{WW*}}",
    "ytitle":   "Events ",
    "scaleSig": 10,
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
    # "scaleSig": 100,
    "extralab": extralab,
}

hists["WW_lep1_p_cut4"] = {
    "output":   "WW_lep1_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     160,
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
    "rebin":    10,
    "xmin":     0,
    "xmax":     160,
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
    "xmax":     3.5,
    # "ymin":     10,
    "ymax":     4300,
    "xtitle":   "#theta_{l_{2}^{WW*}}",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["WW_lep1_theta_final"] = {
    "output":   "WW_lep1_theta",
    "logy":     False,
    "stack":    False,
    "rebin":    20,
    "xmin":     0,
    "xmax":     3.5,
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
    # "ymax":     1700,
    "xtitle":   "#phi_{l_{2}^{WW*}}",
    "ytitle":   "Events ",
    "scaleSig": 10,
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
    "scaleSig": 10,
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
    "scaleSig": 100 if 'nosel' in scheme else 1,
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
    # "ymax":     27000,
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
    # "ymax":     23000,
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
    "xmax":     250,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "m_{WW*} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["WW_mass_cut9"] = {
    "output":   "WW_mass_cut9",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     250,
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
    "rebin":    10,
    "xmin":     0 if 'nosel' in scheme else 50,
    "xmax":     300 if 'nosel' in scheme else 250,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "m_{WW*} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in scheme else 1,
    "extralab": extralab,
}

hists["WW_p_cut4"] = {
    "output":   "WW_p_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     200,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{WW*} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before selections",
}

# hists["WW_p_cut10"] = {
#     "output":   "WW_p_cut10",
#     "logy":     False,
#     "stack":    False,
#     "rebin":    5,
#     "xmin":     0,
#     # "xmax":     100,
#     # "ymin":     10,
#     # "ymax":     100000,
#     "xtitle":   "p_{WW*} [GeV]",
#     "ytitle":   "Events ",
#     # "scaleSig": 100,
#     "extralab": "Before selections",
# }

hists["WW_p_final"] = {
    "output":   "WW_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    "xmin":     0,
    "xmax":     180,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "p_{WW*} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in scheme else 1,
    "extralab": extralab,
}

hists["WW_theta_cut4"] = {
    "output":   "WW_theta_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     0,
    "xmax":     3.5,
    # "ymin":     10,
    "ymax":     3700,
    "xtitle":   "#theta_{WW*}",
    "ytitle":   "Events ",
    "scaleSig": 10,
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
    "scaleSig": 10,
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
    "scaleSig": 10,
    "extralab": "Before selections",
}

hists["zll_WW_dR_cut11"] = {
    "output":   "zll_WW_dR_cut11",
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
    "extralab": "Before #DeltaR(l^{#plus}l^{#minus}, l_{1}^{WW*}l_{2}^{WW*}) selection",
}

hists["zll_WW_dR_final"] = {
    "output":   "zll_WW_dR",
    "logy":     False,
    "stack":    False,
    "rebin":    10,
    "xmin":     2.5,
    "xmax":     7,
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
    "xmax":     250,
    # "ymin":     10,
    # "ymax":     300,
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
    "xmax":     375 if 'nosel' in scheme else 200,
    # "ymin":     10,
    # "ymax":     1000,
    "xtitle":   "E_{miss} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in scheme else 1,
    "extralab": extralab,
}






hists["true_Z_p_final"] = {
    "output":   "true_Z_p",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    # "xmin":     0,
    # "xmax":     375 if 'nosel' in scheme else 180,
    # "ymin":     10,
    "ymax":     100,
    "xtitle":   "E_{miss} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100,
    "extralab": extralab,
}

hists["true_Z_mass_final"] = {
    "output":   "true_Z_mass",
    "logy":     False,
    "stack":    False,
    "rebin":    5,
    # "xmin":     0,
    # "xmax":     375 if 'nosel' in scheme else 180,
    # "ymin":     10,
    "ymax":     100,
    "xtitle":   "E_{miss} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in scheme else 1,
    "extralab": extralab,
}

hists["true_lepton1_p_final"] = {
    "output":   "true_lepton1_p",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     375 if 'nosel' in scheme else 180,
    # "ymin":     10,
    # "ymax":     1000,
    "xtitle":   "E_{miss} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in scheme else 1,
    "extralab": extralab,
}

hists["true_lepton2_p_final"] = {
    "output":   "true_lepton2_p",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     375 if 'nosel' in scheme else 180,
    # "ymin":     10,
    # "ymax":     1000,
    "xtitle":   "E_{miss} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in scheme else 1,
    "extralab": extralab,
}

hists["truth_lepton_dR_final"] = {
    "output":   "truth_lepton_dR",
    "logy":     False,
    "stack":    False,
    # "rebin":    5,
    # "xmin":     0,
    # "xmax":     375 if 'nosel' in scheme else 180,
    # "ymin":     10,
    # "ymax":     1000,
    "xtitle":   "E_{miss} [GeV]",
    "ytitle":   "Events ",
    "scaleSig": 100 if 'nosel' in scheme else 1,
    "extralab": extralab,
}

# hists["eff_total_final"] = {
#     "output":   "eff_total",
#     "logy":     False,
#     "stack":    False,
#     # "rebin":    5,
#     # "xmin":     0,
#     # "xmax":     375 if 'nosel' in scheme else 180,
#     # "ymin":     10,
#     # "ymax":     1000,
#     "xtitle":   "Correct lepton pairing",
#     "ytitle":   "Events ",
#     "scaleSig": 100 if 'nosel' in scheme else 1,
#     "extralab": extralab,
# }


###

# acolinearity
hists["zll_acolinearity_cut4"] = {
    "output":   "zll_acolinearity_cut4",
    "logy":     False,
    "stack":    False,
    "rebin":    50,
    "xmin":     0,
    # "xmax":     1,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "cos(#theta_{acol})",
    "ytitle":   "Events ",
    "scaleSig": 10,
    "extralab": "Before cos(#theta_{acol}) cut",
}

hists["zll_acolinearity_final"] = {
    "output":   "zll_acolinearity",
    "logy":     False,
    "stack":    False,
    "rebin":    100,
    "xmin":     0,
    # "xmax":     1,
    # "ymin":     10,
    # "ymax":     100000,
    "xtitle":   "cos(#theta_{acol})",
    "ytitle":   "Events ",
    # "scaleSig": 100,
    "extralab": extralab,
}


# q^2
if is_plot_new:
    hists["vbf_q1_squared_cut4"] = {
        "output":   "vbf_q1_squared_cut4",
        "logy":     False,
        "stack":    False,
        "rebin":    1000,
        # "xmin":     0,
        # "xmax":     1,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "q_{1}^{2} [GeV^{2}]",
        "ytitle":   "Events ",
        "scaleSig": 20,
        "extralab": "Before selections",
    }

    hists["vbf_q1_squared_final"] = {
        "output":   "vbf_q1_squared",
        "logy":     False,
        "stack":    False,
        "rebin":    5000,
        # "xmin":     0,
        # "xmax":     1,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "q_{1}^{2} [GeV^{2}]",
        "ytitle":   "Events ",
        # "scaleSig": 100,
        # "extralab": "Before selections",
    }

    hists["vbf_q2_squared_cut4"] = {
        "output":   "vbf_q2_squared_cut4",
        "logy":     False,
        "stack":    False,
        "rebin":    1000,
        # "xmin":     0,
        # "xmax":     1,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "q_{2}^{2} [GeV^{2}]",
        "ytitle":   "Events ",
        "scaleSig": 10,
        "extralab": "Before selections",
    }

    hists["vbf_q2_squared_final"] = {
        "output":   "vbf_q2_squared",
        "logy":     False,
        "stack":    False,
        "rebin":    5000,
        # "xmin":     0,
        # "xmax":     1,
        # "ymin":     10,
        # "ymax":     100000,
        "xtitle":   "q_{2}^{2} [GeV^{2}]",
        "ytitle":   "Events ",
        # "scaleSig": 100,
        # "extralab": "Before selections",
    }
