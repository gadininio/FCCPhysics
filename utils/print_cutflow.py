import ROOT
import sys

if len(sys.argv) < 2:
    print("Usage: python print_cutflow.py <root_file_path>")
    exit(1)

root_file_path = sys.argv[1]

# Path to your ROOT file
hist_name = "cutFlow"  # Change if your histogram has a different name

# Open the ROOT file
file = ROOT.TFile.Open(root_file_path)
if not file or file.IsZombie():
    print("Error: Could not open ROOT file.")
    exit(1)

# Get the histogram
hist = file.Get(hist_name)
if not hist:
    print(f"Error: Histogram '{hist_name}' not found in file.")
    exit(1)

# Print bin contents and xlabels
nbins = hist.GetNbinsX()
print("Bin\tLabel\tContent")
for i in range(1, nbins + 1):
    label = hist.GetXaxis().GetBinLabel(i)
    content = hist.GetBinContent(i)
    print(f"{i}\t{label}\t{content}")

file.Close()


'''
python3 ../utils/print_cutflow.py outputs/hists/ee/wzp6_ee_eeH_HWW_ecm240.root
'''