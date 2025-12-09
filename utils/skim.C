
/**
 * This macro skims a ROOT TTree based on a given cut and copies all other.
 * 
 * Run:
 *  root -l -b -q 'skim.C("input.root", "skim.root")'
 * 
 * Or with a custom cut:
 *  root -l -b -q 'skim.C("input.root", "skim.root", "lep_pt>20", "events")'
 * 
 * Examples:
 *  root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva_loose/preselection/full/wzp6_ee_eeH_HWW_ecm240_inc.root", "../../outputs/higgs/zh_hww_4l/mva_loose/preselection/full/wzp6_ee_eeH_HWW_ecm240.root")'
 *  root -l -b -q 'skim.C("../../outputs/higgs/zh_hww_4l/mva_loose/preselection/full/wzp6_ee_mumuH_HWW_ecm240_inc.root", "../../outputs/higgs/zh_hww_4l/mva_loose/preselection/full/wzp6_ee_mumuH_HWW_ecm240.root")'
 *  
 * Parameters:
 * infile   : input ROOT file name
 * outfile  : output ROOT file name
 * cut      : selection cut (in TTree::Draw format)
 * treename : name of the TTree to be skimmed
 * 
 */

 void skim(const char* infile = "input.root",
           const char* outfile = "skim.root",
           const char* cut = "(ww_leptonic == 1)",
           const char* treename = "events")
{
    // Open input file
    TFile *fin = TFile::Open(infile);
    if (!fin || fin->IsZombie()) {
        std::cerr << "Cannot open " << infile << std::endl;
        return;
    }

    // Get the tree
    TTree *tin = (TTree*)fin->Get(treename);
    if (!tin) {
        std::cerr << "Tree '" << treename << "' not found!" << std::endl;
        return;
    }

    // Create output file
    TFile *fout = TFile::Open(outfile, "RECREATE");

    // --- 1. Copy the skimmed tree ---
    TTree *tout = tin->CopyTree(cut);
    tout->Write();  // writes with same name

    // --- 2. Copy all other objects (TParameter, histograms, etc.) ---
    auto keys = fin->GetListOfKeys();
    for (TObject *obj : *keys) {
        auto key = (TKey*)obj;

        // Skip the original TTree
        if (strcmp(key->GetName(), treename) == 0)
            continue;

        // Read and write each object
        TObject *o = key->ReadObj();
        fout->WriteObject(o, key->GetName());
    }

    fout->Close();
    fin->Close();
}
