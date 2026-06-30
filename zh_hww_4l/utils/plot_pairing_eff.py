import ROOT
import os

#########################################################################################################
# Configuration
#########################################################################################################
# ecm = "365"
# scheme = "presel"
# lumi = " 3.0"
# label = "Preslections (f=0.4)"

ecm = "365"
scheme = "presel_chi2-1.0"
lumi = " 3.0"
label = "Preslections (f=1.0)"

# ecm = "365"
# scheme = "medium3"
# lumi = " 3.0"
# label = "Medium3 selections (f=0.4)"

# ecm = "240"
# scheme = "presel"
# lumi = "10.8"
# label = "Preslections (f=0.4)"

# ecm = "240"
# scheme = "presel_chi2-1.0"
# lumi = "10.8"
# label = "Preslections (f=0.1)"
#########################################################################################################

# Define the samples, their legend labels, and their specific colors
if ecm == "240":
    signal_samples = {
        "wzp6_ee_eeH_HWW_llnunu_ecm240":   {"label": "e^{+}e^{-} #rightarrow e^{+}e^{-}H(WW*)", "color": ROOT.kBlue+1},
        "wzp6_ee_mumuH_HWW_llnunu_ecm240": {"label": "e^{+}e^{-} #rightarrow #mu^{+}#mu^{-}H(WW*)", "color": ROOT.kGreen+2}
    }
    
    variables_to_plot = {
        "true_Z_p": {"xtitle": "True p_{Z} [GeV]", "rebin": 2, "ymin": 0.0, "ymax": 2}, 
        "true_Z_mass": {"xtitle": "True m_{Z} [GeV]", "rebin": 2, "ymin": 0.0, "ymax": 2}, 
        "true_lepton1_p": {"xtitle": "True Leading Lepton p [GeV]", "rebin": 2, "ymin": 0.0, "ymax": 2},
        "true_lepton2_p": {"xtitle": "True Sub-leading Lepton p [GeV]", "rebin": 2, "ymin": 0.0, "ymax": 2},
        "truth_lepton_dR": {"xtitle": "True #DeltaR(l_{1}, l_{2})", "rebin": 2, "ymin": 0.0, "ymax": 2},
    }
    
elif ecm == "365":
    signal_samples = {
        "wzp6_ee_eeH_HWW_ecm365":   {"label": "e^{+}e^{-} #rightarrow e^{+}e^{-}H(WW*)", "color": ROOT.kBlue+1},
        "wzp6_ee_mumuH_HWW_ecm365": {"label": "e^{+}e^{-} #rightarrow #mu^{+}#mu^{-}H(WW*)", "color": ROOT.kGreen+2}
    }
    
    variables_to_plot = {
        "true_Z_p": {"xtitle": "True p_{Z} [GeV]", "rebin": 4, "ymin": 0.0, "ymax": 2}, 
        "true_Z_mass": {"xtitle": "True m_{Z} [GeV]", "rebin": 5, "ymin": 0.2, "ymax": 1.7}, 
        "true_lepton1_p": {"xtitle": "True Leading Lepton p [GeV]", "rebin": 4, "ymin": 0.6, "ymax": 1.4},
        "true_lepton2_p": {"xtitle": "True Sub-leading Lepton p [GeV]", "rebin": 4, "ymin": 0.6, "ymax": 1.4},
        "truth_lepton_dR": {"xtitle": "True #DeltaR(l_{1}, l_{2})", "rebin": 2},
    }

base_dir = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{scheme}"
output_dir = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{scheme}/pairing_eff/"

os.makedirs(output_dir, exist_ok=True)

def full_integral(h):
    
    # To get the absolute total of the histogram
    return h.Integral(0, h.GetNbinsX() + 1)

def calculate_total_efficiency(h_num, h_den):
    # Calculate total efficiency with proper error handling
    num = full_integral(h_num)
    den = full_integral(h_den)
    
    if den > 0:
        eff = num / den
        # Calculate binomial error: sqrt(eff * (1 - eff) / den)
        err = (eff * (1 - eff) / den)**0.5 if den > 0 else 0
    else:
        eff = 0
        err = 0
    
    return eff, err

def get_total_efficiency(h_num, h_den, sample_name):
    eff, err = calculate_total_efficiency(h_num, h_den)
    print(f"{sample_name}: Total Efficiency = {eff:.4f} ± {err:.4f} (Num: {full_integral(h_num):.4f}, Den: {full_integral(h_den):.4f})")
    return f"#varepsilon = {eff:.4f} #pm {err:.4f}"

def plot_efficiencies():
    c = ROOT.TCanvas("c", "Efficiency Canvas", 800, 600)
    
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)

    for var, var_dict in variables_to_plot.items():
        xtitle = var_dict["xtitle"]
        rebin = var_dict["rebin"]
        ymin = var_dict.get("ymin", 0.0)
        ymax = var_dict.get("ymax", 2.0)
        
        num_name = f"{var}_selected_final"
        den_name = f"{var}_final"

        # Dictionaries to securely store histograms in memory
        hists_num = {}
        hists_den = {}
        
        h_num_total = None
        h_den_total = None

        total_eff = {}  # Store total efficiencies for each sample for printing and using in legends

        # 1. Extract and Accumulate Histograms
        for sample_name in signal_samples.keys():
            input_file = os.path.join(base_dir, f"{sample_name}.root")
            f = ROOT.TFile.Open(input_file, "READ")
            
            if not f or f.IsZombie():
                print(f"Error: Cannot open {input_file}. Skipping.")
                continue

            h_num_raw = f.Get(num_name)
            h_den_raw = f.Get(den_name)

            if not h_num_raw or not h_den_raw:
                print(f"Warning: Missing '{num_name}' or '{den_name}' in {sample_name}.root.")
                f.Close()
                continue

            # Clone and detach to prevent memory wiping when file closes
            h_num = h_num_raw.Clone(f"{num_name}_{sample_name}")
            h_den = h_den_raw.Clone(f"{den_name}_{sample_name}")
            h_num.SetDirectory(0)
            h_den.SetDirectory(0)
            
            total_eff[sample_name] = get_total_efficiency(h_num, h_den, sample_name)
            
            hists_num[sample_name] = h_num
            hists_den[sample_name] = h_den

            # Accumulate the totals
            if h_num_total is None:
                h_num_total = h_num.Clone(f"{num_name}_total")
                h_den_total = h_den.Clone(f"{den_name}_total")
                h_num_total.SetDirectory(0)
                h_den_total.SetDirectory(0)
            else:
                h_num_total.Add(h_num)
                h_den_total.Add(h_den)

            f.Close()

        # rebin if needed
        if rebin > 1:
            h_num_total.Rebin(rebin)
            h_den_total.Rebin(rebin)
            for sample_name in signal_samples.keys():
                if sample_name in hists_num:
                    hists_num[sample_name].Rebin(rebin)
                    hists_den[sample_name].Rebin(rebin)

        # 2. Build and Draw TEfficiency Objects
        if h_num_total is not None and h_den_total is not None:
            c.Clear()
            c.SetGrid()
            c.SetTicks(1, 1)

            # Setup Legend (X1, Y1, X2, Y2) - adjust coordinates to avoid covering data
            leg = ROOT.TLegend(0.15, 0.60, 0.5, 0.75)
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)
            leg.SetTextSize(0.035)

            # Create Total Efficiency
            eff_total = ROOT.TEfficiency(h_num_total, h_den_total)
            eff_total.SetTitle(f";{xtitle};Lepton Pairing Efficiency")
            eff_total.SetMarkerStyle(20)
            eff_total.SetMarkerSize(1.2)
            eff_total.SetMarkerColor(ROOT.kBlack)
            eff_total.SetLineColor(ROOT.kBlack)
            eff_total.SetLineWidth(2)
            # eff_total.GetXaxis().SetTitleOffset(1.2)
            
            # Draw the first one with "AP" to create axes
            eff_total.Draw("AP")
            
            # Force standard Y-axis limits (0.0 to 1.1)
            ROOT.gPad.Update()
            graph_total = eff_total.GetPaintedGraph()
            if graph_total:
                graph_total.SetMinimum(ymin)
                graph_total.SetMaximum(ymax)

            total_eff_str = get_total_efficiency(h_num_total, h_den_total, "Combined Signal")
            leg.AddEntry(eff_total, f"Combined Signal ({total_eff_str})", "pl")

            # Create and draw individual sample efficiencies
            eff_list = [] # Store references so they aren't garbage collected
            for sample_name in signal_samples.keys():
                if sample_name in hists_num:
                    eff_sample = ROOT.TEfficiency(hists_num[sample_name], hists_den[sample_name])
                    
                    # Apply specific styling
                    color = signal_samples[sample_name]["color"]
                    eff_sample.SetMarkerStyle(21) # Square marker
                    eff_sample.SetMarkerSize(0.9)
                    eff_sample.SetMarkerColor(color)
                    eff_sample.SetLineColor(color)
                    eff_sample.SetLineWidth(2)

                    # Draw over the existing axes
                    eff_sample.Draw("P same")
                    leg.AddEntry(eff_sample, signal_samples[sample_name]["label"] + f" ({total_eff[sample_name]})", "pl")
                    
                    eff_list.append(eff_sample)

            # Draw the legend
            leg.Draw()

            # Draw standard FCC text
            latex_y = 0.92
            latex.DrawLatex(0.10, 0.91, "#bf{FCC-ee} IDEA Simulation (Delphes)")
            latex.DrawLatex(0.62, 0.91, f"#sqrt{{s}} = {ecm} GeV, {lumi} ab^{{-1}}")
            latex.DrawLatex(0.15, latex_y-0.10, "e^{+}e^{-} #rightarrow Z(ll)H, H #rightarrow WW* #rightarrow l#nul#nu")
            latex.DrawLatex(0.15, latex_y-0.15, label)

            # Save the plot
            out_name = os.path.join(output_dir, f"pairing_eff_{var}.pdf")
            c.SaveAs(out_name)
            print(f"Saved {out_name}")

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    plot_efficiencies()