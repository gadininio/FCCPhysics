"""
This script generates comparison plots for the e+e- -> ZH process across multiple selection schemes.
For each variable, it produces 3 plots:
  1. Comparison of all schemes for the inclusive (eeH) distribution.
  2. Comparison of all schemes for the ZH only (mumuH) distribution.
  3. Comparison of all schemes for the VBF + interference distribution.

Run with:
    python3 plot_VBF_compare_schemes.py -ecm 365 -s medium3 -l "Medium3 selections"
"""

import ROOT
import os
import argparse

def generate_comparison_plots(schemes, variables, ecm, lumi, label=''):
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
        for i, scheme_dict in enumerate(schemes):
            scheme = scheme_dict['scheme']
            input_dir = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{scheme}"
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

            # Create VBF first so the un-rebinned axes match perfectly
            h_vbf = h_ee.Clone(f"{var}_vbf_{scheme}")
            h_vbf.Add(h_mumu, -1)
            h_vbf.SetDirectory(0)

            # Rebin logic
            rebin_prop = props.get("rebin", 1)
            if isinstance(rebin_prop, dict):
                rebin_ee = rebin_prop.get("Inclusive", 1)
                rebin_mumu = rebin_prop.get("ZH_Only", 1)
                rebin_vbf = rebin_prop.get("VBF", 1)
            else:
                rebin_ee = rebin_mumu = rebin_vbf = rebin_prop

            # Apply rebinning separately
            if rebin_ee > 1: 
                h_ee.Rebin(rebin_ee)
            if rebin_mumu > 1: 
                h_mumu.Rebin(rebin_mumu)
            if rebin_vbf > 1: 
                h_vbf.Rebin(rebin_vbf)

            # Formatting logic for the current scheme
            c_idx = i % len(colors)
            for h in [h_ee, h_mumu, h_vbf]:
                h.SetLineColor(colors[c_idx])
                # h.SetMarkerColor(colors[c_idx])
                # h.SetMarkerStyle(markers[c_idx])
                # h.SetMarkerSize(1.2)
                h.SetLineWidth(line_width)
                h.SetStats(0)
                h.SetTitle("")

            hists_ee.append((scheme, h_ee, scheme_dict['label']))
            hists_mumu.append((scheme, h_mumu, scheme_dict['label']))
            hists_vbf.append((scheme, h_vbf, scheme_dict['label']))

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
            max_y = max(h.GetMaximum() for _, h, _ in dist_hists)
            min_y = min(h.GetMinimum() for _, h, _ in dist_hists)
            
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
                y_scale = 1+0.2+(0.2 if label != '' else 0)+0.005*len(dist_hists)  # Scale based on number of schemes to avoid legend overlap
                h_base.SetMaximum(max_y * y_scale) # Default scale to fit legend
            
            if ymin is not None:
                h_base.SetMinimum(ymin)
            else:
                if min_y < 0: 
                    h_base.SetMinimum(min_y * 1.5)
                else:
                    h_base.SetMinimum(0)
                    
            bin_width = h_base.GetXaxis().GetBinWidth(1)
                
            unit = ""
            if "GeV" in props.get("xtitle", var):
                unit = " GeV"
            if "GeV^{2}" in props.get("xtitle", var):
                unit = " GeV^{2}"            
            
            h_base.GetYaxis().SetTitle(f'Events / {bin_width:g}{unit}')
            h_base.GetXaxis().SetTitle(props.get("xtitle", var))
            h_base.GetYaxis().SetTitleSize(0.045)
            h_base.GetXaxis().SetTitleSize(0.045)

            # Draw histograms
            for idx, (scheme_name, h, scheme_label) in enumerate(dist_hists):
                # opt = "HIST PL" if idx == 0 else "HIST PL SAME"
                opt = "HIST" if idx == 0 else "HIST SAME"
                h.Draw(opt)

            # Add zero line for interference if applicable
            if h_base.GetMinimum() < 0:
                x_min_line = xmin if xmin is not None else h_base.GetXaxis().GetXmin()
                x_max_line = xmax if xmax is not None else h_base.GetXaxis().GetXmax()
                line = ROOT.TLine(x_min_line, 0, x_max_line, 0)
                line.SetLineColor(ROOT.kGray)
                # line.SetLineStyle(2)
                line.SetLineWidth(2)
                line.Draw("SAME")

            # Draw histograms again to ensure they are on top of the zero line
            for idx, (scheme_name, h, scheme_label) in enumerate(dist_hists):
                h.Draw("HIST SAME")

            # Add LaTeX header
            tex = ROOT.TLatex()
            tex.SetNDC()
            tex.SetTextFont(42)
            tex.SetTextSize(0.03)

            latex_y = 0.9
            latex_x = 0.18
            tex.DrawLatex(0.15, 0.91, "#bf{FCC-ee} IDEA Simulation (Delphes)")
            tex.DrawLatex(0.62, 0.91, f"#sqrt{{s}} = {ecm} GeV, {lumi} ab^{{-1}}")
            tex.DrawLatex(latex_x, latex_y-0.05, "e^{+}e^{-} #rightarrow Z(ll)H, H #rightarrow WW* #rightarrow l#nul#nu")
            if label == '':
                tex.DrawLatex(latex_x, latex_y-0.10, dist_title)
            else:
                tex.DrawLatex(latex_x, latex_y-0.10, "#chi^{2} = (1-f)(m_{ll}-91)^{2} + f(m_{rec}-125)^{2}")
                tex.DrawLatex(latex_x, latex_y-0.15, label)
                tex.DrawLatex(latex_x, latex_y-0.20, dist_title)

            # Setup multi-column legend at the top
            # leg = ROOT.TLegend(0.18, 0.68, 0.88, 0.88)
            # leg.SetNColumns(2)
            # leg = ROOT.TLegend(0.6, latex_y-0.02, 0.88, latex_y-0.02-0.04*len(dist_hists))
            leg = ROOT.TLegend(0.65, latex_y-0.02, 0.88, latex_y-0.02-0.04*len(dist_hists))
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)
            leg.SetTextSize(0.025)
            
            for scheme_name, h, scheme_label in dist_hists:
                if scheme_label:
                    scheme_name_fixed = scheme_label
                else:
                    scheme_name_fixed = f"{scheme_name}_chi2-0.4" if scheme_name == base_scheme else scheme_name
                leg.AddEntry(h, scheme_name_fixed, "l")  # pl
            leg.Draw()
            
            # Save
            output_path = os.path.join(base_output_dir, f"Comp_{dist_key}_{var}.pdf")
            c.SaveAs(output_path)
            print(f"Saved: {output_path}")

# --- Execution block ---
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Generate Multi-Scheme VBF Comparison Plots.")
    parser.add_argument("--ecm", "-ecm", type=str, default="365", help="Center-of-mass energy (e.g., 365)")
    parser.add_argument("--base_scheme", "-s", type=str, default="medium3", help="Scheme to store the plots under (e.g., medium3)")
    parser.add_argument("--label", "-l", type=str, default="medium3", help="Scheme to store the plots under (e.g., medium3)")
    parser.add_argument("--line_width", "-lw", type=int, default=2, help="")
    args = parser.parse_args()

    ecm = args.ecm  # Center-of-mass energy
    lumi = 10.8 if ecm == "240" else 3.0  # Default luminosity based on ecm
    line_width = args.line_width  # Line width for histograms
    base_scheme = args.base_scheme  # Base scheme for comparison
    label = args.label  # Label for the plots
    
    # Define the list of schemes you want to compare
    SCHEMES_TO_COMPARE = [
        # {'scheme': f"{base_scheme}_chi2-0.0", 'label': 'f = 0.0'},
        # {'scheme': f"{base_scheme}_chi2-0.1", 'label': 'f = 0.1'},
        # {'scheme': f"{base_scheme}_chi2-0.2", 'label': 'f = 0.2'},
        # {'scheme': f"{base_scheme}_chi2-0.3", 'label': 'f = 0.3'},
        {'scheme': f"{base_scheme}",          'label': 'f = 0.4'},
        # {'scheme': f"{base_scheme}_chi2-0.5", 'label': 'f = 0.5'},
        # {'scheme': f"{base_scheme}_chi2-0.6", 'label': 'f = 0.6'},
        # {'scheme': f"{base_scheme}_chi2-0.7", 'label': 'f = 0.7'},
        # {'scheme': f"{base_scheme}_chi2-0.8", 'label': 'f = 0.8'},
        # {'scheme': f"{base_scheme}_chi2-0.9", 'label': 'f = 0.9'},
        {'scheme': f"{base_scheme}_chi2-1.0", 'label': 'f = 1.0'},
    ]

    VARIABLES_TO_PLOT = {
        "zll_acolinearity_cut4": {
            "xmin": 0.0, 
            "xmax": 1, 
            "rebin": 50, 
            "xtitle": "cos(#theta_{acol} = #pi-#Delta#theta) (before cut) [rad]",
            "y_limits": {
                # "Inclusive": {"ymin": 0, "ymax": 1},
                # "ZH_Only": {"ymin": 0, "ymax": 0.6},
                # "VBF": {"ymin": -0.1, "ymax": 0.6}
            }
        },
        "zll_acolinearity_final": {
            "xmin": 0.0, 
            "xmax": 1, 
            "rebin": 50, 
            "xtitle": "cos(#theta_{acol} = #pi-#Delta#theta) [rad]",
            "y_limits": {
                # "Inclusive": {"ymin": 0, "ymax": 1},
                # "ZH_Only": {"ymin": 0, "ymax": 0.6},
                # "VBF": {"ymin": -0.1, "ymax": 0.6}
            }
        },
        "zll_m_cut4": {
            "xmin": 0, 
            "xmax": 250, 
            "rebin": {
                "Inclusive": 5,
                "ZH_Only": 5,
                "VBF": 10
            },
            "xtitle": "m_{ll} (before cut) [GeV]",
            "y_limits": {
                # "Inclusive": {"ymin": 0, "ymax": 500},
                # "ZH_Only": {"ymin": 0, "ymax": 450},
                "VBF": {"ymin": -5, "ymax": 13}
            }
        },
        "zll_m_final": {
            "xmin": 71, 
            "xmax": 111, 
            "rebin": {
                "Inclusive": 2,
                "ZH_Only": 2,
                "VBF": 10
            },            "xtitle": "m_{ll} [GeV]",
            "y_limits": {
                # "Inclusive": {"ymin": 0, "ymax": 500},
                # "ZH_Only": {"ymin": 0, "ymax": 450},
                "VBF": {"ymin": -5, "ymax": 9}
            }
        },
        "zll_recoil_m_cut4": {
            "xmin": 50, 
            "xmax": 350, 
            "rebin": 10, 
            "xtitle": "Recoil (before cut) [GeV]",
            "y_limits": {
                # "Inclusive": {"ymin": 0, "ymax": 500},
                # "ZH_Only": {"ymin": 0, "ymax": 450},
                # "VBF": {"ymin": -3, "ymax": 5}
            }
        },
        "zll_recoil_m_final": {
            "xmin": 100, 
            "xmax": 240, 
            "rebin": {
                "Inclusive": 50,
                "ZH_Only": 50,
                "VBF": 100
            },
            "xtitle": "Recoil [GeV]",
            "y_limits": {
                # "Inclusive": {"ymin": 0, "ymax": 500},
                # "ZH_Only": {"ymin": 0, "ymax": 450},
                "VBF": {"ymin": -6, "ymax": 6}
            }
        }
    }

    # Base directory for the outputs
    base_output_dir = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{base_scheme}/scheme_comparison/VBF/"
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)

    ROOT.gROOT.SetBatch(True)

    # Run the generator
    generate_comparison_plots(SCHEMES_TO_COMPARE, VARIABLES_TO_PLOT, ecm, lumi, label)