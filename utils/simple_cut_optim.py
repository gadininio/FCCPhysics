#!/usr/bin/env python3
import ROOT
import math
import itertools

####################################
# User settings
####################################

debug = True
path = '../../outputs/higgs/zh_hww_4l/hists/full_nosel_20251207_100953/'
variables = [
    "lep0_p_final",
    "lep1_p_final",
    "lep2_p_final",
    "lep3_p_final",
    "zll_m_final",
    "zll_m_final",
    "zll_p_final",
    # "zll_recoil_m_final",
    # "cosThetaMiss_final",
    "missingEnergy_final",
    "WW_mass_final",
    "WW_p_final",
    "WW_leps_dR_final",
]

signal_files = [
    "wzp6_ee_mumuH_HWW_ecm240.root",
    "wzp6_ee_eeH_HWW_ecm240.root",
]
background_files = [
    "p8_ee_ZZ_ecm240.root",
    "p8_ee_WW_ecm240.root",
    "wzp6_ee_mumu_ecm240.root",
    # "wzp6_ee_tautau_ecm240.root",
    "wzp6_ee_ee_Mee_30_150_ecm240.root",
]

# Minimum events in window required to consider a cut
min_events = 1e-6


####################################
# Helper: get histogram names from a file
####################################
def get_hist_names(fname):
    f = ROOT.TFile.Open(fname)
    keys = f.GetListOfKeys()
    names = [k.GetName() for k in keys if isinstance(f.Get(k.GetName()), ROOT.TH1)]
    f.Close()
    return names


####################################
# Helper: integrate histogram between bins (inclusive)
####################################
def window_integral(h, i_low, i_high):
    return h.Integral(i_low, i_high)


####################################
# Load histogram names
####################################
hist_names = variables if variables is not None and len(variables)>0 else get_hist_names(path+signal_files[0])
print("Found histograms:", hist_names)


####################################
# Open files
####################################
f_sigs = [ROOT.TFile.Open(path+f) for f in signal_files]
f_bkgs = [ROOT.TFile.Open(path+f) for f in background_files]


####################################
# Loop over histograms and optimise cuts
####################################
results = {}

for hname in hist_names:
    
    print(f"Optimizing cuts for histogram: {hname}")
    
    # Sum of signals
    h_sig_sum = None
    for fs in f_sigs:
        hs = fs.Get(hname)
        if not hs:
            print(f"Histogram {hname} missing in signal file {fs.GetName()}")
            continue
        if h_sig_sum is None:
            h_sig_sum = hs.Clone("sig_sum_" + hname)
        else:
            h_sig_sum.Add(hs)

    # Sum of backgrounds
    h_bkg_sum = None
    for fb in f_bkgs:
        hb = fb.Get(hname)
        if not hb:
            print(f"Histogram {hname} missing in background file {fb.GetName()}")
            continue
        if h_bkg_sum is None:
            h_bkg_sum = hb.Clone("bkg_sum_" + hname)
        else:
            h_bkg_sum.Add(hb)

    nbins = h_sig_sum.GetNbinsX()

    best_Z = -1
    best_pair = None
    best_S = 0
    best_B = 0

    # Scan all (low, high) bin combinations
    for i_low in range(1, nbins + 1):
        for i_high in range(i_low, nbins + 1):
            if debug: print(f"  Testing window bins [{i_low}, {i_high}]...", end="\r")
            
            S = window_integral(h_sig_sum, i_low, i_high)
            B = window_integral(h_bkg_sum, i_low, i_high)

            if S + B < min_events:
                continue

            # Z = S / math.sqrt(S + B)  # simple significance
            Z = math.sqrt( 2*((S+B)*math.log(1+S/B) - S) ) if B > 0 else 0  # Asimov significance

            if Z > best_Z:
                best_Z = Z
                best_pair = (i_low, i_high)
                best_S = S
                best_B = B

    results[hname] = {
        "Z": best_Z,
        "bins": best_pair,
        "S": best_S,
        "B": best_B,
        "low_edge": h_sig_sum.GetXaxis().GetBinLowEdge(best_pair[0]),
        "high_edge": h_sig_sum.GetXaxis().GetBinUpEdge(best_pair[1]),
    }


####################################
# Print results
####################################
print("\n============================")
print(" OPTIMAL DOUBLE-WINDOW CUTS ")
print("============================\n")

for hname, r in results.items():
    print(f"Histogram: {hname}")
    print(f"  Best significance Z = {r['Z']:.4f}")
    print(f"  Cut window in bins = {r['bins']}")
    print(f"  Cut window in x    = [{r['low_edge']:.4f}, {r['high_edge']:.4f}]")
    print(f"  S = {r['S']:.3f},  B = {r['B']:.3f}")
    print("")


####################################
# Close files
####################################
for fs in f_sigs:
    fs.Close()
for fb in f_bkgs:
    fb.Close()