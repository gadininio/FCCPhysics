'''
This script combines cutflow histograms from multiple signal and background samples, calculates the significance at each cut step, and outputs a formatted cutflow table. It can also export the table in LaTeX format.

Run with:

    python3 run_cutflow.py \
        -cfg ./config_ecm240.json \
        -i ./my_input_dir \
        -o ./my_output_dir \
        --latex
'''


import os, sys
import ROOT
import argparse
import math
import json


def load_histogram(file_path, hist_name='cutFlow'):
    # check if file exists
    if not os.path.isfile(file_path):
        raise RuntimeError(f"File not found: {file_path}")
        # print(f"File not found: {file_path}")
        # return None
    
    file = ROOT.TFile.Open(file_path)
    if not file or file.IsZombie():
        raise RuntimeError(f"Cannot open file: {file_path}")
        # print(f"Cannot open file: {file_path}")
        # return None
    
    hist = file.Get(hist_name)
    if not hist:
        raise RuntimeError(f"Histogram {hist_name} not found in {file_path}")
        # print(f"Histogram {hist_name} not found in {file_path}")
        # return None
    
    hist.SetDirectory(0)  # Detach from file
    file.Close()
    return hist


def combine_histograms(hists, hist_keys, combined_name='signal_combined'):
    combined = hists[hist_keys[0]].Clone(combined_name)
    for key in hist_keys[1:]:
        combined.Add(hists[key])
    return combined


def fix_cut_name(cut):
    return cut.replace('{','').replace('}','').replace('#geq','≥').replace('#leq','≤').replace('#Delta','Δ').replace('#theta','θ').replace('#phi','φ').replace('#eta','η').replace('#gamma','γ').replace('#tau','τ').replace('#mu','μ').replace('^+','').replace('^-','')


def to_latex_row(row_list):
    """Helper function to escape LaTeX special characters and format a row."""
    def escape(s):
        s = str(s)
        s = s.replace('\\', r'\textbackslash{}').replace('&', r'\&').replace('%', r'\%').replace('_', r'\_').replace('#', r'\#')
        math_map = {
            '≥': r'$\geq$', '≤': r'$\leq$', 'Δ': r'$\Delta$', 
            'θ': r'$\theta$', 'φ': r'$\phi$', 'η': r'$\eta$', 
            'γ': r'$\gamma$', 'τ': r'$\tau$', 'μ': r'$\mu$'
        }
        for k, v in math_map.items():
            s = s.replace(k, v)
        return s
    return " & ".join([escape(x) for x in row_list]) + " \\\\"


# ---------------------------------------------------------
# Parse command-line arguments
# ---------------------------------------------------------
parser = argparse.ArgumentParser(description="Combine cutflows using a JSON configuration.")
parser.add_argument('--config', '-cfg', type=str, required=True, help='Path to the JSON config file')
parser.add_argument('--inputDir', '-i', type=str, required=True, help='Path to the input directory')
parser.add_argument('--outDir', '-o', type=str, required=True, help='Path to the output directory')
parser.add_argument('--cuts', '-c', type=str, nargs='+', help='List of cuts (overrides JSON config)')
parser.add_argument('--simple', '-s', action='store_true', help='Do not add percentage columns', default=False)
parser.add_argument('--latex', '-l', action='store_true', help='Export to LaTeX (.tex)', default=False)
parser.add_argument('--asimov', '-as', action='store_true', help='Use Asimov significance', default=False)

args = parser.parse_args()


# ---------------------------------------------------------
# Load JSON Configuration
# ---------------------------------------------------------
with open(args.config, 'r') as f:
    config = json.load(f)

procs = config.get('processes', {})
if 'signal' not in procs or 'backgrounds' not in procs:
    raise ValueError("JSON must contain 'processes' with 'signal' and 'backgrounds' definitions.")

signal_combined_name = config.get('signal_combined_name', 'Signal')
scaleSig = config.get('scaleSig', 1.0)
cuts = args.cuts if args.cuts else config.get('cuts', [])

if not cuts:
    raise ValueError("Cuts must be provided either via --cuts argument or in the JSON config.")

add_perc = not args.simple
export_latex = args.latex
asimov = args.asimov
proc_list = list(procs['signal'].keys()) + list(procs['backgrounds'].keys())


# ---------------------------------------------------------
# Directory setup
# ---------------------------------------------------------
input_dir = args.inputDir.replace('../','')
input_dir = '../../' + input_dir
if input_dir.endswith('/'): input_dir = input_dir[:-1]

output_dir = args.outDir.replace('../','')
output_dir = '../../' + output_dir

print(f"Loading configuration from {args.config}")
print(f"Loading histograms from {input_dir}...")


# ---------------------------------------------------------
# Load and process Histograms
# ---------------------------------------------------------
hists = {}
for sample_name in proc_list:
    sample_file = procs['signal'].get(sample_name) or procs['backgrounds'].get(sample_name)
    
    if type(sample_file) == list:
        hists[sample_name] = None
        for sf in sample_file:
            hist = load_histogram(os.path.join(input_dir, f"{sf}.root"))
            # if hist is None:
            #     print(f"Warning: Histogram for {sf} is missing. Skipping this file.")
            #     continue
            if hists[sample_name] is None:
                hists[sample_name] = hist
            else:
                hists[sample_name].Add(hist)
    else:
        hists[sample_name] = load_histogram(os.path.join(input_dir, f"{sample_file}.root"))
        
    if sample_name in procs['signal'] and scaleSig != 1.0:
        hists[sample_name].Scale(1.0 / scaleSig) 

# Combine signal histograms into one
signal_keys = list(procs['signal'].keys())
hists[signal_combined_name] = combine_histograms(hists, signal_keys, combined_name='combined_signal')
proc_list = [signal_combined_name] + proc_list

# Combine background histograms into one for total background
background_keys = list(procs['backgrounds'].keys())
h_tot_bkg = combine_histograms(hists, background_keys, combined_name='total_bkg')


# ---------------------------------------------------------
# Formatting and Output
# ---------------------------------------------------------
out_orig = sys.stdout
output_path_dir = output_dir.replace('ee', 'll').replace('mumu','ll')
os.makedirs(output_path_dir, exist_ok=True)
output_path = f"{output_path_dir}/cutFlow_combined.txt"

# LaTeX Initialization
latex_file = None
if export_latex:
    latex_path = f"{output_path_dir}/cutFlow_combined.tex"
    latex_file = open(latex_path, 'w')
    latex_file.write("\\begin{table}[htbp]\n\\centering\n\\resizebox{\\textwidth}{!}{\n")
    latex_file.write("\\begin{tabular}{|l|l|l|" + "r|" * len(proc_list) + "}\n\\hline\n")

with open(output_path, 'w') as f:
    sys.stdout = f
    headers = ["#", "Cut", "Significance"] + proc_list
    
    if add_perc:
        formatted_row = '{:<10} {:<31} {:<15} ' + ' '.join(['{:<21}']*len(proc_list))
        print(formatted_row.format(*headers))
        print(formatted_row.format(*(["----------"]+["-------------------------------"]+["---------------"]+["---------------------"]*len(proc_list))))
        if export_latex: latex_file.write(to_latex_row(headers) + "\n\\hline\n")

        tmp = []
        tmp2 = []
        tmp0 = []
        for i, cut in enumerate(cuts):
            cut = fix_cut_name(cut)
            s = hists[proc_list[0]].GetBinContent(i+1)
            s_plus_b = sum([hists[p].GetBinContent(i+1) for p in proc_list if p != signal_combined_name])
            b = h_tot_bkg.GetBinContent(i+1)
            
            significance = math.sqrt( 2*((s+b)*math.log(1+s/b) - s) ) if (asimov and b > 0) else (s/(s_plus_b**0.5) if s_plus_b > 0 else 0)
            
            row = [f"Cut {i}", cut, f"{significance:.3f}"]
            for j, sample_name in enumerate(proc_list):
                yield_ = hists[sample_name].GetBinContent(i+1)
                row.append(f"{yield_:.4e} ({yield_/tmp[j] if j<len(tmp) and tmp[j]>0 else 1.:.1%})")
                tmp2.append(yield_)
            
            print(formatted_row.format(*row))
            if export_latex: latex_file.write(to_latex_row(row) + "\n")
                
            if i==0: tmp0 = tmp2
            tmp = tmp2
            tmp2 = []
            
        total_row = ["Total", "", ""]
        total_row += [f"{tmp[j]/tmp0[j]:.4%}" if tmp0[j] > 0 else "0.00%" for j in range(len(tmp0))]
        print('\n'+formatted_row.format(*total_row))
        if export_latex: latex_file.write("\\hline\n" + to_latex_row(total_row) + "\n")
        
    else:
        formatted_row = '{:<10} {:<30} {:<15} ' + ' '.join(['{:<15}']*len(proc_list))
        print(formatted_row.format(*headers))
        print(formatted_row.format(*(["----------"]+["--------------------------"]+["-------------"]*(len(proc_list)+1))))
        if export_latex: latex_file.write(to_latex_row(headers) + "\n\\hline\n")
        
        for i, cut in enumerate(cuts):
            cut = fix_cut_name(cut)
            s = hists[proc_list[0]].GetBinContent(i+1)
            s_plus_b = sum([hists[p].GetBinContent(i+1) for p in proc_list if p != signal_combined_name])
            b = h_tot_bkg.GetBinContent(i+1)
            
            significance = math.sqrt( 2*((s+b)*math.log(1+s/b) - s) ) if (asimov and b > 0) else (s/(s_plus_b**0.5) if s_plus_b > 0 else 0)
            
            row = [f"Cut {i}", cut, f"{significance:.3f}"]
            for j, sample_name in enumerate(proc_list):
                yield_ = hists[sample_name].GetBinContent(i+1)
                row.append("%.4e" % (yield_))
                
            print(formatted_row.format(*row))
            if export_latex: latex_file.write(to_latex_row(row) + "\n")

if export_latex:
    latex_file.write("\\hline\n\\end{tabular}\n}\n\\end{table}\n")
    latex_file.close()

sys.stdout = out_orig
print(f"Significance formula used: {'Asimov formula' if asimov else 'S/sqrt(S+B)'}")
print(f"Cutflow table saved to {output_path}")
if export_latex:
    print(f"LaTeX table saved to {latex_path}")