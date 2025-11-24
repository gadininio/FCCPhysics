
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # add parent dir
import zh_hww_4l.plots as plotter
import ROOT
import argparse

def load_histogram(file_path, hist_name='cutFlow'):
    file = ROOT.TFile.Open(file_path)
    if not file or file.IsZombie():
        raise RuntimeError(f"Cannot open file: {file_path}")
    hist = file.Get(hist_name)
    if not hist:
        raise RuntimeError(f"Histogram {hist_name} not found in {file_path}")
    hist.SetDirectory(0)  # Detach from file
    file.Close()
    return hist

def combine_signal_histograms(hists, signal_keys):
    combined = hists[signal_keys[0]].Clone("signal_combined")
    for key in signal_keys[1:]:
        combined.Add(hists[key])
    return combined

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Combine cutflows and optionally add percentages.")
parser.add_argument('--add-perc', '-a', action='store_true', help='Add percentage columns to the cutflow table', default=False)
args = parser.parse_args()
add_perc = args.add_perc

# Define processes
procs = {}
procs['signal'] = {'Z(ee)H':'wzp6_ee_eeH_HWW_ecm240', 'Z(mumu)H':'wzp6_ee_mumuH_HWW_ecm240'}
procs['backgrounds'] =  {'WW':'p8_ee_WW_ecm240', 'ZZ':'p8_ee_ZZ_ecm240', 'Z':['wzp6_ee_ee_Mee_30_150_ecm240', 'wzp6_ee_mumu_ecm240']}
signal_combined_name = 'Z(ll)H'

# Extract cutflow configuration
cutflow_cfg = plotter.hists['cutFlow']
proc_list = list(procs['signal'].keys()) + list(procs['backgrounds'].keys())
scaleSig = cutflow_cfg['scaleSig'] if 'scaleSig' in cutflow_cfg else 1.
cuts = cutflow_cfg['xtitle']

# Load histogram from a ROOT file
input = plotter.inputDir.replace('../','')
input = '../../' + input
output = plotter.outdir.replace('../','')
output = '../../' + output

hists = {}
for sample_name in proc_list:
    sample_file = procs['signal'][sample_name] if sample_name in procs['signal'] else procs['backgrounds'][sample_name]
    if(type(sample_file) == list):
        # Combine multiple files for this background
        hists[sample_name] = None
        for sf in sample_file:
            hist = load_histogram(os.path.join(input, f"{sf}.root"))
            if hists[sample_name] is None:
                hists[sample_name] = hist
            else:
                hists[sample_name].Add(hist)
    else:
        hists[sample_name] = load_histogram(os.path.join(input, f"{sample_file}.root"))
    if sample_name in procs['signal'] and scaleSig != 1.:
        hists[sample_name].Scale(1./scaleSig) # undo signal scaling

# Combine signal histograms into one
signal_keys = list(procs['signal'].keys())
hists[signal_combined_name] = combine_signal_histograms(hists, signal_keys)
proc_list = [signal_combined_name] + proc_list

out_orig = sys.stdout
output_path = f"{output.replace('ee', 'll').replace('mumu','ll')}/cutFlow_combined.txt"
with open(output_path, 'w') as f:
    sys.stdout = f
    
    if add_perc:
        formatted_row = '{:<10} {:<26} {:<15} ' + ' '.join(['{:<21}']*len(proc_list))
        print(formatted_row.format(*(["#", "Cut", "Significance"]+proc_list)))
        print(formatted_row.format(*(["----------"]+["--------------------------"]+["---------------"]+["---------------------"]*len(proc_list))))

        tmp = []
        tmp2 = []
        tmp0 = []
        for i,cut in enumerate(cuts):
            
            if cut == 'p_{l_{1}},p_{l_{2}},p_{l_{3}},p_{l_{4}}': cut = 'p_{l}'
            
            s = hists[proc_list[0]].GetBinContent(i+1)
            s_plus_b = sum([hists[p].GetBinContent(i+1) for p in proc_list if p != signal_combined_name])
            significance = s/(s_plus_b**0.5) if s_plus_b > 0 else 0
            row = ["Cut %d"%i, cut, "%.3f"%significance]
            for j,sample_name in enumerate(proc_list):
                yield_ = hists[sample_name].GetBinContent(i+1)
                row.append(f"{yield_:.4e} ({yield_/tmp[j] if j<len(tmp) and tmp[j]>0 else 1.:.1%})")
                tmp2.append(yield_)
            print(formatted_row.format(*row))
            if i==0: tmp0 = tmp2
            tmp = tmp2
            tmp2 = []
        row = ["Total", "", ""]
        row += [f"{tmp[j]/tmp0[j]:.4%}" for j in range(len(tmp0))]
        print('\n'+formatted_row.format(*row))
        
    else:
        formatted_row = '{:<10} {:<30} {:<15} ' + ' '.join(['{:<15}']*len(proc_list))
        print(formatted_row.format(*(["#", "Cut", "Significance"]+proc_list)))
        print(formatted_row.format(*(["----------"]+["--------------------------"]+["-------------"]*(len(proc_list)+1))))
        
        for i,cut in enumerate(cuts):
            s = hists[proc_list[0]].GetBinContent(i+1)
            s_plus_b = sum([hists[p].GetBinContent(i+1) for p in proc_list if p != signal_combined_name])
            significance = s/(s_plus_b**0.5) if s_plus_b > 0 else 0
            row = ["Cut %d"%i, cut, "%.3f"%significance]
            for j,sample_name in enumerate(proc_list):
                yield_ = hists[sample_name].GetBinContent(i+1)
                row.append("%.4e" % (yield_))
            print(formatted_row.format(*row))
            # f.write(formatted_row.format(*row) + '\n')
            
sys.stdout = out_orig
print(f"Cutflow table saved to {output_path}")
