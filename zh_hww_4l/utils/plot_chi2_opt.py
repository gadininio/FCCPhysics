'''
Run:

python3 plot_chi2_opt.py --ecm 365 --base-scheme presel --lumi 3.0 --chi2-default 0.4 --ymax 1.15 --ymin 0.55 --label "Preslections"
python3 plot_chi2_opt.py --ecm 365 --base-scheme medium --lumi 3.0 --chi2-default 0.4 --ymax 1.3 --ymin 0.7 --label "Medium selections"
python3 plot_chi2_opt.py --ecm 365 --base-scheme medium2 --lumi 3.0 --chi2-default 0.4 --ymax 1.3 --ymin 0.7 --label "Medium2 selections"
python3 plot_chi2_opt.py --ecm 365 --base-scheme medium3 --lumi 3.0 --chi2-default 0.4 --ymax 1.3 --ymin 0.7 --label "Medium3 selections"
python3 plot_chi2_opt.py --ecm 240 --base-scheme presel --lumi 10.8 --chi2-default 0.4 --ymax 1.02 --ymin 0.85 --label "Preslections"
'''

import argparse
import ROOT
import os
from array import array

# The baseline variable we will use to count total events
var_to_count = "true_Z_p"
num_name = f"{var_to_count}_selected_final"
den_name = f"{var_to_count}_final"

# Define the f values you ran
f_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot the lepton-pairing chi2 optimization for a selected configuration."
    )
    parser.add_argument("--ecm", required=True, help="Center-of-mass energy in GeV (for example, 240 or 365).")
    parser.add_argument("--base-scheme", required=True, help="Base selection scheme name.")
    parser.add_argument("--lumi", required=True, type=float, help="Integrated luminosity in ab^-1.")
    parser.add_argument(
        "--chi2-default",
        required=True,
        type=float,
        help="Default f value whose histograms use the unmodified base scheme name.",
    )
    parser.add_argument("--ymax", required=True, type=float, help="Upper limit of the plot's y-axis.")
    parser.add_argument("--ymin", required=True, type=float, help="Lower limit of the plot's y-axis.")
    parser.add_argument("--label", required=True, help="Selection label displayed on the plot.")
    return parser.parse_args()

def full_integral(h):
    return h.Integral(0, h.GetNbinsX() + 1)

def plot_optimization(args):
    ecm = args.ecm
    base_scheme = args.base_scheme
    lumi = args.lumi
    chi2_default = args.chi2_default
    ymax = args.ymax
    ymin = args.ymin
    label = args.label

    # Define the samples, their legend labels, and their specific colors
    signal_samples = {
        f"wzp6_ee_eeH_HWW_{'llnunu_' if ecm == '240' else ''}ecm{ecm}": {
            # "label": "e^{+}e^{-} #rightarrow e^{+}e^{-}H(WW*)",
            "label": "e^{+}e^{-}H",
            "color": ROOT.kBlue + 1,
            "marker_style": 21,
        },
        f"wzp6_ee_mumuH_HWW_{'llnunu_' if ecm == '240' else ''}ecm{ecm}": {
            # "label": "e^{+}e^{-} #rightarrow #mu^{+}#mu^{-}H(WW*)",
            "label": "#mu^{+}#mu^{-}H",
            "color": ROOT.kGreen + 2,
            "marker_style": 22,
        },
    }

    output_dir = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{base_scheme}/chi2_opt/"
    os.makedirs(output_dir, exist_ok=True)

    # Dictionaries to hold the raw array data for TGraphErrors
    data = {
        "total": {"x": array('d'), "y": array('d'), "ex": array('d'), "ey": array('d')}
    }
    for sample in signal_samples.keys():
        data[sample] = {"x": array('d'), "y": array('d'), "ex": array('d'), "ey": array('d')}

    # 1. Loop over each parameter value
    for f_value in f_values:
        
        if f_value == chi2_default:
            scheme = base_scheme
        else:
            scheme = f"{base_scheme}_chi2-{f_value:.1f}"
        input_dir = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{scheme}"
        
        total_num = 0.0
        total_den = 0.0

        for sample_name in signal_samples.keys():
            file_path = os.path.join(input_dir, f"{sample_name}.root")
            file = ROOT.TFile.Open(file_path, "READ")
            
            if not file or file.IsZombie():
                print(f"Warning: Cannot open {file_path}. Skipping.")
                continue
                
            h_num = file.Get(num_name)
            h_den = file.Get(den_name)
            
            if h_num and h_den:
                num = full_integral(h_num)
                den = full_integral(h_den)
                
                total_num += num
                total_den += den
                
                # Calculate individual sample efficiency
                if den > 0:
                    eff = num / den
                    err = (eff * (1.0 - eff) / den)**0.5
                    
                    data[sample_name]["x"].append(f_value)
                    data[sample_name]["y"].append(eff)
                    data[sample_name]["ex"].append(0.0)
                    data[sample_name]["ey"].append(err)
                
            file.Close()

        # Calculate combined total efficiency
        if total_den > 0:
            eff_tot = total_num / total_den
            err_tot = (eff_tot * (1.0 - eff_tot) / total_den)**0.5
            
            data["total"]["x"].append(f_value)
            data["total"]["y"].append(eff_tot)
            data["total"]["ex"].append(0.0)
            data["total"]["ey"].append(err_tot)

    # 2. Build the MultiGraph and Legend
    mg = ROOT.TMultiGraph()
    
    leg = ROOT.TLegend(0.58, 0.70, 0.95, 0.87)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.035)

    graphs = [] # Keep references to prevent garbage collection

    # Create the Total Combined Graph
    if len(data["total"]["x"]) > 0:
        gr_tot = ROOT.TGraphErrors(len(data["total"]["x"]), data["total"]["x"], data["total"]["y"], data["total"]["ex"], data["total"]["ey"])
        gr_tot.SetMarkerStyle(20)
        gr_tot.SetMarkerSize(1.2)
        gr_tot.SetMarkerColor(ROOT.kBlack)
        gr_tot.SetLineColor(ROOT.kBlack)
        gr_tot.SetLineWidth(2)
        
        mg.Add(gr_tot)
        leg.AddEntry(gr_tot, "Combined Signal", "pl")
        graphs.append(gr_tot)

    # Create Individual Sample Graphs
    for sample_name, props in signal_samples.items():
        if len(data[sample_name]["x"]) > 0:
            gr = ROOT.TGraphErrors(len(data[sample_name]["x"]), data[sample_name]["x"], data[sample_name]["y"], data[sample_name]["ex"], data[sample_name]["ey"])
            
            color = props["color"]
            gr.SetMarkerStyle(props["marker_style"])
            gr.SetMarkerSize(1.0)
            gr.SetMarkerColor(color)
            gr.SetLineColor(color)
            gr.SetLineWidth(2)
            
            mg.Add(gr)
            leg.AddEntry(gr, props["label"], "pl")
            graphs.append(gr)

    # 3. Plotting
    c_canvas = ROOT.TCanvas("c_canvas", "Optimization Canvas", 800, 600)
    # c_canvas.SetGrid()
    # c_canvas.SetTicks(1, 1)

    # Draw the multigraph (A = Axis, P = Points, E = Error bars)
    mg.Draw("APE")
    
    # Apply titles and limits after drawing (TMultiGraph creates the axes during Draw)
    mg.SetTitle(";Fraction of recoil mass term in #chi^{2} (f parameter);Total Lepton Pairing Efficiency")
    mg.GetYaxis().SetRangeUser(ymin, ymax)
    mg.GetXaxis().SetTitleOffset(1.2)
    mg.GetXaxis().SetLimits(-0.1, 1.1)
    
    leg.Draw()

    # --- NEW BLOCK: Draw values near total signal points ---
    point_text = ROOT.TLatex()
    point_text.SetTextFont(42)
    point_text.SetTextSize(0.02)  # Slightly smaller text
    point_text.SetTextColor(ROOT.kBlack)
    point_text.SetTextAlign(21)    # Center-bottom alignment

    for i in range(len(data["total"]["x"])):
        x_val = data["total"]["x"][i]
        y_val = data["total"]["y"][i]
        
        # Draw the text slightly above the data point (y_val + 0.02)
        # Adjust the 0.02 offset depending on your y-axis scale
        # point_text.DrawLatex(x_val+0.048, y_val-0.005, f"{y_val:.2%}")
        point_text.DrawLatex(x_val+0.048, y_val-0.002, f"{y_val:.2%}")
    # -------------------------------------------------------

    # 4. Standard FCC Text
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)
    latex_y = 0.92
    latex.DrawLatex(0.10, 0.91, "#bf{FCC-ee} IDEA Simulation (Delphes)")
    latex.DrawLatex(0.62, 0.91, f"#sqrt{{s}} = {ecm} GeV, {lumi} ab^{{-1}}")
    latex.DrawLatex(0.15, latex_y-0.10, "e^{+}e^{-} #rightarrow Z(ll)H, H #rightarrow WW* #rightarrow l#nul#nu")
    latex.DrawLatex(0.15, latex_y-0.16, "#chi^{2} = (1-f)(m_{ll}-91)^{2} + f(m_{rec}-125)^{2}")
    latex.DrawLatex(0.15, latex_y-0.22, label)

    # Save
    out_name = os.path.join(output_dir, "pairing_chi2_optimization.pdf")
    c_canvas.SaveAs(out_name)
    print(f"Saved optimization plot to {out_name}")

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    plot_optimization(parse_args())
