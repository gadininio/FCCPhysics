#!/bin/bash

# 1. Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <ecm> <scheme>"
    echo "Example: $0 365 medium_full_chi2-1.0_iso-3.0"
    exit 1
fi

# 2. Assign arguments to variables for readability
ECM=$1
SCHEME=$2

# 3. Define the working directory path
WORK_DIR="/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva/ecm${ECM}/${SCHEME}/combine/sel0"

# 4. Check if the directory exists before running Singularity
if [ ! -d "$WORK_DIR" ]; then
    echo "Error: Directory does not exist:"
    echo "$WORK_DIR"
    exit 1
fi

echo "Running scan for ECM=${ECM} and Scheme=${SCHEME}..."
echo "Directory: ${WORK_DIR}"

# 5. Execute the Singularity command
# Note: Double quotes are used here so $WORK_DIR expands correctly inside the container command.
singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c "
    cd ${WORK_DIR} || exit 1;
    
    # Create the workspace (if you haven't already)
    text2workspace.py datacard.txt -o ws.root;
    
    # Run the grid scan
    combine -M MultiDimFit --algo grid --points 100 --rMin 0.8 --rMax 1.2 -n _MyScan ws.root
"

echo "Done! Output saved in ${WORK_DIR}"