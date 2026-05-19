
# list of processes (mandatory)
processList_mumu = {
    # 'p8_ee_ZZ_ecm240':{'fraction': 1, 'chunks': 10},
    # 'p8_ee_WW_ecm240':{'fraction': 1, 'chunks': 10}, 
    'wzp6_ee_mumuH_HWW_ecm240':{'fraction': 1},
}

processList_ee = {
    # 'p8_ee_ZZ_ecm240':{'fraction': 1, 'chunks': 10},
    # 'p8_ee_WW_ecm240':{'fraction': 1, 'chunks': 10}, 
    'wzp6_ee_eeH_HWW_ecm240':{'fraction': 1},
}

processList = processList_mumu | processList_ee

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Additional/custom C++ functions, defined in header files
includePaths = ["../functions.h"]

# Output directory
outputDir   = f"outputs/ntuples/"

# Multithreading: -1 means using all cores
nCPUS       = -1

# Batch settings
runBatch    = True
#batchQueue  = "longlunch"
#compGroup = "group_u_FCC.local_gen"

class RDFanalysis():

    # encapsulate analysis logic, definitions and filters in the dataframe
    def analysers(df):

        # define collections
        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

        # Flag fully-leptonic WW events.
        # This is a truth-level selection - this should be applied on signal samples only!
        df = df.Define("ww_leptonic", "FCCAnalyses::ZHfunctions::is_ww_leptonic(Particle, Particle1)")  
        # df = df.Filter("!ww_leptonic")

        # define muons
        df = df.Alias("Muon0", "Muon#0.index")
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
        df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
        
        df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(10)(muons_all)")
        df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
        df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
        df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
        df = df.Define(f"muons_iso", f"FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
        df = df.Define(f"muons_is_iso", f"FCCAnalyses::ZHfunctions::get_iso(muons_iso, 0.25)") # 1 if isolated, 0 otherwise

        # define electrons
        df = df.Alias("Electron0", "Electron#0.index")
        df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
        df = df.Define("electrons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
        
        df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(electrons_all)")
        df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
        df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
        df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
        df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
        df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
        df = df.Define(f"electrons_iso", f"FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
        df = df.Define(f"electrons_is_iso", f"FCCAnalyses::ZHfunctions::get_iso(electrons_iso, 0.25)") # 1 if isolated, 0 otherwise

        # calculate event variables
        df = df.Define("missingEnergyVec", "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)")
        df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergyVec)")
        df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::get_missing_energy(missingEnergyVec)")
        

        return df

    # define output branches to be saved
    def output():
        branchList = [
            'ww_leptonic',
            'muons_all_p', 'muons_p', 'muons_theta', 'muons_phi', 'muons_q', 'muons_no', 'muons_is_iso', 
            'electrons_all_p', 'electrons_p', 'electrons_theta', 'electrons_phi', 'electrons_q', 'electrons_no', 'electrons_is_iso', 
            # 'zll_m', 'zll_p', 'zll_recoil_m', f'zll_{lepton_collection}_p',
            'cosTheta_miss', 'missingEnergy', 
        ]
        return branchList
