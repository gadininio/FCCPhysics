
from addons.TMVAHelper.TMVAHelper import TMVAHelperXGB

run = 'full' # 'local', 'debug', 'full', 'full+condor'
is_loose = True 
apply_selections = True

if run == 'debug':  # debug run
    print("Running in debug mode: only 1% of bkg and 20% of signal data, 1 chunk")
    fraction = 0.01
    nchunks = 1
    condorize = False
    debug = True
    fullrun = False
elif run == 'full':  # full run
    print("Running in full mode: 100% of the data, 1 chunk")
    fraction = 1
    nchunks = 1
    condorize = False
    debug = False
    fullrun = True
elif run == 'full+condor':  # full run with condor
    print("Running in full mode: 100% of the data, 50 chunks, submitting to condor...")
    fraction = 1
    nchunks = 50
    condorize = True
    debug = False
    fullrun = True
else:  # local run
    print("Running in local mode: only 5% of bkg and 100% of signal data, 1 chunk")
    fraction = 0.05
    nchunks = 1
    condorize = False
    debug = False
    fullrun = False


# list of processes (mandatory)
processList_mumu = {
    'p8_ee_ZZ_ecm240':{'fraction': fraction, 'chunks': nchunks},
    'p8_ee_WW_ecm240':{'fraction': fraction, 'chunks': nchunks},
    'wzp6_ee_mumuH_HWW_ecm240':{'fraction': 1},
}

processList_ee = {
    'p8_ee_ZZ_ecm240':{'fraction': fraction, 'chunks': nchunks},
    'p8_ee_WW_ecm240':{'fraction': fraction, 'chunks': nchunks},
    'wzp6_ee_eeH_HWW_ecm240':{'fraction': 1},
}

processList = {'wzp6_ee_mumuH_HWW_ecm240':{'fraction': 0.2}} if debug else processList_mumu | processList_ee


# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Additional/custom C++ functions, defined in header files
includePaths = ["../../functions.h"]

# Output directory
output_fix = ""
if debug: output_fix = "debug/"
elif fullrun: output_fix = f"full{'_nosel' if not apply_selections else ''}/"
outputDir   = f"../../../outputs/higgs/zh_hww_4l/mva{'_loose' if is_loose else ''}/preselection/{output_fix}/"


# Multithreading: -1 means using all cores
nCPUS       = -1

# Batch settings
runBatch    = condorize
batchQueue  = "longlunch"
compGroup = "group_u_FCC.local_gen"

# After training the BDT model, set to True to run inference and add the MVA score to the output ROOT files
doInference = False


class RDFanalysis():

    # encapsulate analysis logic, definitions and filters in the dataframe
    def analysers(df):

        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

        # For signal events, keep only fully-leptonic WW decays (truth-level selection)
        df = df.Define("ww_leptonic", "FCCAnalyses::ZHfunctions::is_ww_leptonic(Particle, Particle1)")
        # df = df.Filter("ww_leptonic")

        ## define muons
        df = df.Alias("Muon0", "Muon#0.index")
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
        # df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
        
        df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(10)(muons_all)")
        # df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
        # df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
        # df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

        # # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
        # df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
        # df = df.Define("muons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, muons_iso)")

        ## define electrons
        df = df.Alias("Electron0", "Electron#0.index")
        df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
        # df = df.Define("electrons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
        
        df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(10)(electrons_all)")
        # df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
        # df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
        # df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
        df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
        df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")

        # # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
        # df = df.Define("electrons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
        # df = df.Define("electrons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(electrons, electrons_iso)")


        #########
        ### CUT 1: exactly 4 leptons (add isolation later)
        #########
        df = df.Define("n_leptons", "muons_no + electrons_no")
        df = df.Filter("n_leptons == 4")


        #########
        ### CUT 2: at least 2 opposite-sign (OS) leptons
        #########
        # df = df.Filter(f"{leps}_no >= 2 && abs(Sum({leps}_q)) < {leps}_q.size()")
        # df = df.Filter(f"abs(Sum({leps}_q)) <= {leps}_q.size() - 4")
        df = df.Filter(f"abs(Sum(muons_q) + Sum(electrons_q)) <= muons_q.size() + electrons_q.size() - 4")


        #########
        ### CUT 3: at least one same-flavor (SF) lepton pair
        #########
        df = df.Filter("(muons_no >= 2) || (electrons_no >= 2)")


        #########
        ### CUT 4: leptons pT: leading muon pT [25, 80] GeV, subleading muon pT [15, 80] GeV, third muon pT [10,80] GeV, fourth muon pT [10,75] GeV
        #########
        df = df.Define("leptons0", "FCCAnalyses::ReconstructedParticle::merge(muons, electrons)")
        df = df.Define("leptons", "FCCAnalyses::ZHfunctions::sortByPt(leptons0)")
        df = df.Define("leptons_p", "FCCAnalyses::ReconstructedParticle::get_p(leptons)")

        df = df.Define("lep0_p", "leptons_p[0]")
        df = df.Define("lep1_p", "leptons_p[1]")
        df = df.Define("lep2_p", "leptons_p[2]")
        df = df.Define("lep3_p", "leptons_p[3]")
        
        if apply_selections:
            if is_loose:
                df = df.Filter("lep0_p > 20 && lep0_p < 85")
                df = df.Filter("lep1_p > 10 && lep1_p < 80")
                df = df.Filter("lep2_p > 10 && lep2_p < 80")
                df = df.Filter("lep3_p > 10 && lep3_p < 75")
            else:
                df = df.Filter("lep0_p > 25 && lep0_p < 80")
                df = df.Filter("lep1_p > 15 && lep1_p < 80")
                df = df.Filter("lep2_p > 10 && lep2_p < 80")
                df = df.Filter("lep3_p > 10 && lep3_p < 75")


        #########
        ### Reconstruct the Z->ll candidate
        #########
        # Now we build the Z resonance based on the available leptons.
        # The function resonanceBuilder_mass_recoil_advanced returns the best lepton pair compatible with the Z mass (91.2 GeV) and recoil at 125 GeV, out of the 4 leptons, and the two remaining leptons coming from the W's.
        # The argument 0.4 gives a weight to the Z mass and the recoil mass in the chi2 minimization.
        # Technically, it returns a ReconstructedParticleData object with index 0 the Z->ll di-lepton system, index 1 and 2 the leptons of the pair, and index 3 and 4 the other two leptons.
        # If no pair is found, the returned vector is empty.
        # We then require that at least one pair was found (size>=5) to keep the event.
        df = df.Define("zbuilder_result", f"FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil_advanced(91.2, 125, 0.4, 240, false)(muons, electrons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
        df = df.Filter("zbuilder_result.size() >= 5") # make sure at least one pair was found (and additional two leptons)
        
        df = df.Define("zll", "Vec_rp{zbuilder_result[0]}") # the Z
        df = df.Define("zll_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(zll, 0)")
        df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]") # Z mass
        df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]") # momentum of the Z
        df = df.Define("zll_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll)[0]") # momentum of the Z
        df = df.Define("zll_phi", "FCCAnalyses::ReconstructedParticle::get_phi(zll)[0]") # momentum of the Z
    
        ## Recoil mass
        df = df.Define("zll_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zll)") # compute the recoil based on the reconstructed Z
        df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]") # recoil mass
        
        ## Study the Z-lepton candidates
        df = df.Define("zll_leps", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}") # the leptons 
        df = df.Define("zll_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(zll_leps)") # get the momentum of the 2 leptons from the Z resonance
        df = df.Define("zll_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll_leps)") # get the theta of these 2 leptons
        df = df.Define("zll_leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(zll_leps)") # get the phi of these 2 leptons
        df = df.Define("zll_leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(zll_leps)")

        df = df.Define("zll_lep0_p", "zll_leps_p[0]")
        df = df.Define("zll_lep0_theta", "zll_leps_theta[0]")
        df = df.Define("zll_lep0_phi", "zll_leps_phi[0]")
        df = df.Define("zll_lep1_p", "zll_leps_p[1]")
        df = df.Define("zll_lep1_theta", "zll_leps_theta[1]")
        df = df.Define("zll_lep1_phi", "zll_leps_phi[1]")

        df = df.Define("zll_lep0_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(zll_leps, 0)")
        df = df.Define("zll_lep1_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(zll_leps, 1)")
        df = df.Define("zll_leps_dR", "zll_lep0_tlv.DeltaR(zll_lep1_tlv)")
        
        df = df.Define("zll_leps_category", "FCCAnalyses::ZHfunctions::getDileptonCategory(zll_leps)")
        df = df.Define("zll_lep0_p_index", "FCCAnalyses::ZHfunctions::findIndex(zll_lep0_p, {lep0_p, lep1_p, lep2_p, lep3_p})")
        df = df.Define("zll_lep1_p_index", "FCCAnalyses::ZHfunctions::findIndex(zll_lep1_p, {lep0_p, lep1_p, lep2_p, lep3_p})")

        ## Study the WW-lepton candidates
        df = df.Define("WW_leps", "Vec_rp{zbuilder_result[3],zbuilder_result[4]}") # the leptons 
        df = df.Define("WW_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(WW_leps)")
        df = df.Define("WW_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(WW_leps)")
        df = df.Define("WW_leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(WW_leps)")
        df = df.Define("WW_leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(WW_leps)")
        
        df = df.Define("WW_lep0_p", "WW_leps_p[0]")
        df = df.Define("WW_lep0_theta", "WW_leps_theta[0]")
        df = df.Define("WW_lep0_phi", "WW_leps_phi[0]")
        df = df.Define("WW_lep1_p", "WW_leps_p[1]")
        df = df.Define("WW_lep1_theta", "WW_leps_theta[1]")
        df = df.Define("WW_lep1_phi", "WW_leps_phi[1]")
        
        df = df.Define("WW_leps_tlv0", "FCCAnalyses::ReconstructedParticle::get_tlv(WW_leps, 0)")
        df = df.Define("WW_leps_tlv1", "FCCAnalyses::ReconstructedParticle::get_tlv(WW_leps, 1)")
        df = df.Define("WW_leps_dR", "WW_leps_tlv0.DeltaR(WW_leps_tlv1)")

        df = df.Define("WW_leps_category", "FCCAnalyses::ZHfunctions::getDileptonCategory(WW_leps)")
        df = df.Define("WW_lep0_p_index", "FCCAnalyses::ZHfunctions::findIndex(WW_lep0_p, {lep0_p, lep1_p, lep2_p, lep3_p})")
        df = df.Define("WW_lep1_p_index", "FCCAnalyses::ZHfunctions::findIndex(WW_lep1_p, {lep0_p, lep1_p, lep2_p, lep3_p})")
                
        ## Build the WW system using the two leptons not coming from the Z and the missing energy vector
        df = df.Define("missingEnergy_vec", "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)")
        df = df.Define("missingEnergy_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(missingEnergy_vec, 0)")
        df = df.Define("WW_tlv", "missingEnergy_tlv + WW_leps_tlv0 + WW_leps_tlv1")
        df = df.Define("WW_mass", "WW_tlv.M()")
        df = df.Define("WW_p", "WW_tlv.P()")
        df = df.Define("WW_theta", "WW_tlv.Theta()")
        df = df.Define("WW_phi", "WW_tlv.Phi()")

        ## dR(Z, WW)
        df = df.Define("zll_WW_dR", "WW_tlv.DeltaR(zll_tlv)")
        
        
        #########
        ### CUT 5: Z mass window
        #########
        if apply_selections:
            df = df.Filter("zll_m > 76 && zll_m < 106")


        #########
        ### CUT 6: Z momentum
        #########
        if apply_selections:
            df = df.Filter("zll_p > 20 && zll_p < 70")


        #########
        ### CUT 7: recoil mass window (reconstructed Higgs mass using the recoil method)
        #########
        if apply_selections:
            if is_loose:
                df = df.Filter("zll_recoil_m < 145 && zll_recoil_m > 120")
            else:
                df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")


        #########
        ### CUT 8: cosThetaMiss
        #########  
        df = df.Define("miss_cosTheta", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergy_vec)")
        df = df.Define("miss_energy", "FCCAnalyses::ZHfunctions::get_missing_energy(missingEnergy_vec)")
        if apply_selections:
            df = df.Filter("miss_cosTheta < 0.98")


        #########
        ### CUT 9: missingEnergy
        #########  
        if apply_selections:
            if is_loose:
                df = df.Filter("miss_energy > 20 && miss_energy < 120")
            else:
                df = df.Filter("miss_energy > 30 && miss_energy < 110")


        #########
        ### CUT 10: WW system mass window
        #########
        if apply_selections:
            if is_loose:
                df = df.Filter("WW_mass > 60 && WW_mass < 135")
            else:
                df = df.Filter("WW_mass > 80 && WW_mass < 135")


        #########
        ### CUT *: WW system momentum
        #########
        # df = df.Filter("WW_p > 25 && WW_p < 55")


        #########
        ### CUT 10: dR(l_WW, l_WW) > 0.25
        #########  
        if apply_selections:
            df = df.Filter("WW_leps_dR > 0.25")
            
            
        if doInference:
            tmva_helper = TMVAHelperXGB("../../../outputs/higgs/zh_hww_4l/mva/bdt_model_example.root", "bdt_model") # read the XGBoost training
            df = tmva_helper.run_inference(df, col_name="mva_score") # by default, makes a new column mva_score

        return df


    # define output branches to be saved
    def output():
        
        branchList = [
            # leptons
            "lep0_p",
            "lep1_p",
            "lep2_p",
            "lep3_p",
            "muons_no",
            "electrons_no",
            
            # Z->ll system
            "zll_m",
            "zll_p",
            "zll_theta",
            "zll_phi",
            "zll_recoil_m",
            
            # Z->ll leptons 
            "zll_lep0_p",
            "zll_lep0_theta",
            "zll_lep0_phi",
            "zll_lep1_p",
            "zll_lep1_theta",
            "zll_lep1_phi",
            
            "zll_leps_dR",
            "zll_leps_category",
            "zll_lep0_p_index",
            "zll_lep1_p_index",
            
            # WW leptons
            "WW_lep0_p",
            "WW_lep0_theta",
            "WW_lep0_phi",
            "WW_lep1_p",
            "WW_lep1_theta",
            "WW_lep1_phi",

            "WW_leps_dR",
            "WW_leps_category",
            "WW_lep0_p_index",
            "WW_lep1_p_index",
            
            # WW system
            "WW_mass",
            "WW_p",
            "WW_theta",
            "WW_phi",

            # dR(Z, WW)
            "zll_WW_dR",
            
            # missing energy
            "miss_cosTheta",
            "miss_energy",
            
            "ww_leptonic",
        ]

        if doInference:
            branchList.append("mva_score")
            
        return branchList
