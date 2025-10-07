
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # add parent dir
import zh_hww_4l.plotter as plotter
import ROOT

procs = {}
procs['signal'] = {'Z(ee)H':'wzp6_ee_eeH_HWW_ecm240', 'Z(mumu)H':'wzp6_ee_mumuH_HWW_ecm240'}
procs['backgrounds'] =  {'WW':'p8_ee_WW_ecm240', 'ZZ':'p8_ee_ZZ_ecm240'}

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

cutflow_cfg = plotter.hists['cutFlow']
proc_list = list(procs['signal'].keys()) + list(procs['backgrounds'].keys())
scaleSig = cutflow_cfg['scaleSig'] if 'scaleSig' in cutflow_cfg else 1.
cuts = cutflow_cfg['xtitle']

# Load histogram from a ROOT file
hists = {}
for sample_name in proc_list:
    sample_file = procs['signal'][sample_name] if sample_name in procs['signal'] else procs['backgrounds'][sample_name]
    hists[sample_name] = load_histogram(os.path.join('../zh_hww_4l/'+plotter.inputDir, f"{sample_file}.root"))
    if sample_name in procs['signal'] and scaleSig != 1.:
        hists[sample_name].Scale(1./scaleSig) # undo signal scaling

# Combine signal histograms into one
signal_keys = list(procs['signal'].keys())
hists['Z(ll)H'] = combine_signal_histograms(hists, signal_keys)
proc_list = ['Z(ll)H'] + proc_list

out_orig = sys.stdout
with open(f"{'../zh_hww_4l/'+plotter.outdir}/cutFlow_combined.txt", 'w') as f:
    sys.stdout = f
    
    formatted_row = '{:<10} {:<26} {:<15} ' + ' '.join(['{:<15}']*len(proc_list))
    print(formatted_row.format(*(["#", "Cut", "Significance"]+proc_list)))
    print(formatted_row.format(*(["----------"]+["--------------------------"]+["-------------"]*(len(proc_list)+1))))
    for i,cut in enumerate(cuts):
        s = hists[proc_list[0]].GetBinContent(i+1)
        s_plus_b = sum([hists[p].GetBinContent(i+1) for p in proc_list])
        significance = s/(s_plus_b**0.5) if s_plus_b > 0 else 0
        row = ["Cut %d"%i, cut, "%.3f"%significance]
        for j,sample_name in enumerate(proc_list):
            yield_ = hists[sample_name].GetBinContent(i+1)
            row.append("%.4e" % (yield_))

        print(formatted_row.format(*row))
        # f.write(formatted_row.format(*row) + '\n')
sys.stdout = out_orig