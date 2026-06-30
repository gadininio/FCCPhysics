
# Cut-based analysis

## Run histmaker

- Run histmaker to create root files with histograms:

    Preselections only:
        ecm=240 sel_type=0 fccanalysis run histmaker.py
        ecm=365 sel_type=0 fccanalysis run histmaker.py

    Loose/Medium selections:
        ecm=240 sel_type=1 fccanalysis run histmaker.py
        ecm=365 sel_type=5 fccanalysis run histmaker.py

    Medium selections with isolation:
        ecm=365 sel_type=5 chi2=1.0 iso=3 fccanalysis run histmaker.py

    Full run:
        ecm=365 sel_type=5 chi2=1.0 iso=3 fullrun=true fccanalysis run histmaker.py

## Run plotter

- Run plotter to procude pdf files combining all samples:

    fccanalysis plots plots.py
    scheme=medium3_full_chi2-1.0_iso-3.0 inclWW=true iso=true fccanalysis plots plots_ecm365.py
    
- Run cutflow:

    python3 detailed_cutflow.py \
        -cfg ../cutflow_cng/config_240_loose_allbkg.json \
        -i ../../outputs/higgs/zh_hww_4l/histmaker/ecm240/hists/full_loose_20260126_112336/ \
        -o ../../outputs/higgs/zh_hww_4l/histmaker/ecm240/plots/full_loose_20260126_112336/ll/ \
        --latex

    python3 detailed_cutflow.py \
        -cfg ../cutflow_cng/config_365_loose.json \
        -i ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/ \
        -o ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/plots/loose_full/ll/ \
        --latex

    python3 detailed_cutflow.py \
        -cfg ../cutflow_cng/config_365_loose_training.json \
        -i ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_training_full/ \
        -o ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/plots/loose_training_full/ll/ \
        --latex

    python3 detailed_cutflow.py \
        -cfg ../cutflow_cng/config_365_medium4_inclWWInFit.json \
        -i ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium4/ \
        -o ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/plots/medium4/ll/ \
        --latex

- Cut optimization:

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

## Run fit

- Prepare the Combine-compatible datacards:

    ecm=365 scheme=tight_norecoil fccanalysis combine combine.py

- To perform the likelihood fit using the CMS Combine tool inside a Singularity container, run:

    cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm240/combine/full

    cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm365/combine/tight_norecoil
    singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm365/combine/tight_norecoil; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'



singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/combine/full; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'

singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/combine/full_20251125_134522; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'


No BDT:   loose selections - including a cut on the recoil mass. Fit is done using the BDT score.
With BDT: tight selections - no cut is applied on the recoil mass. Fit is done using the recoil mass.