

# Run histmaker

- Run histmaker to create root files with hostograms:

    fccanalysis run histmaker.py

# Run plotter

- Run plotter to procude pdf files combining all samples:

    fccanalysis plots plots.py

# Run fit

- Prepare the Combine-compatible datacards:

    fccanalysis combine combine.py

- To perform the likelihood fit using the CMS Combine tool inside a Singularity container, run:

    cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/combine/full

    singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/combine/full; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'

