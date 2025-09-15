
# flavor = "mumu"
flavor = "ee"

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

if flavor == "mumu":
    processList = processList_mumu
    lepton_collection = "muons"
else:
    processList = processList_ee
    lepton_collection = "electrons"

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Additional/custom C++ functions, defined in header files
includePaths = ["functions.h"]

# Output directory
outputDir   = f"outputs/ntuples/{flavor}/"

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

        df = df.Define("ww_leptonic", "FCCAnalyses::ZHfunctions::is_ww_leptonic(Particle, Particle1)")
        # df = df.Filter("!ww_leptonic")

        # get all the leptons from the collection
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
        df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")

        # select leptons with momentum > 20 GeV
        df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons_all)")
        df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
        df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
        df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
        # df = df.Define(f"muons_iso", f"FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
        # df = df.Define(f"muons_is_iso", f"FCCAnalyses::ZHfunctions::get_iso(muons_iso, 0.25)") # 1 if isolated, 0 otherwise

        df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(electrons_all)")
        df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
        df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
        df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
        df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
        df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
        # df = df.Define(f"electrons_iso", f"FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
        # df = df.Define(f"electrons_is_iso", f"FCCAnalyses::ZHfunctions::get_iso(electrons_iso, 0.25)") # 1 if isolated, 0 otherwise

        # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
        df = df.Define(f"{lepton_collection}_iso", f"FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)({lepton_collection}, ReconstructedParticles)")
        df = df.Define(f"{lepton_collection}_sel_iso", f"FCCAnalyses::ZHfunctions::sel_iso(0.25)({lepton_collection}, {lepton_collection}_iso)")

        # Basic selection: at least 2 OS muons, one isolated
        df = df.Filter(f"{lepton_collection}_no >= 1 && {lepton_collection}_sel_iso.size() > 0")
        df = df.Filter(f"{lepton_collection}_no >= 2 && abs(Sum({lepton_collection}_q)) < {lepton_collection}_q.size()")

        # now we build the Z resonance based on the available leptons.
        # the function resonanceBuilder_mass_recoil returns the best lepton pair compatible with the Z mass (91.2 GeV) and recoil at 125 GeV
        # the argument 0.4 gives a weight to the Z mass and the recoil mass in the chi2 minimization
        # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index 1 and 2 the leptons of the pair
        df = df.Define("zbuilder_result", f"FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)({lepton_collection}, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
        df = df.Define("zll", "Vec_rp{zbuilder_result[0]}") # the Z
        df = df.Define(f"zll_{lepton_collection}", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}") # the leptons 
        df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]") # Z mass
        df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]") # momentum of the Z
        df = df.Define("zll_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zll)") # compute the recoil based on the reconstructed Z
        df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]") # recoil mass
        df = df.Define(f"zll_{lepton_collection}_p", f"FCCAnalyses::ReconstructedParticle::get_p(zll_{lepton_collection})") # get the momentum of the 2 muons from the Z resonance

        df = df.Define("missingEnergyVec", "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)")
        df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergyVec)")
        df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::get_missing_energy(missingEnergyVec)")
        

        return df

    # define output branches to be saved
    def output():
        branchList = [
            'muons_p', 'muons_theta', 'muons_phi', 'muons_q', 'muons_no',
            'electrons_p', 'electrons_theta', 'electrons_phi', 'electrons_q', 'electrons_no',
            'zll_m', 'zll_p', 'zll_recoil_m', f'zll_{lepton_collection}_p',
            'cosTheta_miss', 'missingEnergy', 
            'ww_leptonic',
        ]
        return branchList
