
# Commands

Run in the following order:


    1. Create ntuples with preselected events (preselection.py)

        Loose selections:
            - For training samples:
                run=full ecm=365 training=True sel_type=1 fccanalysis run preselection.py
            - For standard samples:
                run=full ecm=365 training=False sel_type=1 fccanalysis run preselection.py

        Medium selections:
            - For training samples:
                run=full ecm=365 training=True sel_type=5 fccanalysis run preselection.py
            - For standard samples:
                run=full ecm=365 training=False sel_type=5 fccanalysis run preselection.py


        Copy the WW_ee and WW_mumu training samples together with the standard samples, as they are not used for the training but are used fitting.


    2. Apply the ww_leptonic cut on signal samples (utils/skim.C)
    
        - Rename the signal output root files (training and standard samples):
            mv wzp6_ee_eeH_HWW_llnunu_ecm240.root wzp6_ee_eeH_HWW_llnunu_ecm240_inc.root
            mv wzp6_ee_mumuH_HWW_llnunu_ecm240.root wzp6_ee_mumuH_HWW_llnunu_ecm240_inc.root
            mv wzp6_ee_eeH_HWW_ecm240.root wzp6_ee_eeH_HWW_ecm240_inc.root
            mv wzp6_ee_mumuH_HWW_ecm240.root wzp6_ee_mumuH_HWW_ecm240_inc.root

        - Run the skimmer to keep only true leptonic-WW signal events:

        for 240 GeV:
            root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full/preselection/wzp6_ee_eeH_HWW_llnunu_ecm240_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full/preselection/wzp6_ee_eeH_HWW_llnunu_ecm240.root")'
            root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full/preselection/wzp6_ee_mumuH_HWW_llnunu_ecm240_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full/preselection/wzp6_ee_mumuH_HWW_llnunu_ecm240.root")'
            root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full/preselection/training/wzp6_ee_eeH_HWW_llnunu_ecm240_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full/preselection/training/wzp6_ee_eeH_HWW_llnunu_ecm240.root")'
            root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full/preselection/training/wzp6_ee_mumuH_HWW_llnunu_ecm240_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full/preselection/training/wzp6_ee_mumuH_HWW_llnunu_ecm240.root")'

        for 365 GeV:

            Loose:
                root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/preselection/wzp6_ee_eeH_HWW_ecm365_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/preselection/wzp6_ee_eeH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/preselection/wzp6_ee_mumuH_HWW_ecm365_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/preselection/wzp6_ee_mumuH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/preselection/training/wzp6_ee_eeH_HWW_ecm365_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/preselection/training/wzp6_ee_eeH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/preselection/training/wzp6_ee_mumuH_HWW_ecm365_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/preselection/training/wzp6_ee_mumuH_HWW_ecm365.root")'

            Medium:
                root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full/preselection/wzp6_ee_eeH_HWW_ecm365_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full/preselection/wzp6_ee_eeH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full/preselection/wzp6_ee_mumuH_HWW_ecm365_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full/preselection/wzp6_ee_mumuH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full/preselection/training/wzp6_ee_eeH_HWW_ecm365_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full/preselection/training/wzp6_ee_eeH_HWW_ecm365.root")'
                root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full/preselection/training/wzp6_ee_mumuH_HWW_ecm365_inc.root", "../../outputs/higgs/zh_hww_4l/mva/ecm365/medium_full/preselection/training/wzp6_ee_mumuH_HWW_ecm365.root")'

        Old (the rooteventselector doesn't copy other objects in the root file other than the tree):

            After running preselection.py, we need to apply the ww_leptonic cut on signal samples:

                mv wzp6_ee_eeH_HWW_ecm240.root wzp6_ee_eeH_HWW_ecm240_inc.root
                mv wzp6_ee_mumuH_HWW_ecm240.root wzp6_ee_mumuH_HWW_ecm240_inc.root

                rooteventselector -s "(ww_leptonic == 1)" wzp6_ee_eeH_HWW_ecm240_inc.root:events wzp6_ee_eeH_HWW_ecm240.root
                rooteventselector -s "(ww_leptonic == 1)" wzp6_ee_mumuH_HWW_ecm240_inc.root:events wzp6_ee_mumuH_HWW_ecm240.root
            

    3. Train the BDT (train_bdt.py) and make evaluation plots (evaluate_bdt.py)

        python3 train_bdt.py --scheme loose_full --ecm 240
        python3 train_bdt.py --scheme loose_full --ecm 365


    4. Apply MVA score on each of the events in the analysis samples (apply_mva.py)

        python3 apply_mva.py -e 240 -s loose_full
        python3 apply_mva.py -e 365 -s loose_full


    5. Create histograms for two sets of cuts: before and after BDT cut (final_selection.py)

        ecm=240 scheme=loose_full fccanalysis final final_selection.py
        ecm=365 scheme=loose_full fccanalysis final final_selection.py


    6. Make plots for these two sets of cuts (plots.py)

        ecm=240 scheme=loose_full fccanalysis plots plots.py
        ecm=365 scheme=loose_full fccanalysis plots plots.py


    7. Prepare the Combine-compatible datacards (combine.py)

        ecm=240 scheme=loose_full fccanalysis combine combine.py
        ecm=365 scheme=loose_full fccanalysis combine combine.py


    8. Run fit: run CMS Combine tool inside a Singularity container:
    
        cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/ecm240/loose_full/combine/sel0
        singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/ecm240/loose_full/combine/sel0; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'

        cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/combine/sel0
        singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/combine/sel0; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'
        


# Plots style

Copy `util/do_plots.py` to `FCCAnalyses/install/python/do_plots.py` (after compilation) or to `FCCAnalyses/python/do_plots.py` (before compilation).