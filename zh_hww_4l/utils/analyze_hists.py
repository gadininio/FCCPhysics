'''
This script processes ROOT histograms to calculate their full integrals and efficiencies within specified ranges. It can handle both individual ROOT files and directories containing multiple ROOT files. 

Run with:

    1. Process a single file, all histograms (full integral only):

        python3 analyze_hists.py data.root

    2. Process a single file, specific histogram (full integral only):

        python3 analyze_hists.py data.root -n "my_histogram"

    3. Process a single file, specific histogram, with an xmin and xmax range:

        python3 analyze_hists.py data.root -n "my_histogram" --xmin 10.0 --xmax 50.0

    4. Process an entire directory, all histograms, with an xmin and xmax range:

        python3 analyze_hists.py /path/to/root/files/ --xmin 5.0 --xmax 20.0

    5. View the help menu to see all available options:

        python3 analyze_hists.py -h
'''


import os
import glob
import ctypes
import argparse
import ROOT

# Run in batch mode to prevent graphical windows from opening
ROOT.gROOT.SetBatch(True)

def process_histogram(hist, xmin=None, xmax=None):
    """
    Calculates the integral and efficiency of a given TH1 histogram.
    Handles missing xmin or xmax by using the histogram's axis limits.
    """
    err_full = ctypes.c_double(0.0)
    
    # Calculate full integral from bin 1 to the last bin
    full_integral = hist.IntegralAndError(1, hist.GetNbinsX(), err_full)

    print(f"  -> Histogram: {hist.GetName()}")

    # If no range is specified at all, only print the full integral
    if xmin is None and xmax is None:
        print(f"     Full Integral: {full_integral:.4f} +/- {err_full.value:.4f}")
        return full_integral, err_full.value, None

    # If one limit is missing, use the histogram's actual x-axis limits
    actual_xmin = xmin if xmin is not None else hist.GetXaxis().GetXmin()
    actual_xmax = xmax if xmax is not None else hist.GetXaxis().GetXmax()

    bin_min = hist.FindFixBin(actual_xmin)
    bin_max = hist.FindFixBin(actual_xmax)

    err_partial = ctypes.c_double(0.0)
    partial_integral = hist.IntegralAndError(bin_min, bin_max, err_partial)

    # Calculate efficiency
    efficiency = 0.0
    if full_integral != 0:
        efficiency = partial_integral / full_integral

    print(f"     Full Integral: {full_integral:.4f} +/- {err_full.value:.4f}")
    print(f"     Range [{actual_xmin}, {actual_xmax}] Integral: {partial_integral:.4f} +/- {err_partial.value:.4f}")
    print(f"     Efficiency: {efficiency * 100.0:.2f}%")

    return full_integral, partial_integral, efficiency


def analyze_root_data(input_path, hist_names=None, xmin=None, xmax=None):
    """
    Scans a file or directory and processes the requested histograms.
    """
    files_to_process = []

    if os.path.isdir(input_path):
        files_to_process = glob.glob(os.path.join(input_path, "*.root"))
        if not files_to_process:
            print(f"Error: No ROOT files found in directory '{input_path}'")
            return
    elif os.path.isfile(input_path) and input_path.endswith(".root"):
        files_to_process = [input_path]
    else:
        print(f"Error: Invalid input path or file '{input_path}'")
        return

    for file_path in files_to_process:
        print(f"\nProcessing file: {file_path}")
        root_file = ROOT.TFile.Open(file_path, "READ")

        if not root_file or root_file.IsZombie():
            print(f"Failed to open {file_path}")
            continue

        hists_to_process = []
        
        # If a list of specific histogram names is given, fetch them
        if hist_names:
            for name in hist_names:
                obj = root_file.Get(name)
                if obj and obj.InheritsFrom("TH1"):
                    hists_to_process.append(obj)
                else:
                    print(f"Warning: Histogram '{name}' not found or is not a 1D histogram in {file_path}")
        
        # If no histogram names are given, fetch all TH1 objects
        else:
            for key in root_file.GetListOfKeys():
                obj = key.ReadObj()
                if obj.InheritsFrom("TH1"):
                    hists_to_process.append(obj)

        if not hists_to_process:
            print("No histograms to process in this file.")

        for hist in hists_to_process:
            process_histogram(hist, xmin, xmax)

        root_file.Close()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Calculate full integrals and efficiencies of ROOT histograms.")
    parser.add_argument("input_path", type=str, help="Path to a specific .root file or a directory containing .root files.")
    parser.add_argument("-n", "--names", nargs='+', type=str, default=None, help="Name(s) of specific histogram(s) to process. Separate multiple names with spaces. If omitted, all 1D histograms are processed.")
    parser.add_argument("-xmin", "--xmin", type=float, default=None, help="Minimum x-axis value for the efficiency range.")
    parser.add_argument("-xmax", "--xmax", type=float, default=None, help="Maximum x-axis value for the efficiency range.")
    args = parser.parse_args()

    analyze_root_data(args.input_path, args.names, args.xmin, args.xmax)