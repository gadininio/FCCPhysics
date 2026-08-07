
'''
Run with:
    python3 plot_nll.py /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/combined_results/higgsCombine_MyScan.MultiDimFit.mH120.root
'''


import ROOT

# get from the user the path to the Combine output file
import sys
if len(sys.argv) != 2:
    print("Usage: python plot_nll.py <path_to_combine_output_file: higgsCombine_MyScan.MultiDimFit.mH120.root>")
    sys.exit(1)

input_file_path = sys.argv[1]

# Configure ROOT to hide the canvas output during batch generation
ROOT.gROOT.SetBatch(True)

# Open the Combine output file and get the TTree
file = ROOT.TFile.Open(input_file_path)
tree = file.Get("limit")

# Extract the points into a TGraph
graph = ROOT.TGraph()
n = 0

for event in tree:
    # Combine saves the best-fit point at quantileExpected == -1. 
    # We want to skip it if it creates a duplicate point at the minimum, 
    # but drawing all valid deltaNLL points works fine.
    
    r_val = event.r
    # Multiply by 2 to get -2 Delta NLL
    nll_val = 2 * event.deltaNLL 
    
    graph.SetPoint(n, r_val, nll_val)
    n += 1

# Sort the points by the x-axis (r) so the line draws correctly
graph.Sort()


# --- 3. Helper Function to Calculate Crossings ---
def get_crossings(g, level):
    crossings = []
    # Iterate through the points to find where the line crosses the requested level
    for i in range(g.GetN() - 1):
        x1, y1 = g.GetPointX(i), g.GetPointY(i)
        x2, y2 = g.GetPointX(i+1), g.GetPointY(i+1)
        
        # If the Y values straddle the level, interpolate the exact X coordinate
        if (y1 - level) * (y2 - level) <= 0 and y1 != y2:
            slope = (y2 - y1) / (x2 - x1)
            x_cross = x1 + (level - y1) / slope
            crossings.append(x_cross)
    return crossings

# Calculate 1-sigma and 2-sigma precision values
cross1 = get_crossings(graph, 1.0)
cross4 = get_crossings(graph, 4.0)

if len(cross1) >= 2:
    prec_1 = (cross1[-1] - cross1[0]) / 2.0
    print("1-sigma precision: {:.2f}%".format(prec_1 * 100), "from {:.3f} to {:.3f}".format(cross1[0], cross1[-1]))

if len(cross4) >= 2:
    prec_2 = (cross4[-1] - cross4[0]) / 2.0
    print("2-sigma precision: {:.2f}%".format(prec_2 * 100), "from {:.3f} to {:.3f}".format(cross4[0], cross4[-1]))

# --- Draw the Plot ---
# Style the Graph
# graph.SetTitle("Likelihood Scan;Signal Strength (r);-2#Delta NLL")
graph.SetTitle(";Signal Strength (#mu);-2#Delta NLL")
graph.SetLineWidth(2)
graph.SetLineColor(ROOT.kBlue)

# set distance between the xaxis title and the axis
graph.GetXaxis().SetTitleOffset(1.2)

# Create the Canvas and Draw
canvas = ROOT.TCanvas("c1", "NLL Scan", 800, 600)
graph.Draw("AL") # A = Axis, L = Line

# Set Y-axis limits so we can see the 1-sigma and 2-sigma crossings clearly
graph.GetYaxis().SetRangeUser(0, 5)

# Draw horizontal lines for 1-sigma (y=1) and 2-sigma (y=4)
line1 = ROOT.TLine(graph.GetXaxis().GetXmin(), 1.0, graph.GetXaxis().GetXmax(), 1.0)
line1.SetLineStyle(2) # Dashed
line1.SetLineColor(ROOT.kRed)
line1.Draw("same")

line2 = ROOT.TLine(graph.GetXaxis().GetXmin(), 4.0, graph.GetXaxis().GetXmax(), 4.0)
line2.SetLineStyle(2)
line2.SetLineColor(ROOT.kRed)
line2.Draw("same")

# Add the Precision Labels
latex = ROOT.TLatex()
latex.SetTextSize(0.035)
latex.SetTextFont(42)
latex.SetTextAlign(11) # Align to the Bottom-Left of the coordinates
latex.SetTextColor(ROOT.kRed)
latex.DrawLatex(1.121, 1.0-0.05, "1#sigma")
latex.DrawLatex(1.121, 4.0-0.05, "2#sigma")

# Save the plot
# get path from input_file_path
import os
output_dir = os.path.dirname(input_file_path)
canvas.SaveAs(f"{output_dir}/nll_scan.pdf")
# canvas.SaveAs("nll_scan.png")

print("Plot saved to nll_scan.pdf")