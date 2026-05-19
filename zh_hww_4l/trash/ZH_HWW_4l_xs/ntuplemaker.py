
# flavor = "mumu"
# flavor = "ee"

# list of processes (mandatory)
processList_mumu = {
    # 'p8_ee_ZZ_ecm240':{'fraction': 1},
    # 'p8_ee_WW_ecm240':{'fraction': 1}, 
    'wzp6_ee_mumuH_HWW_ecm240':{'fraction': 1},
}

processList_ee = {
    # 'p8_ee_ZZ_ecm240':{'fraction': 1},
    # 'p8_ee_WW_ecm240':{'fraction': 1}, 
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
#runBatch    = False
#batchQueue  = "longlunch"
#compGroup = "group_u_FCC.local_gen"

class RDFanalysis():

    # encapsulate analysis logic, definitions and filters in the dataframe
    def analysers(df):

        # define some aliases to be used later on
        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
        df = df.Alias("Muon0", "Muon#0.index")
        df = df.Alias("Electron0", "Electron#0.index")

        # keep only events where the Higgs decays to leptonic WW*
        df = df.Define("ww_leptonic", "FCCAnalyses::ZHfunctions::is_ww_leptonic(Particle, Particle1)")
        df = df.Filter("!ww_leptonic")

        # get all the leptons from the collection
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
        df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")

        # select leptons with momentum > 20 GeV
        df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
        df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons_all)")
        df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons_all)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons_all)")
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons_all)")
        df = df.Define(f"muons_iso", f"FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons_all, ReconstructedParticles)")
        df = df.Define(f"muons_is_iso", f"FCCAnalyses::ZHfunctions::get_iso(muons_iso, 0.25)") # 1 if isolated, 0 otherwise

        df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
        df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons_all)")
        df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons_all)")
        df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons_all)")
        df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons_all)")
        df = df.Define(f"electrons_iso", f"FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons_all, ReconstructedParticles)")
        df = df.Define(f"electrons_is_iso", f"FCCAnalyses::ZHfunctions::get_iso(electrons_iso, 0.25)") # 1 if isolated, 0 otherwise

        df = df.Define("missingEnergyVec", "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)")
        df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergyVec)")
        df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::get_missing_energy(missingEnergyVec)")
        

        return df

    # define output branches to be saved
    def output():
        branchList = [
            'muons_p', 'muons_theta', 'muons_phi', 'muons_q', 'muons_no', 'muons_is_iso',
            'electrons_p', 'electrons_theta', 'electrons_phi', 'electrons_q', 'electrons_no', 'electrons_is_iso',
            'cosTheta_miss', 'missingEnergy', 
        ]
        return branchList
