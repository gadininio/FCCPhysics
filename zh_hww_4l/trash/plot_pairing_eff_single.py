import ROOT
import os

# Configuration matching your paths
ecm = "365"
scheme = "presel"
signal_sample = "wzp6_ee_mumuH_HWW_ecm365" # Test on your muon signal first

# Path to the ROOT file produced by your histmaker
input_file = f"../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{scheme}/{signal_sample}.root"
output_dir = f"../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{scheme}/efficiency/"

os.makedirs(output_dir, exist_ok=True)

def plot_eff():
    # 1. Open the file
    f = ROOT.TFile.Open(input_file, "READ")
    if not f or f.IsZombie():
        print(f"Error: Cannot open {input_file}")
        return

    # 2. Grab the Numerator and Denominator histograms
    # (Replace these strings with the exact names you used in your histmaker df.Histo1D calls)
    h_num = f.Get("num_pZ") 
    h_den = f.Get("den_pZ")

    if not h_num or not h_den:
        print("Error: Could not find numerator or denominator histograms in the file.")
        return

    # 3. Create the TEfficiency object
    pZ_efficiency = ROOT.TEfficiency(h_num, h_den)
    pZ_efficiency.SetTitle(";True p_{Z} [GeV];Pairing Efficiency")
    
    # 4. Styling
    pZ_efficiency.SetMarkerStyle(20)
    pZ_efficiency.SetMarkerSize(1.2)
    pZ_efficiency.SetMarkerColor(ROOT.kRed)
    pZ_efficiency.SetLineColor(ROOT.kRed)
    pZ_efficiency.SetLineWidth(2)

    # 5. Draw the canvas
    c = ROOT.TCanvas("c", "Efficiency Canvas", 800, 600)
    c.SetGrid()
    c.SetTicks(1, 1)
    
    # Draw with "AP" (Axis and Points)
    pZ_efficiency.Draw("AP")
    
    # Force the Y-axis to scale sensibly (0 to 1.1 so points don't clip the top)
    ROOT.gPad.Update() 
    graph = pZ_efficiency.GetPaintedGraph()
    if graph:
        graph.SetMinimum(0.0)
        graph.SetMaximum(1.1)

    # 6. Add FCC styling text
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)
    latex.DrawLatex(0.15, 0.85, "#bf{FCC-ee} Simulation (Delphes)")
    latex.DrawLatex(0.15, 0.80, f"e^{{+}}e^{{-}} #rightarrow ZH #rightarrow #mu^{{+}}#mu^{{-}} WW^{{*}} (#sqrt{{s}} = {ecm} GeV)")

    # 7. Save the plot
    out_name = os.path.join(output_dir, "pairing_efficiency_vs_pZ.pdf")
    c.SaveAs(out_name)
    print(f"Saved efficiency plot to {out_name}")

if __name__ == "__main__":
    # Prevent ROOT from opening X11 windows
    ROOT.gROOT.SetBatch(True)
    plot_eff()