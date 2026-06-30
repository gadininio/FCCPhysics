import ROOT

# Configure ROOT to hide the canvas output during batch generation
ROOT.gROOT.SetBatch(True)

# 1. Open the Combine output file and get the TTree
file = ROOT.TFile.Open("higgsCombine_MyScan.MultiDimFit.mH120.root")
tree = file.Get("limit")

# 2. Extract the points into a TGraph
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

# 3. Style the Graph
graph.SetTitle("Likelihood Scan;Signal Strength (r);-2#Delta NLL")
graph.SetLineWidth(2)
graph.SetLineColor(ROOT.kBlue)

# 4. Create the Canvas and Draw
canvas = ROOT.TCanvas("c1", "NLL Scan", 800, 600)
graph.Draw("AL") # A = Axis, L = Line

# Set Y-axis limits so we can see the 1-sigma and 2-sigma crossings clearly
graph.GetYaxis().SetRangeUser(0, 5)

# 5. Draw horizontal lines for 1-sigma (y=1) and 2-sigma (y=4)
line1 = ROOT.TLine(graph.GetXaxis().GetXmin(), 1.0, graph.GetXaxis().GetXmax(), 1.0)
line1.SetLineStyle(2) # Dashed
line1.SetLineColor(ROOT.kRed)
line1.Draw("same")

line2 = ROOT.TLine(graph.GetXaxis().GetXmin(), 4.0, graph.GetXaxis().GetXmax(), 4.0)
line2.SetLineStyle(2)
line2.SetLineColor(ROOT.kRed)
line2.Draw("same")

# 6. Save the plot
canvas.SaveAs("nll_scan.pdf")
canvas.SaveAs("nll_scan.png")

print("Plot saved to nll_scan.pdf and nll_scan.png")