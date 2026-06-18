"""
This script generates comparison plots for the e+e- -> ZH process across multiple selection schemes.
For each variable, it produces 3 plots:
  1. Comparison of all schemes for the inclusive (eeH) distribution.
  2. Comparison of all schemes for the ZH only (mumuH) distribution.
  3. Comparison of all schemes for the VBF + interference distribution.

Run with:
    python plot_VBF_compare.py --ecm 365 --lumi 3.0
"""

import ROOT
import os
import argparse

def generate_comparison_plots(schemes, variables, ecm, lumi):
    # Define distinct colors and marker styles for up to 11+ schemes
    colors = [
        ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, 
        ROOT.kMagenta, ROOT.kCyan+1, ROOT.kOrange+7, 
        ROOT.kYellow+2, ROOT.kAzure+7, ROOT.kViolet+1, ROOT.kSpring-6
    ]
    markers = [20, 21, 22, 23, 24, 25, 26, 32, 28, 29, 30]

    for var, props in variables.items():
        # Dictionaries to store histograms for the current variable
        hists_ee = []
        hists_mumu = []
        hists_vbf = []

        # 1. Load and process all histograms across all schemes
        for i, scheme in enumerate(schemes):
            input_dir = f"../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{scheme}"
            file_ee_path = os.path.join(input_dir, "wzp6_ee_eeH_HWW_ecm365.root")
            file_mumu_path = os.path.join(input_dir, "wzp6_ee_mumuH_HWW_ecm365.root")

            f_ee = ROOT.TFile.Open(file_ee_path, "READ")
            f_mumu = ROOT.TFile.Open(file_mumu_path, "READ")

            if not f_ee or f_ee.IsZombie() or not f_mumu or f_mumu.IsZombie():
                print(f"Error: Could not open ROOT files for scheme {scheme}. Skipping.")
                continue

            h_ee_raw = f_ee.Get(var)
            h_mumu_raw = f_mumu.Get(var)

            if not h_ee_raw or not h_mumu_raw:
                print(f"Warning: Histogram '{var}' not found in scheme '{scheme}'. Skipping.")
                f_ee.Close()
                f_mumu.Close()
                continue

            # Clone and detach from directory to keep in memory after files close
            h_ee = h_ee_raw.Clone(f"{var}_ee_{scheme}")
            h_ee.SetDirectory(0)
            h_mumu = h_mumu_raw.Clone(f"{var}_mumu_{scheme}")
            h_mumu.SetDirectory(0)

            # Rebin
            rebin_factor = props.get("rebin", 1)
            if rebin_factor > 1:
                h_ee.Rebin(rebin_factor)
                h_mumu.Rebin(rebin_factor)

            # Create VBF
            h_vbf = h_ee.Clone(f"{var}_vbf_{scheme}")
            h_vbf.Add(h_mumu, -1)
            h_vbf.SetDirectory(0)

            # Formatting logic for the current scheme
            c_idx = i % len(colors)
            for h in [h_ee, h_mumu, h_vbf]:
                h.SetLineColor(colors[c_idx])
                h.SetMarkerColor(colors[c_idx])
                h.SetMarkerStyle(markers[c_idx])
                h.SetMarkerSize(1.2)
                h.SetLineWidth(2)
                h.SetStats(0)
                h.SetTitle("")

            hists_ee.append((scheme, h_ee))
            hists_mumu.append((scheme, h_mumu))
            hists_vbf.append((scheme, h_vbf))

            f_ee.Close()
            f_mumu.Close()

        # If no histograms were successfully loaded, skip drawing
        if not hists_ee:
            continue

        # 2. Draw the comparison canvases
        distributions = [
            ("Inclusive", hists_ee, "Inclusive (e^{+}e^{-}H)"),
            ("ZH_Only", hists_mumu, "ZH (#mu^{+}#mu^{-}H)"),
            ("VBF", hists_vbf, "VBF + interference (e^{+}e^{-}H - #mu^{+}#mu^{-}H)")
        ]

        for dist_key, dist_hists, dist_title in distributions:
            c = ROOT.TCanvas(f"c_{var}_{dist_key}", f"{var} {dist_key}", 800, 800)
            c.SetLeftMargin(0.15)
            c.SetBottomMargin(0.12)
            c.SetGridx()
            c.SetGridy()
            
            # Use the first histogram as the base to draw axes
            h_base = dist_hists[0][1]
            
            # Apply X-axis ranges if specified
            xmin = props.get("xmin")
            xmax = props.get("xmax")
            if xmin is not None and xmax is not None:
                h_base.GetXaxis().SetRangeUser(xmin, xmax)

            # Find global min and max across all schemes for this distribution
            max_y = max(h.GetMaximum() for _, h in dist_hists)
            min_y = min(h.GetMinimum() for _, h in dist_hists)
            
            # Apply Y-axis ranges specifically for this distribution (Inclusive, ZH_Only, or VBF)
            ymin = None
            ymax = None
            
            if "y_limits" in props and dist_key in props["y_limits"]:
                ymin = props["y_limits"][dist_key].get("ymin")
                ymax = props["y_limits"][dist_key].get("ymax")

            # print(f"Drawing {dist_key} for variable '{var}' with Y-axis limits: ymin={ymin}, ymax={ymax}")

            # Fallback to dynamic scaling if manual limits aren't provided for this specific distribution
            if ymax is not None:
                h_base.SetMaximum(ymax)
            else:
                h_base.SetMaximum(max_y * 1.8) # Default scale to fit legend
            
            if ymin is not None:
                h_base.SetMinimum(ymin)
            else:
                if min_y < 0: 
                    h_base.SetMinimum(min_y * 1.5)
                else:
                    h_base.SetMinimum(0)
                    
            bin_width = h_base.GetXaxis().GetBinWidth(1)
            h_base.GetYaxis().SetTitle(f'Events / {bin_width:g} {"GeV" if "GeV" in props.get("xtitle", var) else ""}')
            h_base.GetXaxis().SetTitle(props.get("xtitle", var))
            h_base.GetYaxis().SetTitleSize(0.045)
            h_base.GetXaxis().SetTitleSize(0.045)

            # Draw histograms
            for idx, (scheme_name, h) in enumerate(dist_hists):
                opt = "HIST PL" if idx == 0 else "HIST PL SAME"
                h.Draw(opt)

            # Add zero line for interference if applicable
            if h_base.GetMinimum() < 0:
                x_min_line = xmin if xmin is not None else h_base.GetXaxis().GetXmin()
                x_max_line = xmax if xmax is not None else h_base.GetXaxis().GetXmax()
                line = ROOT.TLine(x_min_line, 0, x_max_line, 0)
                line.SetLineColor(ROOT.kGray)
                line.SetLineStyle(2)
                line.Draw("SAME")

            # Setup multi-column legend at the top
            leg = ROOT.TLegend(0.18, 0.68, 0.88, 0.88)
            leg.SetNColumns(2)
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)
            leg.SetTextSize(0.025)
            
            for scheme_name, h in dist_hists:
                scheme_name_fixed = "medium3_chi2-0.4" if scheme_name == "medium3" else scheme_name
                leg.AddEntry(h, scheme_name_fixed, "pl")
            leg.Draw()

            # Add LaTeX header
            tex = ROOT.TLatex()
            tex.SetNDC()
            tex.SetTextFont(42)
            tex.SetTextSize(0.03)
            
            tex.DrawLatex(0.15, 0.91, "#bf{FCC-ee} IDEA Simulation (Delphes)")
            tex.DrawLatex(0.62, 0.91, f"#sqrt{{s}} = {ecm} GeV, {lumi} ab^{{-1}}")
            tex.DrawLatex(0.18, 0.63, "e^{+}e^{-} #rightarrow Z(ll)H, H #rightarrow WW* #rightarrow l#nul#nu")
            # tex.DrawLatex(0.18, 0.58, "e^{+}e^{-} #rightarrow Z(ll)H, H #rightarrow WW* #rightarrow l#nul#nu")
            tex.DrawLatex(0.18, 0.58, dist_title)

            # Save
            output_path = os.path.join(base_output_dir, f"Comp_{dist_key}_{var}.pdf")
            c.SaveAs(output_path)
            print(f"Saved: {output_path}")

# --- Execution block ---
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Generate Multi-Scheme VBF Comparison Plots.")
    parser.add_argument("--ecm", "-ecm", type=str, default="365", help="Center-of-mass energy (e.g., 365)")
    parser.add_argument("--lumi", "-lumi", type=str, default="3.0", help="Integrated luminosity (e.g., 3.0)")
    parser.add_argument("--base_scheme", "-scheme", type=str, default="medium3", help="Scheme to store the plots under (e.g., medium3)")
    args = parser.parse_args()

    # Define the list of schemes you want to compare
    SCHEMES_TO_COMPARE = [
        "medium3_chi2-0.0",
        "medium3_chi2-0.1",
        "medium3_chi2-0.2",
        "medium3_chi2-0.3",
        "medium3",
        "medium3_chi2-0.5",
        "medium3_chi2-0.6",
        "medium3_chi2-0.7",
        "medium3_chi2-0.8",
        "medium3_chi2-0.9",
        "medium3_chi2-1.0"
    ]

    VARIABLES_TO_PLOT = {
        "zll_acolinearity_final": {
            "xmin": 0.0, 
            "xmax": 1, 
            "rebin": 50, 
            "xtitle": "cos(#theta_{acol} = #pi-#Delta#theta) [rad]",
            "y_limits": {
                "Inclusive": {"ymin": 0, "ymax": 1},
                "ZH_Only": {"ymin": 0, "ymax": 0.6},
                "VBF": {"ymin": -0.1, "ymax": 0.6}
            }
        },
        "zll_m_final": {
            "xmin": 71, 
            "xmax": 111, 
            "rebin": 1, 
            "xtitle": "m_{ll} [GeV]",
            "y_limits": {
                # "Inclusive": {"ymin": 0, "ymax": 500},
                # "ZH_Only": {"ymin": 0, "ymax": 450},
                "VBF": {"ymin": -3, "ymax": 4.5}
            }
        },
        "zll_recoil_m_final": {
            "xmin": 105.0, 
            "xmax": 230.0, 
            "rebin": 50, 
            "xtitle": "Recoil Mass [GeV]",
            "y_limits": {
                # "Inclusive": {"ymin": 0, "ymax": 500},
                # "ZH_Only": {"ymin": 0, "ymax": 450},
                "VBF": {"ymin": -3, "ymax": 5}
            }
        }
    }

    # Base directory for the outputs
    base_output_dir = f"../../outputs/higgs/zh_hww_4l/histmaker/ecm{args.ecm}/plots/{args.base_scheme}/scheme_comparison/VBF/"
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)

    ROOT.gROOT.SetBatch(True)

    # Run the generator
    generate_comparison_plots(SCHEMES_TO_COMPARE, VARIABLES_TO_PLOT, args.ecm, args.lumi)