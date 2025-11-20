
from addons.TMVAHelper.TMVAHelper import TMVAHelperXGB

run = 'full' # 'local', 'debug', 'full', 'full+condor'
is_loose = True 

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
elif fullrun: output_fix = "full/"
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
        df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
        
        df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(10)(muons_all)")
        df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
        df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
        df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

        # # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
        # df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
        # df = df.Define("muons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, muons_iso)")

        ## define electrons
        df = df.Alias("Electron0", "Electron#0.index")
        df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
        df = df.Define("electrons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
        
        df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(10)(electrons_all)")
        df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
        df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
        df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
        df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
        df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")

        # # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
        # df = df.Define("electrons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
        # df = df.Define("electrons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(electrons, electrons_iso)")

        #########
        ### CUT 1: exactly 4 leptons (add isolation later)
        #########
        # df = df.Filter(f"{leps}_no >= 1 && {leps}_sel_iso.size() > 0")
        # df = df.Filter(f"{leps}_no == 4")
        df = df.Filter("muons_no + electrons_no == 4")

        #########
        ### CUT 2: at least 2 opposite-sign (OS) leptons
        #########
        # df = df.Filter(f"{leps}_no >= 2 && abs(Sum({leps}_q)) < {leps}_q.size()")
        # df = df.Filter(f"abs(Sum({leps}_q)) <= {leps}_q.size() - 4")
        df = df.Filter(f"abs(Sum(muons_q) + Sum(electrons_q)) <= muons_q.size() + electrons_q.size() - 4")

        #########
        ### CUT 3: leptons pT: leading muon pT [25, 80] GeV, subleading muon pT [15, 80] GeV, third muon pT [10,80] GeV, fourth muon pT [10,75] GeV
        #########
        df = df.Define("leptons0", "FCCAnalyses::ReconstructedParticle::merge(muons, electrons)")
        df = df.Define("leptons", "FCCAnalyses::ZHfunctions::sortByPt(leptons0)")
        df = df.Define("leptons_p", "FCCAnalyses::ReconstructedParticle::get_p(leptons)")

        df = df.Define("lep0_p", "leptons_p[0]")
        df = df.Define("lep1_p", "leptons_p[1]")
        df = df.Define("lep2_p", "leptons_p[2]")
        df = df.Define("lep3_p", "leptons_p[3]")
        
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
        
        #########
        ### CUT 4: Z mass window
        #########
        df = df.Define("zll", "Vec_rp{zbuilder_result[0]}") # the Z
        df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]") # Z mass
        df = df.Filter("zll_m > 86 && zll_m < 96")

        #########
        ### CUT 5: Z momentum
        #########
        df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]") # momentum of the Z
        df = df.Filter("zll_p > 20 && zll_p < 70")

        #########
        ### CUT 6: recoil mass window (reconstructed Higgs mass using the recoil method)
        #########
        df = df.Define("zll_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zll)") # compute the recoil based on the reconstructed Z
        df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]") # recoil mass
        if is_loose:
            df = df.Filter("zll_recoil_m < 145 && zll_recoil_m > 120")
        else:
            df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")

        #########
        ### CUT 7: cosThetaMiss
        #########  
        df = df.Define("missingEnergy_vec", "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)")
        df = df.Define("miss_cosTheta", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergy_vec)")
        df = df.Filter("miss_cosTheta < 0.98")

        #########
        ### CUT 8: missingEnergy
        #########  
        df = df.Define("miss_energy", "FCCAnalyses::ZHfunctions::get_missing_energy(missingEnergy_vec)")
        if is_loose:
            df = df.Filter("miss_energy > 20 && miss_energy < 120")
        else:
            df = df.Filter("miss_energy > 30 && miss_energy < 110")

        #########
        ### Addotional studies
        #########  
        ## Studies with the two leptons coming from the Z
        df = df.Define("zll_leps", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}") # the leptons 

        df = df.Define("zll_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(zll_leps)") # get the momentum of the 2 leptons from the Z resonance
        df = df.Define("zll_lep1_p", "zll_leps_p[0]") # the leptons 
        df = df.Define("zll_lep2_p", "zll_leps_p[1]") # the leptons 

        df = df.Define("zll_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll_leps)") # get the momentum of the 2 leptons from the Z resonance
        df = df.Define("zll_lep1_theta", "zll_leps_theta[0]") # the leptons 
        df = df.Define("zll_lep2_theta", "zll_leps_theta[1]") # the leptons 
        
        df = df.Define("Zll_leps_tlv0", "FCCAnalyses::ReconstructedParticle::get_tlv(zll_leps, 0)")
        df = df.Define("Zll_leps_tlv1", "FCCAnalyses::ReconstructedParticle::get_tlv(zll_leps, 1)")
        df = df.Define("Zll_leps_dR", "Zll_leps_tlv0.DeltaR(Zll_leps_tlv1)")
        
        ## Additional studies with the two leptons not coming from the Z (to characterize the WW system)
        df = df.Define("WW_leps", "Vec_rp{zbuilder_result[3],zbuilder_result[4]}") # the leptons 
        df = df.Define("WW_leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(WW_leps)")
        df = df.Define("WW_leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(WW_leps)")
        df = df.Define("WW_leps_no", "FCCAnalyses::ReconstructedParticle::get_n(WW_leps)")
        
        df = df.Define("WW_leps_tlv0", "FCCAnalyses::ReconstructedParticle::get_tlv(WW_leps, 0)")
        df = df.Define("WW_leps_tlv1", "FCCAnalyses::ReconstructedParticle::get_tlv(WW_leps, 1)")
        df = df.Define("WW_leps_dR", "WW_leps_tlv0.DeltaR(WW_leps_tlv1)")
        
        df = df.Define("WW_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(WW_leps)")
        df = df.Define("WW_lep1_p", "WW_leps_p[0]")
        df = df.Define("WW_lep2_p", "WW_leps_p[1]")        
        
        df = df.Define("WW_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(WW_leps)")
        df = df.Define("WW_lep1_theta", "WW_leps_theta[0]")
        df = df.Define("WW_lep2_theta", "WW_leps_theta[1]")        
        
        # Build the WW system using the two leptons not coming from the Z and the missing energy vector
        df = df.Define("missingEnergy_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(missingEnergy_vec, 0)")
        df = df.Define("WW_tlv", "missingEnergy_tlv + WW_leps_tlv0 + WW_leps_tlv1")
        df = df.Define("WW_theta", "WW_tlv.Theta()")
        df = df.Define("WW_phi", "WW_tlv.Phi()")
        df = df.Define("WW_mass", "WW_tlv.M()")
        df = df.Define("WW_p", "WW_tlv.P()")

        #########
        ### CUT 9: WW system mass window
        #########
        if is_loose:
            df = df.Filter("WW_mass > 60 && WW_mass < 135")
        else:
            df = df.Filter("WW_mass > 80 && WW_mass < 135")

        #########
        ### CUT 10: WW system momentum
        #########
        # df = df.Filter("WW_p > 25 && WW_p < 55")

        if doInference:
            tmva_helper = TMVAHelperXGB("../../../outputs/higgs/zh_hww_4l/mva/bdt_model_example.root", "bdt_model") # read the XGBoost training
            df = tmva_helper.run_inference(df, col_name="mva_score") # by default, makes a new column mva_score

        return df

    # define output branches to be saved
    def output():
        # branchList = [
        #     # electrons
        #     "electrons_p",
        #     "electrons_theta",
        #     "electrons_phi",
        #     "electrons_q",
        #     "electrons_no",
            
        #     # muons
        #     "muons_p",
        #     "muons_theta",
        #     "muons_phi",
        #     "muons_q",
        #     "muons_no",
            
        #     # zll
        #     "zll_m",
        #     "zll_p",
        #     "zll_recoil_m",
        #     "zll_leps_p",
        #     "zll_leps_p0_index",
        #     "zll_leps_p1_index",
            
        #     # WW leptons
        #     "WW_leps_p",
        #     "WW_leps_theta",
        #     "WW_leps_phi",
        #     "WW_leps_q",
        #     "WW_leps_no",
        #     "WW_leps_dR",
            
        #     # WW system
        #     "WW_mass",
        #     "WW_p",
        #     "WW_theta",
        #     "WW_phi",
            
        #     # missing energy
        #     "miss_cosTheta",
        #     "miss_energy",
            
        #     "ww_leptonic",
        # ]
        
        branchList = [
            # Z->ll system
            "zll_m",
            "zll_p",
            "zll_recoil_m",
            
            # Z->ll leptons 
            "zll_lep1_p",
            "zll_lep2_p",
            "zll_lep1_theta",
            "zll_lep2_theta",
            "Zll_leps_dR",
            
            # WW leptons
            "WW_lep1_p",
            "WW_lep2_p",
            "WW_lep1_theta",
            "WW_lep2_theta",
            "WW_leps_dR",
            
            # WW system
            "WW_mass",
            "WW_p",
            "WW_theta",
            "WW_phi",
            
            # missing energy
            "miss_cosTheta",
            "miss_energy",
        ]
        
        if doInference:
            branchList.append("mva_score")
            
        return branchList
