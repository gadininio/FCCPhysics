
# Cut-based analysis

## Run histmaker

- Run histmaker to create root files with histograms:

    Preselections only:
        ecm=365 sel=false fccanalysis run histmaker.py

    Loose selections:
        ecm=365 sel=true loose=true fccanalysis run histmaker.py

    Tight selections:
        ecm=365 sel=true loose=false fccanalysis run histmaker.py

    Full run:
        ecm=365 sel=true loose=false fullrun=true fccanalysis run histmaker.py

## Run plotter

- Run plotter to procude pdf files combining all samples:

    path=nosel_ fccanalysis plots plots_ecm365.py
    path=loose_ fccanalysis plots plots_ecm365.py
    path=tight_ fccanalysis plots plots_ecm365.py

- Run cutflow:

    python3 run_cutflow.py \
        -cfg ../zh_hww_4l/cutflow_cng/config_365_loose.json \
        -i ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_/ \
        -o ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/plots/loose_/ll/ \
        --latex

- Cut optimization:

    python simple_cut_optim.py \
        --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_' \
        --ecm 365 \
        --variables WW_leps_dR_cut9

## Run fit

- Prepare the Combine-compatible datacards:

    ecm=365 path=tight_ fccanalysis combine combine.py

- To perform the likelihood fit using the CMS Combine tool inside a Singularity container, run:

    cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm240/combine/full

    cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm365/combine/tight_
    singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm365/combine/tight_; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'



singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/combine/full; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'

singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/combine/full_20251125_134522; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'


No BDT:   loose selections - including a cut on the recoil mass. Fit is done using the BDT score.
With BDT: tight selections - no cut is applied on the recoil mass. Fit is done using the recoil mass.