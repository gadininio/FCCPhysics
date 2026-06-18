"""
This script generates plots for the VBF contribution in the e+e- -> ZH process by subtracting the mumuH histogram (ZH only) from the eeH histogram (inclusive). The resulting histogram represents the VBF contribution plus any interference effects.

Run with:
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3 --scheme_postfix " (#chi^{2}=0.4)"
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3_chi2-0.0
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3_chi2-0.1
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3_chi2-0.2
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3_chi2-0.3
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3_chi2-0.5
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3_chi2-0.6
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3_chi2-0.7
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3_chi2-0.8
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3_chi2-0.9
    python plot_VBF.py --ecm 365 --lumi 3.0 --scheme medium3_chi2-1.0
"""



import ROOT
import os

def generate_vbf_plots(file_ee_path, file_mumu_path, variables, output_dir, ecm, lumi):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the ROOT files
    f_ee = ROOT.TFile.Open(file_ee_path, "READ")
    f_mumu = ROOT.TFile.Open(file_mumu_path, "READ")

    if not f_ee or f_ee.IsZombie() or not f_mumu or f_mumu.IsZombie():
        print("Error: Could not open ROOT files.")
        return

    # Loop over the dictionary of specified variables
    for var, props in variables.items():
        # Retrieve histograms
        h_ee = f_ee.Get(var)
        h_mumu = f_mumu.Get(var)

        if not h_ee or not h_mumu:
            print(f"Warning: Histogram '{var}' not found in one or both files. Skipping.")
            continue

        # Apply rebinning if specified and > 1
        rebin_factor = props.get("rebin", 1)
        if rebin_factor > 1:
            h_ee.Rebin(rebin_factor)
            h_mumu.Rebin(rebin_factor)

        # Create the subtraction histogram: eeH - mumuH
        h_vbf = h_ee.Clone(f"{var}_vbf")
        h_vbf.Add(h_mumu, -1)

        # Set up the canvas
        c = ROOT.TCanvas(f"c_{var}", f"Canvas for {var}", 800, 800)
        c.SetLeftMargin(0.15)
        c.SetBottomMargin(0.12)

        # Apply x-axis range if specified
        xmin = props.get("xmin")
        xmax = props.get("xmax")
        if xmin is not None and xmax is not None:
            h_ee.GetXaxis().SetRangeUser(xmin, xmax)
            h_mumu.GetXaxis().SetRangeUser(xmin, xmax)
            h_vbf.GetXaxis().SetRangeUser(xmin, xmax)

        # Formatting: eeH (Inclusive)
        h_ee.SetStats(0)
        h_ee.SetTitle("")
        bin_width = h_ee.GetXaxis().GetBinWidth(1)
        h_ee.GetYaxis().SetTitle(f'Events / {bin_width:g} {"GeV" if "GeV" in props.get("xtitle", var) else ""}')
        h_ee.GetXaxis().SetTitle(props.get("xtitle", var)) # Use custom title from dict
        h_ee.GetYaxis().SetTitleSize(0.045)
        h_ee.GetXaxis().SetTitleSize(0.045)
        h_ee.SetMarkerStyle(20)
        h_ee.SetMarkerSize(1.2)
        h_ee.SetMarkerColor(ROOT.kBlack)
        h_ee.SetLineColor(ROOT.kBlack)
        h_ee.SetLineWidth(2)
            
        # Formatting: mumuH (ZH only)
        h_mumu.SetMarkerStyle(21)
        h_mumu.SetMarkerSize(1.2)
        h_mumu.SetMarkerColor(ROOT.kRed)
        h_mumu.SetLineColor(ROOT.kRed)
        h_mumu.SetLineWidth(2)

        # Formatting: Subtracted (VBF + interference)
        h_vbf.SetMarkerStyle(22)
        h_vbf.SetMarkerSize(1.2)
        h_vbf.SetMarkerColor(ROOT.kBlue)
        h_vbf.SetLineColor(ROOT.kBlue)
        h_vbf.SetLineWidth(2)

        # Calculate maximum Y to scale the axis properly
        # Note: If RangeUser restricts the view, GetMaximum() still checks all bins. 
        # For precision, you might want to calculate the max within the specific range.
        max_y = max(h_ee.GetMaximum(), h_mumu.GetMaximum(), h_vbf.GetMaximum())
        min_y = min(h_ee.GetMinimum(), h_mumu.GetMinimum(), h_vbf.GetMinimum()) 
        h_ee.SetMaximum(max_y * 1.7)
        if min_y < 0: h_ee.SetMinimum(min_y * 2)

        # Draw histograms (Added "P" so your marker settings render correctly alongside the lines)
        h_ee.Draw("HIST PL")
        h_mumu.Draw("HIST PL SAME")
        h_vbf.Draw("HIST PL SAME")

        # Add a zero line if there is negative interference
        if min_y < 0:
            # Use plot limits to draw the zero line accurately within the zoomed range
            x_min_line = xmin if xmin is not None else h_ee.GetXaxis().GetXmin()
            x_max_line = xmax if xmax is not None else h_ee.GetXaxis().GetXmax()
            line = ROOT.TLine(x_min_line, 0, x_max_line, 0)
            line.SetLineColor(ROOT.kGray)
            line.SetLineStyle(1)
            line.Draw("SAME")

        # Construct the Legend
        leg = ROOT.TLegend(0.18, 0.78, 0.5, 0.65)  # coordinates: (X1, Y1, X2, Y2)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.03)
        leg.AddEntry(h_ee, "Inclusive (e^{+}e^{-}H)", "pl")
        # leg.AddEntry(h_ee, "ZH + ZZ VBF + interference (e^{+}e^{-}H)", "pl")
        leg.AddEntry(h_mumu, "ZH (#mu^{+}#mu^{-}H)", "pl")
        leg.AddEntry(h_vbf, "VBF + interference (e^{+}e^{-}H - #mu^{+}#mu^{-}H)", "pl")
        leg.Draw()

        # Add latex texts
        tex = ROOT.TLatex()
        tex.SetNDC()
        tex.SetTextFont(42)
        tex.SetTextSize(0.03)
        
        latex_y = 0.9
        latex_x = 0.18
        tex.DrawLatex(0.15, 0.91, "#bf{FCC-ee} IDEA Simulation (Delphes)")
        tex.DrawLatex(0.62, 0.91, f"#sqrt{{s}} = {ecm} GeV, {lumi} ab^{{-1}}")
        # tex.DrawLatex(latex_x, latex_y-0.05, f"#sqrt{{s}} = {ecm} GeV, L = {lumi} ab^{{-1}}")
        # tex.DrawLatex(latex_x, latex_y-0.05, "e^{+}e^{-} #rightarrow Z(ll) H#left[W(l#nu)W(l#nu)#right]")
        tex.DrawLatex(latex_x, latex_y-0.05, "e^{+}e^{-} #rightarrow Z(ll)H, H #rightarrow WW* #rightarrow l#nul#nu")
        tex.DrawLatex(latex_x, latex_y-0.10, f"Selections: {scheme}{scheme_postfix}")

        # add grid lines
        c.SetGridx()
        c.SetGridy()

        # Save the plot
        output_path = os.path.join(output_dir, f"VBF_{var}.pdf")
        c.SaveAs(output_path)
        print(f"Saved: {output_path}")

    # Clean up
    f_ee.Close()
    f_mumu.Close()

# --- Execution block ---
if __name__ == "__main__":
    
    # get input arguments from user
    import argparse
    parser = argparse.ArgumentParser(description="Generate VBF plots from ROOT files.")
    parser.add_argument("--ecm", "-ecm", type=str, default="365", help="Center-of-mass energy (e.g., 365)")
    parser.add_argument("--lumi", "-lumi", type=str, default="3.0", help="Integrated luminosity (e.g., 3.0)")
    parser.add_argument("--scheme", "-scheme", type=str, default="medium3", help="Selection scheme (e.g., medium3)")
    parser.add_argument("--scheme_postfix", "-scheme_postfix", type=str, default="", help="chi2 parameter value (e.g., #chi2=0.4)")

    args = parser.parse_args()
    
    # Dictionary of variables with properties: xmin, xmax, rebin, xtitle
    VARIABLES_TO_PLOT = {
        "zll_acolinearity_final": {
            "xmin": 0.0, 
            "xmax": 1, 
            "rebin": 50, 
            "xtitle": "cos(#theta_{acol} = #pi-#Delta#theta) [rad]"
        },
        "zll_m_final": {
            "xmin": 71, 
            "xmax": 111, 
            "rebin": 1, 
            "xtitle": "m_{ll} [GeV]"
        },
        "zll_recoil_m_final": {
            "xmin": 105.0, 
            "xmax": 230.0, 
            "rebin": 50, 
            "xtitle": "Recoil Mass [GeV]"
        }
    }
    
    ecm = args.ecm
    lumi = args.lumi
    scheme = args.scheme
    scheme_postfix = args.scheme_postfix
    
    INPUT_DIRECTORY = f"../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{scheme}"
    FILE_EE = os.path.join(INPUT_DIRECTORY, "wzp6_ee_eeH_HWW_ecm365.root")
    FILE_MUMU = os.path.join(INPUT_DIRECTORY, "wzp6_ee_mumuH_HWW_ecm365.root")
    OUTPUT_DIRECTORY = f"../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/{scheme}/VBF/"

    ROOT.gROOT.SetBatch(True)

    # Run the generator
    generate_vbf_plots(FILE_EE, FILE_MUMU, VARIABLES_TO_PLOT, OUTPUT_DIRECTORY, ecm, lumi)