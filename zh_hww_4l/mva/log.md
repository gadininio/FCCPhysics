
Run in the following order:

    1. preselection.py      --> fccanalysis run preselection.py
    2. skim.C               --> root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva_loose/preselection/full/wzp6_ee_eeH_HWW_ecm240_inc.root", "../../outputs/higgs/zh_hww_4l/mva_loose/preselection/full/wzp6_ee_eeH_HWW_ecm240.root")'
                                root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva_loose/preselection/full/wzp6_ee_mumuH_HWW_ecm240_inc.root", "../../outputs/higgs/zh_hww_4l/mva_loose/preselection/full/wzp6_ee_mumuH_HWW_ecm240.root")'
    3. train_bdt.py         --> python3 train_bdt.py
    4. evaluate_bdt.py      --> python3 evaluate_bdt.py -l
    5. apply_mva.py         --> python3 apply_mva.py -f -l
    6. final_selection.py   --> fccanalysis funal final_selection.py


After running preselection.py, we need to apply the ww_leptonic cut on signal samples:

    mv wzp6_ee_eeH_HWW_ecm240.root wzp6_ee_eeH_HWW_ecm240_inc.root
    mv wzp6_ee_mumuH_HWW_ecm240.root wzp6_ee_mumuH_HWW_ecm240_inc.root

    rooteventselector -s "(ww_leptonic == 1)" wzp6_ee_eeH_HWW_ecm240_inc.root:events wzp6_ee_eeH_HWW_ecm240.root
    rooteventselector -s "(ww_leptonic == 1)" wzp6_ee_mumuH_HWW_ecm240_inc.root:events wzp6_ee_mumuH_HWW_ecm240.root
    

singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva_loose/combine/full/sel1; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'

