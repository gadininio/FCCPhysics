'''
This script performs a simple cut optimization by scanning over all possible (low, high) bin combinations of a given histogram and calculating the signal significance (using the Asimov formula) for each window. It identifies the window that maximizes the significance.

Run with:
    python3 simple_cut_optim.py --path <path_to_histograms> --ecm <240_or_365> --variables <list_of_histogram_names> --use_simple_significance
    python3 simple_cut_optim.py --path '../../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full' --ecm 365 --variables WW_leps_dR_cut9
'''


#!/usr/bin/env python3
import ROOT
import math
import argparse

####################################
# User settings
####################################

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Combine cutflows and optionally add percentages.")
parser.add_argument('--path', '-p', help='Do not add percentage columns to the cutflow table', default='../../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_/')
parser.add_argument('--ecm', '-ecm', type=str, help='Do not add percentage columns to the cutflow table', default='365', choices=['240', '365'])
parser.add_argument('--debug', '-d', action='store_true', help='debug', default=False)
parser.add_argument('--variables', '-v', nargs='*', help='List of histogram names to optimise cuts on. If not provided, all histograms in the first signal file will be used.', default=[])
parser.add_argument('--use_asimov_significance', '-as', action='store_true', help='Use simple S/sqrt(S+B) significance instead of Asimov formula', default=False)
parser.add_argument('--xmin', '-xmin', type=float, help='Minimum x value for cut optimization (overrides histogram range)', default=None)
parser.add_argument('--xmax', '-xmax', type=float, help='Minimum x value for cut optimization (overrides histogram range)', default=None)
parser.add_argument('--rebin', '-r', type=int, help='Rebin histograms by this factor before optimization', default=1)
args = parser.parse_args()

ecm = args.ecm
debug = args.debug
path = args.path
variables = args.variables
asimov = args.use_asimov_significance
xmin = args.xmin
xmax = args.xmax

# path = '../../../outputs/higgs/zh_hww_4l/hists/full_nosel_20251207_100953/'  # for 240 GeV
# path = '../../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/nosel_/'  # for 365 GeV
# path = '../../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_/'  # for 365 GeV
# path = '../../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/tight_/'  # for 365 GeV
# path = '../../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/full_tight_/'  # for 365 GeV

# variables = [
#     "WW_leps_dR_cut9"
    
#     # "lep0_p_final",
#     # "lep1_p_final",
#     # "lep2_p_final",
#     # "lep3_p_final",
    
#     # "zll_m_final",
#     # "zll_p_final",
#     "zll_theta_final",
#     "zll_leps_dR_final",
#     # # "zll_recoil_m_final",
    
#     # # "cosThetaMiss_final",
#     # "missingEnergy_final",
#     "zll_WW_dR_final",
    
#     # "WW_mass_final",
#     # "WW_p_final",
#     "WW_theta_final",
#     "WW_phi_final",
#     # "WW_leps_dR_final",
#     "WW_lep0_p_final",
#     "WW_lep1_p_final",
#     "WW_lep0_theta_final",
#     "WW_lep1_theta_final",
#     "WW_lep0_phi_final",
#     "WW_lep1_phi_final",
# ]

signal_files = [
    f"wzp6_ee_mumuH_HWW_{'llnunu_' if ecm=='240' else ''}ecm{ecm}.root",
    f"wzp6_ee_eeH_HWW_{'llnunu_' if ecm=='240' else ''}ecm{ecm}.root",
]
background_files = [
    f"p8_ee_ZZ_ecm{ecm}.root",
    f"p8_ee_WW_ecm{ecm}.root",
    # f"p8_ee_WW_ee_ecm{ecm}.root",
    # f"p8_ee_WW_mumu_ecm{ecm}.root",
    # f"wzp6_ee_mumu_ecm{ecm}.root",
    # f"wzp6_ee_tautau_ecm{ecm}.root",
    # f"wzp6_ee_ee_Mee_30_150_ecm{ecm}.root",
]
if ecm == '365':
    background_files += ["p8_ee_tt_ecm365.root"]
# if 'inclWWInFit' in path:
    # background_files += [f"p8_ee_WW_ecm{ecm}.root"]
# else:
    # background_files += [f"p8_ee_WW_ee_ecm{ecm}.root", f"p8_ee_WW_mumu_ecm{ecm}.root",]


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

def full_integral(h):
    # To get the absolute total of the histogram
    return h.Integral(0, h.GetNbinsX() + 1)

####################################
# Load histogram names
####################################
hist_names = variables if variables is not None and len(variables)>0 else get_hist_names(path+'/'+signal_files[0])
print("Found histograms:", hist_names)


####################################
# Open files
####################################
f_sigs = [ROOT.TFile.Open(f'{path}/{f}') for f in signal_files]
f_bkgs = [ROOT.TFile.Open(f'{path}/{f}') for f in background_files]


####################################
# Loop over histograms and optimise cuts
####################################
results = {}

for hname in hist_names:
    
    print(f"Optimizing cuts for histogram: {hname}")
    
    # Sum of signals
    h_sig_sum = None
    for fs in f_sigs:
        if debug: print(f"  Loading signal histogram {hname} from file {fs.GetName()}...")
        hs = fs.Get(hname)
        if not hs:
            print(f"WARNING Histogram {hname} missing in signal file {fs.GetName()}. Check variable name!")
            continue
        if args.rebin > 1:
            hs = hs.Rebin(args.rebin)
        if h_sig_sum is None:
            h_sig_sum = hs.Clone("sig_sum_" + hname)
        else:
            h_sig_sum.Add(hs)

    # check if signal histogram was found. if not, exit.
    if h_sig_sum is None:
        print(f"ERROR: Histogram {hname} not found in any signal files. Skipping...")
        exit(1)

    # Sum of backgrounds
    h_bkg_sum = None
    for fb in f_bkgs:
        if debug: print(f"  Loading background histogram {hname} from file {fb.GetName()}...")
        hb = fb.Get(hname)
        if not hb:
            print(f"Histogram {hname} missing in background file {fb.GetName()}")
            continue
        if args.rebin > 1:
            hb = hb.Rebin(args.rebin)
        if h_bkg_sum is None:
            h_bkg_sum = hb.Clone("bkg_sum_" + hname)
        else:
            h_bkg_sum.Add(hb)

    # check if background histogram was found. if not, exit.
    if h_bkg_sum is None:
        print(f"ERROR: Histogram {hname} not found in any background files. Skipping...")
        exit(1)

    if debug:
        print(f"  Signal sum integral: {full_integral(h_sig_sum):.3f} (number of entries: {h_sig_sum.GetEntries():.0f}), Background sum integral: {full_integral(h_bkg_sum):.3f} (number of entries: {h_bkg_sum.GetEntries():.0f})")

    # if xmin and xmax are provided, instead of a scan, just calculate the significance for that fixed window
    if xmin is not None and xmax is not None:
        i_low = h_sig_sum.GetXaxis().FindBin(xmin)
        i_high = h_sig_sum.GetXaxis().FindBin(xmax)
        S = window_integral(h_sig_sum, i_low, i_high)
        B = window_integral(h_bkg_sum, i_low, i_high)
        
        if debug: print(f"  For fixed window [{xmin}, {xmax}] corresponding to bins [{i_low}, {i_high}], S = {S:.3f} and B = {B:.3f}")
        
        if asimov:
            Z = math.sqrt( 2*((S+B)*math.log(1+S/B) - S) ) if B > 0 else 0  # Asimov significance
        else:
            Z = S / math.sqrt(S + B)  # simple significance

        results[hname] = {
            "Z": Z,
            "bins": (i_low, i_high),
            "S": S,
            "B": B,
            "low_edge": h_sig_sum.GetXaxis().GetBinLowEdge(i_low),
            "high_edge": h_sig_sum.GetXaxis().GetBinUpEdge(i_high),
        }
        
        print(f"  For fixed window [{xmin}, {xmax}] (bins [{i_low}, {i_high}]), Z = {Z:.4f} with S={S:.3f} and B={B:.3f}")



        # print yields per sample
        print("\n  Signal yields:")
        for fs in f_sigs:
            hs = fs.Get(hname)
            if hs:
                s = window_integral(hs, i_low, i_high)
                s_tot = full_integral(hs)
                print(f"    {fs.GetName()}: {s:.3f} (eff={s/s_tot:.3%}, mean={hs.GetMean():.3f}, std={hs.GetStdDev():.3f})")
        print("  Background yields:")
        for fb in f_bkgs:
            hb = fb.Get(hname)
            if hb:
                b = window_integral(hb, i_low, i_high)
                b_tot = full_integral(hb)
                print(f"    {fb.GetName()}: {b:.3f} (eff={b/b_tot:.3%}, mean={hb.GetMean():.3f}, std={hb.GetStdDev():.3f})")
        print("\n")
                


        # # Find corresponding bins for the specified x range
        # i_low = h_sig_sum.GetXaxis().FindBin(xmin)
        # i_high = h_sig_sum.GetXaxis().FindBin(xmax)
        # if debug: print(f"  Restricting to x range [{xmin}, {xmax}] corresponding to bins [{i_low}, {i_high}]")
        # # Create new histograms with the restricted range
        # h_sig_sum_restricted = h_sig_sum.Clone("sig_sum_restricted_" + hname)
        # h_bkg_sum_restricted = h_bkg_sum.Clone("bkg_sum_restricted_" + hname)
        # for i in range(1, h_sig_sum.GetNbinsX() + 1):
        #     if i < i_low or i > i_high:
        #         h_sig_sum_restricted.SetBinContent(i, 0)
        #         h_bkg_sum_restricted.SetBinContent(i, 0)
        # h_sig_sum = h_sig_sum_restricted
        # h_bkg_sum = h_bkg_sum_restricted
        
        
    else: # scan over all windows to find the optimal one
        nbins = h_sig_sum.GetNbinsX()

        best_Z = -1
        best_pair = None
        best_S = 0
        best_B = 0

        # Scan all (low, high) bin combinations
        for i_low in range(0, nbins + 2):  # include underflow (0) and overflow (nbins+1)
            for i_high in range(i_low, nbins + 2):
                if debug: print(f"  Testing window bins [{i_low}, {i_high}]...", end="\r")
                
                S = window_integral(h_sig_sum, i_low, i_high)
                B = window_integral(h_bkg_sum, i_low, i_high)

                if S + B < min_events:
                    continue

                if asimov:
                    Z = math.sqrt( 2*((S+B)*math.log(1+S/B) - S) ) if B > 0 else 0  # Asimov significance
                else:
                    Z = S / math.sqrt(S + B)  # simple significance

                if Z > best_Z:
                    best_Z = Z
                    best_pair = (i_low, i_high)
                    best_S = S
                    best_B = B

        # Handle the edge cases for printing since overflow bins are taken into account.
        low_edge = h_sig_sum.GetXaxis().GetBinLowEdge(best_pair[0]) if best_pair[0] > 0 else float('-inf')
        high_edge = h_sig_sum.GetXaxis().GetBinUpEdge(best_pair[1]) if best_pair[1] <= nbins else float('inf')

        results[hname] = {
            "Z": best_Z,
            "bins": best_pair,
            "S": best_S,
            "B": best_B,
            "low_edge": low_edge,
            "high_edge": high_edge,
        }
        
        print(f"  Best Z = {best_Z:.4f} for bins [{best_pair[0]}, {best_pair[1]}] with S={best_S:.3f} and B={best_B:.3f}")


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

print("Significance forula used:", "Asimov formula" if asimov else "S/sqrt(S+B)")
print("Cut optimization completed.")

####################################
# Close files
####################################
for fs in f_sigs:
    fs.Close()
for fb in f_bkgs:
    fb.Close()