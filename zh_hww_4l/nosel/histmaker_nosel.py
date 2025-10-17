
flavor = "ee" # mumu, ee
# flavor = "mumu" # mumu, ee

# list of processes (mandatory)
processList_mumu = {
    # 'p8_ee_WW_ecm240':{'fraction': 0.01}, 
    # 'p8_ee_ZZ_ecm240':{'fraction': 0.01},
    'wzp6_ee_mumuH_HWW_ecm240':{'fraction': 1},
}

processList_ee = {
    # 'p8_ee_WW_ecm240':{'fraction': 0.01}, 
    # 'p8_ee_ZZ_ecm240':{'fraction': 0.01},
    'wzp6_ee_eeH_HWW_ecm240':{'fraction': 1},
}

if flavor == "mumu":
    processList = processList_mumu
    leps = 'muons'
else:
    processList = processList_ee
    leps = 'electrons'

processList = processList_mumu | processList_ee

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["../../functions.h"]

# Define the input dir (optional)
#inputDir    = "outputs/FCCee/higgs/mH-recoil/mumu/stage1"
#inputDir    = "localSamples/"

#Optional: output directory, default is local running directory
outputDir   = f"outputs_nosel/hists/"


# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 10800000.0 # 10.8 /ab for 240 GeV


# define some binning for various histograms
bins_p_mu = (250, 0, 250) # 100 MeV bins
bins_m_ll = (250, 0, 250) # 100 MeV bins
bins_p_ll = (250, 0, 250) # 100 MeV bins
bins_recoil = (250, 0, 250) # 1 GeV bins
bins_cosThetaMiss = (10000, 0, 1)

bins_theta = (500, -5, 5)
bins_eta = (600, -3, 3)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)

bins_recoil_final = (200, 120, 140) # 100 MeV bins


# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    # define collections
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

    # For signal events, keep only fully-leptonic WW decays (truth-level selection)
    if "wzp6_ee_eeH_HWW_ecm240" in dataset or "wzp6_ee_mumuH_HWW_ecm240" in dataset:
        df = df.Define("ww_leptonic", "FCCAnalyses::ZHfunctions::is_ww_leptonic(Particle, Particle1)")
        df = df.Filter("ww_leptonic")

    df = df.Define("missingEnergyVec", "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)")
    df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergyVec)")
    results.append(df.Histo1D(("cosThetaMiss", "", *bins_cosThetaMiss), "cosTheta_miss")) # plot it before the cut
    df = df.Define("missing_energy", "FCCAnalyses::ZHfunctions::get_missing_energy(missingEnergyVec)")
    results.append(df.Histo1D(("missing_energy", "", *bins_p_mu), "missing_energy")) # plot it before the cut

    return results, weightsum

