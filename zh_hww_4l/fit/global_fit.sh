#!/bin/bash

# Run with:
# ./global_fit.sh <scheme_240> <scheme_365>
# ./global_fit.sh "loose_full_20260804/combine_with_inclWW" "medium_full_chi2-1.0_iso-3.0/combine_allbkg"


# 1. Define your variables
SCHEME_240=$1
SCHEME_365=$2
SCAN_TYPE=${3:-"0"}  # get the scan type from the third argument, default to "0" if not provided

BASE_DIR="/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/mva"
if [ "$SCAN_TYPE" == "1" ]; then
    COMBINE_DIR="${BASE_DIR}/combined_results/scan"
else
    COMBINE_DIR="${BASE_DIR}/combined_results/default"
fi
CONTAINER="/eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif"

# 2. Define the exact paths to the datacards
CARD_240="${BASE_DIR}/ecm240/${SCHEME_240}/sel0/datacard.txt"
CARD_365="${BASE_DIR}/ecm365/${SCHEME_365}/sel0/datacard.txt"

# 3. SAFETY CHECK: Do these files actually exist?
if [ ! -f "$CARD_240" ]; then
    echo "ERROR: Could not find the 240 GeV datacard!"
    echo "I looked here: $CARD_240"
    echo "Please check your SCHEME_240 argument and directory structure."
    exit 1
fi

if [ ! -f "$CARD_365" ]; then
    echo "ERROR: Could not find the 365 GeV datacard!"
    echo "I looked here: $CARD_365"
    echo "Please check your SCHEME_365 argument and directory structure."
    exit 1
fi

echo "Both datacards found. Proceeding with the combination..."

# 4. Create new directory for the combined results
mkdir -p ${COMBINE_DIR}
cd ${COMBINE_DIR}

# 5. Run the full chain inside Singularity: If scan==1, run the grid scan, otherwise run the default MultiDimFit
if [ "$SCAN_TYPE" == "1" ]; then
    echo "Running grid scan..."
    singularity exec -B /afs -B /eos ${CONTAINER} bash -c "
        combineCards.py ecm240=${CARD_240} ecm365=${CARD_365} > combined_datacard.txt;
        text2workspace.py combined_datacard.txt -o combined_ws.root;
        combine -M MultiDimFit --algo grid --points 100 --rMin 0.90 --rMax 1.10 -n _MyScan combined_ws.root
    "
else
    echo "Running default MultiDimFit..."
    singularity exec -B /afs -B /eos ${CONTAINER} bash -c "
        combineCards.py ecm240=${CARD_240} ecm365=${CARD_365} > combined_datacard.txt;
        text2workspace.py combined_datacard.txt -o combined_ws.root;
        combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 combined_ws.root
    "
fi



# # 5. Run the full chain inside Singularity
# singularity exec -B /afs -B /eos ${CONTAINER} bash -c "
    
#     # Combine the cards
#     combineCards.py ecm240=${CARD_240} ecm365=${CARD_365} > combined_datacard.txt;
    
#     # Create the workspace from the combined card
#     text2workspace.py combined_datacard.txt -o combined_ws.root;
    
#     # Run the MultiDimFit
#     combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 combined_ws.root
#     # combine -M MultiDimFit --algo grid --points 100 --rMin 0.90 --rMax 1.10 -n _MyScan combined_ws.root
# "


# diagnostic fits:

# singularity exec -B /afs -B /eos ${CONTAINER} bash -c "
#     cd ${COMBINE_DIR};
#     combine -M FitDiagnostics -d combined_ws.root --rMin 0.8 --rMax 1.2
# "

# singularity exec -B /afs -B /eos ${CONTAINER} bash -c "
#     cd ${BASE_DIR}/ecm240/${SCHEME_240}/sel0;
#     text2workspace.py datacard.txt -o ws_240.root;
#     combine -M FitDiagnostics ws_240.root
# "

# singularity exec -B /afs -B /eos ${CONTAINER} bash -c "
#     cd ${BASE_DIR}/ecm365/${SCHEME_365}/sel0;
#     text2workspace.py datacard.txt -o ws_365.root;
#     combine -M FitDiagnostics ws_365.root
# "


# singularity exec -B /afs -B /eos ${CONTAINER} bash -c "
#     cd ${COMBINE_DIR};
#     combine -M FitDiagnostics combined_ws.root --freezeParameters all
# "