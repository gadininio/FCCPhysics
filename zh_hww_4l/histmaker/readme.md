
# $Z(\ell\ell)H, H \to WW^* \to \ell\nu\ell\nu$ feasibility study for FCC-ee: cut-based analysis - commands

## Run histmaker

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


## Run plotter

Run plotter to procude pdf files combining all samples:

1. for 240 GeV:
    ```
    fccanalysis plots plots.py
    ```

2. for 365 GeV:
    ```
    scheme=medium3_full_chi2-1.0_iso-3.0_20260813_081619 inclWW=true iso=true fccanalysis plots plots_ecm365.py
    ```


## Run cutflow

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


## Cut optimization

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


## Get efficiency/total yield

for 365 GeV, zll_m_cut4

    python3 analyze_hists.py \
        /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium3_chi2-1.0/wzp6_ee_eeH_HWW_ecm365.root \
        -n zll_m_cut4 --xmin 51 --xmax 131


## Run fit

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