import ROOT
import os

# Configuration
ecm = "365"
scheme = "medium_inclWWInFit_iso"
lumi = "3"

# Define the list of samples to combine
signal_samples = [
    "wzp6_ee_eeH_HWW_ecm365",
    "wzp6_ee_mumuH_HWW_ecm365"
]

base_dir = f"../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{scheme}"
output_dir = f"../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{scheme}/efficiency_combined/"

os.makedirs(output_dir, exist_ok=True)

variables_to_plot = {
    "true_Z_p": "True p_{Z} [GeV]",
    "true_Z_mass": "True m_{Z} [GeV]",
    "true_lepton1_p": "True Leading Lepton p [GeV]",
    "true_lepton2_p": "True Sub-leading Lepton p [GeV]",
    "truth_lepton_dR": "True #DeltaR(l_{1}, l_{2})"
}

def plot_efficiencies():
    c = ROOT.TCanvas("c", "Efficiency Canvas", 800, 600)
    
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)

    # We loop over the variables we want to plot
    for var, xtitle in variables_to_plot.items():
        num_name = f"{var}_selected_final"
        den_name = f"{var}_final"

        h_num_total = None
        h_den_total = None
        
        # We must keep the files open during the loop to avoid memory faults
        open_files = []

        # Loop over the samples and accumulate the histograms
        for sample in signal_samples:
            input_file = os.path.join(base_dir, f"{sample}.root")
            f = ROOT.TFile.Open(input_file, "READ")
            
            if not f or f.IsZombie():
                print(f"Error: Cannot open {input_file}. Skipping.")
                continue
                
            open_files.append(f)

            h_num = f.Get(num_name)
            h_den = f.Get(den_name)

            if not h_num or not h_den:
                print(f"Warning: Could not find '{num_name}' or '{den_name}' in {sample}.root. Skipping.")
                continue

            # If this is the first file, clone the histograms to act as our master accumulators
            if h_num_total is None:
                h_num_total = h_num.Clone(f"{num_name}_total")
                h_den_total = h_den.Clone(f"{den_name}_total")
                
                # Detach them from the file directory so they survive when files are closed
                h_num_total.SetDirectory(0)
                h_den_total.SetDirectory(0)
            else:
                # For subsequent files, add them to the master accumulator
                h_num_total.Add(h_num)
                h_den_total.Add(h_den)

        # Proceed to plot only if we successfully found histograms
        if h_num_total is not None and h_den_total is not None:
            
            # Create TEfficiency from the combined histograms
            eff = ROOT.TEfficiency(h_num_total, h_den_total)
            eff.SetTitle(f";{xtitle};Pairing Efficiency")

            eff.SetMarkerStyle(20)
            eff.SetMarkerSize(1.2)
            eff.SetMarkerColor(ROOT.kRed)
            eff.SetLineColor(ROOT.kRed)
            eff.SetLineWidth(2)

            c.Clear()
            c.SetGrid()
            c.SetTicks(1, 1)

            eff.Draw("AP")

            ROOT.gPad.Update()
            graph = eff.GetPaintedGraph()
            if graph:
                graph.SetMinimum(0.0)
                graph.SetMaximum(1.1)

            # Draw text showing combined samples
            latex.DrawLatex(0.15, 0.85, "#bf{FCC-ee} IDEA Simulation (Delphes)")
            latex.DrawLatex(0.15, 0.80, f"#sqrt{{s}} = {ecm} GeV")
            latex.DrawLatex(0.15, 0.75, f"L = {lumi} " + "ab^{-1}")
            latex.DrawLatex(0.15, 0.70, "e^{+}e^{-} #rightarrow Z(ll) H#left[W(l#nu)W(l#nu)#right]")

            out_name = os.path.join(output_dir, f"pairing_eff_vs_{var}.pdf")
            c.SaveAs(out_name)
            print(f"Saved {out_name}")

        # Clean up files after processing the variable
        for f in open_files:
            f.Close()

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    plot_efficiencies()