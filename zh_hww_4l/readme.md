
# $Z(\ell\ell)H, H \to WW^* \to \ell\nu\ell\nu$ feasibility study for FCC-ee 

## Cut-based analysis - commands

### Run histmaker

Run histmaker to create root files with histograms:

1. for 240 GeV:

    Preselections only:
    ```
    ecm=240 sel_type=0 fccanalysis run histmaker.py
    ```

    Loose selections:
    ```
    ecm=240 sel_type=1 fullrun=true fccanalysis run histmaker.py
    ```

    Training samples: add `training=true`
    

2. for 365 GeV:

    Preselections only:
    ```
    ecm=365 sel_type=0 fccanalysis run histmaker.py
    ```

    Medium selections (required for lepton isolation distributions before selections):
    ```
    ecm=365 sel_type=5 fullrun=true fccanalysis run histmaker.py
    ```

    Medium selections with lepton isolation cut (iso < 3) and f=1.0 in chi2 function:
    ```
    ecm=365 sel_type=5 chi2=1.0 iso=3 fullrun=true fccanalysis run histmaker.py
    ```

    Training samples: add `training=true`


### Run plotter

Run plotter to procude pdf files combining all samples:

1. for 240 GeV:
    ```
    fccanalysis plots plots.py
    ```

2. for 365 GeV:
    ```
    scheme=medium3_full_chi2-1.0_iso-3.0_20260813_081619 inclWW=true iso=true fccanalysis plots plots_ecm365.py
    ```


### Run cutflow

1. for 240 GeV:

    ```
    python3 detailed_cutflow.py \
        -cfg ../cutflow_cng/config_240_loose_allbkg.json \
        -i ../../outputs/higgs/zh_hww_4l/histmaker/ecm240/hists/full_loose_20260126_112336/ \
        -o ../../outputs/higgs/zh_hww_4l/histmaker/ecm240/plots/full_loose_20260126_112336/ll/ \
        --latex
    ```

2. for 365 GeV:

    ```
    python3 detailed_cutflow.py \
        -cfg ../cutflow_cng/config_365_medium3_inclWWInFit_iso.json \
        -i ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium3_full_chi2-1.0_iso-3.0_20260813_081619/ \
        -o ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/plots/medium3_full_chi2-1.0_iso-3.0_20260813_081619/ll/ \
        --latex
    ```


### Cut optimization

Find window with best significance:

    python simple_cut_optim.py \
        --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium3_chi2-1.0' \
        --ecm 365 \
        --variables zll_m_cut4

Get efficiencies per sample for given window:

    python simple_cut_optim.py \
        --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso' \
        --ecm 365 \
        --variables lep3_iso_log_final -r 100 -xmin -15 -xmax -1


### Get efficiency/total yield

for 365 GeV, zll_m_cut4

    python3 analyze_hists.py \
        /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium3_chi2-1.0/wzp6_ee_eeH_HWW_ecm365.root \
        -n zll_m_cut4 --xmin 51 --xmax 131


### Run fit

1. Prepare the Combine-compatible datacards:

    ```
    ecm=365 scheme=tight_norecoil fccanalysis combine combine.py
    ```

2. To perform the likelihood fit using the CMS Combine tool inside a Singularity container, run:

    ```
    cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm240/combine/full
    ```

    ```
    cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm365/combine/tight_norecoil
    singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm365/combine/tight_norecoil; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'
    ```






## MVA analysis - commands

Run in the following order:

1. Create ntuples with preselected events (`preselection.py`)

    for 240 GeV:
        - For training samples:
            run=full ecm=240 training=True sel_type=loose fccanalysis run preselection.py
        - For standard samples:
            run=full ecm=240 training=False sel_type=loose fccanalysis run preselection.py

    for 365 GeV:
        - For training samples:
            run=full ecm=365 training=True  sel_type=medium chi2=1.0 iso=3.0 fccanalysis run preselection.py
        - For standard samples:
            run=full ecm=365 training=False sel_type=medium chi2=1.0 iso=3.0 fccanalysis run preselection.py


2. Add the parameters to the output root files (utils/`add_parameters_to_root.py`)

    for 240 GeV:

        - for the analysis samples:

            python3 ../utils/add_parameters_to_root.py \
                -f ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection \
                -n dataset sel_type chi2 lepton_iso \
                -t string string float float \
                -v winter2023_IDEA loose 0.4 -999

        - for the training samples:

            python3 ../utils/add_parameters_to_root.py \
                -f ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection/training \
                -n dataset sel_type chi2 lepton_iso \
                -t string string float float \
                -v winter2023_training_IDEA loose 0.4 -999

    for 365 GeV:

        - for the analysis samples:

            python3 ../utils/add_parameters_to_root.py \
                -f ../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection \
                -n dataset sel_type chi2 lepton_iso \
                -t string string float float \
                -v winter2023_IDEA medium 1.0 3

        - for the training samples:

            python3 ../utils/add_parameters_to_root.py \
                -f ../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection/training \
                -n dataset sel_type chi2 lepton_iso \
                -t string string float float \
                -v winter2023_training_IDEA medium 1.0 3


3. Apply the ww_leptonic cut on signal samples (utils/skim.C)

    - Rename the signal output root files (training and standard samples):
        mv wzp6_ee_eeH_HWW_llnunu_ecm240.root wzp6_ee_eeH_HWW_llnunu_ecm240_inc.root
        mv wzp6_ee_mumuH_HWW_llnunu_ecm240.root wzp6_ee_mumuH_HWW_llnunu_ecm240_inc.root
        mv wzp6_ee_eeH_HWW_ecm240.root wzp6_ee_eeH_HWW_ecm240_inc.root
        mv wzp6_ee_mumuH_HWW_ecm240.root wzp6_ee_mumuH_HWW_ecm240_inc.root

    - Run the skimmer to keep only true leptonic-WW signal events:

        for 240 GeV:

            root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection/wzp6_ee_eeH_HWW_llnunu_ecm240_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection/wzp6_ee_eeH_HWW_llnunu_ecm240.root")'
            root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection/wzp6_ee_mumuH_HWW_llnunu_ecm240_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection/wzp6_ee_mumuH_HWW_llnunu_ecm240.root")'
            root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection/training/wzp6_ee_eeH_HWW_llnunu_ecm240_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection/training/wzp6_ee_eeH_HWW_llnunu_ecm240.root")'
            root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection/training/wzp6_ee_mumuH_HWW_llnunu_ecm240_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection/training/wzp6_ee_mumuH_HWW_llnunu_ecm240.root")'

        for 365 GeV:

            Loose:
                root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full_20260807_071918/preselection/wzp6_ee_eeH_HWW_ecm365_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full_20260807_071918/preselection/wzp6_ee_eeH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full_20260807_071918/preselection/wzp6_ee_mumuH_HWW_ecm365_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full_20260807_071918/preselection/wzp6_ee_mumuH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full_20260807_071918/preselection/training/wzp6_ee_eeH_HWW_ecm365_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full_20260807_071918/preselection/training/wzp6_ee_eeH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full_20260807_071918/preselection/training/wzp6_ee_mumuH_HWW_ecm365_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full_20260807_071918/preselection/training/wzp6_ee_mumuH_HWW_ecm365.root")'

            Medium:
                root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection/wzp6_ee_eeH_HWW_ecm365_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection/wzp6_ee_eeH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection/wzp6_ee_mumuH_HWW_ecm365_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection/wzp6_ee_mumuH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection/training/wzp6_ee_eeH_HWW_ecm365_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection/training/wzp6_ee_eeH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection/training/wzp6_ee_mumuH_HWW_ecm365_inc.root", "../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection/training/wzp6_ee_mumuH_HWW_ecm365.root")'

        Old (the rooteventselector doesn't copy other objects in the root file other than the tree):

            After running preselection.py, we need to apply the ww_leptonic cut on signal samples:

                mv wzp6_ee_eeH_HWW_ecm240.root wzp6_ee_eeH_HWW_ecm240_inc.root
                mv wzp6_ee_mumuH_HWW_ecm240.root wzp6_ee_mumuH_HWW_ecm240_inc.root

                rooteventselector -s "(ww_leptonic == 1)" wzp6_ee_eeH_HWW_ecm240_inc.root:events wzp6_ee_eeH_HWW_ecm240.root
                rooteventselector -s "(ww_leptonic == 1)" wzp6_ee_mumuH_HWW_ecm240_inc.root:events wzp6_ee_mumuH_HWW_ecm240.root
            

4. Print entries per root file:

    for 240 GeV:

        root -l -q 'PrintEntries.C("../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection")'
        root -l -q 'PrintEntries.C("../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/preselection/training")'

    for 365 GeV:

        root -l -q 'PrintEntries.C("../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection")'
        root -l -q 'PrintEntries.C("../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/preselection/training")'


5. Train the BDT (`train_bdt.py`) and make evaluation plots (`evaluate_bdt.py`)

    python3 train_bdt.py --scheme loose_full_20260807_071918 --ecm 240
    python3 train_bdt.py --scheme medium_full_chi2-1.0_iso-3.0_20260813_091733 --ecm 365


5.1. Plot BDT evaluation plots (called from `train_bdt.py`)

    python3 evaluate_bdt.py \
        -i ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/bdt_model.pkl \
        -o ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/plots_training2

    python3 evaluate_bdt.py \
        -i ../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/bdt_model.pkl \
        -o ../../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/plots_training2


6. Apply MVA score on each of the events in the analysis samples (`apply_mva.py`)

    python3 apply_mva.py -e 240 -s loose_full_20260807_071918
    python3 apply_mva.py -e 365 -s medium_full_chi2-1.0_iso-3.0_20260813_091733


7. Create histograms for two sets of cuts: before and after BDT cut (`final_selection.py`)

    ecm=240 scheme=loose_full_20260807_071918 fccanalysis final final_selection.py
    ecm=365 scheme=medium_full_chi2-1.0_iso-3.0_20260813_091733 fccanalysis final final_selection.py


8. Make plots for these two sets of cuts (`plots.py`)

    ecm=240 scheme=loose_full_20260807_071918 ymax=30000 fccanalysis plots plots.py
    ecm=365 scheme=medium_full_chi2-1.0_iso-3.0_20260813_091733 ymin=0.11 ymax=11000 fccanalysis plots plots.py


9. Prepare the Combine-compatible datacards (`combine.py`)

    ecm=240 scheme=loose_full_20260807_071918 fccanalysis combine combine.py
    ecm=365 scheme=medium_full_chi2-1.0_iso-3.0_20260813_091733 fccanalysis combine combine.py


10. Run fit: run CMS Combine tool inside a Singularity container:

    for 240 GeV:

        cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/combine/sel0
        singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_20260807_071918/combine/sel0; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'

    for 365 GeV:

        cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/combine/sel0
        singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/ecm365/medium_full_chi2-1.0_iso-3.0_20260813_091733/combine/sel0; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'
    

11. Combined fit:

    cd ../fit
    ./global_fit.sh "loose_full_20260807_071918/combine_with_inclWW" "medium_full_chi2-1.0_iso-3.0_20260813_091733/combine_allbkg"


12. Plot NNL scan:

    ./global_fit.sh "loose_full_20260807_071918/combine_with_inclWW" "medium_full_chi2-1.0_iso-3.0_20260813_091733/combine_allbkg" 1
    python3 plot_nll.py /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/combined_results/scan/higgsCombine_MyScan.MultiDimFit.mH120.root


## Plots style

Copy `util/do_plots.py` to `FCCAnalyses/install/python/do_plots.py` (after compilation) or to `FCCAnalyses/python/do_plots.py` (before compilation).


## Plotters

### Lepton pairing optimization: efficiency vs f_value

For 240 GeV:

    cd utils
    python3 plot_chi2_opt.py --ecm 240 --base-scheme presel --lumi 10.8 --chi2-default 0.4 --ymax 1.02 --ymin 0.86 --label "Preslections"

For 365 GeV:

    cd utils
    python3 plot_chi2_opt.py --ecm 365 --base-scheme presel --lumi 3.0 --chi2-default 0.4 --ymax 1.2 --ymin 0.55 --label "Preslections"


### Signal decomposition (365 GeV)

For `f = 0.4`:

    python plot_VBF.py --ecm 365 --scheme medium3 --label "Medium3 selections" --f 0.4

For `f = 1.0`:

    python plot_VBF.py --ecm 365 --scheme medium3_chi2-1.0 --label "Medium3 selections" --f 1.0


### Pairing scheme comparison (365 GeV)

Compare `f=0.4` with `f=1.0`:

    python3 plot_VBF_compare_schemes.py -ecm 365 -s medium3 -l "Medium3 selections"
